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
    {"name": "Biron", "role": "Clash", "tier": "S", "win_rate": 54.2, "pick_rate": 28.5, "ban_rate": 18.1, "red_bias": False, "counters": ["Physical Fighters"], "synergies": ["Dun", "Zhang Fei"], "avatar": "⚡"},
    {"name": "Florentino", "role": "Clash", "tier": "S", "win_rate": 53.8, "pick_rate": 22.1, "ban_rate": 35.4, "red_bias": False, "counters": ["Tank Heavy"], "synergies": ["Yaria"], "avatar": "🌹"},
    {"name": "Dharma", "role": "Clash", "tier": "S", "win_rate": 52.9, "pick_rate": 19.8, "ban_rate": 12.3, "red_bias": False, "counters": ["Immobile Squishies"], "synergies": ["Lady Sun", "Yao"], "avatar": "👊"},
    {"name": "Allain", "role": "Clash", "tier": "A", "win_rate": 51.5, "pick_rate": 16.4, "ban_rate": 8.7, "red_bias": False, "counters": ["Squishy Carry"], "synergies": ["Wang Zhaojun"], "avatar": "⚔️"},
    {"name": "Sun Ce", "role": "Clash", "tier": "A", "win_rate": 51.2, "pick_rate": 18.2, "ban_rate": 11.0, "red_bias": False, "counters": ["Split Pushers"], "synergies": ["Da Qiao", "Nuwa"], "avatar": "⛵"},
    {"name": "Fatih", "role": "Clash", "tier": "A", "win_rate": 50.8, "pick_rate": 14.1, "ban_rate": 6.2, "red_bias": False, "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"], "avatar": "🛡️"},
    
    # Jungle
    {"name": "Lam", "role": "Jungle", "tier": "S", "win_rate": 55.6, "pick_rate": 32.1, "ban_rate": 48.9, "red_bias": False, "counters": ["Low HP Squishies"], "synergies": ["Yaria", "Angela"], "avatar": "🦈"},
    {"name": "Augran", "role": "Jungle", "tier": "S", "win_rate": 54.8, "pick_rate": 30.4, "ban_rate": 42.1, "red_bias": False, "counters": ["Wall Huggers"], "synergies": ["Biron", "Zhang Fei"], "avatar": "👻"},
    {"name": "Feyd", "role": "Jungle", "tier": "S", "win_rate": 53.4, "pick_rate": 24.2, "ban_rate": 29.8, "red_bias": False, "counters": ["Backline MM"], "synergies": ["Kui", "Devara"], "avatar": "🗡️"},
    {"name": "Li Bai", "role": "Jungle", "tier": "A", "win_rate": 51.9, "pick_rate": 18.7, "ban_rate": 15.2, "red_bias": False, "counters": ["Immobile Mages"], "synergies": ["Kui", "Nuwa"], "avatar": "🍾"},
    {"name": "Pei", "role": "Jungle", "tier": "A", "win_rate": 51.1, "pick_rate": 15.3, "ban_rate": 10.4, "red_bias": False, "counters": ["Slow Early Junglers"], "synergies": ["Biron", "Devara"], "avatar": "🐅"},
    {"name": "Musashi", "role": "Jungle", "tier": "A", "win_rate": 50.9, "pick_rate": 14.8, "ban_rate": 7.8, "red_bias": False, "counters": ["Healers"], "synergies": ["Dolia"], "avatar": "⚔️"},
    {"name": "Kaizer", "role": "Jungle", "tier": "A", "win_rate": 50.7, "pick_rate": 16.1, "ban_rate": 9.1, "red_bias": False, "counters": ["Burst Assassins"], "synergies": ["Zhang Fei"], "avatar": "🛡️"},
    {"name": "Ukyo", "role": "Jungle", "tier": "A", "win_rate": 50.2, "pick_rate": 12.5, "ban_rate": 5.3, "red_bias": False, "counters": ["Early Squishies"], "synergies": ["Mozi"], "avatar": "🍎"},
    {"name": "Xuance", "role": "Jungle", "tier": "A", "win_rate": 50.0, "pick_rate": 11.8, "ban_rate": 6.7, "red_bias": False, "counters": ["Immobile Carries"], "synergies": ["Mozi", "Dun"], "avatar": "🪝"},

    # Mid Lane
    {"name": "Haya", "role": "Mid", "tier": "S", "win_rate": 80.0, "pick_rate": 21.0, "ban_rate": 38.0, "red_bias": True, "counters": ["Cluster Comps"], "synergies": ["Feyd", "Li Bai"], "avatar": "🌙"},
    {"name": "Wang Zhaojun", "role": "Mid", "tier": "S", "win_rate": 53.9, "pick_rate": 25.1, "ban_rate": 22.4, "red_bias": False, "counters": ["Dive Comps"], "synergies": ["Biron", "Lady Sun"], "avatar": "❄️"},
    {"name": "Xiao Qiao", "role": "Mid", "tier": "S", "win_rate": 53.2, "pick_rate": 26.8, "ban_rate": 14.5, "red_bias": False, "counters": ["Clustered Enemies"], "synergies": ["Mozi", "Dun", "Arli"], "avatar": "🪭"},
    {"name": "Lorion", "role": "Mid", "tier": "S", "win_rate": 52.8, "pick_rate": 19.4, "ban_rate": 18.2, "red_bias": False, "counters": ["Tight Formations"], "synergies": ["Pei", "Devara"], "avatar": "🔮"},
    {"name": "Nuwa", "role": "Mid", "tier": "A", "win_rate": 51.6, "pick_rate": 13.2, "ban_rate": 8.9, "red_bias": False, "counters": ["Long-range Seige"], "synergies": ["Sun Ce", "Li Bai"], "avatar": "✨"},
    {"name": "Angela", "role": "Mid", "tier": "A", "win_rate": 51.0, "pick_rate": 22.3, "ban_rate": 9.5, "red_bias": False, "counters": ["Frontline Tanks"], "synergies": ["Lam", "Zhang Fei"], "avatar": "🔥"},
    {"name": "Yixing", "role": "Mid", "tier": "S", "win_rate": 54.1, "pick_rate": 18.5, "ban_rate": 21.0, "red_bias": False, "counters": ["No-escape Comps"], "synergies": ["Dharma", "Lady Sun"], "avatar": "♟️"},
    {"name": "Kui", "role": "Mid", "tier": "A", "win_rate": 50.4, "pick_rate": 15.6, "ban_rate": 12.1, "red_bias": False, "counters": ["Immobile Carries"], "synergies": ["Li Bai", "Feyd", "Nuwa"], "avatar": "🪝"},
    {"name": "Heino", "role": "Mid", "tier": "S", "win_rate": 53.5, "pick_rate": 20.1, "ban_rate": 26.3, "red_bias": False, "counters": ["Attrition Comps"], "synergies": ["Dolia"], "avatar": "⏳"},

    # Farm Lane (MM)
    {"name": "Lady Sun", "role": "Farm", "tier": "S", "win_rate": 54.5, "pick_rate": 29.2, "ban_rate": 24.1, "red_bias": False, "counters": ["Low Mobility Tanks"], "synergies": ["Yaria", "Dharma", "Yao"], "avatar": "💥"},
    {"name": "Ao'yin (Loong)", "role": "Farm", "tier": "S", "win_rate": 72.2, "pick_rate": 28.0, "ban_rate": 45.0, "red_bias": True, "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia"], "avatar": "🐉"},
    {"name": "Arli", "role": "Farm", "tier": "S", "win_rate": 53.8, "pick_rate": 24.6, "ban_rate": 31.2, "red_bias": False, "counters": ["Skillshot Mages"], "synergies": ["Mozi", "Xiao Qiao"], "avatar": "☂️"},
    {"name": "Flowborn (MM)", "role": "Farm", "tier": "S", "win_rate": 53.1, "pick_rate": 21.3, "ban_rate": 19.8, "red_bias": False, "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce"], "avatar": "🏹"},
    {"name": "Luara", "role": "Farm", "tier": "A", "win_rate": 51.4, "pick_rate": 17.5, "ban_rate": 11.2, "red_bias": False, "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun"], "avatar": "🧗"},
    {"name": "Marco Polo", "role": "Farm", "tier": "A", "win_rate": 50.8, "pick_rate": 27.1, "ban_rate": 15.6, "red_bias": False, "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei"], "avatar": "🔫"},

    # Roam
    {"name": "Zhang Fei", "role": "Roam", "tier": "S", "win_rate": 65.5, "pick_rate": 31.0, "ban_rate": 28.0, "red_bias": True, "counters": ["Heavy Dive"], "synergies": ["Lady Sun", "Angela"], "avatar": "👺"},
    {"name": "Yaria", "role": "Roam", "tier": "S", "win_rate": 53.8, "pick_rate": 26.5, "ban_rate": 36.1, "red_bias": False, "counters": ["Burst Single Target"], "synergies": ["Lady Sun", "Lam", "Loong"], "avatar": "🦌"},
    {"name": "Dolia", "role": "Roam", "tier": "S", "win_rate": 54.0, "pick_rate": 23.8, "ban_rate": 41.2, "red_bias": False, "counters": ["Short War Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"], "avatar": "🧜‍♀️"},
    {"name": "Devara", "role": "Roam", "tier": "A", "win_rate": 51.2, "pick_rate": 16.9, "ban_rate": 10.5, "red_bias": False, "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"], "avatar": "🗼"},
    {"name": "Mozi", "role": "Roam", "tier": "S", "win_rate": 52.9, "pick_rate": 20.4, "ban_rate": 17.3, "red_bias": False, "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "avatar": "🤖"},
    {"name": "Dun", "role": "Roam", "tier": "A", "win_rate": 50.6, "pick_rate": 18.1, "ban_rate": 8.4, "red_bias": False, "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "avatar": "🛡️"},
    {"name": "Da Qiao", "role": "Roam", "tier": "S", "win_rate": 53.4, "pick_rate": 19.2, "ban_rate": 33.5, "red_bias": False, "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli"], "avatar": "🌊"}
]

