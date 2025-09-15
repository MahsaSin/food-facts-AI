import pandas as pd
from datasets import load_dataset

from src.nutrition import estimate_nutrition

dataset = load_dataset("dongx1997/NutriBench")
sample = dataset["train"].select(range(50))

records = []
for row in sample:
    meal_text = row["meal_description"]
    try:
        rec = estimate_nutrition(meal_text, return_dict=True)
        records.append(rec)
    except Exception as e:
        print(f"Failed on row: {meal_text[:60]}... | Error: {e}")


df = pd.DataFrame(records)
df.to_csv("../data/nutribench_estimated.csv", index=False)
