import logging

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import  async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

logger = logging.getLogger(__name__)

# sync URL: Alembic, and routes not yet converted
Database_URL = (
    f"postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

# async URL: same database, async driver
ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_engine(Database_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)

Base = declarative_base()


async def connect_database():
    try:
        async with async_engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        logger.exception("database connection FAILED")
        raise
    logger.info("database connection OK")


def get_db():
    db = SessionLocal()
    logger.debug("db session opened")
    try:
        yield db
    finally:
        db.close()
        logger.debug("db session closed")


async def get_async_db():
    async with AsyncSessionLocal() as db:
        logger.debug("async db session opened")
        try:
            yield db
        finally: 
            logger.debug("async db session closed")

# DATABASE_HOSTNAME=localhost
# DATABASE_PORT=5432
# DATABASE_NAME=faastapi
# DATABASE_USERNAME=postgres
# DATABASE_PASSWORD=2233





# while True:
#     try:
#         connect = psycopg2.connect(
#             host="localhost",
#             database="faastapi",
#             user="postgres",
#             password=2233,
#             cursor_factory=RealDictCursor,
#         )
#         curser = connect.cursor()
#         print("success")
#         break
#     except Exception as error:
#         print("fail")
#         print("error", error)
#         time.sleep(2)



