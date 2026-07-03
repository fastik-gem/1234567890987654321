# -*- coding: utf-8 -*-
"""
Переводы интерфейса бота на 5 языков:
ru - русский, en - английский, uz - узбекский, ko - корейский, ar - арабский
"""

LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "uz": "🇺🇿 O'zbekcha",
    "ko": "🇰🇷 한국어",
    "ar": "🇸🇦 العربية",
}

TEXT = {
    "ru": {
        "welcome": "Привет! 👋 Я бот погоды и курсов валют.\n\nВыберите язык интерфейса:",
        "lang_set": "✅ Язык установлен: Русский",
        "menu_weather": "🌤 Погода",
        "menu_forecast": "📅 Прогноз на неделю",
        "menu_currency": "💱 Курс валют",
        "menu_crypto": "₿ Крипто",
        "menu_mycity": "📍 Мой город",
        "menu_notify": "🔔 Рассылка",
        "menu_fact": "🎲 Факт дня",
        "menu_language": "🌐 Сменить язык",
        "menu_help": "❓ Помощь",
        "ask_city": "🏙 Введите название города (например: Ташкент):",
        "ask_city_save": "🏙 Введите город, который сохранить по умолчанию:",
        "help": (
            "Я умею:\n"
            "🌤 Показывать текущую погоду в любом городе мира\n"
            "📅 Показывать прогноз погоды на неделю вперёд\n"
            "💱 Показывать актуальный курс валют (USD, EUR, RUB, UZS, KRW, AED, UAH, CNY, KZT, GBP, TRY)\n"
            "🧮 Конвертировать суммы — просто напишите, например: 10$ или 100 евро\n"
            "₿ Показывать курс биткоина и эфириума\n"
            "📍 Запоминать ваш город по умолчанию\n"
            "🔔 Присылать погоду и курс валют каждый день в заданное время\n"
            "🌐 Общаться на 5 языках: русский, английский, узбекский, корейский, арабский\n\n"
            "Команды:\n"
            "/start — перезапустить бота\n"
            "/weather — узнать погоду\n"
            "/forecast — прогноз на неделю\n"
            "/currency — курс валют\n"
            "/crypto — курс криптовалют\n"
            "/fact — случайный интересный факт\n"
            "/mycity — сохранить город по умолчанию\n"
            "/notify ЧЧ:ММ — ежедневная рассылка в это время (по Ташкенту)\n"
            "/notify off — выключить рассылку\n"
            "/language — сменить язык\n"
            "/help — эта справка"
        ),
        "currency_title": "💱 Актуальный курс валют:",
        "convert_title": "💱 {amount} {currency} — это:",
        "weather_in": "Погода в городе {city}:",
        "forecast_in": "📅 Прогноз погоды на неделю — {city}:",
        "temp": "🌡 Температура",
        "feels": "🤔 Ощущается как",
        "wind": "💨 Ветер",
        "humidity": "💧 Влажность",
        "city_not_found": "😕 Город не найден. Проверьте название и попробуйте снова.",
        "error": "⚠️ Произошла ошибка. Попробуйте позже.",
        "loading": "⏳ Секунду, ищу данные...",
        "crypto_title": "₿ Курс криптовалют:",
        "mycity_saved": "✅ Город по умолчанию сохранён: {city}",
        "mycity_current": "📍 Ваш город по умолчанию: {city}\n\nЧтобы изменить — нажмите кнопку снова и введите новый город.",
        "mycity_none": "📍 Город по умолчанию ещё не задан.\nВведите город, чтобы сохранить его:",
        "notify_usage": (
            "🔔 Ежедневная рассылка погоды и курса валют.\n\n"
            "Чтобы включить, напишите: /notify ЧЧ:ММ (время по Ташкенту, UTC+5)\n"
            "Например: /notify 08:00\n\n"
            "Чтобы выключить: /notify off\n\n"
            "Не забудьте сначала сохранить город через /mycity, иначе в рассылке будет только курс валют."
        ),
        "notify_set": "✅ Рассылка включена на {time} (по Ташкенту) каждый день.",
        "notify_off": "🔕 Рассылка выключена.",
        "notify_bad_format": "😕 Неверный формат времени. Пример: /notify 08:00",
        "notify_header": "🔔 Ваша ежедневная сводка:",
    },
    "en": {
        "welcome": "Hi! 👋 I'm a weather & currency exchange bot.\n\nChoose your language:",
        "lang_set": "✅ Language set: English",
        "menu_weather": "🌤 Weather",
        "menu_forecast": "📅 Weekly forecast",
        "menu_currency": "💱 Exchange rate",
        "menu_crypto": "₿ Crypto",
        "menu_mycity": "📍 My city",
        "menu_notify": "🔔 Daily digest",
        "menu_fact": "🎲 Fact of the day",
        "menu_language": "🌐 Change language",
        "menu_help": "❓ Help",
        "ask_city": "🏙 Enter a city name (e.g. London):",
        "ask_city_save": "🏙 Enter the city to save as default:",
        "help": (
            "I can:\n"
            "🌤 Show current weather in any city in the world\n"
            "📅 Show a 7-day weather forecast\n"
            "💱 Show up-to-date exchange rates (USD, EUR, RUB, UZS, KRW, AED, UAH, CNY, KZT, GBP, TRY)\n"
            "🧮 Convert amounts — just type e.g.: 10$ or 100 euro\n"
            "₿ Show Bitcoin and Ethereum prices\n"
            "📍 Remember your default city\n"
            "🔔 Send you a daily weather + currency digest at a chosen time\n"
            "🌐 Chat in 5 languages: Russian, English, Uzbek, Korean, Arabic\n\n"
            "Commands:\n"
            "/start — restart the bot\n"
            "/weather — check weather\n"
            "/forecast — 7-day forecast\n"
            "/currency — exchange rates\n"
            "/crypto — crypto rates\n"
            "/fact — a random interesting fact\n"
            "/mycity — save your default city\n"
            "/notify HH:MM — daily digest at this time (Tashkent time)\n"
            "/notify off — turn off the digest\n"
            "/language — change language\n"
            "/help — this help message"
        ),
        "currency_title": "💱 Current exchange rates:",
        "convert_title": "💱 {amount} {currency} equals:",
        "weather_in": "Weather in {city}:",
        "forecast_in": "📅 7-day weather forecast — {city}:",
        "temp": "🌡 Temperature",
        "feels": "🤔 Feels like",
        "wind": "💨 Wind",
        "humidity": "💧 Humidity",
        "city_not_found": "😕 City not found. Check the spelling and try again.",
        "error": "⚠️ Something went wrong. Please try again later.",
        "loading": "⏳ One second, fetching data...",
        "crypto_title": "₿ Crypto rates:",
        "mycity_saved": "✅ Default city saved: {city}",
        "mycity_current": "📍 Your default city: {city}\n\nTo change it — tap the button again and enter a new city.",
        "mycity_none": "📍 No default city set yet.\nEnter a city to save it:",
        "notify_usage": (
            "🔔 Daily weather & currency digest.\n\n"
            "To enable, send: /notify HH:MM (Tashkent time, UTC+5)\n"
            "Example: /notify 08:00\n\n"
            "To disable: /notify off\n\n"
            "Set your city first via /mycity, otherwise only exchange rates will be sent."
        ),
        "notify_set": "✅ Daily digest enabled at {time} (Tashkent time), every day.",
        "notify_off": "🔕 Daily digest turned off.",
        "notify_bad_format": "😕 Invalid time format. Example: /notify 08:00",
        "notify_header": "🔔 Your daily digest:",
    },
    "uz": {
        "welcome": "Salom! 👋 Men ob-havo va valyuta kursi botiman.\n\nTilni tanlang:",
        "lang_set": "✅ Til o'rnatildi: O'zbekcha",
        "menu_weather": "🌤 Ob-havo",
        "menu_forecast": "📅 Haftalik prognoz",
        "menu_currency": "💱 Valyuta kursi",
        "menu_crypto": "₿ Kripto",
        "menu_mycity": "📍 Mening shahrim",
        "menu_notify": "🔔 Kunlik xabar",
        "menu_fact": "🎲 Kunning faktı",
        "menu_language": "🌐 Tilni o'zgartirish",
        "menu_help": "❓ Yordam",
        "ask_city": "🏙 Shahar nomini kiriting (masalan: Toshkent):",
        "ask_city_save": "🏙 Standart sifatida saqlanadigan shaharni kiriting:",
        "help": (
            "Men quyidagilarni bilaman:\n"
            "🌤 Dunyodagi istalgan shahar ob-havosini ko'rsatish\n"
            "📅 7 kunlik ob-havo prognozini ko'rsatish\n"
            "💱 Dolzarb valyuta kurslarini ko'rsatish (USD, EUR, RUB, UZS, KRW, AED, UAH, CNY, KZT, GBP, TRY)\n"
            "🧮 Summalarni konvertatsiya qilish — yozing, masalan: 10$ yoki 100 evro\n"
            "₿ Bitcoin va Ethereum narxini ko'rsatish\n"
            "📍 Standart shahringizni eslab qolish\n"
            "🔔 Har kuni belgilangan vaqtda ob-havo va valyuta kursini yuborish\n"
            "🌐 5 tilda muloqot qilish: rus, ingliz, o'zbek, koreys, arab\n\n"
            "Buyruqlar:\n"
            "/start — botni qayta ishga tushirish\n"
            "/weather — ob-havoni bilish\n"
            "/forecast — 7 kunlik prognoz\n"
            "/currency — valyuta kursi\n"
            "/crypto — kripto kurslari\n"
            "/fact — tasodifiy qiziqarli fakt\n"
            "/mycity — standart shaharni saqlash\n"
            "/notify SS:DD — shu vaqtda kunlik xabar (Toshkent vaqti)\n"
            "/notify off — xabarni o'chirish\n"
            "/language — tilni o'zgartirish\n"
            "/help — ushbu yordam"
        ),
        "currency_title": "💱 Dolzarb valyuta kurslari:",
        "convert_title": "💱 {amount} {currency} — bu:",
        "weather_in": "{city} shahridagi ob-havo:",
        "forecast_in": "📅 7 kunlik ob-havo prognozi — {city}:",
        "temp": "🌡 Harorat",
        "feels": "🤔 Sezilishi",
        "wind": "💨 Shamol",
        "humidity": "💧 Namlik",
        "city_not_found": "😕 Shahar topilmadi. Nomini tekshirib, qayta urinib ko'ring.",
        "error": "⚠️ Xatolik yuz berdi. Keyinroq urinib ko'ring.",
        "loading": "⏳ Bir soniya, ma'lumot qidiryapman...",
        "crypto_title": "₿ Kripto kurslari:",
        "mycity_saved": "✅ Standart shahar saqlandi: {city}",
        "mycity_current": "📍 Sizning standart shahringiz: {city}\n\nO'zgartirish uchun tugmani qayta bosing va yangi shaharni kiriting.",
        "mycity_none": "📍 Standart shahar hali belgilanmagan.\nSaqlash uchun shaharni kiriting:",
        "notify_usage": (
            "🔔 Kunlik ob-havo va valyuta kursi xabari.\n\n"
            "Yoqish uchun yuboring: /notify SS:DD (Toshkent vaqti, UTC+5)\n"
            "Masalan: /notify 08:00\n\n"
            "O'chirish uchun: /notify off\n\n"
            "Avval /mycity orqali shaharni saqlang, aks holda faqat valyuta kursi yuboriladi."
        ),
        "notify_set": "✅ Kunlik xabar {time} da (Toshkent vaqti) yoqildi, har kuni yuboriladi.",
        "notify_off": "🔕 Kunlik xabar o'chirildi.",
        "notify_bad_format": "😕 Vaqt formati noto'g'ri. Masalan: /notify 08:00",
        "notify_header": "🔔 Kunlik xabaringiz:",
    },
    "ko": {
        "welcome": "안녕하세요! 👋 저는 날씨 및 환율 봇입니다.\n\n언어를 선택하세요:",
        "lang_set": "✅ 언어가 설정되었습니다: 한국어",
        "menu_weather": "🌤 날씨",
        "menu_forecast": "📅 주간 예보",
        "menu_currency": "💱 환율",
        "menu_crypto": "₿ 암호화폐",
        "menu_mycity": "📍 내 도시",
        "menu_notify": "🔔 일일 알림",
        "menu_fact": "🎲 오늘의 사실",
        "menu_language": "🌐 언어 변경",
        "menu_help": "❓ 도움말",
        "ask_city": "🏙 도시 이름을 입력하세요 (예: 서울):",
        "ask_city_save": "🏙 기본으로 저장할 도시를 입력하세요:",
        "help": (
            "제가 할 수 있는 일:\n"
            "🌤 전 세계 모든 도시의 현재 날씨 보기\n"
            "📅 7일간 날씨 예보 보기\n"
            "💱 최신 환율 보기 (USD, EUR, RUB, UZS, KRW, AED, UAH, CNY, KZT, GBP, TRY)\n"
            "🧮 금액 변환 — 예: 10$ 또는 100 유로 라고 입력하세요\n"
            "₿ 비트코인과 이더리움 시세 보기\n"
            "📍 기본 도시 저장\n"
            "🔔 매일 정해진 시간에 날씨와 환율 요약 보내기\n"
            "🌐 5개 언어로 대화 가능: 러시아어, 영어, 우즈베크어, 한국어, 아랍어\n\n"
            "명령어:\n"
            "/start — 봇 재시작\n"
            "/weather — 날씨 확인\n"
            "/forecast — 7일 예보\n"
            "/currency — 환율 확인\n"
            "/crypto — 암호화폐 시세\n"
            "/fact — 무작위 흥미로운 사실\n"
            "/mycity — 기본 도시 저장\n"
            "/notify HH:MM — 이 시간에 매일 알림 (타슈켄트 시간)\n"
            "/notify off — 알림 끄기\n"
            "/language — 언어 변경\n"
            "/help — 도움말 보기"
        ),
        "currency_title": "💱 현재 환율:",
        "convert_title": "💱 {amount} {currency}는:",
        "weather_in": "{city}의 날씨:",
        "forecast_in": "📅 7일 날씨 예보 — {city}:",
        "temp": "🌡 기온",
        "feels": "🤔 체감온도",
        "wind": "💨 바람",
        "humidity": "💧 습도",
        "city_not_found": "😕 도시를 찾을 수 없습니다. 철자를 확인하고 다시 시도하세요.",
        "error": "⚠️ 오류가 발생했습니다. 나중에 다시 시도해 주세요.",
        "loading": "⏳ 잠시만요, 데이터를 찾고 있습니다...",
        "crypto_title": "₿ 암호화폐 시세:",
        "mycity_saved": "✅ 기본 도시가 저장되었습니다: {city}",
        "mycity_current": "📍 기본 도시: {city}\n\n변경하려면 버튼을 다시 누르고 새 도시를 입력하세요.",
        "mycity_none": "📍 아직 기본 도시가 설정되지 않았습니다.\n저장할 도시를 입력하세요:",
        "notify_usage": (
            "🔔 매일 날씨와 환율 요약 알림.\n\n"
            "켜려면 보내세요: /notify HH:MM (타슈켄트 시간, UTC+5)\n"
            "예: /notify 08:00\n\n"
            "끄려면: /notify off\n\n"
            "먼저 /mycity로 도시를 저장하세요. 그렇지 않으면 환율만 전송됩니다."
        ),
        "notify_set": "✅ 매일 {time}에 (타슈켄트 시간) 알림이 켜졌습니다.",
        "notify_off": "🔕 일일 알림이 꺼졌습니다.",
        "notify_bad_format": "😕 시간 형식이 올바르지 않습니다. 예: /notify 08:00",
        "notify_header": "🔔 오늘의 요약:",
    },
    "ar": {
        "welcome": "مرحباً! 👋 أنا بوت الطقس وأسعار الصرف.\n\nاختر اللغة:",
        "lang_set": "✅ تم ضبط اللغة: العربية",
        "menu_weather": "🌤 الطقس",
        "menu_forecast": "📅 توقعات الأسبوع",
        "menu_currency": "💱 سعر الصرف",
        "menu_crypto": "₿ العملات الرقمية",
        "menu_mycity": "📍 مدينتي",
        "menu_notify": "🔔 التنبيه اليومي",
        "menu_fact": "🎲 حقيقة اليوم",
        "menu_language": "🌐 تغيير اللغة",
        "menu_help": "❓ مساعدة",
        "ask_city": "🏙 أدخل اسم المدينة (مثال: دبي):",
        "ask_city_save": "🏙 أدخل المدينة لحفظها كافتراضية:",
        "help": (
            "يمكنني:\n"
            "🌤 عرض حالة الطقس الحالية لأي مدينة في العالم\n"
            "📅 عرض توقعات الطقس لمدة 7 أيام\n"
            "💱 عرض أسعار الصرف المحدثة (USD, EUR, RUB, UZS, KRW, AED, UAH, CNY, KZT, GBP, TRY)\n"
            "🧮 تحويل المبالغ — فقط اكتب مثلاً: 10$ أو 100 يورو\n"
            "₿ عرض أسعار البيتكوين والإيثيريوم\n"
            "📍 حفظ مدينتك الافتراضية\n"
            "🔔 إرسال ملخص يومي للطقس وأسعار الصرف في وقت محدد\n"
            "🌐 التحدث بـ 5 لغات: الروسية، الإنجليزية، الأوزبكية، الكورية، العربية\n\n"
            "الأوامر:\n"
            "/start — إعادة تشغيل البوت\n"
            "/weather — معرفة الطقس\n"
            "/forecast — توقعات 7 أيام\n"
            "/currency — أسعار الصرف\n"
            "/crypto — أسعار العملات الرقمية\n"
            "/fact — حقيقة عشوائية مثيرة للاهتمام\n"
            "/mycity — حفظ المدينة الافتراضية\n"
            "/notify HH:MM — تنبيه يومي في هذا الوقت (بتوقيت طشقند)\n"
            "/notify off — إيقاف التنبيه\n"
            "/language — تغيير اللغة\n"
            "/help — هذه المساعدة"
        ),
        "currency_title": "💱 أسعار الصرف الحالية:",
        "convert_title": "💱 {amount} {currency} يساوي:",
        "weather_in": "الطقس في {city}:",
        "forecast_in": "📅 توقعات الطقس لمدة 7 أيام — {city}:",
        "temp": "🌡 درجة الحرارة",
        "feels": "🤔 الإحساس الحراري",
        "wind": "💨 الرياح",
        "humidity": "💧 الرطوبة",
        "city_not_found": "😕 لم يتم العثور على المدينة. تحقق من الاسم وحاول مرة أخرى.",
        "error": "⚠️ حدث خطأ ما. حاول مرة أخرى لاحقاً.",
        "loading": "⏳ لحظة، جارٍ البحث عن البيانات...",
        "crypto_title": "₿ أسعار العملات الرقمية:",
        "mycity_saved": "✅ تم حفظ المدينة الافتراضية: {city}",
        "mycity_current": "📍 مدينتك الافتراضية: {city}\n\nلتغييرها — اضغط الزر مرة أخرى وأدخل مدينة جديدة.",
        "mycity_none": "📍 لم يتم تعيين مدينة افتراضية بعد.\nأدخل مدينة لحفظها:",
        "notify_usage": (
            "🔔 ملخص يومي للطقس وأسعار الصرف.\n\n"
            "للتفعيل، أرسل: /notify HH:MM (بتوقيت طشقند UTC+5)\n"
            "مثال: /notify 08:00\n\n"
            "للإيقاف: /notify off\n\n"
            "احفظ مدينتك أولاً عبر /mycity، وإلا سيتم إرسال أسعار الصرف فقط."
        ),
        "notify_set": "✅ تم تفعيل الملخص اليومي الساعة {time} (بتوقيت طشقند) كل يوم.",
        "notify_off": "🔕 تم إيقاف الملخص اليومي.",
        "notify_bad_format": "😕 صيغة الوقت غير صحيحة. مثال: /notify 08:00",
        "notify_header": "🔔 ملخصك اليومي:",
    },
}

