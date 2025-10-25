import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
TOKEN = "7807110576:AAFCdnH385CmHwCMBxWybsjkhxnKtOpoJMA"
ADMIN_CHAT_ID = "1235086577"
DB_NAME = "words_bot.db"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Обновление схемы базы данных
def update_db_schema():

    # Добавляет отсутствующие колонки в таблицу users
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(users)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        if 'repeat_words' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN repeat_words INTEGER DEFAULT 0")
            logging.info("Added repeat_words column to users table")
        
        conn.commit()
        conn.close()
        logging.info("Database schema updated successfully")
    except Exception as e:
        logging.error(f"Error updating database schema: {e}")
# Инициализация базы данных
def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                         (user_id INTEGER PRIMARY KEY, level TEXT, subscribe INTEGER, last_sent DATE, repeat_words INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_words
                         (user_id INTEGER, word TEXT, sent_date DATE)''')
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Database initialization error: {e}")

    try:
        if not words:
            return
            
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        today = datetime.now().date()
        
        for word_data in words:
            cursor.execute(
                "INSERT OR IGNORE INTO user_words (user_id, word, sent_date) VALUES (?, ?, ?)",
                (user_id, word_data["word"], today)
            )
        
        cursor.execute(
            "UPDATE users SET last_sent = ? WHERE user_id = ?",
            (today, user_id)
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error in save_sent_words: {e}")