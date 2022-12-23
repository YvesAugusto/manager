from fastapi import APIRouter, Path, Depends, Body
from ..db import get_client, close_client, AsyncIOMotorClient
from ..controllers import subscribe
from ..models.drone import Drone, DroneUpdate

router = APIRouter(prefix='/subscribe', tags=['Dev Tools'])

@router.get('/get/{drone_id}')
async def get_registro_nota(
    client: AsyncIOMotorClient = Depends(get_client), 
    drone_id: int = Path(ge=1)
):
    response = await subscribe.get_registro(client, drone_id)
    close_client(client)
    return response

@router.post('/insert')
async def inserir_registro_nota(
    client: AsyncIOMotorClient = Depends(get_client),
    drone: Drone = Body()
):
    response = await subscribe.inserir_registro(client, drone)
    close_client(client)
    return response

@router.put('/update/{drone_id}')
async def delete_registro_nota(
    client: AsyncIOMotorClient = Depends(get_client), 
    drone_id: int = Path(ge=1), 
    drone: DroneUpdate = Body(),
):
    response = await subscribe.update_registro(client, drone_id, drone)
    close_client(client)
    return response

@router.delete('/delete/{drone_id}')
async def delete_registro_nota(
    client: AsyncIOMotorClient = Depends(get_client), 
    drone_id: int = Path(ge=1),
):
    response = await subscribe.apagar_registro(client, drone_id)
    close_client(client)
    return response

@router.get('/list')
async def lista_registro_nota(
    client: AsyncIOMotorClient = Depends(get_client),
):
    response = await subscribe.listar_registros(client)
    close_client(client)
    return response