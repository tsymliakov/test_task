from fastapi import FastAPI
from api import docs

app = FastAPI()
app.include_router(docs.docs_router)
