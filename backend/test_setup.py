from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Paige's Inner Circle Backend",
        "status": "Setup successful!",
        "database_configured": bool(os.getenv("DATABASE_URL"))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)