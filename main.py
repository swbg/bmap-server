import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://kurze-durststrecke.de",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=[],
)

con = sqlite3.connect("./data/main.db")


@app.get("/entries")
async def get_entries():
    return {}


@app.get("/entries/{place_id}")
async def get_entries_by_place_id(place_id):
    return {"place_id": place_id}


@app.get("/places")
async def get_places():
    return {}


@app.get("/place/{place_id}")
async def get_place(place_id):
    return {"place_id": place_id}


@app.get("/products")
async def get_products():
    cur = con.cursor()
    res = cur.execute("SELECT * FROM products")
    return {"data": res.fetchall()}
