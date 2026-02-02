import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from google.cloud.sql.connector import Connector, IPTypes

# Define the ORM Base
Base = declarative_base()

class ServiceHistory(Base):
    __tablename__ = 'service_history'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    action_type = Column(String(100), nullable=False) # e.g., "Outline Generation", "Draft Chapter 1"
    status = Column(String(50), nullable=False)       # e.g., "Success", "Failed"
    details = Column(Text, nullable=True)             # Short summary or result link
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def get_db_connection():
    """
    Establishes a connection to Cloud SQL (PostgreSQL) using the Python Connector.
    Falls back to SQLite for local development if Cloud SQL env vars are missing.
    """
    instance_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")

    # If Cloud SQL config is present, use it
    if instance_connection_name and db_user:
        connector = Connector()
        
        def getconn():
            conn = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
                ip_type=IPTypes.PUBLIC
            )
            return conn

        engine = create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
    else:
        # Fallback to local SQLite
        print("⚠️ Cloud SQL config missing. Using local SQLite database.")
        engine = create_engine('sqlite:///local_thesis_ai.db', echo=False)

    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def add_history_entry(username, action, status, details=""):
    session = get_db_connection()
    try:
        new_entry = ServiceHistory(
            username=username,
            action_type=action,
            status=status,
            details=details
        )
        session.add(new_entry)
        session.commit()
    except Exception as e:
        print(f"Error logging history: {e}")
    finally:
        session.close()

def get_user_history(username):
    session = get_db_connection()
    try:
        history = session.query(ServiceHistory).filter_by(username=username).order_by(ServiceHistory.timestamp.desc()).all()
        # Convert to list of lists for Gradio Dataframe
        data = [[h.timestamp.strftime("%Y-%m-%d %H:%M"), h.action_type, h.status, h.details] for h in history]
        return data
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []
    finally:
        session.close()
