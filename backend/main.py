from fastapi import FastAPI
from routes.analytics import router as analytics_router
from routes.mining import router as mining_router
from routes.prediction import router as prediction_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SmartCanteen API")

#CORSMiddleware -> allows frontend <-> backend communication.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://canteen-analysis-and-recommendatio.onrender.com/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SmartCanteen API is running"}

app.include_router(analytics_router)
app.include_router(mining_router)
app.include_router(prediction_router)