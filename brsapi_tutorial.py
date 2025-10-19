#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 آموزش کامل کار با APIهای BRSAPI.ir با استفاده از Python
هدف: یادگیری کامل و عملی کار با وب‌سرویس‌های رایگان سایت brsapi.ir

این فایل شامل تمام endpoint های موجود در BRSAPI.ir است:
- قیمت طلا، سکه و ارز
- کامودیتی‌ها (فلزات، انرژی)
- ارزهای دیجیتال
- شاخص‌های بورس ایران
- نمادهای بورس
- سهامداران عمده
- کندل استیک (تاریخچه قیمت)

نویسنده: AI Assistant
تاریخ: 2025
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

# تنظیمات اولیه
API_KEY = "YourApiKey"  # کلید API خود را اینجا قرار دهید
BASE_URL = "https://BrsApi.ir/Api"

class BRSAPIClient:
    """
    کلاس اصلی برای کار با APIهای BRSAPI.ir
    شامل تمام endpoint های موجود با مدیریت خطا
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        انجام درخواست HTTP با مدیریت خطا
        
        Args:
            url: آدرس API
            params: پارامترهای درخواست
            
        Returns:
            داده‌های JSON یا None در صورت خطا
        """
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            # بررسی محتوای پاسخ
            content = response.text.strip()
            if not content:
                print(f"❌ پاسخ خالی از API: {url}")
                return None
            
            # بررسی اینکه آیا پاسخ JSON است
            if content.startswith('{') or content.startswith('['):
                return response.json()
            else:
                print(f"❌ پاسخ غیر JSON از API: {content[:100]}...")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در درخواست API: {e}")
            return None
        except ValueError as e:
            print(f"❌ خطا در پارس JSON: {e}")
            print(f"محتوای پاسخ: {response.text[:200]}...")
            return None
        except Exception as e:
            print(f"❌ خطای غیرمنتظره: {e}")
            return None

    # ==================== ۱. قیمت طلا، سکه و ارز ====================
    def get_gold_currency(self) -> Optional[Dict]:
        """
        دریافت قیمت طلا، سکه و ارز
        
        Endpoint: https://BrsApi.ir/Api/Market/Gold_Currency.php?key=YourApiKey
        
        Returns:
            دیکشنری شامل اطلاعات طلا، سکه و ارزها
        """
        url = f"{BASE_URL}/Market/Gold_Currency.php"
        params = {'key': self.api_key}
        
        print("🪙 دریافت قیمت طلا، سکه و ارز...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ داده‌های طلا و ارز دریافت شد: {len(data)} مورد")
            return data
        else:
            print("❌ خطا در دریافت داده‌های طلا و ارز")
            return None

    # ==================== ۲. کامودیتی‌ها (فلزات، انرژی) ====================
    def get_commodity(self) -> Optional[Dict]:
        """
        دریافت قیمت کامودیتی‌ها (فلزات، انرژی)
        
        Endpoint: https://BrsApi.ir/Api/Market/Commodity.php?key=YourApiKey
        
        Returns:
            دیکشنری شامل اطلاعات کامودیتی‌ها
        """
        url = f"{BASE_URL}/Market/Commodity.php"
        params = {'key': self.api_key}
        
        print("🛢️ دریافت قیمت کامودیتی‌ها...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ داده‌های کامودیتی دریافت شد: {len(data)} مورد")
            return data
        else:
            print("❌ خطا در دریافت داده‌های کامودیتی")
            return None

    # ==================== ۳. ارزهای دیجیتال ====================
    def get_cryptocurrency(self) -> Optional[Dict]:
        """
        دریافت قیمت ارزهای دیجیتال
        
        Endpoint: https://BrsApi.ir/Api/Market/Cryptocurrency.php?key=YourApiKey
        
        Returns:
            دیکشنری شامل اطلاعات ارزهای دیجیتال
        """
        url = f"{BASE_URL}/Market/Cryptocurrency.php"
        params = {'key': self.api_key}
        
        print("🪙 دریافت قیمت ارزهای دیجیتال...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ داده‌های ارزهای دیجیتال دریافت شد: {len(data)} مورد")
            return data
        else:
            print("❌ خطا در دریافت داده‌های ارزهای دیجیتال")
            return None

    # ==================== ۴. شاخص‌های بورس ایران ====================
    def get_index(self, index_type: int = 1) -> Optional[List]:
        """
        دریافت شاخص‌های بورس ایران
        
        Endpoint: https://BrsApi.ir/Api/Tsetmc/Index.php?key=YourApiKey&type=1
        
        Args:
            index_type: نوع شاخص
                1 = شاخص سهام
                2 = شاخص کالا
                3 = شاخص‌های منتخب
                
        Returns:
            لیست شامل اطلاعات شاخص‌ها
        """
        url = f"{BASE_URL}/Tsetmc/Index.php"
        params = {
            'key': self.api_key,
            'type': index_type
        }
        
        type_names = {1: "سهام", 2: "کالا", 3: "منتخب"}
        type_name = type_names.get(index_type, f"نوع {index_type}")
        
        print(f"📈 دریافت شاخص‌های {type_name}...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ داده‌های شاخص {type_name} دریافت شد: {len(data)} مورد")
            return data
        else:
            print(f"❌ خطا در دریافت داده‌های شاخص {type_name}")
            return None

    # ==================== ۵. نمادهای بورس ====================
    def get_symbol(self, symbol: str) -> Optional[Dict]:
        """
        دریافت اطلاعات نماد بورس
        
        Endpoint: https://BrsApi.ir/Api/Tsetmc/Symbol.php?key=YourApiKey&l18=Symbol
        
        Args:
            symbol: نماد بورس (مثل: خودرو، فولاد، شستا)
            
        Returns:
            دیکشنری شامل اطلاعات کامل نماد
        """
        url = f"{BASE_URL}/Tsetmc/Symbol.php"
        params = {
            'key': self.api_key,
            'l18': symbol
        }
        
        print(f"🏢 دریافت اطلاعات نماد {symbol}...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ اطلاعات نماد {symbol} دریافت شد")
            return data
        else:
            print(f"❌ خطا در دریافت اطلاعات نماد {symbol}")
            return None

    # ==================== ۶. سهامداران عمده ====================
    def get_shareholders(self, symbol: str) -> Optional[List]:
        """
        دریافت سهامداران عمده نماد
        
        Endpoint: https://BrsApi.ir/Api/Tsetmc/Shareholder.php?key=YourApiKey&l18=Symbol
        
        Args:
            symbol: نماد بورس
            
        Returns:
            لیست شامل سهامداران عمده
        """
        url = f"{BASE_URL}/Tsetmc/Shareholder.php"
        params = {
            'key': self.api_key,
            'l18': symbol
        }
        
        print(f"👥 دریافت سهامداران عمده {symbol}...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ سهامداران عمده {symbol} دریافت شد: {len(data)} مورد")
            return data
        else:
            print(f"❌ خطا در دریافت سهامداران عمده {symbol}")
            return None

    # ==================== ۷. کندل استیک ====================
    def get_candlestick(self, symbol: str, candle_type: int = 1, count: int = 10) -> Optional[List]:
        """
        دریافت کندل استیک (تاریخچه قیمت نماد)
        
        Endpoint: https://BrsApi.ir/Api/Tsetmc/Candlestick.php?key=YourApiKey&type=1&l18=Symbol&count=10
        
        Args:
            symbol: نماد بورس
            candle_type: نوع کندل (1=روزانه بدون تعدیل)
            count: تعداد کندل بازگشتی
            
        Returns:
            لیست شامل کندل‌های قیمت
        """
        url = f"{BASE_URL}/Tsetmc/Candlestick.php"
        params = {
            'key': self.api_key,
            'l18': symbol,
            'type': candle_type,
            'count': count
        }
        
        print(f"📊 دریافت کندل استیک {symbol} ({count} روز)...")
        data = self.make_request(url, params)
        
        if data:
            print(f"✅ کندل استیک {symbol} دریافت شد: {len(data)} کندل")
            return data
        else:
            print(f"❌ خطا در دریافت کندل استیک {symbol}")
            return None

    # ==================== توابع کمکی ====================
    def format_price(self, price: Any) -> str:
        """فرمت کردن قیمت با جداکننده هزارگان"""
        try:
            return f"{int(float(price)):,}"
        except:
            return str(price)
    
    def format_percent(self, percent: Any) -> str:
        """فرمت کردن درصد"""
        try:
            return f"{float(percent):.2f}%"
        except:
            return str(percent)
    
    def extract_useful_data(self, data: Any, data_type: str) -> Dict:
        """استخراج داده‌های مفید از پاسخ API"""
        if not data:
            return {}
        
        extracted = {}
        
        if data_type == "gold_currency":
            # استخراج دلار، یورو، طلا
            for item in data:
                if isinstance(item, dict):
                    symbol = item.get('symbol', '')
                    name = item.get('name', '')
                    price = item.get('price', 0)
                    
                    if 'USD' in symbol or 'دلار' in name:
                        extracted['دلار'] = self.format_price(price)
                    elif 'EUR' in symbol or 'یورو' in name:
                        extracted['یورو'] = self.format_price(price)
                    elif 'طلا' in name or 'GOLD' in symbol:
                        extracted['طلا'] = self.format_price(price)
        
        elif data_type == "crypto":
            # استخراج بیت‌کوین و اتریوم
            for item in data:
                if isinstance(item, dict):
                    name = item.get('name', '')
                    price = item.get('price', 0)
                    
                    if 'Bitcoin' in name or 'بیت' in name:
                        extracted['بیت‌کوین'] = self.format_price(price)
                    elif 'Ethereum' in name or 'اتریوم' in name:
                        extracted['اتریوم'] = self.format_price(price)
        
        elif data_type == "index":
            # استخراج شاخص کل
            for item in data:
                if isinstance(item, dict):
                    name = item.get('name', '')
                    index = item.get('index', 0)
                    
                    if 'کل' in name or 'TEDPIX' in name:
                        extracted['شاخص کل'] = self.format_price(index)
        
        return extracted

