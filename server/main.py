from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from custom_openapi import setup_custom_openapi
from auth.router import router as router_auth
from auth.router import router_token as router_token
from account.router import router as router_account

app = FastAPI(title='Shop', swagger_ui_parameters={'defaultModelsExpandDepth': -1, "tryItOutEnabled": True})

Base.metadata.create_all(bind=engine)

app.include_router(router_token)
app.include_router(router_auth)
app.include_router(router_account)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

setup_custom_openapi(app)
