import asyncio
import time
import sys
import random
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.network.connection import ConnectionTcpAbridged

print(f"✅ Python: {sys.version}")
print("=" * 50)
print("⏰ Время запуска:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==========================================
# ДАННЫЕ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ (GitHub Secrets)
# ==========================================
API_ID = int(os.environ.get('API_ID', 35315453))
API_HASH = os.environ.get('API_HASH', "7f2e9bf84bc1c44452f8c743b02d08e6")
PHONE = os.environ.get('PHONE', "+79063443355")
# ==========================================

# ==========================================
# НАСТРОЙКИ ВРЕМЕНИ (МОСКОВСКОЕ ВРЕМЯ)
# ==========================================
START_HOUR = 9   # Начинаем в 9:00 по Москве
END_HOUR = 21    # Заканчиваем в 21:00 по Москве
timezone_offset = timedelta(hours=3)  # UTC+3 для Москвы
# ==========================================

# ==========================================
# 5 ВАРИАНТОВ СООБЩЕНИЙ
# ==========================================
MESSAGES = [
    """Добрый день! 👋

Меня зовут Алексей. Уже более 7 лет возвращаю мягкой мебели первозданный вид — быстро, безопасно и без лишних хлопот для вас.

Почему выбирают меня:

✨ Срочность – чистота уже через 1–2 часа после приезда.
✨ Безопасность – гипоаллергенные средства без запаха. Можно детям и животным.
✨ Результат – удаляю даже застарелые пятна, следы от питомцев и стойкие запахи.
✨ Удобство – выезжаю в день звонка, работаю без выходных.

📱 Хотите узнать стоимость?
Просто отправьте фото вашей мебели в бот @HimchistcaSamara_bot — я оценю объём и сложность, назову точную цену.
Без скрытых платежей и сюрпризов.""",

    """Добрый день! 🌿

Меня зовут Алексей, я профессионально занимаюсь химчисткой мебели уже 7 лет. Моя главная гордость — это безопасность для вашей семьи.

Что я гарантирую:

🧴 Только сертифицированные эко-средства без фосфатов и химии.
👶 Без запаха — подходит даже для малышей и аллергиков.
🐾 Бережно удаляю пятна, запахи и следы от питомцев.

Узнайте точную стоимость прямо сейчас:
Просто сфотографируйте мебель и отправьте в бот @HimchistcaSamara_bot — я скажу цену и время чистки. Быстро, честно, без сюрпризов.

Работаю ежедневно, выезд в день обращения.
Сохраните меня в Telegram, чтобы не потерять! 🔥""",

    """Срочно нужна чистота? ⏱️

Меня зовут Алексей, я делаю химчистку мебели более 7 лет. И я знаю, как важна оперативность.

Мои преимущества:

⚡ Чистота уже через 1–2 часа!
🚗 Выезд в день звонка, без выходных.
🧽 Удаляю любые загрязнения — от кофе до следов животных.
🌿 Безопасные средства без резкого запаха.

Не гадайте с ценой — просто отправьте фото!
Бот @HimchistcaSamara_bot мгновенно примет ваш запрос, а я назову точную стоимость по объёму работы.

Спрей-экстракция + энзимы = идеальный результат.
Жду ваше фото! 📸""",

    """Здравствуйте! 👨‍🔧

Меня зовут Алексей, за плечами 7 лет опыта в химчистке мягкой мебели. Я не просто мою — я восстанавливаю.

Почему я профессионал:

🔬 Работаю строго по технологии: преспрей → основная чистка → пятновыведение → промывка.
🧪 Использую энзимные и терпеновые средства — бережно и эффективно.
🏆 Удаляю даже стойкие пятна и запахи, с которыми не справляются другие.

Сколько будет стоить ваша мебель?
Отправьте фото в бот @HimchistcaSamara_bot — я оценю сложность и назову цену. Это займёт меньше минуты.

Работаю каждый день с 8:00 до 23:00.
Сохраните бота — чистота всегда на связи! 📲""",

    """Привет! 👋

Я Алексей, химчистка мебели — моё дело уже 7 лет.

Коротко о главном:

✅ Чистота через 1–2 часа.
✅ Безопасно для детей и животных.
✅ Убираю пятна, запахи, следы от питомцев.
✅ Приезжаю в день звонка.

Хотите узнать цену?
Просто отправьте фото мебели в бот @HimchistcaSamara_bot — я скажу точную стоимость и время работы. Честно, прозрачно, без скрытых платежей.

Работаю с эко-средствами методом спрей-экстракции.
Жду ваше фото! 📸"""
]
# ==========================================

# ==========================================
# СПИСОК КАРТИНОК
# ==========================================
IMAGES = ["photo1.jpg", "photo.jpg", "photo2.jpg"]
# ==========================================

# ==========================================
# ПУТИ К ФАЙЛАМ
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "images")
FRIENDS_FILE = os.path.join(SCRIPT_DIR, "friends.txt")
# ==========================================

