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
        