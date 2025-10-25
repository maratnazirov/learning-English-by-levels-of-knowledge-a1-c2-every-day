import logging
import sqlite3
import random
from datetime import datetime
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
# Обновление схемы базы данных(M)
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
# Инициализация базы данных(M)
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
# Функция сброса прогресса(M)
async def reset_user_progress(user_id: int):
    #Полностью сбрасывает прогресс пользователя
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Удаляем все отправленные слова пользователя
        cursor.execute("DELETE FROM user_words WHERE user_id = ?", (user_id,))
        
        # Сбрасываем флаг повторения
        cursor.execute("UPDATE users SET repeat_words = 0 WHERE user_id = ?", (user_id,))
        
        # Сбрасываем дату последней отправки
        cursor.execute("UPDATE users SET last_sent = NULL WHERE user_id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        logging.info(f"Progress reset for user {user_id}")
        return True
    except Exception as e:
        logging.error(f"Error resetting user progress: {e}")
        return False
# Функция передачи слов пользователям(2 способа: при reset и обычно)(M)
def get_words_for_user(user_id, level, count=10):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT repeat_words FROM users WHERE user_id = ?", (user_id,))
        repeat_result = cursor.fetchone()
        repeat_words = repeat_result[0] if repeat_result else 0
        
        cursor.execute("SELECT word FROM user_words WHERE user_id = ?", (user_id,))
        sent_words = [row[0] for row in cursor.fetchall()]
        
        # Получаем все доступные слова для уровня
        all_level_words = WORDS.get(level, [])
        
        if repeat_words:
            # В режиме повторения берем случайные слова из всех
            if len(all_level_words) <= count:
                selected_words = all_level_words
            else:
                selected_words = random.sample(all_level_words, count)
        else:
            # В обычном режиме берем только неотправленные слова
            available_words = [word for word in all_level_words if word["word"] not in sent_words]
            
            if len(available_words) == 0:
                conn.close()
                return None  # Все слова изучены
            
            if len(available_words) <= count:
                selected_words = available_words
            else:
                selected_words = random.sample(available_words, count)
        
        conn.close()
        return selected_words
    except Exception as e:
        logging.error(f"Error in get_words_for_user: {e}")
        return []
#Окончание слов в БД(M)
async def send_words_to_user(user_id, level, bot):
    try:
        words = get_words_for_user(user_id, level, 10)
        
        # Если слова закончились
        if words is None:
            keyboard = [["🔄 Начать заново", "🚫 Завершить"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            
            await bot.send_message(
                chat_id=user_id, 
                text=f"🎉 Поздравляем! Вы изучили все слова уровня {level}!\n\nХотите начать заново с этим уровнем?",
                reply_markup=reply_markup
            )
            return []
        
        if not words:
            await bot.send_message(
                chat_id=user_id,
                text="❌ Не удалось получить слова. Попробуйте позже."
            )
            return []
        
        message = f"📚 Слова уровня {level}:\n\n"
        for i, word_data in enumerate(words, 1):
            message += f"{i}. {word_data['word']} - {word_data['translation']}\n"
            if word_data.get('example'):
                message += f"   Пример: {word_data['example']}\n"
            message += "\n"
        
        await bot.send_message(chat_id=user_id, text=message)
        return words
    except Exception as e:
        logging.error(f"Error in send_words_to_user: {e}")
        return []
