from typing import Union

from fastapi import Depends, FastAPI
from .routes import CreditProvider, ProjectProvider, UserProvider, TransactionsProvider
from fastapi.middleware.cors import CORSMiddleware


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

