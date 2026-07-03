# -*- coding: utf-8 -*-
"""
Telegram-бот: погода + курс валют + крипто, интерфейс на 5 языках
(русский, английский, узбекский, корейский, арабский).

Как запустить:
1. pip install -r requirements.txt
2. Создать файл .env (см. .env.example) и вписать туда токен бота
3. python bot.py

Токен бота получить у @BotFather в Telegram.
"""

import json
import logging
import os
import random
import re
import threading
from datetime import datetime, time as dt_time, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import httpx
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

from translations import FACTS, LANGUAGES, TEXT, WEATHER_DESC, WEEKDAYS, WMO_CODE_MAP

# ---------------------------------------------------------------------------
# Настройка логирования
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Необязательный прокси для доступа к Telegram (если api.telegram.org
# заблокирован/недоступен у вашего провайдера напрямую).
# Пример значения в .env: PROXY_URL=socks5://127.0.0.1:1080
# или PROXY_URL=http://127.0.0.1:8080
PROXY_URL = os.getenv("PROXY_URL")

LANG_FILE = Path(__file__).parent / "users_lang.json"
SETTINGS_FILE = Path(__file__).parent / "users_settings.json"

# Часовой пояс, в котором пользователи указывают время рассылки (Ташкент, UTC+5)
TASHKENT_TZ = timezone(timedelta(hours=5))

# Валюты, которые показываем
TARGET_CURRENCIES = ["UZS", "RUB", "EUR", "KRW", "AED", "USD", "UAH", "CNY", "KZT", "GBP", "TRY"]

# Соответствие обозначений/слов -> ISO-код валюты (для распознавания сумм типа "10$")
CURRENCY_ALIASES = {
    "$": "USD", "usd": "USD", "дол": "USD", "доллар": "USD", "доллара": "USD",
    "долларов": "USD", "баксов": "USD", "dollar": "USD", "dollars": "USD",
    "€": "EUR", "eur": "EUR", "евро": "EUR", "euro": "EUR",
    "₽": "RUB", "rub": "RUB", "руб": "RUB", "рубль": "RUB", "рубля": "RUB",
    "рублей": "RUB", "р": "RUB",
    "uzs": "UZS", "сум": "UZS", "сума": "UZS", "сумов": "UZS",
    "som": "UZS", "so'm": "UZS", "sum": "UZS", "soum": "UZS",
    "₩": "KRW", "krw": "KRW", "вон": "KRW", "вона": "KRW", "won": "KRW",
    "aed": "AED", "дирхам": "AED", "дирхама": "AED", "дирхамов": "AED", "dirham": "AED",
    "uah": "UAH", "₴": "UAH", "гривна": "UAH", "гривны": "UAH", "гривен": "UAH",
    "гривны": "UAH", "hryvnia": "UAH",
    "cny": "CNY", "¥": "CNY", "юань": "CNY", "юаня": "CNY", "юаней": "CNY",
    "yuan": "CNY", "rmb": "CNY",
    "kzt": "KZT", "тенге": "KZT", "tenge": "KZT",
    "gbp": "GBP", "£": "GBP", "фунт": "GBP", "фунтов": "GBP", "фунта": "GBP",
    "pound": "GBP", "pounds": "GBP",
    "try": "TRY", "₺": "TRY", "лира": "TRY", "лир": "TRY", "лиры": "TRY", "lira": "TRY",
}

_CURRENCY_SYMBOLS = r"\$€₽₩£₴¥₺"
_AMOUNT_BEFORE_RE = re.compile(
    rf"^(\d+(?:[.,]\d+)?)\s*([a-zа-яё'\.]+|[{_CURRENCY_SYMBOLS}])$", re.IGNORECASE
)
_SYMBOL_BEFORE_RE = re.compile(rf"^([{_CURRENCY_SYMBOLS}])\s*(\d+(?:[.,]\d+)?)$")

# Формат времени для /notify: ЧЧ:ММ
_TIME_RE = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")

# Состояния ожидания ввода от пользователя (какой город он вводит и зачем)
WAITING_CITY_USERS = set()           # ждём город для показа текущей погоды
WAITING_FORECAST_CITY_USERS = set()  # ждём город для прогноза на неделю
WAITING_CITY_FOR_SAVE_USERS = set()  # ждём город, чтобы сохранить как "мой город"


def parse_amount_currency(text: str):
    """Пытается распознать сумму с валютой в свободном тексте.
    Возвращает (amount: float, currency_code: str) или None."""
    text = text.strip().lower()

    m = _SYMBOL_BEFORE_RE.match(text)
    if m:
        symbol, amount = m.group(1), m.group(2)
        code = CURRENCY_ALIASES.get(symbol)
        if code:
            return float(amount.replace(",", ".")), code

    m = _AMOUNT_BEFORE_RE.match(text)
    if m:
        amount, token = m.group(1), m.group(2)
        code = CURRENCY_ALIASES.get(token)
        if code:
            return float(amount.replace(",", ".")), code

    return None


# ---------------------------------------------------------------------------
# Хранение настроек пользователя (простые JSON-файлы)
# ---------------------------------------------------------------------------
def _load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


USER_LANGS = _load_json(LANG_FILE)
USER_SETTINGS = _load_json(SETTINGS_FILE)  # {user_id: {"city": str|None, "notify_time": "HH:MM"|None}}


def get_lang(user_id: int) -> str:
    return USER_LANGS.get(str(user_id), "ru")


def set_lang(user_id: int, lang: str) -> None:
    USER_LANGS[str(user_id)] = lang
    _save_json(LANG_FILE, USER_LANGS)


def t(user_id: int, key: str) -> str:
    lang = get_lang(user_id)
    return TEXT[lang][key]


def _user_settings(user_id: int) -> dict:
    return USER_SETTINGS.setdefault(str(user_id), {"city": None, "notify_time": None})


def get_city(user_id: int):
    return _user_settings(user_id).get("city")


def set_city(user_id: int, city: str) -> None:
    _user_settings(user_id)["city"] = city
    _save_json(SETTINGS_FILE, USER_SETTINGS)


def get_notify_time(user_id: int):
    return _user_settings(user_id).get("notify_time")


def set_notify_time(user_id: int, value):
    _user_settings(user_id)["notify_time"] = value
    _save_json(SETTINGS_FILE, USER_SETTINGS)


# ---------------------------------------------------------------------------
# Клавиатуры
# ---------------------------------------------------------------------------
def language_inline_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(name, callback_data=f"setlang:{code}")
        for code, name in LANGUAGES.items()
    ]
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(rows)


