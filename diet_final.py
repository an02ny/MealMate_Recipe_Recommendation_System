import streamlit as st
import pandas as pd
import math

class BooleanRetrievalSystem:
    def __init__(self):
        self.documents = []  # Initialize documents list
        self.inverted_index = {}
        self.doc_lengths = {}
        self.num_docs = 0
        self.stop_words = {"and", "or", "to", "the", "a", "an"}  # Define stop words

    def add_documents(self, documents):
        self.documents.extend(documents)
        self.num_docs += len(documents)
        self.inverted_index = self.create_inverted_index()
        self.calculate_doc_lengths()

    def create_inverted_index(self):
        inverted_index = {}
        for doc_id, doc in enumerate(self.documents):
            for term in doc.split():
                if term.lower() not in self.stop_words:  # Exclude stop words
                    if term in inverted_index:
                        inverted_index[term].add(doc_id)
                    else:
                        inverted_index[term] = {doc_id}
        return inverted_index

    def calculate_doc_lengths(self):
        for term, doc_ids in self.inverted_index.items():
            for doc_id in doc_ids:
                self.doc_lengths[doc_id] = self.doc_lengths.get(doc_id, 0) + 1


    def tfidf_score(self, term, doc_id):
        tf = self.documents[doc_id].count(term)
        idf = math.log(self.num_docs / len(self.inverted_index[term]))
        return tf * idf

# Load dataset from CSV
df = pd.read_csv("IndianFoodDatasetCSV.csv")

# Instantiate Boolean Retrieval System
brs = BooleanRetrievalSystem()
brs.add_documents(df['RecipeName'].tolist())

# Define the function to filter recipes based on ingredients and allergic ingredients
def filter_recipes(query, allergic_ingredients):
    # Split the query string into a list of ingredients
    query_ingredients = [ingredient.strip() for ingredient in query.split(",")]
    
    # Filter recipes based on query ingredients
    filtered_recipes = df[df['RecipeName'].apply(lambda x: all(ingredient.lower() in x.lower() for ingredient in query_ingredients))]
    
    # Exclude recipes containing allergic ingredients
    if allergic_ingredients:
        allergic_ingredients_list = [ingredient.strip() for ingredient in allergic_ingredients.split(",")]
        for allergic_ingredient in allergic_ingredients_list:
            filtered_recipes = filtered_recipes[~filtered_recipes['RecipeName'].str.lower().str.contains(allergic_ingredient.lower())]
    
    return filtered_recipes

# Define the function to sort recipes based on total time
def sort_recipes(filtered_recipes):
    sorted_recipes = filtered_recipes.sort_values(by='TotalTimeInMins')
    return sorted_recipes

# Streamlit UI
st.title("Recipe Search and Diet Planner")

option = st.radio("Select Option:", ("Search Recipes", "View Inverted Index", "View TF-IDF Scores", "View CSV File"))
if option == "Search Recipes":
    st.subheader("Search Recipes")
    query = st.text_input("Enter ingredients separated by comma (e.g., onion, garlic):")
    allergic_ingredients = st.text_input("Enter allergic ingredients separated by comma (e.g., chili, tomato):")
    if st.button("Search"):
        filtered_recipes = filter_recipes(query, allergic_ingredients)
        if not filtered_recipes.empty:
            sorted_recipes = sort_recipes(filtered_recipes)
            st.write("Found recipes:")
            for index, row in sorted_recipes.iterrows():
                st.write(f"**{row['RecipeName']}**")
                st.write(f"**TotalTime:** {row['TotalTimeInMins']}")
                st.write(f"**Ingredients:** {row['Ingredients']}")
                st.write(f"**Preparation Instructions:** {row['Instructions']}")
                st.write('---')
        else:
            st.write("No recipes found.")
elif option == "View Inverted Index":
    st.subheader("Inverted Index for Recipe Names ")
    for term, doc_ids in brs.inverted_index.items():
        if term.lower() not in brs.stop_words:
            st.write(f"{term}: {doc_ids}")
elif option == "View TF-IDF Scores":
    st.subheader("TF-IDF Scores")
    query = st.text_input("Enter term to calculate TF-IDF scores:")
    if st.button("Calculate TF-IDF"):
        if query in brs.inverted_index:
            st.write("TF-IDF Scores:")
            for doc_id, doc in enumerate(brs.documents):
                tfidf = brs.tfidf_score(query, doc_id)
                st.write(f"Document {doc_id + 1}: {tfidf}")
        else:
            st.write(f"The term '{query}' does not exist in the inverted index.")
elif option == "View CSV File":
    st.subheader("DATABASE")
    st.dataframe(df)
