import streamlit as st
import pandas as pd
import json

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Pro Draft Engine | By Siropkokop",
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
        margin-bottom: 10px;
    }
    .metric-box {
        background-color: #11111B;
        border-left: 5px solid #FFD700;
        padding: 12px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .alert-danger {
        background-color: #3d0c11;
        border-left: 5px solid #e74c3c;
        color: #ff9999;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 8px;
        font-weight: bold;
    }
    .alert-success {
        background-color: #0d381e;
        border-left: 5px solid #2ecc71;
        color: #88ffb8;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 8px;
        font-weight: bold;
    }
    .badge-s { background-color: #E74C3C; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .badge-a { background-color: #F39C12; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .badge-role { background-color: #3498DB; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'used_heroes' not in st.session_state:
    st.session_state['used_heroes'] = []
if 'game_number' not in st.session_state:
    st.session_state['game_number'] = 1
if 'match_history' not in st.session_state:
    st.session_state['match_history'] = []

# ==========================================
# COMPLETE HERO DATABASE SEASON 16 (BY ROLE)
# ==========================================
HERO_DB = {
    "Clash": [
        {"name": "Biron", "tier": "S", "wr": 54.2, "pr": "28.5%", "br": "15.2%", "counters": ["Physical Fighters", "Melee Assassins"], "synergies": ["Zhang Fei", "Dun", "Angela"], "desc": "Frontline badak dengan shield tebal dan regen stamina gila."},
        {"name": "Florentino", "tier": "S", "wr": 53.8, "pr": "18.2%", "br": "42.1%", "counters": ["Tank Heavy", "Sustained Duelists"], "synergies": ["Yaria", "Dolia"], "desc": "God-tier duelis 1v1 dengan mekanik gocekan bunga frame-perfect."},
        {"name": "Dharma", "tier": "S", "wr": 53.5, "pr": "22.1%", "br": "25.0%", "counters": ["Immobile Squishies", "Wall Huggers"], "synergies": ["Lady Sun", "Yao", "Yixing"], "desc": "Inisiator wall-slam mematikan pembuka war di area sempit."},
        {"name": "Charlotte", "tier": "S", "wr": 53.1, "pr": "17.5%", "br": "18.4%", "counters": ["Attack Speed Carries", "Basic Attackers"], "synergies": ["Zhang Fei", "Wang Zhaojun"], "desc": "Counter alami hero fisik dengan debuff attack speed & damage reduction."},
        {"name": "Allain", "tier": "A", "wr": 51.8, "pr": "19.4%", "br": "10.5%", "counters": ["Squishy Carries", "Shield Tanks"], "synergies": ["Wang Zhaojun", "Dolia"], "desc": "Duelist hybrid physical/magic damage dengan untargetable ulti."},
        {"name": "Sun Ce", "tier": "A", "wr": 51.2, "pr": "15.0%", "br": "8.2%", "counters": ["Split Pushers", "Immobile Carries"], "synergies": ["Da Qiao", "Nuwa", "Arli"], "desc": "Penguasa kapal rotasi global untuk gank cepat antar lane."},
        {"name": "Fatih", "tier": "A", "wr": 50.8, "pr": "12.3%", "br": "5.1%", "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"], "desc": "Fighter crowd control perusak formasi musuh."},
        {"name": "Li Xin", "tier": "A", "wr": 50.5, "pr": "16.8%", "br": "6.0%", "counters": ["Immobile Mages"], "synergies": ["Dolia", "Zhang Fei"], "desc": "Fighter dua wujud: Light (Aoe Burst) & Dark (Fast Split Push)."},
        {"name": "Dun", "tier": "A", "wr": 52.0, "pr": "21.0%", "br": "4.5%", "counters": ["Dive Assassins"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Tank pasak bumi dengan true damage & shield regenerasi."},
        {"name": "Nezha", "tier": "A", "wr": 51.4, "pr": "10.1%", "br": "7.8%", "counters": ["Healers", "Backline Carries"], "synergies": ["Pei", "Nuwa"], "desc": "Lock-on global target dengan debuff anti-heal bawaan."}
    ],
    "Jungle": [
        {"name": "Augran", "tier": "S", "wr": 55.8, "pr": "32.1%", "br": "58.4%", "counters": ["Wall Huggers", "Tank Comps"], "synergies": ["Biron", "Zhang Fei", "Angela"], "desc": "Jungler T0 paling dominan Season 16 dengan wujud jiwa penyerap HP."},
        {"name": "Lam", "tier": "S", "wr": 54.9, "pr": "29.8%", "br": "62.0%", "counters": ["Low HP Squishies", "Immobile Carries"], "synergies": ["Yaria", "Angela", "Wang Zhaojun"], "desc": "Assassin hiu dengan pasif true damage target HP <30%."},
        {"name": "Jing", "tier": "S", "wr": 54.1, "pr": "15.2%", "br": "48.0%", "counters": ["Clustered Comps"], "synergies": ["Yixing", "Dolia"], "desc": "Assassin cermin mekanik tinggi dengan infinite swap dash."},
        {"name": "Luna", "tier": "S", "wr": 53.9, "pr": "11.8%", "br": "52.1%", "counters": ["No-Hard-CC Comps"], "synergies": ["Da Qiao", "Zhang Fei"], "desc": "Mage-Assassin dengan mark reset ulti tanpa batas."},
        {"name": "Feyd", "tier": "S", "wr": 53.9, "pr": "21.4%", "br": "35.2%", "counters": ["Backline MM", "Vision-less Comps"], "synergies": ["Kui", "Devara", "Haya"], "desc": "Assassin bayangan penyergap lini belakang dari fog of war."},
        {"name": "Li Bai", "tier": "A", "wr": 52.1, "pr": "18.5%", "br": "11.2%", "counters": ["Skillshot Mages", "Immobile Carries"], "synergies": ["Kui", "Nuwa", "Devara"], "desc": "Assassin lincah dengan 2 wujud untargetable & dash balik bayangan."},
        {"name": "Pei", "tier": "A", "wr": 51.8, "pr": "14.2%", "br": "19.0%", "counters": ["Slow Early Junglers"], "synergies": ["Biron", "Devara", "Nezha"], "desc": "Jungler wujud harimau dengan power spike invasif sejak menit 0:30."},
        {"name": "Musashi", "tier": "A", "wr": 51.5, "pr": "16.1%", "br": "8.4%", "counters": ["Healers", "Shield Comps"], "synergies": ["Dolia", "Xiao Qiao"], "desc": "Pendekar pemotong shield & pengunci target tunggal."},
        {"name": "Kaizer", "tier": "A", "wr": 52.2, "pr": "24.0%", "br": "5.1%", "counters": ["Burst Assassins"], "synergies": ["Zhang Fei", "Lady Sun"], "desc": "Jungler Tank/Fighter wujud iblis penahan gempuran fisik."},
        {"name": "Ukyo", "tier": "A", "wr": 51.1, "pr": "12.0%", "br": "3.2%", "counters": ["Early Squishies"], "synergies": ["Mozi", "Xiao Qiao"], "desc": "Samurai burst damage jarak menengah dengan lifesteal cepat."},
        {"name": "Xuance", "tier": "A", "wr": 52.0, "pr": "13.5%", "br": "15.1%", "counters": ["No-escape Carries"], "synergies": ["Mozi", "Dun", "Xiao Qiao"], "desc": "Assassin pancing kait pembalik posisi musuh ke belakang."}
    ],
    "Mid": [
        {"name": "Haya", "tier": "S", "wr": 56.2, "pr": "28.0%", "br": "45.1%", "counters": ["Cluster Formations"], "synergies": ["Feyd", "Li Bai", "Augran"], "desc": "Mage S-Tier Red Side Win Rate 80% pemanggil badai bulan."},
        {"name": "Mai Shiranui", "tier": "S", "wr": 54.5, "pr": "18.0%", "br": "55.0%", "counters": ["Squishy Backlines"], "synergies": ["Feyd", "Augran"], "desc": "Mage-Assassin lincah pembebas energi combo sekali putar."},
        {"name": "Wang Zhaojun", "tier": "S", "wr": 54.1, "pr": "31.2%", "br": "22.0%", "counters": ["Dive Comps", "Melee Assassins"], "synergies": ["Biron", "Lady Sun", "Zhang Fei"], "desc": "Mage kontroller es pembeku area dengan shield pembawa pasif slow."},
        {"name": "Yixing", "tier": "S", "wr": 54.0, "pr": "17.8%", "br": "24.5%", "counters": ["No-escape Comps"], "synergies": ["Dharma", "Lady Sun", "Dolia"], "desc": "Mage papan catur pengurung musuh dalam area raksasa."},
        {"name": "Xiao Qiao", "tier": "S", "wr": 53.8, "pr": "35.1%", "br": "18.2%", "counters": ["Chokepoint War"], "synergies": ["Mozi", "Dun", "Arli"], "desc": "Mage poke & knock-up instan dengan burst kipas raksasa."},
        {"name": "Heino", "tier": "S", "wr": 53.7, "pr": "22.1%", "br": "31.0%", "counters": ["Attrition Comps"], "synergies": ["Dolia", "Flowborn (MM)"], "desc": "Mage pemutar waktu reset HP & tower dengan combo Dolia."},
        {"name": "Lorion", "tier": "S", "wr": 53.5, "pr": "19.2%", "br": "28.0%", "counters": ["Tight Formations"], "synergies": ["Pei", "Devara", "Lam"], "desc": "Mage bola elektrik perusak formasi musuh di udara."},
        {"name": "Shangguan", "tier": "A", "wr": 52.8, "pr": "14.2%", "br": "38.2%", "counters": ["Immobile Mages"], "synergies": ["Lam", "Yaria"], "desc": "Mage kuas terbang untargetable pembantai lini belakang."},
        {"name": "Nuwa", "tier": "A", "wr": 52.4, "pr": "11.5%", "br": "9.1%", "counters": ["Long-range Siege"], "synergies": ["Sun Ce", "Nezha", "Li Bai"], "desc": "Mage pencipta matriks tembok & teleportasi matriks peta global."},
        {"name": "Angela", "tier": "A", "wr": 51.9, "pr": "38.0%", "br": "8.5%", "counters": ["Frontline Tanks"], "synergies": ["Lam", "Zhang Fei", "Biron"], "desc": "Mage pembalas burst laser dengan shield CC-immunity."},
        {"name": "Kui", "tier": "A", "wr": 51.1, "pr": "16.4%", "br": "15.0%", "counters": ["Immobile Carries"], "synergies": ["Li Bai", "Feyd", "Nuwa"], "desc": "Mage kait pengisolasi 1 target dari jarak sangat jauh."}
    ],
    "Farm": [
        {"name": "Ao'yin (Loong)", "tier": "S", "wr": 55.2, "pr": "31.0%", "br": "58.0%", "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia", "Zhang Fei"], "desc": "MM naga elemen dengan ulti wujud terbang untargetable."},
        {"name": "Lady Sun", "tier": "S", "wr": 54.8, "pr": "38.5%", "br": "25.0%", "counters": ["Low Mobility Tanks", "Short Range MM"], "synergies": ["Yaria", "Dharma", "Yao"], "desc": "MM S-Tier burst rolled-attack penghancur armor musuh."},
        {"name": "Arli", "tier": "S", "wr": 54.2, "pr": "24.1%", "br": "41.0%", "counters": ["Skillshot Mages", "Melee Inisiators"], "synergies": ["Mozi", "Xiao Qiao", "Da Qiao"], "desc": "MM 3-dash parasut paling lincah dengan penepis proyektil."},
        {"name": "Flowborn (MM)", "tier": "S", "wr": 53.9, "pr": "20.5%", "br": "22.1%", "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce", "Heino"], "desc": "MM fleksibel dengan sistem 5-stack double cast skill barrage."},
        {"name": "Luara", "tier": "A", "wr": 52.1, "pr": "18.2%", "br": "11.0%", "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun", "Mozi"], "desc": "MM baru pemanjat dinding dengan pantulan panah bertubi-tubi."},
        {"name": "Marco Polo", "tier": "A", "wr": 51.5, "pr": "29.0%", "br": "14.2%", "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei", "Yaria"], "desc": "MM pistol ganda penembak true damage & ultimate mutar."},
        {"name": "Consort Yu", "tier": "A", "wr": 51.0, "pr": "19.5%", "br": "8.0%", "counters": ["Physical Assassins"], "synergies": ["Zhang Fei", "Biron"], "desc": "MM imun serangan fisik dengan skill panah sniper jarak jauh."},
        {"name": "Shouyue", "tier": "A", "wr": 51.8, "pr": "21.0%", "br": "18.5%", "counters": ["Vision-dependent Comps"], "synergies": ["Mozi", "Nuwa"], "desc": "MM sniper jarak ekstra jauh & pemasang trap visi semak."}
    ],
    "Roam": [
        {"name": "Zhang Fei", "tier": "S", "wr": 55.1, "pr": "42.0%", "br": "21.0%", "counters": ["Heavy Dive Comps"], "synergies": ["Lady Sun", "Angela", "Augran"], "desc": "Roamer T0 pelindung carry dengan raungan ulti monster & shield tebal."},
        {"name": "Dolia", "tier": "S", "wr": 54.9, "pr": "31.5%", "br": "52.0%", "counters": ["Short Cooldown Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"], "desc": "Support duyung pemutar waktu reset cooldown ultimate rekan tim."},
        {"name": "Yaria", "tier": "S", "wr": 54.6, "pr": "36.2%", "br": "45.0%", "counters": ["Single Target Burst"], "synergies": ["Lady Sun", "Lam", "Ao'yin (Loong)"], "desc": "Support penempel carry dengan bonus +15% gold & shield penahan CC."},
        {"name": "Mozi", "tier": "S", "wr": 53.8, "pr": "28.4%", "br": "22.0%", "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Support meriam stun jarak jauh perusak konsentrasi musuh."},
        {"name": "Da Qiao", "tier": "S", "wr": 53.5, "pr": "19.0%", "br": "48.2%", "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli", "Luna"], "desc": "Support portal teleportasi pemutar balik pasukan ke base."},
        {"name": "Devara", "tier": "A", "wr": 52.3, "pr": "18.0%", "br": "14.1%", "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"], "desc": "Roamer pilar penjepit lokasi war dengan arena kuncian."},
        {"name": "Dun", "tier": "A", "wr": 51.9, "pr": "20.1%", "br": "3.5%", "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "desc": "Roamer tank tahan banting pencetus hook & knock-up."}
    ]
}

