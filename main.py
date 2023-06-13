from fastapi import FastAPI
from user  import user_router
from auth import auth_router

app=FastAPI()


app.include_router(user_router.router)
app.include_router(auth_router.router)