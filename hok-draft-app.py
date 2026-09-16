import streamlit as st
import pandas as pd
import json

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Pure Hero Draft & Strategy Engine S16 | By Siropkokop",
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
    .badge-s { background-color: #E74C3C; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .badge-a { background-color: #F39C12; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .badge-role { background-color: #3498DB; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .badge-counter { background-color: #9B59B6; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# COMPLETE HERO DATABASE SEASON 16 (BY ROLE)
# ==========================================
HERO_DB = {
    "Clash": [
        {"name": "Biron", "tier": "S", "wr": "54.2%", "pr": "28.5%", "br": "15.2%", "counters": ["Physical Fighters", "Melee Assassins"], "synergies": ["Zhang Fei", "Dun", "Angela"], "desc": "Frontline badak dengan shield tebal dan regen stamina gila."},
        {"name": "Florentino", "tier": "S", "wr": "53.8%", "pr": "18.2%", "br": "42.1%", "counters": ["Tank Heavy", "Sustained Duelists"], "synergies": ["Yaria", "Dolia"], "desc": "God-tier duelis 1v1 dengan mekanik gocekan bunga frame-perfect."},
        {"name": "Dharma", "tier": "S", "wr": "53.5%", "pr": "22.1%", "br": "25.0%", "counters": ["Immobile Squishies", "Wall Huggers"], "synergies": ["Lady Sun", "Yao", "Yixing"], "desc": "Inisiator wall-slam mematikan pembuka war di area sempit."},
        {"name": "Allain", "tier": "A", "wr": "51.8%", "pr": "19.4%", "br": "10.5%", "counters": ["Squishy Carries", "Shield Tanks"], "synergies": ["Wang Zhaojun", "Dolia"], "desc": "Duelist hybrid physical/magic damage dengan untargetable ulti."},
        {"name": "Sun Ce", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "8.2%", "counters": ["Split Pushers", "Immobile Carries"], "synergies": ["Da Qiao", "Nuwa", "Arli"], "desc": "Penguasa kapal rotasi global untuk gank cepat antar lane."},
        {"name": "Fatih", "tier": "A", "wr": "50.8%", "pr": "12.3%", "br": "5.1%", "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"], "desc": "Fighter crowd control perusak formasi musuh."},
        {"name": "Li Xin", "tier": "A", "wr": "50.5%", "pr": "16.8%", "br": "6.0%", "counters": ["Immobile Mages"], "synergies": ["Dolia", "Zhang Fei"], "desc": "Fighter dua wujud: Light (Aoe Burst) & Dark (Fast Split Push)."},
        {"name": "Charlotte", "tier": "S", "wr": "53.1%", "pr": "17.5%", "br": "18.4%", "counters": ["Attack Speed Carries", "Basic Attackers"], "synergies": ["Zhang Fei", "Wang Zhaojun"], "desc": "Counter alami hero fisik dengan debuff attack speed & damage reduction."},
        {"name": "Guan Yu", "tier": "A", "wr": "51.0%", "pr": "11.2%", "br": "14.1%", "counters": ["No-CC Comps"], "synergies": ["Da Qiao", "Yixing"], "desc": "Inisiator kuda pendorong formasi musuh ke arah tim."},
        {"name": "Mulan", "tier": "A", "wr": "50.9%", "pr": "13.4%", "br": "9.2%", "counters": ["Squishy Mages"], "synergies": ["Lam", "Lorion"], "desc": "Assassin-Fighter wujud pedang ganda & pedang berat."},
        {"name": "Mayene", "tier": "A", "wr": "51.5%", "pr": "14.2%", "br": "12.0%", "counters": ["Solo Laners"], "synergies": ["Augran", "Dolia"], "desc": "Fighter kombo pencak silat dengan mobilitas tinggi."},
        {"name": "Dun", "tier": "A", "wr": "52.0%", "pr": "21.0%", "br": "4.5%", "counters": ["Dive Assassins"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Tank pasak bumi dengan true damage & shield regenerasi."},
        {"name": "Nezha", "tier": "A", "wr": "51.4%", "pr": "10.1%", "br": "7.8%", "counters": ["Healers", "Backline Carries"], "synergies": ["Pei", "Nuwa"], "desc": "Lock-on global target dengan debuff anti-heal bawaan."},
        {"name": "Ata", "tier": "B", "wr": "49.5%", "pr": "8.0%", "br": "2.1%", "counters": ["Non-dash Heroes"], "synergies": ["Lady Sun", "Angela"], "desc": "Tank pembangun tembok penghalang jalan musuh."}
    ],
    "Jungle": [
        {"name": "Augran", "tier": "S", "wr": "55.8%", "pr": "32.1%", "br": "58.4%", "counters": ["Wall Huggers", "Tank Comps"], "synergies": ["Biron", "Zhang Fei", "Angela"], "desc": "Jungler T0 paling dominan Season 16 dengan wujud jiwa penyerap HP."},
        {"name": "Lam", "tier": "S", "wr": "54.9%", "pr": "29.8%", "br": "62.0%", "counters": ["Low HP Squishies", "Immobile Carries"], "synergies": ["Yaria", "Angela", "Wang Zhaojun"], "desc": "Assassin hiu dengan pasif true damage target HP <30%."},
        {"name": "Feyd", "tier": "S", "wr": "53.9%", "pr": "21.4%", "br": "35.2%", "counters": ["Backline MM", "Vision-less Comps"], "synergies": ["Kui", "Devara", "Haya"], "desc": "Assassin bayangan penyergap lini belakang dari fog of war."},
        {"name": "Li Bai", "tier": "A", "wr": "52.1%", "pr": "18.5%", "br": "11.2%", "counters": ["Skillshot Mages", "Immobile Carries"], "synergies": ["Kui", "Nuwa", "Devara"], "desc": "Assassin lincah dengan 2 wujud untargetable & dash balik bayangan."},
        {"name": "Pei", "tier": "A", "wr": "51.8%", "pr": "14.2%", "br": "19.0%", "counters": ["Slow Early Junglers"], "synergies": ["Biron", "Devara", "Nezha"], "desc": "Jungler wujud harimau dengan power spike invasif sejak menit 0:30."},
        {"name": "Musashi", "tier": "A", "wr": "51.5%", "pr": "16.1%", "br": "8.4%", "counters": ["Healers", "Shield Comps"], "synergies": ["Dolia", "Xiao Qiao"], "desc": "Pendekar pemotong shield & pengunci target tunggal."},
        {"name": "Kaizer", "tier": "A", "wr": "52.2%", "pr": "24.0%", "br": "5.1%", "counters": ["Burst Assassins"], "synergies": ["Zhang Fei", "Lady Sun"], "desc": "Jungler Tank/Fighter wujud iblis penahan gempuran fisik."},
        {"name": "Ukyo", "tier": "A", "wr": "51.1%", "pr": "12.0%", "br": "3.2%", "counters": ["Early Squishies"], "synergies": ["Mozi", "Xiao Qiao"], "desc": "Samurai burst damage jarak menengah dengan lifesteal cepat."},
        {"name": "Xuance", "tier": "A", "wr": "52.0%", "pr": "13.5%", "br": "15.1%", "counters": ["No-escape Carries"], "synergies": ["Mozi", "Dun", "Xiao Qiao"], "desc": "Assassin pancing kait pembalik posisi musuh ke belakang."},
        {"name": "Jing", "tier": "S", "wr": "54.1%", "pr": "15.2%", "br": "48.0%", "counters": ["Clustered Comps"], "synergies": ["Yixing", "Dolia"], "desc": "Assassin cermin mekanik tinggi dengan infinite swap dash."},
        {"name": "Luna", "tier": "S", "wr": "53.9%", "pr": "11.8%", "br": "52.1%", "counters": ["No-Hard-CC Comps"], "synergies": ["Da Qiao", "Zhang Fei"], "desc": "Mage-Assassin dengan mark reset ulti tanpa batas."},
        {"name": "Wukong", "tier": "A", "wr": "51.2%", "pr": "22.5%", "br": "12.3%", "counters": ["Squishy Backlines"], "synergies": ["Yaria", "Diao Chan"], "desc": "Raja kera pemicu critical burst instan sekali pukul."},
        {"name": "Dian Wei", "tier": "B", "wr": "49.8%", "pr": "14.1%", "br": "2.0%", "counters": ["CC Heavy Comps"], "synergies": ["Cai Yan", "Zhuangzi"], "desc": "Berserker pembersih efek CC dengan stacking true damage."},
        {"name": "Liu Bei", "tier": "B", "wr": "50.1%", "pr": "9.2%", "br": "1.5%", "counters": ["Melee Tanks"], "synergies": ["Yaria"], "desc": "Marksman-Jungle jarak dekat pembantai objektif naga."}
    ],
    "Mid": [
        {"name": "Haya", "tier": "S", "wr": "56.2%", "pr": "28.0%", "br": "45.1%", "counters": ["Cluster Formations"], "synergies": ["Feyd", "Li Bai", "Augran"], "desc": "Mage S-Tier Red Side Win Rate 80% pemanggil badai bulan."},
        {"name": "Wang Zhaojun", "tier": "S", "wr": "54.1%", "pr": "31.2%", "br": "22.0%", "counters": ["Dive Comps", "Melee Assassins"], "synergies": ["Biron", "Lady Sun", "Zhang Fei"], "desc": "Mage kontroller es pembeku area dengan shield pembawa pasif slow."},
        {"name": "Xiao Qiao", "tier": "S", "wr": "53.8%", "pr": "35.1%", "br": "18.2%", "counters": ["Chokepoint War"], "synergies": ["Mozi", "Dun", "Arli"], "desc": "Mage poke & knock-up instan dengan burst kipas raksasa."},
        {"name": "Lorion", "tier": "S", "wr": "53.5%", "pr": "19.2%", "br": "28.0%", "counters": ["Tight Formations"], "synergies": ["Pei", "Devara", "Lam"], "desc": "Mage bola elektrik perusak formasi musuh di udara."},
        {"name": "Nuwa", "tier": "A", "wr": "52.4%", "pr": "11.5%", "br": "9.1%", "counters": ["Long-range Siege"], "synergies": ["Sun Ce", "Nezha", "Li Bai"], "desc": "Mage pencipta matriks tembok & teleportasi matriks peta global."},
        {"name": "Angela", "tier": "A", "wr": "51.9%", "pr": "38.0%", "br": "8.5%", "counters": ["Frontline Tanks"], "synergies": ["Lam", "Zhang Fei", "Biron"], "desc": "Mage pembalas burst laser dengan shield CC-immunity."},
        {"name": "Yixing", "tier": "S", "wr": "54.0%", "pr": "17.8%", "br": "24.5%", "counters": ["No-escape Comps"], "synergies": ["Dharma", "Lady Sun", "Dolia"], "desc": "Mage papan catur pengurung musuh dalam area raksasa."},
        {"name": "Kui", "tier": "A", "wr": "51.1%", "pr": "16.4%", "br": "15.0%", "counters": ["Immobile Carries"], "synergies": ["Li Bai", "Feyd", "Nuwa"], "desc": "Mage kait pengisolasi 1 target dari jarak sangat jauh."},
        {"name": "Heino", "tier": "S", "wr": "53.7%", "pr": "22.1%", "br": "31.0%", "counters": ["Attrition Comps"], "synergies": ["Dolia", "Flowborn (MM)"], "desc": "Mage pemutar waktu reset HP & tower dengan combo Dolia."},
        {"name": "Diao Chan", "tier": "A", "wr": "52.0%", "pr": "21.5%", "br": "29.1%", "counters": ["Skillshot Heavy Comps"], "synergies": ["Zhang Fei", "Wukong"], "desc": "Mage penari dengan cooldown reset & true damage bertubi-tubi."},
        {"name": "Mai Shiranui", "tier": "S", "wr": "54.5%", "pr": "18.0%", "br": "55.0%", "counters": ["Squishy Backlines"], "synergies": ["Feyd", "Augran"], "desc": "Mage-Assassin lincah pembebas energi combo sekali putar."},
        {"name": "Shangguan", "tier": "A", "wr": "52.8%", "pr": "14.2%", "br": "38.2%", "counters": ["Immobile Mages"], "synergies": ["Lam", "Yaria"], "desc": "Mage kuas terbang untargetable pembantai lini belakang."}
    ],
    "Farm": [
        {"name": "Lady Sun", "tier": "S", "wr": "54.8%", "pr": "38.5%", "br": "25.0%", "counters": ["Low Mobility Tanks", "Short Range MM"], "synergies": ["Yaria", "Dharma", "Yao"], "desc": "MM S-Tier burst rolled-attack penghancur armor musuh."},
        {"name": "Ao'yin (Loong)", "tier": "S", "wr": "55.2%", "pr": "31.0%", "br": "58.0%", "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia", "Zhang Fei"], "desc": "MM naga elemen dengan ulti wujud terbang untargetable."},
        {"name": "Arli", "tier": "S", "wr": "54.2%", "pr": "24.1%", "br": "41.0%", "counters": ["Skillshot Mages", "Melee Inisiators"], "synergies": ["Mozi", "Xiao Qiao", "Da Qiao"], "desc": "MM 3-dash parasut paling lincah dengan penepis proyektil."},
        {"name": "Flowborn (MM)", "tier": "S", "wr": "53.9%", "pr": "20.5%", "br": "22.1%", "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce", "Heino"], "desc": "MM fleksibel dengan sistem 5-stack double cast skill barrage."},
        {"name": "Luara", "tier": "A", "wr": "52.1%", "pr": "18.2%", "br": "11.0%", "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun", "Mozi"], "desc": "MM baru pemanjat dinding dengan pantulan panah bertubi-tubi."},
        {"name": "Marco Polo", "tier": "A", "wr": "51.5%", "pr": "29.0%", "br": "14.2%", "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei", "Yaria"], "desc": "MM pistol ganda penembak true damage & ultimate mutar."},
        {"name": "Consort Yu", "tier": "A", "wr": "51.0%", "pr": "19.5%", "br": "8.0%", "counters": ["Physical Assassins"], "synergies": ["Zhang Fei", "Biron"], "desc": "MM imun serangan fisik dengan skill panah sniper jarak jauh."},
        {"name": "Luban No.7", "tier": "B", "wr": "50.2%", "pr": "32.0%", "br": "5.1%", "counters": ["High HP Tanks"], "synergies": ["Zhang Fei", "Cai Yan"], "desc": "MM tembakan roket max HP % damage tanpa ampuni."},
        {"name": "Shouyue", "tier": "A", "wr": "51.8%", "pr": "21.0%", "br": "18.5%", "counters": ["Vision-dependent Comps"], "synergies": ["Mozi", "Nuwa"], "desc": "MM sniper jarak ekstra jauh & pemasang trap visi semak."},
        {"name": "Alessio", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "6.2%", "counters": ["Clustered Tanks"], "synergies": ["Yaria", "Dolia"], "desc": "MM meriam terbang dengan stealth asap penyelamat diri."}
    ],
    "Roam": [
        {"name": "Zhang Fei", "tier": "S", "wr": "55.1%", "pr": "42.0%", "br": "21.0%", "counters": ["Heavy Dive Comps"], "synergies": ["Lady Sun", "Angela", "Augran"], "desc": "Roamer T0 pelindung carry dengan raungan ulti monster & shield tebal."},
        {"name": "Yaria", "tier": "S", "wr": "54.6%", "pr": "36.2%", "br": "45.0%", "counters": ["Single Target Burst"], "synergies": ["Lady Sun", "Lam", "Ao'yin (Loong)"], "desc": "Support penempel carry dengan bonus +15% gold & shield penahan CC."},
        {"name": "Dolia", "tier": "S", "wr": "54.9%", "pr": "31.5%", "br": "52.0%", "counters": ["Short Cooldown Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"], "desc": "Support duyung pemutar waktu reset cooldown ultimate rekan tim."},
        {"name": "Devara", "tier": "A", "wr": "52.3%", "pr": "18.0%", "br": "14.1%", "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"], "desc": "Roamer pilar penjepit lokasi war dengan arena kuncian."},
        {"name": "Mozi", "tier": "S", "wr": "53.8%", "pr": "28.4%", "br": "22.0%", "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Support meriam stun jarak jauh perusak konsentrasi musuh."},
        {"name": "Dun", "tier": "A", "wr": "51.9%", "pr": "20.1%", "br": "3.5%", "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "desc": "Roamer tank tahan banting pencetus hook & knock-up."},
        {"name": "Da Qiao", "tier": "S", "wr": "54.0%", "pr": "19.5%", "br": "49.0%", "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli", "Luna"], "desc": "Support ratu portal pemulang darah instan & pemanggil 5 tim."},
        {"name": "Cai Yan", "tier": "B", "wr": "50.8%", "pr": "25.0%", "br": "12.0%", "counters": ["Poke Comps"], "synergies": ["Luban No.7", "Kaizer"], "desc": "Support mobil penyembuh HP area & pemberi armor ganda."},
        {"name": "Donghuang", "tier": "A", "wr": "52.1%", "pr": "15.8%", "br": "38.0%", "counters": ["High Mobility Assassins"], "synergies": ["Lady Sun", "Angela"], "desc": "Tank kuncian ciuman mati supress yang tidak bisa di-Purify."},
        {"name": "Liang", "tier": "A", "wr": "51.8%", "pr": "14.0%", "br": "32.0%", "counters": ["Hyper Mobile Carries"], "synergies": ["Lam", "Augran"], "desc": "Support/Mid pemegang rantai supress penghenti gerakan musuh."}
    ]
}

