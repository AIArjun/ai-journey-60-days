from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return{"message": "welocme to my first API"}
@app.get("/hello")
def hello():
    return{"name": "Arjun"}
@app.get("/health")
def health():
    return{"status": "OK"}


