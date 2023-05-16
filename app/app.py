from fastapi import FastAPI
import motor.motor_asyncio

from controllers.courses_controller import CoursesController

# Connect to the MongoDB instance
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://192.168.0.122:27017")

# Select the MongoDB database
db = client['kimo-test']

# Initialize FastAPI
app = FastAPI()

# Attach CoursesController as a router
app.include_router(router=CoursesController(db).router)
