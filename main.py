from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is working"}

@app.get("/hello")
def hello():
    return {"message": "hello"}
