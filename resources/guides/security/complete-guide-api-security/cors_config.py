from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Strict CORS — only allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stackpractices.com",
        "https://www.stackpractices.com",
        "https://app.stackpractices.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "X-CSRF-Token"
    ],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
    max_age=3600  # Cache preflight for 1 hour
)

# Never use allow_origins=["*"] with allow_credentials=True
# This is a security vulnerability — browsers will reject it
