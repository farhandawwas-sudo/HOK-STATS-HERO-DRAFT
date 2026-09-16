import streamlit as st
import pandas as pd
import json

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Real-Time Web Draft Assistant | By Siropkokop",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Esports Dark Theme
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFD700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #AAAAAA;
        text-align: center;
        margin-bottom: 20px;
    }
    .stCard {
        background-color: #1E1E2E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #313244;
    }
    .badge-s { background-color: #E74C3C; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; }
    .badge-a { background-color: #F39C12; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; }
    .badge-comfort { background-color: #2ECC71; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; }
    .badge-counter { background-color: #9B59B6; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE HEROES, ROSTER & WEAKNESSES
# ==========================================
HERO_DB = [
    # Clash Lane
    {"name": "Biron", "role": "Clash", "tier": "S", "red_bias": False, "counters": ["Physical Fighters"], "synergies": ["Dun", "Zhang Fei"]},
    {"name": "Florentino", "role": "Clash", "tier": "S", "red_bias": False, "counters": ["Tank Heavy"], "synergies": ["Yaria"]},
    {"name": "Dharma", "role": "Clash", "tier": "S", "red_bias": False, "counters": ["Immobile Squishies"], "synergies": ["Lady Sun", "Yao"]},
    {"name": "Allain", "role": "Clash", "tier": "A", "red_bias": False, "counters": ["Squishy Carry"], "synergies": ["Wang Zhaojun"]},
    {"name": "Sun Ce", "role": "Clash", "tier": "A", "red_bias": False, "counters": ["Split Pushers"], "synergies": ["Da Qiao", "Nuwa"]},
    {"name": "Fatih", "role": "Clash", "tier": "A", "red_bias": False, "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"]},
    
    # Jungle
    {"name": "Lam", "role": "Jungle", "tier": "S", "red_bias": False, "counters": ["Low HP Squishies"], "synergies": ["Yaria", "Angela"]},
    {"name": "Augran", "role": "Jungle", "tier": "S", "red_bias": False, "counters": ["Wall Huggers"], "synergies": ["Biron", "Zhang Fei"]},
    {"name": "Feyd", "role": "Jungle", "tier": "S", "red_bias": False, "counters": ["Backline MM"], "synergies": ["Kui", "Devara"]},
    {"name": "Li Bai", "role": "Jungle", "tier": "A", "red_bias": False, "counters": ["Immobile Mages"], "synergies": ["Kui", "Nuwa"]},
    {"name": "Pei", "role": "Jungle", "tier": "A", "red_bias": False, "counters": ["Slow Early Junglers"], "synergies": ["Biron", "Devara"]},
    {"name": "Musashi", "role": "Jungle", "tier": "A", "red_bias": False, "counters": ["Healers"], "synergies": ["Dolia"]},
    {"name": "Kaizer", "role": "Jungle", "tier": "A", "red_bias": False, "counters": ["Burst Assassins"], "synergies": ["Zhang Fei"]},
    {"name": "Ukyo", "role": "Jungle", "tier": "A", "red_bias": False, "counters": ["Early Squishies"], "synergies": ["Mozi"]},
    {"name": "Xuance", "role": "Jungle", "tier": "A", "red_bias": False, "counters": ["Immobile Carries"], "synergies": ["Mozi", "Dun"]},

    # Mid Lane
    {"name": "Haya", "role": "Mid", "tier": "S", "red_bias": True, "counters": ["Cluster Comps"], "synergies": ["Feyd", "Li Bai"]},
    {"name": "Wang Zhaojun", "role": "Mid", "tier": "S", "red_bias": False, "counters": ["Dive Comps"], "synergies": ["Biron", "Lady Sun"]},
    {"name": "Xiao Qiao", "role": "Mid", "tier": "S", "red_bias": False, "counters": ["Clustered Enemies"], "synergies": ["Mozi", "Dun", "Arli"]},
    {"name": "Lorion", "role": "Mid", "tier": "S", "red_bias": False, "counters": ["Tight Formations"], "synergies": ["Pei", "Devara"]},
    {"name": "Nuwa", "role": "Mid", "tier": "A", "red_bias": False, "counters": ["Long-range Seige"], "synergies": ["Sun Ce", "Li Bai"]},
    {"name": "Angela", "role": "Mid", "tier": "A", "red_bias": False, "counters": ["Frontline Tanks"], "synergies": ["Lam", "Zhang Fei"]},
    {"name": "Yixing", "role": "Mid", "tier": "S", "red_bias": False, "counters": ["No-escape Comps"], "synergies": ["Dharma", "Lady Sun"]},
    {"name": "Kui", "role": "Mid", "tier": "A", "red_bias": False, "counters": ["Immobile Carries"], "synergies": ["Li Bai", "Feyd", "Nuwa"]},
    {"name": "Heino", "role": "Mid", "tier": "S", "red_bias": False, "counters": ["Attrition Comps"], "synergies": ["Dolia"]},

    # Farm Lane (MM)
    {"name": "Lady Sun", "role": "Farm", "tier": "S", "red_bias": False, "counters": ["Low Mobility Tanks"], "synergies": ["Yaria", "Dharma", "Yao"]},
    {"name": "Ao'yin (Loong)", "role": "Farm", "tier": "S", "red_bias": True, "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia"]},
    {"name": "Arli", "role": "Farm", "tier": "S", "red_bias": False, "counters": ["Skillshot Mages"], "synergies": ["Mozi", "Xiao Qiao"]},
    {"name": "Flowborn (MM)", "role": "Farm", "tier": "S", "red_bias": False, "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce"]},
    {"name": "Luara", "role": "Farm", "tier": "A", "red_bias": False, "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun"]},
    {"name": "Marco Polo", "role": "Farm", "tier": "A", "red_bias": False, "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei"]},

    # Roam
    {"name": "Zhang Fei", "role": "Roam", "tier": "S", "red_bias": True, "counters": ["Heavy Dive"], "synergies": ["Lady Sun", "Angela"]},
    {"name": "Yaria", "role": "Roam", "tier": "S", "red_bias": False, "counters": ["Burst Single Target"], "synergies": ["Lady Sun", "Lam", "Loong"]},
    {"name": "Dolia", "role": "Roam", "tier": "S", "red_bias": False, "counters": ["Short War Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"]},
    {"name": "Devara", "role": "Roam", "tier": "A", "red_bias": False, "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"]},
    {"name": "Mozi", "role": "Roam", "tier": "S", "red_bias": False, "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"]},
    {"name": "Dun", "role": "Roam", "tier": "A", "red_bias": False, "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"]},
    {"name": "Da Qiao", "role": "Roam", "tier": "S", "red_bias": False, "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli"]}
]

