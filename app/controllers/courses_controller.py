from enum import Enum
from typing import Optional, List

from bson import ObjectId

from fastapi import HTTPException, APIRouter, Query

from models.courses import CoursesModel


class CourseSortBy(str, Enum):
    ALPHABETICAL = "alphabetical"
    DATE = "date"
    RATING = "rating"


class Rating(Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"


class CoursesController:

    def __init__(self, db):
        self.router = APIRouter()

        # Add appropriate routes
        self.router.add_api_route("/", self.index, methods=["GET"])
        self.router.add_api_route("/courses", self.get_courses, methods=["GET"], response_model=List[CoursesModel])
        self.router.add_api_route("/course/{course_id}", self.get_course, methods=["GET"], response_model=List[CoursesModel])
        self.router.add_api_route("/chapters/{chapter_name}", self.get_chapter_by_name, methods=["GET"])
        self.router.add_api_route("/rate_chapter", self.rate_chapter, methods=["POST"])

        self.db = db
        self.collection = self.db['courses']
    
    # Index Route        
    async def index(self):
        return {"msg": "Hello World"}

    # GET
    # Prints out an overview of all the courses, manipulated by filters
    # params:
    # sort_by -> str (Alphabetical, Date (Descending), Rating (Descending))
    # domain -> str
    async def get_courses(self, sort_by: CourseSortBy = CourseSortBy.ALPHABETICAL, domain: Optional[str] = Query(None)):
        query = {}

        if domain:
            query["domain"] = domain

        sort_param = None
        if sort_by == CourseSortBy.ALPHABETICAL:
            sort_param = [("name", 1)]
        elif sort_by == CourseSortBy.DATE:
            sort_param = [("date", -1)]
        elif sort_by == CourseSortBy.RATING:
            sort_param = [("ratings", -1)]

        courses = []
        async for course in self.collection.find(query).sort(sort_param):
            courses.append(CoursesModel.parse_obj(course))

        return courses

    # GET
    # Prints out an overview of a course selected by _id
    # params:
    # course_id -> id
    async def get_course(self, course_id: str):
        if ObjectId.is_valid(course_id) and (
                course := await self.collection.find_one({"_id": ObjectId(course_id)})) is not None:
            return [CoursesModel.parse_obj(course)]
        else:
            raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

    # GET
    # Prints out an overview of a course selected by _id
    # params:
    # course_id -> id            
    async def get_chapter_by_name(self, chapter_name: str):
        query = {"chapters.name": chapter_name}
        projection = {"chapters.$": 1}
        if (course := await self.collection.find_one(query, projection=projection)) is not None:
            chapter = course["chapters"][0]
            return chapter

        raise HTTPException(status_code=404, detail=f"Chapter {chapter_name} not found")

    # POST
    # Allows user to rate a chapter that's part of a course. Can either be positive or negative.
    # params:
    # course_id -> id 
    # chapter_name -> str
    # rating -> str   

    async def rate_chapter(self, course_id: str, chapter_name: str, rating: Rating):
        chapter = None

        query = {"chapters.name": chapter_name}
        projection = {"chapters.$": 1}
        if (course := await self.collection.find_one(query, projection=projection)) is not None:
            chapter = course["chapters"][0]

        if chapter is None:
            raise HTTPException(status_code=404, detail=f"Chapter {chapter_name} not found")

        if not ObjectId.is_valid(course_id):
            raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

        # Update chapter's rating

        update_query = {
            "_id": ObjectId(course_id),
            "chapters.name": chapter_name
        }

        if rating == Rating.POSITIVE:
            rating_int = 1
        else:
            rating_int = -1

        update_command = {
            "$inc": {
                "chapters.$.ratings": rating_int
            }
        }

        result = await self.collection.update_one(update_query, update_command, upsert=True)

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Chapter {chapter_name} in Course {course_id} not found")

        course = await self.collection.find_one({"_id": ObjectId(course_id)})

        if not course:
            raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

        # Update course's rating. An aggregate of ratings of all chapters it contains.
        total_ratings = 0
        for chapter in course.get("chapters", []):
            chapter_ratings = chapter.get("ratings", 0)
            total_ratings += chapter_ratings

        update_query = {
            "_id": ObjectId(course_id)
        }

        update_command = {
            "$set": {
                "ratings": total_ratings
            }
        }

        await self.collection.update_one(update_query, update_command, upsert=True)

        return {"message": "Rating submitted successfully"}



