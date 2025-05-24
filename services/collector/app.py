from fastapi import FastAPI
import asyncio
from services.collector.scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_scheduler())

@app.get("/health")
async def health_check():
    return {"status": "ok"}
