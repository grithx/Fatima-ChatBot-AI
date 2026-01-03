# 📋 Vercel Deployment Checklist

Use this checklist to ensure you complete all steps for successful deployment.

## Before You Start

- [ ] I have a GitHub account
- [ ] I have a Vercel account (free tier is fine)
- [ ] My code is pushed to a GitHub repository
- [ ] I have read the [DEPLOYMENT.md](DEPLOYMENT.md) guide

---

## 1️⃣ Get Your API Keys and Credentials

### Groq API Key
- [ ] Created account at [console.groq.com](https://console.groq.com)
- [ ] Generated API key
- [ ] Copied and saved the API key securely

### Supabase Setup
- [ ] Created account at [supabase.com](https://supabase.com)
- [ ] Created a new project
- [ ] Copied Project URL (from Settings → API)
- [ ] Copied service_role key (from Settings → API)

### Admin Credentials
- [ ] Decided on admin username (e.g., `admin`)
- [ ] Created a strong password for admin access

### reCAPTCHA (Optional)
- [ ] Registered site at [google.com/recaptcha/admin](https://www.google.com/recaptcha/admin)
- [ ] Copied reCAPTCHA secret key

---

## 2️⃣ Set Up Supabase Database

- [ ] Opened Supabase SQL Editor
- [ ] Created `manual_faqs` table using SQL from DEPLOYMENT.md
- [ ] Created `bot_settings` table using SQL from DEPLOYMENT.md
- [ ] Inserted default settings into `bot_settings`
- [ ] Verified tables exist in Database → Tables view

---

## 3️⃣ Deploy to Vercel

### Import Repository
- [ ] Logged into [vercel.com/dashboard](https://vercel.com/dashboard)
- [ ] Clicked "Add New" → "Project"
- [ ] Selected "Import Git Repository"
- [ ] Connected to GitHub (if not already connected)
- [ ] Selected the correct repository
- [ ] Clicked "Import"

### Configure Project
- [ ] Framework Preset: Selected "Other"
- [ ] Root Directory: Left as "." (root)
- [ ] Build Command: Left empty
- [ ] Output Directory: Left empty

### Add Environment Variables
- [ ] Clicked "Environment Variables" section
- [ ] Added `GROQ_API_KEY` with my Groq API key
- [ ] Added `SUPABASE_URL` with my Supabase project URL
- [ ] Added `SUPABASE_KEY` with my Supabase service_role key
- [ ] Added `ADMIN_USERNAME` with my chosen admin username
- [ ] Added `ADMIN_PASSWORD` with my chosen admin password
- [ ] Added `RECAPTCHA_SECRET_KEY` (if using reCAPTCHA)
- [ ] Selected "Production, Preview, Development" for all variables
- [ ] Double-checked all values are correct

### Deploy
- [ ] Clicked "Deploy" button
- [ ] Waited for deployment to complete (1-3 minutes)
- [ ] Saw "Congratulations!" message
- [ ] Copied the deployment URL

---

## 4️⃣ Verify Deployment

### Test Main Page
- [ ] Visited `https://your-project.vercel.app/`
- [ ] Saw the chatbot interface load correctly

### Test Debug Endpoint
- [ ] Visited `https://your-project.vercel.app/debug-paths`
- [ ] Confirmed `data_exists: true`
- [ ] Confirmed `html_exists: true`

### Test Health Check
- [ ] Visited `https://your-project.vercel.app/health`
- [ ] Confirmed `status: "healthy"`
- [ ] Confirmed `database: "configured"`
- [ ] Confirmed `groq_api: "configured"`

### Test Chatbot
- [ ] Asked a question in the chatbot
- [ ] Received a response from the AI
- [ ] Response was relevant and formatted correctly

### Test Admin Panel
- [ ] Visited `https://your-project.vercel.app/login`
- [ ] Entered admin username and password
- [ ] Completed reCAPTCHA (if enabled)
- [ ] Successfully logged into admin dashboard
- [ ] Admin panel loaded correctly

---

## 5️⃣ Final Configuration (Optional)

- [ ] Added FAQs through admin panel
- [ ] Configured bot settings (response style, priority, context size)
- [ ] Tested FAQ responses
- [ ] Configured custom domain (if desired)

---

## ✅ Success Criteria

Your deployment is successful if:
- ✅ Main page loads without errors
- ✅ Chatbot responds to questions
- ✅ Admin panel is accessible
- ✅ Health check shows all services configured
- ✅ No 500 errors when testing

---

## 🚨 If Something Went Wrong

If any check failed:

1. **Review the error message** in Vercel deployment logs
2. **Check environment variables** are set correctly
3. **Verify Supabase database** tables exist
4. **Consult troubleshooting section** in [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Check function logs** in Vercel dashboard
6. **Test debug endpoints** for more information

### Common Quick Fixes:
- Missing environment variable → Add it in Vercel Settings → Environment Variables → Redeploy
- Database error → Verify SUPABASE_URL and SUPABASE_KEY are correct
- 500 error → Check Vercel function logs for detailed error message

---

## 📞 Need Help?

- Read the detailed guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Check the main README: [README.md](README.md)
- Create a GitHub issue with your error message and steps to reproduce

---

**🎉 Once all checkboxes are complete, your deployment is ready for production use!**
