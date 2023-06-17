from fastapi import FastAPI
from user  import user_router
from auth import auth_router
from tags import tag_router

app=FastAPI(timeout=60)


app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(tag_router.router)