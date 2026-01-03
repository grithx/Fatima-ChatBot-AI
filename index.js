/**
 * IMPORTANT NOTE:
 * 
 * This Express.js server is an ALTERNATIVE option for local development only.
 * It is NOT used for Vercel deployment.
 * 
 * For Vercel deployment:
 * - The project uses FastAPI (Python) via api/app.py
 * - Configuration is in vercel.json
 * - No Node.js setup is required on Vercel
 * 
 * Use this file ONLY if you want to run a local Express server instead of FastAPI.
 * For most users, run the FastAPI server instead:
 *   cd api
 *   uvicorn app:app --reload --host 0.0.0.0 --port 8000
 */

const express = require('express');
const path = require('path');
const app = express();

// Serve static files from templates directory
app.use(express.static(path.join(__dirname, 'templates')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

// This line is important for both cPanel and local development
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));