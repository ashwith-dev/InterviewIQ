from fastapi import FastAPI
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(title="InterviewIQ API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to InterviewIQ API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
