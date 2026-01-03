import os 
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Try relative imports first (for Vercel serverless)
    from response_formatter import ResponseFormatter
    from output_parser import FormattedOutputParser
except ImportError:
    # Fallback to absolute imports (for local development)
    from response_formatter import ResponseFormatter
    from output_parser import FormattedOutputParser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Better Path Configuration ---
CURRENT_FILE = Path(__file__).resolve()
API_DIR = CURRENT_FILE.parent
BASE_DIR = API_DIR.parent 

DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
HTML_PATH = BASE_DIR / "templates" / "index.html"
ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# Environment Variables
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

# Clients Setup - Lazy initialization to prevent startup crashes
_supabase_client = None

def get_supabase() -> Client:
    """
    Lazy initialization of Supabase client.
    Returns None if environment variables are not configured or if initialization fails.
    """
    global _supabase_client
    if _supabase_client is None:
        supabase_url = os.environ.get("SUPABASE_URL", "")
        supabase_key = os.environ.get("SUPABASE_KEY", "")
        if supabase_url and supabase_key:
            try:
                _supabase_client = create_client(supabase_url, supabase_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Supabase client: {e}")
                return None
        else:
            logger.info("SUPABASE_URL or SUPABASE_KEY not configured - database features disabled")
            return None
    return _supabase_client

def get_llm():
    """
    Get ChatGroq LLM instance.
    Raises ValueError if GROQ_API_KEY is not configured.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not configured. "
            "Please set GROQ_API_KEY in your Vercel environment variables."
        )
    
    return ChatGroq(
        groq_api_key=groq_api_key, 
        # Updated to a currently supported model
        model_name="llama-3.1-8b-instant", 
        temperature=0.1 
    )

# --- Auth Helper ---
def check_auth(request: Request):
    return request.cookies.get("admin_session") == "active"

# --- Debug Route ---
@app.get("/debug-paths")
async def debug_paths():
    return {
        "current_file": str(CURRENT_FILE),
        "base_dir": str(BASE_DIR),
        "data_path_exists": DATA_PATH.exists(),
        "data_path_full": str(DATA_PATH),
        "templates_exist": {
            "index": HTML_PATH.exists(),
            "admin": ADMIN_HTML_PATH.exists()
        }
    }

# --- Health Check Route ---
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment verification"""
    supabase = get_supabase()
    return {
        "status": "ok",
        "database": "connected" if supabase else "not_configured",
        "groq_api": "configured" if os.environ.get("GROQ_API_KEY") else "not_configured",
        "data_files": DATA_PATH.exists()
    }

# # --- AI & Main Routes ---

@app.post("/ask")
async def ask_bot(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "").lower().strip()
        if not user_input:
            return {"answer": "Aapka sawal kya hai?"}

        # --- LOAD BOT SETTINGS ---
        supabase = get_supabase()
        try:
            if supabase:
                settings_res = supabase.table("bot_settings").select("*").limit(1).execute()
                if settings_res.data and len(settings_res.data) > 0:
                    settings = settings_res.data[0]
                    response_style = settings.get("response_style", "short")
                    priority = settings.get("priority", "database_first")
                    context_size = settings.get("context_size", 4000)
                else:
                    # Defaults
                    response_style = "short"
                    priority = "database_first"
                    context_size = 4000
            else:
                # Defaults if Supabase not configured
                response_style = "short"
                priority = "database_first"
                context_size = 4000
        except:
            # Defaults if table doesn't exist yet
            response_style = "short"
            priority = "database_first"
            context_size = 4000

        # --- STEP 1: DATABASE CHECK ---
        db_res = None
        db_context = ""  # Initialize db_context
        if supabase:
            try:
                db_res = supabase.table("manual_faqs").select("question, answer").execute()
            except Exception:
                db_res = None
        
        if priority == "database_first" and db_res and db_res.data:
            # Strict database priority - return immediately on match
            for row in db_res.data:
                if row['question'].lower() in user_input:
                    # Apply OutputParser to database answers too
                    output_parser = FormattedOutputParser(style=response_style, user_input=user_input)
                    result = output_parser.parse(row['answer'])
                    return {
                        "answer": result["final_text"],
                        "metadata": {
                            "tokens_used": result["tokens_used"],
                            "truncated": result["truncated"],
                            "source": "database"
                        }
                    }
        elif db_res and db_res.data:
            # AI supplement mode - collect DB context but don't return yet
            for row in db_res.data:
                if row['question'].lower() in user_input:
                    db_context = f"Database Info: {row['answer']}\n\n"
                    break

        # --- STEP 2: SMART FILE ROUTING ---
        # Default file: Agar koi specific keyword na mile toh home page ya general info use karein
        file_name = "zt_home_page.txt" 
        
        if "reseller" in user_input:
            file_name = "reseller_hosting.txt"
        elif any(x in user_input for x in ["domain", ".pk", ".com", "register"]):
            file_name = "domain_registration.txt"
        elif "vps" in user_input:
            file_name = "pro_vps_hosting.txt"
        elif "business" in user_input:
            file_name = "pro_hosting_business_web.txt"
        elif "wordpress" in user_input:
            file_name = "pro_wordpress_hosting.txt"
        elif "email" in user_input:
            file_name = "pro_email_hosting.txt"
        elif "dedicated" in user_input:
            file_name = "pro_dedicated_servers.txt"
        elif "promo" in user_input or "offer" in user_input:
            file_name = "promo_packages.txt"
        elif "shared" in user_input or "web hosting" in user_input:
            file_name = "shared_webhosting.txt"

        target_path = BASE_DIR / "data" / file_name
        
        # Sirf tabhi parhein agar file exist karti ho
        if target_path.exists():
            # Use dynamic context size from settings
            file_context = target_path.read_text(encoding="utf-8")[:context_size]
        else:
            return {"answer": "I am sorry, I don't have specific details about this service yet."}

        # --- STEP 3: AI PROCESSING ---
        llm = get_llm()
        
        # Build system prompt based on response style
        if response_style == "conversational":
            system_prompt = (
                "You are a friendly and helpful ZT Hosting Support assistant. "
                "Answer in a conversational, human-like tone with warmth and empathy. "
                "Feel free to use greetings and be detailed in your explanations. "
                "### CRITICAL INSTRUCTION for Pricing: ### "
                "1. For any plan price, FIRST look at the Markdown Tables. "
                "2. If a table shows a '$1/1st month' offer, you MUST mention it with enthusiasm. "
                "3. Format pricing clearly: 'Great news! You can start with just **$1 for the 1st month**, "
                "and then it renews at **PKR [Price]**'. "
                "4. If info like 'cPanel accounts' or 'SSD Storage' is in a table, extract it accurately. "
                "5. If you cannot find the answer, politely say 'I apologize, but I don't have that specific "
                "information at the moment. Let me connect you with our support team who can help you better.'"
            )
        else:
            # Short and professional
            system_prompt = (
                "You are ZT Hosting Support assistant. Answer ONLY based on the provided context. "
                "Keep responses concise and to-the-point. "
                "### CRITICAL INSTRUCTION for Pricing: ### "
                "1. For any plan price, FIRST look at the Markdown Tables. "
                "2. If a table shows a '$1/1st month' offer, you MUST mention it. Do not just say the PKR price. "
                "3. Format pricing clearly: 'Promo: **$1 for the 1st month**, Renewing at: **PKR [Price]**'. "
                "4. If info like 'cPanel accounts' or 'SSD Storage' is in a table, extract it accurately from the correct column. "
                "5. If you cannot find the answer in the provided text, say 'I am sorry, I don't have this information yet.'"
            )
        
        # Combine contexts if in AI supplement mode and db_context exists
        if priority == "ai_supplement" and db_context:
            context_text = db_context + file_context
        else:
            context_text = file_context
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", f"Context: {context_text}\n\nQuestion: {user_input}")
        ])

        # Create OutputParser with current settings
        output_parser = FormattedOutputParser(style=response_style, user_input=user_input)
        
        # Wire OutputParser into chain via RunnableSequence
        chain = prompt | llm | output_parser
        
        # Invoke the chain - parser returns structured output
        result = chain.invoke({"input": user_input})
        
        # Return the formatted text with metadata
        return {
            "answer": result["final_text"],
            "metadata": {
                "tokens_used": result["tokens_used"],
                "truncated": result["truncated"]
            }
        }

    except ValueError as ve:
        # Handle missing API keys
        if "GROQ_API_KEY" in str(ve):
            return {"answer": "Service configuration error. Please contact the administrator."}
        return {"answer": f"Configuration Error: {str(ve)}"}
    except Exception as e:
        # Code 413 or 429 management
        if "413" in str(e) or "limit" in str(e).lower():
            return {"answer": "The request is too large or system is busy. Please try asking a shorter question."}
        if "429" in str(e):
            return {"answer": "System is busy. Please try again in a few minutes."}
        # Log error for debugging (will appear in Vercel logs)
        logger.error(f"Error in /ask endpoint: {str(e)}", exc_info=True)
        return {"answer": "I apologize, but I'm having trouble processing your request. Please try again."}


