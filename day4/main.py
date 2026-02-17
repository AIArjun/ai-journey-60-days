from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to my first API"}

@app.get("/hello")
def hello():
    return {"name": "Arjun"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="User ID must be a positive integer"
        )

    if user_id > 100:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user_id,
        "message": "User fetched successfully"
    }

@app.get("/items")
def get_items(limit: int = 10):
    if limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than zero"
        )

    return {
        "limit_used": limit,
        "items": list(range(1, limit + 1))
    }
