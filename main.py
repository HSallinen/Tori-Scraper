from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from scraper import toriScraper
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    product: str
    priceMin: int
    priceMax: int
    city: str
    distance: int
    email: str
    data: list


@app.put("/backend/")
async def returnSearch(item: Item):
    item.data=toriScraper(item.product, item.priceMin, item.priceMax, item.distance, item.city, 0)

    return(item)


@app.get("/")
async def root():
    return FileResponse("frontend/dist/index.html")

@app.exception_handler(404)
async def exception_404_handler(request, exc):
    return FileResponse("frontend/dist/index.html")
app.mount("/", StaticFiles(directory="frontend/dist/"), name="ui")