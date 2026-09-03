from fastapi import FastAPI
app = FastAPI(title="API Gestão de Inventário")

@app.get("/")
def root():
    return {"status": "ok"}