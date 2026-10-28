# Telegram Enquiry Notifications — Setup Guide (हिंदी + English)

Nayi enquiry aate hi owner ke Telegram par message aa jata hai — naam, mobile, details
aur ek **WhatsApp reply-link** ke saath. Server (`server/server.js`) ye bhejta hai;
setup sirf 4 step, ~5 minute. Koi coding nahi.

> ⚠️ Bot token = password jaisa hai. Kabhi GitHub, website ya kisi chat me share NA karein.
> Sirf Render ke Environment variables me daalein.

---

## Step 1 — Bot banayein (BotFather se)

1. Telegram kholiye → search me likhiye: **@BotFather** (blue ✓ wala official).
2. Message bhejiye: `/newbot`
3. Bot ka **naam** dijiye, jaise: `Shri Maha Maya Hotel Alerts`
4. Bot ka **username** dijiye (ant me `bot` zaroori), jaise: `ShriMahaMayaPalluAlertsBot`
5. BotFather ek **TOKEN** dega, jaisa: `7234567890:AAExample...` — ise copy kar lijiye।

## Step 2 — Apni chat-id lijiye

1. Telegram me **@userinfobot** search kariye → `/start` bhejiye।
2. Wo aapki **Id** dikhayega, jaise `123456789` — copy kar lijiye। Yahi `TELEGRAM_CHAT_ID` hai।

*(Backup tarika: apne naye bot ko `/start` bhejiye, phir browser me kholiye:
`https://api.telegram.org/bot<TOKEN>/getUpdates` → `"chat":{"id": ...}` wali number.)*

## Step 3 — Render par 2 Environment Variables add karein

Render dashboard → apni service → **Environment** → *Add Environment Variable*:

| Key | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Step 1 wala token |
| `TELEGRAM_CHAT_ID` | Step 2 wali id |

Save karein → Render **apne aap redeploy** ho jayega (1–2 min)।

## Step 4 — Test karein

1. Telegram me apne naye bot ko ek baar **/start** bhejiye (jab tak aap ye nahi karte,
   bot aapko message nahi bhej sakta — ye Telegram ka rule hai)।
2. Website ke chat me ek test booking-enquiry poori kijiye।
3. 1–2 second me Telegram par aisa message aayega:

```
🏨 Nayi enquiry — Shri Maha Maya Hotel
Type: room  ·  Lang: hi  ·  Source: chat
👤 Name: Ram Sharma
📞 Mobile: 9950501306
📝 26 Oct ko deluxe chahiye, 2 log
🕒 2026-10-28T18:19:40Z
💬 Reply on WhatsApp: https://wa.me/919950501306
⚠️ Booking confirm tabhi jab hotel staff confirm kare.
```

---

## Rozmarra ka use / limits

- Notification **one-way alert** hai — reply guest ko aap apne phone ke WhatsApp/call se
  karte hain (message me diya wa.me link ek tap me guest ki chat khol deta hai)।
- Dashboard (`/admin/`) bhi pehle jaisa chalta rahega; Telegram sirf extra alert hai।
- Free limit ~30 messages/second — hotel ke liye kaafi se zyada।

## Troubleshooting

| Problem | Hal |
|---|---|
| Message nahi aaya | Bot ko ek baar `/start` bheja? Render me dono env vars sahi? |
| Token sahi hai ya nahi check karna hai | Browser: `https://api.telegram.org/bot<TOKEN>/getMe` → bot info dikhe |
| Render redeploy nahi hua | Service → *Manual Deploy* → “Deploy latest commit” |
| Env change ke baad bhi purana chal raha | Render free instance 1–2 min leta hai; phir naya test karein |
