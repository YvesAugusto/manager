from ..db import AsyncIOMotorClient
from ..models.drone import Drone, DroneUpdate

def registro_helper(registro) -> dict:
    return {
        'doca_id': registro['drone_id'],
        'camera_uri': registro['camera_uri']
    }

async def query_registro(client: AsyncIOMotorClient, drone_id: int):
    registro = await client.drones.get_collection('drones').find_one({'drone_id': drone_id})
    return registro

async def delete_registro(client: AsyncIOMotorClient, drone_id: int):
    registro = await client.drones.get_collection('drones').delete_many({'drone_id': drone_id})
    return registro

async def insert_registro_common(client: AsyncIOMotorClient, drone: Drone):
    registro = await client.drones.get_collection('drones').insert_one(drone.dict())
    if registro:
        return True
    return False

async def update_registro_common(client: AsyncIOMotorClient, drone_id: int, drone: DroneUpdate):
    up = await client.drones.get_collection('drones').update_one(
        {'drone_id': drone_id}, {'$set': drone.dict()}
    )
    return up