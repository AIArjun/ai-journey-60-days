from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException  # <--- Added HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- PART 1: DATABASE SETUP ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# --- PART 2: THE MODEL ---
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

# --- PART 3: LIFECYCLE ---
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# --- PART 4: THE APP ---
app = FastAPI(lifespan=lifespan)

# --- NEW: THE BUTLER (DEPENDENCY) ---
def get_session():
    with Session(engine) as session:
        yield session
        # Session closes automatically here

# --- STEP 4: CREATE (POST) ---
@app.post("/heroes/")
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# --- STEP 5: READ (GET) ---
@app.get("/heroes/")
def read_heroes(session: Session = Depends(get_session)):
    statement = select(Hero)
    heroes = session.exec(statement).all()
    return heroes

# --- ROOT (Home Page) ---
@app.get("/")  # <--- FIXED: Added the missing decorator!
def root():
    return {"message": "Welcome to the Hero API (Day 7)", "db_status": "Connected"}

# --- DAY 8: UPDATE (PUT) ---
@app.put("/heroes/{hero_id}")
def update_hero(hero_id: int, hero_data: Hero, session: Session = Depends(get_session)):
    # 1. FIND: Get the hero from the DB
    hero_db = session.get(Hero, hero_id)
    
    # 2. CHECK: If hero doesn't exist, stop!
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # 3. MODIFY: Update the fields
    hero_db.name = hero_data.name
    hero_db.secret_name = hero_data.secret_name
    hero_db.age = hero_data.age
    
    # 4. COMMIT: Save to disk
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    
    return hero_db