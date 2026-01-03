# ZT Hosting Chatbot 🤖

An intelligent AI-powered customer support chatbot for ZT Hosting services, built with FastAPI, LangChain, and Groq LLM.

## 📋 Overview

ZT Hosting Chatbot is a professional customer support solution that provides instant, accurate answers to hosting-related questions. It combines:
- **AI-Powered Responses**: Uses Groq's LLaMA 3.1 model for intelligent question answering
- **Smart Context Routing**: Automatically routes questions to relevant knowledge base files
- **Admin Panel**: Manage FAQs and customize responses
- **Database Integration**: Supabase for manual FAQ storage
- **Multiple Hosting Services**: Covers domains, VPS, shared hosting, WordPress, email, and more

## 🌟 Features

### Core Functionality
- **Intelligent Q&A**: AI-driven responses based on comprehensive hosting documentation
- **Multi-Service Support**: Answers questions about:
  - Domain Registration (.pk, .com, international domains)
  - Shared Web Hosting
  - VPS Hosting
  - WordPress Hosting
  - Email Hosting
  - Dedicated Servers
  - Reseller Hosting
  - Promo Packages

### Admin Features
- **Secure Login**: reCAPTCHA-protected admin authentication
- **FAQ CRUD Operations**: Full Create, Read, Update, Delete functionality for FAQs
- **Response Style Control**: Toggle between short/professional and conversational responses
- **Priority Rules**: Configure database-first or AI-supplement modes
- **Context Size Settings**: Adjustable context window (2000/4000/6000 characters)
- **Modern Dashboard**: Tab-based interface with real-time updates
- **Session Management**: Secure cookie-based authentication

### Technical Features
- **Smart File Routing**: Automatically selects relevant knowledge base files
- **Context Optimization**: Limits context to prevent token overages
- **Error Handling**: Graceful degradation and user-friendly error messages
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Path Flexibility**: Works on both local and Vercel deployment

## 🏗️ Architecture

```
ZT-Hosting-chatbot/
├── api/
│   └── app.py                 # Main FastAPI application
├── data/                      # Knowledge base files
│   ├── zt_home_page.txt
│   ├── domain_registration.txt
│   ├── shared_webhosting.txt
│   ├── pro_vps_hosting.txt
│   ├── pro_wordpress_hosting.txt
│   ├── pro_email_hosting.txt
│   ├── pro_dedicated_servers.txt
│   ├── pro_hosting_business_web.txt
│   ├── reseller_hosting.txt
│   ├── promo_packages.txt
│   ├── aboutus.txt
│   ├── contactus.txt
│   ├── privacy-policy.txt
│   ├── terms-condition.txt
│   └── acceptable-policy.txt
├── templates/                 # HTML templates
│   ├── index.html            # Main chatbot interface
│   ├── admin.html            # Admin panel
│   └── login.html            # Login page
├── db/                       # Vector database (ChromaDB)
├── main.py                   # Local chatbot CLI
├── ingest.py                 # Vector database creation
├── crawler.py                # Web scraping utility
├── get_data.py               # Data fetching utilities
├── create_db.py              # Database setup
├── index.js                  # Express server (alternative)
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python version specification
├── vercel.json              # Vercel deployment config
└── .env                      # Environment variables
```

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Node.js 14+ (for Express server option)
- Supabase account
- Groq API key

### Step 1: Clone Repository
```bash
git clone https://github.com/fatima678/ZT-Hosting-chatbot.git
cd ZT-Hosting-chatbot
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Node Dependencies (Optional)
```bash
npm install
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:

```env
# AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Database Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# reCAPTCHA
RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key
```

### Step 5: Set Up Supabase Database

#### Create Required Tables

Run these SQL commands in your Supabase SQL editor:

```sql
-- Create manual_faqs table
CREATE TABLE manual_faqs (
  id BIGSERIAL PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create bot_settings table
CREATE TABLE bot_settings (
  id BIGSERIAL PRIMARY KEY,
  response_style TEXT NOT NULL DEFAULT 'short',
  priority TEXT NOT NULL DEFAULT 'database_first',
  context_size INTEGER NOT NULL DEFAULT 4000,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Insert default settings
INSERT INTO bot_settings (response_style, priority, context_size)
VALUES ('short', 'database_first', 4000);
```

**Note**: For detailed admin dashboard setup instructions, see [ADMIN_SETUP.md](ADMIN_SETUP.md)

## 💻 Usage

### Local Development