def is_working_hours():
    """Проверяет, сейчас рабочие часы по Москве (9:00 – 21:00)"""
    moscow_now = datetime.utcnow() + timezone_offset
    return START_HOUR <= moscow_now.hour < END_HOUR

def get_random_message():
    return random.choice(MESSAGES)

def get_random_image():
    if not os.path.exists(IMAGE_FOLDER):
        return None
    images = [os.path.join(IMAGE_FOLDER, img) for img in IMAGES if os.path.exists(os.path.join(IMAGE_FOLDER, img))]
    return random.choice(images) if images else None

def load_friends():
    friends = []
    try:
        with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.isdigit():
                        friends.append(int(line))
                    else:
                        friends.append(line)
        print(f"✅ Загружено {len(friends)} контактов из friends.txt")
        return friends
    except FileNotFoundError:
        print(f"❌ Файл {FRIENDS_FILE} не найден!")
        return []

async def main():
    print("=" * 50)
    print("🛋️  ОТПРАВКА СООБЩЕНИЙ ДРУЗЬЯМ (GitHub Actions)")
    print("=" * 50)
    
    # Московское время
    moscow_now = datetime.utcnow() + timezone_offset
    print(f"⏰ Московское время: {moscow_now.strftime('%H:%M')}")
    print(f"⏰ Рабочие часы (МСК): {START_HOUR}:00 – {END_HOUR}:00")
    print(f"📁 Папка проекта: {SCRIPT_DIR}")
    
    if not is_working_hours():
        print(f"⏰ Сейчас {moscow_now.strftime('%H:%M')} МСК — нерабочее время. Завершаю.")
        print(f"   Скрипт работает с {START_HOUR}:00 до {END_HOUR}:00 по Москве.")
        return
    
    FRIENDS = load_friends()
    if not FRIENDS:
        print("❌ Нет контактов для отправки!")
        return
    
    print(f"📬 Всего друзей: {len(FRIENDS)}")
    print("📝 5 вариантов сообщений (случайный выбор)")
    print("🖼️  3 картинки (случайный выбор)")
    print("⏳ Пауза: 12-20 минут (случайно)")
    print("=" * 50)
    print()
    
    client = TelegramClient(
        os.path.join(SCRIPT_DIR, "my_account"),
        API_ID,
        API_HASH,
        connection_retries=5,
        retry_delay=2,
        timeout=30
    )
    
    try:
        print("⏳ Подключение к Telegram...")
        await client.start(phone=PHONE)
        
        me = await client.get_me()
        print(f"✅ Вход выполнен: {me.first_name} (@{me.username})")
        print()
        
        sent = 0
        total_sent = 0
        hour_start = time.time()
        
        for idx, friend in enumerate(FRIENDS, 1):
            # Проверка времени по Москве
            moscow_now = datetime.utcnow() + timezone_offset
            if not (START_HOUR <= moscow_now.hour < END_HOUR):
                print(f"\n⏰ {moscow_now.strftime('%H:%M')} МСК - Конец рабочего дня.")
                break
            
            if sent >= 5:
                elapsed = time.time() - hour_start
                if elapsed < 3600:
                    wait_time = int(3600 - elapsed)
                    print(f"\n⏰ Лимит 5 сообщений в час.")
                    print(f"⏳ Ожидание {wait_time // 60} минут...")
                    await asyncio.sleep(wait_time)
                sent = 0
                hour_start = time.time()
            
            try:
                message = get_random_message()
                image_file = get_random_image()
                
                print(f"[{idx}/{len(FRIENDS)}] Отправка для: {friend}...")
                if image_file:
                    await client.send_file(friend, image_file, caption=message)
                else:
                    await client.send_message(friend, message)
                
                sent += 1
                total_sent += 1
                print(f"   ✅ Успешно! (всего: {total_sent}, в час: {sent}/5)")
                
                if idx < len(FRIENDS):
                    wait_minutes = random.randint(12, 20)
                    print(f"   ⏳ Пауза {wait_minutes} минут...")
                    await asyncio.sleep(wait_minutes * 60)
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        print("\n" + "=" * 50)
        print("📊 ИТОГ:")
        print(f"   ✅ Успешно: {total_sent}")
        print(f"   ❌ Ошибок: {len(FRIENDS) - total_sent}")
        print("=" * 50)
        
        await client.disconnect()
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("\nПРОВЕРЬТЕ:")
        print("1. Правильно ли указаны секреты в GitHub?")
        print("2. Есть ли файл friends.txt в репозитории?")
        print("3. Есть ли папка images с картинками?")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Скрипт остановлен пользователем")
