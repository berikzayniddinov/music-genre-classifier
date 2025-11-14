"""
Utility functions for the Music Genre Classification system
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def preprocess_audio_features(features: Dict[str, Any]) -> np.ndarray:
    """
    Preprocess audio features for model prediction

    Args:
        features: Dictionary containing audio features

    Returns:
        numpy array of preprocessed features
    """
    try:
        # Extract features in the correct order expected by the model
        feature_list = [
            features.get('danceability', 0.5),
            features.get('energy', 0.5),
            features.get('loudness', -10.0),
            features.get('speechiness', 0.05),
            features.get('acousticness', 0.1),
            features.get('instrumentalness', 0.0),
            features.get('liveness', 0.1),
            features.get('valence', 0.5),
            features.get('tempo', 120.0),
            features.get('popularity', 50.0)
        ]

        return np.array(feature_list).reshape(1, -1)

    except Exception as e:
        logger.error(f"Error preprocessing features: {e}")
        raise


def normalize_predictions(predictions: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize prediction probabilities to sum to 1

    Args:
        predictions: Dictionary of genre probabilities

    Returns:
        Normalized predictions
    """
    try:
        total = sum(predictions.values())
        if total > 0:
            return {genre: prob / total for genre, prob in predictions.items()}
        return predictions
    except Exception as e:
        logger.error(f"Error normalizing predictions: {e}")
        return predictions


def calculate_confidence(predictions: Dict[str, float]) -> float:
    """
    Calculate overall confidence score from predictions

    Args:
        predictions: Dictionary of genre probabilities

    Returns:
        Confidence score between 0 and 1
    """
    try:
        if not predictions:
            return 0.0

        # Use maximum probability as confidence
        max_prob = max(predictions.values())

        # Adjust confidence based on probability distribution
        if max_prob > 0.7:
            return min(1.0, max_prob * 1.1)  # Boost high confidence
        elif max_prob > 0.3:
            return max_prob  # Use as-is for medium confidence
        else:
            return max_prob * 0.8  # Penalize low confidence

    except Exception as e:
        logger.error(f"Error calculating confidence: {e}")
        return 0.5


def validate_audio_features(features: Dict[str, Any]) -> bool:
    """
    Validate audio feature ranges

    Args:
        features: Dictionary containing audio features

    Returns:
        Boolean indicating if features are valid
    """
    try:
        valid_ranges = {
            'danceability': (0.0, 1.0),
            'energy': (0.0, 1.0),
            'loudness': (-60.0, 0.0),
            'speechiness': (0.0, 1.0),
            'acousticness': (0.0, 1.0),
            'instrumentalness': (0.0, 1.0),
            'liveness': (0.0, 1.0),
            'valence': (0.0, 1.0),
            'tempo': (60.0, 200.0),
            'popularity': (0.0, 100.0)
        }

        for feature, value in features.items():
            if feature in valid_ranges:
                min_val, max_val = valid_ranges[feature]
                if not (min_val <= value <= max_val):
                    logger.warning(f"Feature {feature} value {value} outside valid range [{min_val}, {max_val}]")
                    return False

        return True

    except Exception as e:
        logger.error(f"Error validating features: {e}")
        return False


def generate_mock_predictions(features: Dict[str, Any]) -> Dict[str, float]:
    """
    Generate mock predictions for demo mode

    Args:
        features: Dictionary containing audio features

    Returns:
        Mock genre predictions
    """
    try:
        # Base probabilities influenced by different features
        base_probs = {
            "pop": min(0.7, features.get('danceability', 0.5) * 0.8 + features.get('popularity', 50) * 0.002),
            "rock": min(0.6, features.get('energy', 0.5) * 0.7 + (1 - features.get('danceability', 0.5)) * 0.3),
            "hip_hop": min(0.5, features.get('speechiness', 0.05) * 5 + features.get('energy', 0.5) * 0.3),
            "jazz": min(0.4, features.get('acousticness', 0.1) * 0.6 + (1 - features.get('energy', 0.5)) * 0.2),
            "electronic": min(0.8, features.get('energy', 0.5) * 0.7 + features.get('danceability', 0.5) * 0.5),
            "classical": min(0.3,
                             features.get('instrumentalness', 0.0) * 0.8 + features.get('acousticness', 0.1) * 0.4),
            "r_b": min(0.5, features.get('danceability', 0.5) * 0.6 + features.get('valence', 0.5) * 0.3),
            "country": min(0.4, features.get('acousticness', 0.1) * 0.5 + features.get('valence', 0.5) * 0.3),
            "metal": min(0.3, features.get('energy', 0.5) * 0.8 + (1 - features.get('valence', 0.5)) * 0.2),
            "folk": min(0.3, features.get('acousticness', 0.1) * 0.7 + (1 - features.get('energy', 0.5)) * 0.2)
        }

        # Normalize probabilities
        total = sum(base_probs.values())
        if total > 0:
            normalized_probs = {genre: prob / total * 0.8 for genre, prob in base_probs.items()}
        else:
            normalized_probs = {genre: 0.08 for genre in base_probs.keys()}

        return normalized_probs

    except Exception as e:
        logger.error(f"Error generating mock predictions: {e}")
        # Return equal probabilities as fallback
        return {genre: 0.1 for genre in ["pop", "rock", "hip_hop", "jazz", "electronic",
                                         "classical", "r_b", "country", "metal", "folk"]}