def main_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = get_lang(user_id)
    txt = TEXT[lang]
    keyboard = [
        [txt["menu_weather"], txt["menu_forecast"]],
        [txt["menu_currency"], txt["menu_crypto"]],
        [txt["menu_mycity"], txt["menu_notify"]],
        [txt["menu_fact"], txt["menu_language"]],
        [txt["menu_help"]],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ---------------------------------------------------------------------------
# Внешние API (без ключей): Open-Meteo, open.er-api.com, Binance, Nominatim
# ---------------------------------------------------------------------------
async def _geocode_open_meteo(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "ru", "format": "json"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    logger.info("Open-Meteo geocode('%s') -> %s", city, data)
    results = data.get("results")
    if not results:
        return None
    r = results[0]
    return {
        "lat": r["latitude"],
        "lon": r["longitude"],
        "name": r.get("name", city),
        "country": r.get("country", ""),
    }


async def _geocode_nominatim(city: str):
    """Запасной геокодер через OpenStreetMap Nominatim, если Open-Meteo
    ничего не нашёл или недоступен."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1, "accept-language": "ru"}
    headers = {"User-Agent": "weather-currency-telegram-bot/1.0"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    logger.info("Nominatim geocode('%s') -> %s", city, data)
    if not data:
        return None
    r = data[0]
    display_name = r.get("display_name", city)
    name = display_name.split(",")[0].strip()
    return {
        "lat": float(r["lat"]),
        "lon": float(r["lon"]),
        "name": name,
        "country": display_name.split(",")[-1].strip() if "," in display_name else "",
    }


async def geocode_city(city: str):
    """Находит координаты города. Сначала пробует Open-Meteo, при неудаче —
    запасной вариант через Nominatim (OpenStreetMap)."""
    try:
        geo = await _geocode_open_meteo(city)
        if geo:
            return geo
    except Exception as e:
        logger.warning("Open-Meteo geocoding упал для '%s': %s", city, e)

    try:
        geo = await _geocode_nominatim(city)
        if geo:
            return geo
    except Exception as e:
        logger.warning("Nominatim geocoding упал для '%s': %s", city, e)

    return None


async def fetch_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("current", {})


async def fetch_forecast(lat: float, lon: float):
    """7-дневный прогноз (макс/мин температура + код погоды на каждый день)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": "auto",
        "forecast_days": 7,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("daily", {})


async def fetch_currency_rates():
    """Бесплатный API без ключа: базовая валюта USD."""
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        rates = data.get("rates", {})
        logger.info("Currency rates fetched: %d валют", len(rates))
        return rates
    except Exception as e:
        logger.error("fetch_currency_rates failed: %s", e)
        return {}


async def _fetch_crypto_binance():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbols": '["BTCUSDT","ETHUSDT"]'}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    result = {}
    for item in data:
        if item.get("symbol") == "BTCUSDT":
            result["bitcoin"] = {"usd": float(item["price"])}
        elif item.get("symbol") == "ETHUSDT":
            result["ethereum"] = {"usd": float(item["price"])}
    return result


async def _fetch_crypto_coincap():
    """Запасной источник — CoinCap. Binance иногда блокирует запросы
    с серверов в США (а бесплатные сервера Render часто там и находятся)."""
    result = {}
    async with httpx.AsyncClient(timeout=10) as client:
        for asset_id, key in [("bitcoin", "bitcoin"), ("ethereum", "ethereum")]:
            resp = await client.get(f"https://api.coincap.io/v2/assets/{asset_id}")
            resp.raise_for_status()
            price = resp.json().get("data", {}).get("priceUsd")
            if price:
                result[key] = {"usd": float(price)}
    return result


async def fetch_crypto_rates():
    """Курс BTC/ETH в USD. Сначала пробуем Binance, при неудаче — CoinCap
    (Binance иногда недоступен с серверов в США, где часто размещён Render)."""
    try:
        result = await _fetch_crypto_binance()
        if result:
            logger.info("Crypto rates fetched (Binance): %s", result)
            return result
    except Exception as e:
        logger.warning("Binance crypto fetch упал: %s", e)

    try:
        result = await _fetch_crypto_coincap()
        if result:
            logger.info("Crypto rates fetched (CoinCap): %s", result)
            return result
    except Exception as e:
        logger.error("CoinCap crypto fetch тоже упал: %s", e)

    return {}


# ---------------------------------------------------------------------------
# Формирование текстовых сообщений (переиспользуются командами и рассылкой)
# ---------------------------------------------------------------------------
async def compute_weather_message(lang: str, city: str):
    geo = await geocode_city(city)
    if not geo:
        return None
    current = await fetch_weather(geo["lat"], geo["lon"])
    code = current.get("weather_code", -1)
    desc = WEATHER_DESC[lang][WMO_CODE_MAP.get(code, "unknown")]
    txt = TEXT[lang]
    location_label = geo["name"] + (f", {geo['country']}" if geo["country"] else "")
    return (
        f"{txt['weather_in'].format(city=location_label)}\n\n"
        f"{desc}\n"
        f"{txt['temp']}: {current.get('temperature_2m', '?')}°C\n"
        f"{txt['feels']}: {current.get('apparent_temperature', '?')}°C\n"
        f"{txt['wind']}: {current.get('wind_speed_10m', '?')} км/ч\n"
        f"{txt['humidity']}: {current.get('relative_humidity_2m', '?')}%"
    )


async def compute_forecast_message(lang: str, city: str):
    geo = await geocode_city(city)
    if not geo:
        return None
    daily = await fetch_forecast(geo["lat"], geo["lon"])
    txt = TEXT[lang]
    location_label = geo["name"] + (f", {geo['country']}" if geo["country"] else "")
    lines = [txt["forecast_in"].format(city=location_label), ""]

    dates = daily.get("time", [])
    codes = daily.get("weather_code", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])

    for i, date_str in enumerate(dates):
        try:
            weekday_name = WEEKDAYS[lang][datetime.strptime(date_str, "%Y-%m-%d").weekday()]
        except Exception:
            weekday_name = date_str
        desc = WEATHER_DESC[lang][WMO_CODE_MAP.get(codes[i] if i < len(codes) else -1, "unknown")]
        max_t = tmax[i] if i < len(tmax) else "?"
        min_t = tmin[i] if i < len(tmin) else "?"
        lines.append(f"{weekday_name} ({date_str}): {desc}  {min_t}°...{max_t}°C")

    return "\n".join(lines)


async def compute_currency_message(lang: str):
    rates = await fetch_currency_rates()
    if not rates:
        return None
    txt = TEXT[lang]
    lines = [txt["currency_title"], "", "1 USD ="]
    for cur in TARGET_CURRENCIES:
        if cur == "USD" or cur not in rates:
            continue
        lines.append(f"  {rates[cur]:.2f} {cur}")

    eur_rate = rates.get("EUR")
    if eur_rate:
        usd_per_eur = 1 / eur_rate
        lines.append("\n1 EUR =")
        for cur in ["UZS", "RUB", "USD", "KRW", "AED"]:
            if cur in rates:
                lines.append(f"  {rates[cur] * usd_per_eur:.2f} {cur}")
    return "\n".join(lines)


async def compute_crypto_message(lang: str):
    data = await fetch_crypto_rates()
    if not data:
        return None
    rates = await fetch_currency_rates()
    txt = TEXT[lang]
    lines = [txt["crypto_title"], ""]

    btc = data.get("bitcoin", {}).get("usd")
    eth = data.get("ethereum", {}).get("usd")

    if btc:
        lines.append(f"₿ Bitcoin (BTC): ${btc:,.0f}")
        if rates:
            if "RUB" in rates:
                lines.append(f"    ≈ {btc * rates['RUB']:,.0f} RUB")
            if "UZS" in rates:
                lines.append(f"    ≈ {btc * rates['UZS']:,.0f} UZS")
    if eth:
        lines.append(f"\nΞ Ethereum (ETH): ${eth:,.0f}")
        if rates:
            if "RUB" in rates:
                lines.append(f"    ≈ {eth * rates['RUB']:,.0f} RUB")
            if "UZS" in rates:
                lines.append(f"    ≈ {eth * rates['UZS']:,.0f} UZS")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Хендлеры команд
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if str(user_id) not in USER_LANGS:
        await update.message.reply_text(
            TEXT["ru"]["welcome"], reply_markup=language_inline_keyboard()
        )
    else:
        await update.message.reply_text(
            t(user_id, "welcome").split("\n\n")[0],
            reply_markup=main_menu_keyboard(user_id),
        )


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 " + "/".join(LANGUAGES.values()), reply_markup=language_inline_keyboard()
    )