# ==================== نمونه استفاده ====================
def main():
    """نمونه استفاده از کلاس BRSAPIClient"""
    
    # ایجاد نمونه کلاس
    client = BRSAPIClient(API_KEY)
    
    print("🚀 شروع تست APIهای BRSAPI.ir")
    print("=" * 50)
    
    # ۱. تست دریافت قیمت طلا و ارز
    print("\n📦 تست دریافت قیمت طلا و ارز:")
    gold_data = client.get_gold_currency()
    if gold_data:
        useful_data = client.extract_useful_data(gold_data, "gold_currency")
        for name, price in useful_data.items():
            print(f"  {name}: {price} تومان")
    
    # ۲. تست دریافت کامودیتی‌ها
    print("\n🛢️ تست دریافت کامودیتی‌ها:")
    commodity_data = client.get_commodity()
    if commodity_data and len(commodity_data) > 0:
        first_item = commodity_data[0]
        print(f"  {first_item.get('name', 'نامشخص')}: {first_item.get('price', 0)} {first_item.get('unit', '')}")
    
    # ۳. تست دریافت ارزهای دیجیتال
    print("\n🪙 تست دریافت ارزهای دیجیتال:")
    crypto_data = client.get_cryptocurrency()
    if crypto_data:
        useful_data = client.extract_useful_data(crypto_data, "crypto")
        for name, price in useful_data.items():
            print(f"  {name}: {price} دلار")
    
    # ۴. تست دریافت شاخص‌های بورس
    print("\n📈 تست دریافت شاخص‌های بورس:")
    index_data = client.get_index(1)  # شاخص سهام
    if index_data:
        useful_data = client.extract_useful_data(index_data, "index")
        for name, value in useful_data.items():
            print(f"  {name}: {value}")
    
    # ۵. تست دریافت اطلاعات نماد
    print("\n🏢 تست دریافت اطلاعات نماد خودرو:")
    symbol_data = client.get_symbol("خودرو")
    if symbol_data:
        last_price = symbol_data.get('pl', 'نامشخص')
        print(f"  آخرین قیمت خودرو: {last_price}")
    
    # ۶. تست دریافت سهامداران عمده
    print("\n👥 تست دریافت سهامداران عمده خودرو:")
    shareholders_data = client.get_shareholders("خودرو")
    if shareholders_data and len(shareholders_data) > 0:
        for i, holder in enumerate(shareholders_data[:3]):  # فقط ۳ مورد اول
            name = holder.get('name', 'نامشخص')
            percent = holder.get('percent', 0)
            print(f"  {i+1}. {name}: {percent}%")
    
    # ۷. تست دریافت کندل استیک
    print("\n📊 تست دریافت کندل استیک فولاد:")
    candlestick_data = client.get_candlestick("فولاد", count=5)
    if candlestick_data and len(candlestick_data) > 0:
        latest_candle = candlestick_data[-1]
        date = latest_candle.get('date', 'نامشخص')
        close = latest_candle.get('close', 0)
        print(f"  آخرین کندل فولاد ({date}): {close}")
    
    print("\n✅ تست کامل شد!")

