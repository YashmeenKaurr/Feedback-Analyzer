"""
Simple mock LLM for feedback analysis without OpenAI dependency
"""
import re
from typing import Dict, Any

def analyze_feedback(text: str) -> Dict[str, Any]:
    """
    Analyze feedback text and return sentiment analysis
    This is a mock implementation that doesn't require OpenAI
    """
    if not text or not text.strip():
        return {
            'feedback': text,
            'sentiment': 'neutral',
            'confidence': 0.0,
            'keywords': [],
            'message': 'No text provided'
        }
    
    # Simple rule-based sentiment analysis
    text_lower = text.lower().strip()
    
    # Positive keywords
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
        'love', 'perfect', 'awesome', 'brilliant', 'outstanding', 'superb',
        'happy', 'satisfied', 'pleased', 'delighted', 'impressed', 'recommend'
    ]
    
    # Negative keywords  
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate',
        'worst', 'disappointing', 'frustrated', 'angry', 'annoyed', 'upset',
        'useless', 'broken', 'failed', 'poor', 'slow', 'expensive'
    ]
    
    # Count positive and negative words
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    # Determine sentiment
    if positive_count > negative_count:
        sentiment = 'positive'
        confidence = min(0.9, 0.6 + (positive_count * 0.1))
    elif negative_count > positive_count:
        sentiment = 'negative' 
        confidence = min(0.9, 0.6 + (negative_count * 0.1))
    else:
        sentiment = 'neutral'
        confidence = 0.5
    
    # Extract keywords (simple word extraction)
    words = re.findall(r'\b\w+\b', text_lower)
    keywords = [word for word in words if len(word) > 3][:5]  # First 5 meaningful words
    
    return {
        'feedback': text,
        'sentiment': sentiment,
        'confidence': round(confidence, 2),
        'keywords': keywords,
        'message': f'Mock analysis - detected {sentiment} sentiment with {positive_count} positive and {negative_count} negative indicators.'
    }