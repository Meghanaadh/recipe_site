from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    with sqlite3.connect("recipes.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, ingredients TEXT, instructions TEXT
        )''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        with sqlite3.connect("recipes.db") as conn:
            conn.execute("INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)",
                         (name, ingredients, instructions))
        return redirect('/recipes')
    return render_template('add_recipe.html')

@app.route('/recipes')
def recipes():
    with sqlite3.connect("recipes.db") as conn:
        recipes = conn.execute("SELECT * FROM recipes").fetchall()
    return render_template('recipes.html', recipes=recipes)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))  # Render requires binding to this port
    app.run(host='0.0.0.0', port=port)        # Bind to 0.0.0.0 so it works outside localhost
