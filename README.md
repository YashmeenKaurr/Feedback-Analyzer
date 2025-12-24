# Feedback Analyzer

A web application that analyzes customer feedback using AI/LLM technology with user authentication and MySQL database integration.

## Features

- 🔐 **User Authentication** - Register/Login with email or Google OAuth
- 🤖 **AI-Powered Analysis** - Sentiment analysis using OpenAI/LLM models
- 💾 **MySQL Database** - Persistent storage for users and analyses
- 📊 **Dashboard** - View analysis history and reports
- 🎨 **Modern UI** - React-based frontend with responsive design

## Tech Stack

### Backend
- **Python Flask** - Web framework
- **MySQL** - Database (PyMySQL driver)
- **JWT** - Authentication tokens
- **OpenAI/LangChain** - LLM integration
- **Google OAuth** - Social authentication

### Frontend
- **React** - Frontend framework
- **Vite** - Build tool
- **CSS3** - Styling

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Feedback-Analyzer-main
```

### 2. Database Setup
Follow the detailed [MySQL Setup Guide](MYSQL_SETUP.md) to:
- Install MySQL
- Create database and user
- Configure environment variables

### 3. Backend Setup
```bash
cd Backend

# Install dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env with your MySQL credentials and API keys

# Initialize database
python init_db.py

# Run backend server
python app.py
```

### 4. Frontend Setup
```bash
cd Frontend/feedback_analyser

# Install dependencies
npm install

# Run frontend server
npm run dev
```

### 5. Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Configuration

### Required Environment Variables (Backend/.env)

```env
# Database
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=feedback_analyser
DB_PORT=3306

# Authentication
JWT_SECRET_KEY=your_secret_key

# AI/LLM
OPENAI_API_KEY=your_openai_key

# Optional: Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Analysis
- `POST /api/analyze` - Analyze feedback
- `GET /api/analyses` - Get user's analysis history

## Database Schema

The application uses three main tables:
- **users** - User authentication and profile data
- **user_sessions** - JWT token management
- **user_analyses** - Stored feedback analyses

See [MYSQL_SETUP.md](MYSQL_SETUP.md) for detailed schema information.

## Development

### Project Structure
```
Feedback-Analyzer-main/
├── Backend/
│   ├── app.py              # Flask application
│   ├── auth.py             # Authentication logic
│   ├── database.py         # Database operations
│   ├── llm.py              # LLM integration
│   ├── init_db.py          # Database initialization
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── .env                # Environment variables (not in git)
├── Frontend/
│   └── feedback_analyser/  # React application
├── MYSQL_SETUP.md          # Database setup guide
└── README.md               # This file
```

### Running in Development
1. Start MySQL service
2. Run backend: `cd Backend && python app.py`
3. Run frontend: `cd Frontend/feedback_analyser && npm run dev`

## Troubleshooting

### Common Issues
1. **Database connection errors** - Check MySQL service and credentials
2. **Missing API keys** - Ensure OpenAI API key is set in .env
3. **Port conflicts** - Make sure ports 5000 (backend) and 5173 (frontend) are available

### Getting Help
- Check the [MySQL Setup Guide](MYSQL_SETUP.md) for database issues
- Review the [Authentication Setup](AUTHENTICATION_SETUP.md) for OAuth configuration
- Ensure all dependencies are installed with correct versions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]
