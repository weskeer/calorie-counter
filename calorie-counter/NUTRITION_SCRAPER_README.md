# 健身營養爬蟲功能說明

## 功能概述

這個卡路里計算應用程式新增了健身營養建議爬蟲功能，可以：

1. **爬取健身網站資訊** - 從多個知名健身網站獲取營養建議
2. **個人化營養建議** - 根據用戶資料提供客製化建議
3. **運動營養計劃** - 根據運動類型和時長提供營養計劃
4. **營養資料庫** - 提供科學化的營養資訊
5. **餐點建議** - 根據卡路里需求和目標提供餐點建議

## 檔案結構

```
calorieapp-master/
├── nutrition_scraper.py      # 基礎爬蟲模組
├── advanced_scraper.py       # 進階爬蟲模組
├── server.py                 # 主伺服器（已更新）
├── templates/
│   └── nutrition.html        # 營養建議頁面
└── requirements.txt          # 依賴套件（已更新）
```

## 安裝依賴

```bash
pip install -r requirements.txt
```

新增的依賴套件：
- `requests` - HTTP 請求
- `beautifulsoup4` - HTML 解析
- `lxml` - XML/HTML 解析器

## 功能詳解

### 1. 基礎爬蟲功能 (`nutrition_scraper.py`)

提供基本的營養建議功能：

```python
from nutrition_scraper import NutritionScraper

scraper = NutritionScraper()

# 取得分類建議
tips = scraper.get_fitness_nutrition_tips('weight_loss')

# 搜尋營養資訊
results = scraper.search_nutrition_info('蛋白質')

# 取得餐點建議
suggestions = scraper.get_meal_suggestions(2000, 'weight_loss')
```

### 2. 進階爬蟲功能 (`advanced_scraper.py`)

提供更進階的功能：

```python
from advanced_scraper import AdvancedNutritionScraper

advanced_scraper = AdvancedNutritionScraper()

# 爬取健身網站
results = advanced_scraper.scrape_fitness_websites('protein tips')

# 個人化建議
user_profile = {
    'age': 25,
    'weight': 70,
    'height': 170,
    'gender': 'male',
    'activity_level': 'moderate',
    'goal': 'muscle_gain'
}
advice = advanced_scraper.get_personalized_advice(user_profile)

# 運動營養計劃
plan = advanced_scraper.get_workout_nutrition_plan('strength_training', 60)
```

## API 端點

### 基礎功能

- `GET /nutrition` - 營養建議頁面
- `GET /api/nutrition/tips?category=general` - 取得營養建議
- `GET /api/nutrition/search?query=蛋白質` - 搜尋營養資訊
- `GET /api/nutrition/meal-suggestions?calories=2000&goal=weight_loss` - 餐點建議

### 進階功能

- `POST /api/nutrition/personalized` - 個人化建議
- `GET /api/nutrition/workout-plan?type=strength_training&duration=60` - 運動營養計劃
- `GET /api/nutrition/scrape-websites?query=nutrition tips` - 爬取健身網站
- `GET /api/nutrition/database` - 營養資料庫

## 使用範例

### 1. 取得減重營養建議

```javascript
fetch('/api/nutrition/tips?category=weight_loss')
  .then(response => response.json())
  .then(data => {
    console.log(data.tips);
  });
```

### 2. 取得個人化建議

```javascript
const userProfile = {
  age: 25,
  weight: 70,
  height: 170,
  gender: 'male',
  activity_level: 'moderate',
  goal: 'muscle_gain'
};

fetch('/api/nutrition/personalized', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(userProfile)
})
.then(response => response.json())
.then(data => {
  console.log(data.advice);
});
```

### 3. 取得運動營養計劃

```javascript
fetch('/api/nutrition/workout-plan?type=cardio&duration=45')
  .then(response => response.json())
  .then(data => {
    console.log(data.plan);
  });
```

## 爬蟲網站列表

目前支援的健身網站：

1. **Bodybuilding.com** - 專業健身營養資訊
2. **Men's Health** - 男性健康營養建議
3. **Women's Health** - 女性健康營養建議

## 注意事項

### 1. 爬蟲禮儀

- 已加入隨機延遲避免過度請求
- 使用適當的 User-Agent
- 限制爬取數量避免對網站造成負擔

### 2. 錯誤處理

- 所有爬蟲功能都有錯誤處理機制
- 當爬取失敗時會回傳預設資料
- 記錄錯誤日誌方便除錯

### 3. 資料來源

- 營養資料庫基於科學研究
- 個人化計算使用標準公式
- 餐點建議基於營養學原則

## 擴展功能

### 1. 新增爬蟲網站

在 `advanced_scraper.py` 中的 `fitness_sites` 字典新增網站：

```python
self.fitness_sites = {
    'new_site': {
        'base_url': 'https://example.com',
        'nutrition_section': '/nutrition',
        'search_url': 'https://example.com/search'
    }
}
```

### 2. 自定義營養資料

可以修改 `scrape_nutrition_database()` 方法來新增更多營養資訊。

### 3. 新增運動類型

在 `get_workout_nutrition_plan()` 方法中新增運動類型的營養計劃。

## 測試

```bash
# 啟動伺服器
python server.py

# 訪問營養建議頁面
http://localhost:5000/nutrition
```



## 技術架構

- **後端**: Flask + SQLAlchemy
- **爬蟲**: Requests + BeautifulSoup
- **前端**: HTML + CSS + JavaScript
- **資料庫**: MySQL (用於儲存用戶資料)