# Flat list of all heroes for quick checks
ALL_HEROES_FLAT = []
for role, h_list in HERO_DB.items():
    for h in h_list:
        h_copy = h.copy()
        h_copy["role"] = role
        ALL_HEROES_FLAT.append(h_copy)

# ==========================================
# HEADER & TITLE
# ==========================================
st.markdown("<div class='main-title'>⚔️ HOK PURE HERO DRAFT & STRATEGY ENGINE</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Real-Time Pick & Ban Calculator • Role-Based Search • Game Plan Schema (Patch Season 16)</div>", unsafe_allow_html=True)

# Session state initialization
if 'used_heroes' not in st.session_state:
    st.session_state['used_heroes'] = []

if 'match_history' not in st.session_state:
    st.session_state['match_history'] = []

# ==========================================
# SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.header("⚙️ Draft Setup & Rules")
    
    draft_title = st.text_input("🏷️ Custom Draft Title", "Draft Scrim Unli CC & Dive Strategy")
    match_series = st.selectbox("Turnamen Mode", ["Bo1 Single Match", "Bo3 Series", "Bo5 Series", "Bo7 Grand Final"])
    our_side = st.radio("Tim Kita di Sisi:", ["Blue Side (B1 First Pick)", "Red Side (R5 Counter-Pick)"])
    
    st.markdown("---")
    st.subheader("🔒 Fearless Memory Tracker")
    st.info(f"Hero Terkunci (Dipakai Sebelumnya): **{len(st.session_state['used_heroes'])} Hero**")
    if st.button("🗑️ Reset Memory Fearless"):
        st.session_state['used_heroes'] = []
        st.rerun()

