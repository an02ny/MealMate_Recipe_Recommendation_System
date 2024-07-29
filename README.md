# MealMate - Recipe Recommendation System

MealMate offers users a streamlined approach to discover 700+ recipes using **Inverted Index Tables for Boolean Information Retrieval** that are tailored to their preferances. By entering desired ingredients, users are presented with a curated list of recipe names, along with their corresponding total preparation times. Additionally, users can also **filter** out any allergic ingredients, ensuring that the recommended recipes align with their dietary needs and restrictions.

## Functionalities

MealMate leverages several functionalities to enhance recipe discovery:

1. **Ingredient-Based Recipe Retrieval**: Users can input desired ingredients, and the system retrieves recipes containing those ingredients using an inverted index table for efficient searching.
2. **Relevance Ranking**: TF-IDF (Term Frequency-Inverse Document Frequency) scores are calculated to prioritize and rank relevant recipes.
3. **Performance Optimization**: The length of each document (recipe) and the total number of documents are tracked to optimize search performance.
4. **Allergen Filtering**: Users can specify allergic ingredients, and the system filters out recipes containing those allergens, ensuring dietary compatibility.

## Technology Used

- **Backend**: Python
- **Frontend**: Streamlit for building an interactive web application
- **Search Optimization**: Inverted Index and TF-IDF

## Features

- **Interactive User Interface**: Streamlit provides a user-friendly interface with radio buttons for selecting options, tables to display datasets in CSV format, and a search bar for users to input their recipe queries.
- **Real-time Filtering**: Recipes are filtered in real-time based on user-specified ingredients and allergens.
- **Efficient Search**: Inverted index and TF-IDF ensure fast and relevant recipe retrieval.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/mealmate.git
    cd mealmate
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    streamlit run diet_final.py
    ```

## Usage

1. Open the application in your web browser (usually at `http://localhost:8501`).
2. Enter your desired ingredients in the search bar.
3. Specify any allergic ingredients in the provided field.
4. View the curated list of recipes along with their total preparation times.

The dataset used is from Kaggle:https://www.kaggle.com/datasets/kanishk307/6000-indian-food-recipes-dataset