# ==================== توابع پیشرفته ====================
def create_market_dashboard():
    """ایجاد داشبورد کامل بازار"""
    client = BRSAPIClient(API_KEY)
    
    dashboard = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'gold_currency': {},
        'commodity': {},
        'crypto': {},
        'index': {},
        'top_symbols': []
    }
    
    # دریافت داده‌های طلا و ارز
    gold_data = client.get_gold_currency()
    if gold_data:
        dashboard['gold_currency'] = client.extract_useful_data(gold_data, "gold_currency")
    
    # دریافت داده‌های کامودیتی
    commodity_data = client.get_commodity()
    if commodity_data:
        dashboard['commodity'] = {
            item.get('name', 'نامشخص'): item.get('price', 0) 
            for item in commodity_data[:5]  # ۵ مورد اول
        }
    
    # دریافت داده‌های ارزهای دیجیتال
    crypto_data = client.get_cryptocurrency()
    if crypto_data:
        dashboard['crypto'] = client.extract_useful_data(crypto_data, "crypto")
    
    # دریافت شاخص‌های بورس
    index_data = client.get_index(1)
    if index_data:
        dashboard['index'] = client.extract_useful_data(index_data, "index")
    
    return dashboard

def save_data_to_file(data: Dict, filename: str):
    """ذخیره داده‌ها در فایل JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ داده‌ها در فایل {filename} ذخیره شد")
    except Exception as e:
        print(f"❌ خطا در ذخیره فایل: {e}")

def load_data_from_file(filename: str) -> Dict:
    """بارگذاری داده‌ها از فایل JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ خطا در بارگذاری فایل: {e}")
        return {}