PLAYER_POOLS = {
    "Delfos": ["Fatih", "Biron", "Allain", "Devara", "Dharma", "Zhang Fei", "Dun"],
    "Dapid": ["Augran", "Feyd", "Lam", "Chicha", "Flowborn (MM)", "Menki", "Li Bai", "Pei", "Dun", "Musashi", "Kaizer", "Ukyo", "Xuance"],
    "Kafel": ["Wang Zhaojun", "Angela", "Yixing", "Biron", "Sun Ce", "Xiao Qiao"],
    "Virel": ["Zhang Fei", "Biron", "Dharma", "Allain", "Dun"],
    "Bah": ["Haya", "Lorion", "Nuwa", "Kui", "Lady Sun", "Marco Polo", "Arli"],
    "Reyhan": ["Lady Sun", "Arli", "Flowborn (MM)", "Luara", "Marco Polo"]
}

ENEMY_THREAT_BAN_RECOMMENDATIONS = ["Mai Shiranui", "Luna", "Jing", "Shangguan", "Florentino", "Dolia", "Lam"]

# Initialize Session States
if 'used_heroes' not in st.session_state:
    st.session_state['used_heroes'] = []

if 'recent_matches' not in st.session_state:
    st.session_state['recent_matches'] = []

# ==========================================
# HEADER & SIDEBAR CONFIG
# ==========================================
st.markdown("<p class='main-title'>⚔️ HOK REAL-TIME DRAFT ASSISTANT ⚔️</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Strategy & Probability Engine - Season 16 Meta | By Siropkokop</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Match Configuration")
    
    # Custom Draft Name
    custom_draft_name = st.text_input("📝 Custom Draft Name", "Draft Unli CC - Biron & Xiao Qiao Stun Lock")
    
    # Lineup Selector
    selected_lineup = st.selectbox(
        "👥 Select Team Lineup",
        ["Lineup 1 (Delfos, Dapid, Kafel, Virel, Reyhan)",
         "Lineup 2 (Virel, Dapid, Kafel, Delfos, Bah)",
         "Lineup 3 (Delfos, Dapid, Bah, Virel, Reyhan)",
         "Lineup 4 (Kafel, Dapid, Bah, Delfos, Reyhan)"]
    )
    
    # Active Players mapping
    if "Lineup 1" in selected_lineup:
        active_players = ["Delfos", "Dapid", "Kafel", "Virel", "Reyhan"]
    elif "Lineup 2" in selected_lineup:
        active_players = ["Virel", "Dapid", "Kafel", "Delfos", "Bah"]
    elif "Lineup 3" in selected_lineup:
        active_players = ["Delfos", "Dapid", "Bah", "Virel", "Reyhan"]
    else:
        active_players = ["Kafel", "Dapid", "Bah", "Delfos", "Reyhan"]
        
    st.info(f"**Active Players:** {', '.join(active_players)}")
    
    # Side Bias
    is_red_side = st.checkbox("🔴 Red Side (Sisi Merah - Last Pick R5)", value=False)
    game_number = st.slider("🎮 Game Series Number (Fearless Draft)", 1, 7, 1)
    
    st.markdown("---")
    st.subheader("🔒 Fearless Memory Tracker")
    st.caption("Hero yang sudah dipakai di game sebelumnya (Auto-Lock):")
    st.write(st.session_state['used_heroes'] if st.session_state['used_heroes'] else "Belum ada hero terpakai.")
    if st.button("🔄 Reset Fearless Memory"):
        st.session_state['used_heroes'] = []
        st.rerun()

