# 
FROM python:3.10

ENV PYTHONPATH "${PYTHONPATH}:/app/"

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./app /app

COPY ./tests /app/tests


# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]