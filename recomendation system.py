import math

# Step 1: Data Representation
# Sample data (user-item ratings matrix) for movies, books, and products
# Users: A, B, C, D
# Items: Movies (M1, M2), Books (B1, B2), Products (P1, P2)
ratings = {
    'A': {'M1': 5, 'M2': 3, 'B1': 0, 'B2': 1, 'P1': 4, 'P2': 0},
    'B': {'M1': 4, 'M2': 0, 'B1': 2, 'B2': 0, 'P1': 5, 'P2': 1},
    'C': {'M1': 1, 'M2': 1, 'B1': 5, 'B2': 3, 'P1': 2, 'P2': 4},
    'D': {'M1': 2, 'M2': 5, 'B1': 0, 'B2': 4, 'P1': 3, 'P2': 4}
}

# Item Categories: Movie, Book, Product
item_categories = {
    'M1': 'Movie', 'M2': 'Movie',
    'B1': 'Book', 'B2': 'Book',
    'P1': 'Product', 'P2': 'Product'
}

# Step 2: Calculate Cosine Similarity between users
def cosine_similarity(user1, user2, ratings):
    common_items = set(ratings[user1].keys()).intersection(ratings[user2].keys())
    
    if len(common_items) == 0:
        return 0
    
    dot_product = sum([ratings[user1][item] * ratings[user2][item] for item in common_items])
    magnitude_user1 = math.sqrt(sum([ratings[user1][item] ** 2 for item in common_items]))
    magnitude_user2 = math.sqrt(sum([ratings[user2][item] ** 2 for item in common_items]))
    
    if magnitude_user1 == 0 or magnitude_user2 == 0:
        return 0
    
    return dot_product / (magnitude_user1 * magnitude_user2)

# Step 3: Make Predictions
def predict_rating(user, item, ratings, similarity_func):
    total_similarity = 0
    weighted_sum = 0
    
    for other_user in ratings:
        if other_user != user and item in ratings[other_user]:
            sim = similarity_func(user, other_user, ratings)
            total_similarity += sim
            weighted_sum += sim * ratings[other_user][item]
    
    if total_similarity == 0:
        return 0
    
    return weighted_sum / total_similarity

# Step 4: Recommend Items to a User Based on Categories
def recommend(user, ratings, item_categories, n=3):
    recommendations = {'Movie': [], 'Book': [], 'Product': []}
    
    # Iterate over all items
    for item in ratings[user].keys():
        if ratings[user][item] == 0:  # User hasn't rated this item yet
            predicted_rating = predict_rating(user, item, ratings, cosine_similarity)
            category = item_categories.get(item, 'Unknown')
            
            # Append the predicted rating with category
            recommendations[category].append((item, predicted_rating))
    
    # Sort the recommendations within each category by predicted rating (descending)
    for category in recommendations:
        recommendations[category].sort(key=lambda x: x[1], reverse=True)
    
    # Return the top N items from each category (Movie, Book, Product)
    top_recommendations = {
        'Movie': recommendations['Movie'][:n],
        'Book': recommendations['Book'][:n],
        'Product': recommendations['Product'][:n]
    }
    
    return top_recommendations

# Step 5: Example - Recommend items for User A
recommended_items = recommend('A', ratings, item_categories, n=3)

print("Top 3 recommendations for User A:")

for category, items in recommended_items.items():
    print(f"\nCategory: {category}")
    for item, score in items:
        print(f"  {item} (Predicted Rating: {score:.2f})")
