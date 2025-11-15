from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
from typing import List, Optional, Dict
import os

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Music Genre Classification API",
    description="AI-powered multi-label music genre classification system",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Ensure directories exist
os.makedirs("frontend/static", exist_ok=True)
os.makedirs("frontend/templates", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Mount static and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Models and preprocessing
MODEL = 'backend/models/svm_model.pkl'
SCALER = None

GENRE_LABELS = [
    "pop", "rock", "hip_hop", "jazz", "electronic",
    "classical", "r_b", "country", "metal", "folk"
]


# Pydantic schemas
class TrackData(BaseModel):
    track_name: str
    artists: str
    album_name: Optional[str] = ""
    danceability: float = 0.5
    energy: float = 0.5
    loudness: float = -10.0
    speechiness: float = 0.05
    acousticness: float = 0.1
    instrumentalness: float = 0.0
    liveness: float = 0.1
    valence: float = 0.5
    tempo: float = 120.0
    popularity: float = 50.0


class PredictionResponse(BaseModel):
    track: str
    artists: str
    predictions: Dict[str, float]
    top_genres: List[str]
    confidence: float
    model_version: str
    timestamp: str


class BatchPredictionRequest(BaseModel):
    tracks: List[TrackData]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_tracks: int
    average_confidence: float


@app.on_event("startup")
async def startup_event():
    global MODEL, SCALER
    try:
        if os.path.exists('backend/models/svm_model.pkl'):
            MODEL = joblib.load('backend/models/svm_model.pkl')
            logger.info("✅ SVM model loaded successfully")
        else:
            logger.warning("⚠️ Model file not found, running in demo mode")

        if os.path.exists('models/scaler.pkl'):
            SCALER = joblib.load('models/scaler.pkl')
            logger.info("✅ Scaler loaded successfully")
        else:
            logger.warning("⚠️ Scaler not found, using default scaling")
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")


# Frontend routes
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recommend")
async def recommend(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})


@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


# API endpoints
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }


@app.get("/api/genres")
async def get_available_genres():
    return {"genres": GENRE_LABELS}


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_genres(track_data: TrackData):
    if MODEL is None:
        # Demo mode - return mock predictions
        return await demo_predict(track_data)

    try:
        # Prepare features for prediction
        features = [
            track_data.danceability,
            track_data.energy,
            track_data.loudness,
            track_data.speechiness,
            track_data.acousticness,
            track_data.instrumentalness,
            track_data.liveness,
            track_data.valence,
            track_data.tempo,
            track_data.popularity
        ]

        # Make prediction
        features_array = np.array(features).reshape(1, -1)
        probabilities = MODEL.predict_proba(features_array)

        # Handle different probability formats
        if hasattr(probabilities, '__len__') and len(probabilities) > 0:
            if isinstance(probabilities[0], np.ndarray):
                probabilities = np.array([prob[1] for prob in probabilities])
            else:
                probabilities = probabilities[0]
        else:
            probabilities = np.random.rand(len(GENRE_LABELS))

        # Create predictions dictionary
        predictions = {}
        for i, genre in enumerate(GENRE_LABELS):
            if i < len(probabilities):
                predictions[genre] = float(probabilities[i])
            else:
                predictions[genre] = 0.0

        # Get top genres (above 0.5 confidence)
        top_genres = [genre for genre, prob in predictions.items() if prob > 0.5]
        confidence = np.mean(list(predictions.values()))

        return PredictionResponse(
            track=track_data.track_name,
            artists=track_data.artists,
            predictions=predictions,
            top_genres=top_genres,
            confidence=confidence,
            model_version="SVM-v2.0",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        # Fallback to demo mode
        return await demo_predict(track_data)


async def demo_predict(track_data: TrackData):
    """Demo prediction when model is not available"""
    # Generate mock probabilities based on input features
    base_probs = {
        "pop": min(0.7, track_data.danceability * 0.8 + track_data.popularity * 0.002),
        "rock": min(0.6, track_data.energy * 0.7 + (1 - track_data.danceability) * 0.3),
        "hip_hop": min(0.5, track_data.speechiness * 5 + track_data.energy * 0.3),
        "jazz": min(0.4, track_data.acousticness * 0.6 + (1 - track_data.energy) * 0.2),
        "electronic": min(0.8, track_data.energy * 0.7 + track_data.danceability * 0.5),
        "classical": min(0.3, track_data.instrumentalness * 0.8 + track_data.acousticness * 0.4),
        "r_b": min(0.5, track_data.danceability * 0.6 + track_data.valence * 0.3),
        "country": min(0.4, track_data.acousticness * 0.5 + track_data.valence * 0.3),
        "metal": min(0.3, track_data.energy * 0.8 + (1 - track_data.valence) * 0.2),
        "folk": min(0.3, track_data.acousticness * 0.7 + (1 - track_data.energy) * 0.2)
    }

    # Normalize probabilities
    total = sum(base_probs.values())
    predictions = {genre: prob / total * 0.8 for genre, prob in base_probs.items()}

    top_genres = [g for g, p in predictions.items() if p > 0.5]
    confidence = np.mean(list(predictions.values()))

    return PredictionResponse(
        track=track_data.track_name,
        artists=track_data.artists,
        predictions=predictions,
        top_genres=top_genres,
        confidence=confidence,
        model_version="DEMO-MODE",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/predict/batch", response_model=BatchPredictionResponse)
async def predict_genres_batch(batch_request: BatchPredictionRequest):
    predictions = []
    total_confidence = 0.0

    for track in batch_request.tracks:
        resp = await predict_genres(track)
        predictions.append(resp)
        total_confidence += resp.confidence

    avg_confidence = total_confidence / len(predictions) if predictions else 0.0
    return BatchPredictionResponse(
        predictions=predictions,
        total_tracks=len(predictions),
        average_confidence=avg_confidence
    )


@app.get("/api/metrics")
async def get_model_metrics():
    return {
        "model_name": "Support Vector Machine (SVM)",
        "accuracy": 0.948,
        "f1_score": 0.451,
        "training_samples": 114000,
        "last_trained": "2025-11-11",
        "genres_supported": len(GENRE_LABELS),
        "demo_mode": MODEL is None
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")