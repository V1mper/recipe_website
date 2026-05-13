import os

from flask import Flask, flash, redirect, render_template, request, url_for

from models import (
    ensure_db,
    get_categories,
    get_recipes_by_category,
    get_recipe_details,
    get_random_recipe,
    submit_recipe,
    get_recipes_grouped_by_meal,
    suggest_daily_ration,
)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-change-me')

ensure_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/categories')
def categories():
    categories_list = get_categories()
    return render_template('categories.html', categories=categories_list)


@app.route('/category/<category_name>')
def category(category_name):
    recipes = get_recipes_by_category(category_name)
    return render_template(
        'category_recipes.html',
        category_name=category_name,
        recipes=recipes,
    )


@app.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    recipe_details = get_recipe_details(recipe_name)
    if recipe_details:
        return render_template('recipe.html', recipe=recipe_details)
    flash('Рецепт не найден', 'error')
    return redirect(url_for('index'))


@app.route('/random')
def random_recipe():
    recipe_details = get_random_recipe()
    if recipe_details:
        return render_template('random.html', recipe=recipe_details)
    flash('Не удалось найти случайный рецепт', 'error')
    return redirect(url_for('index'))


@app.route('/ration', methods=['GET', 'POST'])
def ration():
    grouped = get_recipes_grouped_by_meal()
    suggestion = None
    if request.method == 'POST' and request.form.get('auto'):
        try:
            tk = float(request.form.get('target_kcal', 0))
            tp = float(request.form.get('target_protein', 0))
            tf = float(request.form.get('target_fat', 0))
            tc = float(request.form.get('target_carbs', 0))
        except ValueError:
            flash('Введите числовые значения целей КБЖУ', 'error')
            return render_template('ration.html', grouped=grouped, suggestion=None)
        if tk <= 0 or tp <= 0 or tf <= 0 or tc <= 0:
            flash('Укажите положительные цели по всем показателям КБЖУ', 'error')
            return render_template('ration.html', grouped=grouped, suggestion=None)
        suggestion = suggest_daily_ration(tk, tp, tf, tc)
        if not suggestion:
            flash('Недостаточно рецептов для автоподбора', 'error')
    return render_template('ration.html', grouped=grouped, suggestion=suggestion)


@app.route('/share', methods=['GET', 'POST'])
def share_recipe():
    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Аноним')
        recipe_text = request.form.get('recipe_text')
        if recipe_text:
            submit_recipe(user_name, recipe_text)
            flash('Спасибо! Ваш рецепт отправлен на модерацию.', 'success')
            return redirect(url_for('index'))
        flash('Пожалуйста, заполните поле с рецептом', 'error')
    return render_template('share.html')


if __name__ == '__main__':
    app.run(debug=True)
