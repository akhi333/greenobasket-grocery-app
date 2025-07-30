#!/usr/bin/env python3
"""
🔄 Example: Update Products to Use Local Images
================================================

This script shows how to update your products database in backend/app.py
to use local images instead of external URLs.

BEFORE: External URLs (slow, unreliable)
AFTER:  Local paths (fast, reliable)
"""

# Example: How to update products in backend/app.py

# BEFORE (External URLs) ❌
products_db_old = [
    {
        "id": 1,
        "name": "Organic Bananas",
        "category": "fruits",
        "price": 45,
        "image": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300&h=200&fit=crop",
        # ... other fields
    },
    {
        "id": 2,
        "name": "Himalayan Red Apples", 
        "category": "fruits",
        "price": 150,
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=200&fit=crop",
        # ... other fields
    }
]

# AFTER (Local Paths) ✅
products_db_new = [
    {
        "id": 1,
        "name": "Organic Bananas",
        "category": "fruits", 
        "price": 45,
        "image": "/static/images/products/bananas.jpg",  # ← Updated to local path
        "description": "Premium organic bananas - naturally ripened, 1 dozen pack",
        "weight": "1200g",
        "stock": 50,
        "rating": 4.5,
        "visible": True
    },
    {
        "id": 2,
        "name": "Himalayan Red Apples",
        "category": "fruits",
        "price": 150, 
        "image": "/static/images/products/apples.jpg",   # ← Updated to local path
        "description": "Premium Himalayan red apples - crisp, sweet and naturally grown",
        "weight": "1000g",
        "stock": 30,
        "rating": 4.8,
        "visible": True
    },
    {
        "id": 11,
        "name": "Organic Avocados",
        "category": "fruits",
        "price": 180,
        "image": "/static/images/products/avocados.jpg", # ← Updated to local path
        "description": "Premium organic avocados - perfect for salads and toast",
        "weight": "250g",
        "stock": 25,
        "rating": 4.7,
        "visible": True
    },
    {
        "id": 3,
        "name": "Farm Fresh Tomatoes", 
        "category": "vegetables",
        "price": 35,
        "image": "/static/images/products/tomatoes.jpg", # ← Updated to local path
        "description": "Farm fresh tomatoes - perfect for salads and cooking",
        "weight": "500g",
        "stock": 40,
        "rating": 4.6,
        "visible": True
    },
    {
        "id": 5,
        "name": "Organic Baby Spinach",
        "category": "vegetables",
        "price": 45,
        "image": "/static/images/products/spinach.jpg",  # ← Updated to local path
        "description": "Fresh organic baby spinach - perfect for salads",
        "weight": "200g", 
        "stock": 30,
        "rating": 4.7,
        "visible": True
    },
    {
        "id": 9,
        "name": "A2 Organic Milk",
        "category": "dairy",
        "price": 85,
        "image": "/static/images/products/milk.jpg",     # ← Updated to local path
        "description": "Pure A2 organic milk - rich in nutrients",
        "weight": "1000ml",
        "stock": 20,
        "rating": 4.8,
        "visible": True
    }
]

# 📝 INSTRUCTIONS:
# 1. Copy the above products (with local image paths) 
# 2. Replace the corresponding products in backend/app.py
# 3. Download real images and save them to static/images/products/
# 4. Restart your Flask app
# 5. Test that images load correctly

# 🎯 IMAGE NAMING CONVENTION:
image_naming_guide = {
    "Organic Bananas": "bananas.jpg",
    "Himalayan Red Apples": "apples.jpg", 
    "Farm Fresh Tomatoes": "tomatoes.jpg",
    "Organic Baby Spinach": "spinach.jpg",
    "A2 Organic Milk": "milk.jpg",
    "Organic Avocados": "avocados.jpg",
    "Premium Oranges": "oranges.jpg",
    "Fresh Potatoes": "potatoes.jpg",
    "Organic Red Onions": "onions.jpg",
    "Baby Carrots": "carrots.jpg"
}

print("✅ This file shows examples of how to update your products!")
print("📂 Your images should go in: static/images/products/")
print("🔄 Update backend/app.py with the local paths shown above")
print("🚀 Then restart your app to see local images!") 