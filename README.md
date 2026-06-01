# 💊 Meds Reminder Bot — Setup Guide

## Step 1: Get a Bot Token (safe & free)

1. Go to https://discord.com/developers/applications
2. Click **New Application** → give it any name
3. Go to **Bot** tab → click **Reset Token** → copy the token
4. Scroll down → enable **Message Content Intent**
5. Go to **OAuth2 → URL Generator**
   - Scopes: `bot`
   - Permissions: `Send Messages`
   - Open the generated URL → add bot to your server

## Step 2: Get the Target User ID

1. Open Discord → Settings → Advanced → Enable **Developer Mode**
2. Right-click the person you want to DM → **Copy User ID**

## Step 3: Deploy to Railway

1. Go to https://github.com → New Repository → name it `meds-reminder`
2. Upload all 3 files: `meds_reminder.py`, `requirements.txt`, `railway.toml`
3. Go to https://railway.app → Login with GitHub
4. New Project → Deploy from GitHub → select `meds-reminder`
5. Go to **Variables** tab and add:
   - `TOKEN` = your bot token
   - `USER_ID` = the target user's ID
6. Click **Deploy** ✅

## Schedule
Bot sends "Meds in X mins (TIME) 💊" before:
- 2:00 PM
- 4:00 PM
- 6:00 PM
- 10:00 PM

Each day the offset (5–15 mins early) is randomized uniquely per slot.
