import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # app 폴더의 main.py 안의 app 객체
        host="0.0.0.0",
        port=8000,
        reload=True
    )