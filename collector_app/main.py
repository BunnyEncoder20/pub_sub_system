from fastapi import FastAPI, status

# routes
from api.device import router as device_router
from api.location import router as location_router

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Utils: Start the logger
from logger import setup_logging
setup_logging()

'''------------------------------------------------------------------'''

# making FastAPI class instance
app = FastAPI()

# lists of alllowed origins that can reach out backend
allowed_orgins = ['*']

# Adding the CORS middleware to our app
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# root route
@app.get("/")
async def root():
    return {"status_code": status.HTTP_200_OK , "msg": "Hello World. This is the Collector FastAPI App"}

# health check endpoint for Docker
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "collector_app"}

# include routers
app.include_router(device_router)
app.include_router(location_router)