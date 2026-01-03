# Complete Step-by-Step Deployment Guide for Vercel

This guide provides **detailed step-by-step instructions** for deploying the Fatima ChatBot AI (ZT Hosting ChatBot) on Vercel.

## 🎯 Understanding the Project Architecture

**Important Clarification**: This project uses **FastAPI (Python)** as the main backend framework. The `index.js` (Express/Node.js) file is an alternative option that is **NOT used for Vercel deployment**. 

On Vercel, the deployment is configured via `vercel.json` to use only the Python FastAPI application (`api/app.py`). You do **NOT** need to configure Node.js separately.

### What Gets Deployed:
- ✅ **Python FastAPI** (`api/app.py`) - Main application
- ✅ **HTML Templates** (`templates/` folder)
- ✅ **Data Files** (`data/` folder with knowledge base)
- ❌ **Express.js** (`index.js`) - NOT used on Vercel

---

## 📋 Prerequisites

Before starting deployment, you need:

### 1. **Vercel Account** (Free)
   - Sign up at [https://vercel.com/signup](https://vercel.com/signup)
   - Use GitHub authentication for easier integration

### 2. **Groq API Key** (Free tier available)
   - Sign up at [https://console.groq.com](https://console.groq.com)
   - Create an API key from the dashboard
   - Copy and save your API key securely

### 3. **Supabase Account** (Free tier available)
   - Sign up at [https://supabase.com](https://supabase.com)
   - Create a new project
   - Note down your project URL and API key

### 4. **Google reCAPTCHA** (Optional but recommended)
   - Visit [https://www.google.com/recaptcha/admin](https://www.google.com/recaptcha/admin)
   - Register a new site (reCAPTCHA v2)
   - Save your Site Key and Secret Key

### 5. **GitHub Repository**
   - Fork or have access to this repository on GitHub

---

## 🗄️ Step 1: Set Up Supabase Database

Before deploying to Vercel, you need to configure your database:

### 1.1 Access Supabase SQL Editor

1. Go to your Supabase project dashboard
2. Click on **SQL Editor** in the left sidebar
3. Click **New Query**

### 1.2 Create Required Tables

Copy and paste the following SQL commands and click **RUN**:

```sql
-- Create manual_faqs table for storing custom Q&A
CREATE TABLE IF NOT EXISTS manual_faqs (
    id BIGSERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create bot_settings table for chatbot configuration
CREATE TABLE IF NOT EXISTS bot_settings (
    id BIGSERIAL PRIMARY KEY,
    response_style TEXT NOT NULL DEFAULT 'short',
    priority TEXT NOT NULL DEFAULT 'database_first',
    context_size INTEGER NOT NULL DEFAULT 4000,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Insert default settings (run only once)
INSERT INTO bot_settings (response_style, priority, context_size)
VALUES ('short', 'database_first', 4000)
ON CONFLICT (id) DO NOTHING;
```

### 1.3 Get Your Supabase Credentials

1. Go to **Project Settings** (gear icon) → **API**
2. Copy the following:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **Project API key** (use `service_role` key for server-side access)

---

## 🚀 Step 2: Deploy to Vercel

### 2.1 Import Your GitHub Repository

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** → **Project**
3. Select **Import Git Repository**
4. Choose your GitHub repository (authorize GitHub if needed)
5. Click **Import**

### 2.2 Configure Project Settings

On the project configuration screen:

1. **Framework Preset**: Select **Other** (Vercel will auto-detect from `vercel.json`)
2. **Root Directory**: Leave as `.` (root)
3. **Build Command**: Leave empty (not needed for serverless Python)
4. **Output Directory**: Leave empty

### 2.3 Add Environment Variables

**CRITICAL STEP**: Before clicking "Deploy", add all environment variables:

Click **Environment Variables** and add the following:

| Variable Name | Value | Required |
|--------------|-------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `SUPABASE_URL` | Your Supabase project URL | ✅ Yes |
| `SUPABASE_KEY` | Your Supabase service_role key | ✅ Yes |
| `ADMIN_USERNAME` | Choose admin username (e.g., `admin`) | ✅ Yes |
| `ADMIN_PASSWORD` | Choose strong admin password | ✅ Yes |
| `RECAPTCHA_SECRET_KEY` | Your Google reCAPTCHA secret key | ⚠️ Optional |

**Important Notes:**
- Select **Production**, **Preview**, and **Development** for all variables
- Never share these values publicly
- Use a strong password for `ADMIN_PASSWORD`

### 2.4 Deploy

1. After adding all environment variables, click **Deploy**
2. Wait for the deployment to complete (usually 1-3 minutes)
3. You'll see "Congratulations!" when it's done

---

## ✅ Step 3: Verify Your Deployment

### 3.1 Test the Main Chatbot Page

Visit: `https://your-project-name.vercel.app/`

**Expected Result**: You should see the chatbot interface

### 3.2 Test the Debug Endpoint

Visit: `https://your-project-name.vercel.app/debug-paths`

**Expected Result**: JSON response showing file paths and their status:
```json
{
  "base_dir": "/var/task",
  "data_path": "/var/task/data/zt_data.txt",
  "data_exists": true,
  "html_path": "/var/task/templates/index.html",
  "html_exists": true,
  ...
}
```

### 3.3 Test the Health Check

Visit: `https://your-project-name.vercel.app/health`

**Expected Result**:
```json
{
  "status": "healthy",
  "database": "configured",
  "groq_api": "configured"
}
```

### 3.4 Test the Chatbot Functionality

1. Go to the main page
2. Type a question like "What are your hosting plans?"
3. You should receive a response from the AI

### 3.5 Test the Admin Panel

1. Visit: `https://your-project-name.vercel.app/login`
2. Enter your `ADMIN_USERNAME` and `ADMIN_PASSWORD`
3. Complete the reCAPTCHA (if configured)
4. You should be redirected to the admin dashboard

---

## 🔧 Step 4: Understanding the Vercel Configuration

The `vercel.json` file in the repository configures the deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/app.py",
      "use": "@vercel/python"
    }
  ],
  "rewrites": [
    { "source": "/(.*)", "destination": "api/app.py" }
  ]
}
```

**What this does:**
- **builds**: Tells Vercel to use Python runtime for `api/app.py`
- **rewrites**: Routes all incoming requests to the FastAPI application
- **No Node.js configuration needed**: The Express.js code is not used

---

## 🛠️ Troubleshooting Common Issues

### Issue 1: "500 Internal Server Error"

**Possible Causes:**
- Missing environment variables
- Incorrect environment variable values
- Database connection issues

**Solutions:**
1. Check Vercel **Settings** → **Environment Variables**
2. Verify all required variables are set correctly
3. Redeploy the application after adding missing variables

### Issue 2: "GROQ_API_KEY is not configured"

**Solution:**
1. Go to Vercel project **Settings** → **Environment Variables**
2. Add `GROQ_API_KEY` with your Groq API key
3. Click **Save**
4. Go to **Deployments** → Click **Redeploy** on the latest deployment

### Issue 3: Database Connection Failed

**Check:**
1. Verify `SUPABASE_URL` is correct (should be `https://xxxxx.supabase.co`)
2. Verify `SUPABASE_KEY` is the `service_role` key (not `anon` key)
3. Ensure your Supabase project is active (not paused)

### Issue 4: "Knowledge base file is missing"

**Solution:**
1. Check the `/debug-paths` endpoint
2. Verify that `data_exists` is `true`
3. If false, check that the `data/` folder exists in your repository
4. Ensure `data/zt_data.txt` or individual data files exist

### Issue 5: Admin Panel Won't Load

**Solutions:**
1. Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD` are set in Vercel
2. Check that `templates/admin.html` exists in your repository
3. Try clearing browser cookies and cache

### Issue 6: reCAPTCHA Not Working

**Solutions:**
1. Verify `RECAPTCHA_SECRET_KEY` is set in Vercel environment variables
2. Check that the reCAPTCHA Site Key is correctly embedded in `templates/login.html`
3. Ensure your reCAPTCHA is configured for the correct domain

---

## 🔐 Security Best Practices

### Do's ✅
- Use strong, unique passwords for `ADMIN_PASSWORD`
- Enable reCAPTCHA for admin login
- Regularly rotate your API keys
- Use Vercel's environment variables (never commit secrets to Git)
- Monitor your Vercel deployment logs for unusual activity

### Don'ts ❌
- Never commit `.env` files to GitHub
- Never share your environment variables publicly
- Don't use weak passwords
- Don't use the same password across multiple services

---

## 🔄 Updating Your Deployment

### Automatic Deployments (Recommended)

When you push changes to your GitHub repository:
1. Vercel automatically detects the changes
2. Starts a new deployment
3. Your site updates automatically (usually within 1-2 minutes)

### Manual Deployments

If needed, you can manually redeploy:
1. Go to Vercel **Dashboard** → Your Project
2. Click **Deployments** tab
3. Click the three dots (**...**) on any deployment
4. Click **Redeploy**

### Updating Environment Variables

After updating environment variables:
1. Go to **Settings** → **Environment Variables**
2. Update the variable value
3. Click **Save**
4. Go to **Deployments** and **Redeploy** the latest deployment

---

## 📊 Monitoring Your Deployment

### View Deployment Logs

1. Go to Vercel **Dashboard** → Your Project
2. Click on a deployment
3. Click **Functions** tab to see serverless function logs
4. Check for errors or warnings

### Check Function Performance

1. In the deployment details, check **Function Duration**
2. Ensure functions complete within Vercel's timeout limits
3. Optimize if you see frequent timeouts

---

## ❓ Frequently Asked Questions

### Q1: Do I need to configure Node.js separately?

**A:** No! The project uses only Python FastAPI on Vercel. The `index.js` file is not used in production.

### Q2: What about the `package.json` and `node_modules`?

**A:** These are legacy files from an alternative setup. They don't affect Vercel deployment. You can safely ignore them.

### Q3: Can I use a custom domain?

**A:** Yes! In Vercel project settings:
1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Follow the DNS configuration instructions

### Q4: How much does Vercel cost?

**A:** Vercel offers a generous free tier (Hobby plan) that's sufficient for most small to medium projects. Check [Vercel Pricing](https://vercel.com/pricing) for details.

### Q5: What are Vercel's limits?

**A:** On the free tier:
- 100 GB bandwidth per month
- 100 serverless function executions per day (Hobby)
- 10 second function timeout
- Unlimited deployments

### Q6: Can I run this on another platform?

**A:** Yes! While optimized for Vercel, you can also deploy on:
- **Railway**: Supports Python apps
- **Render**: Has free tier for Python apps
- **PythonAnywhere**: Specialized Python hosting
- **DigitalOcean App Platform**: Supports FastAPI

---

## 📞 Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review Vercel deployment logs** for error messages
3. **Test the debug endpoints** (`/debug-paths`, `/health`)
4. **Create a GitHub issue** with:
   - Error message
   - Steps to reproduce
   - Screenshots of Vercel dashboard (hide sensitive info)

---

## 🎉 Success!

If all steps completed successfully:
- ✅ Your chatbot is live on Vercel
- ✅ Database is connected
- ✅ Admin panel is accessible
- ✅ AI is responding to questions

**Next Steps:**
- Customize the chatbot responses
- Add FAQs through the admin panel
- Configure bot settings (response style, priority, context size)
- Share your chatbot URL with users

---

**Need more help?** Check the main [README.md](README.md) for additional documentation and features.
