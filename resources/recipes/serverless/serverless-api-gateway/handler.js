exports.handler = async (event) => {
  const { httpMethod, path, body } = event;

  if (httpMethod === 'GET' && path === '/users') {
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ users: ['alice', 'bob'] })
    };
  }

  if (httpMethod === 'POST' && path === '/users') {
    try {
      const data = JSON.parse(body);
      return {
        statusCode: 201,
        body: JSON.stringify({ id: '123', name: data.name })
      };
    } catch {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid JSON body' }) };
    }
  }

  return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };
};