PLAYER_POOLS = {
    "Delfos": ["Fatih", "Biron", "Allain", "Devara", "Dharma", "Zhang Fei", "Dun"],
    "Dapid": ["Augran", "Feyd", "Lam", "Chicha", "Flowborn (MM)", "Menki", "Li Bai", "Pei", "Dun", "Musashi", "Kaizer", "Ukyo", "Xuance"],
    "Kafel": ["Wang Zhaojun", "Angela", "Yixing", "Biron", "Sun Ce", "Xiao Qiao"],
    "Virel": ["Zhang Fei", "Biron", "Dharma", "Allain", "Dun"],
    "Bah": ["Haya", "Lorion", "Nuwa", "Kui", "Lady Sun", "Marco Polo", "Arli"],
    "Reyhan": ["Lady Sun", "Arli", "Flowborn (MM)", "Luara", "Marco Polo"],
    "IceVrigid": ["Allain", "Dharma", "Biron", "Zhang Fei", "Sun Ce"],
    "Bonaparte": ["Musashi", "Kaizer", "Dun", "Ukyo", "Pei", "Augran", "Lam", "Feyd"]
}

ENEMY_THREAT_BAN_RECOMMENDATIONS = ["Mai Shiranui", "Luna", "Jing", "Shangguan", "Chicha", "Donghuang", "Nezha"]

# ==========================================
# INITIALIZE SESSION STATE FOR FEARLESS MEMORY
# ==========================================
if 'used_heroes' not in st.session_state:
    st.session_state['used_heroes'] = []

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.header("⚙️ Game Setup & Lineup")

match_mode = st.sidebar.selectbox("Format Match", ["Bo1", "Bo3 (Fearless)", "Bo5 (Fearless)", "Bo7 (Fearless)"])
game_num = st.sidebar.slider("Game Ke-", 1, 7, 1)
our_side = st.sidebar.radio("Sisi Tim Kita", ["Blue Side (Pilih B1)", "Red Side (Counter R5)"])

st.sidebar.subheader("👥 Active Roster Selection")
lineup_preset = st.sidebar.selectbox("Presisi Roster Tim", [
    "Lineup 1 (CL: Delfos, Jung: Dapid, Mid: Kafel, Roam: Virel, MM: Reyhan)",
    "Lineup 2 (CL: Virel, Jung: Dapid, Mid: Kafel, Roam: Delfos, MM: Bah)",
    "Lineup 3 (CL: Delfos, Jung: Dapid, Mid: Bah, Roam: Virel, MM: Reyhan)",
    "Lineup 4 (CL: Kafel, Jung: Dapid, Mid: Bah, Roam: Delfos, MM: Reyhan)",
    "Custom Roster"
])

# Determine active players based on preset
if "Lineup 1" in lineup_preset:
    active_players = ["Delfos", "Dapid", "Kafel", "Virel", "Reyhan"]
elif "Lineup 2" in lineup_preset:
    active_players = ["Virel", "Dapid", "Kafel", "Delfos", "Bah"]
elif "Lineup 3" in lineup_preset:
    active_players = ["Delfos", "Dapid", "Bah", "Virel", "Reyhan"]
elif "Lineup 4" in lineup_preset:
    active_players = ["Kafel", "Dapid", "Bah", "Delfos", "Reyhan"]
else:
    active_players = st.sidebar.multiselect("Pilih Pemain Aktif", list(PLAYER_POOLS.keys()), default=["Delfos", "Dapid", "Bah", "Virel", "Reyhan"])

# Display Used Heroes (Fearless Draft Memory)
st.sidebar.subheader("🔒 Fearless Memory (Locked Heroes)")
st.sidebar.caption("Hero yang sudah dipakai tim di game sebelumnya:")
st.sidebar.write(", ".join(st.session_state['used_heroes']) if st.session_state['used_heroes'] else "Belum ada hero terpakai.")

if st.sidebar.button("🗑️ Reset Fearless Memory (New Match)"):
    st.session_state['used_heroes'] = []
    st.rerun()

# ==========================================
# MAIN DRAFTING INTERFACE
# ==========================================
col_draft, col_recom = st.columns([1.1, 1])

with col_draft:
    st.subheader("📋 Input Live Ban & Pick Phase")
    
    # BAN PHASE
    st.markdown("##### 🚫 Ban Phase")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        our_bans = st.multiselect("Ban Tim Kita", [h["name"] for h in HERO_DB], key="our_bans")
    with b_col2:
        enemy_bans = st.multiselect("Ban Tim Musuh", [h["name"] for h in HERO_DB], key="enemy_bans")
        
    # PICK PHASE
    st.markdown("##### ⚔️ Pick Phase")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("**🔵 Blue Side Picks**")
        b1 = st.selectbox("Blue 1 (B1)", ["None"] + [h["name"] for h in HERO_DB], key="b1")
        b2 = st.selectbox("Blue 2 (B2)", ["None"] + [h["name"] for h in HERO_DB], key="b2")
        b3 = st.selectbox("Blue 3 (B3)", ["None"] + [h["name"] for h in HERO_DB], key="b3")
        b4 = st.selectbox("Blue 4 (B4)", ["None"] + [h["name"] for h in HERO_DB], key="b4")
        b5 = st.selectbox("Blue 5 (B5)", ["None"] + [h["name"] for h in HERO_DB], key="b5")
    with p_col2:
        st.markdown("**🔴 Red Side Picks**")
        r1 = st.selectbox("Red 1 (R1)", ["None"] + [h["name"] for h in HERO_DB], key="r1")
        r2 = st.selectbox("Red 2 (R2)", ["None"] + [h["name"] for h in HERO_DB], key="r2")
        r3 = st.selectbox("Red 3 (R3)", ["None"] + [h["name"] for h in HERO_DB], key="r3")
        r4 = st.selectbox("Red 4 (R4)", ["None"] + [h["name"] for h in HERO_DB], key="r4")
        r5 = st.selectbox("Red 5 (R5)", ["None"] + [h["name"] for h in HERO_DB], key="r5")

    # Determine picks based on side selection
    blue_picks = [p for p in [b1, b2, b3, b4, b5] if p != "None"]
    red_picks = [p for p in [r1, r2, r3, r4, r5] if p != "None"]
    
    if "Blue Side" in our_side:
        our_picks = blue_picks
        enemy_picks = red_picks
    else:
        our_picks = red_picks
        enemy_picks = blue_picks

    # Save used heroes button
    if st.button("💾 Simpan Hero Terpakai ke Fearless Memory (End Game)"):
        for hero in our_picks:
            if hero not in st.session_state['used_heroes']:
                st.session_state['used_heroes'].append(hero)
        st.success("Hero berhasil disimpan ke Fearless Memory!")
        st.rerun()

