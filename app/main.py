from fastapi import FastAPI
from routers import user, room


app = FastAPI()

app.include_router(user.router)
app.include_router(room.router)
