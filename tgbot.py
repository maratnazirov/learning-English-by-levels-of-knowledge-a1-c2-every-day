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

# Слова для всех уровней
WORDS = {
    "A1": [
        {"word": "hello", "translation": "привет", "example": "Hello, how are you?"},
        {"word": "goodbye", "translation": "пока", "example": "Goodbye, see you tomorrow!"},
        {"word": "thank you", "translation": "спасибо", "example": "Thank you for your help."},
        {"word": "please", "translation": "пожалуйста", "example": "Can I have some water, please?"},
        {"word": "sorry", "translation": "извините", "example": "I'm sorry for being late."},
        {"word": "yes", "translation": "да", "example": "Yes, I understand."},
        {"word": "no", "translation": "нет", "example": "No, thank you."},
        {"word": "apple", "translation": "яблоко", "example": "I eat an apple every day."},
        {"word": "book", "translation": "книга", "example": "I'm reading an interesting book."},
        {"word": "house", "translation": "дом", "example": "We live in a big house."},
        {"word": "water", "translation": "вода", "example": "Please drink more water."},
        {"word": "friend", "translation": "друг", "example": "She is my best friend."},
        {"word": "family", "translation": "семья", "example": "I have a big family."},
        {"word": "school", "translation": "школа", "example": "My children go to school."},
        {"word": "work", "translation": "работа", "example": "I go to work at 9 am."},
        {"word": "time", "translation": "время", "example": "What time is it?"},
        {"word": "day", "translation": "день", "example": "Have a nice day!"},
        {"word": "night", "translation": "ночь", "example": "I sleep at night."},
        {"word": "week", "translation": "неделя", "example": "See you next week!"},
        {"word": "month", "translation": "месяц", "example": "February is a short month."},
        {"word": "year", "translation": "год", "example": "I was born in 1990."},
        {"word": "man", "translation": "мужчина", "example": "That man is my father."},
        {"word": "woman", "translation": "женщина", "example": "The woman is reading a book."},
        {"word": "child", "translation": "ребенок", "example": "The children are playing outside."},
        {"word": "city", "translation": "город", "example": "I live in a big city."},
        {"word": "country", "translation": "страна", "example": "France is a beautiful country."},
        {"word": "food", "translation": "еда", "example": "Italian food is delicious."},
        {"word": "money", "translation": "деньги", "example": "I need to save money."},
        {"word": "car", "translation": "машина", "example": "We drive a red car."},
        {"word": "home", "translation": "дом", "example": "I go home after work."},
        {"word": "bed", "translation": "кровать", "example": "I go to bed at 11 pm."},
        {"word": "table", "translation": "стол", "example": "We eat at the kitchen table."},
        {"word": "chair", "translation": "стул", "example": "Please sit on this chair."},
        {"word": "computer", "translation": "компьютер", "example": "I work on my computer."},
        {"word": "phone", "translation": "телефон", "example": "My phone is ringing."},
        {"word": "door", "translation": "дверь", "example": "Close the door, please."},
        {"word": "window", "translation": "окно", "example": "Open the window for fresh air."},
        {"word": "pen", "translation": "ручка", "example": "Can I borrow your pen?"},
        {"word": "paper", "translation": "бумага", "example": "I need paper to write on."},
        {"word": "bag", "translation": "сумка", "example": "This is my school bag."},
        {"word": "shoe", "translation": "обувь", "example": "I bought new shoes."},
        {"word": "clothes", "translation": "одежда", "example": "I need to wash my clothes."},
        {"word": "cat", "translation": "кот", "example": "My cat is sleeping."},
        {"word": "dog", "translation": "собака", "example": "The dog is barking."},
        {"word": "sun", "translation": "солнце", "example": "The sun is shining today."},
        {"word": "rain", "translation": "дождь", "example": "It's raining outside."},
        {"word": "hot", "translation": "горячий", "example": "The tea is too hot."},
        {"word": "cold", "translation": "холодный", "example": "The water is cold."},
        {"word": "big", "translation": "большой", "example": "They have a big house."},
        {"word": "small", "translation": "маленький", "example": "This is a small room."},
        {"word": "good", "translation": "хороший", "example": "This is a good book."},
        {"word": "bad", "translation": "плохой", "example": "The weather is bad today."},
        {"word": "happy", "translation": "счастливый", "example": "I am happy to see you."},
        {"word": "sad", "translation": "грустный", "example": "She looks sad today."},
        {"word": "new", "translation": "новый", "example": "I have a new phone."},
        {"word": "old", "translation": "старый", "example": "This is an old house."},
        {"word": "young", "translation": "молодой", "example": "He is a young man."},
        {"word": "beautiful", "translation": "красивый", "example": "She is beautiful."},
        {"word": "easy", "translation": "легкий", "example": "This test is easy."},
        {"word": "difficult", "translation": "трудный", "example": "Math is difficult for me."},
        {"word": "fast", "translation": "быстрый", "example": "This car is very fast."},
        {"word": "slow", "translation": "медленный", "example": "The internet is slow today."},
        {"word": "high", "translation": "высокий", "example": "This mountain is high."},
        {"word": "low", "translation": "низкий", "example": "The price is low."},
        {"word": "long", "translation": "длинный", "example": "Her hair is long."},
        {"word": "short", "translation": "короткий", "example": "It was a short meeting."},
        {"word": "clean", "translation": "чистый", "example": "The room is clean."},
        {"word": "dirty", "translation": "грязный", "example": "My hands are dirty."},
        {"word": "light", "translation": "легкий", "example": "This bag is light."},
        {"word": "heavy", "translation": "тяжелый", "example": "The box is heavy."},
        {"word": "full", "translation": "полный", "example": "The glass is full."},
        {"word": "empty", "translation": "пустой", "example": "The room is empty."},
        {"word": "right", "translation": "правый", "example": "Turn right at the corner."},
        {"word": "left", "translation": "левый", "example": "My left hand hurts."},
        {"word": "red", "translation": "красный", "example": "I have a red car."},
        {"word": "blue", "translation": "синий", "example": "The sky is blue."},
        {"word": "green", "translation": "зеленый", "example": "The grass is green."},
        {"word": "yellow", "translation": "желтый", "example": "Bananas are yellow."},
        {"word": "black", "translation": "черный", "example": "I have black hair."},
        {"word": "white", "translation": "белый", "example": "Snow is white."},
        {"word": "brown", "translation": "коричневый", "example": "Chocolate is brown."},
        {"word": "one", "translation": "один", "example": "I have one brother."},
        {"word": "two", "translation": "два", "example": "I have two sisters."},
        {"word": "three", "translation": "три", "example": "There are three apples."},
        {"word": "four", "translation": "четыре", "example": "Four seasons in a year."},
        {"word": "five", "translation": "пять", "example": "I work five days a week."},
        {"word": "six", "translation": "шесть", "example": "A cube has six sides."},
        {"word": "seven", "translation": "семь", "example": "There are seven days in a week."},
        {"word": "eight", "translation": "восемь", "example": "An octopus has eight legs."},
        {"word": "nine", "translation": "девять", "example": "A cat has nine lives."},
        {"word": "ten", "translation": "десять", "example": "I have ten fingers."},
        {"word": "eat", "translation": "есть", "example": "I eat breakfast at 8 am."},
        {"word": "drink", "translation": "пить", "example": "I drink coffee every morning."},
        {"word": "sleep", "translation": "спать", "example": "I sleep 8 hours every night."},
        {"word": "work", "translation": "работать", "example": "I work in an office."},
        {"word": "study", "translation": "учиться", "example": "I study English every day."},
        {"word": "read", "translation": "читать", "example": "I read books in my free time."},
        {"word": "write", "translation": "писать", "example": "I write emails every day."},
        {"word": "speak", "translation": "говорить", "example": "I speak English and Russian."},
        {"word": "listen", "translation": "слушать", "example": "I listen to music."},
        {"word": "watch", "translation": "смотреть", "example": "I watch TV in the evening."}
    ],

    "A2": [
        {"word": "journey", "translation": "путешествие", "example": "The journey was long but exciting."},
        {"word": "environment", "translation": "окружающая среда", "example": "We must protect the environment."},
        {"word": "decision", "translation": "решение", "example": "It was a difficult decision."},
        {"word": "experience", "translation": "опыт", "example": "She has teaching experience."},
        {"word": "information", "translation": "информация", "example": "I need more information."},
        {"word": "problem", "translation": "проблема", "example": "Let me solve this problem."},
        {"word": "question", "translation": "вопрос", "example": "Do you have any questions?"},
        {"word": "reason", "translation": "причина", "example": "What's the reason for your visit?"},
        {"word": "result", "translation": "результат", "example": "The test results are good."},
        {"word": "system", "translation": "система", "example": "The education system needs improvement."},
        {"word": "moment", "translation": "момент", "example": "Wait a moment, please."},
        {"word": "opportunity", "translation": "возможность", "example": "This is a great opportunity."},
        {"word": "development", "translation": "развитие", "example": "Child development is important."},
        {"word": "knowledge", "translation": "знание", "example": "He has good knowledge of history."},
        {"word": "situation", "translation": "ситуация", "example": "The situation is under control."},
        {"word": "community", "translation": "сообщество", "example": "Our community is very friendly."},
        {"word": "government", "translation": "правительство", "example": "The government announced new laws."},
        {"word": "company", "translation": "компания", "example": "She works for a large company."},
        {"word": "business", "translation": "бизнес", "example": "He started his own business."},
        {"word": "market", "translation": "рынок", "example": "We buy vegetables at the market."},
        {"word": "price", "translation": "цена", "example": "The price of this car is high."},
        {"word": "service", "translation": "услуга", "example": "The hotel service was excellent."},
        {"word": "product", "translation": "продукт", "example": "This is a new product."},
        {"word": "quality", "translation": "качество", "example": "We offer high quality products."},
        {"word": "popular", "translation": "популярный", "example": "This restaurant is very popular."},
        {"word": "possible", "translation": "возможный", "example": "Is it possible to finish today?"},
        {"word": "special", "translation": "особенный", "example": "Today is a special day."},
        {"word": "traditional", "translation": "традиционный", "example": "We cook traditional food."},
        {"word": "understand", "translation": "понимать", "example": "I understand your problem."},
        {"word": "remember", "translation": "помнить", "example": "I remember that day."},
        {"word": "forget", "translation": "забывать", "example": "Don't forget your keys."},
        {"word": "believe", "translation": "верить", "example": "I believe in you."},
        {"word": "decide", "translation": "решать", "example": "You need to decide now."},
        {"word": "discover", "translation": "открывать", "example": "Scientists discover new things."},
        {"word": "explain", "translation": "объяснять", "example": "Can you explain this to me?"},
        {"word": "suggest", "translation": "предлагать", "example": "I suggest we go tomorrow."},
        {"word": "discuss", "translation": "обсуждать", "example": "Let's discuss this later."},
        {"word": "agree", "translation": "соглашаться", "example": "I agree with you."},
        {"word": "disagree", "translation": "не соглашаться", "example": "I disagree with that idea."},
        {"word": "promise", "translation": "обещать", "example": "I promise to help you."},
        {"word": "refuse", "translation": "отказываться", "example": "He refused to answer."},
        {"word": "offer", "translation": "предлагать", "example": "They offered me a job."},
        {"word": "receive", "translation": "получать", "example": "I received your email."},
        {"word": "accept", "translation": "принимать", "example": "I accept your apology."},
        {"word": "complete", "translation": "завершать", "example": "I need to complete this work."},
        {"word": "continue", "translation": "продолжать", "example": "Please continue your story."},
        {"word": "arrive", "translation": "прибывать", "example": "We arrive at 5 pm."},
        {"word": "leave", "translation": "уходить", "example": "I leave work at 6 pm."},
        {"word": "begin", "translation": "начинать", "example": "Let's begin the lesson."},
        {"word": "end", "translation": "заканчивать", "example": "The movie ends at 10 pm."},
        {"word": "change", "translation": "менять", "example": "I need to change my plans."},
        {"word": "help", "translation": "помогать", "example": "Can you help me?"},
        {"word": "learn", "translation": "учить", "example": "I learn new words every day."},
        {"word": "teach", "translation": "учить", "example": "She teaches English."},
        {"word": "meet", "translation": "встречать", "example": "I'll meet you at the station."},
        {"word": "wait", "translation": "ждать", "example": "Wait for me, please."},
        {"word": "stay", "translation": "оставаться", "example": "I stay at home today."},
        {"word": "travel", "translation": "путешествовать", "example": "I love to travel."},
        {"word": "visit", "translation": "посещать", "example": "I visit my parents every weekend."},
        {"word": "buy", "translation": "покупать", "example": "I need to buy some food."},
        {"word": "sell", "translation": "продавать", "example": "They sell fresh bread here."},
        {"word": "pay", "translation": "платить", "example": "I pay by credit card."},
        {"word": "cost", "translation": "стоить", "example": "How much does it cost?"},
        {"word": "spend", "translation": "тратить", "example": "I spend too much money."},
        {"word": "save", "translation": "экономить", "example": "I save money for my vacation."},
        {"word": "earn", "translation": "зарабатывать", "example": "He earns a good salary."},
        {"word": "build", "translation": "строить", "example": "They build new houses."},
        {"word": "break", "translation": "ломать", "example": "Don't break the glass."},
        {"word": "fix", "translation": "чинить", "example": "I need to fix my computer."},
        {"word": "clean", "translation": "чистить", "example": "I clean my room every week."},
        {"word": "wash", "translation": "мыть", "example": "Wash your hands before eating."},
        {"word": "cook", "translation": "готовить", "example": "I cook dinner every evening."},
        {"word": "feel", "translation": "чувствовать", "example": "I feel happy today."},
        {"word": "look", "translation": "смотреть", "example": "Look at this picture."},
        {"word": "hear", "translation": "слышать", "example": "I hear music from next door."},
        {"word": "smell", "translation": "нюхать", "example": "I smell something burning."},
        {"word": "taste", "translation": "пробовать", "example": "Taste this soup, it's delicious."},
        {"word": "touch", "translation": "трогать", "example": "Don't touch the hot stove."},
        {"word": "hold", "translation": "держать", "example": "Hold my hand, please."},
        {"word": "carry", "translation": "нести", "example": "Can you carry this bag?"},
        {"word": "bring", "translation": "приносить", "example": "Bring your passport."},
        {"word": "show", "translation": "показывать", "example": "Show me your work."},
        {"word": "send", "translation": "отправлять", "example": "I'll send you an email."},
        {"word": "open", "translation": "открывать", "example": "Open the window, please."},
        {"word": "close", "translation": "закрывать", "example": "Close the door behind you."},
        {"word": "start", "translation": "начинать", "example": "Let's start the meeting."},
        {"word": "stop", "translation": "останавливать", "example": "Stop talking and listen."},
        {"word": "finish", "translation": "заканчивать", "example": "I finish work at 5 pm."},
        {"word": "try", "translation": "пытаться", "example": "Try to do your best."},
        {"word": "hope", "translation": "надеяться", "example": "I hope you feel better."},
        {"word": "expect", "translation": "ожидать", "example": "I expect to finish soon."},
        {"word": "plan", "translation": "планировать", "example": "I plan to travel next year."},
        {"word": "prepare", "translation": "готовить", "example": "Prepare for the exam."},
        {"word": "practice", "translation": "практиковать", "example": "Practice English every day."},
        {"word": "enjoy", "translation": "наслаждаться", "example": "I enjoy reading books."},
        {"word": "prefer", "translation": "предпочитать", "example": "I prefer tea to coffee."},
        {"word": "weather", "translation": "погода", "example": "The weather is nice today."},
        {"word": "temperature", "translation": "температура", "example": "The temperature is 20 degrees."}
    ],

    "B1": [
        {"word": "achievement", "translation": "достижение", "example": "Winning the competition was a great achievement."},
        {"word": "advantage", "translation": "преимущество", "example": "Speaking English is an advantage in business."},
        {"word": "challenge", "translation": "вызов", "example": "This job presents new challenges."},
        {"word": "communication", "translation": "общение", "example": "Good communication is key to success."},
        {"word": "competition", "translation": "конкуренция", "example": "There is strong competition in the market."},
        {"word": "confidence", "translation": "уверенность", "example": "She speaks with great confidence."},
        {"word": "consequence", "translation": "последствие", "example": "Think about the consequences of your actions."},
        {"word": "consumer", "translation": "потребитель", "example": "Consumer demand is increasing."},
        {"word": "contribution", "translation": "вклад", "example": "He made a significant contribution to science."},
        {"word": "conversation", "translation": "разговор", "example": "We had an interesting conversation."},
        {"word": "culture", "translation": "культура", "example": "I'm interested in Japanese culture."},
        {"word": "customer", "translation": "клиент", "example": "The customer is always right."},
        {"word": "education", "translation": "образование", "example": "Education is important for everyone."},
        {"word": "election", "translation": "выборы", "example": "The election results were surprising."},
        {"word": "energy", "translation": "энергия", "example": "Solar energy is becoming popular."},
        {"word": "equipment", "translation": "оборудование", "example": "We need new office equipment."},
        {"word": "evidence", "translation": "доказательство", "example": "There is no evidence to support this."},
        {"word": "expert", "translation": "эксперт", "example": "He is an expert in his field."},
        {"word": "facility", "translation": "удобство", "example": "The hotel has excellent facilities."},
        {"word": "freedom", "translation": "свобода", "example": "Freedom of speech is important."},
        {"word": "growth", "translation": "рост", "example": "The company shows strong growth."},
        {"word": "income", "translation": "доход", "example": "His monthly income is stable."},
        {"word": "influence", "translation": "влияние", "example": "Parents have great influence on children."},
        {"word": "management", "translation": "управление", "example": "Good management is essential."},
        {"word": "organization", "translation": "организация", "example": "She works for a non-profit organization."},
        {"word": "performance", "translation": "производительность", "example": "His performance at work is excellent."},
        {"word": "population", "translation": "население", "example": "The population of the city is growing."},
        {"word": "pressure", "translation": "давление", "example": "I work well under pressure."},
        {"word": "professional", "translation": "профессионал", "example": "He is a true professional."},
        {"word": "responsibility", "translation": "ответственность", "example": "This is a big responsibility."},
        {"word": "security", "translation": "безопасность", "example": "Airport security is very strict."},
        {"word": "solution", "translation": "решение", "example": "We need to find a solution."},
        {"word": "strategy", "translation": "стратегия", "example": "We need a new marketing strategy."},
        {"word": "success", "translation": "успех", "example": "Hard work leads to success."},
        {"word": "technology", "translation": "технология", "example": "Modern technology changes quickly."},
        {"word": "treatment", "translation": "лечение", "example": "He is receiving medical treatment."},
        {"word": "variety", "translation": "разнообразие", "example": "We offer a variety of products."},
        {"word": "welfare", "translation": "благосостояние", "example": "Animal welfare is important."},
        {"word": "appropriate", "translation": "подходящий", "example": "This is not an appropriate time."},
        {"word": "available", "translation": "доступный", "example": "Is this book available?"},
        {"word": "complex", "translation": "сложный", "example": "This is a complex problem."},
        {"word": "effective", "translation": "эффективный", "example": "This medicine is very effective."},
        {"word": "essential", "translation": "необходимый", "example": "Water is essential for life."},
        {"word": "financial", "translation": "финансовый", "example": "We have financial difficulties."},
        {"word": "independent", "translation": "независимый", "example": "She is very independent."},
        {"word": "positive", "translation": "позитивный", "example": "Try to stay positive."},
        {"word": "potential", "translation": "потенциальный", "example": "He has great potential."},
        {"word": "significant", "translation": "значительный", "example": "This is a significant improvement."},
        {"word": "similar", "translation": "похожий", "example": "Our opinions are similar."},
        {"word": "sufficient", "translation": "достаточный", "example": "We have sufficient resources."},
        {"word": "achieve", "translation": "достигать", "example": "I want to achieve my goals."},
        {"word": "acquire", "translation": "приобретать", "example": "She acquired new skills."},
        {"word": "adapt", "translation": "адаптировать", "example": "We need to adapt to changes."},
        {"word": "adjust", "translation": "настраивать", "example": "Adjust the temperature, please."},
        {"word": "admire", "translation": "восхищаться", "example": "I admire your courage."},
        {"word": "admit", "translation": "признавать", "example": "He admitted his mistake."},
        {"word": "advise", "translation": "советовать", "example": "I advise you to study more."},
        {"word": "affect", "translation": "влиять", "example": "Weather affects my mood."},
        {"word": "allow", "translation": "позволять", "example": "Smoking is not allowed here."},
        {"word": "announce", "translation": "объявлять", "example": "They announced the results."},
        {"word": "appreciate", "translation": "ценить", "example": "I appreciate your help."},
        {"word": "approve", "translation": "одобрять", "example": "My boss approved my plan."},
        {"word": "argue", "translation": "спорить", "example": "They argue about politics."},
        {"word": "arrange", "translation": "организовывать", "example": "I'll arrange a meeting."},
        {"word": "assume", "translation": "предполагать", "example": "I assume you're busy."},
        {"word": "assure", "translation": "уверять", "example": "I assure you it's safe."},
        {"word": "attach", "translation": "прикреплять", "example": "Attach the file to the email."},
        {"word": "attend", "translation": "посещать", "example": "I attend meetings regularly."},
        {"word": "avoid", "translation": "избегать", "example": "Avoid making the same mistake."},
        {"word": "bother", "translation": "беспокоить", "example": "Don't bother me now."},
        {"word": "cancel", "translation": "отменять", "example": "They canceled the flight."},
        {"word": "claim", "translation": "утверждать", "example": "He claims to be innocent."},
        {"word": "collect", "translation": "собирать", "example": "I collect stamps."},
        {"word": "compare", "translation": "сравнивать", "example": "Compare these two products."},
        {"word": "complain", "translation": "жаловаться", "example": "Customers often complain."},
        {"word": "concern", "translation": "беспокоить", "example": "This concerns all of us."},
        {"word": "confirm", "translation": "подтверждать", "example": "Please confirm your reservation."},
        {"word": "connect", "translation": "соединять", "example": "Connect the cables properly."},
        {"word": "consider", "translation": "рассматривать", "example": "Consider all options."},
        {"word": "consist", "translation": "состоять", "example": "Water consists of hydrogen and oxygen."},
        {"word": "contact", "translation": "контактировать", "example": "Contact me by email."},
        {"word": "contain", "translation": "содержать", "example": "This box contains books."},
        {"word": "convince", "translation": "убеждать", "example": "I convinced him to come."},
        {"word": "create", "translation": "создавать", "example": "Artists create beautiful works."},
        {"word": "deal", "translation": "иметь дело", "example": "I deal with customers daily."},
        {"word": "declare", "translation": "объявлять", "example": "They declared independence."},
        {"word": "decrease", "translation": "уменьшать", "example": "Prices decreased last month."},
        {"word": "deliver", "translation": "доставлять", "example": "We deliver worldwide."},
        {"word": "demand", "translation": "требовать", "example": "Customers demand quality."},
        {"word": "deny", "translation": "отрицать", "example": "He denied the accusation."},
        {"word": "depend", "translation": "зависеть", "example": "It depends on the weather."},
        {"word": "describe", "translation": "описывать", "example": "Describe what you see."},
        {"word": "deserve", "translation": "заслуживать", "example": "You deserve a reward."},
        {"word": "destroy", "translation": "уничтожать", "example": "The fire destroyed the building."},
        {"word": "determine", "translation": "определять", "example": "We need to determine the cause."},
        {"word": "develop", "translation": "развивать", "example": "Children develop quickly."},
        {"word": "differ", "translation": "отличаться", "example": "Opinions differ on this matter."}
    ],

    "B2": [
        {"word": "comprehensive", "translation": "всеобъемлющий", "example": "We need a comprehensive plan."},
        {"word": "sophisticated", "translation": "искушенный", "example": "This is a sophisticated device."},
        {"word": "controversial", "translation": "спорный", "example": "This is a controversial topic."},
        {"word": "conventional", "translation": "традиционный", "example": "This is a conventional approach."},
        {"word": "fundamental", "translation": "фундаментальный", "example": "This is a fundamental principle."},
        {"word": "innovative", "translation": "инновационный", "example": "They developed an innovative solution."},
        {"word": "profound", "translation": "глубокий", "example": "This book had a profound effect on me."},
        {"word": "radical", "translation": "радикальный", "example": "We need radical changes."},
        {"word": "reliable", "translation": "надежный", "example": "This car is very reliable."},
        {"word": "remarkable", "translation": "замечательный", "example": "She made remarkable progress."},
        {"word": "substantial", "translation": "существенный", "example": "We need substantial evidence."},
        {"word": "ambiguous", "translation": "двусмысленный", "example": "His answer was ambiguous."},
        {"word": "coherent", "translation": "связный", "example": "Her argument was coherent."},
        {"word": "compatible", "translation": "совместимый", "example": "This software is compatible with Windows."},
        {"word": "complementary", "translation": "дополнительный", "example": "These skills are complementary."},
        {"word": "consecutive", "translation": "последовательный", "example": "It rained for three consecutive days."},
        {"word": "consistent", "translation": "последовательный", "example": "His work is consistently good."},
        {"word": "crucial", "translation": "решающий", "example": "This meeting is crucial."},
        {"word": "deliberate", "translation": "преднамеренный", "example": "It was a deliberate mistake."},
        {"word": "discretionary", "translation": "дискреционный", "example": "This is discretionary spending."},
        {"word": "dynamic", "translation": "динамичный", "example": "The market is very dynamic."},
        {"word": "elaborate", "translation": "тщательно разработанный", "example": "They made elaborate preparations."},
        {"word": "explicit", "translation": "явный", "example": "He gave explicit instructions."},
        {"word": "feasible", "translation": "осуществимый", "example": "This plan is not feasible."},
        {"word": "flexible", "translation": "гибкий", "example": "We need a flexible approach."},
        {"word": "implicit", "translation": "подразумеваемый", "example": "There was implicit agreement."},
        {"word": "inevitable", "translation": "неизбежный", "example": "Change is inevitable."},
        {"word": "inherent", "translation": "присущий", "example": "There are inherent risks."},
        {"word": "intricate", "translation": "сложный", "example": "This is an intricate design."},
        {"word": "legitimate", "translation": "законный", "example": "This is a legitimate concern."},
        {"word": "mutual", "translation": "взаимный", "example": "We have mutual respect."},
        {"word": "neutral", "translation": "нейтральный", "example": "Stay neutral in this conflict."},
        {"word": "notable", "translation": "примечательный", "example": "This is a notable achievement."},
        {"word": "objective", "translation": "объективный", "example": "We need objective analysis."},
        {"word": "optimal", "translation": "оптимальный", "example": "This is the optimal solution."},
        {"word": "plausible", "translation": "правдоподобный", "example": "This explanation seems plausible."},
        {"word": "pragmatic", "translation": "прагматичный", "example": "We need a pragmatic approach."},
        {"word": "preliminary", "translation": "предварительный", "example": "These are preliminary results."},
        {"word": "proactive", "translation": "проактивный", "example": "Be proactive in solving problems."},
        {"word": "rational", "translation": "рациональный", "example": "Make rational decisions."},
        {"word": "relevant", "translation": "релевантный", "example": "This information is not relevant."},
        {"word": "rigorous", "translation": "строгий", "example": "We need rigorous testing."},
        {"word": "spontaneous", "translation": "спонтанный", "example": "It was a spontaneous decision."},
        {"word": "strategic", "translation": "стратегический", "example": "This is a strategic location."},
        {"word": "subjective", "translation": "субъективный", "example": "This is a subjective opinion."},
        {"word": "systematic", "translation": "систематический", "example": "We need systematic approach."},
        {"word": "tentative", "translation": "предварительный", "example": "This is a tentative plan."},
        {"word": "thorough", "translation": "тщательный", "example": "Do a thorough investigation."},
        {"word": "versatile", "translation": "универсальный", "example": "This tool is very versatile."},
        {"word": "accommodate", "translation": "размещать", "example": "The hotel can accommodate 200 guests."},
        {"word": "accumulate", "translation": "накапливать", "example": "Dust accumulates quickly."},
        {"word": "acknowledge", "translation": "признавать", "example": "I acknowledge your point."},
        {"word": "advocate", "translation": "защитник", "example": "She is an advocate for human rights."},
        {"word": "alleviate", "translation": "облегчать", "example": "This medicine alleviates pain."},
        {"word": "allocate", "translation": "распределять", "example": "We need to allocate resources."},
        {"word": "anticipate", "translation": "предвидеть", "example": "We anticipate problems."},
        {"word": "appraise", "translation": "оценивать", "example": "Appraise the situation carefully."},
        {"word": "ascertain", "translation": "устанавливать", "example": "We need to ascertain the facts."},
        {"word": "aspire", "translation": "стремиться", "example": "I aspire to be successful."},
        {"word": "assert", "translation": "утверждать", "example": "He asserted his authority."},
        {"word": "assess", "translation": "оценивать", "example": "Assess the damage first."},
        {"word": "attribute", "translation": "приписывать", "example": "Success is attributed to hard work."},
        {"word": "augment", "translation": "увеличивать", "example": "We need to augment our staff."},
        {"word": "authorize", "translation": "уполномочивать", "example": "I am authorized to sign."},
        {"word": "clarify", "translation": "прояснять", "example": "Let me clarify this point."},
        {"word": "collaborate", "translation": "сотрудничать", "example": "We collaborate with partners."},
        {"word": "compensate", "translation": "компенсировать", "example": "We will compensate for the loss."},
        {"word": "comprehend", "translation": "понимать", "example": "I cannot comprehend this."},
        {"word": "conceive", "translation": "задумывать", "example": "It's hard to conceive such beauty."},
        {"word": "conclude", "translation": "заключать", "example": "I conclude that we should wait."},
        {"word": "confer", "translation": "совещаться", "example": "We need to confer about this."},
        {"word": "confine", "translation": "ограничивать", "example": "Confine your remarks to the topic."},
        {"word": "conform", "translation": "соответствовать", "example": "We must conform to regulations."},
        {"word": "consolidate", "translation": "консолидировать", "example": "Consolidate your gains."},
        {"word": "constitute", "translation": "составлять", "example": "These elements constitute the whole."},
        {"word": "contradict", "translation": "противоречить", "example": "Your story contradicts his."},
        {"word": "convene", "translation": "созывать", "example": "We will convene a meeting."},
        {"word": "convey", "translation": "передавать", "example": "Words cannot convey my feelings."},
        {"word": "corroborate", "translation": "подтверждать", "example": "Evidence corroborates his story."},
        {"word": "deduce", "translation": "выводить", "example": "From this we can deduce the answer."},
        {"word": "deem", "translation": "считать", "example": "I deem it necessary."},
        {"word": "defer", "translation": "откладывать", "example": "Let's defer the decision."},
        {"word": "demonstrate", "translation": "демонстрировать", "example": "Demonstrate how it works."},
        {"word": "derive", "translation": "получать", "example": "We derive pleasure from music."},
        {"word": "designate", "translation": "назначать", "example": "Designate a team leader."},
        {"word": "deviate", "translation": "отклоняться", "example": "Don't deviate from the plan."},
        {"word": "differentiate", "translation": "различать", "example": "Differentiate between facts and opinions."},
        {"word": "discern", "translation": "различать", "example": "It's hard to discern the truth."},
        {"word": "disclose", "translation": "раскрывать", "example": "I cannot disclose that information."},
        {"word": "discrete", "translation": "отдельный", "example": "These are discrete elements."},
        {"word": "discriminate", "translation": "различать", "example": "Learn to discriminate between them."},
        {"word": "dispose", "translation": "располагать", "example": "How do you dispose of waste?"},
        {"word": "disseminate", "translation": "распространять", "example": "Disseminate the information."},
        {"word": "distinguish", "translation": "отличать", "example": "Can you distinguish them?"},
        {"word": "divert", "translation": "отвлекать", "example": "Divert attention from the problem."},
        {"word": "elicit", "translation": "вызывать", "example": "His words elicited laughter."},
        {"word": "embark", "translation": "начинать", "example": "We embark on a new project."},
        {"word": "endorse", "translation": "поддерживать", "example": "I endorse this proposal."},
        {"word": "enhance", "translation": "улучшать", "example": "This enhances our chances."},
        {"word": "envisage", "translation": "представлять", "example": "I envisage a bright future."},
        {"word": "equate", "translation": "приравнивать", "example": "Don't equate money with happiness."},
        {"word": "erode", "translation": "разрушать", "example": "Water erodes rocks over time."},
        {"word": "establish", "translation": "устанавливать", "example": "We need to establish rules."},
        {"word": "evaluate", "translation": "оценивать", "example": "Evaluate the results carefully."},
        {"word": "exclude", "translation": "исключать", "example": "We cannot exclude any possibility."},
        {"word": "facilitate", "translation": "облегчать", "example": "This facilitates learning."}
    ],

    "C1": [
        {"word": "meticulous", "translation": "дотошный", "example": "She is meticulous in her work."},
        {"word": "ubiquitous", "translation": "вездесущий", "example": "Smartphones are ubiquitous nowadays."},
        {"word": "paradigm", "translation": "парадигма", "example": "This represents a paradigm shift."},
        {"word": "ambivalent", "translation": "двойственный", "example": "I feel ambivalent about this decision."},
        {"word": "anomaly", "translation": "аномалия", "example": "This result is an anomaly."},
        {"word": "arduous", "translation": "трудный", "example": "It was an arduous journey."},
        {"word": "benevolent", "translation": "благожелательный", "example": "He is a benevolent leader."},
        {"word": "candid", "translation": "откровенный", "example": "Please be candid with me."},
        {"word": "capricious", "translation": "капризный", "example": "The weather is capricious."},
        {"word": "cogent", "translation": "убедительный", "example": "She presented a cogent argument."},
        {"word": "convoluted", "translation": "запутанный", "example": "The plot was convoluted."},
        {"word": "dichotomy", "translation": "дихотомия", "example": "There is a dichotomy between theory and practice."},
        {"word": "diligent", "translation": "усердный", "example": "She is a diligent student."},
        {"word": "discerning", "translation": "проницательный", "example": "He has discerning taste."},
        {"word": "ebullient", "translation": "восторженный", "example": "She has an ebullient personality."},
        {"word": "egregious", "translation": "вопиющий", "example": "This is an egregious error."},
        {"word": "eloquent", "translation": "красноречивый", "example": "He gave an eloquent speech."},
        {"word": "empirical", "translation": "эмпирический", "example": "We need empirical evidence."},
        {"word": "enigmatic", "translation": "загадочный", "example": "She has an enigmatic smile."},
        {"word": "ephemeral", "translation": "мимолетный", "example": "Fame is often ephemeral."},
        {"word": "equitable", "translation": "справедливый", "example": "We need an equitable solution."},
        {"word": "erudite", "translation": "эрудированный", "example": "He is an erudite scholar."},
        {"word": "exemplary", "translation": "образцовый", "example": "Her behavior was exemplary."},
        {"word": "exhaustive", "translation": "исчерпывающий", "example": "They conducted exhaustive research."},
        {"word": "expedient", "translation": "целесообразный", "example": "This is the most expedient solution."},
        {"word": "fastidious", "translation": "привередливый", "example": "He is fastidious about details."},
        {"word": "gregarious", "translation": "общительный", "example": "She has a gregarious nature."},
        {"word": "idiosyncratic", "translation": "своеобразный", "example": "His style is idiosyncratic."},
        {"word": "impeccable", "translation": "безупречный", "example": "Her English is impeccable."},
        {"word": "imperative", "translation": "императивный", "example": "It is imperative that we act now."},
        {"word": "incontrovertible", "translation": "неопровержимый", "example": "The evidence is incontrovertible."},
        {"word": "indefatigable", "translation": "неутомимый", "example": "She is an indefatigable worker."},
        {"word": "indomitable", "translation": "неукротимый", "example": "He has an indomitable spirit."},
        {"word": "inextricable", "translation": "неразрывный", "example": "These issues are inextricably linked."},
        {"word": "ingenious", "translation": "гениальный", "example": "This is an ingenious solution."},
        {"word": "inscrutable", "translation": "непостижимый", "example": "His motives are inscrutable."},
        {"word": "judicious", "translation": "благоразумный", "example": "She made a judicious decision."},
        {"word": "lucid", "translation": "ясный", "example": "He gave a lucid explanation."},
        {"word": "magnanimous", "translation": "великодушный", "example": "It was a magnanimous gesture."},
        {"word": "munificent", "translation": "щедрый", "example": "They received munificent support."},
        {"word": "nefarious", "translation": "зловещий", "example": "They have nefarious intentions."},
        {"word": "obfuscate", "translation": "затемнять", "example": "Don't obfuscate the issue."},
        {"word": "ostensible", "translation": "мнимый", "example": "The ostensible reason was different."},
        {"word": "perfunctory", "translation": "поверхностный", "example": "He gave a perfunctory response."},
        {"word": "perspicacious", "translation": "проницательный", "example": "She is a perspicacious observer."},
        {"word": "prolific", "translation": "плодовитый", "example": "He is a prolific writer."},
        {"word": "prudent", "translation": "благоразумный", "example": "It would be prudent to wait."},
        {"word": "punctilious", "translation": "педантичный", "example": "He is punctilious about rules."},
        {"word": "resilient", "translation": "устойчивый", "example": "Children are remarkably resilient."},
        {"word": "abstruse", "translation": "заумный", "example": "The concept was too abstruse for me."},
        {"word": "acumen", "translation": "проницательность", "example": "She has remarkable business acumen."},
        {"word": "adumbrate", "translation": "предвещать", "example": "The report adumbrated future changes."},
        {"word": "alacrity", "translation": "готовность", "example": "He accepted with alacrity."},
        {"word": "anachronism", "translation": "анахронизм", "example": "This law is an anachronism."},
        {"word": "antithesis", "translation": "антитеза", "example": "This is the antithesis of democracy."},
        {"word": "apotheosis", "translation": "апофеоз", "example": "This work is the apotheosis of his career."},
        {"word": "asseverate", "translation": "утверждать", "example": "I must asseverate my innocence."},
        {"word": "assiduous", "translation": "усердный", "example": "She is assiduous in her studies."},
        {"word": "bellicose", "translation": "воинственный", "example": "His bellicose rhetoric worried everyone."},
        {"word": "bowdlerize", "translation": "цензурировать", "example": "The film was bowdlerized for television."},
        {"word": "charlatan", "translation": "шарлатан", "example": "He was exposed as a charlatan."},
        {"word": "circumlocution", "translation": "обиняк", "example": "Stop using circumlocution and be direct."},
        {"word": "demagogue", "translation": "демагог", "example": "He was a dangerous demagogue."},
        {"word": "dilatory", "translation": "медлительный", "example": "Stop being so dilatory."},
        {"word": "disingenuous", "translation": "неискренний", "example": "His apology seemed disingenuous."},
        {"word": "equanimity", "translation": "хладнокровие", "example": "She faced the crisis with equanimity."},
        {"word": "eschew", "translation": "избегать", "example": "He eschews modern technology."},
        {"word": "exacerbate", "translation": "обострять", "example": "This will only exacerbate the problem."},
        {"word": "exigent", "translation": "срочный", "example": "We face exigent circumstances."},
        {"word": "extrapolate", "translation": "экстраполировать", "example": "We can extrapolate from these results."},
        {"word": "facetious", "translation": "шутливый", "example": "Don't be facetious about serious matters."},
        {"word": "garrulous", "translation": "болтливый", "example": "He became garrulous after drinking."},
        {"word": "iconoclast", "translation": "иконоборец", "example": "He was an iconoclast in his field."},
        {"word": "idiosyncrasy", "translation": "особенность", "example": "We all have our idiosyncrasies."},
        {"word": "impecunious", "translation": "бедный", "example": "The impecunious student struggled."},
        {"word": "impervious", "translation": "непроницаемый", "example": "He is impervious to criticism."},
        {"word": "inchoate", "translation": "зарождающийся", "example": "These are inchoate ideas."},
        {"word": "inimical", "translation": "враждебный", "example": "This environment is inimical to growth."},
        {"word": "intransigent", "translation": "непримиримый", "example": "He remains intransigent on this issue."},
        {"word": "inveterate", "translation": "закоренелый", "example": "He is an inveterate liar."},
        {"word": "juxtaposition", "translation": "сопоставление", "example": "The juxtaposition was striking."},
        {"word": "laconic", "translation": "лаконичный", "example": "He gave a laconic reply."},
        {"word": "magnate", "translation": "магнат", "example": "He is a media magnate."},
        {"word": "mendacious", "translation": "лживый", "example": "The statement was mendacious."},
        {"word": "obdurate", "translation": "упрямый", "example": "She remained obdurate in her refusal."},
        {"word": "obsequious", "translation": "раболепный", "example": "His obsequious behavior was annoying."},
        {"word": "parsimonious", "translation": "скупой", "example": "He is parsimonious with compliments."},
        {"word": "perfidious", "translation": "вероломный", "example": "This was a perfidious act."},
        {"word": "pertinacious", "translation": "упорный", "example": "She is pertinacious in her pursuit."},
        {"word": "phlegmatic", "translation": "флегматичный", "example": "He has a phlegmatic temperament."},
        {"word": "precipitate", "translation": "поспешный", "example": "Don't make precipitate decisions."},
        {"word": "propitious", "translation": "благоприятный", "example": "The timing is propitious."},
        {"word": "pugnacious", "translation": "драчливый", "example": "He has a pugnacious personality."},
        {"word": "quixotic", "translation": "донкихотский", "example": "It was a quixotic endeavor."},
        {"word": "recalcitrant", "translation": "непокорный", "example": "The recalcitrant child refused to obey."},
        {"word": "sagacious", "translation": "мудрый", "example": "She offered sagacious advice."},
        {"word": "salubrious", "translation": "здоровый", "example": "The mountain air is salubrious."},
        {"word": "sanguine", "translation": "оптимистичный", "example": "He is sanguine about the future."},
        {"word": "scintillating", "translation": "блистательный", "example": "She gave a scintillating performance."},
        {"word": "serendipity", "translation": "счастливая случайность", "example": "Finding this book was pure serendipity."},
        {"word": "sporadic", "translation": "спорадический", "example": "We had sporadic rain all day."},
        {"word": "superfluous", "translation": "излишний", "example": "This information is superfluous."},
        {"word": "taciturn", "translation": "молчаливый", "example": "He is a taciturn man."},
        {"word": "tenacious", "translation": "упорный", "example": "She is tenacious in her beliefs."},
        {"word": "transient", "translation": "временный", "example": "Happiness is often transient."},
        {"word": "ubiquity", "translation": "вездесущность", "example": "The ubiquity of smartphones is remarkable."},
        {"word": "vacillate", "translation": "колебаться", "example": "Don't vacillate - make a decision."},
        {"word": "venerable", "translation": "почтенный", "example": "He is a venerable scholar."},
        {"word": "verbose", "translation": "многословный", "example": "His writing is often verbose."},
        {"word": "vicarious", "translation": "косвенный", "example": "I get vicarious pleasure from her success."},
        {"word": "vindicate", "translation": "оправдывать", "example": "The evidence vindicated him."},
        {"word": "vociferous", "translation": "шумный", "example": "The protestors were vociferous."},
        {"word": "wary", "translation": "осторожный", "example": "Be wary of strangers."},
        {"word": "zealous", "translation": "ревностный", "example": "He is a zealous supporter."}
    ],

    "C2": [
        {"word": "sesquipedalian", "translation": "многосложный", "example": "He enjoys using sesquipedalian words."},
        {"word": "supercilious", "translation": "надменный", "example": "She gave him a supercilious look."},
        {"word": "vicissitude", "translation": "изменение", "example": "Life is full of vicissitudes."},
        {"word": "aberrant", "translation": "отклоняющийся", "example": "This behavior is aberrant."},
        {"word": "abnegation", "translation": "самоотречение", "example": "His abnegation was admirable."},
        {"word": "accretion", "translation": "прирост", "example": "The accretion of knowledge takes time."},
        {"word": "adumbrate", "translation": "предвещать", "example": "The signs adumbrate trouble ahead."},
        {"word": "alacrity", "translation": "готовность", "example": "He accepted with alacrity."},
        {"word": "anachronism", "translation": "анахронизм", "example": "This law is an anachronism."},
        {"word": "antediluvian", "translation": "допотопный", "example": "His ideas are antediluvian."},
        {"word": "apogee", "translation": "апогей", "example": "This represents the apogee of his career."},
        {"word": "apostate", "translation": "отступник", "example": "He was considered an apostate."},
        {"word": "asseverate", "translation": "утверждать", "example": "I must asseverate my position."},
        {"word": "assiduous", "translation": "усердный", "example": "She is assiduous in her work."},
        {"word": "bellicose", "translation": "воинственный", "example": "His bellicose attitude caused problems."},
        {"word": "bowdlerize", "translation": "цензурировать", "example": "The text was bowdlerized for publication."},
        {"word": "calumniate", "translation": "клеветать", "example": "He tried to calumniate his opponent."},
        {"word": "captious", "translation": "придирчивый", "example": "She is captious in her criticism."},
        {"word": "cavil", "translation": "придираться", "example": "Don't cavil at minor details."},
        {"word": "celerity", "translation": "быстрота", "example": "He moved with surprising celerity."},
        {"word": "charlatan", "translation": "шарлатан", "example": "The charlatan deceived many people."},
        {"word": "circumlocution", "translation": "обиняк", "example": "Avoid circumlocution in your writing."},
        {"word": "contumacious", "translation": "непокорный", "example": "His contumacious behavior was punished."},
        {"word": "convivial", "translation": "веселый", "example": "The party had a convivial atmosphere."},
        {"word": "demagogue", "translation": "демагог", "example": "The demagogue manipulated the crowd."},
        {"word": "desultory", "translation": "бессистемный", "example": "His desultory reading lacked focus."},
        {"word": "diaphanous", "translation": "прозрачный", "example": "She wore a diaphanous dress."},
        {"word": "dilatory", "translation": "медлительный", "example": "His dilatory tactics delayed the project."},
        {"word": "disingenuous", "translation": "неискренний", "example": "Her apology seemed disingenuous."},
        {"word": "dissemble", "translation": "скрывать", "example": "He tried to dissemble his true intentions."},
        {"word": "efficacious", "translation": "действенный", "example": "The treatment proved efficacious."},
        {"word": "effluvium", "translation": "испарение", "example": "An unpleasant effluvium filled the room."},
        {"word": "egregious", "translation": "вопиющий", "example": "It was an egregious error."},
        {"word": "encomium", "translation": "панегирик", "example": "He received encomiums for his work."},
        {"word": "ephemeral", "translation": "мимолетный", "example": "Fame is often ephemeral."},
        {"word": "equanimity", "translation": "хладнокровие", "example": "She maintained her equanimity under pressure."},
        {"word": "eschew", "translation": "избегать", "example": "He eschews all forms of violence."},
        {"word": "excoriate", "translation": "критиковать", "example": "The critic excoriated the film."},
        {"word": "exegesis", "translation": "толкование", "example": "His exegesis of the text was brilliant."},
        {"word": "expiate", "translation": "искупать", "example": "He tried to expiate his sins."},
        {"word": "extirpate", "translation": "искоренять", "example": "We must extirpate this evil."},
        {"word": "facetious", "translation": "шутливый", "example": "Don't be facetious about serious matters."},
        {"word": "fallacious", "translation": "ошибочный", "example": "His argument was fallacious."},
        {"word": "fatuous", "translation": "глупый", "example": "It was a fatuous remark."},
        {"word": "garrulous", "translation": "болтливый", "example": "The garrulous old man talked for hours."},
        {"word": "grandiloquent", "translation": "высокопарный", "example": "His grandiloquent speech bored everyone."},
        {"word": "harangue", "translation": "разглагольствовать", "example": "He delivered a long harangue."},
        {"word": "hegemony", "translation": "гегемония", "example": "The country sought cultural hegemony."},
        {"word": "iconoclast", "translation": "иконоборец", "example": "He was an iconoclast in his field."},
        {"word": "idiosyncratic", "translation": "своеобразный", "example": "His style is highly idiosyncratic."},
        {"word": "impecunious", "translation": "бедный", "example": "The impecunious artist struggled to survive."},
        {"word": "impervious", "translation": "непроницаемый", "example": "He is impervious to criticism."},
        {"word": "inchoate", "translation": "зарождающийся", "example": "These are inchoate ideas that need development."},
        {"word": "incontrovertible", "translation": "неопровержимый", "example": "The evidence is incontrovertible."},
        {"word": "indefatigable", "translation": "неутомимый", "example": "She is an indefatigable worker."},
        {"word": "ineffable", "translation": "невыразимый", "example": "The beauty was ineffable."},
        {"word": "insouciant", "translation": "беспечный", "example": "His insouciant attitude worried his parents."},
        {"word": "intransigent", "translation": "непримиримый", "example": "He remains intransigent on this issue."},
        {"word": "invective", "translation": "оскорбление", "example": "He hurled invective at his opponents."},
        {"word": "inveterate", "translation": "закоренелый", "example": "He is an inveterate gambler."},
        {"word": "jejune", "translation": "незрелый", "example": "His arguments were jejune and unconvincing."},
        {"word": "lachrymose", "translation": "слезливый", "example": "The movie had a lachrymose ending."},
        {"word": "laconic", "translation": "лаконичный", "example": "He gave a laconic reply."},
        {"word": "languid", "translation": "вялый", "example": "She moved with languid grace."},
        {"word": "largess", "translation": "щедрость", "example": "His largess helped many charities."},
        {"word": "legerdemain", "translation": "ловкость рук", "example": "The magician's legerdemain amazed the audience."},
        {"word": "loquacious", "translation": "разговорчивый", "example": "She is loquacious at parties."},
        {"word": "lugubrious", "translation": "печальный", "example": "He spoke in a lugubrious tone."},
        {"word": "mendacious", "translation": "лживый", "example": "The statement was mendacious."},
        {"word": "meretricious", "translation": "безвкусный", "example": "The decoration was meretricious."},
        {"word": "mettlesome", "translation": "живой", "example": "She has a mettlesome personality."},
        {"word": "mordant", "translation": "едкий", "example": "His mordant wit made him famous."},
        {"word": "munificent", "translation": "щедрый", "example": "The munificent donation helped the hospital."},
        {"word": "nebulous", "translation": "туманный", "example": "The concept was nebulous and hard to grasp."},
        {"word": "noisome", "translation": "вредный", "example": "A noisome odor filled the room."},
        {"word": "obdurate", "translation": "упрямый", "example": "She remained obdurate in her refusal."},
        {"word": "obfuscate", "translation": "затемнять", "example": "Don't obfuscate the issue with irrelevant details."},
        {"word": "obsequious", "translation": "раболепный", "example": "His obsequious behavior was embarrassing."},
        {"word": "obviate", "translation": "устранять", "example": "This new method obviates the need for manual labor."},
        {"word": "occlude", "translation": "закрывать", "example": "The clouds occlude the sun."},
        {"word": "odious", "translation": "отвратительный", "example": "It was an odious task."},
        {"word": "officious", "translation": "назойливый", "example": "The officious clerk annoyed everyone."},
        {"word": "ossify", "translation": "окостеневать", "example": "Traditions can ossify over time."},
        {"word": "overweening", "translation": "самоуверенный", "example": "His overweening pride was his downfall."},
        {"word": "palpable", "translation": "осязаемый", "example": "The tension in the room was palpable."},
        {"word": "parsimonious", "translation": "скупой", "example": "He is parsimonious with his praise."},
        {"word": "pecuniary", "translation": "денежный", "example": "He had pecuniary difficulties."},
        {"word": "perfidious", "translation": "вероломный", "example": "It was a perfidious act of betrayal."},
        {"word": "perfunctory", "translation": "поверхностный", "example": "He gave a perfunctory greeting."},
        {"word": "pertinacious", "translation": "упорный", "example": "Her pertinacious efforts finally paid off."},
        {"word": "phlegmatic", "translation": "флегматичный", "example": "His phlegmatic nature helped in crises."},
        {"word": "piquant", "translation": "пикантный", "example": "The sauce had a piquant flavor."},
        {"word": "plangent", "translation": "жалобный", "example": "The plangent sound of the violin moved everyone."},
        {"word": "platitude", "translation": "банальность", "example": "He spoke in platitudes."},
        {"word": "plethora", "translation": "избыток", "example": "There is a plethora of information available."},
        {"word": "precipitate", "translation": "поспешный", "example": "Don't make precipitate decisions."},
        {"word": "profligate", "translation": "расточительный", "example": "His profligate spending ruined him."},
        {"word": "propitious", "translation": "благоприятный", "example": "The timing is propitious for change."},
        {"word": "puerile", "translation": "детский", "example": "His puerile behavior was inappropriate."},
        {"word": "pugnacious", "translation": "драчливый", "example": "He has a pugnacious personality."},
        {"word": "pusillanimous", "translation": "малодушный", "example": "His pusillanimous response disappointed everyone."},
        {"word": "quixotic", "translation": "донкихотский", "example": "It was a quixotic attempt to change the system."},
        {"word": "recalcitrant", "translation": "непокорный", "example": "The recalcitrant student was expelled."},
        {"word": "redolent", "translation": "ароматный", "example": "The kitchen was redolent with the smell of baking."},
        {"word": "refulgent", "translation": "сияющий", "example": "The refulgent moon lit up the night."},
        {"word": "sagacious", "translation": "мудрый", "example": "She offered sagacious advice."},
        {"word": "salubrious", "translation": "здоровый", "example": "The mountain air is salubrious."},
        {"word": "sanguine", "translation": "оптимистичный", "example": "He is sanguine about his chances."},
        {"word": "sardonic", "translation": "саркастический", "example": "She gave a sardonic smile."}
    ]
}

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)
    
    try:
        if update and update.effective_user:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text="❌ Произошла ошибка. Пожалуйста, попробуйте еще раз."
            )
    except Exception as e:
        logging.error(f"Error in error handler: {e}")

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
#Сохранение слов в БД()
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

# Команда /start()
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

# Обработка выбора уровня()
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

# Обработка выбора сброса прогресса()
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

# Команда /reset()
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

# Команда /help()
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

# Ежедневная рассылка()
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

# Команда остановки()
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

# Команда для проверки статуса()
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
            
            # Считаем количество изученных слов
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

# Команда для принудительной отправки слов /send()
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
            if words is not None:  # Если не все слова изучены
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

# Основная функция
def main():
    init_db()
    update_db_schema()
    
    application = Application.builder().token(TOKEN).build()

    application.add_error_handler(error_handler)

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("send", send_now))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(🔄 Начать заново|🚫 Завершить)$"), handle_reset_choice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_level))

    # Настройка ежедневной рассылки
    job_queue = application.job_queue
    job_queue.run_daily(
        send_daily_words,
        time=datetime.strptime("09:00", "%H:%M").time(),
        days=(0, 1, 2, 3, 4, 5, 6),
        name="daily_words"
    )

    logging.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()