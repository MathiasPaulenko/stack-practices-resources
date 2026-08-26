// Express + swagger-ui-express example — design-first OpenAPI serving.
//
// Run: node javascript_express.js
// Then open http://localhost:3000/api-docs

const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const app = express();
const swaggerDocument = YAML.load('./openapi.yaml');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
app.listen(3000);