# Helper: Get All Heroes in DB
ALL_HERO_NAMES = set()
for r, h_list in HERO_DB.items():
    for h in h_list:
        ALL_HERO_NAMES.add(h["name"])

# ==========================================
# HEADER & SIDEBAR CONFIG
# ==========================================
st.markdown("<div class='main-title'>⚔️ HOK PRO DRAFT & STRATEGY ENGINE S16</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Real-Time Analytics • Side Bias • Fearless Series Lock • By Siropkokop</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Match Configuration")
    
    draft_title = st.text_input("Nama Strategy / Title", "Scrim Game 1 - Heavy Engagement")
    match_series = st.selectbox("Format Turnamen", ["Best of 3 (Bo3)", "Best of 5 (Bo5)", "Best of 7 (Bo7 - Decider)", "Single Scrim Match"])
    
    st.markdown("---")
    st.subheader("🔵🔴 Side Bias Selector")
    our_side = st.radio("Sisi Tim Kita:", ["🔵 Blue Side (B1 First Pick)", "🔴 Red Side (R5 Counter Pick)"])
    
    st.markdown("---")
    st.subheader("🔒 Fearless Memory Tracker")
    st.write(f"**Game Ke:** {st.session_state['game_number']}")
    if st.session_state['used_heroes']:
        st.write("**Hero Terkunci (Fearless):**")
        st.info(", ".join(st.session_state['used_heroes']))
    else:
        st.caption("Belum ada hero yang terkunci di series ini.")
        
    if st.button("🔄 Reset Memory (Series Baru)"):
        st.session_state['used_heroes'] = []
        st.session_state['game_number'] = 1
        st.success("Memory Fearless berhasil direset!")
        st.rerun()

