from pymongo import AsyncMongoClient
from app.config import settings
from loguru import logger


client: AsyncMongoClient = None


async def connect_to_mongo():
    """Create database connection"""
    global client, database
    try:
        # For MongoDB Atlas, ensure SSL/TLS is properly configured
        # Motor automatically uses TLS for mongodb+srv:// connections
        # The connection string should already include SSL parameters
        client = AsyncMongoClient(
            settings.MONGO_URL,
            serverSelectionTimeoutMS=30000,  # 30 seconds timeout
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            # TLS is automatically enabled for mongodb+srv:// connections
            # System CA certificates (installed via ca-certificates package) will be used
        )
        database = client[settings.DB_NAME]
        # Test connection
        await client.admin.command('ping')
        logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        # AsyncMongoClient.close() is a coroutine in recent versions,
        # so ensure we await it to avoid the RuntimeWarning observed when
        # running the module directly.
        await client.close()
        logger.info("✅ MongoDB connection closed")




def get_database():
    """Get database instance.

    Callers should ensure `connect_to_mongo` has been awaited first (e.g. via
    startup event in FastAPI). The module-level `database` variable is
    populated by that coroutine.
    """
    try:
        return database
    except NameError:
        raise RuntimeError("Database not initialized; call connect_to_mongo() first")


if __name__ == "__main__":
    # running the module directly for testing/connectivity
    import asyncio

    async def _main():
        await connect_to_mongo()
        await close_mongo_connection()

    asyncio.run(_main())
