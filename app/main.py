from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import create_db_and_tables


from app.Movies.movie_controls import router as movie_routes
from app.Movies.showTime_controls import router as showTime_controls
from app.users.register_routes import router as register
from app.users.login_routes import router as login
from app.snacks.snacks_controls import router as snacks_routes
from app.bookings.bookings_controls import router as bookings_routes


app = FastAPI(
    title="Warzone Cinemas API",
    description="API for movie registration, login, and cinema data",
    version="1.0.0"
)

# CORS Configuration for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 specify frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "🎬 Welcome to Warzone Cinemas API"}

app.include_router(movie_routes, prefix="/movies")
app.include_router(showTime_controls, prefix="/showtimes")
app.include_router(register, prefix="/auth")
app.include_router(login, prefix="/auth")
app.include_router(snacks_routes, prefix="/snacks")
app.include_router(bookings_routes, prefix="/bookings")


