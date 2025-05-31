from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Social Media App",
    description="""<b>This project serves as a scaffolding tool for building Python applications that are production-ready. It emphasizes modularity, scalability, and a clear separation of concerns, providing a solid foundation for developing maintainable and well-structured codebases.</b>
    Whether you are starting a new project or looking to standardize your development practices, this scaffold helps you adopt best practices from the ground up.""",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Use only in development. In production, specify allowed origins (e.g., domain names or IPs)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
