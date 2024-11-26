from fastapi import APIRouter

router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

@router.get("/")
async def main(name: str):
    return {'name': name}