async def set_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split(":")[1]
    user_id = query.from_user.id
    set_lang(user_id, lang_code)
    await query.edit_message_text(TEXT[lang_code]["lang_set"])
    await context.bot.send_message(
        chat_id=user_id,
        text=TEXT[lang_code]["help"],
        reply_markup=main_menu_keyboard(user_id),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(t(user_id, "help"), reply_markup=main_menu_keyboard(user_id))


# --- Погода -----------------------------------------------------------------
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        await send_weather(update, user_id, " ".join(context.args))
        return
    saved_city = get_city(user_id)
    if saved_city:
        await send_weather(update, user_id, saved_city)
    else:
        WAITING_CITY_USERS.add(user_id)
        await update.message.reply_text(t(user_id, "ask_city"))


async def send_weather(update: Update, user_id: int, city: str):
    lang = get_lang(user_id)
    loading_msg = await update.message.reply_text(t(user_id, "loading"))
    try:
        message = await compute_weather_message(lang, city)
        await loading_msg.edit_text(message or t(user_id, "city_not_found"))
    except Exception as e:
        logger.exception("Weather fetch failed: %s", e)
        await loading_msg.edit_text(t(user_id, "error"))


# --- Прогноз на неделю --------------------------------------------------------
async def forecast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        await send_forecast(update, user_id, " ".join(context.args))
        return
    saved_city = get_city(user_id)
    if saved_city:
        await send_forecast(update, user_id, saved_city)
    else:
        WAITING_FORECAST_CITY_USERS.add(user_id)
        await update.message.reply_text(t(user_id, "ask_city"))


async def send_forecast(update: Update, user_id: int, city: str):
    lang = get_lang(user_id)
    loading_msg = await update.message.reply_text(t(user_id, "loading"))
    try:
        message = await compute_forecast_message(lang, city)
        await loading_msg.edit_text(message or t(user_id, "city_not_found"))
    except Exception as e:
        logger.exception("Forecast fetch failed: %s", e)
        await loading_msg.edit_text(t(user_id, "error"))


# --- Курс валют / конвертер ---------------------------------------------------
async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    loading_msg = await update.message.reply_text(t(user_id, "loading"))
    try:
        message = await compute_currency_message(get_lang(user_id))
        await loading_msg.edit_text(message or t(user_id, "error"))
    except Exception as e:
        logger.exception("Currency fetch failed: %s", e)
        await loading_msg.edit_text(t(user_id, "error"))


async def send_conversion(update: Update, user_id: int, amount: float, currency_code: str):
    lang = get_lang(user_id)
    loading_msg = await update.message.reply_text(t(user_id, "loading"))
    try:
        rates = await fetch_currency_rates()
        if not rates or currency_code not in rates:
            await loading_msg.edit_text(t(user_id, "error"))
            return

        amount_in_usd = amount if currency_code == "USD" else amount / rates[currency_code]
        amount_str = f"{amount:,.0f}" if amount == int(amount) else f"{amount:,.2f}"
        title = TEXT[lang]["convert_title"].format(amount=amount_str, currency=currency_code)
        lines = [title, ""]
        for cur in TARGET_CURRENCIES:
            if cur == currency_code or cur not in rates:
                continue
            value = amount_in_usd * rates[cur]
            lines.append(f"  {value:,.2f} {cur}")

        await loading_msg.edit_text("\n".join(lines))
    except Exception as e:
        logger.exception("Conversion failed: %s", e)
        await loading_msg.edit_text(t(user_id, "error"))


# --- Крипто ------------------------------------------------------------------
async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    loading_msg = await update.message.reply_text(t(user_id, "loading"))
    try:
        message = await compute_crypto_message(get_lang(user_id))
        await loading_msg.edit_text(message or t(user_id, "error"))
    except Exception as e:
        logger.exception("Crypto fetch failed: %s", e)
        await loading_msg.edit_text(t(user_id, "error"))


# --- Факт дня ------------------------------------------------------------------
async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    fact = random.choice(FACTS[lang])
    await update.message.reply_text(fact)


# --- Мой город (по умолчанию) -------------------------------------------------
async def save_city(update: Update, user_id: int, city: str):
    loading_msg = await update.message.reply_text(t(user_id, "loading"))
    try:
        geo = await geocode_city(city)
        if not geo:
            await loading_msg.edit_text(t(user_id, "city_not_found"))
            return
        label = geo["name"] + (f", {geo['country']}" if geo["country"] else "")
        set_city(user_id, label)
        await loading_msg.edit_text(t(user_id, "mycity_saved").format(city=label))
    except Exception as e:
        logger.exception("Save city failed: %s", e)
        await loading_msg.edit_text(t(user_id, "error"))


async def mycity_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = getattr(context, "args", None)
    if args:
        await save_city(update, user_id, " ".join(args))
        return

    current = get_city(user_id)
    if current:
        await update.message.reply_text(t(user_id, "mycity_current").format(city=current))
    else:
        await update.message.reply_text(t(user_id, "mycity_none"))
    WAITING_CITY_FOR_SAVE_USERS.add(user_id)


# --- Ежедневная рассылка ------------------------------------------------------
def _notify_job_name(user_id: int) -> str:
    return f"notify_{user_id}"


def schedule_notify_job(application: Application, user_id: int, hour: int, minute: int) -> None:
    if application.job_queue is None:
        logger.warning("JobQueue недоступен — рассылка не будет работать. "
                        "Установите зависимость: pip install \"python-telegram-bot[job-queue]\"")
        return
    job_name = _notify_job_name(user_id)
    for job in application.job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()
    application.job_queue.run_daily(
        send_daily_notification,
        time=dt_time(hour=hour, minute=minute, tzinfo=TASHKENT_TZ),
        name=job_name,
        data={"user_id": user_id},
    )


def remove_notify_job(application: Application, user_id: int) -> None:
    if application.job_queue is None:
        return
    for job in application.job_queue.get_jobs_by_name(_notify_job_name(user_id)):
        job.schedule_removal()


async def send_daily_notification(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data["user_id"]
    lang = get_lang(user_id)
    txt = TEXT[lang]
    parts = [txt["notify_header"], ""]

    city = get_city(user_id)
    if city:
        try:
            weather_msg = await compute_weather_message(lang, city)
            if weather_msg:
                parts.append(weather_msg)
                parts.append("")
        except Exception as e:
            logger.exception("Daily weather failed for %s: %s", user_id, e)

    try:
        currency_msg = await compute_currency_message(lang)
        if currency_msg:
            parts.append(currency_msg)
    except Exception as e:
        logger.exception("Daily currency failed for %s: %s", user_id, e)

    try:
        await context.bot.send_message(chat_id=user_id, text="\n".join(parts))
    except Exception as e:
        logger.exception("Failed to send daily notification to %s: %s", user_id, e)


async def notify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = getattr(context, "args", None)

    if not args:
        await update.message.reply_text(t(user_id, "notify_usage"))
        return

    arg = args[0].strip().lower()
    if arg == "off":
        remove_notify_job(context.application, user_id)
        set_notify_time(user_id, None)
        await update.message.reply_text(t(user_id, "notify_off"))
        return

    m = _TIME_RE.match(arg)
    if not m:
        await update.message.reply_text(t(user_id, "notify_bad_format"))
        return

    hour, minute = int(m.group(1)), int(m.group(2))
    time_str = f"{hour:02d}:{minute:02d}"
    set_notify_time(user_id, time_str)
    schedule_notify_job(context.application, user_id, hour, minute)
    await update.message.reply_text(t(user_id, "notify_set").format(time=time_str))


# ---------------------------------------------------------------------------
# Обработка текстовых сообщений (кнопки главного меню + свободный ввод)
# ---------------------------------------------------------------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    lang = get_lang(user_id)
    txt = TEXT[lang]

    if user_id in WAITING_CITY_FOR_SAVE_USERS:
        WAITING_CITY_FOR_SAVE_USERS.discard(user_id)
        await save_city(update, user_id, text)
        return

    if user_id in WAITING_FORECAST_CITY_USERS:
        WAITING_FORECAST_CITY_USERS.discard(user_id)
        await send_forecast(update, user_id, text)
        return

    if user_id in WAITING_CITY_USERS:
        WAITING_CITY_USERS.discard(user_id)
        await send_weather(update, user_id, text)
        return

    if text == txt["menu_weather"]:
        saved_city = get_city(user_id)
        if saved_city:
            await send_weather(update, user_id, saved_city)
        else:
            WAITING_CITY_USERS.add(user_id)
            await update.message.reply_text(txt["ask_city"])
    elif text == txt["menu_forecast"]:
        saved_city = get_city(user_id)
        if saved_city:
            await send_forecast(update, user_id, saved_city)
        else:
            WAITING_FORECAST_CITY_USERS.add(user_id)
            await update.message.reply_text(txt["ask_city"])
    elif text == txt["menu_currency"]:
        await currency_command(update, context)
    elif text == txt["menu_crypto"]:
        await crypto_command(update, context)
    elif text == txt["menu_fact"]:
        await fact_command(update, context)
    elif text == txt["menu_mycity"]:
        await mycity_command(update, context)
    elif text == txt["menu_notify"]:
        await update.message.reply_text(txt["notify_usage"])
    elif text == txt["menu_language"]:
        await language_command(update, context)
    elif text == txt["menu_help"]:
        await help_command(update, context)
    else:
        parsed = parse_amount_currency(text)
        if parsed:
            amount, currency_code = parsed
            await send_conversion(update, user_id, amount, currency_code)
        else:
            # Иначе считаем, что это может быть название города
            await send_weather(update, user_id, text)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------
def restore_notify_jobs(application: Application) -> None:
    """После рестарта сервиса (например, редеплоя на Render) заново
    ставим в очередь все ежедневные рассылки, сохранённые в users_settings.json."""
    if application.job_queue is None:
        return
    restored = 0
    for user_id_str, settings in USER_SETTINGS.items():
        notify_time = settings.get("notify_time")
        if not notify_time:
            continue
        try:
            hour, minute = map(int, notify_time.split(":"))
        except Exception:
            continue
        schedule_notify_job(application, int(user_id_str), hour, minute)
        restored += 1
    if restored:
        logger.info("Восстановлено рассылок после перезапуска: %d", restored)


class _HealthCheckHandler(BaseHTTPRequestHandler):
    """Простейший HTTP-обработчик, чтобы Render (Web Service) видел
    открытый порт и не считал деплой зависшим. Сам бот при этом
    продолжает работать через polling, а не через этот сервер."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Бот работает ✅".encode("utf-8"))

    def log_message(self, format, *args):
        pass  # не засоряем логи HTTP-запросами health-check


def start_health_check_server():
    """Запускает мини-сервер в отдельном потоке на порту из переменной
    окружения PORT (Render передаёт её автоматически для Web Service).
    Если PORT не задан (например, при локальном запуске) — сервер не нужен."""
    port_str = os.getenv("PORT")
    if not port_str:
        return
    port = int(port_str)
    server = HTTPServer(("0.0.0.0", port), _HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info("Health-check сервер запущен на порту %d (для Render Web Service)", port)


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Создайте файл .env (см. .env.example) "
            "и укажите там токен от @BotFather."
        )

    start_health_check_server()

    builder = Application.builder().token(BOT_TOKEN)

    if PROXY_URL:
        logger.info("Использую прокси для подключения к Telegram: %s", PROXY_URL)
        request = HTTPXRequest(proxy=PROXY_URL, connect_timeout=15, read_timeout=15)
        get_updates_request = HTTPXRequest(proxy=PROXY_URL, connect_timeout=15, read_timeout=15)
        builder = builder.request(request).get_updates_request(get_updates_request)

    application = builder.build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("forecast", forecast_command))
    application.add_handler(CommandHandler("currency", currency_command))
    application.add_handler(CommandHandler("crypto", crypto_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("mycity", mycity_command))
    application.add_handler(CommandHandler("notify", notify_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CallbackQueryHandler(set_language_callback, pattern=r"^setlang:"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    restore_notify_jobs(application)

    logger.info("Бот запущен, ожидаю сообщения...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
