# 🤖 AI Blog Generator

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini-API-red.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT%20with%20Attribution-yellow.svg)](LICENSE)

**⭐ If you use this code, please give credit to the original author!**

A powerful full-stack web application that generates high-quality, AI-powered blog articles using Google's Gemini API. Create, edit, and publish professional content in seconds with an intuitive interface and advanced AI-assisted editing.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Advanced Features](#-advanced-features) • [API Documentation](#-api-documentation) • [Deployment](#-deployment) • [Contributing](#-contributing) • [Attribution](#-attribution-requirement)

</div>

---

## 🎯 Overview

The AI Blog Generator is a complete content creation solution that combines AI-powered blog generation with intelligent editing capabilities. Whether you're a content creator, marketer, blogger, or developer, this tool streamlines your workflow from ideation to publication.

**Key Highlights:**
- ⚡ Generate multiple blogs simultaneously
- 🎨 Smart AI-assisted editing with single or multiple suggestions
- 💾 Automatic change persistence with undo capability
- 📥 Export to 7 different formats (PDF, DOCX, HTML, JSON, CSV, Markdown, Text)
- 🔐 User authentication with blog history
- 🎯 Trending categories with 5-minute refresh
- 📱 Fully responsive design
- 🚀 Production-ready Flask backend

---

## ✨ Features

### 🧠 AI-Powered Blog Generation
- **Google Gemini API Integration** - Uses cutting-edge Google Gemini 2.5 Flash model
- **Batch Processing** - Generate multiple blogs simultaneously
- **Smart Context Detection** - Automatically identifies technical vs. general topics
- **Customizable Prompts** - Add optional details to guide AI content generation
- **Fast & Reliable** - Generates high-quality content in seconds

### ✏️ Advanced AI Chat Editor
- **Intelligent Request Parsing**
  - Single requests (rephrase, improve, simplify) → One optimized suggestion
  - Specific numbers (5, 3, 10) → Multiple numbered options
  - Works with titles, paragraphs, and any text length

- **Smart Text Matching**
  - Three-pass matching system for paragraph-level changes
  - Handles text split across multiple DOM nodes
  - Preserves original formatting (bold, italics, links)

- **Change Management**
  - Complete change history tracking
  - Revert changes one at a time
  - Changes persist to database/session

### 📥 Multiple Export Formats
- **PDF** - Professional document format with styling
- **DOCX** - Microsoft Word format for further editing
- **HTML** - Standalone web pages
- **JSON** - Structured data for programmatic access
- **CSV** - Spreadsheet format for bulk management
- **Markdown** - Perfect for GitHub and documentation
- **Text** - Plain text format

### 🏛️ Professional UI/UX
- **Paper-like Blog Display** - Professional article formatting
- **Trending Categories Sidebar** - 8 categories with 10+ topics each
- **Auto-Rotating Topics** - Fresh suggestions every 5 minutes
- **Real-time Text Selection** - Yellow highlighting for clarity
- **One-Click Application** - "Use This" buttons for instant changes
- **Success Notifications** - Visual feedback for all actions

### 👤 User Authentication
- **Secure Registration** - Email and password-based signup
- **Blog History** - Access all your previously generated blogs with filtering
- **Persistent Changes** - All edits saved to your account
- **Session Management** - Remember me option available
- **Database Integration** - SQLAlchemy with SQLite

### 📊 Dashboard & Blog Management
- **Statistics Dashboard** - Track total blogs generated and downloads
- **Category Auto-Detection** - Blogs automatically categorized (Tech, Beauty, Education, Gaming, Health, Travel, Lifestyle, Business, General)
- **Advanced Filtering** - Filter by:
  - **Time** - Recent, Month, or Year
  - **Category** - Filter by auto-detected blog categories
  - **Search** - Search blogs by title
- **Clear History** - One-click deletion of all blogs
- **Blog Management** - Delete individual blogs or clear entire history

### 💾 Smart Data Persistence
- **Auto-Save** - No manual save button needed
- **Dual Storage**
  - Session storage for guests
  - Database storage for authenticated users
- **Change Tracking** - Complete history of all modifications
- **File Generation** - Updated downloads reflect all changes

---

## 📋 Project Structure

