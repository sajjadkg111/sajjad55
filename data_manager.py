import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class DataManager:
    def __init__(self, data_file: str = "price_history.json"):
        self.data_file = data_file
        self.price_history = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        """بارگذاری داده‌های ذخیره شده"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        """ذخیره داده‌ها در فایل"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.price_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره داده‌ها: {e}")
    
    def get_previous_price(self, key: str) -> Optional[float]:
        """دریافت قیمت قبلی برای مقایسه"""
        price = self.price_history.get(key)
        if price is not None:
            try:
                return float(price)
            except (ValueError, TypeError):
                return None
        return None
    
    def update_price(self, key: str, price: Any):
        """به‌روزرسانی قیمت جدید"""
        try:
            # تبدیل به float برای ذخیره
            float_price = float(price)
            self.price_history[key] = float_price
            self.save_data()
        except (ValueError, TypeError) as e:
            print(f"خطا در تبدیل قیمت {key}: {price} - {e}")
    
    def get_price_change(self, key: str, current_price: Any) -> str:
        """محاسبه تغییرات قیمت و بازگرداندن ایموجی مناسب"""
        try:
            # تبدیل قیمت فعلی به float
            current_float = float(current_price)
            previous_price = self.get_previous_price(key)
            
            if previous_price is None:
                return "➖"
            
            if current_float > previous_price:
                return "🔺"
            elif current_float < previous_price:
                return "🔻"
            else:
                return "➖"
        except (ValueError, TypeError) as e:
            print(f"خطا در مقایسه قیمت {key}: {current_price} - {e}")
            return "➖"
    
    def format_price(self, price: Any) -> str:
        """فرمت‌بندی قیمت با کاما (همه قیمت‌ها به تومان یا دلار)"""
        try:
            # تبدیل به float و سپس int برای نمایش
            float_price = float(price)
            return f"{int(float_price):,}"
        except (ValueError, TypeError) as e:
            print(f"خطا در فرمت قیمت: {price} - {e}")
            return str(price)
    
    def get_current_time(self) -> str:
        """دریافت زمان فعلی"""
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S") 