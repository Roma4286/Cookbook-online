from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    name: str
    age: int


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/submit/")
async def submit(item: Item):
    response = {"message": f"Привет, {item.name}! Твой возраст: {item.age}"}
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
