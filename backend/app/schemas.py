"""
Pydantic schemas for the Music Genre Classification API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class TrackData(BaseModel):
    """Schema for track data input"""
    track_name: str = Field(..., description="Name of the track", example="Blinding Lights")
    artists: str = Field(..., description="Artist names", example="The Weeknd")
    album_name: Optional[str] = Field("", description="Album name", example="After Hours")

    # Audio features with validation ranges
    danceability: float = Field(0.5, ge=0.0, le=1.0, description="Danceability score")
    energy: float = Field(0.5, ge=0.0, le=1.0, description="Energy level")
    loudness: float = Field(-10.0, ge=-60.0, le=0.0, description="Loudness in dB")
    speechiness: float = Field(0.05, ge=0.0, le=1.0, description="Speechiness score")
    acousticness: float = Field(0.1, ge=0.0, le=1.0, description="Acousticness score")
    instrumentalness: float = Field(0.0, ge=0.0, le=1.0, description="Instrumentalness score")
    liveness: float = Field(0.1, ge=0.0, le=1.0, description="Liveness score")
    valence: float = Field(0.5, ge=0.0, le=1.0, description="Musical positiveness")
    tempo: float = Field(120.0, ge=60.0, le=200.0, description="Tempo in BPM")
    popularity: float = Field(50.0, ge=0.0, le=100.0, description="Popularity score")

    class Config:
        schema_extra = {
            "example": {
                "track_name": "Blinding Lights",
                "artists": "The Weeknd",
                "album_name": "After Hours",
                "danceability": 0.8,
                "energy": 0.7,
                "loudness": -5.2,
                "speechiness": 0.1,
                "acousticness": 0.2,
                "instrumentalness": 0.0,
                "liveness": 0.1,
                "valence": 0.6,
                "tempo": 120.0,
                "popularity": 95.0
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    track: str = Field(..., description="Track name")
    artists: str = Field(..., description="Artist names")
    predictions: Dict[str, float] = Field(..., description="Genre probabilities")
    top_genres: List[str] = Field(..., description="Top predicted genres")
    confidence: float = Field(..., description="Overall confidence score")
    model_version: str = Field(..., description="Model version used")
    timestamp: str = Field(..., description="Prediction timestamp")

    class Config:
        schema_extra = {
            "example": {
                "track": "Blinding Lights",
                "artists": "The Weeknd",
                "predictions": {
                    "pop": 0.85,
                    "rock": 0.12,
                    "electronic": 0.67
                },
                "top_genres": ["pop", "electronic"],
                "confidence": 0.76,
                "model_version": "SVM-v2.0",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction request"""
    tracks: List[TrackData] = Field(..., description="List of tracks to analyze")


class BatchPredictionResponse(BaseModel):
    """Schema for batch prediction response"""
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    total_tracks: int = Field(..., description="Total number of tracks processed")
    average_confidence: float = Field(..., description="Average confidence score")


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    timestamp: str = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")


class MetricsResponse(BaseModel):
    """Schema for model metrics response"""
    model_name: str = Field(..., description="Model name")
    accuracy: float = Field(..., description="Model accuracy")
    f1_score: float = Field(..., description="F1 score")
    training_samples: int = Field(..., description="Number of training samples")
    last_trained: str = Field(..., description="Last training date")
    genres_supported: int = Field(..., description="Number of supported genres")
    demo_mode: Optional[bool] = Field(False, description="Whether running in demo mode")


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str = Field(..., description="Error details")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: str = Field(..., description="Error timestamp")

    class Config:
        schema_extra = {
            "example": {
                "detail": "Model not loaded",
                "error_code": "MODEL_NOT_LOADED",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }