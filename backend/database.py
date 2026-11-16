from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for obtaining a SQLAlchemy DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create tables and apply incremental schema changes if needed."""
    Base.metadata.create_all(bind=engine)
    if DATABASE_URL.startswith("sqlite"):
        with engine.connect() as conn:
            # Auto-migrate user_id in user_profiles
            try:
                res = conn.execute(text("PRAGMA table_info(user_profiles)"))
                columns = [r[1] for r in res.fetchall()]
                if columns and "user_id" not in columns:
                    conn.execute(text("ALTER TABLE user_profiles ADD COLUMN user_id INTEGER"))
                    conn.commit()
            except Exception:
                pass
            
            # Auto-migrate user_id in chat_history
            try:
                res = conn.execute(text("PRAGMA table_info(chat_history)"))
                columns = [r[1] for r in res.fetchall()]
                if columns and "user_id" not in columns:
                    conn.execute(text("ALTER TABLE chat_history ADD COLUMN user_id INTEGER"))
                    conn.commit()
            except Exception:
                pass
