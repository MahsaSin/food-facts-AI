
cd src 
set PYTHONPATH=.
uv run uvicorn app:app --host 0.0.0.0 --port 8001

cd ..
docker build -t my-food-fact-app . -f ./src/Dockerfile
docker run -p 8001:8001 --env-file .env my-food-fact-app


To Do:
add to Github
LangSmith
evaluation of ingredients with LLM  judge (f1-score, recall)
evaluation of nutrition with RMSE and AME