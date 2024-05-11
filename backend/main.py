from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root(text: str):
    return {"message": text}