"""Module for running Web Server"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def api_test():
    """Function for API Test"""
    return "Hello World"
