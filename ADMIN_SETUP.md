# Admin Dashboard Setup Guide

This guide will help you set up the enhanced admin dashboard with FAQ CRUD operations and bot settings management.

## Prerequisites

- Supabase account and project
- Existing `manual_faqs` table (should already exist from previous setup)

## Step 1: Create Bot Settings Table

Log in to your Supabase dashboard and run this SQL query:

```sql
-- Create bot_settings table
CREATE TABLE IF NOT EXISTS bot_settings (
  id BIGSERIAL PRIMARY KEY,
  response_style TEXT NOT NULL DEFAULT 'short',
  priority TEXT NOT NULL DEFAULT 'database_first',
  context_size INTEGER NOT NULL DEFAULT 4000,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Insert default settings
INSERT INTO bot_settings (response_style, priority, context_size)
VALUES ('short', 'database_first', 4000)
ON CONFLICT DO NOTHING;

-- Add updated_at trigger (optional but recommended)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_bot_settings_updated_at 
    BEFORE UPDATE ON bot_settings 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

## Step 2: Verify Existing Tables

Make sure your `manual_faqs` table exists with the correct structure:

```sql
-- Verify manual_faqs table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'manual_faqs';

-- Should show: id, question, answer, created_at
```

If the table doesn't exist or needs modification:

```sql
-- Create or update manual_faqs table
CREATE TABLE IF NOT EXISTS manual_faqs (
  id BIGSERIAL PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_manual_faqs_question 
ON manual_faqs USING gin(to_tsvector('english', question));
```

## Step 3: Configure Environment Variables

Ensure these environment variables are set in your `.env` file or Vercel settings:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_service_key

# Admin Authentication
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# Groq API
GROQ_API_KEY=your_groq_api_key

# reCAPTCHA
RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key
```

## Step 4: Access the Admin Dashboard

1. Navigate to: `https://your-domain.com/login`
2. Enter your admin credentials
3. You'll be redirected to `/admin-zt`

## Features

### FAQ Management Tab

- **Add New FAQ**: Create new question-answer pairs
- **View All FAQs**: See all existing FAQs in a list
- **Edit FAQ**: Click "Edit" button to modify existing FAQs
- **Delete FAQ**: Remove FAQs you no longer need
- **Refresh List**: Reload the FAQ list from database

### Bot Settings Tab

#### Response Style
- **Short & Professional**: Concise, to-the-point answers (default)
- **Human-like & Conversational**: Friendly, detailed, empathetic responses

#### Knowledge Source Priority
- **Database First**: Manual FAQs always take priority over AI (default)
  - If a FAQ matches, return it immediately
  - AI is only used when no FAQ matches
- **AI Supplement**: Use AI even with partial FAQ matches
  - Combines database FAQs with AI-generated context
  - Provides more comprehensive answers

#### Context Window Size
- **2000 characters**: Fastest response, less context
- **4000 characters**: Balanced (default)
- **6000 characters**: Slowest response, more comprehensive context

## API Endpoints

### FAQ Management
- `POST /add-faq` - Create new FAQ
- `GET /get-faqs` - List all FAQs
- `PUT /update-faq` - Update existing FAQ
- `DELETE /delete-faq` - Delete FAQ

### Settings Management
- `GET /get-settings` - Get current bot settings
- `POST /save-settings` - Update bot settings

### Authentication
- `GET /login` - Login page
- `POST /login` - Authenticate admin
- `GET /logout` - Logout and clear session
- `GET /admin-zt` - Admin dashboard (requires authentication)

## Database Schema

### manual_faqs
```
id          BIGSERIAL PRIMARY KEY
question    TEXT NOT NULL
answer      TEXT NOT NULL
created_at  TIMESTAMP WITH TIME ZONE
```

### bot_settings
```
id              BIGSERIAL PRIMARY KEY
response_style  TEXT NOT NULL (values: 'short' or 'conversational')
priority        TEXT NOT NULL (values: 'database_first' or 'ai_supplement')
context_size    INTEGER NOT NULL (values: 2000, 4000, or 6000)
updated_at      TIMESTAMP WITH TIME ZONE
```

## Troubleshooting

### "Unauthorized" Error
- Make sure you're logged in
- Check that your session cookie is active
- Try logging out and back in

### Settings Not Saving
- Verify the `bot_settings` table exists in Supabase
- Check Supabase connection credentials
- Look at browser console for error messages

### FAQs Not Loading
- Verify the `manual_faqs` table exists
- Check Supabase permissions (RLS policies)
- Ensure SUPABASE_KEY has appropriate permissions

### Changes Not Reflected in Chatbot
- Settings are loaded on each request
- No need to restart the server
- If issues persist, check the `/ask` endpoint logs

## Security Notes

1. **Admin Authentication**: Uses cookie-based sessions with reCAPTCHA
2. **Authorization**: All admin endpoints check `check_auth()` before execution
3. **SQL Injection**: Protected by Supabase's parameterized queries
4. **XSS Protection**: HTML escaping implemented in frontend
5. **Secure Cookies**: HttpOnly, Secure, SameSite=Lax flags enabled

## Best Practices

1. **Regular Backups**: Export your FAQs periodically from Supabase
2. **Testing**: Test settings changes with sample questions
3. **Documentation**: Keep track of commonly asked questions
4. **Monitoring**: Review chatbot interactions to improve FAQs
5. **Security**: Use strong admin passwords and rotate them regularly

## Support

For issues or questions:
- Check the main README.md for general documentation
- Review Supabase logs for database errors
- Check browser console for frontend errors
- Verify all environment variables are set correctly
