from fastapi import FastAPI

APP_NAME = "E-commerce Backend"

APP_DESCRIPTION = "Production-ready e-commerce backend built with FastAPI."

APP_VERSION = "1.0.0"

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

@app.get("/")
def home():
    return {
        "message" : "Welcome to the E-Commerce Backend API"
    }

@app.get("/health")
def health():
    return {
        "status" : "healthy"
    }

@app.get("/version")
def get_version():
    return {
        "version" : APP_VERSION
    }