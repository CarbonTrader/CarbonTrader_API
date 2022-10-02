from fastapi import Depends, FastAPI
from .routes import BlockchainProvider, CreditProvider, ProjectProvider, UserProvider, TransactionsProvider, Test
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
import firebase_admin


class Settings(BaseSettings):
    CREDENTIALS_PATH= "app/secrets/credentials.json"
    DB_URL = "https://carbontrader-1111-default-rtdb.firebaseio.com/"


settings = Settings()

cred_obj = firebase_admin.credentials.Certificate(settings.CREDENTIALS_PATH)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': settings.DB_URL
})
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(CreditProvider.router)
app.include_router(ProjectProvider.router)
app.include_router(UserProvider.router)
app.include_router(TransactionsProvider.router)
app.include_router(BlockchainProvider.router)
app.include_router(Test.router)
