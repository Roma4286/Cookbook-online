from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.database import Base, engine
from server.custom_openapi import setup_custom_openapi
from server.auth.router import router as router_auth
from server.auth.router import router_token as router_token

app = FastAPI(title='Shop', swagger_ui_parameters={'defaultModelsExpandDepth': -1, "tryItOutEnabled": True})

Base.metadata.create_all(bind=engine)

app.include_router(router_auth)
app.include_router(router_token)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

setup_custom_openapi(app)
