from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import init_mongo
from movies.router import movie_router


app = FastAPI(
    title="Media App",
    description="""<b>This project serves as a scaffolding tool
    for building Python applications that are production-ready.</b><br/>
    <br/>
    It emphasizes modularity, scalability, and a clear
    separation of concerns, providing a solid foundation for
    developing maintainable and well-structured codebases.<br/>
    Whether you are starting a new project or looking to
    standardize your development practices, this scaffold
    helps you adopt best practices from the ground up.""",
    docs_url="/",
)

app.include_router(movie_router, prefix="/movies", tags=["movies"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use only in development.
    # In production, specify allowed origins (e.g., domain names or IPs)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: Figure out the new way of implementing startup events in FastAPI
@app.on_event("startup")
async def startup_event():
    await init_mongo()  # type: ignore


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