# ==========================================
# MAIN DRAFTING INTERFACE
# ==========================================
col_draft_our, col_vs, col_draft_enemy = st.columns([5, 1, 5])

# Filter out used heroes from dropdowns
available_heroes = [h for h in sorted(ALL_HERO_NAMES) if h not in st.session_state['used_heroes']]

with col_draft_our:
    st.subheader("🔵 DRAF TIM KITA (OUR TEAM)")
    
    st.markdown("##### 🚫 Ban Phase Kita")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        our_ban_1 = st.selectbox("Ban 1 Kita", ["None"] + available_heroes, key="ob1")
    with b_col2:
        available_ob2 = [h for h in available_heroes if h != our_ban_1]
        our_ban_2 = st.selectbox("Ban 2 Kita", ["None"] + available_ob2, key="ob2")
        
    st.markdown("##### 🛡️ Pick Phase Kita")
    p_clash = st.selectbox("Clash Lane", ["None"] + [h["name"] for h in HERO_DB["Clash"] if h["name"] in available_heroes and h["name"] not in [our_ban_1, our_ban_2]], key="op_clash")
    p_jungle = st.selectbox("Jungle", ["None"] + [h["name"] for h in HERO_DB["Jungle"] if h["name"] in available_heroes and h["name"] not in [our_ban_1, our_ban_2, p_clash]], key="op_jungle")
    p_mid = st.selectbox("Mid Lane", ["None"] + [h["name"] for h in HERO_DB["Mid"] if h["name"] in available_heroes and h["name"] not in [our_ban_1, our_ban_2, p_clash, p_jungle]], key="op_mid")
    p_farm = st.selectbox("Farm Lane (MM)", ["None"] + [h["name"] for h in HERO_DB["Farm"] if h["name"] in available_heroes and h["name"] not in [our_ban_1, our_ban_2, p_clash, p_jungle, p_mid]], key="op_farm")
    p_roam = st.selectbox("Roamer", ["None"] + [h["name"] for h in HERO_DB["Roam"] if h["name"] in available_heroes and h["name"] not in [our_ban_1, our_ban_2, p_clash, p_jungle, p_mid, p_farm]], key="op_roam")

