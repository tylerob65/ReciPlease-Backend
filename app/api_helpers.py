import os
import requests

base_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
RAPID_API_HOST = os.environ.get('RAPID_API_HOST')
headers_get = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST,
}
headers_post = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST
}

class API_Calls():
    def get_random_recipe():
        url = base_url + "/recipes/random"
        querystring = {"number":"1"}
        response = requests.get(url, headers=headers_get, params=querystring)
        results = response.json()
        results = results["recipes"][0]
        return results
    
    def get_analyze_user_recipe(
            title,
            ingredients_list,
            instructions,
            servings=1,
            include_nutrition=True):
        
        # Make sure instructions are a single string
        if isinstance(instructions,list):
            temp = [item + "." if item[-1]!="." else item for item in instructions]
            instructions = " ".join(temp)
        
        if not servings:
            servings = 1

        querystring = {"language":"en","includeNutrition":include_nutrition,"includeTaste":"false"}

        payload = {
            "title": title,
            "ingredients": ingredients_list,
            "instructions": instructions,
            "servings":servings,
        }

        url = base_url + "/recipes/analyze"
        
        response = requests.post(url, json=payload, headers=headers_post, params=querystring)
        return response.json()

    def get_nutrition_spoonacular(spoonacular_id):
        url = f"{base_url}/recipes/{spoonacular_id}/nutritionWidget.json"
        response = requests.get(url, headers=headers_get)
        return response.json()

    def process_nutrition(nutrients):
        nutritional_info = {
            "primary":{},
            "secondary":{},
        }
        for nutrient in nutrients:
            name = nutrient["name"]
            info = {
                "amount":nutrient["amount"],
                "unit":nutrient["unit"],
                "percentOfDailyNeeds":nutrient["percentOfDailyNeeds"],
            }
            
            primary_set = set([
                "Cholesterol",
                "Fat",
                "Fiber",
                "Net Carbohydrates",
                "Protein",
                "Sodium",
                "Sugar",
            ])

            if name == "Calories":
                nutritional_info["Calories"] = info
            elif name == "Carbohydrates":
                nutritional_info["primary"]["Carbs"] = info
            elif name in primary_set:
                nutritional_info["primary"][name] = info
            else: 
                nutritional_info["secondary"][name] = info
        return nutritional_info
        
    def get_recipe_info_spoonacular(spoonacular_id):
        url = f"{base_url}/recipes/{spoonacular_id}/information"
        response = requests.get(url, headers=headers_get)
        return response.json()

    def process_recipe_info_spoonacular(recipe):
        ingredients = [ingredient["original"] for ingredient in recipe["extendedIngredients"]]
        instructions = []
        for instruction_group in recipe["analyzedInstructions"]:
            for instruction in instruction_group["steps"]:
                instructions.append(instruction["step"])
        
        recipe_info = {
            "title":recipe["title"],
            "image_url":recipe["image"],
            "source_url":recipe["sourceUrl"],
            "servings":recipe["servings"],
            "cook_time":recipe["readyInMinutes"],
            "ingredients":ingredients,
            "instructions":instructions,
            "spoonacular_id":recipe["id"]
        }
        return recipe_info

        

        
        
        

    
