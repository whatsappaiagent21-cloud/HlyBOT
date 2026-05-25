"""
██╗  ██╗██╗  ██╗   ██╗██████╗  ██████╗ ████████╗
██║  ██║██║  ╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
███████║██║   ╚████╔╝ ██████╔╝██║   ██║   ██║
██╔══██║██║    ╚██╔╝  ██╔══██╗██║   ██║   ██║
██║  ██║███████╗██║   ██████╔╝╚██████╔╝   ██║
╚═╝  ╚═╝╚══════╝╚═╝   ╚═════╝  ╚═════╝    ╚═╝

HlyBOT — Bot Telegram tout-en-un
─────────────────────────────────────────────────
✅ Stats & détection d'activité
✅ Poster VIP automatique (mots-clés + activité)
✅ Anti-liens (escalade avertissement → ban)
✅ Bienvenue automatique
✅ FAQ / Commandes slash (/vip /regles /contact /resultats /aide)
─────────────────────────────────────────────────
"""

import asyncio
import json
import random
import re
import time
from collections import deque
from datetime import datetime

import redis as redis_lib
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import (
    BOT_TOKEN, GROUP_ID, REDIS_URL,
    ACTIVITY_THRESHOLD, ACTIVITY_WINDOW_SECS, COOLDOWN_VIP_MINS,
    VIP_KEYWORDS, VIP_MESSAGES,
    WELCOME_MESSAGE,
    FAQ_RESPONSES, ADMIN_ONLY_COMMANDS,
)

# ═══════════════════════════════════════════════════════════════════
#  REDIS
# ═══════════════════════════════════════════════════════════════════

_redis: redis_lib.Redis | None = None

def r() -> redis_lib.Redis:
    global _redis
    if _redis is None:
        _redis = redis_lib.from_url(REDIS_URL, decode_responses=True)
    return _redis

# ── Helpers Redis ────────────────────────────────────────────────

def stats_load() -> dict:
    raw = r().get("hlybot:stats")
    if raw:
        return json.loads(raw)
    return {
        "total_messages": 0,
        "daily": {},
        "hourly_distribution": {str(h): 0 for h in range(24)},
        "keyword_triggers": 0,
        "activity_triggers": 0,
        "vip_messages_sent": 0,
        "links_blocked": 0,
        "members_warned": {},
    }

def stats_save(s: dict):
    r().set("hlybot:stats", json.dumps(s))

def get_last_vip_sent() -> float:
    val = r().get("hlybot:vip:last_sent")
    return float(val) if val else 0.0

def set_last_vip_sent():
    r().set("hlybot:vip:last_sent", str(time.time()))

def get_last_vip_index() -> int:
    val = r().get("hlybot:vip:last_index")
    return int(val) if val else -1

def set_last_vip_index(idx: int):
    r().set("hlybot:vip:last_index", str(idx))

def get_warn(user_id: int) -> int:
    val = r().get(f"hlybot:warn:{user_id}")
    return int(val) if val else 0

def inc_warn(user_id: int) -> int:
    count = r().incr(f"hlybot:warn:{user_id}")
    r().expire(f"hlybot:warn:{user_id}", 60 * 60 * 24 * 7)
    return count

def reset_warn(user_id: int):
    r().delete(f"hlybot:warn:{user_id}")

# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════

LINK_PATTERN = re.compile(
    r"(https?://\S+|t\.me/\S+|@\w{5,}|www\.\S+|\b\w+\.(com|net|org|io|xyz|biz|gg)\b)",
    re.IGNORECASE,
)

# Fenêtre glissante locale (en mémoire, dans ce process)
_message_times: deque = deque()

WARN_TEXTS = [
    "⚠️ Les liens ne sont pas autorisés ici pour les membres.",
    "🚫 Deuxième avertissement — prochaine fois tu seras temporairement banni.",
    "❌ Dernier avertissement enregistré.",
]