```
AI-BLOG-GENERATOR/
├── app.py                      # Main Flask application & API routes
├── models.py                   # Database models (User, UserBlog)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── Procfile                    # Heroku deployment config
├── README.md                   # This file
│
├── templates/
│   ├── index.html              # Generate page with trending categories
│   ├── blog_list.html          # View & edit blogs with AI chat
│   ├── login.html              # User authentication
│   ├── register.html           # User registration
│   ├── auth.html               # Auth base template
│   └── blog_history.html       # User blog history
│
├── static/
│   ├── style.css               # Complete styling for all pages
│   └── icons/
│       ├── tech.svg            # Category icons
│       ├── beauty.svg
│       ├── education.svg
│       ├── gaming.png
│       ├── health.png
│       ├── travel.png
│       ├── lifestyle.png
│       └── business.png
│
├── instance/
│   └── database.db             # SQLite database (auto-created)
│
└── data/
    └── last_blogs_*.json       # Session blog cache files
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key
- Modern web browser

### Step 1: Clone Repository

```bash
git clone https://github.com/deebak4064/AI-BLOG-GENERATOR.git
cd AI-BLOG-GENERATOR
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key in new project"
3. Copy your API key

### Step 5: Configure Environment

Create a `.env` file in the project root:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
CHAT_ASSISTANT_API_KEY=your_gemini_api_key_here

# Flask Configuration (optional)
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### Step 6: Run Application

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 💡 Usage Guide

### Generating Blogs

1. **Visit Homepage** - Go to the Generate page
2. **Enter Blog Topics** - One topic per line
3. **Optional Details** - Add ` | ` followed by custom instructions
4. **Click Generate** - AI creates blogs instantly

**Example Input:**
```
Understanding Python Decorators | Focus on practical examples and use cases
Building REST APIs with FastAPI | Include Docker deployment steps
Top 10 Machine Learning Libraries 2025 | Technical overview with pros/cons
```

### Viewing & Editing Blogs

1. **View Generated Content** - Blogs display in professional format
2. **Select Text** - Click and drag to highlight any text
3. **Request Changes** - Use the AI Chat panel:
   - "Rephrase this" → Get one improved version
   - "Give me 5 alternatives" → Get multiple options
4. **Apply Suggestions** - Click "Use This" button
5. **Revert Changes** - Use "Revert Last Change" button anytime
6. **Download** - Export in your preferred format

### Downloading Blogs

Click the "Download" button to choose format:
- **PDF** - Professional document with styling
- **DOCX** - Editable Word document
- **HTML** - Standalone web page
- **JSON** - Structured data format
- **CSV** - Spreadsheet format
- **Markdown** - GitHub-friendly format
- **Text** - Plain text file

---

## 🎨 Advanced Features

### Trending Categories

The app includes 8 trending categories that automatically refresh every 5 minutes with fresh topic suggestions:

| Category | Topics Include |
|----------|-----------------|
| **Tech** | AI, Cloud, Security, Development, Blockchain |
| **Beauty** | Skincare, Makeup, Wellness, Hair Care |
| **Education** | Learning, Courses, Teaching, STEM |
| **Gaming** | Reviews, Streaming, Esports, VR |
| **Health** | Fitness, Nutrition, Mental Health, Wellness |
| **Travel** | Budget Tips, Adventure, Culture, Destinations |
| **Lifestyle** | Minimalism, Productivity, Habits, Wellness |
| **Business** | Startup, Marketing, Leadership, Finance |

**How to Use:**
1. Click any category button
2. Select from suggested topics
3. Topic is copied to clipboard and/or input field
4. Topics refresh every 5 minutes

### Smart AI Editor

The AI Chat Assistant intelligently detects your intent:

**Single Request Examples:**
- "Make this more professional" → 1 suggestion
- "Simplify this paragraph" → 1 optimized version
- "Improve the opening" → 1 enhanced version

**Multiple Request Examples:**
- "Give me 5 better titles" → 5 numbered options
- "Suggest 3 different headlines" → 3 variations
- "Provide 10 alternative openings" → 10 choices

**Change Tracking:**
- Every change is logged to history
- Revert one change at a time
- Perfect for trying different variations

### Blog History & Filtering

Access all your generated blogs with intelligent filtering:

