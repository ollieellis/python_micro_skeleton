from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel
from pydantic_yaml import YamlModel


class Payload(BaseModel):
    """mocks the payloads to your endpoints to control the typing of the incoming json objects"""

    string: str
    integer: int


class Config(YamlModel):
    """Allows easy config of the app via a yaml file: see start_up()"""

    mockMode: bool
    debugMode: bool


class MyApp:
    def __init__(self, config_file: str = "config/config.yaml"):
        self.config = Config.parse_file(config_file)
        self.router = APIRouter()
        self.router.add_api_route("/endpoint", self.endpoint, methods=["POST"])
        self.router.add_api_route("/liveness", self.liveness, methods=["GET"])
        self.router.add_api_route("/readiness", self.liveness, methods=["GET"])

    def endpoint(self, payload: Payload):
        print(payload)
        if self.config.mockMode:
            return {"message": "mock_mode enabled"}
        else:
            response = self.construct_payload(payload.string, payload.integer)
            return {"message": response}

    @staticmethod
    def construct_payload(string: str, integer: int) -> str:
        """dummy func to ensure get function cleanliness"""
        return f"endpoint called with payload: {string} {integer}"

    def build_app(self):
        return FastAPI(lifespan=self.lifespan)

    @asynccontextmanager
    async def lifespan(self, __app: FastAPI):
        """Handle the start_up/shut_down of app (pre/post *yield* keyword)"""
        try:
            self.start_up()
            __app.include_router(self.router)
            logger.info("app started with config: " + str(self.config))
        except Exception as e:
            logger.critical("failed to start up app: " + str(e))
            exit()
        yield
        self.shut_down()

    def start_up(self):
        """called on app start up"""
        self.config = Config.parse_file("config/config.yaml")
        # self.app.include_router(self.router)

    def shut_down(self):
        """called on app shut down"""
        logger.info("app gracefully shutting down")

    def liveness(self):
        """kubernetes liveliness probe"""
        return {"status": "ok"}

    def readiness(self):
        """kubernetes readiness probe"""
        return {"status": "ok"}


# uvicorn looks for a fastApi object called app in main.py
# uvicorn main:app
my_app = MyApp("config/config.yaml")
app = my_app.build_app()
