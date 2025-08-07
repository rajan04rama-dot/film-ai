from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import requests
import os

# load .env (so OPENAI_API_KEY and TMDB_API_KEY are picked up)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TMDB_API_KEY    = os.getenv("TMDB_API_KEY")

app = FastAPI()

# ─── CORS SETUP ────────────────────────────────────────────────────────────────
origins = [
    "https://film-ai-l8uf.vercel.app",
    "https://film-ai-9jng.vercel.app",
    # if you spin up yet another preview, add it here
    # OR for testing you can use: "*"  (but be careful in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # <-- whitelist your front-end domains
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow any headers
)
# ────────────────────────────────────────────────────────────────────────────────

class UserInput(BaseModel):
    description: str

@app.post("/recommendations")
def recommend(user_input: UserInput):
    # 1. ask OpenAI to extract keywords
    prompt = f"Extract up to 3 genres/keywords from: “{user_input.description}”"
    gpt = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )
    criteria = gpt.choices[0].message.content.strip()

    # 2. fetch top 5 matching movies from TMDB
    tmdb_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query":   criteria
    }
    resp = requests.get(tmdb_url, params=params).json().get("results", [])[:5]

    # 3. return only title + overview
    return [
        {"title":   m["title"],
         "overview":m["overview"]}
        for m in resp
    ]
