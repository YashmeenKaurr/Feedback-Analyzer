from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": allowed_origins}},
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
)

# Test route to check if server is running
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Backend server is running!',
        'python_version': '3.14.2',
        'mysql_status': 'not_configured'
    })

# Simple test route for feedback analysis (mock response)
@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'feedback' not in data:
            return jsonify({'error': 'No feedback provided'}), 400
        
        feedback = data['feedback']
        
        # Mock analysis response (since we don't have OpenAI configured yet)
        mock_analysis = {
            'feedback': feedback,
            'sentiment': 'positive' if any(word in feedback.lower() for word in ['good', 'great', 'excellent', 'amazing', 'love']) else 'negative' if any(word in feedback.lower() for word in ['bad', 'terrible', 'awful', 'hate', 'worst']) else 'neutral',
            'confidence': 0.85,
            'keywords': feedback.split()[:5],  # First 5 words as keywords
            'message': 'This is a mock analysis. Configure OpenAI API for real analysis.'
        }
        
        return jsonify(mock_analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test database connection (will fail gracefully without MySQL)
@app.route('/api/db-test', methods=['GET'])
def test_db():
    try:
        # This will fail without MySQL, but we'll handle it gracefully
        from database import get_db_connection
        connection = get_db_connection()
        connection.close()
        return jsonify({'database': 'connected', 'status': 'MySQL is working!'})
    except Exception as e:
        return jsonify({
            'database': 'not_connected', 
            'status': 'MySQL not configured',
            'error': str(e),
            'instructions': 'Install MySQL and update .env file to enable database features'
        })

if __name__ == '__main__':
    print("🚀 Starting Feedback Analyzer Backend (Test Mode)")
    print("📡 Server will run on: http://127.0.0.1:5000")
    print("🔗 Frontend should run on: http://localhost:5173")
    print()
    print("Available endpoints:")
    print("  GET  /api/health     - Health check")
    print("  POST /api/analyze    - Analyze feedback (mock)")
    print("  GET  /api/db-test    - Test database connection")
    print()
    
    app.run(debug=True, host='127.0.0.1', port=5000)