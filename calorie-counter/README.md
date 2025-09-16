# AI Calorie Counter App

This GPT-4o powered Flask web app tells you how many calories there are in an image of a meal you upload

## Quick Start

0. Rename the `.env.sample` file into `.env` and add your OpenAI API key

1. Start the server:

```sh
$ python3 server.py
```

2. Go to http://localhost:5000


## Terminal usage

You can also use it from the terminal:

```sh
$ python3 calorie_counter.py IMAGE_FILE
```
# 卡路里記錄系統 - MySQL 資料庫版本

## 安裝步驟

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定 MySQL 資料庫


#### ：手動設定

1. 登入 MySQL：
```bash
mysql -u root -p
```

2. 建立資料庫：
```sql
CREATE DATABASE calorie_db;
USE calorie_db;
```

3. 建立表格：
```sql
CREATE TABLE meal_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_calories INT NOT NULL
);

CREATE TABLE food_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    calories INT NOT NULL,
    meal_record_id INT NOT NULL,
    FOREIGN KEY (meal_record_id) REFERENCES meal_record(id) ON DELETE CASCADE
);

CREATE INDEX idx_meal_record_date ON meal_record(date);
CREATE INDEX idx_food_item_meal_id ON food_item(meal_record_id);
```

### 3. 更新資料庫連線設定

在 `server.py` 中更新資料庫連線字串：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://使用者名稱:密碼@主機:埠號/資料庫名稱'
```

例如：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:your_password@localhost:3306/calorie_db'
```

### 4. 執行應用程式

```bash
python server.py
```

## 使用說明

### 主頁面 (`/`)
- 上傳食物圖片進行卡路里識別
- 點擊「紀錄這餐」進入記錄頁面
- 點擊「查看所有記錄」查看歷史記錄

### 記錄頁面 (`/record`)
- 輸入食物名稱和卡路里
- 點擊「新增一行」增加更多食物項目
- 點擊「刪除」移除不需要的行
- 點擊「儲存餐點記錄」將資料儲存到資料庫

### 記錄查看頁面 (`/meals`)
- 顯示所有儲存的餐點記錄
- 按日期排序（最新的在前）
- 支援分頁載入，點擊「載入更多」查看更多記錄
- 點擊「刪除」按鈕可以刪除記錄

## 資料庫結構

### meal_record 表格
- `id`: 主鍵，自動遞增
- `date`: 記錄時間，自動設定為當前時間
- `total_calories`: 該餐總卡路里

### food_item 表格
- `id`: 主鍵，自動遞增
- `name`: 食物名稱
- `calories`: 該食物卡路里
- `meal_record_id`: 外鍵，關聯到 meal_record 表格

## API 端點

- `POST /save_meal`: 儲存餐點記錄
- `GET /api/meals`: 取得餐點記錄（支援分頁）
- `DELETE /delete_meal/<id>`: 刪除指定餐點記錄

## 注意事項

1. 確保 MySQL 服務正在運行
2. 確保資料庫連線資訊正確
3. 首次執行時會自動建立表格
4. 刪除餐點記錄會同時刪除相關的食物項目（CASCADE）

## 故障排除

### 連線錯誤
- 檢查 MySQL 服務是否運行
- 確認使用者名稱和密碼正確
- 確認主機地址和埠號正確

### 表格不存在
- 執行 `python database_setup.py` 重新建立表格
- 或手動執行 SQL 建立表格

### 權限錯誤
- 確保 MySQL 使用者有建立資料庫和表格的權限
- 使用 root 使用者或具有適當權限的使用者 