import os
import asyncpg
from dotenv import load_dotenv
from logger import logger

load_dotenv()

class Database:
    def __init__(self):
        self.conn = None

    async def connect(self):
        try:
            self.conn = await asyncpg.connect(
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                database=os.getenv('POSTGRES_DB'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT')
            )
            logger.info("Successfully connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise

    async def close(self):
        if self.conn:
            await self.conn.close()
            logger.info("Closed PostgreSQL connection")

    async def create_user(self, user_id: int, language: str = None):
        try:
            await self.conn.execute(
                "INSERT INTO users (user_id, language) VALUES ($1, $2) ON CONFLICT (user_id) DO NOTHING",
                user_id, language
            )
            logger.info(f"Created/checked user {user_id}")
        except Exception as e:
            logger.error(f"Error creating user {user_id}: {e}")

    async def update_user_language(self, user_id: int, language: str):
        try:
            await self.conn.execute(
                "UPDATE users SET language = $1 WHERE user_id = $2",
                language, user_id
            )
            logger.info(f"Updated language for user {user_id} to {language}")
        except Exception as e:
            logger.error(f"Error updating language for user {user_id}: {e}")

    async def update_user_birth_date(self, user_id: int, birth_date):
        try:
            await self.conn.execute(
                "UPDATE users SET birth_date = $1 WHERE user_id = $2",
                birth_date, user_id
            )
            logger.info(f"Updated birth date for user {user_id} to {birth_date}")
        except Exception as e:
            logger.error(f"Error updating birth date for user {user_id}: {e}")

    async def get_user(self, user_id: int):
        try:
            user = await self.conn.fetchrow(
                "SELECT * FROM users WHERE user_id = $1",
                user_id
            )
            if user:
                logger.info(f"Retrieved user {user_id} from database")
            else:
                logger.info(f"User {user_id} not found in database")
            return user
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

db = Database()