import discord
import asyncio
import random
import os
from datetime import datetime
import pytz

# --- CONFIG (set these in Railway Variables) ---
TOKEN = os.environ.get("TOKEN", "your_bot_token_here")
TARGET_USER_ID = int(os.environ.get("USER_ID", "123456789"))

TIMEZONE = pytz.timezone("Asia/Kolkata")

# Target times (hour, display label)
SEND_TIMES = [
    (14, "2 PM"),
    (16, "4 PM"),
    (18, "6 PM"),
    (22, "10 PM"),
]

EARLY_OFFSET_MIN = 5
EARLY_OFFSET_MAX = 15

# Use discord.Client() for bot token
client = discord.Client()

async def human_type_and_send(channel, message):
    """Simulates human typing — pauses, bursts, realistic rhythm."""

    # Phase 1: thinking pause
    async with channel.typing():
        await asyncio.sleep(random.uniform(0.8, 1.5))

    await asyncio.sleep(random.uniform(0.3, 0.7))

    # Phase 2: typing with mid-pauses
    async with channel.typing():
        char_count = len(message)
        typing_time = char_count * random.uniform(0.08, 0.15)
        typing_time += random.uniform(0.5, 1.2)

        pauses = random.randint(1, 2)
        for _ in range(pauses):
            await asyncio.sleep(typing_time / (pauses + 1))
            await asyncio.sleep(random.uniform(0.2, 0.5))

        await asyncio.sleep(random.uniform(0.3, 0.6))

    # Phase 3: small gap before sending
    await asyncio.sleep(random.uniform(0.4, 1.0))

    await channel.send(message)
    print(f"[{datetime.now(TIMEZONE).strftime('%H:%M:%S')}] ✅ Sent: '{message}'")


def build_message(target_label, offset_used):
    return f"Meds in {offset_used} mins ({target_label}) 💊"


def get_randomized_times():
    """Every day picks UNIQUE random offsets per slot."""
    randomized = []
    used_offsets = []

    for hour, label in SEND_TIMES:
        while True:
            offset = random.randint(EARLY_OFFSET_MIN, EARLY_OFFSET_MAX)
            if offset not in used_offsets:
                used_offsets.append(offset)
                break

        actual_total = hour * 60 - offset
        actual_hour = actual_total // 60
        actual_minute = actual_total % 60
        randomized.append((actual_hour, actual_minute, label, offset))
        print(f"  📅 {label} → {actual_hour:02d}:{actual_minute:02d} ({offset} mins early)")

    return randomized


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    last_date = None
    scheduled_times = []
    sent_flags = []

    while True:
        now = datetime.now(TIMEZONE)
        today = now.date()

        if last_date != today:
            last_date = today
            print(f"\n📆 {today} — Today's schedule:")
            scheduled_times = get_randomized_times()
            sent_flags = [False] * len(scheduled_times)

        for i, (s_hour, s_minute, label, offset) in enumerate(scheduled_times):
            if (
                not sent_flags[i]
                and now.hour == s_hour
                and now.minute == s_minute
            ):
                user = await client.fetch_user(TARGET_USER_ID)
                dm_channel = await user.create_dm()
                msg = build_message(label, offset)
                await human_type_and_send(dm_channel, msg)
                sent_flags[i] = True

        await asyncio.sleep(30)


client.run(TOKEN)
