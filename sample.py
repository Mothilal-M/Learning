import logging

from fastapi import FastAPI
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app.
app = FastAPI()


class SumRequest(BaseModel):
    """Two numbers to add."""

    num1: float
    num2: float


@app.get("/")
def read_root():
    logger.info("Health check endpoint called")
    return {"message": "Welcome to the FastAPI app!"}


@app.post("/sum")
def calculate_sum(request: SumRequest):
    result = request.num1 + request.num2
    logger.info("The sum of %s and %s is %s", request.num1, request.num2, result)
    return {"num1": request.num1, "num2": request.num2, "sum": result}


# Run with: uvicorn sample:app --reload