# Описание погодных условий (WMO weather codes) на 5 языках
WEATHER_DESC = {
    "ru": {
        "clear": "Ясно ☀️", "mainly_clear": "Малооблачно 🌤",
        "cloudy": "Облачно ☁️", "overcast": "Пасмурно ☁️",
        "fog": "Туман 🌫", "drizzle": "Морось 🌦",
        "rain": "Дождь 🌧", "snow": "Снег 🌨",
        "showers": "Ливень 🌧", "thunderstorm": "Гроза ⛈",
        "unknown": "Неизвестно",
    },
    "en": {
        "clear": "Clear ☀️", "mainly_clear": "Mostly clear 🌤",
        "cloudy": "Cloudy ☁️", "overcast": "Overcast ☁️",
        "fog": "Fog 🌫", "drizzle": "Drizzle 🌦",
        "rain": "Rain 🌧", "snow": "Snow 🌨",
        "showers": "Showers 🌧", "thunderstorm": "Thunderstorm ⛈",
        "unknown": "Unknown",
    },
    "uz": {
        "clear": "Ochiq ☀️", "mainly_clear": "Deyarli ochiq 🌤",
        "cloudy": "Bulutli ☁️", "overcast": "Bulutli havo ☁️",
        "fog": "Tuman 🌫", "drizzle": "Mayda yomg'ir 🌦",
        "rain": "Yomg'ir 🌧", "snow": "Qor 🌨",
        "showers": "Jala 🌧", "thunderstorm": "Momaqaldiroq ⛈",
        "unknown": "Noma'lum",
    },
    "ko": {
        "clear": "맑음 ☀️", "mainly_clear": "대체로 맑음 🌤",
        "cloudy": "흐림 ☁️", "overcast": "구름 많음 ☁️",
        "fog": "안개 🌫", "drizzle": "이슬비 🌦",
        "rain": "비 🌧", "snow": "눈 🌨",
        "showers": "소나기 🌧", "thunderstorm": "뇌우 ⛈",
        "unknown": "알 수 없음",
    },
    "ar": {
        "clear": "صافٍ ☀️", "mainly_clear": "صافٍ غالباً 🌤",
        "cloudy": "غائم ☁️", "overcast": "غائم كلياً ☁️",
        "fog": "ضباب 🌫", "drizzle": "رذاذ 🌦",
        "rain": "مطر 🌧", "snow": "ثلج 🌨",
        "showers": "زخات مطر 🌧", "thunderstorm": "عاصفة رعدية ⛈",
        "unknown": "غير معروف",
    },
}

