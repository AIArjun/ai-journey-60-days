from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tony Stark", age=48)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()
    print("Heroes saved!")

def select_heroes():
    with Session(engine) as session:

        statement = select(Hero)
        
        results = session.exec(statement)
        
        print("\n--- Reading from Database ---")
        for hero in results:
            print(f"Hero ID: {hero.id} | Name: {hero.name} | Age: {hero.age}")

if __name__ == "__main__":
    create_db_and_tables()
    select_heroes()