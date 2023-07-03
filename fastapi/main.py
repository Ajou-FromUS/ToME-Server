from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def api_test():
    return "Hello World"