our_picks = [p for p in [p_clash, p_jungle, p_mid, p_farm, p_roam] if p != "None"]
our_bans = [b for b in [our_ban_1, our_ban_2] if b != "None"]

with col_vs:
    st.markdown("<br><br><br><br><h2 style='text-align: center; color: #FFD700;'>VS</h2>", unsafe_allow_html=True)

with col_draft_enemy:
    st.subheader("🔴 DRAF TIM MUSUH (ENEMY TEAM)")
    
    # Filter out our picks & bans
    avail_enemy_ban = [h for h in available_heroes if h not in our_picks and h not in our_bans]
    
    st.markdown("##### 🚫 Ban Phase Musuh")
    eb_col1, eb_col2 = st.columns(2)
    with eb_col1:
        enemy_ban_1 = st.selectbox("Ban 1 Musuh", ["None"] + avail_enemy_ban, key="eb1")
    with eb_col2:
        avail_eb2 = [h for h in avail_enemy_ban if h != enemy_ban_1]
        enemy_ban_2 = st.selectbox("Ban 2 Musuh", ["None"] + avail_eb2, key="eb2")
        
    enemy_bans = [b for b in [enemy_ban_1, enemy_ban_2] if b != "None"]
    avail_enemy_pick = [h for h in avail_enemy_ban if h not in enemy_bans]
    
    st.markdown("##### ⚔️ Pick Phase Musuh")
    ep_clash = st.selectbox("Clash Musuh", ["None"] + [h["name"] for h in HERO_DB["Clash"] if h["name"] in avail_enemy_pick], key="ep_clash")
    ep_jungle = st.selectbox("Jungle Musuh", ["None"] + [h["name"] for h in HERO_DB["Jungle"] if h["name"] in avail_enemy_pick and h["name"] != ep_clash], key="ep_jungle")
    ep_mid = st.selectbox("Mid Musuh", ["None"] + [h["name"] for h in HERO_DB["Mid"] if h["name"] in avail_enemy_pick and h["name"] not in [ep_clash, ep_jungle]], key="ep_mid")
    ep_farm = st.selectbox("Farm Musuh", ["None"] + [h["name"] for h in HERO_DB["Farm"] if h["name"] in avail_enemy_pick and h["name"] not in [ep_clash, ep_jungle, ep_mid]], key="ep_farm")
    ep_roam = st.selectbox("Roam Musuh", ["None"] + [h["name"] for h in HERO_DB["Roam"] if h["name"] in avail_enemy_pick and h["name"] not in [ep_clash, ep_jungle, ep_mid, ep_farm]], key="ep_roam")

