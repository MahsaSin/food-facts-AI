FROM python:3.12-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY src ./



ENV PYTHONPATH=.

EXPOSE 8000

CMD [ ".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001" ]
