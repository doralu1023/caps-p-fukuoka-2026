#!/usr/bin/env python3
"""
Telegram 推播腳本 — 福岡旅行 2026
推送時機：每天晚上21:00（前一天提醒）+ 當天早上出發前1小時
"""

import os
import requests
from datetime import datetime, date
import pytz

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]
JST = pytz.timezone("Asia/Tokyo")

ITINERARY = {
    "2026-05-08": {
        "title": "Day 1 🛬 抵達福岡",
        "evening_alert": (
            "🗓 *明天出發了！*\n\n"
            "✈️ IT720 明天 *14:30* 桃園出發\n"
            "🛬 *17:55* 抵達福岡機場\n"
            "🚇 地鐵2站到博多站（約5分）\n"
            "🍜 晚上去博多吃拉麵！\n\n"
            "📋 記得帶：護照、JR Pass（Klook憑證）、日圓現金"
        ),
        "morning_alert": None,
    },
    "2026-05-09": {
        "title": "Day 2 🎀 岡山・凱蒂貓展・倉敷",
        "evening_alert": (
            "🗓 *明天：岡山・凱蒂貓展・倉敷*\n\n"
            "⏰ 明天 *6:59* 博多出發（さくら740號）\n"
            "🎀 Hello Kitty展 *9:00* 開門，*8:30* 到門口排隊\n"
            "🏛 倉敷美觀地區下午散策\n"
            "🍺 晚餐：星屋食堂（倉敷）\n\n"
            "💡 JR Pass 今天啟用第1天！請先去窗口劃指定席"
        ),
        "morning_alert": (
            "⏰ *出發提醒：6:59 さくら740號*\n\n"
            "🚅 博多 → 岡山（1小時51分）\n"
            "📍 出發前請確認：JR Pass + 護照\n"
            "🎀 8:30 到美術館門口排隊！"
        ),
        "depart_hour": 6,
    },
    "2026-05-10": {
        "title": "Day 3 🕊 廣島・宮島",
        "evening_alert": (
            "🗓 *明天：廣島・宮島*\n\n"
            "⏰ 明天 *7:00* 博多出發（新幹線，約45分到廣島）\n"
            "🕊 原爆ドーム + 平和記念博物館（¥200）\n"
            "🦪 午餐：廣島牡蠣\n"
            "⛩ 嚴島神社 + 宮島纜車上彌山\n"
            "🐟 晚餐：宮島口穴子飯\n\n"
            "💡 JR Pass 第2天，宮島渡輪也包含在內"
        ),
        "morning_alert": (
            "⏰ *出發提醒：7:00 新幹線*\n\n"
            "🚅 博多 → 廣島（約45分）\n"
            "📍 JR Pass 第2天啟用\n"
            "🕊 8:30 到原爆ドーム"
        ),
        "depart_hour": 7,
    },
    "2026-05-11": {
        "title": "Day 4 🏛 門司港・下關",
        "evening_alert": (
            "🗓 *明天：門司港・下關*\n\n"
            "⏰ 明天 *9:00* 博多出發\n"
            "🏛 門司港レトロ展望室（¥300）\n"
            "🍛 午餐：ukiwa 焼きカレー（不用排隊）\n"
            "⛴ 渡輪到下關（補票¥200）唐戶市場吃河豚壽司\n"
            "☕ cafe liberté 看關門海峽\n\n"
            "💡 JR Pass 第3天！門司港→下關渡輪需另外補票"
        ),
        "morning_alert": (
            "⏰ *出發提醒：9:00 新幹線*\n\n"
            "🚅 博多 → 小倉 → 門司港\n"
            "📍 JR Pass 第3天\n"
            "💡 別忘了帶零錢，下關渡輪¥200"
        ),
        "depart_hour": 9,
    },
    "2026-05-12": {
        "title": "Day 5 ⛩ 太宰府・柳川",
        "evening_alert": (
            "🗓 *明天：太宰府・柳川*\n\n"
            "⏰ 明天 *8:30* 天神出發（西鐵）\n"
            "⛩ 太宰府天滿宮 + 梅枝餅\n"
            "🚤 柳川川下り（約40分，¥2,000）\n"
            "🐟 午餐：鰻魚せいろ蒸し\n"
            "🍲 晚餐：もつ鍋一藤 博多店（有訂位嗎？）\n\n"
            "💡 今天用西鐵，JR Pass不需要。建議買西鐵套票"
        ),
        "morning_alert": (
            "⏰ *出發提醒：8:30 西鐵天神*\n\n"
            "🚃 天神 → 二日市 → 太宰府（約45分）\n"
            "⛩ 9:30 太宰府天滿宮\n"
            "💡 今天用西鐵，記得帶IC卡或現金"
        ),
        "depart_hour": 8,
    },
    "2026-05-13": {
        "title": "Day 6 ✈️ 最後一天・回台",
        "evening_alert": (
            "🗓 *明天：最後一天，回台灣！*\n\n"
            "🏨 退房 + 行李寄放\n"
            "🛍 マイング + KITTE 博多掃伴手禮\n"
            "🍽 最後一餐：博多いねや or Torimabushi\n"
            "✈️ IT721 *18:55* 福岡出發\n"
            "📍 *17:30 前*到福岡機場！\n\n"
            "💡 明太子、博多通りもん、ひよ子⋯別忘了！"
        ),
        "morning_alert": (
            "✈️ *今天回台灣！*\n\n"
            "⏰ IT721 18:55 福岡出發\n"
            "📍 *17:30 必須在機場*\n"
            "🚇 博多站→福岡空港 約5分鐘（¥260）\n\n"
            "🛍 伴手禮清單：\n"
            "• 明太子 辛子めんたいこ\n"
            "• 博多通りもん\n"
            "• ひよ子\n\n"
            "お疲れ様でした！いい旅を！🇯🇵"
        ),
        "depart_hour": 15,
    },
}


def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    print(f"✅ Sent: {text[:50]}...")


def main():
    now = datetime.now(JST)
    today_str = now.strftime("%Y-%m-%d")
    hour = now.hour

    # 找明天的行程（晚上21:00提醒）
    from datetime import timedelta
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    if hour == 21:
        # 晚上21:00 → 推送明天的提醒
        if tomorrow in ITINERARY:
            day = ITINERARY[tomorrow]
            msg = f"🌙 *明日行程提醒*\n{day['title']}\n\n{day['evening_alert']}"
            send_message(msg)
        else:
            print(f"No itinerary for tomorrow: {tomorrow}")

    elif hour >= 5 and hour <= 10:
        # 早上 → 檢查當天是否需要出發提醒
        if today_str in ITINERARY:
            day = ITINERARY[today_str]
            if day.get("morning_alert") and day.get("depart_hour"):
                depart_hour = day["depart_hour"]
                # 出發前1小時推送
                if hour == depart_hour - 1:
                    msg = f"🌅 *今日出發提醒*\n{day['title']}\n\n{day['morning_alert']}"
                    send_message(msg)
    else:
        print(f"Not a notification hour: {hour}:00 JST")


if __name__ == "__main__":
    main()