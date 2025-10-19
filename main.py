#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات تلگرام قیمت‌یاب
نویسنده: Assistant
تاریخ: 2024
"""

import asyncio
import signal
import sys
from telegram_bot import TelegramBot

def signal_handler(signum, frame):
    """مدیریت سیگنال‌های توقف"""
    print("\n🛑 دریافت سیگنال توقف...")
    sys.exit(0)

async def main():
    """تابع اصلی"""
    print("🤖 شروع ربات تلگرام قیمت‌یاب...")
    print("=" * 50)
    
    # تنظیم سیگنال‌ها
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # ایجاد و شروع ربات
        bot = TelegramBot()
        
        print("📡 اتصال به تلگرام...")
        print("⏰ تنظیم زمان‌بندی...")
        print("🚀 شروع ارسال پیام‌ها...")
        
        # شروع ربات
        await bot.start()
        
    except KeyboardInterrupt:
        print("\n🛑 توقف ربات توسط کاربر...")
    except Exception as e:
        print(f"❌ خطا در اجرای ربات: {e}")
        sys.exit(1)
    finally:
        print("👋 ربات متوقف شد")

if __name__ == "__main__":
    # اجرای ربات
    asyncio.run(main())
