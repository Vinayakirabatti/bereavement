import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors  # For retrieval-based response matching

# Load the dataset
df = pd.read_csv('D:/Vinayak/fullstack/bereavement/bereavement/python-streamlit/bereavement_train.csv')

# Prepare features (X) and responses (y)
X = df['Query']  # Input: User queries
y = df['Response']  # Output: Predefined bot responses

# Vectorize user queries
vec = TfidfVectorizer(stop_words='english', max_features=1000)
X_vec = vec.fit_transform(X)

# Train a retrieval model (find nearest matching query)
model = NearestNeighbors(n_neighbors=1, metric='cosine')
model.fit(X_vec)

# Define prediction function
def get_bot_response(user_query):
    query_vec = vec.transform([user_query])
    _, index = model.kneighbors(query_vec)
    return y.iloc[index[0][0]]

# Example usage
user_input = "How do I notify the bank about a death?"
response = get_bot_response(user_input)
print(f"User Query: {user_input}")
print(f"Bot Response: {response}")