enemy_picks = [p for p in [ep_clash, ep_jungle, ep_mid, ep_farm, ep_roam] if p != "None"]

# Button to Lock Game to Fearless Memory
st.markdown("---")
if st.button("⏭️ Selesaikan Game & Lock Hero ke Fearless Memory"):
    if our_picks:
        for hero in our_picks:
            if hero not in st.session_state['used_heroes']:
                st.session_state['used_heroes'].append(hero)
        st.session_state['game_number'] += 1
        st.success(f"Hero {our_picks} berhasil terkunci! Lanjut ke Game {st.session_state['game_number']}.")
        st.rerun()
    else:
        st.warning("Pilih minimal 1 hero sebelum mengunci ke Fearless Memory!")

# ==========================================
# REAL-TIME COMBO ALERTS & WARNING BANNERS
# ==========================================
st.markdown("### ⚠️ Real-Time Combo & Threat Alert System")

# Check Enemy Threats
threat_alerts = []
if "Dolia" in enemy_picks:
    threat_alerts.append("🔴 **AWAS ENEMY PICK DOLIA!** Potensi Combo Celestial Reset (Heino / Marco Polo / Yixing). Amankan Heino atau Biron/Angela CC burst!")
if "Nezha" in enemy_picks:
    threat_alerts.append("🔴 **AWAS ENEMY PICK NEZHA!** Lock-on global ke Mid/MM kita. Siapkan Zhang Fei (Shield) atau Biron (Sustain) buat cover!")