#### Option 1: FastAPI Server
```bash
cd api
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Access at: `http://localhost:8000`

#### Option 2: CLI Chatbot
```bash
python main.py
```

#### Option 3: Express Server
```bash
node index.js
```
Access at: `http://localhost:3000`

### Running the Crawler
To scrape fresh data from ZT Hosting website:
```bash
python crawler.py
```

### Creating Vector Database (Optional)
```bash
python ingest.py
```

### Using the Admin Dashboard

1. **Access Login Page**
   ```
   http://localhost:8000/login
   ```

2. **Login with Credentials**
   - Enter your admin username and password
   - Complete reCAPTCHA verification

3. **Manage FAQs**
   - **Add**: Fill in question and answer, click "Add FAQ"
   - **View**: Click "Refresh List" to see all FAQs
   - **Edit**: Click "Edit" button on any FAQ
   - **Delete**: Click "Delete" button with confirmation

4. **Configure Bot Settings**
   - Switch to "Bot Settings" tab
   - Choose response style (Short or Conversational)
   - Set priority mode (Database First or AI Supplement)
   - Adjust context window size
   - Click "Save Settings"

**For detailed admin features, see [ADMIN_SETUP.md](ADMIN_SETUP.md)**

## 🌐 Deployment

### Vercel Deployment (Recommended)

**📘 For complete step-by-step deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

This project is optimized for deployment on Vercel using **FastAPI (Python)**. The `index.js` (Express/Node.js) file is an alternative local option and is **NOT used for Vercel deployment**.

#### Quick Deployment Steps:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Import Project"
   - Select your GitHub repository

3. **Configure Environment Variables**
   Add all required variables in Vercel Settings → Environment Variables:
   - `GROQ_API_KEY` (required)
   - `SUPABASE_URL` (required)
   - `SUPABASE_KEY` (required)
   - `ADMIN_USERNAME` (required)
   - `ADMIN_PASSWORD` (required)
   - `RECAPTCHA_SECRET_KEY` (optional)

4. **Deploy**
   - Vercel will automatically deploy using `vercel.json` configuration
   - Access at: `https://your-project.vercel.app`

**⚠️ Important:** 
- You do NOT need to configure Node.js separately for Vercel
- The deployment uses only Python FastAPI (`api/app.py`)
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting

## 🔌 API Endpoints

### Public Endpoints

#### `POST /ask`
Send a question to the chatbot
```json
Request:
{
  "message": "What are your VPS hosting plans?"
}

Response:
{
  "answer": "Here are our VPS plans..."
}
```

#### `GET /`
Main chatbot interface (HTML)

#### `GET /debug-paths`
Debug endpoint to verify file paths and configurations

### Admin Endpoints

#### `GET /login`
Admin login page

#### `POST /login`
Authenticate admin
```
Form Data:
- username
- password
- g-recaptcha-response
```

#### `GET /admin-zt`
Admin panel (requires authentication)

#### `POST /add-faq`
Add manual FAQ (requires authentication)
```json
{
  "question": "What is your refund policy?",
  "answer": "We offer 30-day money back guarantee..."
}
```

#### `GET /get-faqs`
List all FAQs (requires authentication)
```json
Response:
{
  "status": "success",
  "faqs": [
    {"id": 1, "question": "...", "answer": "..."},
    ...
  ]
}
```

#### `PUT /update-faq`
Update existing FAQ (requires authentication)
```json
{
  "id": 1,
  "question": "Updated question?",
  "answer": "Updated answer..."
}
```

#### `DELETE /delete-faq`
Delete FAQ (requires authentication)
```json
{
  "id": 1
}
```

#### `GET /get-settings`
Get current bot settings (requires authentication)
```json
Response:
{
  "status": "success",
  "settings": {
    "response_style": "short",
    "priority": "database_first",
    "context_size": 4000
  }
}
```

#### `POST /save-settings`
Update bot settings (requires authentication)
```json
{
  "response_style": "conversational",
  "priority": "ai_supplement",
  "context_size": 6000
}
```

#### `GET /logout`
Logout admin session

## 🧠 How It Works

### Question Processing Flow

1. **User Input**: Question received via `/ask` endpoint
2. **Load Settings**: Retrieves bot configuration from Supabase (response style, priority mode, context size)
3. **Database Check**: Searches manual FAQs in Supabase
   - **Database First Mode**: Returns immediately if FAQ matches
   - **AI Supplement Mode**: Collects FAQ context to combine with AI