# ==========================================
# MAIN INTERFACE: PURE HERO PICK & BAN PHASE
# ==========================================
st.markdown("### 🚫 1. Banning & Picking Phase (Role-Organized)")

# Helper function to get available hero list filtered by banned/picked and used
def get_available_heroes(role=None):
    avail = []
    for h in ALL_HEROES_FLAT:
        if role and h['role'] != role:
            continue
        if h['name'] in st.session_state['used_heroes']:
            continue
        avail.append(h['name'])
    return sorted(list(set(avail)))

# BAN PHASE UI
col_ban1, col_ban2 = st.columns(2)

with col_ban1:
    st.subheader("🔵 BAN TIM KITA")
    b1_options = ["None"] + get_available_heroes()
    our_ban_1 = st.selectbox("Ban #1 Kita", b1_options, index=0, key="ob1")
    
    b2_options = ["None"] + [h for h in get_available_heroes() if h != our_ban_1]
    our_ban_2 = st.selectbox("Ban #2 Kita", b2_options, index=0, key="ob2")

with col_ban2:
    st.subheader("🔴 BAN TIM MUSUH")
    eb1_options = ["None"] + [h for h in get_available_heroes() if h not in [our_ban_1, our_ban_2]]
    enemy_ban_1 = st.selectbox("Ban #1 Musuh", eb1_options, index=0, key="eb1")
    
    eb2_options = ["None"] + [h for h in get_available_heroes() if h not in [our_ban_1, our_ban_2, enemy_ban_1]]
    enemy_ban_2 = st.selectbox("Ban #2 Musuh", eb2_options, index=0, key="eb2")

