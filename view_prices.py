import json
from datetime import datetime

def view_prices():
    """نمایش قیمت‌های ذخیره شده"""
    try:
        with open('price_history.json', 'r', encoding='utf-8') as f:
            prices = json.load(f)
        
        print("=" * 60)
        print("💰 قیمت‌های ذخیره شده در ربات")
        print("=" * 60)
        print(f"📅 آخرین به‌روزرسانی: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
        print()
        
        # طلا و دلار
        print("🏆 طلا و دلار:")
        print("-" * 30)
        if 'dollar' in prices:
            print(f"💵 دلار: {prices['dollar']:,.0f} تومان")
        if 'gold_coin_emami' in prices:
            print(f"🪙 سکه امامی: {prices['gold_coin_emami']:,.0f} تومان")
        if 'gold_gram_18' in prices:
            print(f"🥇 گرم ۱۸ عیار: {prices['gold_gram_18']:,.0f} تومان")
        if 'gold_gram_24' in prices:
            print(f"🥇 گرم ۲۴ عیار: {prices['gold_gram_24']:,.0f} تومان")
        if 'gold_melted' in prices:
            print(f"🥇 طلای آب‌شده: {prices['gold_melted']:,.0f} تومان")
        if 'gold_ounce' in prices:
            print(f"🥇 انس طلا: {prices['gold_ounce']:,.2f} دلار")
        print()
        
        # ارزهای مهم
        print("🌍 ارزهای مهم:")
        print("-" * 30)
        currency_mapping = {
            'currency_euro': 'یورو',
            'currency_pound': 'پوند',
            'currency_yen': 'ین ژاپن',
            'currency_dirham': 'درهم امارات',
            'currency_kuwait_dinar': 'دینار کویت',
            'usdt_toman': 'تتر (تومان)'
        }
        
        for key, name in currency_mapping.items():
            if key in prices:
                print(f"💱 {name}: {prices[key]:,.0f} تومان")
        print()
        
        # ارزهای دیجیتال
        print("🪙 ارزهای دیجیتال:")
        print("-" * 30)
        crypto_mapping = {
            'crypto_bitcoin': 'بیت‌کوین',
            'crypto_ethereum': 'اتریوم',
            'crypto_tether': 'تتر',
            'crypto_xrp': 'ایکس‌آر‌پی',
            'crypto_bnb': 'بی‌ان‌بی',
            'crypto_solana': 'سولانا'
        }
        
        for key, name in crypto_mapping.items():
            if key in prices:
                if name == 'تتر':
                    print(f"💎 {name}: {prices[key]:,.2f} تومان")
                else:
                    print(f"💎 {name}: ${prices[key]:,.2f}")
        print()
        
        # شاخص‌های بورس
        print("📈 شاخص‌های بورس:")
        print("-" * 30)
        bourse_mapping = {
            'bourse_total': 'شاخص کل',
            'bourse_price': 'شاخص قیمت',
            'bourse_free_float': 'شاخص آزاد شناور',
            'bourse_market1': 'شاخص بازار اول',
            'bourse_market2': 'شاخص بازار دوم'
        }
        
        for key, name in bourse_mapping.items():
            if key in prices:
                print(f"📊 {name}: {prices[key]:,.2f}")
        print()
        
        # نمادهای بورس
        print("📋 نمادهای بورس:")
        print("-" * 30)
        symbol_count = 0
        for key, value in prices.items():
            if key.startswith('symbol_'):
                symbol_name = key.replace('symbol_', '')
                print(f"📈 {symbol_name}: {value:,.0f} تومان")
                symbol_count += 1
                if symbol_count >= 10:  # فقط 10 نماد اول
                    break
        print()
        
        print("=" * 60)
        print(f"📊 تعداد کل قیمت‌ها: {len(prices)}")
        print("=" * 60)
        
    except FileNotFoundError:
        print("❌ فایل price_history.json یافت نشد!")
    except Exception as e:
        print(f"❌ خطا در خواندن فایل: {e}")

if __name__ == "__main__":
    view_prices() 