4. **File Routing**: Identifies relevant knowledge base file based on keywords:
   - "reseller" → `reseller_hosting.txt`
   - "domain" → `domain_registration.txt`
   - "vps" → `pro_vps_hosting.txt`
   - "wordpress" → `pro_wordpress_hosting.txt`
   - etc.
5. **Context Loading**: Loads relevant file content (dynamic size from settings)
6. **AI Processing**: Sends to Groq LLM with style-specific prompt
7. **Response Formatting**: Returns formatted answer with bold pricing

### Key Technologies

- **FastAPI**: Modern async web framework
- **LangChain**: LLM application framework
- **Groq**: High-speed LLM inference
- **Supabase**: PostgreSQL database
- **ChromaDB**: Vector database for embeddings (optional)
- **reCAPTCHA**: Bot protection for admin login

## 📝 Configuration

### Supported Groq Models
Current: `llama-3.1-8b-instant`

Other options:
- `llama-3.3-70b-versatile` (higher accuracy, more tokens)
- `mixtral-8x7b-32768` (larger context window)

### Context Limits
- Default: 4000 characters per query
- Adjustable via Admin Dashboard: 2000/4000/6000 characters
- Setting is applied dynamically on each request

### Temperature Setting
- Current: 0.1 (more deterministic and factual responses, reduces randomness and hallucinations)
- Range: 0.0 - 1.0

## 🔧 Customization

### Adding New Knowledge Base Files
1. Create new `.txt` file in `data/` directory
2. Add keyword routing in `api/app.py`:
```python
elif "your_keyword" in user_input:
    file_name = "your_new_file.txt"
```

### Customizing AI Behavior
Modify the system prompt in `api/app.py` (line 2989-2997):
```python
system_prompt = (
    "You are ZT Hosting Support assistant. Answer ONLY based on the provided context. "
    "### CRITICAL INSTRUCTION for Pricing: ### "
    "1. For any plan price, FIRST look at the Markdown Tables. "
    "2. If a table shows a '$1/1st month' offer, you MUST mention it. Do not just say the PKR price. "
    "3. Format pricing clearly: 'Promo: **$1 for the 1st month**, Renewing at: **PKR [Price]**'. "
    "4. If info like 'cPanel accounts' or 'SSD Storage' is in a table, extract it accurately from the correct column. "
    "5. If you cannot find the answer in the provided text, say 'I am sorry, I don't have this information yet.'"
)
```

### Adding Manual FAQs
1. Login to admin panel: `/login`
2. Go to admin dashboard: `/admin-zt`
3. Add question and answer
4. FAQs are stored in Supabase and have priority over AI

## 🐛 Troubleshooting

### Common Issues

**Issue**: "GROQ_API_KEY is not set"
- **Solution**: Add `GROQ_API_KEY` to `.env` file or Vercel environment variables

**Issue**: "Knowledge base file is missing"
- **Solution**: Ensure all `.txt` files exist in `data/` directory

**Issue**: "Database folder not found"
- **Solution**: Run `python ingest.py` or ensure manual FAQs in Supabase

**Issue**: Rate limit errors (429)
- **Solution**: Wait 10 minutes or upgrade Groq API plan

**Issue**: Token limit exceeded (413)
- **Solution**: Reduce context limit in code or ask shorter questions

## 📊 Data Sources

The chatbot's knowledge base includes:
- ZT Hosting website content
- Pricing tables
- Service specifications
- Contact information
- Terms and policies

Data is periodically scraped using `crawler.py` with FireCrawl API.

**Note**: Some data files may have formatting variations (e.g., content on single lines). The chatbot handles these variations automatically during processing.

## 🔒 Security

- **Authentication**: Cookie-based sessions for admin
- **reCAPTCHA**: Protects login from bots
- **Environment Variables**: Sensitive data stored securely
- **CORS**: Configurable origins
- **HttpOnly Cookies**: Prevents XSS attacks

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Chat history tracking
- [ ] Analytics dashboard
- [ ] Email notifications for admin
- [ ] Live chat handoff
- [ ] Voice input support
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License.

## 👥 Author

**Fatima**
- GitHub: [@fatima678](https://github.com/fatima678)

## 🙏 Acknowledgments

- Groq for fast LLM inference
- LangChain for LLM orchestration
- Supabase for database services
- Vercel for hosting platform
- ZT Hosting for the business case

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/fatima678/ZT-Hosting-chatbot/issues)
- Email: Contact through ZT Hosting website

---

**Built with ❤️ for ZT Hosting**
