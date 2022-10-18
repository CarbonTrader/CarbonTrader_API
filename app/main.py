from fastapi import Depends, FastAPI
from firebase_admin import firestore
from app.routes import RecoveryProvider
from .routes import BlockchainProvider, CreditProvider, ProjectProvider, UserProvider, TransactionsProvider, Test,AuthProvider
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthProvider.router)
app.include_router(CreditProvider.router)
app.include_router(ProjectProvider.router)
app.include_router(UserProvider.router)
app.include_router(TransactionsProvider.router)
app.include_router(BlockchainProvider.router)
app.include_router(RecoveryProvider.router)
app.include_router(Test.router)
