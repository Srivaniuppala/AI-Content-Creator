# 🎨 AI Content Creator

An intelligent platform for personalized content creation using AI. Generate LinkedIn posts, professional emails, ad content, and more with the power of large language models.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-required-blue.svg)

## 📋 Features

- 🤖 **AI-Powered Generation**: Uses Groq API with LLaMA 3.3 70B for high-quality content
- 🔐 **Secure Authentication**: Password-based authentication with PBKDF2-HMAC-SHA256 hashing
- 💬 **Chat History**: Continue previous conversations seamlessly
- 📝 **Multiple Content Types**: LinkedIn posts, emails, ads, blog posts, and more
- ⚙️ **Customizable**: Adjust tone, length, and style
- 📊 **Analytics**: Track your content generation statistics
- ⭐ **Favorites**: Save and organize your best content
- 🎨 **Modern UI**: Beautiful, responsive Streamlit interface
- ⚡ **Fast Response**: Cloud-based API for instant generation

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit     │ ← User Interface
│   Frontend      │
└────────┬────────┘
         │
┌────────▼────────┐
│   PostgreSQL    │ ← Data Storage
│   Database      │
└─────────────────┘

┌─────────────────┐
│   Groq API      │ ← LLM Inference
│ (LLaMA 3.3 70B) │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Groq API Key** (free at https://console.groq.com)
- At least **2GB RAM** for the application

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd sriproject
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_api_key_here
```

3. **Start the application**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Streamlit app on port 8501

4. **Access the application**

Open your browser and go to: `http://localhost:8501`

## 📖 Usage Guide

### Getting Started

1. **Sign Up / Login**
   - Create an account with your email
   - Or login if you already have an account

2. **Generate Content**
   - Select content type (LinkedIn Post, Email, etc.)
   - Choose tone (Professional, Casual, Creative, etc.)
   - Select length (Short, Medium, Long)
   - Enter your prompt
   - Click "Generate Content"

3. **Chat Continuity**
   - Your conversations are saved automatically
   - Click on recent chats in the sidebar to continue
   - Start a new chat anytime

4. **View History**
   - Access all your generated content
   - Filter by content type
   - Search your content
   - Mark favorites
   - Download content

5. **Manage Profile**
   - Update your display name
   - Set default preferences
   - Change password
   - View statistics
   - Reset password

## 🛠️ Project Structure

```
sriproject/
├── app/
│   ├── auth/
│   │   └── firebase_auth.py      # Simple password authentication
│   ├── database/
│   │   └── db.py                 # PostgreSQL operations
│   ├── services/
│   │   └── ollama_service.py     # Groq API integration
│   ├── pages/
│   │   ├── login.py              # Login/Signup page
│   │   ├── home.py               # Content generation
│   │   ├── history.py            # Content history
│   │   └── profile.py            # User profile
│   ├── utils/
│   │   └── ui_helpers.py         # UI components
│   └── main.py                   # Main application
├── database/
│   └── init.sql                  # Database schema
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Streamlit container
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------||
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `GROQ_API_KEY` | Groq API authentication key | Required |
| `GROQ_MODEL` | LLM model name | `llama-3.3-70b-versatile` |

### Database Schema

The application uses PostgreSQL with the following tables:
- `users` - User profiles with password hashes
- `content_types` - Available content types
- `chat_sessions` - Chat conversation sessions
- `chat_messages` - Individual messages
- `generated_content` - Final generated content
- `user_preferences` - User settings

## 🐳 Docker Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Restart specific service
```bash
docker-compose restart streamlit
```

### Access database
```bash
docker exec -it content_creator_db psql -U content_admin -d content_creator
```

### Change Groq model
```bash
# Edit .env file and change GROQ_MODEL to:
# llama-3.1-70b-versatile
# mixtral-8x7b-32768
# gemma2-9b-it
# Then restart:
docker-compose restart streamlit
```

### Remove all data (⚠️ destructive)
```bash
docker-compose down -v
```

## 🎯 Available Content Types

1. **LinkedIn Post** - Professional social media content
2. **Professional Email** - Formal business emails
3. **Ad Content** - Marketing and advertising copy
4. **Conversational Text** - Casual messages
5. **Blog Post** - Long-form articles
6. **Social Media Caption** - Instagram, Twitter, Facebook

## 🔍 Troubleshooting

### Groq API errors
```bash
# Check API key is configured
docker exec content_creator_app env | grep GROQ

# Test API connection
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# View app logs
docker logs content_creator_app
```

### Database connection issues
```bash
# Check PostgreSQL status
docker exec content_creator_db pg_isready

# View database logs
docker logs content_creator_db
```

### Streamlit errors
```bash
# View app logs
docker logs content_creator_app

# Rebuild and restart
docker-compose up -d --build streamlit
```

### Rate limit errors
- Groq free tier has rate limits
- Check usage at https://console.groq.com
- Wait a moment and retry
- Consider upgrading to paid plan for higher limits

### API key issues
- Verify API key in `.env` file
- Ensure no extra spaces or quotes
- Get new key from https://console.groq.com

## 🚀 Performance Tips

1. **Model Selection**: `llama-3.3-70b-versatile` offers best quality, `gemma2-9b-it` is faster
2. **Rate Limits**: Free tier allows 30 requests/minute, plan accordingly
3. **Caching**: Generated content is stored in database for quick access
4. **Database Optimization**: Regular vacuuming and indexing for large datasets

## 🔒 Security Notes

- **Never commit `.env` file** with API keys to version control
- Use strong passwords for database
- User passwords are hashed with PBKDF2-HMAC-SHA256 (100k iterations)
- **Keep Groq API key secret** - it provides access to paid resources
- Use HTTPS in production
- Regularly update dependencies
- Rotate API keys periodically

## 📝 Development

### Adding New Content Types

1. Add to database:
```sql
INSERT INTO content_types (name, description) 
VALUES ('New Type', 'Description');
```

2. Add prompt template in `app/services/ollama_service.py`

### Customizing UI

Edit styles in `app/utils/ui_helpers.py`

### Changing AI Models

Groq supports multiple models. Edit `.env`:
```bash
# Best quality (default)
GROQ_MODEL=llama-3.3-70b-versatile

# Faster responses
GROQ_MODEL=llama-3.1-70b-versatile
GROQ_MODEL=mixtral-8x7b-32768
GROQ_MODEL=gemma2-9b-it
```

### Database Migrations

Modify `database/init.sql` and restart PostgreSQL:
```bash
docker-compose down
docker-compose up -d
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Groq** - Fast LLM inference API
- **Meta AI** - LLaMA language models
- **Streamlit** - Web framework
- **PostgreSQL** - Database

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check troubleshooting section
- Review Docker logs

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Support for more AI providers (OpenAI, Anthropic)
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] REST API endpoints
- [ ] Mobile app
- [ ] Content templates library
- [ ] Export to various formats (PDF, DOCX)
- [ ] Content scheduling and publishing

---

**Built with ❤️ for content creators**
