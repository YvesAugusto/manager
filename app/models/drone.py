from pydantic import BaseModel

class Drone(BaseModel):

    camera_uri: str
    drone_id: int

class DroneUpdate(BaseModel):

    camera_uri: str