# ==========================================
# MAIN LAYOUT TABS
# ==========================================
tab_draft, tab_next_schema, tab_db, tab_history, tab_export = st.tabs([
    "⚔️ Real-Time B/P Interactive",
    "💡 Next Pick & Ban Schema",
    "📚 Hero Database & Stats",
    "📊 Recent Match Analysis",
    "📱 Copy to WhatsApp"
])

# Helper function to get available heroes (filtering out used, picked, banned)
def get_available_hero_names(selected_and_banned, role=None):
    banned_or_picked = set(selected_and_banned + st.session_state['used_heroes'])
    names = []
    for h in HERO_DB:
        if h["name"] not in banned_or_picked:
            if role is None or h["role"] == role:
                names.append(f"{h['avatar']} {h['name']} ({h['role']} - {h['tier']}-Tier)")
    return sorted(names)

def clean_hero_name(formatted_name):
    if not formatted_name or formatted_name == "None":
        return None
    # Strip avatar emoji and (Role - Tier)
    parts = formatted_name.split(" ")
    if len(parts) >= 2:
        # Find hero name between avatar and '('
        name = " ".join(parts[1:]).split("(")[0].strip()
        return name
    return formatted_name

# ==========================================
# TAB 1: REAL-TIME B/P INTERACTIVE
# ==========================================
with tab_draft:
    st.subheader(f"📌 {custom_draft_name}")
    
    col_bans, col_picks = st.columns([1, 2])
    
    with col_bans:
        st.markdown("### 🚫 BAN PHASE")
        st.caption("Hero yang di-ban tidak akan muncul lagi di pilihan Pick.")
        
        # We need to collect current bans first to filter pick dropdowns
        our_ban_1_raw = st.selectbox("Our Ban 1", ["None"] + get_available_hero_names([]), key="ob1")
        our_ban_2_raw = st.selectbox("Our Ban 2", ["None"] + get_available_hero_names([clean_hero_name(our_ban_1_raw)]), key="ob2")
        
        current_banned_so_far = [clean_hero_name(our_ban_1_raw), clean_hero_name(our_ban_2_raw)]
        current_banned_so_far = [x for x in current_banned_so_far if x]
        
        enemy_ban_1_raw = st.selectbox("Enemy Ban 1", ["None"] + get_available_hero_names(current_banned_so_far), key="eb1")
        enemy_ban_2_raw = st.selectbox("Enemy Ban 2", ["None"] + get_available_hero_names(current_banned_so_far + [clean_hero_name(enemy_ban_1_raw)]), key="eb2")
        
        our_bans = [x for x in [clean_hero_name(our_ban_1_raw), clean_hero_name(our_ban_2_raw)] if x]
        enemy_bans = [x for x in [clean_hero_name(enemy_ban_1_raw), clean_hero_name(enemy_ban_2_raw)] if x]
        
        all_banned = list(set(our_bans + enemy_bans))
    
    with col_picks:
        st.markdown("### 🛡️ OUR TEAM PICKS (BLUE / RED)")
        
        all_unavailable = list(set(all_banned + st.session_state['used_heroes']))
        
        c_clash, c_jungle, c_mid, c_farm, c_roam = st.columns(5)
        
        with c_clash:
            clash_pick_raw = st.selectbox("Clash Lane", ["None"] + get_available_hero_names(all_unavailable, "Clash"), key="p_clash")
        with c_jungle:
            jungle_pick_raw = st.selectbox("Jungle", ["None"] + get_available_hero_names(all_unavailable, "Jungle"), key="p_jungle")
        with c_mid:
            mid_pick_raw = st.selectbox("Mid Lane", ["None"] + get_available_hero_names(all_unavailable, "Mid"), key="p_mid")
        with c_farm:
            farm_pick_raw = st.selectbox("Farm Lane", ["None"] + get_available_hero_names(all_unavailable, "Farm"), key="p_farm")
        with c_roam:
            roam_pick_raw = st.selectbox("Roamer", ["None"] + get_available_hero_names(all_unavailable, "Roam"), key="p_roam")
            
        our_picks = [clean_hero_name(x) for x in [clash_pick_raw, jungle_pick_raw, mid_pick_raw, farm_pick_raw, roam_pick_raw] if clean_hero_name(x)]
        
        st.markdown("---")
        st.markdown("### 🎯 ENEMY PICKS")
        
        all_unavailable_with_picks = list(set(all_unavailable + our_picks))
        
        ec1, ec2, ec3, ec4, ec5 = st.columns(5)
        with ec1: ep1_raw = st.selectbox("Enemy 1", ["None"] + get_available_hero_names(all_unavailable_with_picks), key="ep1")
        with ec2: ep2_raw = st.selectbox("Enemy 2", ["None"] + get_available_hero_names(all_unavailable_with_picks), key="ep2")
        with ec3: ep3_raw = st.selectbox("Enemy 3", ["None"] + get_available_hero_names(all_unavailable_with_picks), key="ep3")
        with ec4: ep4_raw = st.selectbox("Enemy 4", ["None"] + get_available_hero_names(all_unavailable_with_picks), key="ep4")
        with ec5: ep5_raw = st.selectbox("Enemy 5", ["None"] + get_available_hero_names(all_unavailable_with_picks), key="ep5")
        
        enemy_picks = [clean_hero_name(x) for x in [ep1_raw, ep2_raw, ep3_raw, ep4_raw, ep5_raw] if clean_hero_name(x)]

    # Save to Fearless Memory Button
    if st.button("💾 Simpan Hero Terpakai ke Fearless Memory (End Game)"):
        for hero in our_picks:
            if hero not in st.session_state['used_heroes']:
                st.session_state['used_heroes'].append(hero)
        st.success("Hero berhasil disimpan ke Fearless Memory!")
        st.rerun()