# ==================== مثال‌های پیشرفته ====================
def example_advanced_usage():
    """مثال‌های پیشرفته استفاده از API"""
    
    client = BRSAPIClient(API_KEY)
    
    print("🧠 مثال‌های پیشرفته:")
    print("=" * 30)
    
    # مثال ۱: دریافت و مقایسه قیمت‌ها
    print("\n📊 مثال ۱: مقایسه قیمت‌های مختلف")
    
    gold_data = client.get_gold_currency()
    crypto_data = client.get_cryptocurrency()
    
    if gold_data and crypto_data:
        print("قیمت‌های فعلی:")
        
        # استخراج دلار
        dollar_price = None
        for item in gold_data:
            if 'USD' in item.get('symbol', ''):
                dollar_price = item.get('price', 0)
                break
        
        # استخراج بیت‌کوین
        bitcoin_price = None
        for item in crypto_data:
            if 'Bitcoin' in item.get('name', ''):
                bitcoin_price = item.get('price', 0)
                break
        
        if dollar_price and bitcoin_price:
            bitcoin_toman = float(bitcoin_price) * float(dollar_price)
            print(f"  دلار: {client.format_price(dollar_price)} تومان")
            print(f"  بیت‌کوین: {client.format_price(bitcoin_price)} دلار")
            print(f"  بیت‌کوین: {client.format_price(bitcoin_toman)} تومان")
    
    # مثال ۲: تحلیل روند قیمت
    print("\n📈 مثال ۲: تحلیل روند قیمت فولاد")
    
    candlestick_data = client.get_candlestick("فولاد", count=10)
    if candlestick_data and len(candlestick_data) >= 2:
        latest = candlestick_data[-1]
        previous = candlestick_data[-2]
        
        latest_close = float(latest.get('close', 0))
        previous_close = float(previous.get('close', 0))
        
        if previous_close > 0:
            change_percent = ((latest_close - previous_close) / previous_close) * 100
            change_text = "📈 افزایش" if change_percent > 0 else "📉 کاهش"
            print(f"  {change_text}: {abs(change_percent):.2f}%")
            print(f"  قیمت فعلی: {client.format_price(latest_close)}")
            print(f"  قیمت قبلی: {client.format_price(previous_close)}")
    
    # مثال ۳: بررسی سهامداران عمده
    print("\n👥 مثال ۳: بررسی سهامداران عمده خودرو")
    
    shareholders_data = client.get_shareholders("خودرو")
    if shareholders_data:
        total_percent = sum(float(holder.get('percent', 0)) for holder in shareholders_data)
        print(f"  مجموع درصد سهامداران عمده: {total_percent:.2f}%")
        
        # سهامداران با بیشترین درصد
        top_holders = sorted(shareholders_data, key=lambda x: float(x.get('percent', 0)), reverse=True)[:3]
        print("  سهامداران عمده:")
        for i, holder in enumerate(top_holders, 1):
            name = holder.get('name', 'نامشخص')
            percent = holder.get('percent', 0)
            volume = holder.get('volume', 0)
            print(f"    {i}. {name}: {percent}% ({client.format_price(volume)} سهم)")

if __name__ == "__main__":
    # تست اصلی
    main()
    
    # مثال‌های پیشرفته
    example_advanced_usage()
    
    # ایجاد داشبورد
    print("\n🎯 ایجاد داشبورد کامل بازار:")
    dashboard = create_market_dashboard()
    save_data_to_file(dashboard, 'market_dashboard.json')
    
    print("\n📚 آموزش کامل شد!")
    print("برای اطلاعات بیشتر به مستندات BRSAPI.ir مراجعه کنید.") 