async def check_is_admin(ctx: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    admins = await ctx.bot.get_chat_administrators(GROUP_ID)
    return user_id in {a.user.id for a in admins}


def pick_vip_message() -> tuple[int, str]:
    """Rotation intelligente — jamais le même message 2x de suite."""
    last = get_last_vip_index()
    indices = [i for i in range(len(VIP_MESSAGES)) if i != last]
    idx = random.choice(indices)
    set_last_vip_index(idx)
    return idx, VIP_MESSAGES[idx]


async def post_vip(bot: Bot, reason: str):
    idx, msg = pick_vip_message()
    await bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
    print(f"[HlyBOT][VIP] msg#{idx} envoyé | reason={reason} | {time.strftime('%H:%M:%S')}")


# ═══════════════════════════════════════════════════════════════════
#  HANDLER 1 — MESSAGES TEXTE
#  • Stats & activité
#  • Déclenchement VIP (activité + mots-clés)
#  • Anti-liens
# ═══════════════════════════════════════════════════════════════════

async def on_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg  = update.effective_message
    user = update.effective_user
    if not msg or not msg.text or not user:
        return

    now  = time.time()
    text = msg.text

    # ── 1. Stats ──────────────────────────────────────────────────
    s = stats_load()
    s["total_messages"] += 1
    today = str(datetime.now().date())
    s["daily"][today] = s["daily"].get(today, 0) + 1
    hour = str(datetime.now().hour)
    s["hourly_distribution"][hour] = s["hourly_distribution"].get(hour, 0) + 1
    stats_save(s)

    # ── 2. Score d'activité (fenêtre glissante) ───────────────────
    _message_times.append(now)
    cutoff = now - ACTIVITY_WINDOW_SECS
    while _message_times and _message_times[0] < cutoff:
        _message_times.popleft()
    activity_score = len(_message_times)

    # ── 3. Anti-liens ─────────────────────────────────────────────
    if LINK_PATTERN.search(text):
        if not await check_is_admin(ctx, user.id):
            try:
                await msg.delete()
            except Exception as e:
                print(f"[HlyBOT][ANTILIEN] delete error: {e}")
                return

            count = inc_warn(user.id)
            s = stats_load()
            s["links_blocked"] = s.get("links_blocked", 0) + 1
            s.setdefault("members_warned", {})[str(user.id)] = count
            stats_save(s)

            warn_txt = WARN_TEXTS[min(count - 1, len(WARN_TEXTS) - 1)]
            sent = await ctx.bot.send_message(
                chat_id=GROUP_ID,
                text=f"*{user.first_name}* — {warn_txt}",
                parse_mode=ParseMode.MARKDOWN,
            )
            await asyncio.sleep(12)
            try:
                await sent.delete()
            except Exception:
                pass

            if count >= 3:
                try:
                    await ctx.bot.ban_chat_member(GROUP_ID, user.id)
                    print(f"[HlyBOT][BAN] {user.first_name} ({user.id}) — 10 min")
                    await asyncio.sleep(600)
                    await ctx.bot.unban_chat_member(GROUP_ID, user.id)
                    reset_warn(user.id)
                    await ctx.bot.send_message(
                        chat_id=GROUP_ID,
                        text=f"*{user.first_name}* a été temporairement banni 10 min pour partage répété de liens.",
                        parse_mode=ParseMode.MARKDOWN,
                    )
                except Exception as e:
                    print(f"[HlyBOT][BAN ERROR] {e}")
            return  # message supprimé → pas de suite

    # ── 4. Déclenchement VIP ──────────────────────────────────────
    keyword_hit  = any(kw in text.lower() for kw in VIP_KEYWORDS)
    activity_hit = activity_score >= ACTIVITY_THRESHOLD
    cooldown_ok  = (now - get_last_vip_sent()) > (COOLDOWN_VIP_MINS * 60)

    if cooldown_ok and (keyword_hit or activity_hit):
        reason = "activité élevée" if activity_hit else "mot-clé détecté"
        set_last_vip_sent()

        s = stats_load()
        s["vip_messages_sent"] += 1
        if keyword_hit:
            s["keyword_triggers"] += 1
        else:
            s["activity_triggers"] += 1
        stats_save(s)

        await post_vip(ctx.bot, reason)


# ═══════════════════════════════════════════════════════════════════
#  HANDLER 2 — NOUVEAU MEMBRE → Bienvenue
# ═══════════════════════════════════════════════════════════════════

def _member_joined(update_cm) -> bool:
    old = update_cm.old_chat_member
    new = update_cm.new_chat_member
    if not old or not new:
        return False
    return (
        old.status in ("left", "kicked", "restricted") and
        new.status in ("member", "administrator", "creator")
    )


async def on_new_member(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not update.chat_member or not _member_joined(update.chat_member):
        return

    user = update.chat_member.new_chat_member.user
    name = user.first_name or "nouveau membre"

    try:
        sent = await ctx.bot.send_message(
            chat_id=GROUP_ID,
            text=WELCOME_MESSAGE.format(name=name),
            parse_mode=ParseMode.MARKDOWN,
        )
        print(f"[HlyBOT][WELCOME] {name} ({user.id})")
        await asyncio.sleep(60)
        try:
            await sent.delete()
        except Exception:
            pass
    except Exception as e:
        print(f"[HlyBOT][WELCOME ERROR] {e}")


# ═══════════════════════════════════════════════════════════════════
#  HANDLER 3 — COMMANDES SLASH / FAQ
# ═══════════════════════════════════════════════════════════════════

async def on_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg  = update.effective_message
    user = update.effective_user
    if not msg or not user:
        return

    command  = msg.text.lstrip("/").split("@")[0].split()[0].lower()
    response = FAQ_RESPONSES.get(command)
    if not response:
        return

    # /resultats → admins uniquement
    if command in ADMIN_ONLY_COMMANDS:
        if not await check_is_admin(ctx, user.id):
            try:
                await msg.delete()
            except Exception:
                pass
            sent = await ctx.bot.send_message(
                chat_id=GROUP_ID,
                text=f"🔒 *{user.first_name}*, cette commande est réservée aux admins.",
                parse_mode=ParseMode.MARKDOWN,
            )
            await asyncio.sleep(8)
            try:
                await sent.delete()
            except Exception:
                pass
            print(f"[HlyBOT][FAQ] /{command} refusé à {user.first_name} ({user.id})")
            return

    try:
        await msg.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        print(f"[HlyBOT][FAQ] /{command} → {user.first_name} ({user.id})")
    except Exception as e:
        print(f"[HlyBOT][FAQ ERROR] {e}")


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print("""
██╗  ██╗██╗  ██╗   ██╗██████╗  ██████╗ ████████╗
██║  ██║██║  ╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
███████║██║   ╚████╔╝ ██████╔╝██║   ██║   ██║
██╔══██║██║    ╚██╔╝  ██╔══██╗██║   ██║   ██║
██║  ██║███████╗██║   ██████╔╝╚██████╔╝   ██║
╚═╝  ╚═╝╚══════╝╚═╝   ╚═════╝  ╚═════╝    ╚═╝
✅ HlyBOT démarré — tous modules actifs
""")

    app = Application.builder().token(BOT_TOKEN).build()

    # Messages texte → stats + anti-liens + VIP
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Chat(GROUP_ID), on_message)
    )

    # Nouveaux membres → bienvenue
    app.add_handler(
        ChatMemberHandler(on_new_member, ChatMemberHandler.CHAT_MEMBER)
    )

    # Commandes slash → FAQ
    for cmd in FAQ_RESPONSES.keys():
        app.add_handler(CommandHandler(cmd, on_command))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
