#!/usr/bin/env python3
"""
測試環境設定和套件安裝狀況
"""

import sys
import os

def test_imports():
    """測試必要的套件是否已安裝"""
    print("=== 測試套件安裝狀況 ===")
    
    try:
        import flask
        print(f"✅ Flask 版本: {flask.__version__}")
    except ImportError:
        print("❌ Flask 未安裝")
        return False
    
    try:
        import flask_sqlalchemy
        print(f"✅ Flask-SQLAlchemy 版本: {flask_sqlalchemy.__version__}")
    except ImportError:
        print("❌ Flask-SQLAlchemy 未安裝")
        return False
    
    try:
        import mysql.connector
        print("✅ mysql-connector-python 已安裝")
    except ImportError:
        print("❌ mysql-connector-python 未安裝")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 已安裝")
    except ImportError:
        print("❌ python-dotenv 未安裝")
        return False
    
    try:
        from openai import OpenAI
        print("✅ openai 已安裝")
    except ImportError:
        print("❌ openai 未安裝")
        return False
    
    return True

def test_env_file():
    """測試 .env 檔案"""
    print("\n=== 測試 .env 檔案 ===")
    
    if os.path.exists('.env'):
        print("✅ .env 檔案存在")
        
        # 載入環境變數
        from dotenv import load_dotenv
        load_dotenv()
        
        # 檢查必要的環境變數
        required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'OPENAI_API_KEY']
        for var in required_vars:
            value = os.getenv(var)
            if value:
                print(f"✅ {var}: {'*' * len(value)} (已設定)")
            else:
                print(f"❌ {var}: 未設定")
    else:
        print("❌ .env 檔案不存在")
        return False
    
    return True

def test_database_connection():
    """測試資料庫連線"""
    print("\n=== 測試資料庫連線 ===")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import mysql.connector
        from mysql.connector import Error
        
        # 取得連線資訊
        host = os.getenv('DB_HOST', 'localhost')
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', 'password')
        database = os.getenv('DB_NAME', 'calorie_db')
        
        print(f"嘗試連接到: {host}")
        print(f"使用者: {user}")
        print(f"資料庫: {database}")
        
        # 先嘗試連接到 MySQL 伺服器
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✅ 成功連接到 MySQL 伺服器")
            
            cursor = connection.cursor()
            
            # 檢查資料庫是否存在
            cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ 資料庫 '{database}' 存在")
                
                # 嘗試使用資料庫
                cursor.execute(f"USE {database}")
                print(f"✅ 成功切換到資料庫 '{database}'")
                
                # 檢查表格是否存在
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"✅ 資料庫中有 {len(tables)} 個表格")
                
            else:
                print(f"❌ 資料庫 '{database}' 不存在")
                print("請執行 python database_setup.py 來建立資料庫")
            
            cursor.close()
            connection.close()
            print("✅ 資料庫連線已關閉")
            
        return True
        
    except Error as e:
        print(f"❌ 資料庫連線錯誤: {e}")
        return False

def main():
    """主函數"""
    print("開始測試環境設定...\n")
    
    # 測試套件安裝
    if not test_imports():
        print("\n請執行以下命令安裝缺少的套件:")
        print("pip install flask flask-sqlalchemy mysql-connector-python python-dotenv openai")
        return
    
    # 測試 .env 檔案
    if not test_env_file():
        print("\n請建立 .env 檔案並設定必要的環境變數")
        return
    
    # 測試資料庫連線
    if not test_database_connection():
        print("\n請檢查 MySQL 服務是否運行，並確認連線資訊正確")
        return
    
    print("\n=== 所有測試通過！ ===")
    print("您現在可以執行: python server.py")

if __name__ == "__main__":
    main() 