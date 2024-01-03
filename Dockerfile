FROM python:3.11-slim AS project-dependencies

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-dev --no-root

FROM project-dependencies AS dev

COPY . .

EXPOSE 8000

RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py migrate

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
