from typing import Dict, List
from data_manager import DataManager
from config import STICKERS

class MessageFormatter:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def format_gold_dollar_message(self, prices: Dict[str, float]) -> str:
        """فرمت‌بندی پیام طلا و دلار"""
        if not prices:
            return "❌ خطا در دریافت اطلاعات طلا و دلار"
        
        message = f"🏆 قیمت لحظه‌ای طلا و دلار\n"
        message += f"⏰ {self.data_manager.get_current_time()}\n"
        message += "=" * 30 + "\n\n"
        
        # ابتدا تمام قیمت‌ها را به‌روزرسانی می‌کنیم
        updated_prices = {}
        
        # قیمت دلار
        if 'dollar' in prices:
            dollar_price = prices['dollar']
            dollar_change = self.data_manager.get_price_change('dollar', dollar_price)
            message += f"💵 دلار: {self.data_manager.format_price(dollar_price)} تومان {dollar_change}\n"
            updated_prices['dollar'] = dollar_price
        
        # سکه امامی
        if 'gold_coin_emami' in prices:
            coin_price = prices['gold_coin_emami']
            coin_change = self.data_manager.get_price_change('gold_coin_emami', coin_price)
            message += f"🪙 سکه امامی: {self.data_manager.format_price(coin_price)} تومان {coin_change}\n"
            updated_prices['gold_coin_emami'] = coin_price
        
        # گرم ۱۸ عیار
        if 'gold_gram_18' in prices:
            gram_price = prices['gold_gram_18']
            gram_change = self.data_manager.get_price_change('gold_gram_18', gram_price)
            message += f"🥇 گرم ۱۸ عیار: {self.data_manager.format_price(gram_price)} تومان {gram_change}\n"
            updated_prices['gold_gram_18'] = gram_price
        
        # گرم ۲۴ عیار
        if 'gold_gram_24' in prices:
            gold24_price = prices['gold_gram_24']
            gold24_change = self.data_manager.get_price_change('gold_gram_24', gold24_price)
            message += f"🥇 گرم ۲۴ عیار: {self.data_manager.format_price(gold24_price)} تومان {gold24_change}\n"
            updated_prices['gold_gram_24'] = gold24_price
        
        # طلای آب‌شده
        if 'gold_melted' in prices:
            melted_price = prices['gold_melted']
            melted_change = self.data_manager.get_price_change('gold_melted', melted_price)
            message += f"🥇 طلای آب‌شده: {self.data_manager.format_price(melted_price)} تومان {melted_change}\n"
            updated_prices['gold_melted'] = melted_price
        
        # انس طلا
        if 'gold_ounce' in prices:
            ounce_price = prices['gold_ounce']
            ounce_change = self.data_manager.get_price_change('gold_ounce', ounce_price)
            message += f"🥇 انس طلا: {self.data_manager.format_price(ounce_price)} دلار {ounce_change}\n"
            updated_prices['gold_ounce'] = ounce_price
        
        # سکه یک گرمی
        if 'gold_coin_1g' in prices:
            coin1g_price = prices['gold_coin_1g']
            coin1g_change = self.data_manager.get_price_change('gold_coin_1g', coin1g_price)
            message += f"🪙 سکه یک گرمی: {self.data_manager.format_price(coin1g_price)} تومان {coin1g_change}\n"
            updated_prices['gold_coin_1g'] = coin1g_price
        
        # ربع سکه
        if 'gold_coin_quarter' in prices:
            quarter_price = prices['gold_coin_quarter']
            quarter_change = self.data_manager.get_price_change('gold_coin_quarter', quarter_price)
            message += f"🪙 ربع سکه: {self.data_manager.format_price(quarter_price)} تومان {quarter_change}\n"
            updated_prices['gold_coin_quarter'] = quarter_price
        
        # نیم سکه
        if 'gold_coin_half' in prices:
            half_price = prices['gold_coin_half']
            half_change = self.data_manager.get_price_change('gold_coin_half', half_price)
            message += f"🪙 نیم سکه: {self.data_manager.format_price(half_price)} تومان {half_change}\n"
            updated_prices['gold_coin_half'] = half_price
        
        # سکه بهار آزادی
        if 'gold_coin_bahar' in prices:
            bahar_price = prices['gold_coin_bahar']
            bahar_change = self.data_manager.get_price_change('gold_coin_bahar', bahar_price)
            message += f"🪙 سکه بهار آزادی: {self.data_manager.format_price(bahar_price)} تومان {bahar_change}\n"
            updated_prices['gold_coin_bahar'] = bahar_price
        
        message += "\n📊 تحلیل روند: "
        if any('🔺' in line for line in message.split('\n')):
            message += "صعودی 📈"
        elif any('🔻' in line for line in message.split('\n')):
            message += "نزولی 📉"
        else:
            message += "پایدار 📊"
        
        message += "\n\n📢 کانال ما: @Dollar_404_58"
        
        # به‌روزرسانی تمام قیمت‌ها در انتها
        for key, price in updated_prices.items():
            self.data_manager.update_price(key, price)
        
        return message
    
    def format_currency_message(self, prices: Dict[str, float]) -> str:
        """فرمت‌بندی پیام ارزهای مختلف"""
        if not prices:
            return "❌ خطا در دریافت اطلاعات ارزها"
        
        message = f"🌍 قیمت ارزهای جهانی\n"
        message += f"⏰ {self.data_manager.get_current_time()}\n"
        message += "=" * 30 + "\n\n"
        
        # ارزهای اصلی
        currency_mapping = {
            'currency_euro': 'یورو',
            'currency_pound': 'پوند',
            'currency_yen': 'ین ژاپن',
            'currency_dirham': 'درهم امارات',
            'currency_kuwait_dinar': 'دینار کویت',
            'currency_australian_dollar': 'دلار استرالیا',
            'currency_canadian_dollar': 'دلار کانادا',
            'currency_chinese_yuan': 'یوآن چین',
            'currency_turkish_lira': 'لیر ترکیه',
            'currency_saudi_riyal': 'ریال عربستان',
            'currency_swiss_franc': 'فرانک سوئیس',
            'currency_indian_rupee': 'روپیه هند',
            'currency_pakistani_rupee': 'روپیه پاکستان',
            'currency_iraqi_dinar': 'دینار عراق',
            'currency_syrian_lira': 'لیر سوریه',
            'currency_swedish_krona': 'کرون سوئد',
            'currency_qatari_riyal': 'ریال قطر',
            'currency_omani_rial': 'ریال عمان',
            'currency_bahraini_dinar': 'دینار بحرین',
            'currency_afghan_afghani': 'افغانی',
            'currency_malaysian_ringgit': 'رینگیت مالزی',
            'currency_thai_baht': 'بات تایلند',
            'currency_russian_ruble': 'روبل روسیه',
            'currency_azerbaijani_manat': 'منات آذربایجان',
            'currency_armenian_dram': 'درام ارمنستان',
            'currency_georgian_lari': 'لاری گرجستان',
            'usdt_toman': 'تتر (تومان)'
        }
        
        for currency_key, price in prices.items():
            if currency_key in currency_mapping:
                currency_name = currency_mapping[currency_key]
                change = self.data_manager.get_price_change(currency_key, price)
                message += f"💱 {currency_name}: {self.data_manager.format_price(price)} تومان {change}\n"
                self.data_manager.update_price(currency_key, price)
        
        message += "\n📊 تحلیل روند: "
        if any('🔺' in line for line in message.split('\n')):
            message += "صعودی 📈"
        elif any('🔻' in line for line in message.split('\n')):
            message += "نزولی 📉"
        else:
            message += "پایدار 📊"
        
        message += "\n\n📢 کانال ما: @Dollar_404_58"
        
        return message
    
    def format_crypto_message(self, prices: Dict[str, float]) -> str:
        """فرمت‌بندی پیام ارزهای دیجیتال"""
        if not prices:
            return "❌ خطا در دریافت اطلاعات ارزهای دیجیتال"
        
        message = f"🪙 قیمت ارزهای دیجیتال\n"
        message += f"⏰ {self.data_manager.get_current_time()}\n"
        message += "=" * 30 + "\n\n"
        
        # ارزهای دیجیتال اصلی
        crypto_mapping = {
            'crypto_bitcoin': 'بیت‌کوین',
            'crypto_ethereum': 'اتریوم',
            'crypto_tether': 'تتر',
            'crypto_xrp': 'ایکس‌آر‌پی',
            'crypto_bnb': 'بی‌ان‌بی',
            'crypto_solana': 'سولانا',
            'crypto_usd_coin': 'یواس‌دی کوین',
            'crypto_tron': 'ترون',
            'crypto_dogecoin': 'دوج‌کوین',
            'crypto_cardano': 'کاردانو',
            'crypto_chainlink': 'چین‌لینک',
            'crypto_stellar': 'استلار',
            'crypto_avalanche': 'آوالانچ',
            'crypto_shiba_inu': 'شیبا اینو',
            'crypto_litecoin': 'لایت‌کوین',
            'crypto_polkadot': 'پولکادات',
            'crypto_uniswap': 'یونی‌سواپ',
            'crypto_cosmos': 'کازماس',
            'crypto_filecoin': 'فایل‌کوین'
        }
        
        for crypto_key, price in prices.items():
            if crypto_key in crypto_mapping:
                crypto_name = crypto_mapping[crypto_key]
                change = self.data_manager.get_price_change(crypto_key, price)
                
                # تشخیص تتر و نمایش به تومان
                if crypto_name == 'تتر':
                    # اگر قیمت تتر کمتر از 1000 است، احتمالاً به دلار است و باید به تومان تبدیل شود
                    try:
                        price_float = float(price)
                        if price_float < 1000:
                            # تبدیل دلار به تومان (تقریبی)
                            toman_price = price_float * 580000  # نرخ تقریبی دلار
                            message += f"💎 {crypto_name}: {self.data_manager.format_price(toman_price)} تومان {change}\n"
                        else:
                            message += f"💎 {crypto_name}: {self.data_manager.format_price(price)} تومان {change}\n"
                    except (ValueError, TypeError):
                        message += f"💎 {crypto_name}: {self.data_manager.format_price(price)} تومان {change}\n"
                else:
                    try:
                        price_float = float(price)
                        message += f"💎 {crypto_name}: ${price_float:,.2f} {change}\n"
                    except (ValueError, TypeError):
                        message += f"💎 {crypto_name}: ${price} {change}\n"
                
                self.data_manager.update_price(crypto_key, price)
        
        message += "\n📊 تحلیل روند: "
        if any('🔺' in line for line in message.split('\n')):
            message += "صعودی 📈"
        elif any('🔻' in line for line in message.split('\n')):
            message += "نزولی 📉"
        else:
            message += "پایدار 📊"
        
        message += "\n\n📢 کانال ما: @Dollar_404_58"
        
        return message
    
    def format_bourse_message(self, prices: Dict[str, float]) -> str:
        """فرمت‌بندی پیام شاخص‌های بورس"""
        if not prices:
            return "❌ خطا در دریافت اطلاعات بورس"
        
        message = f"📈 شاخص‌های بورس ایران\n"
        message += f"⏰ {self.data_manager.get_current_time()}\n"
        message += "=" * 30 + "\n\n"
        
        # شاخص‌های اصلی
        bourse_mapping = {
            'bourse_total': 'شاخص کل',
            'bourse_equal_weight': 'شاخص هم‌وزن',
            'bourse_farabourse': 'شاخص فرابورس',
            'bourse_price': 'شاخص قیمت',
            'bourse_free_float': 'شاخص آزاد شناور',
            'bourse_market1': 'شاخص بازار اول',
            'bourse_market2': 'شاخص بازار دوم'
        }
        
        # نمایش شاخص‌های اصلی
        for bourse_key, persian_name in bourse_mapping.items():
            if bourse_key in prices:
                value = prices[bourse_key]
                change = self.data_manager.get_price_change(bourse_key, value)
                message += f"📊 {persian_name}: {self.data_manager.format_price(value)} {change}\n"
                self.data_manager.update_price(bourse_key, value)
        
        # نمایش سایر شاخص‌ها
        other_bourse_prices = {k: v for k, v in prices.items() 
                              if k.startswith('bourse_') and k not in bourse_mapping}
        
        for bourse_key, value in other_bourse_prices.items():
            index_name = bourse_key.replace('bourse_', '').replace('_', ' ')
            change = self.data_manager.get_price_change(bourse_key, value)
            message += f"📊 {index_name}: {self.data_manager.format_price(value)} {change}\n"
            self.data_manager.update_price(bourse_key, value)
        
        message += "\n📊 تحلیل روند: "
        if any('🔺' in line for line in message.split('\n')):
            message += "صعودی 📈"
        elif any('🔻' in line for line in message.split('\n')):
            message += "نزولی 📉"
        else:
            message += "پایدار 📊"
        
        message += "\n\n📢 کانال ما: @Dollar_404_58"
        
        return message
    
    def format_symbols_message(self, prices: Dict[str, float]) -> str:
        """فرمت‌بندی پیام نمادهای بورس"""
        if not prices:
            return "❌ خطا در دریافت اطلاعات نمادهای بورس"
        
        message = f"📈 نمادهای برتر بورس ایران\n"
        message += f"⏰ {self.data_manager.get_current_time()}\n"
        message += "=" * 30 + "\n\n"
        
        # نمادهای بورس
        symbol_prices = {k: v for k, v in prices.items() if k.startswith('symbol_') and not k.endswith(('_change', '_percent', '_close', '_name'))}
        
        # نمایش 10 نماد برتر
        top_symbols = sorted(symbol_prices.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for symbol_key, price in top_symbols:
            symbol_name = symbol_key.replace('symbol_', '')
            
            # دریافت اطلاعات تغییرات
            change_key = f"{symbol_key}_change"
            percent_key = f"{symbol_key}_percent"
            name_key = f"{symbol_key}_name"
            
            change = self.data_manager.get_price_change(symbol_key, price)
            company_name = prices.get(name_key, symbol_name.upper())
            
            message += f"📊 {company_name} ({symbol_name.upper()}): {self.data_manager.format_price(price)} ریال {change}\n"
            self.data_manager.update_price(symbol_key, price)
        
        message += "\n📊 تحلیل روند: "
        if any('🔺' in line for line in message.split('\n')):
            message += "صعودی 📈"
        elif any('🔻' in line for line in message.split('\n')):
            message += "نزولی 📉"
        else:
            message += "پایدار 📊"
        
        message += "\n\n📢 کانال ما: @Dollar_404_58"
        
        return message
    
    def get_sticker_for_message(self, message_type: str) -> str:
        """دریافت استیکر مناسب برای نوع پیام"""
        sticker_map = {
            'gold_dollar': STICKERS.get('gold', ''),
            'currency': STICKERS.get('dollar', ''),
            'crypto': STICKERS.get('crypto', ''),
            'bourse': STICKERS.get('bourse', ''),
            'symbols': STICKERS.get('bourse', '')
        }
        return sticker_map.get(message_type, '') 