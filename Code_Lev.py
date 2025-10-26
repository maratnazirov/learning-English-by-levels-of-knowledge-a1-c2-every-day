# Обработка выбора сброса прогресса
# Обработка выбора сброса прогресса
async def handle_reset_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        choice = update.message.text

        if choice == "🔄 Начать заново":
            success = await reset_user_progress(user_id)
            if success:
                # Получаем текущий уровень пользователя
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    level = result[0]
                    words = await send_words_to_user(user_id, level, context.bot)
                    save_sent_words(user_id, words)

                    await update.message.reply_text(
                        "🔄 Прогресс сброшен! Вы начинаете уровень заново.\n"
                        "Теперь вы будете получать слова с самого начала."
                    )
            else:
                await update.message.reply_text("❌ Не удалось сбросить прогресс. Попробуйте позже.")

        elif choice == "🚫 Завершить":
            await update.message.reply_text(
                "🎉 Отлично проделанная работа!\n"
                "Используйте /start чтобы выбрать другой уровень\n"
                "Или /reset чтобы начать этот уровень заново"
            )

    except Exception as e:
        logging.error(f"Error in handle_reset_choice: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")


# Команда /reset
async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id

        # Проверяем, есть ли пользователь в базе
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            await update.message.reply_text(
                "❌ У вас нет активного уровня.\n"
                "Используйте /start чтобы начать обучение."
            )
            return

        level = result[0]
        success = await reset_user_progress(user_id)

        if success:
            words = await send_words_to_user(user_id, level, context.bot)
            save_sent_words(user_id, words)

            await update.message.reply_text(
                f"🔄 Прогресс уровня {level} сброшен!\n"
                "Вы начинаете изучать слова заново с самого начала.\n "
                "Используйте /send для получения 10 слов сразу же"
            )
        else:
            await update.message.reply_text("❌ Не удалось сбросить прогресс. Попробуйте позже.")

    except Exception as e:
        logging.error(f"Error in reset command: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_text = (
            "🤖 English Words Bot - Помощь\n\n"
            "Доступные команды:\n\n"
            "/start - Выбрать уровень английского\n"
            "/send - Получить 10 слов сейчас\n"
            "/status - Проверить статус\n"
            "/reset - Начать уровень заново\n"
            "/stop - Остановить рассылку\n"
            "/help - Показать все команды\n\n"
            "📚 Бот присылает 10 новых слов каждый день в 9:00"
        )
        await update.message.reply_text(help_text)
    except Exception as e:
        logging.error(f"Error in help command: {e}")


# Ежедневная рассылка
async def send_daily_words(context: ContextTypes.DEFAULT_TYPE):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, level FROM users WHERE subscribe = 1")
        users = cursor.fetchall()

        for user_id, level in users:
            try:
                cursor.execute("SELECT last_sent FROM users WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()

                if result and result[0]:
                    last_sent = datetime.strptime(result[0], "%Y-%m-%d").date()
                    if datetime.now().date() <= last_sent:
                        continue

                words = await send_words_to_user(user_id, level, context.bot)
                if words is not None:  # Если не все слова изучены
                    save_sent_words(user_id, words)

            except Exception as e:
                logging.error(f"Error sending to user {user_id}: {e}")

        conn.close()
    except Exception as e:
        logging.error(f"Error in send_daily_words: {e}")
