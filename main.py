import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.handlers import employee_router
from api.login_handler import login_router

# Create instance of the app
app = FastAPI(title="education_platform")

# Create the instance for the routes
main_api_router = APIRouter()
main_api_router.include_router(employee_router)
main_api_router.include_router(login_router)
# Set routes to the app instance
app.include_router(main_api_router)

if __name__ == "__main__":
    # Run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
