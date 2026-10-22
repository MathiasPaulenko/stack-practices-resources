// Google Cloud Functions HTTP function from the recipe.
//
// Run locally:
//   npm install
//   npm start          # serves on http://localhost:8080
//   curl "http://localhost:8080/?name=Mathias"
//
// Deploy:
//   gcloud functions deploy helloHttp --runtime nodejs20 --trigger-http --allow-unauthenticated

const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  const name = req.query.name || 'World';
  res.json({ message: `Hello, ${name}!` });
});
