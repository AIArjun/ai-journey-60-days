from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends
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