# ==========================================
# TAB 2: NEXT PICK & BAN SCHEMA
# ==========================================
with tab_next_schema:
    st.subheader("💡 Real-Time Next Pick & Ban Strategy Schema")
    
    # CALCULATE PROBABILITY SCORE
    base_score = 50
    score_breakdown = []
    
    # Tier bonuses
    for hero in our_picks:
        h_data = next((x for x in HERO_DB if x['name'] == hero), None)
        if h_data:
            if h_data['tier'] == 'S':
                base_score += 8
                score_breakdown.append(f"+8 Pts: {hero} (S-Tier Meta)")
            else:
                base_score += 4
                score_breakdown.append(f"+4 Pts: {hero} (A-Tier Meta)")
                
            if is_red_side and h_data['red_bias']:
                base_score += 7
                score_breakdown.append(f"+7 Pts: {hero} (Red Side High Winrate)")
                
            # Comfort check
            for player in active_players:
                if player in PLAYER_POOLS and hero in PLAYER_POOLS[player]:
                    base_score += 5
                    score_breakdown.append(f"+5 Pts: {hero} is Comfort Pick for {player}")
                    break

    win_prob = min(base_score, 95)
    
    col_gauge, col_recom_details = st.columns([1, 2])
    
    with col_gauge:
        st.metric("Estimated Win Probability", f"{win_prob}%", delta=f"{win_prob - 50}% vs Avg")
        st.progress(win_prob / 100.0)
        st.markdown("**Score Breakdown:**")
        for item in score_breakdown:
            st.caption(item)
            
    with col_recom_details:
        st.markdown("#### 🎯 Recommended NEXT BAN Targets")
        rec_bans = [b for b in ENEMY_THREAT_BAN_RECOMMENDATIONS if b not in our_bans and b not in enemy_bans and b not in st.session_state['used_heroes']]
        for b in rec_bans[:4]:
            st.warning(f"🚫 **{b}** — High threat against active roster weakness.")
            
        st.markdown("#### 💡 Recommended NEXT PICKS per Role")
        
        roles = ["Clash", "Jungle", "Mid", "Farm", "Roam"]
        r_cols = st.columns(5)
        
        for idx, r in enumerate(roles):
            with r_cols[idx]:
                st.write(f"**{r} Lane:**")
                avail_r = [h for h in HERO_DB if h['role'] == r and h['name'] not in our_picks and h['name'] not in enemy_picks and h['name'] not in all_banned and h['name'] not in st.session_state['used_heroes']]
                avail_r = sorted(avail_r, key=lambda x: x['win_rate'], reverse=True)
                
                for top_h in avail_r[:2]:
                    st.markdown(f"{top_h['avatar']} **{top_h['name']}**")
                    st.caption(f"WR: {top_h['win_rate']}% | Tier {top_h['tier']}")

