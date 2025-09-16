#!/usr/bin/env python3
"""
自動建立資料庫和表格
使用 .env 檔案中的設定
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def create_database():
    """建立資料庫和表格"""
    
    # 載入環境變數
    load_dotenv()
    
    # 取得連線資訊
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'password')
    database_name = os.getenv('DB_NAME', 'calorie_db')
    
    print("=== 自動建立資料庫 ===")
    print(f"主機: {host}")
    print(f"使用者: {user}")
    print(f"資料庫: {database_name}")
    
    connection = None
    try:
        # 連接到 MySQL 伺服器
        print(f"\n正在連接到 MySQL 伺服器 {host}...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 建立資料庫
            print(f"正在建立資料庫 '{database_name}'...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"資料庫 '{database_name}' 建立成功！")
            
            # 使用資料庫
            cursor.execute(f"USE {database_name}")
            
            # 建立表格
            print("正在建立表格...")
            
            # meal_record 表格
            create_meal_record_table = """
            CREATE TABLE IF NOT EXISTS meal_record (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_calories INT NOT NULL
            )
            """
            cursor.execute(create_meal_record_table)
            print("meal_record 表格建立成功！")
            
            # food_item 表格
            create_food_item_table = """
            CREATE TABLE IF NOT EXISTS food_item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                calories INT NOT NULL,
                meal_record_id INT NOT NULL,
                FOREIGN KEY (meal_record_id) REFERENCES meal_record(id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_food_item_table)
            print("food_item 表格建立成功！")
            
            # 建立索引 (MySQL 不支援 IF NOT EXISTS 語法)
            try:
                cursor.execute("CREATE INDEX idx_meal_record_date ON meal_record(date)")
                print("meal_record 日期索引建立成功！")
            except:
                print("meal_record 日期索引已存在")
                
            try:
                cursor.execute("CREATE INDEX idx_food_item_meal_id ON food_item(meal_record_id)")
                print("food_item 外鍵索引建立成功！")
            except:
                print("food_item 外鍵索引已存在")
            
            connection.commit()
            print("\n=== 資料庫設定完成 ===")
            print(f"資料庫名稱: {database_name}")
            print(f"主機: {host}")
            print(f"使用者: {user}")
            
            return True
            
    except Error as e:
        print(f"錯誤: {e}")
        if "Access denied" in str(e):
            print("\n可能的解決方案:")
            print("1. 檢查 MySQL 密碼是否正確")
            print("2. 確認 MySQL 服務正在運行")
            print("3. 確認使用者有建立資料庫的權限")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n資料庫連線已關閉")

if __name__ == "__main__":
    success = create_database()
    if success:
        print("\n✅ 資料庫建立成功！現在可以執行: python server.py")
    else:
        print("\n❌ 資料庫建立失敗，請檢查錯誤訊息") 