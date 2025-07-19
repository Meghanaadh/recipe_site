# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
# A secret key is needed to use flash messages
app.config['SECRET_KEY'] = 'your_super_secret_key_change_me'

# --- Database Initialization ---
def init_db():
    """Initializes the SQLite database and adds sample data if empty."""
    with sqlite3.connect("recipes.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                image_url TEXT
            )
        ''')
        # Check if the table is empty before inserting sample data
        cursor.execute("SELECT COUNT(*) FROM recipes")
        if cursor.fetchone()[0] == 0:
            sample_recipes = [
                ('Spaghetti Carbonara', 'Pasta, Eggs, Pancetta, Parmesan Cheese, Pepper', '1. Cook pasta until al dente. \n2. Fry pancetta until crisp. \n3. In a bowl, whisk eggs, cheese, and pepper. \n4. Drain pasta, reserving some pasta water. \n5. Combine pasta, pancetta, and egg mixture. Add pasta water if needed to create a creamy sauce.', 'https://images.unsplash.com/photo-1588315029754-2dd089d39a1a?q=80&w=2070&auto=format&fit=crop'),
                ('Classic Pancakes', 'Flour, Milk, Eggs, Sugar, Baking Powder, Salt, Butter', '1. In a large bowl, sift together the flour, baking powder, salt and sugar. \n2. Make a well in the center and pour in the milk, egg and melted butter; mix until smooth. \n3. Heat a lightly oiled griddle or frying pan over medium high heat. \n4. Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake. Brown on both sides and serve hot.', 'https://images.unsplash.com/photo-1528207776546-365bb710ee93?q=80&w=2070&auto=format&fit=crop'),
                ('Avocado Toast', 'Bread, Avocado, Salt, Pepper, Red Pepper Flakes, Lemon Juice', '1. Toast your favorite bread to your liking. \n2. While the bread is toasting, mash the avocado in a small bowl and mix in salt, pepper, and a squeeze of lemon juice. \n3. Spread the avocado mixture on the toast. \n4. Sprinkle with red pepper flakes for a little heat.', 'https://images.unsplash.com/photo-1584308666744-8480436122AE?q=80&w=2070&auto=format&fit=crop')
            ]
            cursor.executemany("INSERT INTO recipes (name, ingredients, instructions, image_url) VALUES (?, ?, ?, ?)", sample_recipes)
        conn.commit()

def get_recipe(recipe_id):
    """Gets a single recipe by its ID."""
    with sqlite3.connect("recipes.db") as conn:
        conn.row_factory = sqlite3.Row
        recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    return recipe

# --- Routes ---
@app.route('/')
def index():
    """Renders the homepage with a few featured recipes."""
    with sqlite3.connect("recipes.db") as conn:
        conn.row_factory = sqlite3.Row
        recipes = conn.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 3").fetchall()
    return render_template('index.html', recipes=recipes)

@app.route('/recipes')
def recipes():
    """Displays all recipes."""
    with sqlite3.connect("recipes.db") as conn:
        conn.row_factory = sqlite3.Row
        all_recipes = conn.execute("SELECT * FROM recipes ORDER BY id DESC").fetchall()
    return render_template('recipes.html', recipes=all_recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Displays the details of a single recipe."""
    recipe = get_recipe(recipe_id)
    if recipe is None:
        flash("Recipe not found!", "error")
        return redirect(url_for('recipes'))
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    """Handles adding a new recipe."""
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image_url = request.form.get('image_url')

        with sqlite3.connect("recipes.db") as conn:
            conn.execute(
                "INSERT INTO recipes (name, ingredients, instructions, image_url) VALUES (?, ?, ?, ?)",
                (name, ingredients, instructions, image_url)
            )
            conn.commit()
        flash(f"Recipe '{name}' was successfully added!", "success")
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html')

@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """Handles editing an existing recipe."""
    recipe = get_recipe(recipe_id)
    if recipe is None:
        flash("Recipe not found!", "error")
        return redirect(url_for('recipes'))

    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image_url = request.form.get('image_url')

        with sqlite3.connect("recipes.db") as conn:
            conn.execute(
                "UPDATE recipes SET name = ?, ingredients = ?, instructions = ?, image_url = ? WHERE id = ?",
                (name, ingredients, instructions, image_url, recipe_id)
            )
            conn.commit()
        flash(f"Recipe '{name}' was successfully updated!", "success")
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))

    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    """Handles deleting a recipe."""
    recipe = get_recipe(recipe_id)
    if recipe is None:
        flash("Recipe not found!", "error")
        return redirect(url_for('recipes'))
        
    with sqlite3.connect("recipes.db") as conn:
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
    flash(f"Recipe '{recipe['name']}' was successfully deleted.", "success")
    return redirect(url_for('recipes'))


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