# --- Routes for UI (Baqi routes same rahenge) ---
@app.get("/", response_class=HTMLResponse)
async def get_home():
    if HTML_PATH.exists(): return HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Chatbot Home</h1>"

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    if LOGIN_HTML_PATH.exists(): return LOGIN_HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Login Page Missing</h1>"

@app.post("/login")
async def do_login(username: str = Form(...), password: str = Form(...), g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")):
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    res = requests.post(verify_url, data={"secret": RECAPTCHA_SECRET_KEY, "response": g_recaptcha_response}).json()
    if not res.get("success"): return HTMLResponse("<h2>Captcha Failed!</h2>", status_code=400)
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin-zt", status_code=303)
        response.set_cookie(key="admin_session", value="active", httponly=True, secure=True, samesite="lax")
        return response
    return HTMLResponse("<h2>Invalid Credentials!</h2>", status_code=401)

@app.get("/admin-zt", response_class=HTMLResponse)
async def get_admin(request: Request):
    if not check_auth(request): return RedirectResponse(url="/login", status_code=303)
    if ADMIN_HTML_PATH.exists(): return ADMIN_HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Admin Page Missing</h1>"

@app.post("/add-faq")
async def add_faq(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    
    if not question or not answer:
        return {"status": "error", "message": "Question and answer are required"}
    
    if len(question) > 500:
        return {"status": "error", "message": "Question too long (max 500 characters)"}
    
    if len(answer) > 5000:
        return {"status": "error", "message": "Answer too long (max 5000 characters)"}
    
    try:
        supabase = get_supabase()
        if not supabase:
            return {"status": "error", "message": "Database not configured"}
        supabase.table("manual_faqs").insert({"question": question.lower(), "answer": answer}).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.get("/get-faqs")
async def get_faqs(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    try:
        supabase = get_supabase()
        if not supabase:
            return {"status": "error", "message": "Database not configured"}
        response = supabase.table("manual_faqs").select("*").order("id", desc=True).execute()
        return {"status": "success", "faqs": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.put("/update-faq")
async def update_faq(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    faq_id = data.get("id")
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    
    if not isinstance(faq_id, int) or faq_id <= 0:
        return {"status": "error", "message": "Invalid FAQ ID"}
    
    if not question or not answer:
        return {"status": "error", "message": "Question and answer are required"}
    
    if len(question) > 500:
        return {"status": "error", "message": "Question too long (max 500 characters)"}
    
    if len(answer) > 5000:
        return {"status": "error", "message": "Answer too long (max 5000 characters)"}
    
    try:
        supabase = get_supabase()
        if not supabase:
            return {"status": "error", "message": "Database not configured"}
        supabase.table("manual_faqs").update({
            "question": question.lower(),
            "answer": answer
        }).eq("id", faq_id).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.delete("/delete-faq")
async def delete_faq(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    faq_id = data.get("id")
    
    if not isinstance(faq_id, int) or faq_id <= 0:
        return {"status": "error", "message": "Invalid FAQ ID"}
    
    try:
        supabase = get_supabase()
        if not supabase:
            return {"status": "error", "message": "Database not configured"}
        supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.get("/get-settings")
async def get_settings(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    try:
        supabase = get_supabase()
        if not supabase:
            # Return defaults if Supabase not configured
            return {
                "status": "success",
                "settings": {
                    "response_style": "short",
                    "priority": "database_first",
                    "context_size": 4000
                }
            }
        response = supabase.table("bot_settings").select("*").limit(1).execute()
        if response.data and len(response.data) > 0:
            return {"status": "success", "settings": response.data[0]}
        else:
            # Return defaults
            return {
                "status": "success",
                "settings": {
                    "response_style": "short",
                    "priority": "database_first",
                    "context_size": 4000
                }
            }
    except Exception as e:
        # Return defaults on error
        return {
            "status": "success",
            "settings": {
                "response_style": "short",
                "priority": "database_first",
                "context_size": 4000
            }
        }

@app.post("/save-settings")
async def save_settings(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    response_style = data.get("response_style")
    priority = data.get("priority")
    context_size = data.get("context_size")
    
    # Validate response_style
    if response_style not in ["short", "conversational"]:
        return {"status": "error", "message": "Invalid response_style"}
    
    # Validate priority
    if priority not in ["database_first", "ai_supplement"]:
        return {"status": "error", "message": "Invalid priority"}
    
    # Validate context_size
    if not isinstance(context_size, int) or context_size not in [2000, 4000, 6000]:
        return {"status": "error", "message": "Invalid context_size"}
    
    try:
        supabase = get_supabase()
        if not supabase:
            return {"status": "error", "message": "Database not configured"}
        # Check if settings exist
        existing = supabase.table("bot_settings").select("*").limit(1).execute()
        
        settings_data = {
            "response_style": response_style,
            "priority": priority,
            "context_size": context_size
        }
        
        if existing.data and len(existing.data) > 0:
            # Update existing
            supabase.table("bot_settings").update(settings_data).eq("id", existing.data[0]["id"]).execute()
        else:
            # Insert new
            supabase.table("bot_settings").insert(settings_data).execute()
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("admin_session")
    return response