# ==========================================
# REAL-TIME RECOMMENDATION ENGINE
# ==========================================
with col_recom:
    st.subheader("📊 Real-Time Recommendation & Probability Engine")
    
    # 1. BAN RECOMMENDATIONS
    st.markdown("#### 🎯 Top Target Ban Recommendations")import streamlit as st
import pandas as pd
import json
import os

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Real-Time Web Draft Assistant | By Siropkokop",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Esports Dark Theme & Hero Cards
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFD700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #AAAAAA;
        text-align: center;
        margin-bottom: 15px;
    }
    .stCard {
        background-color: #181825;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #313244;
        margin-bottom: 15px;
    }
    .hero-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border: 1px solid #45475a;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .hero-img {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #f9e2af;
        margin-bottom: 5px;
    }
    .badge-s { background-color: #f38ba8; color: #11111b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    .badge-a { background-color: #fab387; color: #11111b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    .badge-comfort { background-color: #a6e3a1; color: #11111b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    .badge-counter { background-color: #cba6f7; color: #11111b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    .stat-text { font-size: 0.82rem; color: #bac2de; margin-top: 4px; }
    .win-badge { color: #a6e3a1; font-weight: bold; }
    .loss-badge { color: #f38ba8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE HEROES WITH STATS & AVATARS
# ==========================================
# Default high quality avatar placeholders / CDN icons
AVATAR_BASE = "https://img.icons8.com/color/96/000000/sword.png"

HERO_DB = [
    # Clash Lane
    {"name": "Biron", "role": "Clash", "tier": "S", "win_rate": 54.2, "pick_rate": 31.5, "ban_rate": 18.4, "specialty": "Shield & Heavy Sustain", "counters": ["Physical Fighters"], "synergies": ["Dun", "Zhang Fei", "Angela"], "img": "https://img.icons8.com/color/96/lightning-bolt.png"},
    {"name": "Florentino", "role": "Clash", "tier": "S", "win_rate": 56.8, "pick_rate": 28.0, "ban_rate": 42.1, "specialty": "True Damage Duelist", "counters": ["Tank Heavy"], "synergies": ["Yaria", "Lam"], "img": "https://img.icons8.com/color/96/fencing.png"},
    {"name": "Dharma", "role": "Clash", "tier": "S", "win_rate": 53.5, "pick_rate": 22.4, "ban_rate": 15.0, "specialty": "Wall Slam Inisiator", "counters": ["Immobile Squishies"], "synergies": ["Lady Sun", "Yao", "Virel"], "img": "https://img.icons8.com/color/96/boxing-glove.png"},
    {"name": "Allain", "role": "Clash", "tier": "A", "win_rate": 51.8, "pick_rate": 19.2, "ban_rate": 8.5, "specialty": "Hybrid Lock-down", "counters": ["Squishy Carry"], "synergies": ["Wang Zhaojun", "Delfos"], "img": "https://img.icons8.com/color/96/broadsword.png"},
    {"name": "Sun Ce", "role": "Clash", "tier": "A", "win_rate": 52.4, "pick_rate": 25.1, "ban_rate": 12.3, "specialty": "Global Ship Transport", "counters": ["Split Pushers"], "synergies": ["Da Qiao", "Nuwa"], "img": "https://img.icons8.com/color/96/paddles.png"},
    {"name": "Fatih", "role": "Clash", "tier": "A", "win_rate": 50.9, "pick_rate": 14.8, "ban_rate": 5.2, "specialty": "Frontline Melee brawler", "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"], "img": "https://img.icons8.com/color/96/shield.png"},
    {"name": "Dunshan", "role": "Clash", "tier": "A", "win_rate": 51.2, "pick_rate": 12.0, "ban_rate": 14.2, "specialty": "Turret Repair & Shield Block", "counters": ["Ranged Projectiles"], "synergies": ["Xiao Qiao", "Dun"], "img": "https://img.icons8.com/color/96/castle.png"},

    # Jungle
    {"name": "Lam", "role": "Jungle", "tier": "S", "win_rate": 58.5, "pick_rate": 42.1, "ban_rate": 68.4, "specialty": "Submerge & Executing Dive", "counters": ["Low HP Squishies"], "synergies": ["Yaria", "Angela", "Dapid"], "img": "https://img.icons8.com/color/96/shark.png"},
    {"name": "Augran", "role": "Jungle", "tier": "S", "win_rate": 57.2, "pick_rate": 38.0, "ban_rate": 55.1, "specialty": "Soul Tether & Wall Pass", "counters": ["Wall Huggers"], "synergies": ["Biron", "Zhang Fei"], "img": "https://img.icons8.com/color/96/ghost.png"},
    {"name": "Feyd", "role": "Jungle", "tier": "S", "win_rate": 55.4, "pick_rate": 29.6, "ban_rate": 38.2, "specialty": "Shadow Ambush Burst", "counters": ["Backline MM"], "synergies": ["Kui", "Devara"], "img": "https://img.icons8.com/color/96/ninja.png"},
    {"name": "Li Bai", "role": "Jungle", "tier": "A", "win_rate": 52.1, "pick_rate": 21.0, "ban_rate": 16.5, "specialty": "Untargetable Sword Combo", "counters": ["Immobile Mages"], "synergies": ["Kui", "Nuwa"], "img": "https://img.icons8.com/color/96/katana.png"},
    {"name": "Pei", "role": "Jungle", "tier": "A", "win_rate": 53.0, "pick_rate": 18.5, "ban_rate": 11.2, "specialty": "Tiger Form Early Invade", "counters": ["Slow Early Junglers"], "synergies": ["Biron", "Devara"], "img": "https://img.icons8.com/color/96/tiger.png"},
    {"name": "Musashi", "role": "Jungle", "tier": "A", "win_rate": 51.5, "pick_rate": 17.2, "ban_rate": 9.4, "specialty": "Anti-Heal Locking", "counters": ["Healers"], "synergies": ["Dolia"], "img": "https://img.icons8.com/color/96/samurai.png"},
    {"name": "Kaizer", "role": "Jungle", "tier": "A", "win_rate": 52.8, "pick_rate": 24.0, "ban_rate": 14.1, "specialty": "Demon Form Tank brawler", "counters": ["Burst Assassins"], "synergies": ["Zhang Fei"], "img": "https://img.icons8.com/color/96/demon.png"},
    {"name": "Ukyo", "role": "Jungle", "tier": "A", "win_rate": 50.4, "pick_rate": 13.5, "ban_rate": 4.8, "specialty": "Early Poke & Slash", "counters": ["Early Squishies"], "synergies": ["Mozi"], "img": "https://img.icons8.com/color/96/sword.png"},
    {"name": "Xuance", "role": "Jungle", "tier": "A", "win_rate": 51.9, "pick_rate": 15.1, "ban_rate": 8.0, "specialty": "Hook & Throw Back", "counters": ["Immobile Carries"], "synergies": ["Mozi", "Dun"], "img": "https://img.icons8.com/color/96/hook.png"},
    {"name": "Luna", "role": "Jungle", "tier": "S", "win_rate": 56.1, "pick_rate": 18.9, "ban_rate": 72.0, "specialty": "Infinite Reset Dash", "counters": ["No Hard CC Comps"], "synergies": ["Da Qiao"], "img": "https://img.icons8.com/color/96/full-moon.png"},
    {"name": "Jing", "role": "Jungle", "tier": "S", "win_rate": 55.8, "pick_rate": 20.2, "ban_rate": 69.5, "specialty": "Mirror Image Swap Burst", "counters": ["Immobile Backline"], "synergies": ["Lorion"], "img": "https://img.icons8.com/color/96/mirror.png"},

    # Mid Lane
    {"name": "Haya", "role": "Mid", "tier": "S", "win_rate": 80.0, "pick_rate": 35.4, "ban_rate": 61.2, "specialty": "Red Side Mirage Burst", "counters": ["Cluster Comps"], "synergies": ["Feyd", "Li Bai", "Bah"], "img": "https://img.icons8.com/color/96/magic-wand.png"},
    {"name": "Wang Zhaojun", "role": "Mid", "tier": "S", "win_rate": 54.5, "pick_rate": 33.1, "ban_rate": 21.0, "specialty": "Ice Freeze Zone CC", "counters": ["Dive Comps"], "synergies": ["Biron", "Lady Sun", "Kafel"], "img": "https://img.icons8.com/color/96/snowflake.png"},
    {"name": "Xiao Qiao", "role": "Mid", "tier": "S", "win_rate": 53.9, "pick_rate": 31.0, "ban_rate": 15.4, "specialty": "Fan Throw & Knock-up Burst", "counters": ["Clustered Enemies"], "synergies": ["Mozi", "Dun", "Arli"], "img": "https://img.icons8.com/color/96/folding-fan.png"},
    {"name": "Lorion", "role": "Mid", "tier": "S", "win_rate": 54.1, "pick_rate": 26.5, "ban_rate": 19.8, "specialty": "Dark Orb Vortex CC", "counters": ["Tight Formations"], "synergies": ["Pei", "Devara"], "img": "https://img.icons8.com/color/96/galaxy.png"},
    {"name": "Nuwa", "role": "Mid", "tier": "A", "win_rate": 52.6, "pick_rate": 16.2, "ban_rate": 7.5, "specialty": "Matrix Wall & Global Teleport", "counters": ["Long-range Seige"], "synergies": ["Sun Ce", "Li Bai"], "img": "https://img.icons8.com/color/96/space-shuttle.png"},
    {"name": "Angela", "role": "Mid", "tier": "A", "win_rate": 51.4, "pick_rate": 28.0, "ban_rate": 6.2, "specialty": "Scorch Beam Melt", "counters": ["Frontline Tanks"], "synergies": ["Lam", "Zhang Fei"], "img": "https://img.icons8.com/color/96/fire-element.png"},
    {"name": "Yixing", "role": "Mid", "tier": "S", "win_rate": 55.1, "pick_rate": 24.3, "ban_rate": 28.6, "specialty": "Go Board Chess Grid CC", "counters": ["No-escape Comps"], "synergies": ["Dharma", "Lady Sun"], "img": "https://img.icons8.com/color/96/chess-king.png"},
    {"name": "Kui", "role": "Mid", "tier": "A", "win_rate": 50.8, "pick_rate": 19.5, "ban_rate": 12.0, "specialty": "Hook & Swallow Isolation", "counters": ["Immobile Carries"], "synergies": ["Li Bai", "Feyd", "Nuwa"], "img": "https://img.icons8.com/color/96/pirate-hook.png"},
    {"name": "Heino", "role": "Mid", "tier": "S", "win_rate": 54.8, "pick_rate": 22.1, "ban_rate": 35.0, "specialty": "Time Reversal Reset", "counters": ["Attrition Comps"], "synergies": ["Dolia"], "img": "https://img.icons8.com/color/96/hourglass.png"},
    {"name": "Wang Wei", "role": "Mid", "tier": "A", "win_rate": 51.0, "pick_rate": 11.4, "ban_rate": 5.0, "specialty": "Mist Fog Concealment", "counters": ["Targeted Spells"], "synergies": ["Augran", "Feyd"], "img": "https://img.icons8.com/color/96/fog.png"},
    {"name": "Mai Shiranui", "role": "Mid", "tier": "S", "win_rate": 56.4, "pick_rate": 25.0, "ban_rate": 58.0, "specialty": "High Mobility Fan Dive", "counters": ["Immobile Mages"], "synergies": ["Lam"], "img": "https://img.icons8.com/color/96/fire-flame.png"},

    # Farm Lane (MM)
    {"name": "Lady Sun", "role": "Farm", "tier": "S", "win_rate": 55.6, "pick_rate": 36.2, "ban_rate": 24.5, "specialty": "Roll Dash Armor Shred Burst", "counters": ["Low Mobility Tanks"], "synergies": ["Yaria", "Dharma", "Yao", "Reyhan"], "img": "https://img.icons8.com/color/96/cannon.png"},
    {"name": "Ao'yin (Loong)", "role": "Farm", "tier": "S", "win_rate": 72.2, "pick_rate": 41.0, "ban_rate": 65.0, "specialty": "4 Elemental Souls & Dragon Ulti", "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia"], "img": "https://img.icons8.com/color/96/dragon.png"},
    {"name": "Arli", "role": "Farm", "tier": "S", "win_rate": 56.0, "pick_rate": 30.5, "ban_rate": 48.0, "specialty": "Umbrella Teleport Outplay", "counters": ["Skillshot Mages"], "synergies": ["Mozi", "Xiao Qiao"], "img": "https://img.icons8.com/color/96/umbrella.png"},
    {"name": "Flowborn (MM)", "role": "Farm", "tier": "S", "win_rate": 54.9, "pick_rate": 27.8, "ban_rate": 31.0, "specialty": "5-Stack Flow Barrage", "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce"], "img": "https://img.icons8.com/color/96/bow-and-arrow.png"},
    {"name": "Luara", "role": "Farm", "tier": "A", "win_rate": 52.3, "pick_rate": 18.0, "ban_rate": 12.5, "specialty": "Wall Climbing Sniper", "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun"], "img": "https://img.icons8.com/color/96/crossbow.png"},
    {"name": "Marco Polo", "role": "Farm", "tier": "A", "win_rate": 51.7, "pick_rate": 32.0, "ban_rate": 10.2, "specialty": "True Damage Spin", "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei"], "img": "https://img.icons8.com/color/96/revolver.png"},

    # Roam
    {"name": "Zhang Fei", "role": "Roam", "tier": "S", "win_rate": 58.5, "pick_rate": 45.0, "ban_rate": 39.0, "specialty": "Massive Shield & Demon Roar", "counters": ["Heavy Dive"], "synergies": ["Lady Sun", "Angela", "Virel"], "img": "https://img.icons8.com/color/96/gorilla.png"},
    {"name": "Yaria", "role": "Roam", "tier": "S", "win_rate": 53.8, "pick_rate": 39.5, "ban_rate": 52.0, "specialty": "True Damage Attachment Shield", "counters": ["Burst Single Target"], "synergies": ["Lady Sun", "Lam", "Loong"], "img": "https://img.icons8.com/color/96/deer.png"},
    {"name": "Dolia", "role": "Roam", "tier": "S", "win_rate": 55.2, "pick_rate": 34.0, "ban_rate": 58.0, "specialty": "Mermaid Cooldown Reset", "counters": ["Short War Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"], "img": "https://img.icons8.com/color/96/mermaid.png"},
    {"name": "Devara", "role": "Roam", "tier": "A", "win_rate": 52.0, "pick_rate": 20.1, "ban_rate": 14.0, "specialty": "Pillar Locking & Zone Control", "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd", "Delfos"], "img": "https://img.icons8.com/color/96/pillar.png"},
    {"name": "Mozi", "role": "Roam", "tier": "S", "win_rate": 54.0, "pick_rate": 28.4, "ban_rate": 22.5, "specialty": "Long-range Energy Cannon Stun", "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "img": "https://img.icons8.com/color/96/robot.png"},
    {"name": "Dun", "role": "Roam", "tier": "A", "win_rate": 51.5, "pick_rate": 21.0, "ban_rate": 8.0, "specialty": "Blade Hook & Shield Tank", "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "img": "https://img.icons8.com/color/96/viking-helmet.png"},
    {"name": "Da Qiao", "role": "Roam", "tier": "S", "win_rate": 55.9, "pick_rate": 23.0, "ban_rate": 62.0, "specialty": "Ocean Portal Global Recall", "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli"]},
    {"name": "Yao", "role": "Roam", "tier": "S", "win_rate": 54.2, "pick_rate": 25.1, "ban_rate": 18.0, "specialty": "Possession Shield & Stun", "counters": ["Single Target Burst"], "synergies": ["Dharma", "Lady Sun"]}
]

