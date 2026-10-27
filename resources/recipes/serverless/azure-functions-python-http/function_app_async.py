import azure.functions as func
import json
import aiohttp

app = func.FunctionApp()

@app.route(route="weather/{city}")
async def get_weather(req: func.HttpRequest) -> func.HttpResponse:
    city = req.route_params.get('city')
    api_key = req.params.get('api_key', 'default')

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.weather.example.com/{city}",
            headers={"X-API-Key": api_key},
        ) as response:
            data = await response.json()

    return func.HttpResponse(
        body=json.dumps(data),
        status_code=200,
        mimetype="application/json",
    )
