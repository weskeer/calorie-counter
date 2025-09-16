#!/usr/bin/env python3
"""
MySQL 資料庫設定工具
用於建立資料庫和表格
"""

import mysql.connector
from mysql.connector import Error
import getpass

def create_database():
    """建立資料庫和表格"""
    
    print("=== MySQL 資料庫設定 ===")
    print("請輸入您的 MySQL 連線資訊：")
    
    # 取得連線資訊
    host = input("主機地址 (預設: localhost): ").strip() or "localhost"
    port = input("埠號 (預設: 3306): ").strip() or "3306"
    user = input("使用者名稱 (預設: root): ").strip() or "root"
    password = getpass.getpass("密碼: ")
    database_name = input("資料庫名稱 (預設: calorie_db): ").strip() or "calorie_db"
    
    try:
        # 連接到 MySQL 伺服器
        print(f"\n正在連接到 MySQL 伺服器 {host}:{port}...")
        connection = mysql.connector.connect(
            host=host,
            port=int(port),
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
            
            # 建立索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_meal_record_date ON meal_record(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_food_item_meal_id ON food_item(meal_record_id)")
            print("索引建立成功！")
            
            connection.commit()
            print("\n=== 資料庫設定完成 ===")
            print(f"資料庫名稱: {database_name}")
            print(f"主機: {host}:{port}")
            print(f"使用者: {user}")
            
            # 產生連線字串
            connection_string = f"mysql://{user}:{password}@{host}:{port}/{database_name}"
            print(f"\n請將以下連線字串更新到 server.py 中：")
            print(f"app.config['SQLALCHEMY_DATABASE_URI'] = '{connection_string}'")
            
    except Error as e:
        print(f"錯誤: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n資料庫連線已關閉")

if __name__ == "__main__":
    create_database() 