from fastapi import FastAPI
import uvicorn


app = FastAPI()










@app.get("/predict")
async def predict(vector: str):
    print(vector)