# ==========================================
# TAB 3: HERO DATABASE & STATS
# ==========================================
with tab_db:
    st.subheader("📚 Honor of Kings Season 16 Complete Hero Database")
    
    df_heroes = pd.DataFrame(HERO_DB)
    df_heroes = df_heroes[["name", "role", "tier", "win_rate", "pick_rate", "ban_rate", "counters", "synergies"]]
    df_heroes.columns = ["Hero Name", "Role", "Tier", "Win Rate (%)", "Pick Rate (%)", "Ban Rate (%)", "Counters", "Synergies"]
    
    role_filter = st.multiselect("Filter by Role", ["Clash", "Jungle", "Mid", "Farm", "Roam"], default=["Clash", "Jungle", "Mid", "Farm", "Roam"])
    df_filtered = df_heroes[df_heroes["Role"].isin(role_filter)]
    
    st.dataframe(df_filtered, use_container_width=True)

# ==========================================
# TAB 4: RECENT MATCH ANALYSIS
# ==========================================
with tab_history:
    st.subheader("📊 Recent Scrim & Match Log Upload")
    
    with st.form("add_match_form"):
        st.markdown("### 📝 Log New Match Result")
        m_opp = st.text_input("Opponent / Scrim Team", "EVOS / KPL Academy")
        m_res = st.selectbox("Result", ["WIN 🏆", "LOSS ❌"])
        m_dur = st.text_input("Match Duration", "15:42")
        m_mvp = st.text_input("MVP Player", "Dapid (Augran)")
        m_notes = st.text_area("Coach Notes & Analysis", "Lini depan tebal, inisiasi Dharma bagus. Catatan: Yixing sempat diculik Nezha di menit 8.")
        
        submit_match = st.form_submit_button("💾 Save Match to History")
        if submit_match:
            st.session_state['recent_matches'].append({
                "Opponent": m_opp,
                "Result": m_res,
                "Duration": m_dur,
                "MVP": m_mvp,
                "Notes": m_notes,
                "Draft": custom_draft_name
            })
            st.success("Match berhasil disimpan!")
            st.rerun()
            
    st.markdown("---")
    st.markdown("### 📜 Match History Log")
    if st.session_state['recent_matches']:
        for i, m in enumerate(reversed(st.session_state['recent_matches'])):
            with st.expander(f"Match #{len(st.session_state['recent_matches'])-i}: {m['Result']} vs {m['Opponent']} ({m['Draft']})"):
                st.write(f"**Duration:** {m['Duration']} | **MVP:** {m['MVP']}")
                st.write(f"**Coach Analysis:** {m['Notes']}")
    else:
        st.info("Belum ada match history yang disimpan.")

# ==========================================
# TAB 5: COPY TO WHATSAPP
# ==========================================
with tab_export:
    st.subheader("📱 Export Draft Summary to WhatsApp")
    
    wa_text = f"""*BLUEPRINT DRAFT MATCH* 🎮🔥
*Draft Name:* {custom_draft_name}
*Lineup:* {selected_lineup}
*Side:* {"🔴 Red Side" if is_red_side else "🔵 Blue Side"} | *Game:* #{game_number}

🚫 *OUR BANS:* {', '.join(our_bans) if our_bans else 'None'}
🚫 *ENEMY BANS:* {', '.join(enemy_bans) if enemy_bans else 'None'}

🛡️ *OUR PICKS:*
• Clash: {clash_pick_raw}
• Jungle: {jungle_pick_raw}
• Mid: {mid_pick_raw}
• Farm: {farm_pick_raw}
• Roamer: {roam_pick_raw}

🎯 *ESTIMATED WIN PROBABILITY:* {win_prob}%

*Keep focus & build chemistry!* 🚀🔥"""

    st.code(wa_text, language="markdown")
    st.caption("Klik tombol copy di kanan atas kotak kode di atas, lalu paste ke WhatsApp tim!")