# Active Banned Heroes List
all_banned = [h for h in [our_ban_1, our_ban_2, enemy_ban_1, enemy_ban_2] if h != "None"]

st.markdown("---")

# PICK PHASE UI BY ROLE
st.markdown("### 🛡️ 2. Role-Based Pick Selection")
col_our_picks, col_enemy_picks = st.columns(2)

# Function to get unselected hero options
def get_pick_options(role, current_selected_heroes):
    excluded = set(all_banned + current_selected_heroes + st.session_state['used_heroes'])
    role_heroes = [h['name'] for h in HERO_DB.get(role, []) if h['name'] not in excluded]
    return ["None"] + sorted(role_heroes)

# Initialize pick containers
our_picks = []
enemy_picks = []

with col_our_picks:
    st.subheader("🔵 PICK TIM KITA (OUR TEAM)")
    
    # Track selection in real-time
    selected_so_far_our = []
    
    p_clash = st.selectbox("⚔️ Clash Lane", get_pick_options("Clash", selected_so_far_our), key="op_clash")
    if p_clash != "None": selected_so_far_our.append(p_clash)
    
    p_jungle = st.selectbox("🐅 Jungle", get_pick_options("Jungle", selected_so_far_our), key="op_jungle")
    if p_jungle != "None": selected_so_far_our.append(p_jungle)
    
    p_mid = st.selectbox("🔮 Mid Lane", get_pick_options("Mid", selected_so_far_our), key="op_mid")
    if p_mid != "None": selected_so_far_our.append(p_mid)
    
    p_farm = st.selectbox("🏹 Farm Lane (MM)", get_pick_options("Farm", selected_so_far_our), key="op_farm")
    if p_farm != "None": selected_so_far_our.append(p_farm)
    
    p_roam = st.selectbox("🛡️ Roamer", get_pick_options("Roam", selected_so_far_our), key="op_roam")
    if p_roam != "None": selected_so_far_our.append(p_roam)
    
    our_picks = [h for h in [p_clash, p_jungle, p_mid, p_farm, p_roam] if h != "None"]

