import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import httpx

from config import BOT_TOKEN, CHANNEL_ID, STICKERS
from data_manager import DataManager
from api_client import APIClient
from message_formatter import MessageFormatter

class TelegramBot:
    def __init__(self):
        # تنظیم bot با تنظیمات connection pool
        from telegram.request import HTTPXRequest
        
        # تنظیم connection pool برای جلوگیری از timeout
        request = HTTPXRequest(
            connection_pool_size=20,
            pool_timeout=30.0,
            read_timeout=30.0,
            write_timeout=30.0,
            connect_timeout=30.0
        )
        
        self.bot = Bot(token=BOT_TOKEN, request=request)
        
        self.data_manager = DataManager()
        self.api_client = APIClient()
        self.message_formatter = MessageFormatter(self.data_manager)
        self.scheduler = AsyncIOScheduler()
        
        # تنظیم لاگینگ
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
    
    async def send_message_with_sticker(self, message: str, sticker_id: str = None):
        """ارسال پیام همراه با استیکر"""
        try:
            # ارسال پیام
            await self.bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode='HTML'
            )
            
            # تاخیر کوتاه بین ارسال پیام و استیکر
            await asyncio.sleep(1)
            
            # ارسال استیکر اگر موجود باشد
            if sticker_id:
                await self.bot.send_sticker(
                    chat_id=CHANNEL_ID,
                    sticker=sticker_id
                )
            
            self.logger.info("پیام با موفقیت ارسال شد")
            
        except TelegramError as e:
            self.logger.error(f"خطا در ارسال پیام: {e}")
        except Exception as e:
            self.logger.error(f"خطای غیرمنتظره: {e}")
    
    async def send_gold_dollar_update(self):
        """ارسال به‌روزرسانی طلا و دلار (هر 1 دقیقه)"""
        try:
            self.logger.info("دریافت اطلاعات طلا و دلار...")
            
            # دریافت داده‌ها
            data = self.api_client.get_gold_currency_data()
            if not data:
                await self.send_message_with_sticker("❌ خطا در دریافت اطلاعات طلا و دلار")
                return
            
            # استخراج قیمت‌ها
            prices = self.api_client.extract_prices(data)
            if not prices:
                await self.send_message_with_sticker("❌ خطا در استخراج قیمت‌ها")
                return
            
            # فرمت‌بندی پیام
            message = self.message_formatter.format_gold_dollar_message(prices)
            sticker_id = self.message_formatter.get_sticker_for_message('gold_dollar')
            
            # ارسال پیام
            await self.send_message_with_sticker(message, sticker_id)
            
            # تاخیر کوتاه بعد از ارسال
            await asyncio.sleep(2)
            
        except Exception as e:
            self.logger.error(f"خطا در به‌روزرسانی طلا و دلار: {e}")
            await self.send_message_with_sticker("❌ خطا در به‌روزرسانی طلا و دلار")
    
    async def send_currency_update(self):
        """ارسال به‌روزرسانی ارزهای مختلف (هر 5 دقیقه)"""
        try:
            self.logger.info("=== شروع وظیفه ارزهای مختلف ===")
            self.logger.info("دریافت اطلاعات ارزهای مختلف...")
            
            # دریافت داده‌های ارز
            currency_data = self.api_client.get_currency_data()
            self.logger.info(f"داده‌های ارز دریافت شد: {currency_data is not None}")
            if currency_data:
                currency_prices = self.api_client.extract_prices(currency_data)
                self.logger.info(f"قیمت‌های ارز استخراج شد: {len(currency_prices)} مورد")
                if currency_prices:
                    message = self.message_formatter.format_currency_message(currency_prices)
                    sticker_id = self.message_formatter.get_sticker_for_message('currency')
                    await self.send_message_with_sticker(message, sticker_id)
                    # تاخیر بین ارسال پیام‌ها
                    await asyncio.sleep(3)
                else:
                    self.logger.warning("هیچ قیمت ارزی استخراج نشد")
            else:
                self.logger.warning("داده‌های ارز دریافت نشد")
            
            # دریافت داده‌های نمادهای بورس
            symbols_data = self.api_client.get_symbols_data()
            self.logger.info(f"داده‌های نمادهای بورس دریافت شد: {symbols_data is not None}")
            if symbols_data:
                symbols_prices = self.api_client.extract_prices(symbols_data)
                self.logger.info(f"قیمت‌های نمادهای بورس استخراج شد: {len(symbols_prices)} مورد")
                if symbols_prices:
                    message = self.message_formatter.format_symbols_message(symbols_prices)
                    sticker_id = self.message_formatter.get_sticker_for_message('symbols')
                    await self.send_message_with_sticker(message, sticker_id)
                else:
                    self.logger.warning("هیچ قیمت نماد بورسی استخراج نشد")
            else:
                self.logger.warning("داده‌های نمادهای بورس دریافت نشد")
            
        except Exception as e:
            self.logger.error(f"خطا در به‌روزرسانی ارزها: {e}")
            await self.send_message_with_sticker("❌ خطا در به‌روزرسانی ارزها")
    
    async def send_crypto_bourse_update(self):
        """ارسال به‌روزرسانی ارزهای دیجیتال و بورس (هر 10 دقیقه)"""
        try:
            self.logger.info("=== شروع وظیفه ارزهای دیجیتال و بورس ===")
            self.logger.info("دریافت اطلاعات ارزهای دیجیتال و بورس...")
            
            # دریافت داده‌های ارزهای دیجیتال
            crypto_data = self.api_client.get_crypto_data()
            self.logger.info(f"داده‌های ارزهای دیجیتال دریافت شد: {crypto_data is not None}")
            if crypto_data:
                crypto_prices = self.api_client.extract_prices(crypto_data)
                self.logger.info(f"قیمت‌های ارزهای دیجیتال استخراج شد: {len(crypto_prices)} مورد")
                if crypto_prices:
                    message = self.message_formatter.format_crypto_message(crypto_prices)
                    sticker_id = self.message_formatter.get_sticker_for_message('crypto')
                    await self.send_message_with_sticker(message, sticker_id)
                    # تاخیر بین ارسال پیام‌ها
                    await asyncio.sleep(3)
                else:
                    self.logger.warning("هیچ قیمت ارز دیجیتالی استخراج نشد")
            else:
                self.logger.warning("داده‌های ارزهای دیجیتال دریافت نشد")
            
            # دریافت داده‌های شاخص‌های بورس - شاخص اصلی
            bourse_data = self.api_client.get_bourse_data()
            self.logger.info(f"داده‌های شاخص‌های بورس دریافت شد: {bourse_data is not None}")
            if bourse_data:
                bourse_prices = self.api_client.extract_prices(bourse_data)
                self.logger.info(f"قیمت‌های شاخص‌های بورس استخراج شد: {len(bourse_prices)} مورد")
                if bourse_prices:
                    message = self.message_formatter.format_bourse_message(bourse_prices)
                    sticker_id = self.message_formatter.get_sticker_for_message('bourse')
                    await self.send_message_with_sticker(message, sticker_id)
                    # تاخیر بین ارسال پیام‌ها
                    await asyncio.sleep(3)
                else:
                    self.logger.warning("هیچ قیمت شاخص بورسی استخراج نشد")
            else:
                self.logger.warning("داده‌های شاخص‌های بورس دریافت نشد")
            
            # دریافت داده‌های فرابورس
            farabourse_data = self.api_client.get_farabourse_data()
            self.logger.info(f"داده‌های فرابورس دریافت شد: {farabourse_data is not None}")
            if farabourse_data:
                farabourse_prices = self.api_client.extract_prices(farabourse_data)
                self.logger.info(f"قیمت‌های فرابورس استخراج شد: {len(farabourse_prices)} مورد")
                if farabourse_prices:
                    message = self.message_formatter.format_bourse_message(farabourse_prices)
                    sticker_id = self.message_formatter.get_sticker_for_message('bourse')
                    await self.send_message_with_sticker(message, sticker_id)
                    # تاخیر بین ارسال پیام‌ها
                    await asyncio.sleep(3)
                else:
                    self.logger.warning("هیچ قیمت فرابورسی استخراج نشد")
            else:
                self.logger.warning("داده‌های فرابورس دریافت نشد")
            
            # دریافت شاخص‌های منتخب
            selected_indices_data = self.api_client.get_selected_indices_data()
            self.logger.info(f"داده‌های شاخص‌های منتخب دریافت شد: {selected_indices_data is not None}")
            if selected_indices_data:
                selected_prices = self.api_client.extract_prices(selected_indices_data)
                self.logger.info(f"قیمت‌های شاخص‌های منتخب استخراج شد: {len(selected_prices)} مورد")
                if selected_prices:
                    message = self.message_formatter.format_bourse_message(selected_prices)
                    sticker_id = self.message_formatter.get_sticker_for_message('bourse')
                    await self.send_message_with_sticker(message, sticker_id)
                else:
                    self.logger.warning("هیچ قیمت شاخص منتخبی استخراج نشد")
            else:
                self.logger.warning("داده‌های شاخص‌های منتخب دریافت نشد")
            
        except Exception as e:
            self.logger.error(f"خطا در به‌روزرسانی ارزهای دیجیتال و بورس: {e}")
            await self.send_message_with_sticker("❌ خطا در به‌روزرسانی ارزهای دیجیتال و بورس")
    
    def setup_scheduler(self):
        """تنظیم زمان‌بندی وظایف"""
        from config import GOLD_DOLLAR_INTERVAL, CURRENCY_INTERVAL, CRYPTO_BORSE_INTERVAL
        
        # طلا و دلار - هر 2 دقیقه
        self.scheduler.add_job(
            self.send_gold_dollar_update,
            IntervalTrigger(seconds=GOLD_DOLLAR_INTERVAL),
            id='gold_dollar_job',
            name='Gold and Dollar Update'
        )
        
        # ارزهای مختلف - هر 10 دقیقه
        self.scheduler.add_job(
            self.send_currency_update,
            IntervalTrigger(seconds=CURRENCY_INTERVAL),
            id='currency_job',
            name='Currency Update',
            misfire_grace_time=60  # اجازه تاخیر تا 60 ثانیه
        )
        
        # ارزهای دیجیتال و بورس - هر 15 دقیقه
        self.scheduler.add_job(
            self.send_crypto_bourse_update,
            IntervalTrigger(seconds=CRYPTO_BORSE_INTERVAL),
            id='crypto_bourse_job',
            name='Crypto and Bourse Update',
            misfire_grace_time=60  # اجازه تاخیر تا 60 ثانیه
        )
        
        # نمایش زمان‌بندی‌ها
        self.logger.info("زمان‌بندی وظایف تنظیم شد:")
        self.logger.info(f"- طلا و دلار: هر {GOLD_DOLLAR_INTERVAL//60} دقیقه")
        self.logger.info(f"- ارزهای مختلف: هر {CURRENCY_INTERVAL//60} دقیقه")
        self.logger.info(f"- ارزهای دیجیتال و بورس: هر {CRYPTO_BORSE_INTERVAL//60} دقیقه")
    
    async def start(self):
        """شروع ربات"""
        try:
            self.logger.info("شروع ربات تلگرام...")
            
            # تنظیم زمان‌بندی
            self.setup_scheduler()
            
            # شروع زمان‌بندی
            self.scheduler.start()
            
            # ارسال پیام شروع
            from config import GOLD_DOLLAR_INTERVAL, CURRENCY_INTERVAL, CRYPTO_BORSE_INTERVAL
            
            start_message = "🤖 ربات قیمت‌یاب شروع به کار کرد!\n\n"
            start_message += "📅 زمان‌بندی:\n"
            start_message += f"• طلا و دلار: هر {GOLD_DOLLAR_INTERVAL//60} دقیقه\n"
            start_message += f"• ارزهای مختلف: هر {CURRENCY_INTERVAL//60} دقیقه\n"
            start_message += f"• ارزهای دیجیتال و بورس: هر {CRYPTO_BORSE_INTERVAL//60} دقیقه\n\n"
            start_message += "⏰ " + self.data_manager.get_current_time()
            start_message += "\n\n📢 کانال ما: @Dollar_025"
            
            await self.send_message_with_sticker(start_message)
            
            self.logger.info("ربات با موفقیت شروع شد")
            
            # نگه داشتن ربات فعال
            while True:
                await asyncio.sleep(60)
                
        except Exception as e:
            self.logger.error(f"خطا در شروع ربات: {e}")
            raise
    
    def stop(self):
        """توقف ربات"""
        self.logger.info("توقف ربات...")
        self.scheduler.shutdown()
        self.logger.info("ربات متوقف شد") 