# Сопоставление кодов WMO с ключами из WEATHER_DESC
WMO_CODE_MAP = {
    0: "clear",
    1: "mainly_clear", 2: "cloudy", 3: "overcast",
    45: "fog", 48: "fog",
    51: "drizzle", 53: "drizzle", 55: "drizzle",
    56: "drizzle", 57: "drizzle",
    61: "rain", 63: "rain", 65: "rain",
    66: "rain", 67: "rain",
    71: "snow", 73: "snow", 75: "snow", 77: "snow",
    80: "showers", 81: "showers", 82: "showers",
    85: "snow", 86: "snow",
    95: "thunderstorm", 96: "thunderstorm", 99: "thunderstorm",
}

# Названия дней недели для прогноза (индекс 0 = понедельник, как в Python weekday())
WEEKDAYS = {
    "ru": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "uz": ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"],
    "ko": ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
    "ar": ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"],
}

# Факты дня на 5 языках (случайный факт по команде /fact)
FACTS = {
    "ru": [
        "🍯 Мёд практически не портится — археологи находили съедобный мёд в египетских гробницах возрастом более 3000 лет.",
        "🐙 У осьминога три сердца и голубая кровь.",
        "🌍 Один день на Венере длиннее, чем один год на Венере.",
        "🦒 У жирафа и человека одинаковое количество шейных позвонков — по семь.",
        "🍌 Бананы — это ягоды, а клубника — нет.",
        "🧠 Мозг человека использует около 20% всей энергии тела.",
        "🐘 Слоны — единственные животные, которые не умеют прыгать.",
        "❄️ Снежинка может состоять из более чем 200 кристаллов льда.",
        "🌊 Мирового океана изучено меньше, чем поверхности Луны.",
        "🐌 Улитка может спать до трёх лет подряд.",
        "🍫 Шоколад когда-то использовался как денежная единица у ацтеков.",
        "🦈 Акулы существуют на Земле дольше, чем деревья.",
        "🌕 Луна медленно удаляется от Земли — примерно на 3,8 см в год.",
        "🐝 Пчёлы могут узнавать человеческие лица.",
        "🕰 Первый будильник мог звонить только в 4 утра.",
        "🐧 Пингвины делают предложение своей паре, преподнося камешек.",
        "🍅 Помидор ботанически является фруктом, а не овощем.",
        "⚡ Молния горячее поверхности Солнца.",
        "🐬 Дельфины дают своим детёнышам имена в виде уникального свиста.",
        "📚 Мёд — единственный продукт питания, который никогда не портится.",
    ],
    "en": [
        "🍯 Honey never spoils — archaeologists have found edible honey in Egyptian tombs over 3,000 years old.",
        "🐙 An octopus has three hearts and blue blood.",
        "🌍 A day on Venus is longer than a year on Venus.",
        "🦒 Giraffes and humans have the same number of neck vertebrae — seven.",
        "🍌 Bananas are berries, but strawberries aren't.",
        "🧠 The human brain uses about 20% of the body's total energy.",
        "🐘 Elephants are the only animals that can't jump.",
        "❄️ A single snowflake can contain over 200 ice crystals.",
        "🌊 More of the ocean floor has been mapped on the Moon than on Earth.",
        "🐌 A snail can sleep for up to three years at a time.",
        "🍫 Chocolate was once used as currency by the Aztecs.",
        "🦈 Sharks have existed longer than trees.",
        "🌕 The Moon is slowly drifting away from Earth — about 3.8 cm per year.",
        "🐝 Bees can recognize human faces.",
        "🕰 The first alarm clock could only ring at 4 a.m.",
        "🐧 Penguins propose to their mate with a pebble.",
        "🍅 A tomato is botanically a fruit, not a vegetable.",
        "⚡ Lightning is hotter than the surface of the Sun.",
        "🐬 Dolphins give their calves unique signature whistles as names.",
        "📚 Honey is the only food that never spoils.",
    ],
    "uz": [
        "🍯 Asal hech qachon buzilmaydi — arxeologlar Misr qabrlaridan 3000 yildan oshgan yeyiladigan asal topishgan.",
        "🐙 Sakkizoyoqning uchta yuragi va ko'k qoni bor.",
        "🌍 Venerada bir kun Veneradagi bir yildan uzunroq.",
        "🦒 Jirafa va odamning bo'yin umurtqalari soni bir xil — yettitadan.",
        "🍌 Banan bu — rezavor, lekin qulupnay unday emas.",
        "🧠 Inson miyasi tananing umumiy energiyasining taxminan 20 foizini sarflaydi.",
        "🐘 Fillar sakray olmaydigan yagona hayvonlar.",
        "❄️ Bitta qor parchasida 200 dan ortiq muz kristali bo'lishi mumkin.",
        "🌊 Oy yuzasi Yer okeani tubidan ko'ra ko'proq o'rganilgan.",
        "🐌 Salyanka uch yilgacha uxlab yotishi mumkin.",
        "🍫 Shokolad bir vaqtlar atseklarda pul o'rnida ishlatilgan.",
        "🦈 Akulalar daraxtlarga qaraganda ancha uzoq vaqtdan beri mavjud.",
        "🌕 Oy Yerdan sekin uzoqlashmoqda — yiliga taxminan 3,8 sm.",
        "🐝 Asalarilar inson yuzlarini tanishi mumkin.",
        "🕰 Birinchi uyg'otuvchi soat faqat ertalab soat 4 da jiringlagan.",
        "🐧 Pingvinlar juftiga toshcha sovg'a qilib turmush qurishni taklif qilishadi.",
        "🍅 Pomidor botanik jihatdan meva hisoblanadi, sabzavot emas.",
        "⚡ Chaqmoq Quyosh yuzasidan ham issiqroq.",
        "🐬 Delfinlar bolalariga o'ziga xos hushtak nomlarini berishadi.",
        "📚 Asal — hech qachon buzilmaydigan yagona oziq-ovqat mahsuloti.",
    ],
    "ko": [
        "🍯 꿀은 절대 상하지 않습니다 — 고고학자들은 3,000년 넘은 이집트 무덤에서 먹을 수 있는 꿀을 발견했습니다.",
        "🐙 문어는 심장이 3개이고 피가 파란색입니다.",
        "🌍 금성의 하루는 금성의 1년보다 깁니다.",
        "🦒 기린과 인간의 목뼈 개수는 똑같이 7개입니다.",
        "🍌 바나나는 베리류지만 딸기는 아닙니다.",
        "🧠 인간의 뇌는 신체 전체 에너지의 약 20%를 사용합니다.",
        "🐘 코끼리는 점프를 못하는 유일한 동물입니다.",
        "❄️ 눈송이 하나에 200개가 넘는 얼음 결정이 포함될 수 있습니다.",
        "🌊 지구 해저보다 달 표면이 더 많이 지도화되었습니다.",
        "🐌 달팽이는 한 번에 최대 3년까지 잠을 잘 수 있습니다.",
        "🍫 초콜릿은 한때 아즈텍인들 사이에서 화폐로 쓰였습니다.",
        "🦈 상어는 나무보다 오래전부터 존재했습니다.",
        "🌕 달은 매년 약 3.8cm씩 지구에서 멀어지고 있습니다.",
        "🐝 꿀벌은 사람의 얼굴을 알아볼 수 있습니다.",
        "🕰 최초의 자명종은 새벽 4시에만 울릴 수 있었습니다.",
        "🐧 펭귄은 조약돌을 선물하며 짝에게 청혼합니다.",
        "🍅 토마토는 식물학적으로 채소가 아니라 과일입니다.",
        "⚡ 번개는 태양 표면보다 뜨겁습니다.",
        "🐬 돌고래는 새끼에게 고유한 휘파람 소리로 이름을 지어줍니다.",
        "📚 꿀은 절대 상하지 않는 유일한 식품입니다.",
    ],
    "ar": [
        "🍯 العسل لا يفسد أبداً — عثر علماء الآثار على عسل صالح للأكل في مقابر مصرية عمرها أكثر من 3000 عام.",
        "🐙 الأخطبوط لديه ثلاثة قلوب ودمه أزرق.",
        "🌍 اليوم على كوكب الزهرة أطول من سنة كاملة عليه.",
        "🦒 الزرافة والإنسان لديهما نفس عدد فقرات الرقبة — سبع فقرات.",
        "🍌 الموز يُصنّف نباتياً كتوت، لكن الفراولة ليست كذلك.",
        "🧠 يستهلك دماغ الإنسان حوالي 20٪ من طاقة الجسم الكلية.",
        "🐘 الفيلة هي الحيوانات الوحيدة التي لا تستطيع القفز.",
        "❄️ قد تحتوي رقاقة ثلج واحدة على أكثر من 200 بلورة جليدية.",
        "🌊 تم رسم خرائط سطح القمر أكثر من قاع المحيطات على الأرض.",
        "🐌 يمكن للحلزون أن ينام لمدة تصل إلى ثلاث سنوات متواصلة.",
        "🍫 استُخدمت الشوكولاتة في وقت من الأوقات كعملة عند شعب الأزتك.",
        "🦈 توجد أسماك القرش على الأرض منذ زمن أطول من الأشجار.",
        "🌕 يبتعد القمر ببطء عن الأرض بمعدل 3.8 سم تقريباً كل عام.",
        "🐝 يمكن للنحل التعرف على وجوه البشر.",
        "🕰 كان المنبه الأول يرن فقط في الساعة 4 فجراً.",
        "🐧 يتقدم طائر البطريق لشريكه بهدية حصاة صغيرة.",
        "🍅 الطماطم من الناحية النباتية فاكهة وليست خضاراً.",
        "⚡ البرق أسخن من سطح الشمس.",
        "🐬 تُطلق الدلافين على صغارها أسماء عبر صفير فريد خاص بكل واحد.",
        "📚 العسل هو الغذاء الوحيد الذي لا يفسد أبداً.",
    ],
}
