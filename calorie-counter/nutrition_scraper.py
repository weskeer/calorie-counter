import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re
from typing import List, Dict, Optional

class NutritionScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_fitness_nutrition_tips(self, category: str = "general") -> List[Dict]:
        """
        爬取健身營養建議
        category: general, weight_loss, muscle_gain, endurance
        """
        tips = []
        
        try:
            # 這裡可以爬取多個健身營養網站
            if category == "weight_loss":
                tips.extend(self._scrape_weight_loss_tips())
            elif category == "muscle_gain":
                tips.extend(self._scrape_muscle_gain_tips())
            elif category == "endurance":
                tips.extend(self._scrape_endurance_tips())
            else:
                tips.extend(self._scrape_general_tips())
                
        except Exception as e:
            print(f"爬取過程中發生錯誤: {str(e)}")
            # 回傳預設建議
            tips = self._get_default_tips(category)
        
        return tips
    
    def _scrape_general_tips(self) -> List[Dict]:
        """爬取一般健身營養建議"""
        tips = []
        
        # 這裡可以爬取實際的健身網站，目前使用模擬資料
        general_tips = [
            {
                "title": "蛋白質攝取建議",
                "content": "每天攝取體重每公斤1.6-2.2克的蛋白質，有助於肌肉修復和生長。",
                "category": "protein",
                "source": "健身營養指南",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "碳水化合物的重要性",
                "content": "運動前2-3小時攝取適量碳水化合物，提供運動所需的能量。",
                "category": "carbohydrates",
                "source": "運動營養學",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "水分補充",
                "content": "運動前後都要充分補充水分，每小時運動至少補充500-1000ml的水。",
                "category": "hydration",
                "source": "運動醫學",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return general_tips
    
    def _scrape_weight_loss_tips(self) -> List[Dict]:
        """爬取減重營養建議"""
        tips = []
        
        weight_loss_tips = [
            {
                "title": "熱量赤字原則",
                "content": "每天創造300-500卡路里的熱量赤字，可以安全地每週減重0.5-1公斤。",
                "category": "weight_loss",
                "source": "減重營養學",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "高纖維食物",
                "content": "多攝取蔬菜、水果和全穀類，增加飽足感並促進腸道健康。",
                "category": "fiber",
                "source": "營養學研究",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "蛋白質優先",
                "content": "減重期間增加蛋白質攝取，有助於保持肌肉量並提高代謝率。",
                "category": "protein",
                "source": "減重科學",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return weight_loss_tips
    
    def _scrape_muscle_gain_tips(self) -> List[Dict]:
        """爬取增肌營養建議"""
        tips = []
        
        muscle_gain_tips = [
            {
                "title": "增肌期熱量盈餘",
                "content": "每天攝取比消耗多200-300卡路里，配合重量訓練促進肌肉生長。",
                "category": "muscle_gain",
                "source": "增肌營養學",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "訓練後營養補充",
                "content": "訓練後30分鐘內攝取20-30克蛋白質和適量碳水化合物，促進肌肉修復。",
                "category": "post_workout",
                "source": "運動營養學",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "肌酸補充",
                "content": "考慮補充肌酸，有助於提高訓練強度和肌肉力量。",
                "category": "supplements",
                "source": "運動營養研究",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return muscle_gain_tips
    
    def _scrape_endurance_tips(self) -> List[Dict]:
        """爬取耐力運動營養建議"""
        tips = []
        
        endurance_tips = [
            {
                "title": "碳水化合物負荷",
                "content": "長時間運動前24-48小時增加碳水化合物攝取，儲存肝醣。",
                "category": "endurance",
                "source": "耐力運動營養",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "運動中補充",
                "content": "運動超過1小時時，每小時補充30-60克碳水化合物和電解質。",
                "category": "during_exercise",
                "source": "運動醫學",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "恢復期營養",
                "content": "運動後2小時內補充碳水化合物和蛋白質，促進恢復。",
                "category": "recovery",
                "source": "運動營養學",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return endurance_tips
    
    def _get_default_tips(self, category: str) -> List[Dict]:
        """當爬取失敗時回傳預設建議"""
        default_tips = [
            {
                "title": "基本營養原則",
                "content": "均衡攝取蛋白質、碳水化合物和健康脂肪，配合適量運動。",
                "category": "general",
                "source": "營養學基礎",
                "timestamp": datetime.now().isoformat()
            }
        ]
        return default_tips
    
    def search_nutrition_info(self, query: str) -> List[Dict]:
        """搜尋特定營養資訊"""
        # 這裡可以實作搜尋功能，目前回傳模擬資料
        search_results = [
            {
                "title": f"關於 {query} 的營養資訊",
                "content": f"這裡是關於 {query} 的詳細營養資訊和建議。",
                "category": "search",
                "source": "營養資料庫",
                "timestamp": datetime.now().isoformat()
            }
        ]
        return search_results
    
    def get_meal_suggestions(self, calories: int, goal: str = "maintenance") -> List[Dict]:
        """根據卡路里和目標提供餐點建議"""
        suggestions = []
        
        if goal == "weight_loss":
            suggestions = [
                {
                    "meal": "早餐",
                    "suggestion": "燕麥粥配藍莓和堅果",
                    "calories": calories * 0.25,
                    "protein": "15g",
                    "carbs": "45g",
                    "fat": "8g"
                },
                {
                    "meal": "午餐",
                    "suggestion": "雞胸肉沙拉配糙米",
                    "calories": calories * 0.35,
                    "protein": "35g",
                    "carbs": "40g",
                    "fat": "12g"
                },
                {
                    "meal": "晚餐",
                    "suggestion": "鮭魚配蒸蔬菜",
                    "calories": calories * 0.30,
                    "protein": "30g",
                    "carbs": "25g",
                    "fat": "15g"
                },
                {
                    "meal": "點心",
                    "suggestion": "希臘優格配水果",
                    "calories": calories * 0.10,
                    "protein": "10g",
                    "carbs": "15g",
                    "fat": "5g"
                }
            ]
        else:
            suggestions = [
                {
                    "meal": "早餐",
                    "suggestion": "全麥吐司配雞蛋和酪梨",
                    "calories": calories * 0.25,
                    "protein": "20g",
                    "carbs": "50g",
                    "fat": "15g"
                },
                {
                    "meal": "午餐",
                    "suggestion": "牛肉漢堡配地瓜",
                    "calories": calories * 0.35,
                    "protein": "40g",
                    "carbs": "55g",
                    "fat": "20g"
                },
                {
                    "meal": "晚餐",
                    "suggestion": "雞胸肉配義大利麵",
                    "calories": calories * 0.30,
                    "protein": "35g",
                    "carbs": "60g",
                    "fat": "18g"
                },
                {
                    "meal": "點心",
                    "suggestion": "蛋白質奶昔配香蕉",
                    "calories": calories * 0.10,
                    "protein": "15g",
                    "carbs": "20g",
                    "fat": "8g"
                }
            ]
        
        return suggestions 