**Filter Options:**
- **Time Filter** - View Recent, This Month, or This Year
- **Category Filter** - Auto-detected categories (Tech, Beauty, Education, Gaming, Health, Travel, Lifestyle, Business, General)
- **Search Filter** - Find blogs by title keyword

**Features:**
- View complete blog history in a clean list
- Each blog shows title and creation date
- Apply multiple filters simultaneously
- Clear entire history with one click
- Delete individual blogs as needed

**How to Use:**
1. Go to "View Blogs" from navigation
2. Select your filter criteria (time, category, search)
3. Click "Apply Filters"
4. Click blog title to view full content
5. Use "Clear History" button to delete all blogs

### Multi-Format Export

All downloads include:
- AI-generated content only (no input metadata)
- Original formatting preservation
- Professional styling (where applicable)
- Optimized for publishing

---

## 🔌 API Documentation

### REST Endpoints

#### Chat API
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Give me 5 better titles for: How to Learn Python"
}
```

**Response:**
```json
{
  "response": "1. Master Python: A Comprehensive Learning Guide\n2. Python Programming: From Zero to Hero\n3. Learn Python Fast: Essential Concepts for Beginners\n4. Python Development: Your Complete Roadmap\n5. Getting Started with Python: A Practical Approach"
}
```

#### Save Blog Content
```http
POST /api/save-blog-content
Content-Type: application/json

{
  "idx": 0,
  "body_html": "<p>Updated content here</p>"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Blog content saved"
}
```

#### Get Trending Topics
```http
GET /api/trending-topics
```

**Response:**
```json
{
  "Tech": [
    "AI and Machine Learning Trends 2025",
    "Web Development Best Practices",
    "Cloud Computing Security"
  ],
  "Beauty": [...],
  ...
}
```

### Database Models

#### User Model
```python
- id (Integer, Primary Key)
- username (String, Unique)
- email (String, Unique)
- password_hash (String)
- created_at (DateTime)
- blogs (Relationship → UserBlog)
```

#### UserBlog Model
```python
- id (Integer, Primary Key)
- user_id (Foreign Key → User)
- title (String)
- details (Text)
- body (Text) - Plain text content
- body_html (Text) - HTML formatted content
- filename_base (String)
- created_at (DateTime)
```

---

## 🔒 Security Features

### API Key Management
- ✅ Environment variables only (never hardcoded)
- ✅ .env file excluded from version control
- ✅ Multiple API key support (failover capability)

### User Authentication
- ✅ Password hashing with werkzeug.security
- ✅ Session-based authentication with Flask-Login
- ✅ CSRF protection
- ✅ Secure cookie handling

### Database Security
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ Input validation on all forms
- ✅ Foreign key constraints
- ✅ Database isolation per user

### Content Safety
- ✅ HTML escaping in templates
- ✅ XSS prevention
- ✅ Content sanitization

---

## 📱 Responsive Design

### Desktop (1200px+)
- Two-column layout
- Side-by-side blog and chat
- Full trending panel

### Tablet (768px - 1199px)
- Responsive grid layout
- Collapsible sidebar
- Touch-optimized controls

### Mobile (< 768px)
- Single-column layout
- Hamburger menu for categories
- Full-width content
- Optimized text selection

---

## ⚙️ Configuration

### Environment Variables

```env
# Required
GEMINI_API_KEY=your_key_here

# Optional
CHAT_ASSISTANT_API_KEY=your_key_here  # Defaults to GEMINI_API_KEY
FLASK_ENV=production                   # development or production
SECRET_KEY=your_secret_key             # For session management
DATABASE_URL=sqlite:///database.db     # Database connection
```

### Flask Configuration

Edit `app.py` to modify:
- Session timeout duration
- File upload limits
- API timeout settings
- Database location

---

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_key_here
   heroku config:set SECRET_KEY=your_secret_here
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

### Docker Deployment

1. **Build Image**
   ```bash
   docker build -t ai-blog-generator .
   ```

2. **Run Container**
   ```bash
   docker run -e GEMINI_API_KEY=your_key \
              -p 5000:5000 \
              ai-blog-generator
   ```

3. **Visit** http://localhost:5000

### AWS/EC2 Deployment

1. Launch EC2 instance (Ubuntu 20.04+)
2. Install Python and dependencies
3. Clone repository
4. Configure environment variables
5. Run with Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

---

## 🔧 Troubleshooting

### Common Issues

**API Key Error**
```
Error: GEMINI_API_KEY is not configured
```
Solution: Check `.env` file exists and contains correct key

**Import Errors**
```
ModuleNotFoundError: No module named 'flask'
```
Solution: Run `pip install -r requirements.txt`

**Database Lock**
```
sqlite3.OperationalError: database is locked
```
Solution: Restart the application

**Port Already In Use**
```
OSError: [Errno 48] Address already in use
```
Solution: Change port in app.py or kill existing process

---

## 📊 Performance Metrics

- **Blog Generation:** < 5 seconds per blog
- **Chat Response:** < 2 seconds
- **Text Search:** < 100ms (local)
- **Database Query:** < 50ms (average)
- **Page Load:** < 1 second (optimized)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork Repository**
   ```bash
   git clone https://github.com/your-username/AI-BLOG-GENERATOR.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open Pull Request**

