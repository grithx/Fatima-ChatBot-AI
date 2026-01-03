# 🔧 Troubleshooting Guide - Common Vercel Deployment Errors

This guide covers the most common errors you might encounter when deploying the Fatima ChatBot AI on Vercel and how to fix them.

---

## Error 1: 500 Internal Server Error

### Symptoms
- Deployment succeeds but visiting the site shows "500 INTERNAL_SERVER_ERROR"
- Function logs show generic error messages

### Common Causes & Solutions

#### ❌ Missing Environment Variables
**Check:** All 5 required environment variables must be set

**Solution:**
1. Go to Vercel Dashboard → Your Project → **Settings** → **Environment Variables**
2. Verify these exist:
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
3. If any are missing, add them
4. Go to **Deployments** → Click **Redeploy** on the latest deployment

#### ❌ Wrong Environment Variable Values
**Check:** Values are correct and have no extra spaces

**Solution:**
1. Verify `GROQ_API_KEY` is valid (test at [console.groq.com](https://console.groq.com))
2. Verify `SUPABASE_URL` format: `https://xxxxx.supabase.co`
3. Verify `SUPABASE_KEY` is the `service_role` key (not `anon` key)
4. Redeploy after corrections

---

## Error 2: "GROQ_API_KEY is not configured"

### Symptoms
- Error message specifically mentions GROQ_API_KEY
- Chatbot doesn't respond to questions

### Solution

**Step 1:** Add the missing variable
1. Go to Vercel → Settings → Environment Variables
2. Add new variable:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key from [console.groq.com](https://console.groq.com)
   - **Environments**: Select all (Production, Preview, Development)

**Step 2:** Redeploy
1. Go to **Deployments** tab
2. Find the latest deployment
3. Click the three dots (**...**) → **Redeploy**
4. Wait for deployment to complete

---

## Error 3: Database Connection Failed

### Symptoms
- `/health` endpoint shows `"database": "not_configured"`
- Admin panel doesn't work
- FAQs don't load

### Common Causes & Solutions

#### ❌ Wrong Supabase Key Type
**Problem:** Using `anon` key instead of `service_role` key

**Solution:**
1. Go to Supabase → Your Project → **Settings** → **API**
2. Find the **`service_role`** key (not the `anon` key)
3. Copy the full key
4. Update `SUPABASE_KEY` in Vercel environment variables
5. Redeploy

#### ❌ Supabase Project Paused
**Problem:** Free tier projects pause after inactivity

**Solution:**
1. Go to your Supabase project dashboard
2. If you see "Project Paused", click **Resume**
3. Wait for project to activate
4. Test your Vercel deployment again

#### ❌ Tables Not Created
**Problem:** Database tables don't exist

**Solution:**
1. Go to Supabase → SQL Editor
2. Run the table creation SQL from [DEPLOYMENT.md](DEPLOYMENT.md#12-create-required-tables)
3. Verify tables exist in **Database** → **Tables**

---

## Error 4: Function Timeout

### Symptoms
- Deployment shows "FUNCTION_INVOCATION_TIMEOUT"
- Some requests work, others timeout
- Logs show incomplete execution

### Solutions

**Solution 1: Reduce Context Size**
1. Login to admin panel
2. Go to "Bot Settings" tab
3. Change context size from 6000 to 4000 or 2000
4. Click "Save Settings"

**Solution 2: Check Groq API Status**
1. Verify Groq API is not experiencing outages
2. Check your rate limits at [console.groq.com](https://console.groq.com)
3. Consider upgrading if hitting free tier limits

**Solution 3: Optimize Query**
- Ask shorter questions
- Avoid very complex queries

---

## Error 5: "Knowledge base file is missing"

### Symptoms
- Error mentions missing `.txt` files
- `/debug-paths` shows `"data_exists": false`

### Solutions

**Check File Structure:**
1. Visit your GitHub repository
2. Verify `data/` folder exists in root
3. Verify data files exist (e.g., `data/zt_data.txt` or individual service files)

**If Files Missing:**
1. Add the missing files to your repository
2. Commit and push to GitHub
3. Vercel will automatically redeploy

**Check Paths:**
1. Visit `https://your-domain.vercel.app/debug-paths`
2. Check which files are missing
3. Add them to the correct location

---

## Error 6: Admin Panel Shows Blank/White Page

### Symptoms
- Login succeeds but admin page is blank
- Browser console shows errors

### Solutions

**Solution 1: Check Template Files**
1. Verify `templates/admin.html` exists in repository
2. Check the file is not corrupted (valid HTML)

**Solution 2: Clear Browser Cache**
1. Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. Or clear browser cache completely

**Solution 3: Check Browser Console**
1. Press `F12` to open developer tools
2. Go to **Console** tab
3. Look for JavaScript errors
4. Report specific errors in GitHub issues

---

## Error 7: reCAPTCHA Not Loading

### Symptoms
- Login page shows no reCAPTCHA checkbox
- Can't complete login

### Solutions

**If reCAPTCHA is Optional for You:**
1. Simply don't set `RECAPTCHA_SECRET_KEY` in Vercel
2. The app will work without it (less secure but functional)

**If You Want reCAPTCHA:**
1. Register your site at [google.com/recaptcha/admin](https://www.google.com/recaptcha/admin)
2. Choose reCAPTCHA v2 (Checkbox)
3. Add your Vercel domain to allowed domains
4. Add `RECAPTCHA_SECRET_KEY` to Vercel environment variables
5. Update `templates/login.html` with your reCAPTCHA Site Key

---

## Error 8: Build/Deployment Fails

### Symptoms
- Deployment never completes
- Error during build phase
- Red error in deployment logs

### Solutions

**Check Python Version:**
1. Verify `runtime.txt` contains `python-3.11`
2. This is the version Vercel will use

**Check Requirements:**
1. Verify `requirements.txt` has all dependencies
2. No syntax errors in the file
3. All packages are available on PyPI

**Check Import Errors:**
1. Review deployment logs for "ModuleNotFoundError"
2. Add missing packages to `requirements.txt`
3. Redeploy

---

## Error 9: CORS Errors in Browser Console

### Symptoms
- Browser console shows "CORS policy" errors
- Frontend can't communicate with backend

### Solution

**For Vercel Deployment:**
- The FastAPI app already has CORS configured to allow all origins
- This should not be an issue on Vercel
- If it persists, check that requests are going to the correct domain

---

## Error 10: Rate Limit Errors (429)

### Symptoms
- Error message: "Rate limit exceeded"
- Chatbot stops responding after several queries
- Groq API returns 429 status

### Solutions

**Free Tier Limits:**
1. Groq free tier has rate limits
2. Wait 10-15 minutes before trying again
3. Consider upgrading to paid tier for higher limits

**Reduce Requests:**
1. Lower context size in bot settings
2. Reduce frequency of queries
3. Monitor usage at [console.groq.com](https://console.groq.com)

---

## General Debugging Steps

When encountering any error:

### 1. Check Vercel Function Logs
1. Go to Vercel Dashboard → Your Project
2. Click on the latest deployment
3. Go to **Functions** tab
4. Review logs for detailed error messages

### 2. Test Debug Endpoints
Visit these endpoints to gather information:
- `/health` - Check service status
- `/debug-paths` - Verify file paths

### 3. Verify Environment Variables
1. Settings → Environment Variables
2. Check all required variables exist
3. Verify no typos in variable names
4. Ensure values are correct (no quotes, no extra spaces)

### 4. Review Recent Changes
- What changed since last working version?
- Did you add new dependencies?
- Did you modify critical files?

### 5. Check External Services
- Is Groq API working? → [console.groq.com](https://console.groq.com)
- Is Supabase active? → Your Supabase dashboard
- Any service outages?

---

## Still Stuck?

If none of these solutions work:

1. **Collect Information:**
   - Exact error message
   - Steps to reproduce
   - Screenshots of Vercel logs
   - Environment variable names (not values!)

2. **Create a GitHub Issue:**
   - Go to repository → Issues → New Issue
   - Provide all collected information
   - Include what you've tried already

3. **Check Existing Issues:**
   - Someone might have had the same problem
   - Look through closed issues too

---

## Quick Reference: Vercel Environment Variables

Required variables (must be set):

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_strong_password_here
```

Optional variable:

```
RECAPTCHA_SECRET_KEY=6Lfxxxxxxxxxxxxxxxxxxxxxxx
```

---

**Need more help?** Check the [Complete Deployment Guide](DEPLOYMENT.md) or [Quick Start](QUICKSTART.md)
