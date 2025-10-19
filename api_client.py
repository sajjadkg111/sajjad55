import requests
import time
from typing import Dict, List, Any, Optional
from config import API_KEY

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """انجام درخواست HTTP با مدیریت خطا"""
        try:
            response = self.session.get(url, params=params, timeout=30)  # افزایش timeout به 30 ثانیه
            response.raise_for_status()
            
            # بررسی محتوای پاسخ
            content = response.text.strip()
            if not content:
                print(f"پاسخ خالی از API: {url}")
                return None
            
            # بررسی اینکه آیا پاسخ JSON است
            if content.startswith('{') or content.startswith('['):
                return response.json()
            else:
                print(f"پاسخ غیر JSON از API: {content[:100]}...")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"خطا در درخواست API: {e}")
            return None
        except ValueError as e:
            print(f"خطا در پارس JSON: {e}")
            print(f"محتوای پاسخ: {response.text[:200]}...")
            return None
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")
            return None
    
    def get_gold_currency_data(self) -> Optional[Dict]:
        """دریافت داده‌های طلا و ارز از API اصلی"""
        url = "https://BrsApi.ir/Api/Market/Gold_Currency.php"
        params = {
            'key': API_KEY
        }
        
        return self.make_request(url, params)
    
    def get_currency_data(self) -> Optional[Dict]:
        """دریافت داده‌های ارزهای مختلف"""
        url = "https://BrsApi.ir/Api/Market/Gold_Currency.php"
        params = {
            'key': API_KEY
        }
        
        return self.make_request(url, params)
    
    def get_crypto_data(self) -> Optional[Dict]:
        """دریافت داده‌های ارزهای دیجیتال"""
        url = "https://BrsApi.ir/Api/Market/Gold_Currency.php"
        params = {
            'key': API_KEY
        }
        
        return self.make_request(url, params)
    
    def get_bourse_data(self) -> Optional[List]:
        """دریافت داده‌های شاخص‌های بورس"""
        url = "https://BrsApi.ir/Api/Tsetmc/Index.php"
        params = {
            'key': API_KEY,
            'type': 1  # شاخص بورس
        }
        
        return self.make_request(url, params)
    
    def get_farabourse_data(self) -> Optional[List]:
        """دریافت داده‌های شاخص فرابورس"""
        url = "https://BrsApi.ir/Api/Tsetmc/Index.php"
        params = {
            'key': API_KEY,
            'type': 2  # شاخص فرابورس
        }
        
        return self.make_request(url, params)
    
    def get_selected_indices_data(self) -> Optional[List]:
        """دریافت داده‌های شاخص‌های منتخب"""
        url = "https://BrsApi.ir/Api/Tsetmc/Index.php"
        params = {
            'key': API_KEY,
            'type': 3  # شاخص‌های منتخب
        }
        
        return self.make_request(url, params)
    
    def get_symbols_data(self) -> Optional[List]:
        """دریافت داده‌های نمادهای بورس"""
        url = "https://BrsApi.ir/Api/Tsetmc/AllSymbols.php"
        params = {
            'key': API_KEY,
            'type': 1  # سهام بورس و فرابورس + صندوق‌های ETF + حق‌تقدم
        }
        
        return self.make_request(url, params)
    
    def extract_prices(self, data: Any) -> Dict[str, float]:
        """استخراج قیمت‌ها از داده‌های API طبق ساختار واقعی"""
        prices = {}
        
        if not data:
            return prices
        
        try:
            # بررسی نوع داده دریافتی
            print(f"نوع داده دریافتی: {type(data)}")
            
            # پردازش ساختار واقعی API
            if isinstance(data, dict):
                # پردازش بخش طلا
                if 'gold' in data and isinstance(data['gold'], list):
                    for item in data['gold']:
                        if isinstance(item, dict):
                            symbol = item.get('symbol', '')
                            name = item.get('name', '')
                            price = item.get('price', 0)
                            change_value = item.get('change_value', 0)
                            change_percent = item.get('change_percent', 0)
                            unit = item.get('unit', '')
                            
                            if symbol and price:
                                try:
                                    price_value = float(price)
                                    # طلا و سکه
                                    if symbol == 'USD':
                                        prices['dollar'] = price_value
                                        prices['dollar_change'] = float(change_value)
                                        prices['dollar_change_percent'] = float(change_percent)
                                        prices['dollar_unit'] = unit
                                    elif symbol == 'IR_COIN_EMAMI':
                                        prices['gold_coin_emami'] = price_value
                                        prices['gold_coin_emami_change'] = float(change_value)
                                        prices['gold_coin_emami_change_percent'] = float(change_percent)
                                        prices['gold_coin_emami_unit'] = unit
                                    elif symbol == 'IR_GOLD_18K':
                                        prices['gold_gram_18'] = price_value
                                        prices['gold_gram_18_change'] = float(change_value)
                                        prices['gold_gram_18_change_percent'] = float(change_percent)
                                        prices['gold_gram_18_unit'] = unit
                                    elif symbol == 'IR_GOLD_24K':
                                        prices['gold_gram_24'] = price_value
                                        prices['gold_gram_24_change'] = float(change_value)
                                        prices['gold_gram_24_change_percent'] = float(change_percent)
                                        prices['gold_gram_24_unit'] = unit
                                    elif symbol == 'IR_GOLD_MELTED':
                                        prices['gold_melted'] = price_value
                                        prices['gold_melted_change'] = float(change_value)
                                        prices['gold_melted_change_percent'] = float(change_percent)
                                        prices['gold_melted_unit'] = unit
                                    elif symbol == 'XAUUSD':
                                        prices['gold_ounce'] = price_value
                                        prices['gold_ounce_change'] = float(change_value)
                                        prices['gold_ounce_change_percent'] = float(change_percent)
                                        prices['gold_ounce_unit'] = unit
                                    elif symbol == 'IR_COIN_1G':
                                        prices['gold_coin_1g'] = price_value
                                        prices['gold_coin_1g_change'] = float(change_value)
                                        prices['gold_coin_1g_change_percent'] = float(change_percent)
                                        prices['gold_coin_1g_unit'] = unit
                                    elif symbol == 'IR_COIN_QUARTER':
                                        prices['gold_coin_quarter'] = price_value
                                        prices['gold_coin_quarter_change'] = float(change_value)
                                        prices['gold_coin_quarter_change_percent'] = float(change_percent)
                                        prices['gold_coin_quarter_unit'] = unit
                                    elif symbol == 'IR_COIN_HALF':
                                        prices['gold_coin_half'] = price_value
                                        prices['gold_coin_half_change'] = float(change_value)
                                        prices['gold_coin_half_change_percent'] = float(change_percent)
                                        prices['gold_coin_half_unit'] = unit
                                    elif symbol == 'IR_COIN_BAHAR':
                                        prices['gold_coin_bahar'] = price_value
                                        prices['gold_coin_bahar_change'] = float(change_value)
                                        prices['gold_coin_bahar_change_percent'] = float(change_percent)
                                        prices['gold_coin_bahar_unit'] = unit
                                except (ValueError, TypeError):
                                    continue
                
                # پردازش بخش ارز
                if 'currency' in data and isinstance(data['currency'], list):
                    for item in data['currency']:
                        if isinstance(item, dict):
                            symbol = item.get('symbol', '')
                            name = item.get('name', '')
                            price = item.get('price', 0)
                            change_value = item.get('change_value', 0)
                            change_percent = item.get('change_percent', 0)
                            unit = item.get('unit', '')
                            
                            if symbol and price:
                                try:
                                    price_value = float(price)
                                    # ارزهای اصلی
                                    if symbol == 'USD':
                                        prices['dollar'] = price_value
                                        prices['dollar_change'] = float(change_value)
                                        prices['dollar_change_percent'] = float(change_percent)
                                        prices['dollar_unit'] = unit
                                    elif symbol == 'EUR':
                                        prices['currency_euro'] = price_value
                                        prices['currency_euro_change'] = float(change_value)
                                        prices['currency_euro_change_percent'] = float(change_percent)
                                        prices['currency_euro_unit'] = unit
                                    elif symbol == 'GBP':
                                        prices['currency_pound'] = price_value
                                        prices['currency_pound_change'] = float(change_value)
                                        prices['currency_pound_change_percent'] = float(change_percent)
                                        prices['currency_pound_unit'] = unit
                                    elif symbol == 'JPY':
                                        prices['currency_yen'] = price_value
                                        prices['currency_yen_change'] = float(change_value)
                                        prices['currency_yen_change_percent'] = float(change_percent)
                                        prices['currency_yen_unit'] = unit
                                    elif symbol == 'AED':
                                        prices['currency_dirham'] = price_value
                                        prices['currency_dirham_change'] = float(change_value)
                                        prices['currency_dirham_change_percent'] = float(change_percent)
                                        prices['currency_dirham_unit'] = unit
                                    elif symbol == 'USDT_IRT':
                                        prices['usdt_toman'] = price_value
                                        prices['usdt_toman_change'] = float(change_value)
                                        prices['usdt_toman_change_percent'] = float(change_percent)
                                        prices['usdt_toman_unit'] = unit
                                    # ارزهای دیگر
                                    elif symbol == 'KWD':
                                        prices['currency_kuwait_dinar'] = price_value
                                        prices['currency_kuwait_dinar_change'] = float(change_value)
                                        prices['currency_kuwait_dinar_change_percent'] = float(change_percent)
                                        prices['currency_kuwait_dinar_unit'] = unit
                                    elif symbol == 'AUD':
                                        prices['currency_australian_dollar'] = price_value
                                        prices['currency_australian_dollar_change'] = float(change_value)
                                        prices['currency_australian_dollar_change_percent'] = float(change_percent)
                                        prices['currency_australian_dollar_unit'] = unit
                                    elif symbol == 'CAD':
                                        prices['currency_canadian_dollar'] = price_value
                                        prices['currency_canadian_dollar_change'] = float(change_value)
                                        prices['currency_canadian_dollar_change_percent'] = float(change_percent)
                                        prices['currency_canadian_dollar_unit'] = unit
                                    elif symbol == 'CNY':
                                        prices['currency_chinese_yuan'] = price_value
                                        prices['currency_chinese_yuan_change'] = float(change_value)
                                        prices['currency_chinese_yuan_change_percent'] = float(change_percent)
                                        prices['currency_chinese_yuan_unit'] = unit
                                    elif symbol == 'TRY':
                                        prices['currency_turkish_lira'] = price_value
                                        prices['currency_turkish_lira_change'] = float(change_value)
                                        prices['currency_turkish_lira_change_percent'] = float(change_percent)
                                        prices['currency_turkish_lira_unit'] = unit
                                    elif symbol == 'SAR':
                                        prices['currency_saudi_riyal'] = price_value
                                        prices['currency_saudi_riyal_change'] = float(change_value)
                                        prices['currency_saudi_riyal_change_percent'] = float(change_percent)
                                        prices['currency_saudi_riyal_unit'] = unit
                                    elif symbol == 'CHF':
                                        prices['currency_swiss_franc'] = price_value
                                        prices['currency_swiss_franc_change'] = float(change_value)
                                        prices['currency_swiss_franc_change_percent'] = float(change_percent)
                                        prices['currency_swiss_franc_unit'] = unit
                                    elif symbol == 'INR':
                                        prices['currency_indian_rupee'] = price_value
                                        prices['currency_indian_rupee_change'] = float(change_value)
                                        prices['currency_indian_rupee_change_percent'] = float(change_percent)
                                        prices['currency_indian_rupee_unit'] = unit
                                    elif symbol == 'PKR':
                                        prices['currency_pakistani_rupee'] = price_value
                                        prices['currency_pakistani_rupee_change'] = float(change_value)
                                        prices['currency_pakistani_rupee_change_percent'] = float(change_percent)
                                        prices['currency_pakistani_rupee_unit'] = unit
                                    elif symbol == 'IQD':
                                        prices['currency_iraqi_dinar'] = price_value
                                        prices['currency_iraqi_dinar_change'] = float(change_value)
                                        prices['currency_iraqi_dinar_change_percent'] = float(change_percent)
                                        prices['currency_iraqi_dinar_unit'] = unit
                                    elif symbol == 'SYP':
                                        prices['currency_syrian_lira'] = price_value
                                        prices['currency_syrian_lira_change'] = float(change_value)
                                        prices['currency_syrian_lira_change_percent'] = float(change_percent)
                                        prices['currency_syrian_lira_unit'] = unit
                                    elif symbol == 'SEK':
                                        prices['currency_swedish_krona'] = price_value
                                        prices['currency_swedish_krona_change'] = float(change_value)
                                        prices['currency_swedish_krona_change_percent'] = float(change_percent)
                                        prices['currency_swedish_krona_unit'] = unit
                                    elif symbol == 'QAR':
                                        prices['currency_qatari_riyal'] = price_value
                                        prices['currency_qatari_riyal_change'] = float(change_value)
                                        prices['currency_qatari_riyal_change_percent'] = float(change_percent)
                                        prices['currency_qatari_riyal_unit'] = unit
                                    elif symbol == 'OMR':
                                        prices['currency_omani_rial'] = price_value
                                        prices['currency_omani_rial_change'] = float(change_value)
                                        prices['currency_omani_rial_change_percent'] = float(change_percent)
                                        prices['currency_omani_rial_unit'] = unit
                                    elif symbol == 'BHD':
                                        prices['currency_bahraini_dinar'] = price_value
                                        prices['currency_bahraini_dinar_change'] = float(change_value)
                                        prices['currency_bahraini_dinar_change_percent'] = float(change_percent)
                                        prices['currency_bahraini_dinar_unit'] = unit
                                    elif symbol == 'AFN':
                                        prices['currency_afghan_afghani'] = price_value
                                        prices['currency_afghan_afghani_change'] = float(change_value)
                                        prices['currency_afghan_afghani_change_percent'] = float(change_percent)
                                        prices['currency_afghan_afghani_unit'] = unit
                                    elif symbol == 'MYR':
                                        prices['currency_malaysian_ringgit'] = price_value
                                        prices['currency_malaysian_ringgit_change'] = float(change_value)
                                        prices['currency_malaysian_ringgit_change_percent'] = float(change_percent)
                                        prices['currency_malaysian_ringgit_unit'] = unit
                                    elif symbol == 'THB':
                                        prices['currency_thai_baht'] = price_value
                                        prices['currency_thai_baht_change'] = float(change_value)
                                        prices['currency_thai_baht_change_percent'] = float(change_percent)
                                        prices['currency_thai_baht_unit'] = unit
                                    elif symbol == 'RUB':
                                        prices['currency_russian_ruble'] = price_value
                                        prices['currency_russian_ruble_change'] = float(change_value)
                                        prices['currency_russian_ruble_change_percent'] = float(change_percent)
                                        prices['currency_russian_ruble_unit'] = unit
                                    elif symbol == 'AZN':
                                        prices['currency_azerbaijani_manat'] = price_value
                                        prices['currency_azerbaijani_manat_change'] = float(change_value)
                                        prices['currency_azerbaijani_manat_change_percent'] = float(change_percent)
                                        prices['currency_azerbaijani_manat_unit'] = unit
                                    elif symbol == 'AMD':
                                        prices['currency_armenian_dram'] = price_value
                                        prices['currency_armenian_dram_change'] = float(change_value)
                                        prices['currency_armenian_dram_change_percent'] = float(change_percent)
                                        prices['currency_armenian_dram_unit'] = unit
                                    elif symbol == 'GEL':
                                        prices['currency_georgian_lari'] = price_value
                                        prices['currency_georgian_lari_change'] = float(change_value)
                                        prices['currency_georgian_lari_change_percent'] = float(change_percent)
                                        prices['currency_georgian_lari_unit'] = unit
                                    else:
                                        prices[f"currency_{symbol.lower()}"] = price_value
                                        prices[f"currency_{symbol.lower()}_change"] = float(change_value)
                                        prices[f"currency_{symbol.lower()}_change_percent"] = float(change_percent)
                                        prices[f"currency_{symbol.lower()}_unit"] = unit
                                except (ValueError, TypeError):
                                    continue
                
                # پردازش بخش ارزهای دیجیتال
                if 'cryptocurrency' in data and isinstance(data['cryptocurrency'], list):
                    for item in data['cryptocurrency']:
                        if isinstance(item, dict):
                            symbol = item.get('symbol', '')
                            name = item.get('name', '')
                            price = item.get('price', 0)
                            change_value = item.get('change_value', 0)
                            change_percent = item.get('change_percent', 0)
                            unit = item.get('unit', '')
                            
                            if symbol and price:
                                try:
                                    price_value = float(price)
                                    # ارزهای دیجیتال اصلی
                                    if symbol == 'BTC':
                                        prices['crypto_bitcoin'] = price_value
                                        prices['crypto_bitcoin_change'] = float(change_value)
                                        prices['crypto_bitcoin_change_percent'] = float(change_percent)
                                        prices['crypto_bitcoin_unit'] = unit
                                    elif symbol == 'ETH':
                                        prices['crypto_ethereum'] = price_value
                                        prices['crypto_ethereum_change'] = float(change_value)
                                        prices['crypto_ethereum_change_percent'] = float(change_percent)
                                        prices['crypto_ethereum_unit'] = unit
                                    elif symbol == 'USDT':
                                        prices['crypto_tether'] = price_value
                                        prices['crypto_tether_change'] = float(change_value)
                                        prices['crypto_tether_change_percent'] = float(change_percent)
                                        prices['crypto_tether_unit'] = unit
                                    elif symbol == 'XRP':
                                        prices['crypto_xrp'] = price_value
                                        prices['crypto_xrp_change'] = float(change_value)
                                        prices['crypto_xrp_change_percent'] = float(change_percent)
                                        prices['crypto_xrp_unit'] = unit
                                    elif symbol == 'BNB':
                                        prices['crypto_bnb'] = price_value
                                        prices['crypto_bnb_change'] = float(change_value)
                                        prices['crypto_bnb_change_percent'] = float(change_percent)
                                        prices['crypto_bnb_unit'] = unit
                                    elif symbol == 'SOL':
                                        prices['crypto_solana'] = price_value
                                        prices['crypto_solana_change'] = float(change_value)
                                        prices['crypto_solana_change_percent'] = float(change_percent)
                                        prices['crypto_solana_unit'] = unit
                                    elif symbol == 'USDC':
                                        prices['crypto_usd_coin'] = price_value
                                        prices['crypto_usd_coin_change'] = float(change_value)
                                        prices['crypto_usd_coin_change_percent'] = float(change_percent)
                                        prices['crypto_usd_coin_unit'] = unit
                                    elif symbol == 'TRX':
                                        prices['crypto_tron'] = price_value
                                        prices['crypto_tron_change'] = float(change_value)
                                        prices['crypto_tron_change_percent'] = float(change_percent)
                                        prices['crypto_tron_unit'] = unit
                                    elif symbol == 'DOGE':
                                        prices['crypto_dogecoin'] = price_value
                                        prices['crypto_dogecoin_change'] = float(change_value)
                                        prices['crypto_dogecoin_change_percent'] = float(change_percent)
                                        prices['crypto_dogecoin_unit'] = unit
                                    elif symbol == 'ADA':
                                        prices['crypto_cardano'] = price_value
                                        prices['crypto_cardano_change'] = float(change_value)
                                        prices['crypto_cardano_change_percent'] = float(change_percent)
                                        prices['crypto_cardano_unit'] = unit
                                    elif symbol == 'LINK':
                                        prices['crypto_chainlink'] = price_value
                                        prices['crypto_chainlink_change'] = float(change_value)
                                        prices['crypto_chainlink_change_percent'] = float(change_percent)
                                        prices['crypto_chainlink_unit'] = unit
                                    elif symbol == 'XLM':
                                        prices['crypto_stellar'] = price_value
                                        prices['crypto_stellar_change'] = float(change_value)
                                        prices['crypto_stellar_change_percent'] = float(change_percent)
                                        prices['crypto_stellar_unit'] = unit
                                    elif symbol == 'AVAX':
                                        prices['crypto_avalanche'] = price_value
                                        prices['crypto_avalanche_change'] = float(change_value)
                                        prices['crypto_avalanche_change_percent'] = float(change_percent)
                                        prices['crypto_avalanche_unit'] = unit
                                    elif symbol == 'SHIB':
                                        prices['crypto_shiba_inu'] = price_value
                                        prices['crypto_shiba_inu_change'] = float(change_value)
                                        prices['crypto_shiba_inu_change_percent'] = float(change_percent)
                                        prices['crypto_shiba_inu_unit'] = unit
                                    elif symbol == 'LTC':
                                        prices['crypto_litecoin'] = price_value
                                        prices['crypto_litecoin_change'] = float(change_value)
                                        prices['crypto_litecoin_change_percent'] = float(change_percent)
                                        prices['crypto_litecoin_unit'] = unit
                                    elif symbol == 'DOT':
                                        prices['crypto_polkadot'] = price_value
                                        prices['crypto_polkadot_change'] = float(change_value)
                                        prices['crypto_polkadot_change_percent'] = float(change_percent)
                                        prices['crypto_polkadot_unit'] = unit
                                    elif symbol == 'UNI':
                                        prices['crypto_uniswap'] = price_value
                                        prices['crypto_uniswap_change'] = float(change_value)
                                        prices['crypto_uniswap_change_percent'] = float(change_percent)
                                        prices['crypto_uniswap_unit'] = unit
                                    elif symbol == 'ATOM':
                                        prices['crypto_cosmos'] = price_value
                                        prices['crypto_cosmos_change'] = float(change_value)
                                        prices['crypto_cosmos_change_percent'] = float(change_percent)
                                        prices['crypto_cosmos_unit'] = unit
                                    elif symbol == 'FIL':
                                        prices['crypto_filecoin'] = price_value
                                        prices['crypto_filecoin_change'] = float(change_value)
                                        prices['crypto_filecoin_change_percent'] = float(change_percent)
                                        prices['crypto_filecoin_unit'] = unit
                                    else:
                                        prices[f"crypto_{symbol.lower()}"] = price_value
                                        prices[f"crypto_{symbol.lower()}_change"] = float(change_value)
                                        prices[f"crypto_{symbol.lower()}_change_percent"] = float(change_percent)
                                        prices[f"crypto_{symbol.lower()}_unit"] = unit
                                except (ValueError, TypeError):
                                    continue
            
            # پردازش داده‌های بورس (اگر جداگانه ارسال شوند)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # برای شاخص‌های بورس
                        index = item.get('index', 0)
                        name = item.get('name', '')
                        index_change = item.get('index_change', 0)
                        index_change_percent = item.get('index_change_percent', 0)
                        state = item.get('state', '')
                        date = item.get('date', '')
                        time = item.get('time', '')
                        
                        if index and name:
                            try:
                                index_value = float(index)
                                change_value = float(index_change) if index_change else 0
                                change_percent = float(index_change_percent) if index_change_percent else 0
                                
                                # شاخص‌های اصلی
                                if 'شاخص کل' in name:
                                    prices['bourse_total'] = index_value
                                    prices['bourse_total_change'] = change_value
                                    prices['bourse_total_percent'] = change_percent
                                    prices['bourse_total_state'] = state
                                    prices['bourse_total_date'] = date
                                    prices['bourse_total_time'] = time
                                elif 'شاخص هم‌وزن' in name:
                                    prices['bourse_equal_weight'] = index_value
                                    prices['bourse_equal_weight_change'] = change_value
                                    prices['bourse_equal_weight_percent'] = change_percent
                                    prices['bourse_equal_weight_state'] = state
                                    prices['bourse_equal_weight_date'] = date
                                    prices['bourse_equal_weight_time'] = time
                                elif 'شاخص فرابورس' in name:
                                    prices['bourse_farabourse'] = index_value
                                    prices['bourse_farabourse_change'] = change_value
                                    prices['bourse_farabourse_percent'] = change_percent
                                    prices['bourse_farabourse_state'] = state
                                    prices['bourse_farabourse_date'] = date
                                    prices['bourse_farabourse_time'] = time
                                elif 'شاخص قیمت' in name:
                                    prices['bourse_price'] = index_value
                                    prices['bourse_price_change'] = change_value
                                    prices['bourse_price_percent'] = change_percent
                                    prices['bourse_price_state'] = state
                                    prices['bourse_price_date'] = date
                                    prices['bourse_price_time'] = time
                                elif 'شاخص آزاد شناور' in name:
                                    prices['bourse_free_float'] = index_value
                                    prices['bourse_free_float_change'] = change_value
                                    prices['bourse_free_float_percent'] = change_percent
                                    prices['bourse_free_float_state'] = state
                                    prices['bourse_free_float_date'] = date
                                    prices['bourse_free_float_time'] = time
                                elif 'شاخص بازار اول' in name:
                                    prices['bourse_market1'] = index_value
                                    prices['bourse_market1_change'] = change_value
                                    prices['bourse_market1_percent'] = change_percent
                                    prices['bourse_market1_state'] = state
                                    prices['bourse_market1_date'] = date
                                    prices['bourse_market1_time'] = time
                                elif 'شاخص بازار دوم' in name:
                                    prices['bourse_market2'] = index_value
                                    prices['bourse_market2_change'] = change_value
                                    prices['bourse_market2_percent'] = change_percent
                                    prices['bourse_market2_state'] = state
                                    prices['bourse_market2_date'] = date
                                    prices['bourse_market2_time'] = time
                                else:
                                    # سایر شاخص‌ها
                                    safe_name = name.replace(' ', '_').replace('/', '_').replace('-', '_')
                                    prices[f"bourse_{safe_name}"] = index_value
                                    prices[f"bourse_{safe_name}_change"] = change_value
                                    prices[f"bourse_{safe_name}_percent"] = change_percent
                                    prices[f"bourse_{safe_name}_state"] = state
                                    prices[f"bourse_{safe_name}_date"] = date
                                    prices[f"bourse_{safe_name}_time"] = time
                            except (ValueError, TypeError):
                                continue
                        
                        # برای نمادهای بورس
                        l18 = item.get('l18', '')  # نماد
                        l30 = item.get('l30', '')  # نام شرکت
                        pl = item.get('pl', 0)     # آخرین قیمت
                        pc = item.get('pc', 0)     # قیمت پایانی
                        plc = item.get('plc', 0)   # تغییر آخرین قیمت
                        plp = item.get('plp', 0)   # درصد تغییر آخرین قیمت
                        pcc = item.get('pcc', 0)   # تغییر قیمت پایانی
                        pcp = item.get('pcp', 0)   # درصد تغییر قیمت پایانی
                        tno = item.get('tno', 0)   # تعداد معاملات
                        tvol = item.get('tvol', 0) # حجم معاملات
                        tval = item.get('tval', 0) # ارزش معاملات
                        mv = item.get('mv', 0)     # ارزش بازار
                        time = item.get('time', '') # زمان آخرین اطلاعات
                        
                        if l18 and pl:
                            try:
                                price_value = float(pl)
                                change_value = float(plc)
                                change_percent = float(plp)
                                close_price = float(pc)
                                close_change = float(pcc)
                                close_percent = float(pcp)
                                volume = float(tvol)
                                value = float(tval)
                                market_value = float(mv)
                                trade_count = float(tno)
                                
                                # ذخیره اطلاعات نماد
                                prices[f"symbol_{l18}"] = price_value
                                prices[f"symbol_{l18}_change"] = change_value
                                prices[f"symbol_{l18}_percent"] = change_percent
                                prices[f"symbol_{l18}_close"] = close_price
                                prices[f"symbol_{l18}_close_change"] = close_change
                                prices[f"symbol_{l18}_close_percent"] = close_percent
                                prices[f"symbol_{l18}_name"] = l30
                                prices[f"symbol_{l18}_volume"] = volume
                                prices[f"symbol_{l18}_value"] = value
                                prices[f"symbol_{l18}_market_value"] = market_value
                                prices[f"symbol_{l18}_trade_count"] = trade_count
                                prices[f"symbol_{l18}_time"] = time
                                
                            except (ValueError, TypeError):
                                continue
        
        except Exception as e:
            print(f"خطا در استخراج قیمت‌ها: {e}")
            print(f"داده دریافتی: {data}")
        
        return prices
    
    def get_all_data(self) -> Dict[str, Any]:
        """دریافت تمام داده‌ها در یک درخواست"""
        all_data = {}
        
        # دریافت طلا و ارز
        gold_currency = self.get_gold_currency_data()
        if gold_currency:
            all_data.update(self.extract_prices(gold_currency))
        
        # دریافت ارزهای مختلف
        currency_data = self.get_currency_data()
        if currency_data:
            all_data.update(self.extract_prices(currency_data))
        
        # دریافت ارزهای دیجیتال
        crypto_data = self.get_crypto_data()
        if crypto_data:
            all_data.update(self.extract_prices(crypto_data))
        
        # دریافت داده‌های بورس - شاخص اصلی
        bourse_data = self.get_bourse_data()
        if bourse_data:
            all_data.update(self.extract_prices(bourse_data))
        
        # دریافت داده‌های فرابورس
        farabourse_data = self.get_farabourse_data()
        if farabourse_data:
            all_data.update(self.extract_prices(farabourse_data))
        
        # دریافت شاخص‌های منتخب
        selected_indices_data = self.get_selected_indices_data()
        if selected_indices_data:
            all_data.update(self.extract_prices(selected_indices_data))
        
        # دریافت نمادهای بورس
        symbols_data = self.get_symbols_data()
        if symbols_data:
            all_data.update(self.extract_prices(symbols_data))
        
        return all_data 