"""
config.py — HlyBOT
Tous les paramètres du bot en un seul endroit.
"""

import os

# ═══════════════════════════════════════════════════════════════════
#  TOKEN — un seul bot via @BotFather
# ═══════════════════════════════════════════════════════════════════
BOT_TOKEN = os.getenv("BOT_TOKEN", "TON_TOKEN_HLYBOT")

# ═══════════════════════════════════════════════════════════════════
#  GROUPE
# ═══════════════════════════════════════════════════════════════════
GROUP_ID = int(os.getenv("GROUP_ID", "-1001234567890"))

# ═══════════════════════════════════════════════════════════════════
#  REDIS
# ═══════════════════════════════════════════════════════════════════
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# ═══════════════════════════════════════════════════════════════════
#  ACTIVITÉ & VIP
# ═══════════════════════════════════════════════════════════════════
ACTIVITY_THRESHOLD   = 15    # messages en fenêtre glissante pour déclencher VIP
ACTIVITY_WINDOW_SECS = 300   # fenêtre glissante = 5 minutes
COOLDOWN_VIP_MINS    = 30    # délai minimum entre 2 messages VIP automatiques

VIP_KEYWORDS = [
    "mai dior", "the hly", "the_hly", "maidior", "mangue", "miss971",
    "badmina", "vip",
]

# ═══════════════════════════════════════════════════════════════════
#  MESSAGES VIP (rotation — jamais le même 2x de suite)
# ═══════════════════════════════════════════════════════════════════
VIP_MESSAGES = [
    (
        "👑 LE PLUS GROS VIP JAMAIS SORTI SUR TELEGRAM EST LÀ.\n\n"
        "+4000 vidéos exclusives. Des centaines de grosses influenceuses."
        "Qualité premium HD/4K. 100% privé et sécurisé.\n"
        "Tu sais ce que tu fais. Rejoins l'élite.\n"
        "📩 Contact : @hlytsukiyamaa"
    ),
    (
        "🌸 Certains savent. Les autres passent à côté.\n"
        "VIP TSUKIYAMA — le contenu que tu ne trouveras nulle part ailleurs."
        "+2K de contenu mis à jour régulièrement. De toute origine, sans limite.\n"
        "Exclusif • Premium • Illimité\n"
        "📩 Contact : @hlytsukiyamaa"
    ),
    (
        "⚡ +4000 vidéos. Les meilleures influenceuses. Accès instantané.\n"
        "Arrête de chercher, tout est là. VIP TSUKIYAMA sur Telegram —"
        "le seul VIP qui mérite sa réputation.\n"
        "📩 Contact : @hlytsukiyamaa"
    ),
    (
        "🥀 Le VIP ultime, pour les vrais connaisseurs.\n"
        "Ici c'est HD/4K, 100% privé, mis à jour en continu."
        "Rejoins ceux qui ont déjà compris.\n"
        "📩 Contact : @hlytsukiyamaa"
    ),
    (
        "👁️ +4000 vidéos exclusives. Grosses influenceuses. Accès VIP instantané.\n"
        "Contenu unique — nulle part ailleurs.\n"
        "REJOINS TSUKIYAMA.\n"
        "📩 Contact : @hlytsukiyamaa"
    ),
]

# ═══════════════════════════════════════════════════════════════════
#  MESSAGE DE BIENVENUE
# ═══════════════════════════════════════════════════════════════════
WELCOME_MESSAGE = (
    "👋 Bienvenue *{name}* dans le groupe !\n\n"
    "📌 *Règles essentielles :*\n"
    "• Pas de liens sans autorisation admin\n"
    "• Respecte les membres\n"
    "• Pas de spam ni de pub\n\n"
    "💎 Ce groupe est gratuit.\n"
    "Pour accéder au vip → contacte @hlytsukiyamaa pour le *VIP*.\n\n"
)

# ═══════════════════════════════════════════════════════════════════
#  FAQ — commandes slash
# ═══════════════════════════════════════════════════════════════════
ADMIN_ONLY_COMMANDS = set()

FAQ_RESPONSES = {
    "vip": (
        "💎 *Le VIP — Accès Premium*\n\n"
        "Le canal VIP est *payant* et donne accès à:\n"
        "• +4000 vidéos exclusives\n"
        "• Qualité premium des vidéos\n"
        "• Des dossiers sur les influenceurs les plus connues\n"
        "• Accès à vie\n\n"
        "📩 Contacte @hlytsukiyamaa pour les modalités d'accès."
    ),
    "regles": (
        "📌 *Règles du groupe*\n\n"
        "1️⃣ Pas de liens sans accord admin\n"
        "2️⃣ Pas de spam ou pub\n"
        "3️⃣ Respecte les autres membres\n"
        "⚠️ Toute violation entraîne un avertissement puis un bannissement."
    ),
    "contact": (
        "📩 *Contacter @hlytsukiyamaa*\n\n"
        "Pour toute question sur le VIP ou un signalement :\n"
    ),
    "teaser": (
    "🎬 *Teaser — Aperçu exclusif*\n\n"
    "Tu veux voir ce que nos membres VIP reçoivent ?\n"
    "👉 [Accéder au teaser](https://t.me/+c2qdEEGpZXM5NWJk)\n\n"
    "⚠️ L'accès au teaser n'est pas automatique.\n"
    "Tu dois être *accepté par un admin*.\n\n"
    "🏆 Les membres les plus actifs du groupe sont prioritaires.\n"
    "Participe, échange, contribue — et tu seras remarqué.\n\n"
),
    "aide": (
        "🤖 *Commandes HlyBOT*\n\n"
        "/vip — Infos sur l'accès VIP\n"
        "/regles — Règles du groupe\n"
        "/contact — Contact pour le vip\n"
        "/preuve — Preuve en dm\n"
        "/aide — Cette aide"
    ),
}
