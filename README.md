# MongoDB with FastAPI & Docker - Kimo Assessment
This repository contains a FastAPI project integrated with MongoDB, packaged as a Docker container. It provides a starting point for building RESTful APIs with FastAPI and MongoDB.

# Prerequisites
1. Python version >= 3.10
2. Docker installed on your local machine


# Usage

1. Pull the Docker Image
To get started, you need to pull the Docker image from the Docker Hub repository. Open a terminal and run the following command:

```bash
docker pull <image_name>
Replace <image_name> with the name of the Docker image for this project. In this case, the image name is kimo-assessment.
```

2. Run the Docker Container
Once the Docker image is pulled, you can run the container locally on your machine. Use the following command:

```bash
docker run -p 80:80 <image_name>
Replace <image_name> with the name of the Docker image for this project, which is kimo-assessment.
```


3. Access the FastAPI Application
After running the Docker container, you can access the FastAPI application on your local machine. Open your web browser and visit http://localhost:80 to interact with the API.

```bash
Customizing the MongoDB Configuration
By default, the FastAPI application is configured to connect to a MongoDB database. If you want to customize the MongoDB configuration, you can modify the app.py file located in the app directory. Look for the MongoDB connection settings and update them according to your MongoDB instance.
```

# Test Application
If you want to test the application simply run the below command in the root directory of the app.

```bash
pytest
```

# Development Workflow
If you want to make changes to the FastAPI application and test them locally, follow these steps:

1. Clone the repository to your local machine.
2. Make the necessary modifications to the code.
3. Build a new Docker image using the updated code:

```bash
docker build -t <image_name> .
```

Run the Docker container using the new image:
```bash
docker run -p 80:80 <image_name>
```
