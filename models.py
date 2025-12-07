from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///liga.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ---------------------
# TABLA USUARIOS (LOGIN)
# ---------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    club = Column(String)

# -------------------------
# TABLA PAREJAS
# -------------------------
class Pareja(Base):
    __tablename__ = "parejas"
    id = Column(Integer, primary_key=True)
    jugador1 = Column(String)
    jugador2 = Column(String)
    categoria = Column(String)

# -------------------------
# TABLA FIXTURE
# -------------------------
class Fixture(Base):
    __tablename__ = "fixture"
    id = Column(Integer, primary_key=True)
    pareja_a = Column(String)
    pareja_b = Column(String)
    fecha = Column(String)
    categoria = Column(String)

# -------------------------
# TABLA RESULTADOS
# -------------------------
class Resultado(Base):
    __tablename__ = "resultados"
    id = Column(Integer, primary_key=True)
    partido_id = Column(Integer)
    ganador = Column(String)
    set1 = Column(String)
    set2 = Column(String)
    set3 = Column(String)

# -------------------------
# TABLA POSICIONES
# -------------------------
class Posicion(Base):
    __tablename__ = "posiciones"
    id = Column(Integer, primary_key=True)
    pareja = Column(String)
    puntos = Column(Integer)
    categoria = Column(String)

# -------------------------
# TABLA LLAVES
# -------------------------
class Llave(Base):
    __tablename__ = "llaves"
    id = Column(Integer, primary_key=True)
    ronda = Column(String)
    pareja = Column(String)
    categoria = Column(String)

# CREAR TABLAS AUTOMÁTICAMENTE
def init_db():
    Base.metadata.create_all(engine)

