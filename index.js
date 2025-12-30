// const express = require('express');
// const path = require('path');
// const app = express();

// app.use(express.static('templates')); // Aapki index.html yahan se load hogi

// // Vercel ke liye serverless function setup
// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'templates', 'index.html'));
// });

// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => console.log(`Server running on port ${PORT}`));



const express = require('express');
const path = require('path');
const app = express();

// Behtar tariqa: Absolute path use karein
app.use(express.static(path.join(__dirname, 'templates')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

// Ye line cPanel aur Vercel dono ke liye zaroori hai
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));