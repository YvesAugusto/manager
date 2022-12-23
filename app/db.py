import os

import motor.motor_asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.db")

# load_dotenv(env_path)

CONNECTION_STRING = 'mongodb://{}:{}@{}:{}/{}?authSource=admin'
CONNECTION_STRING = CONNECTION_STRING.format(
    os.getenv('MONGODB_USERNAME'), os.getenv('MONGODB_PASSWORD'), os.getenv('MONGODB_HOSTNAME'),
    os.getenv("MONGODB_PORT"), os.getenv('MONGODB_DATABASE')
)

def get_client():
    client = AsyncIOMotorClient(CONNECTION_STRING)
    return client
    
def close_client(client):
    client.close()
