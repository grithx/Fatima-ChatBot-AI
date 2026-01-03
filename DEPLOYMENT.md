# Deployment Guide for Fatima ChatBot AI

This guide explains how to deploy the ZT Hosting ChatBot AI on Vercel.

## Prerequisites

Before deploying, ensure you have:
1. A Vercel account
2. A Groq API key (for the LLM)
3. A Supabase project (for database)
4. Google reCAPTCHA keys (for admin login protection)

## Environment Variables

Configure the following environment variables in your Vercel project settings:

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key for the LLM |
| `SUPABASE_URL` | Yes | Your Supabase project URL |
| `SUPABASE_KEY` | Yes | Your Supabase service role key |
| `ADMIN_USERNAME` | Yes | Admin panel username |
| `ADMIN_PASSWORD` | Yes | Admin panel password |
| `RECAPTCHA_SECRET_KEY` | No | Google reCAPTCHA secret key for login protection |

### How to Set Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable listed above
4. Select the environments (Production, Preview, Development) where each variable should be available
5. Click **Save**

## Supabase Database Setup

Create the following tables in your Supabase project:

### Table: `manual_faqs`

```sql
CREATE TABLE manual_faqs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Table: `bot_settings`

```sql
CREATE TABLE bot_settings (
    id SERIAL PRIMARY KEY,
    response_style TEXT DEFAULT 'short',
    priority TEXT DEFAULT 'database_first',
    context_size INTEGER DEFAULT 4000
);
```

## Vercel Configuration

The project includes a `vercel.json` file that configures:
- Python runtime using `@vercel/python`
- Routes all requests to `api/app.py`

## Deployment Steps

1. **Connect to GitHub**: Link your Vercel project to this GitHub repository
2. **Configure Environment Variables**: Add all required variables in Vercel settings
3. **Deploy**: Vercel will automatically deploy on push to the main branch

## Verifying Deployment

After deployment, check these endpoints:

1. **Health Check**: `https://your-domain.vercel.app/health`
   - Returns the status of all services
   - Check if database and API are properly configured

2. **Debug Paths**: `https://your-domain.vercel.app/debug-paths`
   - Shows file paths and their existence status
   - Useful for debugging file-related issues

3. **Main Page**: `https://your-domain.vercel.app/`
   - Should display the chatbot interface

## Troubleshooting

### Error: 500 INTERNAL_SERVER_ERROR

This usually indicates:
1. **Missing Environment Variables**: Check that all required variables are set in Vercel
2. **Database Connection Issues**: Verify your Supabase URL and key are correct
3. **File Path Issues**: Check the `/debug-paths` endpoint to verify files exist

### Error: Function Timeout

Vercel serverless functions have a timeout limit. If you experience timeouts:
1. Reduce the `context_size` in bot settings
2. Ensure your Groq API is responsive

### Database Not Configured

If the health check shows `"database": "not_configured"`:
1. Verify `SUPABASE_URL` and `SUPABASE_KEY` are set correctly
2. Check that your Supabase project is active
3. Verify the API key has the correct permissions

## Security Notes

- **Never commit `.env` files** to the repository
- Use Vercel's environment variables for all secrets
- The `.env` file should be in `.gitignore`
- Use strong passwords for the admin panel
- Enable reCAPTCHA for additional login protection
