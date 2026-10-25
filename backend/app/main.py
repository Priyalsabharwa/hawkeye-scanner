from fastapi import FastAPI

app = FastAPI(title="Hawkeye", description="Scan files and links. Know why.")


@app.get("/health")
def health():
    return {"status": "Hawkeye is running"}