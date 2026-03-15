# 🍽️ Restaurant Recommendation System

A Restaurant Recommendation System built using Python, Machine Learning, and Streamlit that suggests restaurants based on user preferences such as city, cuisine, rating, and cost.

## 🧹 Data Cleaning
* Removed duplicate records
* Handled missing values

## ⚙️ Data Preprocessing
* Applied One-Hot Encoding to city and cuisine
* Ensured all features are numerical

## 🤖 Recommendation System
The system recommends restaurants using:
* K-Means Clustering or
* Cosine Similarity

Recommendations are generated using the encoded dataset and mapped back to cleaned_data.csv to display restaurant details.

## 💻 Streamlit Application
The Streamlit app allows users to:
* Enter preferences (city, cuisine, rating, cost)
* Generate restaurant recommendations

View results with restaurant details

## 🛠️ Technologies Used
* Python
* Pandas
* Scikit-learn
* Streamlit
* Pickle
    
