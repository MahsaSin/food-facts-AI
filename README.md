# 🍽️ NutriBench Assistant

A project for extracting **ingredients** from meal descriptions and estimating **nutritional values** (macros + energy).  
Built with **Python 3.12** and **FastAPI**, structured for readability, maintainability, evaluation, and fully Dockerized.  

Leverages **LangChain + OpenAI** for structured reasoning about food, ingredients, and nutrition.  
Provides both **ingredient breakdowns** and **macro estimations**, and can be evaluated against the **NutriBench dataset**.  

We used **LangSmith** for monitoring, debugging, and evaluating LLM runs to ensure accuracy and reliability.

---

## Project Structure

src/              → Core logic (ingredients, nutrition, schemas, app)  
data/             → Generated CSVs or evaluation outputs  
evaluation/       → Evaluating nutrition output  
.gitignore        → Ignore data & artifacts  
.python-version   → Python 3.12  
pyproject.toml    → Metadata & dependencies  
uv.lock           → Locked deps for reproducibility  
Dockerfile        → Containerized API runtime  
README.md         → You’re here  

---

## Overview

This project helps analyze meals by:  

- Extracting **dishes, serving sizes, and ingredients**  
- Estimating **total carbs, fat, protein, and calories**  
- Returning outputs in validated **Pydantic schemas**  
- Providing a **FastAPI** service for easy integration  
- Enabling **evaluation** against the [NutriBench dataset](https://huggingface.co/datasets/dongx1997/NutriBench)  

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/MahsaSin/food-facts-AI.git
cd food-facts-AI
```

### Running with Docker

The project includes a Dockerfile based on Python 3.12 slim, pre-configured with dependencies like ffmpeg and uv.

**Build the Docker image:**
```bash
cd ..
docker build -t my-food-fact-app . -f ./src/Dockerfile
```

**Run the container:**
```bash
docker run -p 8001:8001 --env-file .env my-food-fact-app
```

**Once running, the API will be accessible at:**
```bash
http://localhost:8001
```

### Running the app

**Run the app with fastAPI:**
```bash
cd src 
set PYTHONPATH=.
uv run uvicorn app:app --host 0.0.0.0 --port 8001
```

## Evaluation

Evaluate predictions against NutriBench:
```bash
cd evaluation
uv run python .\nutrieval.py
```

The evaluation in your project (via NutritionEvaluator.evaluate) returns two things:

1. Per-metric DataFrame → error statistics for each nutrient
- metric: which nutrient (carb, fat, energy, protein)
- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- N: number of rows evaluated

2. Overall dictionary → aggregated metrics
- AME_macro: average MAE across all metrics
- RMSE_macro: average RMSE across all metrics
- rows_evaluated: number of joined rows (overlap between reference and predictions)
- MAE_micro: pooled MAE across all nutrient values
- RMSE_micro: pooled RMSE across all nutrient values