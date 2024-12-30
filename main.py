from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app_api = FastAPI()

app.mount("/api", app_api)
app.mount("/", StaticFiles(directory="public", html=True), name="public")


@app_api.get("/items/")
def get_items():
    items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    return items
