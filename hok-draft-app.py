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
    st.markdown("#### 🎯 Top Target Ban Recommendations")
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
