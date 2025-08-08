from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import openai, requests, os
from dotenv import load_dotenv

load_dotenv()

AI_API_KEY = os.getenv("OPENROUTER_API_KEY")
TMDB_API_KEY   = os.getenv("TMDB_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="OPENROUTER_API_KEY",
)

app = FastAPI()

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

class UserInput(BaseModel):
    description: str

@app.post("/recommendations")
def recommend(user_input: UserInput):
    prompt = f'Extract up to 3 genres/keywords from: "{user_input.description}"'
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    criteria =  response.choices[0].message.content
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key":TMDB_API_KEY, "query":criteria}
    res = requests.get(url, params=params).json().get("results", [])[:5]
    return [{"title":m["title"], "overview":m["overview"]} for m in res]
