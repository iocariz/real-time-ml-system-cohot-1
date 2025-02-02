FROM python:3.11-slim   

RUN pip install poetry==1.8.2

#strean output to terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

#copy pyproject.toml and poetry.lock to the container

COPY pyproject.toml poetry.lock /app/

#install dependencies from pyproject.toml
RUN poetry install

#copy all source code to the container
COPY . /app

CMD ["poetry", "run", "python", "src/main.py"]
