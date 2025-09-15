import os
import re
import json
from typing import Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from conf import MODEL_VERSION_NUTRITION
from ingredients import extract_ingredients
from schemas import NutriBenchRecord


def estimate_nutrition(user_input: str, *, return_dict: bool = True):
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    dishes_struct = extract_ingredients(user_input, return_dict=True)
    dishes_struct_json = json.dumps(dishes_struct, ensure_ascii=False)

    reasoning = {"effort": "medium"}
    llm = ChatOpenAI(model=MODEL_VERSION_NUTRITION, reasoning=reasoning, api_key=api_key)
    structured_llm = llm.with_structured_output(NutriBenchRecord)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a professional nutritionist. Given a structured list of dishes and ingredients with quantities, "
         "estimate total macros for the entire meal. Use grams for macronutrients and kilocalories for energy."),
        ("human",
         "Return a single JSON object with this exact schema:\n"
         "{{\n"
         '  "meal_description": string,\n'
         '  "carb": float,        // grams\n'
         '  "fat": float,         // grams\n'
         '  "energy": float,      // kilocalories\n'
         '  "protein": float,     // grams\n'
         '  "country": string|null,\n'
         '  "serving_type": "metric"|"natural"|null\n'
         "}}\n\n"
         "Requirements:\n"
         "- Aggregate across ALL dishes and ingredients.\n"
         "- If any quantity is missing, make a reasonable, conservative assumption based on common serving sizes.\n"
         "- Output numeric values (floats) without units.\n"
         "- Do not include any extra keys or text.\n\n"
         "Inputs:\n"
         "- meal_description: {meal_description}\n"
         "- dishes_struct (JSON): {dishes_struct_json}\n")
    ])

    record = (prompt | structured_llm).invoke({
        "meal_description": user_input,
        "dishes_struct_json": dishes_struct_json,
    })

    if record.serving_type is None:
        record.serving_type = _infer_serving_type(user_input)

    return record.model_dump() if return_dict else record

def _infer_serving_type(text: str) -> Optional[str]:
    metric_patterns = r"\b(g|gram|grams|kg|ml|l|liter|litre|milliliter|millilitre|mg)\b"
    return "metric" if re.search(metric_patterns, text.lower()) else "natural"


# if __name__ == "__main__":
#     user_input = input("Ipmort your meal:")
#     ingredients = extract_ingredients(user_input, return_dict=True)
#     nutrition = estimate_nutrition(user_input=user_input, return_dict=True)

#     print(json.dumps(ingredients, indent=2))
#     print(json.dumps(nutrition, indent=2))