with col_enemy_picks:
    st.subheader("🔴 PICK TIM MUSUH (ENEMY TEAM)")
    
    selected_so_far_enemy = []
    
    ep_clash = st.selectbox("⚔️ Enemy Clash Lane", get_pick_options("Clash", our_picks + selected_so_far_enemy), key="ep_clash")
    if ep_clash != "None": selected_so_far_enemy.append(ep_clash)
    
    ep_jungle = st.selectbox("🐅 Enemy Jungle", get_pick_options("Jungle", our_picks + selected_so_far_enemy), key="ep_jungle")
    if ep_jungle != "None": selected_so_far_enemy.append(ep_jungle)
    
    ep_mid = st.selectbox("🔮 Enemy Mid Lane", get_pick_options("Mid", our_picks + selected_so_far_enemy), key="ep_mid")
    if ep_mid != "None": selected_so_far_enemy.append(ep_mid)
    
    ep_farm = st.selectbox("🏹 Enemy Farm Lane", get_pick_options("Farm", our_picks + selected_so_far_enemy), key="ep_farm")
    if ep_farm != "None": selected_so_far_enemy.append(ep_farm)
    
    ep_roam = st.selectbox("🛡️ Enemy Roamer", get_pick_options("Roam", our_picks + selected_so_far_enemy), key="ep_roam")
    if ep_roam != "None": selected_so_far_enemy.append(ep_roam)
    
    enemy_picks = [h for h in [ep_clash, ep_jungle, ep_mid, ep_farm, ep_roam] if h != "None"]

