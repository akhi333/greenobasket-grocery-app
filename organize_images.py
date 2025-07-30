#!/usr/bin/env python3
"""
🗂️ Organize Product Images by Category
======================================

This script moves product images from the main products folder 
into category-specific subfolders for better organization.
"""

import os
import shutil
from pathlib import Path

# Define the base products directory
PRODUCTS_DIR = Path("static/images/products")

# Image categorization mapping
image_categories = {
    # 🍎 FRUITS
    "fruits": [
        "Aamla.jpg", "Chikoo.jpg", "Custardapple.jpg", "DragonFruit.jpg", 
        "Grapes.jpg", "Guava.jpg", "Lemons.jpg", "Mango-2.jpg", "Mango_1.jpg", 
        "Mosambi.jpg", "Orange.jpg", "Pomegrenate.jpg", "Roseapple.jpg", 
        "Watermelon.jpg", "apples.jpg", "blackgrapes.jpg", "muskmelon.jpg", 
        "small_banana.jpg", "raw_banana.jpg"
    ],
    
    # 🥕 VEGETABLES  
    "vegetables": [
        "Brinjal.jpg", "Beans.jpg", "Capsicum.webp", "Carrot.jpeg", 
        "Cauliflower.jpeg", "Corn.jpeg", "Dondakaya.JPG", "Drumstick.jpg", 
        "Garlic.jpg", "Ginger.avif", "Ladysfinger.jpg", "Mirchi.avif", 
        "Mullangi.jpg", "Onion.avif", "Onion_2.avif", "Pepper.avif", 
        "Potato.avif", "Tomato.avif", "ash gourd.avif", "beerakaya.jpg", 
        "beetroot.jpg", "cucumber.jpg", "dosakaya.jpeg", "gummadikaya.jpg", 
        "kakarkaya.jpg", "potlakaya.jpeg", "raw_jackfruit.webp", "sorakaya.webp", 
        "spinegourd-Boda_kakarkaya.jpg", "sweetpotato.png", "taroot.jpeg", 
        "Tapioca.jpg", "Godichikkudu.webp", "BraodBeans.jpg"
    ],
    
    # 🥬 LEAFY VEGETABLES
    "leafy-vegetables": [
        "Keera.avif", "Gongura.webp", "Menthi.jpg", "Pudina.jpg", 
        "Thotakura.jpeg", "spinach.avif", "Agathi Keerai.avif", 
        "Kothimeera or Coriander Leaves.png", "Munaga Aaku.png", 
        "curryleaves.jpg", "manthakaali.jpg", "banana-flowers.jpg", 
        "bananaStem.png"
    ],
    
    # 🌶️ SPICES
    "spices": [
        "Bayleaf - BiryaniAaku.jpg", "BlackPepper - Miriyalu.jpg", 
        "CarawaySeeds - shajeera.jpg", "Cardamom-Elachi.jpg", 
        "Cinamon-DlachamChekka.jpg", "Cloves-Lavangalu.jpg", 
        "CorrianderSeeds - Dhaniyalu.jpg", "Cuminseeds-Jeelakarra.jpg", 
        "Fennelseeds - soamp.jpg", "FenugreekSeeds-Menthulu.jpg", 
        "JaajiKaya.jpg", "Mace - Japathri .jpg", "MustardSeeds - Aavalu.jpg", 
        "Staranise - Anasapuvvu.jpg", "Turmeric_root.webp", "KasthuriMethi.jpg"
    ],
    
    # 🫘 PULSES/LEGUMES
    "pulses": [
        "Chenadal.jpeg", "Kandipappu.png", "black minapappu.jpeg", 
        "gundu_minapa.jpeg", "half_minapappu.jpg", "kidney-beans-1296x728-feature.jpg", 
        "mysorepappu.jpeg", "pesarlu.jpeg", "pesarpappu.jpg", "ulavalu.jpg"
    ],
    
    # 🌾 MILLETS
    "millets": [
        "Amarnathseeds-Thotakura Ginjalu.jpg", "PearMillet-Sajjalu.jpg", 
        "Sorgam-Jonnalu.jpg", "barnyard_millet-oodalu.jpg", 
        "browntopMillet-Andu_Korelu.jpg", "fingermillet.jpg", 
        "fox_tail_korralu.jpg", "kodomillet.jpg", "little_millet_saamalu.jpg", 
        "prosomillet-variga.jpg"
    ],
    
    # 🥛 DAIRY
    "dairy": [
        "milk.jpg"
    ],
    
    # 📁 OTHERS (placeholder files or uncategorized)
    "others": [
        "bananas.jpg", "avocados.jpg", "tomatoes.jpg", "spinach.jpg", 
        "carrots.jpg", "onions.jpg", "oranges.jpg", "potatoes.jpg"
    ]
}

def organize_images():
    """Move images from main products folder to category subfolders"""
    
    print("🗂️  Starting Image Organization...")
    print("=" * 50)
    
    moved_count = 0
    skipped_count = 0
    
    # Process each category
    for category, filenames in image_categories.items():
        category_dir = PRODUCTS_DIR / category
        category_dir.mkdir(exist_ok=True)
        
        print(f"\n📂 Processing category: {category.upper()}")
        
        for filename in filenames:
            source_path = PRODUCTS_DIR / filename
            dest_path = category_dir / filename
            
            if source_path.exists():
                try:
                    shutil.move(str(source_path), str(dest_path))
                    print(f"   ✅ Moved: {filename}")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Error moving {filename}: {e}")
                    skipped_count += 1
            else:
                print(f"   ⚠️  Not found: {filename}")
                skipped_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Organization Complete!")
    print(f"📦 Total moved: {moved_count} files")
    print(f"⚠️  Skipped: {skipped_count} files")
    
    # Show final structure
    print(f"\n📁 Final folder structure:")
    for category in image_categories.keys():
        category_path = PRODUCTS_DIR / category
        if category_path.exists():
            file_count = len(list(category_path.glob("*")))
            print(f"   📂 {category}/  ({file_count} files)")

if __name__ == "__main__":
    organize_images()
    
    print(f"\n🔄 NEW IMAGE PATHS (for backend/app.py):")
    print("=" * 50)
    
    path_examples = {
        "Organic Bananas": "/static/images/products/fruits/small_banana.jpg",
        "Himalayan Red Apples": "/static/images/products/fruits/apples.jpg", 
        "Farm Fresh Tomatoes": "/static/images/products/vegetables/Tomato.avif",
        "Organic Baby Spinach": "/static/images/products/leafy-vegetables/spinach.avif",
        "A2 Organic Milk": "/static/images/products/dairy/milk.jpg",
        "Organic Carrots": "/static/images/products/vegetables/Carrot.jpeg",
        "Red Onions": "/static/images/products/vegetables/Onion.avif",
        "Turmeric Powder": "/static/images/products/spices/Turmeric_root.webp",
        "Chana Dal": "/static/images/products/pulses/Chenadal.jpeg",
        "Finger Millet": "/static/images/products/millets/fingermillet.jpg"
    }
    
    for product, path in path_examples.items():
        print(f"   {product}: \"{path}\"")
        
    print(f"\n📝 Next Steps:")
    print("1. Update backend/app.py with new image paths")
    print("2. Restart your Flask application") 
    print("3. Test that images load correctly")
    print("4. Consider updating product names to match image files")
