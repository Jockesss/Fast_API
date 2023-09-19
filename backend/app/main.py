from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


def create_app():
    from auth.routers import router as auth_router
    from kakao.routers import router as kakao_router
    app = FastAPI()
    origins = ["http://localhost:3000"]
    app.include_router(auth_router, prefix='/auth', tags=['auth'])
    app.include_router(kakao_router, prefix='/kakao', tags=['kakao'])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


ca = create_app()