# Lock heroes to Fearless Memory button
if st.button("💾 Lock Our Picks to Fearless Memory (Save Game Session)"):
    for h in our_picks:
        if h not in st.session_state['used_heroes']:
            st.session_state['used_heroes'].append(h)
    st.success("Hero berhasil disimpan ke memori Fearless Draft!")
    st.rerun()

st.markdown("---")

# ==========================================
# REAL TIME PROBABILITY & GAME SCHEMA ENGINE
# (PLACED DIRECTLY BELOW DRAFTING SECTION)
# ==========================================
st.markdown("## 📊 REAL-TIME PROBABILITY & SKEMA PERMAINAN (GAME PLAN)")

# CALCULATE PROBABILITY SCORE
our_score = 50.0
enemy_score = 50.0

# Base Tier Calculations
for h_name in our_picks:
    h_data = next((item for item in ALL_HEROES_FLAT if item["name"] == h_name), None)
    if h_data:
        our_score += 6.0 if h_data["tier"] == "S" else 4.0

for h_name in enemy_picks:
    h_data = next((item for item in ALL_HEROES_FLAT if item["name"] == h_name), None)
    if h_data:
        enemy_score += 6.0 if h_data["tier"] == "S" else 4.0

# Side Bias
if "Red Side" in our_side:
    our_score += 3.5
    for h_name in our_picks:
        if h_name in ["Haya", "Ao'yin (Loong)", "Zhang Fei"]:
            our_score += 4.0
