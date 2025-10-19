

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست API های واقعی
"""

from api_client import APIClient

def test_real_apis():
    """تست API های واقعی"""
    print("🧪 تست API های واقعی")
    print("=" * 40)
    
    client = APIClient()
    
    # تست API طلا و ارز
    print("📊 تست API طلا و ارز...")
    gold_data = client.get_gold_currency_data()
    if gold_data:
        print("✅ API طلا و ارز کار می‌کند")
        print(f"📄 ساختار داده: {type(gold_data)}")
        if isinstance(gold_data, list):
            print(f"📊 تعداد آیتم‌ها: {len(gold_data)}")
            if gold_data:
                print(f"📋 نمونه آیتم: {gold_data[0]}")
        prices = client.extract_prices(gold_data)
        print(f"📈 قیمت‌های استخراج شده: {prices}")
    else:
        print("❌ API طلا و ارز کار نمی‌کند")
    
    # تست API بورس
    print("\n📈 تست API بورس...")
    bourse_data = client.get_bourse_data()
    if bourse_data:
        print("✅ API بورس کار می‌کند")
        print(f"📄 ساختار داده: {type(bourse_data)}")
        if isinstance(bourse_data, dict):
            print(f"📋 نمونه داده: {bourse_data}")
        prices = client.extract_prices(bourse_data)
        print(f"📈 شاخص‌های استخراج شده: {prices}")
    else:
        print("❌ API بورس کار نمی‌کند")
    
    # تست API نمادهای بورس
    print("\n📊 تست API نمادهای بورس...")
    symbols_data = client.get_symbols_data()
    if symbols_data:
        print("✅ API نمادهای بورس کار می‌کند")
        print(f"📄 ساختار داده: {type(symbols_data)}")
        if isinstance(symbols_data, list):
            print(f"📊 تعداد نمادها: {len(symbols_data)}")
            if symbols_data:
                print(f"📋 نمونه نماد: {symbols_data[0]}")
        prices = client.extract_prices(symbols_data)
        print(f"📈 نمادهای استخراج شده: {len([k for k in prices.keys() if k.startswith('symbol_')])} نماد")
    else:
        print("❌ API نمادهای بورس کار نمی‌کند")
    
    print("\n" + "=" * 40)
    print("✅ تست تکمیل شد")

if __name__ == "__main__":
    test_real_apis() 