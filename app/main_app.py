from fastapi import FastAPI
from app.routes import openai as openai_routes

app = FastAPI()
app.include_router(openai_routes.router)

# health
@app.get('/health')
def health():
    return {"status": "ok"}
