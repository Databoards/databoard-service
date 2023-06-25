from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from auth import auth_router
from tags import tag_router
from user import user_router
from clock import clock_router

app = FastAPI(timeout=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    field_names = [error["loc"][1] for error in errors]
    error_message = f"Validation error: fields {', '.join(field_names)} are required"
    return JSONResponse(
        status_code=400,
        content={
            "status": "Error",
            "message": "You didn't enter some values correctly",
            "data": error_message,
        },
    )


app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(tag_router.router)
app.include_router(clock_router.router)
