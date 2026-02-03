import os
import datetime
import shutil
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from google.cloud.sql.connector import Connector, IPTypes

# Define the ORM Base
Base = declarative_base()

class ServiceHistory(Base):
    __tablename__ = 'service_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    action_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Global Session Maker
SessionLocal = None

def init_db():
    global SessionLocal
    
    instance_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    
    # Check if we assume Cloud SQL
    use_cloud_sql = bool(instance_connection_name and "thesis-ai-generator" in str(instance_connection_name))

    engine = None
    if use_cloud_sql:
        try:
            print(f"🔄 Connecting to Cloud SQL: {instance_connection_name}")
            connector = Connector()
            def getconn():
                conn = connector.connect(
                    instance_connection_name,
                    "pg8000",
                    user=db_user,
                    password=db_pass,
                    db=os.getenv("DB_NAME", "postgres"),
                    ip_type=IPTypes.PUBLIC
                )
                return conn
            
            engine = create_engine("postgresql+pg8000://", creator=getconn)
            print("✅ Cloud SQL Connected.")
        except Exception as e:
            print(f"⚠️ Cloud SQL Connection Failed: {e}. Falling back to SQLite.")
            use_cloud_sql = False

    if not use_cloud_sql or engine is None:
        print("ℹ️ Using Local SQLite Database (history.db)")
        engine = create_engine('sqlite:///history.db', echo=False, connect_args={"check_same_thread": False})

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db_session():
    if SessionLocal is None:
        init_db()
    return SessionLocal()

def add_history_entry(username, action, status, details=""):
    session = get_db_session()
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
        print(f"❌ DB Log Error: {e}")
        session.rollback()
    finally:
        session.close()

def get_user_history(username):
    session = get_db_session()
    try:
        if not username: return []
        history = session.query(ServiceHistory).filter_by(username=username).order_by(ServiceHistory.timestamp.desc()).limit(50).all()
        return [[h.timestamp.strftime("%Y-%m-%d %H:%M"), h.action_type, h.status, h.details] for h in history]
    except Exception as e:
        print(f"❌ DB Fetch Error: {e}")
        return []
    finally:
        session.close()

# Initialize immediately to fail fast if issues
try:
    init_db()
except Exception as e:
    print(f"CRITICAL DB INIT FAILURE: {e}")