else:
    our_score += 2.0  # Blue side first pick advantage

# Counter & Synergy checks
syn_count = 0
for h_name in our_picks:
    h_data = next((item for item in ALL_HEROES_FLAT if item["name"] == h_name), None)
    if h_data:
        for partner in our_picks:
            if partner in h_data.get("synergies", []):
                our_score += 3.0
                syn_count += 1

total_prob = our_score + enemy_score
our_win_rate = round((our_score / total_prob) * 100, 1)
enemy_win_rate = round(100 - our_win_rate, 1)

# DISPLAY PROBABILITY METRICS
res_col1, res_col2, res_col3 = st.columns([1, 1, 2])

with res_col1:
    st.metric("🔥 Our Win Probability", f"{our_win_rate}%", delta=f"{our_win_rate - 50.0:.1f}% vs Neutral")

with res_col2:
    st.metric("💀 Enemy Win Probability", f"{enemy_win_rate}%")

with res_col3:
    st.write(f"**Draft Name:** `{draft_title}`")
    st.write(f"**Active Sinergi Combos Detected:** `{syn_count} Combo Connections`")
    if our_win_rate >= 60.0:
        st.success("🎯 **STATUS DRAFT:** SUPERIOR ADVANTAGE (Dominan S-Tier Synergy)")
    elif our_win_rate >= 50.0:
        st.info("⚖️ **STATUS DRAFT:** BALANCED MATCHUP (Fokus Eksekusi In-Game)")
    else:
        st.warning("⚠️ **STATUS DRAFT:** COUNTERED / DISADVANTAGE (Butuh Disiplin High Ground)")

st.markdown("---")

# DYNAMIC REAL-TIME GAME PLAN SCHEMA BASED ON PICKED HEROES
st.markdown("### 📜 SKEMA PERMAINAN TAKTIS IN-GAME (GAME PLAN SCHEMA)")

schema_col1, schema_col2 = st.columns(2)

with schema_col1:
    st.markdown("#### ⚡ 1. Early Game Strategy (Menit 0:00 - 4:00)")
    
    # Dynamic early strategy check
    has_pei = "Pei" in our_picks
    has_biron = "Biron" in our_picks or "Dharma" in our_picks
    has_zhangfei = "Zhang Fei" in our_picks or "Mozi" in our_picks
    
    if has_pei or (has_biron and has_zhangfei):
        st.write("• **Aggressive Invade Plan:** Menit 0:30 Roamer + Mid + Jungle langsung melakukan rusuh/invasi ke *Buff Merah/Biru* musuh.")
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
    
    # Dynamic positioning advice based on picks
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
*Series:* {match_series} | *Side:* {our_side}
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
st.markdown("<div style='text-align: center; color: #888;'>HOK Draft & Strategy Engine S16 • Built for Esports Analytics • Credit: <b>By Siropkokop</b></div>", unsafe_allow_html=True)
