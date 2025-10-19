#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست رفع خطاهای تبدیل نوع داده
"""

from data_manager import DataManager
from message_formatter import MessageFormatter

def test_data_manager_fixes():
    """تست رفع خطاهای DataManager"""
    print("=== تست رفع خطاهای DataManager ===")
    
    dm = DataManager()
    
    # تست با مقادیر مختلف
    test_cases = [
        ("test_price", 1000.5),
        ("test_string", "1500"),
        ("test_float", 2000.0),
        ("test_int", 3000),
        ("test_invalid", "invalid_price")
    ]
    
    for key, value in test_cases:
        print(f"\nتست {key}: {value} (نوع: {type(value)})")
        
        # تست update_price
        try:
            dm.update_price(key, value)
            print(f"  ✓ update_price موفق")
        except Exception as e:
            print(f"  ✗ update_price خطا: {e}")
        
        # تست format_price
        try:
            formatted = dm.format_price(value)
            print(f"  ✓ format_price: {formatted}")
        except Exception as e:
            print(f"  ✗ format_price خطا: {e}")
        
        # تست get_price_change
        try:
            change = dm.get_price_change(key, value)
            print(f"  ✓ get_price_change: {change}")
        except Exception as e:
            print(f"  ✗ get_price_change خطا: {e}")

def test_message_formatter_fixes():
    """تست رفع خطاهای MessageFormatter"""
    print("\n=== تست رفع خطاهای MessageFormatter ===")
    
    dm = DataManager()
    mf = MessageFormatter(dm)
    
    # تست با داده‌های ارزهای دیجیتال
    crypto_prices = {
        'crypto_bitcoin': 45000.5,
        'crypto_ethereum': "3200.75",
        'crypto_tether': 1.0,
        'crypto_invalid': "invalid_value"
    }
    
    try:
        message = mf.format_crypto_message(crypto_prices)
        print("✓ format_crypto_message موفق")
        print(f"پیام: {message[:200]}...")
    except Exception as e:
        print(f"✗ format_crypto_message خطا: {e}")

def test_edge_cases():
    """تست موارد خاص"""
    print("\n=== تست موارد خاص ===")
    
    dm = DataManager()
    mf = MessageFormatter(dm)
    
    # تست با داده‌های خالی
    try:
        message = mf.format_currency_message({})
        print("✓ format_currency_message با داده خالی موفق")
    except Exception as e:
        print(f"✗ format_currency_message با داده خالی خطا: {e}")
    
    # تست با داده‌های None
    try:
        message = mf.format_bourse_message(None)
        print("✓ format_bourse_message با None موفق")
    except Exception as e:
        print(f"✗ format_bourse_message با None خطا: {e}")

if __name__ == "__main__":
    print("شروع تست رفع خطاها...")
    
    test_data_manager_fixes()
    test_message_formatter_fixes()
    test_edge_cases()
    
    print("\n=== تست کامل شد ===")
