import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from dotenv import load_dotenv

load_dotenv()


# URL de SQLite para dev
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# Si usas PostgreSQL en el futuro sería:
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost:5432/nomascartera"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Solo necesario en SQLite
# )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # OJO: aquí ya NO usamos connect_args={"check_same_thread": False}
    # eso es solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para inyectar la sesión en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
