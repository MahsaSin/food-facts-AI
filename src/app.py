from fastapi import FastAPI, HTTPException

from ingredients import extract_ingredients
from nutrition import estimate_nutrition
from schemas import EstimateRequest

app = FastAPI()


@app.post("/ingredients")
async def ingredients(req: EstimateRequest):
    try:
        ingredients = extract_ingredients(req.meal, return_dict=True)
        return {"ingredients": ingredients}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/nutrition")
async def nutrition(req: EstimateRequest):
    try:
        nutrition = estimate_nutrition(user_input=req.meal, return_dict=True)
        return {"nutrition": nutrition}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
