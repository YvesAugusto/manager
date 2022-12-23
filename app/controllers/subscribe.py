import pydantic
from fastapi.responses import JSONResponse

from ..controllers.help import (delete_registro, insert_registro_common,
                                query_registro, registro_helper,
                                update_registro_common)
from ..db import AsyncIOMotorClient
from ..models.drone import Drone, DroneUpdate

async def get_registro(client: AsyncIOMotorClient, drone_id: int):
    registro = await query_registro(client, drone_id)
    if registro:
        return JSONResponse(content={"error": False, "data": registro_helper(registro)}, status_code=200)
    return JSONResponse(content={"message": "Registro não encontrado", "error": True, "data": {}}, status_code=404)
    
async def inserir_registro(client: AsyncIOMotorClient, drone: Drone):
    registro = await query_registro(client, drone.drone_id)
    if registro:
        return JSONResponse(content={"message": "Registro já existe", "error": True, "data": {}}, status_code=406)
    valid = await insert_registro_common(client, drone)
    if not valid:
        return JSONResponse(content={"message": "Não foi possível registrar", "error": True, "data": {}}, status_code=422)
    return JSONResponse(content={"message": "Registro cadastrado com sucesso", "error": False, "data": registro_helper(drone.dict())}, status_code=200)

async def update_registro(client: AsyncIOMotorClient, drone_id: int, drone: DroneUpdate):
    registro = await query_registro(client, drone_id)
    if not registro:
        return JSONResponse(content={"message": "Registro não encontrado", "error": True, "data": {}}, status_code=404)
    updated_registro = await update_registro_common(client, drone_id, drone)
    if not updated_registro:
        return JSONResponse(content={"message": "Não foi possível atualizar registro", "error": True, "data": {}}, status_code=422)
    updated_registro = drone.dict()
    updated_registro['drone_id'] = drone_id
    return JSONResponse(content={"message": "Registro atualizado com sucesso", "error": False, "data": registro_helper(updated_registro)}, status_code=200)

async def apagar_registro(client: AsyncIOMotorClient, drone_id: int):
    registro = await query_registro(client, drone_id)
    if not registro:
        return JSONResponse(content={"message": "Registro não encontrado", "error": True, "data": {}}, status_code=404)
    deleted = await delete_registro(client, drone_id)
    if not deleted:
        return JSONResponse(content={"message": "Não foi possível apagar registro", "error": True, "data": {}}, status_code=422)
    return JSONResponse(content={"message": "Registro apagado com sucesso", "error": False, "data": registro_helper(registro)}, status_code=200)

async def listar_registros(client: AsyncIOMotorClient):
    registros = []
    async for registro in client.drones.get_collection('drones').find():
        del registro['_id']
        registros.append(registro_helper(registro))
    return JSONResponse(content={"error": False, "data": registros}, status_code=200)
