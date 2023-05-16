import json

from pymongo import MongoClient


# TO RUN : python initializers/import_course_data.py

class ImportCourseData:

    def __init__(self):
        mongodb_uri = "mongodb://localhost:27017"
        database_name = "kimo-test"

        # Connect to MongoDB
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]

        self.run()

    def run(self):
        # Read course data from JSON file
        with open('courses.json', 'r') as file:
            course_data = json.load(file)

        # Access the courses collection
        collection = self.db['courses']

        # Create indices for efficient retrieval
        collection.create_index('_id')
        collection.create_index('name')
        collection.create_index('date')



        # Insert the course data into the collection
        result = collection.insert_many(course_data)

        print('Course data inserted successfully. Inserted IDs:', result.inserted_ids)

        # Close the MongoDB connection
        self.client.close()


if __name__ == "__main__":
    ImportCourseData()