### Areas for Contribution
- [ ] Additional export formats (EPUB, LaTeX)
- [ ] Image generation integration
- [ ] Multiple language support
- [ ] Advanced analytics dashboard
- [ ] Collaborative editing features
- [ ] Template library
- [ ] SEO optimization tools

---

## 📚 Technology Stack

### Backend
- **Framework:** Flask 2.0+
- **Database:** SQLAlchemy with SQLite
- **Authentication:** Flask-Login
- **API:** Google Gemini AI 2.5 Flash
- **Server:** Gunicorn (production)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox/grid
- **Vanilla JavaScript** - No framework dependencies
- **Font Awesome** - Icon library
- **Google Fonts** - Typography

### DevOps
- **Containerization:** Docker
- **Version Control:** Git
- **Hosting:** Heroku, AWS, Azure ready
- **Database:** SQLite (development), PostgreSQL (production ready)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Deebak Kumar K**
- 📧 Email: deebakintern@gmail.com
- 🔗 LinkedIn: [linkedin.com/in/deebak-kumar-k-632b96285](https://linkedin.com/in/deebak-kumar-k-632b96285)
- 🐙 GitHub: [@deebak4064](https://github.com/deebak4064)

---

## 🙏 Acknowledgments

- Google Gemini AI for powerful language model
- Flask community for excellent framework
- Contributors and users for feedback

---

## 📞 Support

- **Issues:** Open an issue on GitHub
- **Discussions:** GitHub Discussions
- **Email:** deebakintern@gmail.com
- **Documentation:** [Full docs coming soon]

---

## 🗺️ Roadmap

- [ ] OpenAI API integration
- [ ] Real-time collaboration
- [ ] Advanced analytics
- [ ] Content calendar
- [ ] SEO tools
- [ ] Plagiarism checker
- [ ] Mobile app
- [ ] Browser extension

---

## ✅ Attribution Requirement

**If you use, fork, modify, or deploy this project, you MUST:**

1. **Include the LICENSE file** in your project
2. **Give credit** to the original author (Deepak Kumar) with a link to the original repository
3. **Add a notice** in your README or footer stating: *"Based on AI Blog Generator by [Deepak Kumar](https://github.com/deebak4064/AI-BLOG-GENERATOR)"*
4. **Document any changes** you make to the original code

### How to Cite This Project

**In Code Comments:**
```python
# Based on AI Blog Generator by Deepak Kumar
# Repository: https://github.com/deebak4064/AI-BLOG-GENERATOR
```

**In README:**
```markdown
This project is based on [AI Blog Generator](https://github.com/deebak4064/AI-BLOG-GENERATOR) 
created by [Deepak Kumar](https://github.com/deebak4064).
```

**Using BibTeX (for academic work):**
```bibtex
@software{kumar2024aibloggenerator,
  title={AI Blog Generator},
  author={Kumar, Deepak},
  year={2024},
  url={https://github.com/deebak4064/AI-BLOG-GENERATOR}
}
```

**Using CFF (Citation File Format):**
See [CITATION.cff](CITATION.cff) for structured citation information.

---

**Made with ❤️ by Deepak Kumar | [GitHub](https://github.com/deebak4064) | [Repository](https://github.com/deebak4064/AI-BLOG-GENERATOR)**

**Star ⭐ this repo if you find it useful!**
