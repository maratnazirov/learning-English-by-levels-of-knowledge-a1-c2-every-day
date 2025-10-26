#Сохранение слов в БД
def save_sent_words(user_id, words):
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

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [["A1", "A2", "B1", "B2", "C1", "C2"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            "Посмотреть команды /help .Выберите ваш уровень английского:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error in start command: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")

# Обработка выбора уровня
async def set_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    level = update.message.text

    if level not in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        await update.message.reply_text("Пожалуйста, выберите уровень из предложенных вариантов.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users (user_id, level, subscribe, last_sent, repeat_words) VALUES (?, ?, 1, ?, 0)",
            (user_id, level, datetime.now().date())
        )
        conn.commit()
        conn.close()

        words = await send_words_to_user(user_id, level, context.bot)
        save_sent_words(user_id, words)
        
        if words:
            await update.message.reply_text(
                f"✅ Отлично! Ваш уровень: {level}\n"
                "Теперь вы будете получать 10 новых слов каждый день в 9:00\n\n"
                "Команды:\n"
                "/send - получить слова сейчас\n"
                "/status - проверить статус\n"
                "/stop - остановить рассылку\n"
                "/reset - начать уровень заново\n"
                "/help - все команды"
            )
    except Exception as e:
        logging.error(f"Error in set_level: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")