PLAYER_POOLS = {
    "Delfos": ["Fatih", "Biron", "Allain", "Devara", "Dharma", "Zhang Fei", "Dun"],
    "Dapid": ["Augran", "Feyd", "Lam", "Chicha", "Flowborn (MM)", "Menki", "Li Bai", "Pei", "Dun", "Musashi", "Kaizer", "Ukyo", "Xuance"],
    "Kafel": ["Wang Zhaojun", "Angela", "Yixing", "Biron", "Sun Ce", "Xiao Qiao"],
    "Virel": ["Zhang Fei", "Biron", "Dharma", "Allain", "Dun"],
    "Bahimut / Bah": ["Haya", "Lorion", "Nuwa", "Kui", "Lady Sun", "Marco Polo", "Arli"],
    "你好Duarr": ["Wang Zhaojun", "Angela", "Xiao Qiao", "Yixing", "Nuwa"],
    "Reyhan": ["Lady Sun", "Arli", "Flowborn (MM)", "Luara", "Marco Polo"]
}

PLAYER_WEAKNESSES = {
    "Kafel": ["Mai Shiranui", "Shangguan"],
    "你好Duarr": ["Mai Shiranui", "Lorion"],
    "Dapid": ["Luna", "Jing"],
    "Bonaparte": ["Luna", "Jing", "Yao", "Han Xin"],
    "Delfos": ["Chicha"],
    "IceVrigid": ["Mayene", "Devara"]
}

