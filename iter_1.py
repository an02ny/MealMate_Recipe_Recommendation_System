import streamlit as st
import pandas as pd

# Load the IndianFoodDatasetCSV.csv into a DataFrame
df = pd.read_csv("IndianFoodDatasetCSV.csv")

# Define the function to filter recipes based on ingredients and allergic ingredients
def filter_recipes(query, allergic_ingredients):
    # Split the query string into a list of ingredients
    query_ingredients = [ingredient.strip() for ingredient in query.split(",")]
    
    # Filter recipes based on query ingredients
    filtered_recipes = df[df['Ingredients'].apply(lambda x: all(ingredient.lower() in x.lower() for ingredient in query_ingredients))]
    
    # Exclude recipes containing allergic ingredients
    if allergic_ingredients:
        allergic_ingredients_list = [ingredient.strip() for ingredient in allergic_ingredients.split(",")]
        for allergic_ingredient in allergic_ingredients_list:
            filtered_recipes = filtered_recipes[~filtered_recipes['Ingredients'].str.lower().str.contains(allergic_ingredient.lower())]
    
    return filtered_recipes

# Define the function to sort recipes based on prep time
def sort_recipes(filtered_recipes):
    sorted_recipes = filtered_recipes.sort_values(by='PrepTimeInMins')
    return sorted_recipes

# Define the search page
def search_page():
    st.title("Recipe Search")
    query = st.text_input("Enter ingredients separated by comma (e.g., onion, garlic):")
    allergic_ingredients = st.text_input("Enter allergic ingredients separated by comma (e.g., chili, tomato):")

    if st.button("Search"):
        filtered_recipes = filter_recipes(query, allergic_ingredients)
        
        if not filtered_recipes.empty:
            sorted_recipes = sort_recipes(filtered_recipes)
            st.write("Found recipes:")
            st.write(sorted_recipes)
        else:
            st.write("No recipes found.")

# Define the main function
def main():
    search_page()

if __name__ == "__main__":
    main()
