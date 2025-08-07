from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai, requests, os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TMDB_API_KEY    = os.getenv("TMDB_API_KEY")

app = FastAPI()

# ─── CORS ───────────────────────────────────────────────────────────────
origins = [
    "https://film-ai-l8uf.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://film-ai-l8uf.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ────────────────────────────────────────────────────────────────────────

class UserInput(BaseModel):
    description: str

@app.post("/recommendations")
def recommend(user_input: UserInput):
    prompt = f"Extract up to 3 genres/keywords from: \"{user_input.description}\""
    gpt = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )
    criteria = gpt.choices[0].message.content.strip()
    url  = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": criteria}
    res = requests.get(url, params=params).json().get("results", [])[:5]
    return [
        {"title": m["title"], "overview": m["overview"]}
        for m in res
    ]
