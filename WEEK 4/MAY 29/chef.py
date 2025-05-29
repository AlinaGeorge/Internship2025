import asyncio
import json
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

# Load ingredients database
with open("ingredients.json") as f:
    INGREDIENTS_DB = json.load(f)



async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY"),
    )
    def calculate_nutrition(ingredients: dict, servings: int) -> dict:
        """
        Calculate total nutrition per serving from ingredient amounts (in grams).
        Returns a dict with per-serving values for calories, protein, carbs, fat.
        """
        totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for item, grams in ingredients.items():
            if item not in INGREDIENTS_DB:
                raise ValueError(f"Unknown ingredient: {item}")
            data = INGREDIENTS_DB[item]
            factor = grams / 100
            for key in totals:
                totals[key] += data[key] * factor
        for key in totals:
            totals[key] /= servings
        return totals


    # Tool: Generate recipe
    def generate_recipe(task: str) -> dict:
        if "vegan" in task.lower():
            recipe = {
                "name": "Vegan Stir-Fry Bowl",
                "servings": 2,
                "ingredients": {
                    "tofu": 200,
                    "broccoli": 150,
                    "quinoa": 150,
                    "olive oil": 15,
                    "carrot": 100,
                    "spinach": 50
                },
                "steps": [
                    "Cook quinoa according to package.",
                    "Sauté tofu in olive oil until golden.",
                    "Add chopped broccoli, carrots, and spinach; stir-fry for 5 minutes.",
                    "Combine with quinoa and serve hot."
                ]
            }
            return recipe
        return {"error": "No suitable recipe found."}


    # Tool: Check nutrition
    def check_nutrition(recipe_json: str) -> str:
        try:
            recipe = json.loads(recipe_json)
            nutrition = calculate_nutrition(recipe["ingredients"], recipe["servings"])
            msg = (
                f"Per serving - Calories: {nutrition['calories']:.1f}, "
                f"Protein: {nutrition['protein']:.1f}g, "
                f"Carbs: {nutrition['carbs']:.1f}g, Fat: {nutrition['fat']:.1f}g"
            )
            is_balanced = nutrition["protein"] >= 10 and nutrition["calories"] <= 700
            msg += "\nNutrition: " + ("Balanced ✅" if is_balanced else "Unbalanced ❌")
            return msg + "\nTERMINATE"
        except Exception as e:
            return f"Nutrition check failed: {str(e)}\nTERMINATE"

        
    recipe_creator = AssistantAgent(
        name="recipe_creator_agent",
        model_client=model_client,
        description="Creates a recipe using ingredients.json and dietary preferences.",
        system_message="Generate a recipe based on the input task using available ingredients. Use JSON format.",
        tools=[generate_recipe]
    )

    nutrition_checker = AssistantAgent(
        name="nutrition_checker_agent",
        model_client=model_client,
        description="Checks the nutritional balance of the recipe.",
        system_message="Verify the recipe's calories, protein, fat, and carbs. Ensure it's balanced. If valid, respond with 'TERMINATE'.",
        tools=[check_nutrition]
    )

    user= UserProxyAgent(
        name="user_proxy_agent",
        description="A user agent that interacts with the problem solver and verifier agents.",    
    )

    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        [recipe_creator, nutrition_checker, user],
        termination_condition=termination
    )

    task = "Generate a vegan dinner recipe for 2 people."
    await Console(group_chat.run_stream(task=task))
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