if "Mai Shiranui" in enemy_picks or "Shangguan" in enemy_picks:
    threat_alerts.append("🔴 **AWAS ENEMY PICK MAGE ASSASSIN!** Dive burst ke backline. Prio Angela (Shield immunity) / Consort Yu / Zhang Fei!")
if "Augran" in enemy_picks or "Lam" in enemy_picks:
    threat_alerts.append("🔴 **AWAS ENEMY PICK T0 JUNGLER!** High true damage & execution. Siapkan Musashi / Charlotte debuff!")

# Check Our Synergies
synergy_alerts = []
if "Dolia" in our_picks and "Heino" in our_picks:
    synergy_alerts.append("🟢 **COMBO CELESTIAL RESET ACTIVE!** Double Ultimate time rewind & reset tower HP!")
if "Mozi" in our_picks and ("Xiao Qiao" in our_picks or "Arli" in our_picks):
    synergy_alerts.append("🟢 **COMBO UNLI CC ACTIVE!** Long-range Stun Mozi -> Knock-up Xiao Qiao / Gocek Arli!")
if "Yaria" in our_picks and ("Lady Sun" in our_picks or "Ao'yin (Loong)" in our_picks or "Lam" in our_picks):
    synergy_alerts.append("🟢 **COMBO SUPPORT REVAMP ACTIVE!** +15% Gold boost & heavy anti-dive shield!")
if "Sun Ce" in our_picks and ("Da Qiao" in our_picks or "Nuwa" in our_picks):
    synergy_alerts.append("🟢 **COMBO GLOBAL TELEPORT ACTIVE!** Instant boat gank & matrix teleportasi!")

col_alt1, col_alt2 = st.columns(2)
with col_alt1:
    st.markdown("##### 🚨 Danger / Counter Threats")
    if threat_alerts:
        for ta in threat_alerts:
            st.markdown(f"<div class='alert-danger'>{ta}</div>", unsafe_allow_html=True)
    else:
        st.caption("Belum ada ancaman combo berbahaya dari musuh.")

with col_alt2:
    st.markdown("##### 🔥 Active Team Synergies")
    if synergy_alerts:
        for sa in synergy_alerts:
            st.markdown(f"<div class='alert-success'>{sa}</div>", unsafe_allow_html=True)
    else:
        st.caption("Pilih hero kombo (Dolia+Heino, Mozi+Xiao Qiao, Yaria+Lady Sun) untuk mengaktifkan bonus sinergi.")

# ==========================================
# REAL-TIME PROBABILITY ENGINE & GAME PLAN
# ==========================================
st.markdown("---")
st.markdown("### 📊 Real-Time Draft Probability & Strategy Engine")

# Calculate Win Rate Score
base_wr = 50.0
total_wr_bonus = 0.0

# Calculate based on our picks
for role, h_list in HERO_DB.items():
    for h in h_list:
        if h["name"] in our_picks:
            total_wr_bonus += (h["wr"] - 50.0)

# Apply Side Bias Bonus
if "Red Side" in our_side:
    st.info("🔴 **Red Side Multiplier Active:** Red Side memberikan slot R5 Last Counter Pick. Bonus Win Rate diterapkan untuk Haya (+10%), Ao'yin (+8%), & Zhang Fei (+5%).")
    if "Haya" in our_picks: total_wr_bonus += 5.0
    if "Ao'yin (Loong)" in our_picks: total_wr_bonus += 4.0
    if "Zhang Fei" in our_picks: total_wr_bonus += 3.0
