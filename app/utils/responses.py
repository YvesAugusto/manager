from fastapi.responses import JSONResponse


async def capture_success_wait_response(lectures: list[dict]):
    return JSONResponse(
        content={
            "message": "Captura em andamento",
            "data": lectures,
            "error": False
        },
        status_code=200
    )

async def camera_not_enrolled(camera_id: int):
    return JSONResponse(
            content={
                "message": "Camera {} não registrada".format(camera_id),
                "error": True
            },
            status_code=404
    )

async def camera_not_connected(camera_id: int):
    return JSONResponse(
            content={
                "message": "Não há conexão entre a câmera {} e o servidor central".format(camera_id),
                "error": True
            },
            status_code=404
    )
