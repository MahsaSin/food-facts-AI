import os
from typing import List

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from conf import MODEL_VERSION_NUTRITION
from ingredients import extract_ingredients
from schemas import NutritionList


def estimate_nutrition(user_input: str, *, return_dict: bool = True):
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    dishes_obj = extract_ingredients(user_input, return_dict=False)

    dish_names: List[str] = [
        d.dish_name for d in (dishes_obj.dishes or []) if getattr(d, "dish_name", None)
    ]
    dish_names_str = (
        "\n".join(f"- {n}" for n in dish_names) if dish_names else "- unknown dish"
    )

    reasoning = {"effort": "medium"}

    llm_nutrition = ChatOpenAI(model=MODEL_VERSION_NUTRITION, reasoning=reasoning, api_key=openai_api_key)
    structured_llm_nutrition = llm_nutrition.with_structured_output(NutritionList)

    prompt_nutrition = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a professional nutritionist dedicated to analyzing meal information.",
            ),
            (
                "human",
                "For each of these dishes based on their ingredients, return calories, protein_g, carbs_g, and fat_g per serving:\n{dish_names}",
            ),
        ]
    )

    chain_nutrition = prompt_nutrition | structured_llm_nutrition
    result_nutrition = chain_nutrition.invoke({"dish_names": dish_names_str})

    if return_dict:
        return result_nutrition.model_dump()
    return result_nutrition

# if __name__ == "__main__":
#     user_input = input("Ipmort your meal:")
#     ingredients = extract_ingredients(user_input, return_dict=True)
#     nutrition = estimate_nutrition(user_input=user_input, return_dict=True)

#     print(json.dumps(ingredients, indent=2))
#     print(json.dumps(nutrition, indent=2))
