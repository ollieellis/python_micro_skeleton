from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel
from pydantic_yaml import YamlModel


class payload(BaseModel):  # start working with the xml jaki sent over asap!!
    string: str
    intiger: int

class config(YamlModel):
    mockMode: bool
    debugMode: bool

#as app grows change globals to be a class
def constructPayload(string: str, intiger: int) -> str:
    """dummy func to ensure get function cleanyness"""
    return "endpoint called with payload: " + string + " " + intiger


def startUp():
    """called on app start up"""
    global cfg # global so dont have to read on api calls
    cfg = config.parse_file("config/config.yaml")
    return


def shutDown():
    """called on app shut down"""
    logger.info("app gracefully shutting down")
    return


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle the startUp/shutDown of app (pre/post *yield* keyword)"""
    try:
        startUp()
        logger.info("app started with config: " + str(cfg))
    except Exception as e:
        logger.critical("failed to start up app", print(str(e)))
        exit()
    yield
    shutDown()


app = FastAPI(lifespan=lifespan)


@app.get("/endpoint")
def endpoint(payload: payload):
    if cfg.mockMode:
        return {"message": "mock_mode enabled"}  
    else:
        responce = constructPayload(payload.string, payload.intiger)
        return {"message": responce}


# these probes are actually quite powerful and should look into better utilising them
@app.get("/liveness")
def liveness():
    """kubernetes livenss probe"""
    return {"status": "ok"}


@app.get("/readiness")
def readiness():
    """kubernetes readyness probe"""
    return {"status": "ok"}