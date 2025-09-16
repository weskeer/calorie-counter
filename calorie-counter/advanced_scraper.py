import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import random

class AdvancedNutritionScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 健身網站列表
        self.fitness_sites = {
            'bodybuilding': {
                'base_url': 'https://www.bodybuilding.com',
                'nutrition_section': '/nutrition',
                'search_url': 'https://www.bodybuilding.com/search'
            },
            'men_health': {
                'base_url': 'https://www.menshealth.com',
                'nutrition_section': '/nutrition',
                'search_url': 'https://www.menshealth.com/search'
            },
            'women_health': {
                'base_url': 'https://www.womenshealthmag.com',
                'nutrition_section': '/nutrition',
                'search_url': 'https://www.womenshealthmag.com/search'
            }
        }
    
    def scrape_fitness_websites(self, query: str = "nutrition tips") -> List[Dict]:
        """爬取多個健身網站的營養資訊"""
        all_results = []
        
        for site_name, site_info in self.fitness_sites.items():
            try:
                results = self._scrape_single_site(site_name, site_info, query)
                all_results.extend(results)
                # 避免請求過於頻繁
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"爬取 {site_name} 時發生錯誤: {str(e)}")
                continue
        
        return all_results
    
    def _scrape_single_site(self, site_name: str, site_info: Dict, query: str) -> List[Dict]:
        """爬取單一網站的資訊"""
        results = []
        
        try:
            # 嘗試爬取營養相關頁面
            nutrition_url = urljoin(site_info['base_url'], site_info['nutrition_section'])
            response = self.session.get(nutrition_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 尋找文章標題和內容
                articles = soup.find_all(['article', 'div'], class_=re.compile(r'article|post|content'))
                
                for article in articles[:5]:  # 限制數量避免過度爬取
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                    content_elem = article.find(['p', 'div'], class_=re.compile(r'content|excerpt|summary'))
                    
                    if title_elem and content_elem:
                        title = title_elem.get_text(strip=True)
                        content = content_elem.get_text(strip=True)[:200] + "..."  # 限制長度
                        
                        if query.lower() in title.lower() or query.lower() in content.lower():
                            results.append({
                                "title": title,
                                "content": content,
                                "source": f"{site_name.title()}",
                                "url": nutrition_url,
                                "timestamp": datetime.now().isoformat(),
                                "category": "scraped"
                            })
            
        except Exception as e:
            print(f"爬取 {site_name} 詳細頁面時發生錯誤: {str(e)}")
        
        return results
    
    def scrape_nutrition_database(self) -> List[Dict]:
        """爬取營養資料庫資訊"""
        nutrition_data = [
            {
                "title": "蛋白質攝取指南",
                "content": "根據美國運動醫學學會建議，運動員每天應攝取體重每公斤1.2-2.0克的蛋白質。對於力量訓練者，建議攝取1.6-2.2克/公斤體重。",
                "source": "美國運動醫學學會",
                "category": "protein",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "碳水化合物補充策略",
                "content": "運動前2-4小時攝取1-4克/公斤體重的碳水化合物，運動中每小時補充30-60克，運動後立即補充1-1.2克/公斤體重。",
                "source": "國際運動營養學會",
                "category": "carbohydrates",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "脂肪攝取建議",
                "content": "脂肪應佔總熱量的20-35%，選擇健康脂肪如橄欖油、堅果、魚油等。避免反式脂肪和過量飽和脂肪。",
                "source": "美國心臟協會",
                "category": "fats",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "水分補充原則",
                "content": "運動前2小時補充500ml水，運動中每15-20分鐘補充150-300ml，運動後補充流失體重的1.5倍水分。",
                "source": "美國運動醫學學會",
                "category": "hydration",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "維生素D與運動表現",
                "content": "維生素D有助於肌肉功能和骨骼健康，建議每天攝取600-800IU，戶外運動者可能需要更多。",
                "source": "運動營養學研究",
                "category": "vitamins",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "運動後恢復營養",
                "content": "運動後30分鐘內攝取20-30克蛋白質和適量碳水化合物，有助於肌肉修復和肝醣補充。",
                "source": "運動醫學期刊",
                "category": "recovery",
                "timestamp": datetime.now().isoformat()
            }
            ,
            {
                "title": "鐵質（Iron）攝取要點",
                "content": "鐵質有助於血紅素形成與氧氣運輸。一般成人每日建議攝取量約為男性8mg、女性18mg（育齡期），素食者可考慮提高1.8倍；富含鐵質的食物包含紅肉、內臟、貝類、深綠色蔬菜與豆類。與維生素C同時攝取可提升吸收，避免與高劑量鈣質同時服用。",
                "source": "營養學參考資料",
                "category": "iron",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "鋅（Zinc）攝取要點",
                "content": "鋅參與免疫功能與傷口癒合。成年男性建議11mg/日、女性8mg/日。來源有紅肉、海鮮（特別是牡蠣）、全穀、堅果。高植酸飲食可能降低吸收。",
                "source": "營養學參考資料",
                "category": "zinc",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "鎂（Magnesium）攝取要點",
                "content": "鎂參與肌肉與神經功能、能量代謝。成年男性建議400–420mg/日、女性310–320mg/日。來源有堅果、全穀、深綠色蔬菜、豆類。",
                "source": "營養學參考資料",
                "category": "magnesium",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "鈣（Calcium）攝取要點",
                "content": "鈣維持骨骼與牙齒健康。多數成人建議1000mg/日（女性50歲以上、男性70歲以上1200mg/日）。來源有乳製品、小魚乾、深綠色蔬菜、強化飲品。",
                "source": "營養學參考資料",
                "category": "calcium",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "鉀（Potassium）攝取要點",
                "content": "鉀協助維持體液平衡與血壓。一般成人目標約2600–3400mg/日。來源有水果（香蕉、柑橘）、馬鈴薯、豆類、乳製品。腎臟疾病者需遵循醫囑。",
                "source": "營養學參考資料",
                "category": "potassium",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "維生素C（Vitamin C）攝取要點",
                "content": "維生素C具抗氧化並促進鐵吸收。成年男性90mg/日、女性75mg/日。來源有柑橘類、奇異果、彩椒、莓果。吸菸者需求較高。",
                "source": "營養學參考資料",
                "category": "vitamin_c",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "葉酸（Folate，維生素B9）攝取要點",
                "content": "葉酸參與DNA合成與胎兒神經管發育。成人400µg DFE/日，備孕與懷孕早期通常建議補充葉酸。來源有深綠色蔬菜、豆類、強化穀物。",
                "source": "營養學參考資料",
                "category": "folate",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return nutrition_data
    
    def get_personalized_advice(self, user_profile: Dict) -> List[Dict]:
        """根據用戶資料提供個人化建議"""
        advice = []
        
        age = user_profile.get('age', 25)
        weight = user_profile.get('weight', 70)
        height = user_profile.get('height', 170)
        activity_level = user_profile.get('activity_level', 'moderate')
        goal = user_profile.get('goal', 'maintenance')
        
        # 計算基礎代謝率 (BMR)
        bmr = self._calculate_bmr(age, weight, height, user_profile.get('gender', 'male'))
        
        # 計算每日總熱量需求
        tdee = self._calculate_tdee(bmr, activity_level)
        
        # 根據目標調整熱量
        if goal == 'weight_loss':
            target_calories = tdee - 500
            advice.append({
                "title": "減重期熱量建議",
                "content": f"您的每日熱量需求約為 {target_calories} 卡路里，建議創造500卡路里的熱量赤字。",
                "category": "calories",
                "source": "個人化計算",
                "timestamp": datetime.now().isoformat()
            })
        elif goal == 'muscle_gain':
            target_calories = tdee + 300
            advice.append({
                "title": "增肌期熱量建議",
                "content": f"您的每日熱量需求約為 {target_calories} 卡路里，建議增加300卡路里的熱量盈餘。",
                "category": "calories",
                "source": "個人化計算",
                "timestamp": datetime.now().isoformat()
            })
        else:
            target_calories = tdee
            advice.append({
                "title": "維持期熱量建議",
                "content": f"您的每日熱量需求約為 {target_calories} 卡路里，建議維持此熱量攝取。",
                "category": "calories",
                "source": "個人化計算",
                "timestamp": datetime.now().isoformat()
            })
        
        # 蛋白質建議
        protein_needs = weight * 1.6 if goal == 'muscle_gain' else weight * 1.2
        advice.append({
            "title": "蛋白質攝取建議",
            "content": f"建議每天攝取 {protein_needs:.0f} 克蛋白質，約佔總熱量的 {(protein_needs * 4 / target_calories * 100):.0f}%。",
            "category": "protein",
            "source": "個人化計算",
            "timestamp": datetime.now().isoformat()
        })
        
        # 碳水化合物建議
        carb_percentage = 0.45 if goal == 'weight_loss' else 0.55
        carb_needs = (target_calories * carb_percentage) / 4
        advice.append({
            "title": "碳水化合物攝取建議",
            "content": f"建議每天攝取 {carb_needs:.0f} 克碳水化合物，約佔總熱量的 {(carb_percentage * 100):.0f}%。",
            "category": "carbohydrates",
            "source": "個人化計算",
            "timestamp": datetime.now().isoformat()
        })
        
        return advice
    
    def _calculate_bmr(self, age: int, weight: float, height: float, gender: str) -> float:
        """計算基礎代謝率 (Mifflin-St Jeor 公式)"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr
    
    def _calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """計算每日總熱量消耗"""
        activity_multipliers = {
            'sedentary': 1.2,      # 久坐不動
            'light': 1.375,        # 輕度活動
            'moderate': 1.55,      # 中度活動
            'active': 1.725,       # 高度活動
            'very_active': 1.9     # 極度活動
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.55)
        return bmr * multiplier
    
    def get_workout_nutrition_plan(self, workout_type: str, duration: int) -> Dict:
        """根據運動類型和時長提供營養計劃"""
        plans = {
            'strength_training': {
                'pre_workout': {
                    'timing': '運動前2-3小時',
                    'foods': ['燕麥粥配香蕉', '全麥吐司配雞蛋', '希臘優格配堅果'],
                    'calories': 300,
                    'protein': '20-30g',
                    'carbs': '40-60g'
                },
                'during_workout': {
                    'timing': '運動中',
                    'foods': ['運動飲料', '能量膠'],
                    'calories': 100,
                    'protein': '0g',
                    'carbs': '25g'
                },
                'post_workout': {
                    'timing': '運動後30分鐘內',
                    'foods': ['蛋白質奶昔', '雞胸肉配糙米', '鮭魚配地瓜'],
                    'calories': 400,
                    'protein': '30-40g',
                    'carbs': '50-70g'
                }
            },
            'cardio': {
                'pre_workout': {
                    'timing': '運動前1-2小時',
                    'foods': ['香蕉', '能量棒', '果汁'],
                    'calories': 200,
                    'protein': '5-10g',
                    'carbs': '30-40g'
                },
                'during_workout': {
                    'timing': '運動中',
                    'foods': ['運動飲料', '能量膠', '水'],
                    'calories': 150,
                    'protein': '0g',
                    'carbs': '35g'
                },
                'post_workout': {
                    'timing': '運動後30分鐘內',
                    'foods': ['蛋白質奶昔', '水果', '全麥麵包'],
                    'calories': 300,
                    'protein': '20-25g',
                    'carbs': '40-50g'
                }
            },
            'endurance': {
                'pre_workout': {
                    'timing': '運動前3-4小時',
                    'foods': ['義大利麵', '糙米飯', '馬鈴薯'],
                    'calories': 500,
                    'protein': '15-20g',
                    'carbs': '80-100g'
                },
                'during_workout': {
                    'timing': '運動中每小時',
                    'foods': ['運動飲料', '能量膠', '香蕉'],
                    'calories': 200,
                    'protein': '0g',
                    'carbs': '50g'
                },
                'post_workout': {
                    'timing': '運動後2小時內',
                    'foods': ['蛋白質奶昔', '雞胸肉', '地瓜'],
                    'calories': 600,
                    'protein': '30-40g',
                    'carbs': '80-100g'
                }
            }
        }
        
        return plans.get(workout_type, plans['strength_training']) 

    # ----------------------
    # 多樣化餐點建議（隨機）
    # ----------------------
    def get_diverse_meal_suggestions(self, daily_calories: int, goal: str = 'maintenance') -> List[Dict]:
        """根據每日卡路里與健身目標，提供早餐/午餐/晚餐/點心的隨機餐點建議。

        - 僅回傳4筆（早餐、午餐、晚餐、點心）
        - 每次呼叫會隨機挑選不同餐點
        - 依目標調整宏量營養素比例與各餐熱量分配
        - 回傳每道餐點的估算熱量與營養素（克數）
        """
        goal_key = goal if goal in {'weight_loss', 'muscle_gain', 'maintenance'} else 'maintenance'

        # 各目標的宏量營養比例（以總熱量為基準）
        macro_profiles = {
            'weight_loss': {'protein': 0.30, 'carbs': 0.40, 'fat': 0.30},
            'maintenance': {'protein': 0.25, 'carbs': 0.50, 'fat': 0.25},
            'muscle_gain': {'protein': 0.30, 'carbs': 0.50, 'fat': 0.20},
        }

        # 各餐熱量分配
        meal_distribution = {
            '早餐': 0.25,
            '午餐': 0.35,
            '晚餐': 0.30,
            '點心': 0.10,
        }

        # 各目標下可隨機挑選的餐點池（可持續擴充）
        meal_pools = {
            '早餐': {
                'weight_loss': [
                    '高纖燕麥粥配藍莓與杏仁', '優格碗（希臘優格＋莓果＋奇亞籽）', '蛋白蛋餅配菠菜與番茄',
                    '酪梨全麥吐司配水煮蛋', '思慕昔碗（菠菜香蕉蛋白粉）', '低糖穀片配無糖豆奶'
                ],
                'maintenance': [
                    '花生醬香蕉全麥吐司', '雞蛋番茄起司墨西哥捲', '鮪魚沙拉全麥三明治',
                    '優格麥片杯', '地瓜泥配雞蛋與蔬菜', '燕麥牛奶粥配堅果'
                ],
                'muscle_gain': [
                    '高蛋白燕麥（加乳清、花生醬、香蕉）', '牛奶燕麥配葡萄乾與核桃', '三顆炒蛋配火雞胸與吐司',
                    '蛋白粉水果思慕昔', '鮭魚酪梨貝果', '奶油起司煙燻鮭魚三明治'
                ],
            },
            '午餐': {
                'weight_loss': [
                    '雞胸沙拉配藜麥與橄欖油', '鮭魚碗（花椰菜米＋蔬菜）', '豆腐蔬菜炒配糙米',
                    '火雞胸全麥捲餅', '蝦仁青醬西葫蘆麵', '韓式拌飯（少油版）'
                ],
                'maintenance': [
                    '牛肉糙米佛陀碗', '雞腿排配地瓜與時蔬', '鮭魚義大利麵（清炒）',
                    '照燒雞丼飯（減糖）', '豬里肌蔬菜炒烏龍', '香料雞胸捲餅'
                ],
                'muscle_gain': [
                    '牛排配白飯與沙拉', '雞胸義大利麵番茄肉醬', '鮭魚壽司碗（白飯＋蛋）',
                    '豬里肌咖哩飯（低油）', '牛肉起司捲餅配玉米', '雞腿排奶油焗馬鈴薯'
                ],
            },
            '晚餐': {
                'weight_loss': [
                    '香煎鮭魚配蒸蔬菜', '蒜香雞胸配花椰菜泥', '味噌烤鱈魚配菠菜',
                    '火雞肉丸配櫛瓜麵', '清炒蝦仁彩椒配藜麥', '番茄豆腐鍋配少量糙米'
                ],
                'maintenance': [
                    '牛肉蔬菜燉飯', '雞腿蘑菇奶油義大利麵（輕醬）', '烤鯖魚配味噌湯與白飯',
                    '泰式打拋雞配米飯（減糖）', '番茄海鮮鍋配全麥麵包', '日式親子丼（少油）'
                ],
                'muscle_gain': [
                    '奶油鮭魚義大利麵', '牛肉馬鈴薯燉菜配白飯', '雞胸起司焗通心粉',
                    '豬里肌番茄燉飯', '厚煎鮭魚排配奶油馬鈴薯泥', '日式牛丼（加蛋）'
                ],
            },
            '點心': {
                'weight_loss': [
                    '蘋果配花生醬（小份）', '胡蘿蔔條配鷹嘴豆泥', '蒟蒻果凍',
                    '水煮蛋一顆', '米餅配低脂起司', '無糖優格'
                ],
                'maintenance': [
                    '香蕉與堅果一把', '希臘優格蜂蜜', '全麥餅乾配起司',
                    '無糖豆漿', '玉米棒', '烤地瓜小份'
                ],
                'muscle_gain': [
                    '蛋白奶昔（乳清＋牛奶）', '花生醬三明治（小份）', '巧克力牛奶',
                    '優格加麥片', '堅果與葡萄乾混合', '起司棒＋餅乾'
                ],
            },
        }

        # 目標宏量比例
        profile = macro_profiles[goal_key]

        def pick(meal_name: str) -> str:
            pool = meal_pools[meal_name][goal_key]
            return random.choice(pool)

        def compute_macros(calories_for_meal: float) -> Dict:
            protein_g = calories_for_meal * profile['protein'] / 4.0
            carbs_g = calories_for_meal * profile['carbs'] / 4.0
            fat_g = calories_for_meal * profile['fat'] / 9.0
            # 加入小幅隨機波動以模擬份量差異（±7%）
            jitter = lambda x: max(0, x * random.uniform(0.93, 1.07))
            return {
                'protein_g': round(jitter(protein_g)),
                'carbs_g': round(jitter(carbs_g)),
                'fat_g': round(jitter(fat_g)),
            }

        results: List[Dict] = []
        for meal_name, frac in meal_distribution.items():
            cals = daily_calories * frac
            # 每餐熱量也加一點點隨機（±6%）
            cals = cals * random.uniform(0.94, 1.06)
            macros = compute_macros(cals)
            results.append({
                'meal': meal_name,
                'name': pick(meal_name),
                'calories': round(cals),
                **macros,
            })

        return results