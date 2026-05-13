import sqlite3
import os
from itertools import product
from math import inf

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes.db')


def ensure_db():
    """Создаёт БД при первом запуске; при устаревшей схеме пересоздаёт файл."""
    if not os.path.exists(DB_PATH):
        init_db()
        return
    conn = get_db_connection()
    rows = conn.execute('PRAGMA table_info(recipes)').fetchall()
    conn.close()
    col_names = [r[1] for r in rows]
    if not col_names or 'kcal' not in col_names:
        os.remove(DB_PATH)
        init_db()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY,
            category_id INTEGER,
            name TEXT NOT NULL,
            instructions TEXT NOT NULL,
            kcal INTEGER NOT NULL,
            protein_g REAL NOT NULL,
            fat_g REAL NOT NULL,
            carbs_g REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            amount TEXT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients (id),
            PRIMARY KEY (recipe_id, ingredient_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE recipe_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            recipe_text TEXT,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    categories = ['Завтрак', 'Обед', 'Ужин', 'Перекус']
    cursor.executemany('INSERT INTO categories (name) VALUES (?)', [(c,) for c in categories])

    ingredients = [
        (1, 'Овсяные хлопья'), (2, 'Молоко 1.5%'), (3, 'Ягоды замороженные'), (4, 'Мёд'),
        (5, 'Яйцо куриное'), (6, 'Брокколи'), (7, 'Оливковое масло'), (8, 'Соль'),
        (9, 'Творог 5%'), (10, 'Сметана 10%'), (11, 'Зелень'),
        (12, 'Куриная грудка'), (13, 'Гречка'), (14, 'Лук репчатый'),
        (15, 'Филе трески'), (16, 'Картофель'), (17, 'Морковь'),
        (18, 'Тунец консервированный в собственном соку'), (19, 'Фасоль красная консервированная'),
        (20, 'Огурец свежий'), (21, 'Помидоры черри'), (22, 'Листья салата'),
        (23, 'Филе индейки'), (24, 'Киноа'), (25, 'Чеснок'),
        (26, 'Творог 2%'), (27, 'Банан'), (28, 'Миндаль'),
        (29, 'Греческий йогурт натуральный'), (30, 'Яблоко'),
    ]
    cursor.executemany('INSERT INTO ingredients (id, name) VALUES (?, ?)', ingredients)

    # (category_id, name, instructions, kcal, protein_g, fat_g, carbs_g)
    recipes = [
        (1, 'Овсянка с ягодами',
         '1. Смешать хлопья с молоком.\n2. Довести до кипения, варить 5–7 минут на среднем огне.\n3. Добавить ягоды и мёд по вкусу.',
         320, 12.0, 8.0, 48.0),
        (1, 'Омлет с брокколи',
         '1. Отварить брокколи 3–4 минуты.\n2. Взбить яйца с солью.\n3. Обжарить брокколи на антипригарной сковороде с каплей масла.\n4. Залить яйцами, накрыть крышкой 5–6 минут.',
         240, 18.0, 14.0, 10.0),
        (1, 'Творожная миска со сметаной',
         '1. Выложить творог в миску.\n2. Добавить сметану и зелень.\n3. Перемешать, подавать сразу.',
         280, 28.0, 12.0, 14.0),
        (2, 'Куриная грудка с гречкой',
         '1. Нарезать грудку, обжарить до готовности.\n2. Отварить гречку.\n3. Пассеровать лук, смешать с курицей и гречкой.',
         480, 48.0, 12.0, 42.0),
        (2, 'Треска на пару с овощами',
         '1. Нарезать овощи.\n2. Выложить рыбу и овощи в пароварку на 12–15 минут.\n3. Сбрызнуть маслом, посолить.',
         360, 38.0, 8.0, 32.0),
        (2, 'Салат с тунцом и фасолью',
         '1. Смешать тунец с фасолью.\n2. Добавить нарезанные огурец и помидоры.\n3. Заправить лимонным соком или йогуртом.',
         410, 36.0, 10.0, 38.0),
        (3, 'Индейка с киноа',
         '1. Отварить киноа.\n2. Обжарить индейку с чесноком до готовности.\n3. Подать с киноа и зеленью.',
         400, 42.0, 10.0, 34.0),
        (3, 'Запечённые овощи с индейкой',
         '1. Нарезать овощи и филе.\n2. Выложить на противень, сбрызнуть маслом.\n3. Запекать при 190 °C 25–30 минут.',
         380, 40.0, 14.0, 28.0),
        (3, 'Рыба с брокколи в духовке',
         '1. Выложить рыбу и брокколи в форму.\n2. Посолить, добавить масло.\n3. Запекать 18–20 минут при 180 °C.',
         310, 34.0, 9.0, 22.0),
        (4, 'Смузи творожно-банановый',
         '1. Пробить в блендере творог, банан и немного молока до гладкости.\n2. Подавать охлаждённым.',
         220, 22.0, 4.0, 24.0),
        (4, 'Яблоко и миндаль',
         '1. Нарезать яблоко дольками.\n2. Подать с горстью миндаля (20–25 г).',
         200, 6.0, 12.0, 20.0),
        (4, 'Греческий йогурт',
         '1. Выложить йогурт в чашку.\n2. По желанию добавить ягоды или ложку мёда.',
         140, 14.0, 7.0, 9.0),
    ]
    cursor.executemany(
        '''INSERT INTO recipes
           (category_id, name, instructions, kcal, protein_g, fat_g, carbs_g)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        recipes,
    )

    recipe_ingredients = [
        (1, 1, '50 г'), (1, 2, '200 мл'), (1, 3, '50 г'), (1, 4, '1 ч.л.'),
        (2, 5, '2 шт'), (2, 6, '100 г'), (2, 7, '1 ч.л.'), (2, 8, 'щепотка'),
        (3, 9, '150 г'), (3, 10, '1 ст.л.'), (3, 11, 'по вкусу'),
        (4, 12, '200 г'), (4, 13, '60 г сухой'), (4, 14, '½ луковицы'),
        (5, 15, '200 г'), (5, 16, '1 шт'), (5, 17, '1 шт'), (5, 8, 'щепотка'),
        (6, 18, '1 банка'), (6, 19, '150 г'), (6, 20, '1 шт'), (6, 21, '100 г'),
        (7, 23, '200 г'), (7, 24, '60 г сухой'), (7, 25, '1 зубчик'), (7, 11, 'по вкусу'),
        (8, 23, '180 г'), (8, 16, '1 шт'), (8, 17, '1 шт'), (8, 7, '1 ст.л.'),
        (9, 15, '200 г'), (9, 6, '200 г'), (9, 7, '1 ст.л.'), (9, 8, 'щепотка'),
        (10, 26, '120 г'), (10, 27, '½ шт'), (10, 2, '80 мл'),
        (11, 30, '1 шт'), (11, 28, '25 г'),
        (12, 29, '150 г'),
    ]
    cursor.executemany(
        'INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount) VALUES (?, ?, ?)',
        recipe_ingredients,
    )

    conn.commit()
    conn.close()


def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return categories


def _row_to_recipe_summary(recipe):
    return {
        'id': recipe['id'],
        'name': recipe['name'],
        'category_id': recipe['category_id'],
        'instructions': recipe['instructions'],
        'kcal': recipe['kcal'],
        'protein_g': recipe['protein_g'],
        'fat_g': recipe['fat_g'],
        'carbs_g': recipe['carbs_g'],
    }


def get_recipes_by_category(category_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    category_result = cursor.fetchone()
    if category_result:
        category_id = category_result[0]
        cursor.execute(
            'SELECT * FROM recipes WHERE category_id = ? ORDER BY name',
            (category_id,),
        )
        recipes_list = [_row_to_recipe_summary(r) for r in cursor.fetchall()]
    else:
        recipes_list = []
    conn.close()
    return recipes_list


def get_recipe_details(recipe_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes WHERE name = ?', (recipe_name,))
    recipe = cursor.fetchone()
    if recipe:
        cursor.execute('SELECT name FROM categories WHERE id = ?', (recipe['category_id'],))
        category = cursor.fetchone()
        cursor.execute(
            '''
            SELECT i.name, ri.amount
            FROM ingredients i
            JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
            ''',
            (recipe['id'],),
        )
        ingredients = cursor.fetchall()
        recipe_details = {
            'id': recipe['id'],
            'name': recipe['name'],
            'category': category['name'] if category else 'Неизвестно',
            'instructions': recipe['instructions'],
            'ingredients': ingredients,
            'kcal': recipe['kcal'],
            'protein_g': recipe['protein_g'],
            'fat_g': recipe['fat_g'],
            'carbs_g': recipe['carbs_g'],
        }
    else:
        recipe_details = None
    conn.close()
    return recipe_details


def get_random_recipe():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1')
    recipe = cursor.fetchone()
    conn.close()
    if recipe:
        return get_recipe_details(recipe['name'])
    return None


def submit_recipe(user_name, recipe_text):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO recipe_submissions (user_name, recipe_text) VALUES (?, ?)',
        (user_name, recipe_text),
    )
    conn.commit()
    conn.close()


def get_recipes_grouped_by_meal():
    """Для конструктора дня: словарь категория → список рецептов с КБЖУ."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT r.*, c.name AS category_name
        FROM recipes r
        JOIN categories c ON c.id = r.category_id
        ORDER BY c.id, r.name
        '''
    )
    rows = cursor.fetchall()
    conn.close()
    grouped = {}
    for row in rows:
        cat = row['category_name']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(_row_to_recipe_summary(row))
    return grouped


def suggest_daily_ration(target_kcal, target_protein, target_fat, target_carbs):
    """
    Подбирает по одному блюду из каждого приёма (Завтрак → Перекус → Обед → Ужин),
    минимизируя относительное отклонение от целевых КБЖУ за день.
    """
    order = ['Завтрак', 'Перекус', 'Обед', 'Ужин']
    grouped = get_recipes_grouped_by_meal()
    lists_by_slot = [grouped.get(name, []) for name in order]
    if any(len(lst) == 0 for lst in lists_by_slot):
        return None

    def rel_err(actual, target):
        if target <= 0:
            return 0.0
        return abs(actual - target) / target

    best_combo = None
    best_score = inf
    for combo in product(*lists_by_slot):
        k = sum(r['kcal'] for r in combo)
        p = sum(r['protein_g'] for r in combo)
        f = sum(r['fat_g'] for r in combo)
        c = sum(r['carbs_g'] for r in combo)
        score = (
            rel_err(k, target_kcal)
            + rel_err(p, target_protein)
            + rel_err(f, target_fat)
            + rel_err(c, target_carbs)
        )
        if score < best_score:
            best_score = score
            best_combo = list(zip(order, combo))
    return best_combo
