async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET subscribe = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            "⏸️ Рассылка остановлена\n\n"
            "Используйте:\n"
            "/start - возобновить\n"
            "/send - получить слова сейчас\n"
            "/reset - начать уровень заново\n"
            "/help - все команды"
        )
    except Exception as e:
        logging.error(f"Error in stop command: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT level, subscribe FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            level, subscribe = result
            status_text = "активна" if subscribe else "остановлена"
            
            cursor.execute("SELECT COUNT(DISTINCT word) FROM user_words WHERE user_id = ?", (user_id,))
            learned_count = cursor.fetchone()[0]
            total_count = len(WORDS.get(level, []))
            
            conn.close()
            
            await update.message.reply_text(
                f"📊 Ваш статус:\n"
                f"• Уровень: {level}\n"
                f"• Рассылка: {status_text}\n"
                f"• Изучено слов: {learned_count}/{total_count}\n\n"
                f"Используйте:\n"
                f"/send - получить слова сейчас\n"
                f"/reset - начать уровень заново"
            )
        else:
            conn.close()
            await update.message.reply_text(
                "❌ Вы еще не выбрали уровень\n\n"
                "Используйте /start чтобы начать"
            )
    except Exception as e:
        logging.error(f"Error in status command: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")

async def send_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            level = result[0]
            words = await send_words_to_user(user_id, level, context.bot)
            if words is not None:  
                save_sent_words(user_id, words)
                
            if words:
                await update.message.reply_text("✅ Слова отправлены! Используйте /send для следующих слов")
        else:
            await update.message.reply_text(
                "❌ Сначала выберите уровень\n\n"
                "Используйте /start чтобы начать"
            )
    except Exception as e:
        logging.error(f"Error in send_now command: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")
