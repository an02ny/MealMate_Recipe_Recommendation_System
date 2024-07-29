import streamlit as st
import pandas as pd
import math

class BooleanRetrievalSystem:
    def __init__(self):  # <-- Corrected initialization method name
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

    def retrieve_documents(self, query):
        query_terms = query.split()
        if len(query_terms) == 1:
            return self.inverted_index.get(query_terms[0], set())
        else:
            result_set = self.inverted_index.get(query_terms[0], set())
            for term in query_terms[1:]:
                result_set = result_set.intersection(self.inverted_index.get(term, set()))
            return result_set

    def tfidf_score(self, term, doc_id):
        tf = self.documents[doc_id].count(term)
        idf = math.log(self.num_docs / len(self.inverted_index[term]))
        return tf * idf

# Load dataset from CSV
df = pd.read_csv('IndianFoodDatasetCSV.csv')

# Instantiate Boolean Retrieval System
brs = BooleanRetrievalSystem()
brs.add_documents(df['RecipeName'].tolist())

# Streamlit UI
st.title("Diet Planner")

option = st.radio("Select Option:", ("View Inverted Index", "Enter Query", "View CSV File"))
if option == "View Inverted Index":
    st.subheader("Inverted Index for Recipe Names ")
    for term, doc_ids in brs.inverted_index.items():
        if term.lower() not in brs.stop_words:
            st.write(f"{term}: {doc_ids}")
elif option == "View CSV File":
    st.subheader("DATABASE")
    st.dataframe(df)
else:
    query = st.text_input("Enter Query:")
    allergic_ingredients = st.text_input("Enter Allergic Ingredients (comma-separated):")
    if query:
        result_set = brs.retrieve_documents(query)
        if len(result_set) > 0:
            st.subheader("Documents containing the Query")
            ranked_results = sorted(result_set, key=lambda x: df['TotalTimeInMins'][x])
            for doc_id in ranked_results:
                st.markdown(f"*Recipe Name:* {df['RecipeName'][doc_id]}")
                st.write("Time to Prepare:", df['TotalTimeInMins'][doc_id], "minutes")
                st.write("Servings:", df['Servings'][doc_id])
                st.write("Cuisine:", df['Cuisine'][doc_id])
                st.write("Course:", df['Course'][doc_id])
                st.write("Diet:", df['Diet'][doc_id])
                tfidf_score = brs.tfidf_score(query, doc_id)
                st.write("TF-IDF Score:", tfidf_score)
                st.write("Instructions:", df['Instructions'][doc_id])
        else:
            st.write("No documents found containing the query.")