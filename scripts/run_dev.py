import os
import uvicorn

if __name__ == "__main__":
    os.environ.setdefault("APP_ENV", "dev")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
