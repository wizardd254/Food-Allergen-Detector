import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('allergy_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergies (
        allergen_list TEXT,
        allergy_name TEXT
    )
''')

# Sample data of 100 allergies with their allergens
allergy_data = [
    ("Peanut", "Rash"), 
    ( "Milk", "Digestion Issues"), #Diarrhoea
    ( "Egg", "Swelling"), 
    ( "Soybean", "Digestion Issues"), 
    ( "Shrimp", "Digestion Issues"), 
    ("Wheat", "Digestion Issues"), 
    ("Almond", "Digestion Issues"),
    ("Salmon", "Rash"), 
    ( "Sesame", "Digestion Issues"),
    ( "Latex", "Rash"),
    ( "Pollen", "Asthma"), #Asthama, Breathelessness
    ( "Dust Mite", "Rash"),
    ( "Bee", "Rash"), 
    ("Penicillin", "Rash"),
    ("Cat", "Asthma"), #Asthama
    ( "Mold", "Rash"), 
    ( "Sunflower Seed", "Digestion Issues"),  
    ("Coconut", "Digestion"),  
    ("Oat", "Digestion Issues"),
    ("Sesame", "Digestion"),
    ("Hazelnut", "Digestion Issues"),
    ("Cucumber", "Digestion Issues"),
    ( "Pineapple", "Digestion Issues"),
    ("Pistachio", "Digestion Issues"),
    ( "Cantaloupe", "Digestion Issues"),
    ( "Barley", "Digestion Issues"),
    ( "Tofu", "Digestion Issues"),
    ( "Quinoa", "Digestion Issues"),
    ( "Garlic", "Digestion Issues"),
    ( "Anise", "Digestion Issues"),
    ("Chia Seed", "Digestion Issues"),
    ( "Artichoke", "Digestion Issues"),
    ( "Saffron", "Digestion Issues"),
    ( "Kombucha", "Digestion Issues"),
    ("Jicama", "Digestion Issues"),
    ( "Arrowroot", "Digestion Issues"),
    ("Cashew", "Rash"),
    ("Kiwi", "Swelling"),
    ("Peach", "Rash"), 
    ("Lactose", "Digestion Issues"), 
    ("Chicken", "Rash"), 
    ("Cocoa", "Rash"), 
    ("Coffee", "Digestion Issues"),
    ("Tea", "Digestion Issues"), 
    ("Hazelnut", "Rash"), 
    ("Pistachio", "Rash"), 
    ("Cashew", "Swelling"), 
    ("Tomato", "Rash"), 
    ("Lettuce", "Digestion Issues"), 
    ("Bell Pepper", "Rash"), 
    ("Carrot", "Digestion Issues"), 
    ("Blueberry", "Rash"), 
    ("Raspberry", "Digestion Issues"), 
    ("Blackberry", "Rash"), 
    ("Strawberry", "Swelling"), 
    ("Cherry", "Rash"), 
    ("Apricot", "Digestion Issues"), 
    ("Grapes", "Digestion Issues"), 
    ("Cranberry", "Rash"), 
    ("Onion", "Sneezing"),
    ("Garlic", "Sneezing"),
    ("Black Pepper", "Sneezing"),
    ("Chili Powder", "Sneezing"),
    ("Cayenne Pepper", "Sneezing"),
    ("Mustard", "Sneezing"),
    ("Horseradish", "Sneezing"),
    ("Wasabi", "Sneezing"),
    ("Vinegar", "Sneezing"),
    ("Citrus", "Itchy Nose"),
    ("Tomato", "Itchy Nose"),
    ("Bell Pepper", "Itchy Nose"),
    ("Spices", "Sneezing"),
    ("Curry Powder", "Sneezing"),
    ("Paprika", "Sneezing"),
    ("Cumin", "Sneezing"),
    ("Fennel", "Sneezing"),
    ("Coriander", "Sneezing"),
    ("Cardamom", "Sneezing"),
    ("Nutmeg", "Sneezing"),
    ("Cinnamon", "Sneezing"),
    ("Cocoa Powder", "Sneezing"),
    ("Vanilla Extract", "Sneezing"),
    ("Nut", "Itchy Nose"),
    ("Celery", "Itchy Nose"),
    ("Caraway Seeds", "Sneezing"),
    ("Dill", "Sneezing"),
    ("Soy Sauce", "Sneezing"),
    ("Wheat Flour", "Sneezing"),
    ("Rye", "Sneezing"),
    ("Barley", "Sneezing"),
    ("Malt", "Sneezing"),
    ("Pineapple", "Itchy Nose"),
    ("Kiwi", "Itchy Nose"),
    ("Papaya", "Itchy Nose"),
    ("Avocado", "Itchy Nose"),
    ("Mango", "Itchy Nose"),
    ("Passion Fruit", "Itchy Nose"),
    ("Cantaloupe", "Itchy Nose"),
    ("Honeydew Melon", "Itchy Nose"),
    ("Asparagus", "Sneezing"),
    ("Mushrooms", "Sneezing"),
    ("Sesame Seeds", "Sneezing"),
    ("Poppy Seeds", "Sneezing"),  
]

# Insert the sample data into the database
#The .executemany method in SQLite is used to execute the same SQL statement multiple times with different sets of parameters. 
cursor.executemany('INSERT INTO allergies (allergen_list, allergy_name) VALUES (?, ?)', allergy_data)

# Commit the changes and close the database connection
conn.commit()
conn.close()