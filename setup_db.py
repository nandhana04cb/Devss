from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
DATABASE_URL = "sqlite:///kalavara.db"

# Create SQLAlchemy engine and base
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the tables
class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    dish_name = Column(String(100), nullable=False)

class AdminView(Base):
    __tablename__ = 'admin_view'
    id = Column(Integer, primary_key=True)
    total_dishes = Column(Integer, default=0)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Create tables and initialize the database
def setup_database():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert initial admin view data if not already present
    if not session.query(AdminView).filter_by(id=1).first():
        admin_entry = AdminView(id=1, total_dishes=0)
        session.add(admin_entry)
        session.commit()

    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
