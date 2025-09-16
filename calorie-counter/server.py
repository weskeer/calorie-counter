from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tempfile
import os
from dotenv import load_dotenv

from calorie_counter import get_calories_from_image
from nutrition_scraper import NutritionScraper
from advanced_scraper import AdvancedNutritionScraper

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 資料庫配置 - 從環境變數讀取
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'password')
db_name = os.getenv('DB_NAME', 'calorie_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料庫模型
class MealRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_calories = db.Column(db.Integer, nullable=False)
    foods = db.relationship('FoodItem', backref='meal_record', lazy=True, cascade='all, delete-orphan')

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    meal_record_id = db.Column(db.Integer, db.ForeignKey('meal_record.id'), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]

    if image.filename == "":
        return {
            "error": "No image uploaded",
        }, 400

    # 將臨時檔案存到專案根目錄
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.getcwd())
    image.save(temp_file.name)

    calories = get_calories_from_image(temp_file.name)
    temp_file.close()

    return {
        "calories": calories,
    }

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/save_meal", methods=["POST"])
def save_meal():
    try:
        data = request.get_json()
        foods = data.get('foods', [])
        total_calories = data.get('total_calories', 0)
        
        # 建立新的餐點記錄
        meal_record = MealRecord(total_calories=total_calories)
        db.session.add(meal_record)
        db.session.flush()  # 取得ID
        
        # 新增食物項目
        for food in foods:
            food_item = FoodItem(
                name=food['name'],
                calories=food['calories'],
                meal_record_id=meal_record.id
            )
            db.session.add(food_item)
        
        db.session.commit()
        return jsonify({"success": True, "message": "餐點記錄已儲存"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"儲存失敗: {str(e)}"}), 500

@app.route("/meals")
def meals():
    # 取得所有餐點記錄，按日期排序
    meal_records = MealRecord.query.order_by(MealRecord.date.desc()).all()
    return render_template("meals.html", meal_records=meal_records)