else:
    st.info("🔵 **Blue Side Multiplier Active:** Blue Side memberikan keunggulan B1 Power Pick (Augran, Lam, Yaria, Haya).")

our_win_rate = round(base_wr + total_wr_bonus, 1)
our_win_rate = max(35.0, min(85.0, our_win_rate))

col_m1, col_m2 = st.columns([1, 2])
with col_m1:
    st.markdown(f"""
    <div class='metric-box'>
        <h3 style='margin:0; color:#FFD700;'>Est. Win Probability</h3>
        <h1 style='margin:0; font-size: 3rem;'>{our_win_rate}%</h1>
        <p style='margin:0; color:#888;'>Target Score Threshold: > 60.0%</p>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.progress(int(our_win_rate))
    if our_win_rate >= 65.0:
        st.success("🔥 **SUPERIOR DRAFT ADVANTAGE!** Komposisi draf memiliki sinergi tinggi dan meng-counter mayoritas hero lawan.")
    elif our_win_rate >= 55.0:
        st.info("✅ **BALANCED SOLID DRAFT.** Draf stabil dengan power spike seimbang di Mid & Late Game.")
    else:
        st.warning("⚠️ **RISKY DRAFT COMPOSITION.** Perhatikan counter-threat musuh atau amankan hero comfort di slot tersisa.")

# ==========================================
# DYNAMIC IN-GAME STRATEGY SCHEMA
# ==========================================
st.markdown("### 💡 Skema Permainan In-Game (Dynamic Game Plan)")

schema_col1, schema_col2 = st.columns(2)

with schema_col1:
    st.markdown("#### ⏱️ 1. Early Game Execution (Menit 0:00 - 4:00)")
    if "Pei" in our_picks or "Biron" in our_picks:
        st.write("• **Aggressive Boar Invade (Menit 0:30):** Biron / Pei punya power spike sejak menit awal. Lakukan invasi ke babi/buff kecil musuh!")
    else:
        st.write("• **Standard Wave Clear & Prio Mid:** Roamer bantu Mid sapu wave pertama minion. Amankan visi sungai & curi babi kecil musuh.")
    
    st.write("• **Space Sprite Contest (Menit 1:00):** Clash Lane wajib amankan bunga teleportasi buat gank kilat ke Farm Lane.")
    st.write("• **Level 4 Power Spike (Menit 1:20 - 2:00):** Jungle selesai clear hutan pertama. Lakukan gank pertama ke lane musuh yang overextend.")

    st.markdown("#### ⚔️ 2. Mid Game Strategy (Menit 4:00 - 10:00)")
    st.write("• **Turret Plate Collapse (Menit 4:00):** Pelat turret rontok. Alihkan prioritas ke **Tyrant pertama** buat dapet buff damage serangan!")
    st.write("• **Gold Sharing Rules:** Terapkan 2-player wave sharing (160% total gold) di Mid Lane buat ngeboost ekonomi MM & Jungle.")
    st.write("• **Primal Bond Awareness:** Jangan bunuh Overlord & Tyrant bersamaan! Kena debuff -50% damage ke naga kedua selama 90 detik.")

with schema_col2:
    st.markdown("#### 🏆 3. Late Game & Teamfight Execution (Menit 10:00 - 20:00+)")
    
    if "Lady Sun" in our_picks or "Ao'yin (Loong)" in our_picks:
        st.write("• **Core Protection (Peel Carry):** Lady Sun / Loong adalah finisher utama. Roamer & Clash wajib pasang badan di depan.")
    elif "Arli" in our_picks:
        st.write("• **Kiting & Flank Strategy:** Arli gocek dari semak samping, tumpukan CC Roamer pemicu ruang bebas.")
    
    if "Angela" in our_picks or "Wang Zhaojun" in our_picks or "Xiao Qiao" in our_picks:
        st.write("• **Chokepoint Stun Lock:** Pancing war di area sempit dekat sungai/naga biar AoE skill Mid hit 3-5 orang instan.")
        
    st.write("• **Tempest Dragon Penentu (Menit 20:00+):** Peringatan keras! **Dilarang bunuh naga biasa di menit 18:30-19:00** biar tidak kena debuff Primal Bond (-60% damage) pas Tempest Dragon muncul di menit 20:00!")

st.markdown("---")

# ==========================================
# EXPORT & MATCH HISTORY LOG TABS
# ==========================================
tab_export, tab_history, tab_database = st.tabs(["📲 Export to WhatsApp", "📊 Recent Match Analysis", "📚 Complete Hero Database S16"])

with tab_export:
    st.subheader("📋 WhatsApp Copy-Paste Summary")
    
    wa_text = f"""*BLUEPRINT DRAFT HOK* 🎮🔥
*Title:* {draft_title}
*Series:* {match_series} (Game {st.session_state['game_number']}) | *Side:* {our_side}
*Win Probability Engine:* {our_win_rate}% (Our Team)

🚫 *BANS:*
• *Our Bans:* {', '.join([h for h in [our_ban_1, our_ban_2] if h != 'None']) or 'None'}
• *Enemy Bans:* {', '.join([h for h in [enemy_ban_1, enemy_ban_2] if h != 'None']) or 'None'}

🛡️ *OUR PICKS:*
• *Clash:* {p_clash}
• *Jungle:* {p_jungle}
• *Mid:* {p_mid}
• *Farm:* {p_farm}
• *Roam:* {p_roam}

🔴 *ENEMY PICKS:*
• *Clash:* {ep_clash} | *Jungle:* {ep_jungle} | *Mid:* {ep_mid} | *Farm:* {ep_farm} | *Roam:* {ep_roam}

⚡ *KEY GAME PLAN:*
• Early Prio Mid & Space Sprite (Min 1:00)
• Tyrant First Priority (Min 4:00)
• Beware Primal Bond Debuff on Double Dragon!

*Gaspol, Bantai Semuanya! Let's Go!* 🚀🔥"""

    st.code(wa_text, language="markdown")
    st.info("💡 Tinggal klik ikon 'Copy' di pojok kanan atas kotak di atas, lalu paste ke WhatsApp tim!")

with tab_history:
    st.subheader("📊 Recent Match Logger & Coach Notes")
    
    with st.form("match_log_form"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            m_opp = st.text_input("Lawan / Opponent Team", "EVOS / RRQ / Scrim Match")
            m_res = st.selectbox("Hasil Match", ["WIN 🏆", "LOSS ❌"])
        with col_m2:
            m_kda = st.text_input("Score KDA Tim", "18 - 10")
            m_dur = st.text_input("Durasi Match", "14:25")
        with col_m3:
            m_mvp = st.text_input("MVP Player & Hero", "Dapid (Augran) / Reyhan (Lady Sun)")
            
        m_notes = st.text_area("Catatan Evaluasi Coach / Takeaways", "Disiplin cover Mid jalan rapi. Targeting late game pas diinisiasi Dharma langsung dapet 3 kill.")
        
        submit_log = st.form_submit_button("💾 Save Match to History")
        if submit_log:
            st.session_state['match_history'].append({
                "title": draft_title,
                "opp": m_opp,
                "res": m_res,
                "kda": m_kda,
                "dur": m_dur,
                "mvp": m_mvp,
                "notes": m_notes,
                "picks": ", ".join(our_picks)
            })
            st.success("Hasil match berhasil disimpan ke History Log!")
            st.rerun()

    # Display History
    if st.session_state['match_history']:
        st.markdown("#### 📜 History Match Logged")
        df_hist = pd.DataFrame(st.session_state['match_history'])
        st.dataframe(df_hist, use_container_width=True)

with tab_database:
    st.subheader("📚 Hero Database & Stats (Season 16)")
    
    role_filter = st.radio("Filter Role:", ["All", "Clash", "Jungle", "Mid", "Farm", "Roam"], horizontal=True)
    
    filtered_db = []
    for r, h_list in HERO_DB.items():
        if role_filter == "All" or role_filter == r:
            for h in h_list:
                item = h.copy()
                item["Role"] = r
                filtered_db.append(item)
                
    df_db = pd.DataFrame(filtered_db)[["name", "Role", "tier", "wr", "pr", "br", "desc"]]
    df_db.columns = ["Hero Name", "Role", "Tier", "Win Rate", "Pick Rate", "Ban Rate", "Specialization / Description"]
    st.dataframe(df_db, use_container_width=True)

# Footer Credit
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>HOK Pro Draft & Strategy Engine S16 • Built for Esports Analytics • Credit: <b>By Siropkokop</b></div>", unsafe_allow_html=True)
