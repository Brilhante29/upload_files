const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const distPath = path.join(__dirname, 'dist', 'app');
app.use(express.static(distPath));
app.get('/config', (req, res) => {
  const url = fs.readFileSync('/config/api_url', 'utf8').trim();
  res.json({ apiUrl: url });
});
app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});
const port = process.env.PORT || 80;
app.listen(port, '0.0.0.0', () => console.log(`Server running on ${port}`));