@app.route("/api/meals")
def api_meals():
    # API端點，回傳JSON格式的餐點記錄
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    meal_records = MealRecord.query.order_by(MealRecord.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    meals_data = []
    for meal in meal_records.items:
        meals_data.append({
            'id': meal.id,
            'date': meal.date.strftime('%Y-%m-%d %H:%M'),
            'total_calories': meal.total_calories,
            'foods': [{'name': food.name, 'calories': food.calories} for food in meal.foods]
        })
    
    return jsonify({
        'meals': meals_data,
        'total': meal_records.total,
        'pages': meal_records.pages,
        'current_page': page,
        'has_next': meal_records.has_next,
        'has_prev': meal_records.has_prev
    })

@app.route("/delete_meal/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    try:
        meal_record = MealRecord.query.get_or_404(meal_id)
        db.session.delete(meal_record)
        db.session.commit()
        return jsonify({"success": True, "message": "餐點記錄已刪除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"刪除失敗: {str(e)}"}), 500

# 建立資料庫表格
def create_tables():
    with app.app_context():
        db.create_all()

# 初始化爬蟲
scraper = NutritionScraper()
advanced_scraper = AdvancedNutritionScraper()

@app.route("/nutrition")
def nutrition():
    """營養建議頁面"""
    return render_template("nutrition.html")

@app.route("/personalized-meals")
def personalized_meals():
    """個人化餐點建議頁面"""
    return render_template("personalized_meals.html")

@app.route("/api/nutrition/tips")
def api_nutrition_tips():
    """API端點：取得營養建議"""
    category = request.args.get('category', 'general')
    tips = scraper.get_fitness_nutrition_tips(category)
    return jsonify({"tips": tips})

@app.route("/api/nutrition/search")
def api_nutrition_search():
    """API端點：搜尋營養資訊"""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "請提供搜尋關鍵字"}), 400
    
    # 建立同義詞映射（可視需要擴充）
    synonyms_map = {
        'iron': {"iron", "鐵", "鐵質", "fe", "ferrous", "ferric"},
        'zinc': {"zinc", "鋅"},
        'magnesium': {"magnesium", "鎂"},
        'calcium': {"calcium", "鈣", "ca"},
        'potassium': {"potassium", "鉀", "k"},
        'vitamin_c': {"vitamin c", "維生素c", "抗壞血酸", "ascorbic acid"},
        'folate': {"folate", "葉酸", "維生素b9", "vitamin b9"},
    }
    q_lower = query.lower().strip()
    # 若輸入屬於某一群同義詞，擴充查找關鍵字集合
    expanded_keywords = {q_lower}
    for key, variants in synonyms_map.items():
        if q_lower in variants or q_lower == key:
            expanded_keywords = expanded_keywords.union(variants).union({key})
            break
    
    # 先嘗試使用進階爬蟲抓取真實內容
    try:
        scraped = advanced_scraper.scrape_fitness_websites(query)
    except Exception as e:
        scraped = []
    
    # 若進階爬蟲無結果，嘗試使用內建資料庫作為後備
    db_results = []
    if not scraped:
        try:
            db_entries = advanced_scraper.scrape_nutrition_database()
            for entry in db_entries:
                title = (entry.get('title') or '').lower()
                content = (entry.get('content') or '').lower()
                category = (entry.get('category') or '').lower()
                # 若任一擴充關鍵字命中，即加入結果
                if any(k in title or k in content or k in category for k in expanded_keywords):
                    db_results.append(entry)
        except Exception:
            db_results = []
    
    # 仍無資料時，退回到基本模擬資料
    basic = []
    if not scraped and not db_results:
        basic = scraper.search_nutrition_info(query) or []
    
    # 合併結果（避免重複，保留有內容的）
    seen_titles = set()
    merged = []
    for item in (scraped + db_results + basic):
        title = item.get('title')
        if title and title not in seen_titles:
            seen_titles.add(title)
            merged.append(item)
    
    return jsonify({"results": merged})

@app.route("/api/nutrition/meal-suggestions")
def api_meal_suggestions():
    """API端點：取得餐點建議"""
    calories = request.args.get('calories', type=int, default=2000)
    goal = request.args.get('goal', 'maintenance')
    
    # 使用進階爬蟲的多樣化餐點建議（含隨機性與營養素）
    try:
        suggestions = advanced_scraper.get_diverse_meal_suggestions(calories, goal)
    except Exception:
        # 後備：使用基本建議
        basic = scraper.get_meal_suggestions(calories, goal)
        # 轉換為新欄位命名以便前端一致渲染
        mapped = []
        for item in basic:
            mapped.append({
                'meal': item.get('meal'),
                'name': item.get('suggestion'),
                'calories': int(item.get('calories', 0)),
                'protein_g': int(str(item.get('protein', '0')).replace('g','') or 0),
                'carbs_g': int(str(item.get('carbs', '0')).replace('g','') or 0),
                'fat_g': int(str(item.get('fat', '0')).replace('g','') or 0),
            })
        suggestions = mapped
    return jsonify({"suggestions": suggestions})

@app.route("/api/nutrition/personalized")
def api_personalized_advice():
    """API端點：取得個人化建議"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "請提供用戶資料"}), 400
        
        advice = advanced_scraper.get_personalized_advice(data)
        return jsonify({"advice": advice})
    except Exception as e:
        return jsonify({"error": f"取得建議失敗: {str(e)}"}), 500

@app.route("/api/nutrition/workout-plan")
def api_workout_nutrition_plan():
    """API端點：取得運動營養計劃"""
    workout_type = request.args.get('type', 'strength_training')
    duration = request.args.get('duration', type=int, default=60)
    
    plan = advanced_scraper.get_workout_nutrition_plan(workout_type, duration)
    return jsonify({"plan": plan})

@app.route("/api/nutrition/scrape-websites")
def api_scrape_websites():
    """API端點：爬取健身網站"""
    query = request.args.get('query', 'nutrition tips')
    
    try:
        results = advanced_scraper.scrape_fitness_websites(query)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": f"爬取失敗: {str(e)}"}), 500

@app.route("/api/nutrition/database")
def api_nutrition_database():
    """API端點：取得營養資料庫資訊"""
    try:
        data = advanced_scraper.scrape_nutrition_database()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": f"取得資料失敗: {str(e)}"}), 500

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
