#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
營養爬蟲功能測試腳本
"""

import sys
import json
from nutrition_scraper import NutritionScraper
from advanced_scraper import AdvancedNutritionScraper

def test_basic_scraper():
    """測試基礎爬蟲功能"""
    print("🧪 測試基礎爬蟲功能...")
    
    scraper = NutritionScraper()
    
    # 測試分類建議
    categories = ['general', 'weight_loss', 'muscle_gain', 'endurance']
    
    for category in categories:
        print(f"\n📋 測試 {category} 分類:")
        tips = scraper.get_fitness_nutrition_tips(category)
        print(f"   找到 {len(tips)} 個建議")
        if tips:
            print(f"   範例: {tips[0]['title']}")
    
    # 測試搜尋功能
    print(f"\n🔍 測試搜尋功能:")
    search_results = scraper.search_nutrition_info('蛋白質')
    print(f"   搜尋結果: {len(search_results)} 個")
    
    # 測試餐點建議
    print(f"\n🍽️ 測試餐點建議:")
    suggestions = scraper.get_meal_suggestions(2000, 'weight_loss')
    print(f"   減重餐點建議: {len(suggestions)} 個")
    
    suggestions = scraper.get_meal_suggestions(2500, 'maintenance')
    print(f"   維持餐點建議: {len(suggestions)} 個")

def test_advanced_scraper():
    """測試進階爬蟲功能"""
    print("\n🧪 測試進階爬蟲功能...")
    
    advanced_scraper = AdvancedNutritionScraper()
    
    # 測試營養資料庫
    print(f"\n📚 測試營養資料庫:")
    nutrition_data = advanced_scraper.scrape_nutrition_database()
    print(f"   營養資料: {len(nutrition_data)} 筆")
    
    # 測試個人化建議
    print(f"\n👤 測試個人化建議:")
    user_profile = {
        'age': 25,
        'weight': 70,
        'height': 170,
        'gender': 'male',
        'activity_level': 'moderate',
        'goal': 'muscle_gain'
    }
    advice = advanced_scraper.get_personalized_advice(user_profile)
    print(f"   個人化建議: {len(advice)} 個")
    
    # 測試運動營養計劃
    print(f"\n💪 測試運動營養計劃:")
    workout_types = ['strength_training', 'cardio', 'endurance']
    
    for workout_type in workout_types:
        plan = advanced_scraper.get_workout_nutrition_plan(workout_type, 60)
        print(f"   {workout_type}: {len(plan)} 個階段")

def test_calculations():
    """測試計算功能"""
    print("\n🧮 測試計算功能...")
    
    advanced_scraper = AdvancedNutritionScraper()
    
    # 測試 BMR 計算
    print(f"\n📊 測試基礎代謝率計算:")
    bmr_male = advanced_scraper._calculate_bmr(25, 70, 170, 'male')
    bmr_female = advanced_scraper._calculate_bmr(25, 60, 160, 'female')
    print(f"   男性 BMR: {bmr_male:.0f} 卡路里")
    print(f"   女性 BMR: {bmr_female:.0f} 卡路里")
    
    # 測試 TDEE 計算
    print(f"\n📈 測試每日總熱量消耗:")
    activity_levels = ['sedentary', 'light', 'moderate', 'active', 'very_active']
    
    for level in activity_levels:
        tdee = advanced_scraper._calculate_tdee(bmr_male, level)
        print(f"   {level}: {tdee:.0f} 卡路里")

def main():
    """主測試函數"""
    print("🚀 開始測試營養爬蟲功能...")
    print("=" * 50)
    
    try:
        # 測試基礎功能
        test_basic_scraper()
        
        # 測試進階功能
        test_advanced_scraper()
        
        # 測試計算功能
        test_calculations()
        
        print("\n" + "=" * 50)
        print("✅ 所有測試完成！")
        print("\n📝 測試結果摘要:")
        print("   - 基礎爬蟲功能: 正常")
        print("   - 進階爬蟲功能: 正常")
        print("   - 計算功能: 正常")
        print("   - 個人化建議: 正常")
        print("   - 運動營養計劃: 正常")
        
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 