# 🇯🇵 福岡・岡山 旅行計畫 2026

私人旅行行程網頁，含 Telegram 自動推播提醒。

## 🔗 連結

- **行程網頁**：[doralu1023.github.io/caps-p-fukuoka-2026](https://doralu1023.github.io/caps-p-fukuoka-2026)
- **Telegram Channel**：[t.me/CapsPFukuoka2026Channel](https://t.me/CapsPFukuoka2026Channel)

## ✈️ 行程概覽

| 日期 | 行程 |
|------|------|
| 5/8（五）| 抵達福岡・博多拉麵宵夜 |
| 5/9（六）| 岡山 Hello Kitty 展・倉敷美觀地區 |
| 5/10（日）| 廣島・宮島嚴島神社・彌山纜車 |
| 5/11（一）| 門司港レトロ・下關唐戶市場 |
| 5/12（二）| 太宰府天滿宮・柳川川下り |
| 5/13（三）| 博多伴手禮・回台灣 |

## 📁 檔案結構

```
├── index.html              # 主頁行程總覽
├── days/
│   ├── shared.css          # 共用樣式
│   ├── 508.html            # 5/8 詳細行程
│   ├── 509.html            # 5/9 詳細行程
│   ├── 510.html            # 5/10 詳細行程
│   ├── 511.html            # 5/11 詳細行程
│   ├── 512.html            # 5/12 詳細行程
│   └── 513.html            # 5/13 詳細行程
├── scripts/
│   └── notify.py           # Telegram 推播腳本
└── .github/
    └── workflows/
        └── notify.yml      # GitHub Actions 排程
```

## 🔔 Telegram 推播

GitHub Actions 每小時執行一次，自動判斷推送時機：

- **每晚 21:00 JST**：推送隔天行程預告
- **出發前 1 小時**：推送當天出發提醒

### 手動測試推播

前往 [Actions](../../actions) → **Telegram Travel Notifications** → **Run workflow**

## ⚙️ 環境變數

在 GitHub repo 的 Settings → Secrets and variables → Actions 設定：

| Secret | 說明 |
|--------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `TELEGRAM_CHANNEL_ID` | Channel ID（格式：`-100xxxxxxxxxx`）|