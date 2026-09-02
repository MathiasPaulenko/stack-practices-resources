const request = require('supertest');
const app = require('./javascript_express');

describe('RFC 7807 Problem Details', () => {
  it('returns Problem Details for 404', async () => {
    const res = await request(app).get('/users/-1');
    expect(res.status).toBe(404);
    expect(res.headers['content-type']).toMatch(/application\/problem\+json/);
    expect(res.body.type).toBe('https://api.example.com/errors/not-found');
    expect(res.body.title).toBe('User Not Found');
    expect(res.body.status).toBe(404);
  });

  it('returns 200 for valid user', async () => {
    const res = await request(app).get('/users/1');
    expect(res.status).toBe(200);
    expect(res.body.name).toBe('Ada');
  });

  it('returns 500 for unhandled errors', async () => {
    const res = await request(app).get('/crash');
    expect(res.status).toBe(500);
    expect(res.body.status).toBe(500);
  });

  it('includes instance field', async () => {
    const res = await request(app).get('/users/-1');
    expect(res.body.instance).toBeDefined();
    expect(res.body.instance).toContain('/users/-1');
  });

  it('sets application/problem+json content type', async () => {
    const res = await request(app).get('/users/-1');
    expect(res.headers['content-type']).toMatch(/application\/problem\+json/);
  });
});
