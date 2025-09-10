import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from conf import MODEL_VERSION_INGREDIENTS
from schemas import Dishes


def extract_ingredients(user_input: str, *, return_dict: bool = True):
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    reasoning = {"effort": "low"}

    llm_ingredients = ChatOpenAI(model=MODEL_VERSION_INGREDIENTS, reasoning=reasoning, api_key=openai_api_key)

    structured_llm_ingredients = llm_ingredients.with_structured_output(Dishes)

    prompt_ingredients = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a professional nutritionist dedicated to analyzing meal information.",
            ),
            (
                "human",
                "For each dish in the meal, return:\n"
                "- dish_name\n"
                "- quantity (serving size)\n"
                "- ingredients: list of all ingredients.\n"
                "For every ingredient item, ALWAYS include a quantity, even if approximate "
                "(e.g. '2 oz', '1 tbsp', 'a handful').\n\n"
                "Meal: {user_input}",
            ),
        ]
    )

    chain_ingredients = prompt_ingredients | structured_llm_ingredients
    result_ingredients = chain_ingredients.invoke({"user_input": user_input})

    if return_dict:
        return result_ingredients.model_dump()
    return result_ingredients
