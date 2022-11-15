from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the home route"}


@app.get("/httpx")
async def httpx_test():
    async with AsyncClient(base_url="https://httpbin.org") as ac:
        response = await ac.get("/get")
    # alt: response = await AsyncClient().get("https://httpbin.org/get")
    return response.json()
