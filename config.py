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
    "signal", "signaux", "vip", "premium", "trade", "analyse",
    "entrée", "sortie", "tp", "sl", "profit", "forex", "crypto",
    "binance", "bybit", "pump", "moon", "airdrop", "call",
    "formation", "stratégie", "résultats", "gains", "copy trading",
]

# ═══════════════════════════════════════════════════════════════════
#  MESSAGES VIP (rotation — jamais le même 2x de suite)
# ═══════════════════════════════════════════════════════════════════
VIP_MESSAGES = [
    (
        "🔐 *Accès VIP — Zone Premium*\n\n"
        "Les signaux que tout le monde cherche ne circulent pas ici.\n"
        "Nos membres VIP ont accès à :\n"
        "• 📊 Analyses exclusives avant le marché\n"
        "• 🎯 Signaux précis avec TP/SL définis\n"
        "• 💬 Suivi en temps réel\n"
        "• 🧠 Stratégies enseignées pas-à-pas\n\n"
        "📩 Contacte un admin pour rejoindre le VIP."
    ),
    (
        "💎 *Tu cherches des signaux fiables ?*\n\n"
        "Nos membres VIP ne cherchent plus — ils reçoivent.\n\n"
        "✅ Signaux vérifiés\n"
        "✅ Support dédié\n"
        "✅ Résultats transparents\n\n"
        "📩 Glisse en DM à un admin pour accéder au VIP."
    ),
    (
        "⚡ *La différence entre profit et perte ?*\n"
        "L'information. Et le timing.\n\n"
        "Notre canal VIP te donne les deux.\n"
        "Les places sont limitées — la qualité aussi exige ça.\n\n"
        "📩 Contacte un admin pour les modalités."
    ),
    (
        "🧩 *Ce groupe est gratuit. Le VIP, c'est autre chose.*\n\n"
        "Si tu veux passer au niveau supérieur :\n"
        "signaux premium • analyses poussées • accès privé\n\n"
        "📩 Renseigne-toi auprès d'un admin."
    ),
    (
        "📈 *Pendant que certains hésitent, d'autres agissent.*\n\n"
        "Nos membres VIP ont déjà leurs positions.\n"
        "Tu veux être de ceux qui savent avant les autres ?\n\n"
        "📩 Un message à un admin suffit."
    ),
]

# ═══════════════════════════════════════════════════════════════════
#  MESSAGE DE BIENVENUE
# ═══════════════════════════════════════════════════════════════════
WELCOME_MESSAGE = (
    "👋 Bienvenue *{name}* dans le groupe !\n\n"
    "📌 *Règles essentielles :*\n"
    "• Pas de liens sans autorisation admin\n"
    "• Respecte les membres et les analyses\n"
    "• Pas de spam ni de pub\n\n"
    "💎 Ce groupe est gratuit.\n"
    "Pour accéder aux signaux premium et analyses exclusives → contacte un admin pour le *VIP*.\n\n"
    "Bonne analyse à tous ! 🚀"
)

# ═══════════════════════════════════════════════════════════════════
#  FAQ — commandes slash
# ═══════════════════════════════════════════════════════════════════
ADMIN_ONLY_COMMANDS = {"resultats"}   # commandes réservées aux admins

FAQ_RESPONSES = {
    "vip": (
        "💎 *Le VIP — Accès Premium*\n\n"
        "Le canal VIP est *payant* et donne accès à :\n"
        "• Signaux avec TP/SL précis\n"
        "• Analyses avant ouverture de marché\n"
        "• Suivi en temps réel\n"
        "• Formation et stratégies\n\n"
        "📩 Contacte un admin pour les modalités d'accès."
    ),
    "regles": (
        "📌 *Règles du groupe*\n\n"
        "1️⃣ Pas de liens sans accord admin\n"
        "2️⃣ Pas de spam ou pub\n"
        "3️⃣ Respecte les autres membres\n"
        "4️⃣ Pas de DM non sollicités\n"
        "5️⃣ Les signaux gratuits sont limités — VIP pour le reste\n\n"
        "⚠️ Toute violation entraîne un avertissement puis un bannissement."
    ),
    "contact": (
        "📩 *Contacter un admin*\n\n"
        "Pour toute question sur le VIP, un partenariat, ou un signalement :\n"
        "→ Glisse un DM à un admin du groupe.\n\n"
        "On te répond dans les meilleurs délais. ✅"
    ),
    "resultats": (
        "📊 *Résultats & transparence*\n\n"
        "Nos performances sont partagées exclusivement dans le canal VIP.\n"
        "Pas de faux screenshots — que du réel, vérifiable.\n\n"
        "Pour voir les résultats → rejoins le VIP.\n"
        "📩 Contacte un admin."
    ),
    "aide": (
        "🤖 *Commandes HlyBOT*\n\n"
        "/vip — Infos sur l'accès VIP\n"
        "/regles — Règles du groupe\n"
        "/contact — Contacter un admin\n"
        "/resultats — Performances (admins uniquement)\n"
        "/aide — Cette aide"
    ),
}