# Lineups Preset
LINEUPS = {
    "Lineup 1 (Delfos, Dapid, Kafel, Virel, Reyhan)": {
        "Clash": "Delfos", "Jungle": "Dapid", "Mid": "Kafel", "Roam": "Virel", "Farm": "Reyhan"
    },
    "Lineup 2 (Virel, Dapid, Kafel, Delfos, Bah)": {
        "Clash": "Virel", "Jungle": "Dapid", "Mid": "Kafel", "Roam": "Delfos", "Farm": "Bahimut / Bah"
    },
    "Lineup 3 (Delfos, Dapid, Bah, Virel, Reyhan)": {
        "Clash": "Delfos", "Jungle": "Dapid", "Mid": "Bahimut / Bah", "Roam": "Virel", "Farm": "Reyhan"
    },
    "Lineup 4 (Kafel, Dapid, Bah, Delfos, Reyhan)": {
        "Clash": "Kafel", "Jungle": "Dapid", "Mid": "Bahimut / Bah", "Roam": "Delfos", "Farm": "Reyhan"
    }
}

MATCH_FILE = "/workspace/scratch/match_history.json"

def load_match_history():
    if os.path.exists(MATCH_FILE):
        try:
            with open(MATCH_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_match_history(history):
    os.makedirs(os.path.dirname(MATCH_FILE), exist_ok=True)
    with open(MATCH_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Initialize Session States
if "our_bans" not in st.session_state:
    st.session_state.our_bans = []
if "enemy_bans" not in st.session_state:
    st.session_state.enemy_bans = []
if "our_picks" not in st.session_state:
    st.session_state.our_picks = {"Clash": None, "Jungle": None, "Mid": None, "Farm": None, "Roam": None}
if "enemy_picks" not in st.session_state:
    st.session_state.enemy_picks = {"Clash": None, "Jungle": None, "Mid": None, "Farm": None, "Roam": None}
if "draft_title" not in st.session_state:
    st.session_state.draft_title = "Unli CC Stun Lock Strategy"

# ==========================================
# HEADER SECTION
# ==========================================
st.markdown('<div class="main-title">⚔️ HOK REAL-TIME DRAFTING ASSISTANT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Engine Probability & Counter Generator | Developed by Coach Siropkokop</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_draft, tab_recommend, tab_matches, tab_whatsapp = st.tabs([
    "🎮 Real-Time Draft Phase", 
    "💡 Next Pick & Ban Schema", 
    "📊 Recent Match Analysis", 
    "📲 Export to WhatsApp"
])

# ==========================================
# SIDEBAR: CONFIG & LINEUP
# ==========================================
with st.sidebar:
    st.header("⚙️ Match Configuration")
    
    # Custom Draft Title Feature
    st.session_state.draft_title = st.text_input("🏷️ Custom Draft Name:", value=st.session_state.draft_title)
    
    selected_lineup_name = st.selectbox("👥 Active Lineup Preset:", list(LINEUPS.keys()))
    active_lineup = LINEUPS[selected_lineup_name]
    
    side = st.radio("🚩 Match Side:", ["Blue Side (First Pick)", "Red Side (Counter-Pick R5)"])
    is_red_side = "Red Side" in side
    
    fearless_mode = st.checkbox("🔒 Fearless Draft Mode (Lock Used Heroes)", value=True)
    
    st.markdown("---")
    st.subheader("👥 Active Roster Players")
    for role, p_name in active_lineup.items():
        st.write(f"• **{role}:** {p_name}")

    if st.button("🔄 Reset Current Draft"):
        st.session_state.our_bans = []
        st.session_state.enemy_bans = []
        st.session_state.our_picks = {"Clash": None, "Jungle": None, "Mid": None, "Farm": None, "Roam": None}
        st.session_state.enemy_picks = {"Clash": None, "Jungle": None, "Mid": None, "Farm": None, "Roam": None}
        st.rerun()

# Get list of ALL currently unavailable heroes (banned or picked)
all_unavailable = set(st.session_state.our_bans + st.session_state.enemy_bans)
for p in st.session_state.our_picks.values():
    if p: all_unavailable.add(p)
for p in st.session_state.enemy_picks.values():
    if p: all_unavailable.add(p)

all_hero_names = [h["name"] for h in HERO_DB]

def get_selectable_heroes(role=None, current_selection=None):
    """Filters out banned or already picked heroes dynamically."""
    available = []
    for h in HERO_DB:
        name = h["name"]
        if role and h["role"] != role:
            continue
        # Allow keeping current selection, but hide if unavailable elsewhere
        if name not in all_unavailable or name == current_selection:
            available.append(name)
    return sorted(available)

# ==========================================
# TAB 1: REAL-TIME DRAFT PHASE
# ==========================================
with tab_draft:
    st.subheader(f"📋 Strategy Draft: {st.session_state.draft_title}")
    
    # BAN SECTION
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown("### 🚫 OUR BANS")
        b1_opts = get_selectable_heroes()
        our_b1 = st.multiselect("Select Our Bans (Max 4):", options=b1_opts, default=[b for b in st.session_state.our_bans if b in b1_opts], max_selections=4)
        st.session_state.our_bans = our_b1
        
    with col_b2:
        st.markdown("### ❌ ENEMY BANS")
        b2_opts = get_selectable_heroes()
        enemy_b2 = st.multiselect("Select Enemy Bans (Max 4):", options=b2_opts, default=[b for b in st.session_state.enemy_bans if b in b2_opts], max_selections=4)
        st.session_state.enemy_bans = enemy_b2

    st.markdown("---")
    
    # PICK SECTION
    col_p1, col_p2 = st.columns(2)
    
    roles = ["Clash", "Jungle", "Mid", "Farm", "Roam"]
    
    with col_p1:
        st.markdown("### 🔵 OUR PICKS")
        for r in roles:
            player_name = active_lineup.get(r, "Player")
            opts = ["None"] + get_selectable_heroes(role=r, current_selection=st.session_state.our_picks[r])
            curr_val = st.session_state.our_picks[r] if st.session_state.our_picks[r] in opts else "None"
            sel = st.selectbox(f"**{r}** ({player_name}):", options=opts, index=opts.index(curr_val), key=f"our_{r}")
            st.session_state.our_picks[r] = None if sel == "None" else sel
            
            # Show Hero Stats Card if selected
            if st.session_state.our_picks[r]:
                h_info = next((item for item in HERO_DB if item["name"] == st.session_state.our_picks[r]), None)
                if h_info:
                    st.caption(f"⭐ Tier {h_info['tier']} | WR: {h_info['win_rate']}% | Pick: {h_info['pick_rate']}% | {h_info['specialty']}")

    with col_p2:
        st.markdown("### 🔴 ENEMY PICKS")
        for r in roles:
            opts = ["None"] + get_selectable_heroes(role=r, current_selection=st.session_state.enemy_picks[r])
            curr_val = st.session_state.enemy_picks[r] if st.session_state.enemy_picks[r] in opts else "None"
            sel = st.selectbox(f"**Enemy {r}:**", options=opts, index=opts.index(curr_val), key=f"enemy_{r}")
            st.session_state.enemy_picks[r] = None if sel == "None" else sel

    st.markdown("---")
    
    # Game 7 Blind Pick Emergency Button
    if st.button("🚨 Emergency Game 7 Blind Pick Generator (3-Min Rule)"):
        st.info("⚡ Generating 100% Comfort Pick Composition for Game 7...")
        st.session_state.our_picks = {
            "Clash": "Biron", "Jungle": "Augran", "Mid": "Wang Zhaojun", "Farm": "Lady Sun", "Roam": "Zhang Fei"
        }
        st.rerun()

# ==========================================
# TAB 2: NEXT PICK & BAN SCHEMA & PROBABILITY
# ==========================================
with tab_recommend:
    st.subheader("🧠 Real-Time Recommendation Engine & Next Step Schema")
    
    # Calculate Threat Bans for Enemies based on Player Weaknesses
    st.markdown("#### 🚫 RECOMMENDED NEXT BANS FOR OUR TEAM")
    recommended_bans = []
    
    # Weakness checks
    for role, p_name in active_lineup.items():
        if p_name in PLAYER_WEAKNESSES:
            for w in PLAYER_WEAKNESSES[p_name]:
                if w not in all_unavailable and w not in recommended_bans:
                    recommended_bans.append({"hero": w, "reason": f"Shuts down {p_name}'s weakness ({role})", "priority": "HIGH"})
    
    # Enemy high wr picks
    for h in HERO_DB:
        if h["tier"] == "S" and h["win_rate"] >= 55.0 and h["name"] not in all_unavailable and h["name"] not in [r["hero"] for r in recommended_bans]:
            recommended_bans.append({"hero": h["name"], "reason": f"High Meta Power Pick ({h['win_rate']}% WR)", "priority": "MEDIUM"})
            
    b_cols = st.columns(4)
    for idx, b_item in enumerate(recommended_bans[:4]):
        with b_cols[idx % 4]:
            st.markdown(f"""
            <div class="hero-card">
                <span class="badge-s">PRIO BAN</span>
                <h4>{b_item['hero']}</h4>
                <div class="stat-text">{b_item['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    
    st.markdown("#### 💡 RECOMMENDED NEXT PICKS PER ROLE")
    rec_cols = st.columns(5)
    
    for idx, r in enumerate(roles):
        p_name = active_lineup.get(r, "")
        p_pool = PLAYER_POOLS.get(p_name, [])
        
        # Calculate best candidate for role
        candidates = []
        for h in HERO_DB:
            if h["role"] == r and h["name"] not in all_unavailable:
                score = 50
                if h["tier"] == "S": score += 20
                if h["name"] in p_pool: score += 25
                if is_red_side and h.get("red_bias"): score += 15
                
                # Check synergies with our locked picks
                for locked_r, locked_h in st.session_state.our_picks.items():
                    if locked_h and locked_h in h["synergies"]:
                        score += 15
                        
                candidates.append((h, score))
                
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        with rec_cols[idx]:
            st.markdown(f"**{r}** ({p_name})")
            if candidates:
                best_h, b_score = candidates[0]
                is_comfort = best_h['name'] in p_pool
                badge_class = "badge-comfort" if is_comfort else "badge-s"
                badge_text = "COMFORT" if is_comfort else "META S"
                
                img_url = best_h.get("img", AVATAR_BASE)
                
                st.markdown(f"""
                <div class="hero-card">
                    <img src="{img_url}" class="hero-img" alt="{best_h['name']}">
                    <br>
                    <span class="{badge_class}">{badge_text}</span>
                    <h5>{best_h['name']}</h5>
                    <div class="stat-text">WR: {best_h['win_rate']}% | Tier {best_h['tier']}</div>
                    <div class="stat-text"><b>Score: {b_score} Pts</b></div>
                    <div style="font-size:0.75rem; color:#f9e2af; margin-top:4px;">{best_h['specialty']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("No hero available")

    # Probability Score Gauge
    total_score = 0
    picked_count = 0
    for r, h_name in st.session_state.our_picks.items():
        if h_name:
            picked_count += 1
            h_info = next((item for item in HERO_DB if item["name"] == h_name), None)
            if h_info:
                total_score += 80 if h_info["tier"] == "S" else 65
                if h_info["name"] in PLAYER_POOLS.get(active_lineup.get(r, ""), []):
                    total_score += 20

    win_prob = min(85.0, round(50.0 + (total_score / 500.0) * 35.0, 1)) if picked_count > 0 else 50.0
    
    st.markdown("---")
    st.markdown(f"### 📈 ESTIMATED DRAFT WIN PROBABILITY: <span class='win-badge'>{win_prob}%</span>", unsafe_allow_html=True)
    st.progress(int(win_prob))

# ==========================================
# TAB 3: RECENT MATCH LOG & ANALYSIS
# ==========================================
with tab_matches:
    st.subheader("📊 Recent Match Log & Direct Performance Analysis")
    
    match_history = load_match_history()
    
    col_m1, col_m2 = st.columns([1, 2])
    
    with col_m1:
        st.markdown("### 📝 Log New Match Result")
        with st.form("match_form"):
            m_title = st.text_input("Match Title / Opponent:", value="Scrim vs Team Apex")
            m_result = st.selectbox("Match Result:", ["WIN 🏆", "LOSS ❌"])
            m_score = st.text_input("KDA Score (Kills - Deaths):", value="18 - 9")
            m_duration = st.text_input("Duration (e.g. 14:25):", value="15:10")
            m_mvp = st.selectbox("MVP Player:", ["Reyhan", "Dapid", "Delfos", "Virel", "Kafel", "Bahimut / Bah"])
            m_notes = st.text_area("Coach Notes / Takeaways:", value="Dharma wall slam late game berhasil follow up Lady Sun. Rebut Tyrant 10 min.")
            
            submit_match = st.form_submit_button("💾 Save Match Record")
            
            if submit_match:
                new_entry = {
                    "id": len(match_history) + 1,
                    "title": m_title,
                    "draft_name": st.session_state.draft_title,
                    "result": m_result,
                    "score": m_score,
                    "duration": m_duration,
                    "mvp": m_mvp,
                    "notes": m_notes,
                    "picks": dict(st.session_state.our_picks)
                }
                match_history.append(new_entry)
                save_match_history(match_history)
                st.success("Match Record saved successfully!")
                st.rerun()

    with col_m2:
        st.markdown("### 📜 Match History & Analytics")
        if match_history:
            total_matches = len(match_history)
            wins = sum(1 for m in match_history if "WIN" in m["result"])
            win_rate_match = round((wins / total_matches) * 100, 1)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Matches Logged", total_matches)
            c2.metric("Wins", wins)
            c3.metric("Match Win Rate", f"{win_rate_match}%")
            
            st.markdown("---")
            for m in reversed(match_history):
                res_class = "win-badge" if "WIN" in m["result"] else "loss-badge"
                with st.expander(f"Match #{m['id']}: {m['title']} - {m['result']} ({m['score']})"):
                    st.markdown(f"**Draft Name:** `{m['draft_name']}`")
                    st.markdown(f"**Duration:** {m['duration']} | **MVP:** {m['mvp']}")
                    st.markdown(f"**Coach Notes:** {m['notes']}")
                    
                    st.markdown("**Lineup Picks:**")
                    p_str = " | ".join([f"{r}: {h}" for r, h in m['picks'].items() if h])
                    st.write(p_str)
        else:
            st.info("No recent match records logged yet. Fill out the form on the left to save your first match analysis!")

# ==========================================
# TAB 4: EXPORT TO WHATSAPP
# ==========================================
with tab_whatsapp:
    st.subheader("📲 Export Formatted Draft to WhatsApp")
    
    p_clash = st.session_state.our_picks['Clash'] or 'TBD'
    p_jungle = st.session_state.our_picks['Jungle'] or 'TBD'
    p_mid = st.session_state.our_picks['Mid'] or 'TBD'
    p_farm = st.session_state.our_picks['Farm'] or 'TBD'
    p_roam = st.session_state.our_picks['Roam'] or 'TBD'
    
    b_our = ", ".join(st.session_state.our_bans) if st.session_state.our_bans else "None"
    b_enemy = ", ".join(st.session_state.enemy_bans) if st.session_state.enemy_bans else "None"
    
    wa_text = f"""📋 *BLUEPRINT DRAFT: {st.session_state.draft_title.upper()}* 🎮🔥

*ACTIVE LINEUP & HERO PICKS:*
• *Clash Lane ({active_lineup['Clash']}):* {p_clash}
• *Jungle ({active_lineup['Jungle']}):* {p_jungle}
• *Mid Lane ({active_lineup['Mid']}):* {p_mid}
• *Farm Lane ({active_lineup['Farm']}):* {p_farm}
• *Roamer ({active_lineup['Roam']}):* {p_roam}

---
🚫 *BAN STATUS:*
• *Our Bans:* {b_our}
• *Enemy Bans:* {b_enemy}

📈 *ESTIMATED WIN PROBABILITY:* {win_prob}%

*Bismillah, main disiplin, info visi jalan, bantai semuanya! Let's go!* 🚀🔥
"""
    
    st.text_area("Copy Text Below & Paste to WhatsApp Group:", value=wa_text, height=300)
    st.info("💡 Simply select all text in the box above, copy (Ctrl+C), and paste directly into your WhatsApp team group!")

    ban_recoms = []
    for threat in ENEMY_THREAT_BAN_RECOMMENDATIONS:
        if threat not in our_bans and threat not in enemy_bans and threat not in st.session_state['used_heroes']:
            ban_recoms.append(threat)
    st.warning(f"**Prioritas BAN Wajib:** {', '.join(ban_recoms[:4])}")
    st.caption("Alasan: Mengcover weakness pool pemain aktif (Mai Shiranui, Luna, Jing) atau mematikan power-pick musuh.")

    st.markdown("---")

    # 2. PICK RECOMMENDATIONS & CALCULATOR
    st.markdown("#### 💡 Recommended Picks per Role")
    
    # Combine active player comfort pools
    active_comfort_pool = []
    for player in active_players:
        if player in PLAYER_POOLS:
            active_comfort_pool.extend(PLAYER_POOLS[player])
    
    # Calculate Scores for each hero in DB
    scored_heroes = []
    for hero in HERO_DB:
        h_name = hero["name"]
        
        # Check if unavailable (Fearless lock, banned, or picked)
        if h_name in st.session_state['used_heroes'] or h_name in our_bans or h_name in enemy_bans or h_name in our_picks or h_name in enemy_picks:
            continue
            
        score = 0
        badges = []
        
        # Base Tier
        if hero["tier"] == "S":
            score += 40
            badges.append("S-Tier")
        else:
            score += 25
            
        # Player Comfort Match
        if h_name in active_comfort_pool:
            score += 25
            badges.append("🔥 Comfort Pick")
            
        # Red Side Bias
        if "Red Side" in our_side and hero["red_bias"]:
            score += 20
            badges.append("🚩 Red-Side 80% WR")
            
        # Synergy with Ally Picks
        for ally in our_picks:
            if ally in hero["synergies"]:
                score += 20
                badges.append(f"⚡ Synergy ({ally})")
                
        # Counter vs Enemy Picks
        for enemy in enemy_picks:
            if enemy in hero["counters"]:
                score += 25
                badges.append(f"🛡️ Counter ({enemy})")

        scored_heroes.append({
            "name": h_name,
            "role": hero["role"],
            "tier": hero["tier"],
            "score": score,
            "badges": " | ".join(badges)
        })

    df_scores = pd.DataFrame(scored_heroes)
    
    if not df_scores.empty:
        df_scores = df_scores.sort_values(by="score", ascending=False)
        
        roles = ["Clash", "Jungle", "Mid", "Farm", "Roam"]
        tabs = st.tabs(roles)
        
        for idx, role in enumerate(roles):
            with tabs[idx]:
                df_role = df_scores[df_scores["role"] == role].head(4)
                for _, row in df_role.iterrows():
                    st.markdown(f"**{row['name']}** (Score: {row['score']} Pts)")
                    st.caption(f"Tags: {row['badges']}")
                    st.markdown("---")
    else:
        st.info("Pilih phase ban & pick untuk melihat kalkulasi rekomendasi real-time!")

    # 3. GAME 7 EMERGENCY BLIND PICK GENERATOR
    st.markdown("#### 🚨 Game 7 Blind Pick Generator (3-Menit)")
    if st.button("⚡ Generate Game 7 Blind Pick (Instant Comfort 5)"):
        g7_lineup = []
        roles_needed = ["Clash", "Jungle", "Mid", "Farm", "Roam"]
        
        for role in roles_needed:
            # Pick highest score comfort hero per role
            candidates = df_scores[(df_scores["role"] == role) & (df_scores["name"].isin(active_comfort_pool))]
            if not candidates.empty:
                g7_lineup.append(f"**{role}:** {candidates.iloc[0]['name']}")
            else:
                fallback = df_scores[df_scores["role"] == role]
                if not fallback.empty:
                    g7_lineup.append(f"**{role}:** {fallback.iloc[0]['name']}")
                    
        st.success("Lineup Darurat Game 7 Siap Digunakan:")
        for l in g7_lineup:
            st.write(l)
        st.warning("⚠️ Ingat: Tulis persis di kertas draf & serahkan ke refree dalam 3 menit biar gak denda 30%!")
