# 🎯 Quick Start: Deploy to Vercel in 10 Minutes

**New to deployment?** Follow this simplified guide to get your chatbot live in ~10 minutes.

---

## What You'll Deploy

This is a **FastAPI (Python)** chatbot application. You do **NOT** need Node.js for Vercel deployment.

**Files that matter:**
- ✅ `api/app.py` - Your main application (Python/FastAPI)
- ✅ `vercel.json` - Deployment configuration
- ✅ `requirements.txt` - Python dependencies
- ❌ `index.js` - NOT used for Vercel (ignore this)
- ❌ `package.json` - NOT used for Vercel (ignore this)

---

## Step-by-Step (10 Minutes)

### ⏱️ 2 Minutes: Get API Keys

1. **Groq**: Go to [console.groq.com](https://console.groq.com) → Sign up → Create API key
2. **Supabase**: Go to [supabase.com](https://supabase.com) → New project → Copy URL and API key

### ⏱️ 3 Minutes: Setup Database

1. Open your Supabase project → **SQL Editor**
2. Copy-paste this SQL and click **RUN**:

```sql
CREATE TABLE manual_faqs (
    id BIGSERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE TABLE bot_settings (
    id BIGSERIAL PRIMARY KEY,
    response_style TEXT NOT NULL DEFAULT 'short',
    priority TEXT NOT NULL DEFAULT 'database_first',
    context_size INTEGER NOT NULL DEFAULT 4000,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

INSERT INTO bot_settings (response_style, priority, context_size)
VALUES ('short', 'database_first', 4000);
```

### ⏱️ 3 Minutes: Deploy on Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. **Before clicking Deploy**, add these environment variables:

   | Variable | Where to get it |
   |----------|-----------------|
   | `GROQ_API_KEY` | From Groq dashboard |
   | `SUPABASE_URL` | From Supabase Settings → API |
   | `SUPABASE_KEY` | From Supabase Settings → API (use service_role key) |
   | `ADMIN_USERNAME` | Choose any username (e.g., `admin`) |
   | `ADMIN_PASSWORD` | Choose a strong password |

5. Click **"Deploy"**
6. Wait 1-2 minutes ⏳

### ⏱️ 2 Minutes: Verify It Works

1. Click on your deployment URL
2. You should see the chatbot interface 🎉
3. Type a question like "What are your hosting plans?"
4. Get a response from the AI ✅

---

## ✅ Success!

Your chatbot is now live at `https://your-project.vercel.app`

**Admin Panel:** Visit `https://your-project.vercel.app/login` to manage FAQs

---

## 🚨 Something Not Working?

### Error: 500 Internal Server Error
→ Check that all 5 environment variables are set correctly in Vercel

### Error: GROQ_API_KEY not configured
→ Go to Vercel Settings → Environment Variables → Add `GROQ_API_KEY` → Redeploy

### Database connection failed
→ Verify you used the `service_role` key (not `anon` key) from Supabase

### Still stuck?
→ Read the detailed guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📚 What's Next?

- ✅ Customize chatbot responses
- ✅ Add FAQs via admin panel
- ✅ Configure bot settings
- ✅ Add a custom domain (optional)

---

**Need the full guide?** → [DEPLOYMENT.md](DEPLOYMENT.md)  
**Checklist to follow?** → [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
