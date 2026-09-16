import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Pro Draft & Strategy Engine V7 | By Siropkokop",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Esports Dark Theme & Ergonomic UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFD700;
        text-align: center;
        margin-bottom: 2px;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #AAAAAA;
        text-align: center;
        margin-bottom: 15px;
    }
    .stCard {
        background-color: #1E1E2E;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #313244;
        margin-bottom: 10px;
    }
    .flex-radar-card {
        background-color: #181825;
        border-left: 4px solid #E74C3C;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .flex-synergy-card {
        background-color: #132a18;
        border-left: 4px solid #2ECC71;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .flex-item-card {
        background-color: #1c2536;
        border-left: 4px solid #3498DB;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .badge-s { background-color: #E74C3C; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-a { background-color: #F39C12; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-b { background-color: #3498DB; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .alert-danger { background-color: #421212; border: 1px solid #E74C3C; color: #FF9999; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
    .alert-success { background-color: #123318; border: 1px solid #2ECC71; color: #99FFBB; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# COMPLETE HERO DATABASE (116 HEROES - SEASON 16)
# ==========================================
HERO_DB = {
    "Clash": [
        {"name": "Biron", "tier": "S", "wr": "54.2%", "pr": "28.5%", "br": "15.2%", "counters": ["Physical Fighters", "Melee Assassins"], "synergies": ["Zhang Fei", "Dun", "Angela"], "desc": "Frontline shield & sustain badak."},
        {"name": "Florentino", "tier": "S", "wr": "53.8%", "pr": "18.2%", "br": "42.1%", "counters": ["Tank Heavy"], "synergies": ["Yaria", "Dolia"], "desc": "Duelis 1v1 gocekan bunga frame-perfect."},
        {"name": "Dharma", "tier": "S", "wr": "53.5%", "pr": "22.1%", "br": "25.0%", "counters": ["Immobile Squishies"], "synergies": ["Lady Sun", "Yao", "Yixing"], "desc": "Inisiator wall-slam pembuka war sempit."},
        {"name": "Charlotte", "tier": "S", "wr": "53.1%", "pr": "17.5%", "br": "18.4%", "counters": ["Attack Speed Carries"], "synergies": ["Zhang Fei", "Wang Zhaojun"], "desc": "Counter alami hero fisik & attack speed."},
        {"name": "Allain", "tier": "A", "wr": "51.8%", "pr": "19.4%", "br": "10.5%", "counters": ["Squishy Carries"], "synergies": ["Wang Zhaojun", "Dolia"], "desc": "Duelist hybrid damage untargetable ulti."},
        {"name": "Sun Ce", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "8.2%", "counters": ["Split Pushers"], "synergies": ["Da Qiao", "Nuwa"], "desc": "Penguasa kapal rotasi global gank kilat."},
        {"name": "Fatih", "tier": "A", "wr": "50.8%", "pr": "12.3%", "br": "5.1%", "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"], "desc": "Fighter crowd control perusak formasi."},
        {"name": "Li Xin", "tier": "A", "wr": "50.5%", "pr": "16.8%", "br": "6.0%", "counters": ["Immobile Mages"], "synergies": ["Dolia", "Zhang Fei"], "desc": "Dual form: Light AoE & Dark Split Push."},
        {"name": "Guan Yu", "tier": "A", "wr": "51.0%", "pr": "11.2%", "br": "14.1%", "counters": ["No-CC Comps"], "synergies": ["Da Qiao", "Yixing"], "desc": "Inisiator kuda pendorong formasi musuh."},
        {"name": "Mulan", "tier": "A", "wr": "50.9%", "pr": "13.4%", "br": "9.2%", "counters": ["Squishy Mages"], "synergies": ["Lam", "Lorion"], "desc": "Assassin dual blade & heavy sword combo."},
        {"name": "Mayene", "tier": "A", "wr": "51.5%", "pr": "14.2%", "br": "12.0%", "counters": ["Solo Laners"], "synergies": ["Augran", "Dolia"], "desc": "Fighter silat mobilitas tinggi."},
        {"name": "Dun", "tier": "A", "wr": "52.0%", "pr": "21.0%", "br": "4.5%", "counters": ["Dive Assassins"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Tank pasak bumi true damage & regen."},
        {"name": "Nezha", "tier": "A", "wr": "51.4%", "pr": "10.1%", "br": "7.8%", "counters": ["Healers", "Backlines"], "synergies": ["Pei", "Nuwa"], "desc": "Global lock-on target & anti-heal."},
        {"name": "Ata", "tier": "B", "wr": "49.5%", "pr": "8.0%", "br": "2.1%", "counters": ["Non-dash Heroes"], "synergies": ["Lady Sun", "Angela"], "desc": "Tank pembangun tembok penghalang."},
        {"name": "Arthur", "tier": "B", "wr": "49.8%", "pr": "18.0%", "br": "1.0%", "counters": ["High Mobility"], "synergies": ["Cai Yan"], "desc": "Fighter simpel penekan silence."},
        {"name": "Wuyan", "tier": "B", "wr": "50.1%", "pr": "9.5%", "br": "2.0%", "counters": ["Melee Clustered"], "synergies": ["Zhang Fei"], "desc": "Fighter palu efek petrik pasif."},
        {"name": "Kaizer (Clash)", "tier": "A", "wr": "51.5%", "pr": "12.0%", "br": "3.5%", "counters": ["Burst Damage"], "synergies": ["Lady Sun"], "desc": "Fighter wujud iblis penahan gempuran."},
        {"name": "Sun Wukong (Clash)", "tier": "B", "wr": "49.2%", "pr": "5.0%", "br": "2.0%", "counters": ["Squishies"], "synergies": ["Yaria"], "desc": "Crit burst melee fighter."},
        {"name": "Lian Po", "tier": "A", "wr": "51.3%", "pr": "10.5%", "br": "3.0%", "counters": ["CC Comps"], "synergies": ["Xiao Qiao"], "desc": "Tank super immune CC inisiator 3-step knockup."},
        {"name": "Meng Ya (Clash)", "tier": "B", "wr": "48.9%", "pr": "3.0%", "br": "1.0%", "counters": ["Melee Tanks"], "synergies": ["Dolia"], "desc": "Off-meta clash lane heavy sustain."},
        {"name": "Yang Jian", "tier": "B", "wr": "49.6%", "pr": "6.2%", "br": "1.5%", "counters": ["Low HP Targets"], "synergies": ["Kui"], "desc": "Fighter anjing pelacak true damage laser."},
        {"name": "Sima Yi (Clash)", "tier": "B", "wr": "49.0%", "pr": "4.1%", "br": "3.0%", "counters": ["Magic Damage"], "synergies": ["Feyd"], "desc": "Anti-mage silence diver."},
        {"name": "Cheng Yaojin", "tier": "B", "wr": "50.0%", "pr": "11.0%", "br": "2.5%", "counters": ["Low Anti-heal"], "synergies": ["Dolia"], "desc": "Tank regen HP gila splitter lane."}
    ],
    "Jungle": [
        {"name": "Augran", "tier": "S", "wr": "55.8%", "pr": "32.1%", "br": "58.4%", "counters": ["Wall Huggers", "Tanks"], "synergies": ["Biron", "Zhang Fei", "Angela"], "desc": "Jungler T0 soul absorber HP drain."},
        {"name": "Lam", "tier": "S", "wr": "54.9%", "pr": "29.8%", "br": "62.0%", "counters": ["Low HP Squishies"], "synergies": ["Yaria", "Angela", "Wang Zhaojun"], "desc": "Assassin hiu pasif true damage <30% HP."},
        {"name": "Feyd", "tier": "S", "wr": "53.9%", "pr": "21.4%", "br": "35.2%", "counters": ["Backline MM"], "synergies": ["Kui", "Devara", "Haya"], "desc": "Assassin bayangan penyergap fog of war."},
        {"name": "Jing", "tier": "S", "wr": "54.1%", "pr": "15.2%", "br": "48.0%", "counters": ["Clustered Comps"], "synergies": ["Yixing", "Dolia"], "desc": "Assassin cermin infinite swap dash."},
        {"name": "Luna", "tier": "S", "wr": "53.9%", "pr": "11.8%", "br": "52.1%", "counters": ["No-Hard-CC"], "synergies": ["Da Qiao", "Zhang Fei"], "desc": "Mage-Assassin mark reset ulti tanpa batas."},
        {"name": "Li Bai", "tier": "A", "wr": "52.1%", "pr": "18.5%", "br": "11.2%", "counters": ["Skillshot Mages"], "synergies": ["Kui", "Nuwa", "Devara"], "desc": "Assassin 2 untargetable & dash shadow return."},
        {"name": "Pei", "tier": "A", "wr": "51.8%", "pr": "14.2%", "br": "19.0%", "counters": ["Slow Early Junglers"], "synergies": ["Biron", "Devara", "Nezha"], "desc": "Jungler harimau invade menit 0:30."},
        {"name": "Musashi", "tier": "A", "wr": "51.5%", "pr": "16.1%", "br": "8.4%", "counters": ["Healers", "Shields"], "synergies": ["Dolia", "Xiao Qiao"], "desc": "Pendekar pemotong shield single target lock."},
        {"name": "Kaizer", "tier": "A", "wr": "52.2%", "pr": "24.0%", "br": "5.1%", "counters": ["Burst Assassins"], "synergies": ["Zhang Fei", "Lady Sun"], "desc": "Jungler Tank/Fighter wujud iblis."},
        {"name": "Ukyo", "tier": "A", "wr": "51.1%", "pr": "12.0%", "br": "3.2%", "counters": ["Early Squishies"], "synergies": ["Mozi", "Xiao Qiao"], "desc": "Samurai burst damage lifesteal cepat."},
        {"name": "Xuance", "tier": "A", "wr": "52.0%", "pr": "13.5%", "br": "15.1%", "counters": ["No-escape Carries"], "synergies": ["Mozi", "Dun", "Xiao Qiao"], "desc": "Assassin hook pancing pembalik posisi."},
        {"name": "Wukong", "tier": "A", "wr": "51.2%", "pr": "22.5%", "br": "12.3%", "counters": ["Squishy Backlines"], "synergies": ["Yaria", "Diao Chan"], "desc": "Raja kera critical burst instan."},
        {"name": "Dian Wei", "tier": "B", "wr": "49.8%", "pr": "14.1%", "br": "2.0%", "counters": ["CC Heavy Comps"], "synergies": ["Cai Yan"], "desc": "Berserker pembersih CC stack true damage."},
        {"name": "Liu Bei", "tier": "B", "wr": "50.1%", "pr": "9.2%", "br": "1.5%", "counters": ["Melee Tanks"], "synergies": ["Yaria"], "desc": "Marksman-Jungle pembantai naga."},
        {"name": "Nakoruru", "tier": "A", "wr": "51.6%", "pr": "13.1%", "br": "6.2%", "counters": ["High HP Tanks"], "synergies": ["Yaria"], "desc": "Assassin burung burst max HP % damage."},
        {"name": "Mai Shiranui (Jungle)", "tier": "B", "wr": "49.5%", "pr": "3.2%", "br": "12.0%", "counters": ["Squishies"], "synergies": ["Dolia"], "desc": "Off-meta mage assassin jungle."},
        {"name": "Prince of Lanling", "tier": "A", "wr": "51.0%", "pr": "16.0%", "br": "22.1%", "counters": ["Immobile Carries"], "synergies": ["Biron"], "desc": "Assassin stealth permanen penculik awal game."},
        {"name": "Han Xin", "tier": "A", "wr": "51.3%", "pr": "17.4%", "br": "11.0%", "counters": ["Slow Rotations"], "synergies": ["Da Qiao"], "desc": "Assassin multi-dash penguasa split push."},
        {"name": "Zilong", "tier": "B", "wr": "50.0%", "pr": "15.2%", "br": "2.0%", "counters": ["Squishy Mages"], "synergies": ["Zhang Fei"], "desc": "Fighter-Assassin spear dive knockup."},
        {"name": "Fang (Jungle)", "tier": "B", "wr": "50.2%", "pr": "8.1%", "br": "1.2%", "counters": ["Early Dragons"], "synergies": ["Dun"], "desc": "MM jungle pengaman objektif cepat."},
        {"name": "Chicha", "tier": "A", "wr": "51.7%", "pr": "11.0%", "br": "5.4%", "counters": ["Melee Junglers"], "synergies": ["Wang Zhaojun"], "desc": "Jungler fleksibel penekan gank."},
        {"name": "Umbrosa", "tier": "A", "wr": "52.3%", "pr": "14.0%", "br": "18.0%", "counters": ["Immobile Backlines"], "synergies": ["Devara"], "desc": "Jungler 6-mark execution rework S16."},
        {"name": "Cirrus", "tier": "B", "wr": "49.1%", "pr": "6.0%", "br": "1.0%", "counters": ["Low CC"], "synergies": ["Yaria"], "desc": "Jungler terbang penembus tembok."},
        {"name": "Ake", "tier": "A", "wr": "51.4%", "pr": "12.5%", "br": "14.2%", "counters": ["Low HP Comps"], "synergies": ["Zhang Fei"], "desc": "Assassin backstab stealth reset cooldown kill."},
        {"name": "Bao Si", "tier": "B", "wr": "48.8%", "pr": "4.0%", "br": "1.0%", "counters": ["Frontlines"], "synergies": ["Dolia"], "desc": "Jungler mage burst bintik energi."}
    ],
    "Mid": [
        {"name": "Haya", "tier": "S", "wr": "56.2%", "pr": "28.0%", "br": "45.1%", "counters": ["Cluster Formations"], "synergies": ["Feyd", "Li Bai", "Augran"], "desc": "Mage S-Tier Red Side Win Rate 80% badai bulan."},
        {"name": "Wang Zhaojun", "tier": "S", "wr": "54.1%", "pr": "31.2%", "br": "22.0%", "counters": ["Dive Comps"], "synergies": ["Biron", "Lady Sun", "Zhang Fei"], "desc": "Mage es pembeku area & shield pasif slow."},
        {"name": "Xiao Qiao", "tier": "S", "wr": "53.8%", "pr": "35.1%", "br": "18.2%", "counters": ["Chokepoints"], "synergies": ["Mozi", "Dun", "Arli"], "desc": "Mage poke & knock-up instan kipas raksasa."},
        {"name": "Lorion", "tier": "S", "wr": "53.5%", "pr": "19.2%", "br": "28.0%", "counters": ["Tight Formations"], "synergies": ["Pei", "Devara", "Lam"], "desc": "Mage bola elektrik perusak formasi udara."},
        {"name": "Heino", "tier": "S", "wr": "53.7%", "pr": "22.1%", "br": "31.0%", "counters": ["Attrition Comps"], "synergies": ["Dolia", "Flowborn (MM)"], "desc": "Mage pemutar waktu reset HP & tower combo Dolia."},
        {"name": "Mai Shiranui", "tier": "S", "wr": "54.5%", "pr": "18.0%", "br": "55.0%", "counters": ["Squishy Backlines"], "synergies": ["Feyd", "Augran"], "desc": "Mage-Assassin energi combo sekali putar."},
        {"name": "Yixing", "tier": "S", "wr": "54.0%", "pr": "17.8%", "br": "24.5%", "counters": ["No-escape Comps"], "synergies": ["Dharma", "Lady Sun", "Dolia"], "desc": "Mage papan catur pengurung area raksasa."},
        {"name": "Nuwa", "tier": "A", "wr": "52.4%", "pr": "11.5%", "br": "9.1%", "counters": ["Long-range Siege"], "synergies": ["Sun Ce", "Nezha", "Li Bai"], "desc": "Mage tembok matriks & teleportasi peta."},
        {"name": "Angela", "tier": "A", "wr": "51.9%", "pr": "38.0%", "br": "8.5%", "counters": ["Frontline Tanks"], "synergies": ["Lam", "Zhang Fei", "Biron"], "desc": "Mage laser burst shield CC-immunity."},
        {"name": "Kui", "tier": "A", "wr": "51.1%", "pr": "16.4%", "br": "15.0%", "counters": ["Immobile Carries"], "synergies": ["Li Bai", "Feyd", "Nuwa"], "desc": "Mage kait pengisolasi 1 target jarak jauh."},
        {"name": "Diao Chan", "tier": "A", "wr": "52.0%", "pr": "21.5%", "br": "29.1%", "counters": ["Skillshot Comps"], "synergies": ["Zhang Fei", "Wukong"], "desc": "Mage penari cooldown reset & true damage."},
        {"name": "Shangguan", "tier": "A", "wr": "52.8%", "pr": "14.2%", "br": "38.2%", "counters": ["Immobile Mages"], "synergies": ["Lam", "Yaria"], "desc": "Mage kuas terbang untargetable backline."},
        {"name": "Zhou Yu", "tier": "A", "wr": "51.5%", "pr": "12.0%", "br": "4.5%", "counters": ["Immobile Turret Push"], "synergies": ["Zhang Fei"], "desc": "Mage api penyebar karpet bakar turret."},
        {"name": "Ganzhi", "tier": "B", "wr": "50.2%", "pr": "8.5%", "br": "2.0%", "counters": ["Melee Tanks"], "synergies": ["Dun"], "desc": "Mage pedang kembar sniper mid."},
        {"name": "Princess Frost", "tier": "S", "wr": "54.0%", "pr": "29.0%", "br": "20.0%", "counters": ["Dive Comps"], "synergies": ["Biron", "Lady Sun"], "desc": "Mage es pembeku area pertahanan."},
        {"name": "Sima Yi", "tier": "A", "wr": "51.8%", "pr": "10.0%", "br": "12.0%", "counters": ["Squishy Mages"], "synergies": ["Feyd"], "desc": "Mage-Assassin bayangan hitam silence."},
        {"name": "Dr Bian", "tier": "A", "wr": "51.9%", "pr": "13.0%", "br": "3.0%", "counters": ["Attrition Tank Comps"], "synergies": ["Zhang Fei", "Dolia"], "desc": "Mage racun & heal sustain pertempuran panjang."},
        {"name": "Milady", "tier": "A", "wr": "51.4%", "pr": "20.0%", "br": "11.0%", "counters": ["Roamed Mages"], "synergies": ["Liu Bei"], "desc": "Mage robot penghancur turret kilat."},
        {"name": "Mozi (Mid)", "tier": "A", "wr": "51.6%", "pr": "15.0%", "br": "8.0%", "counters": ["Long-range Poke"], "synergies": ["Xiao Qiao"], "desc": "Mage tembakan stun jarak jauh."},
        {"name": "Ziya", "tier": "A", "wr": "51.0%", "pr": "11.0%", "br": "5.0%", "counters": ["Level Advantage"], "synergies": ["Lady Sun"], "desc": "Mage penembus batas level 25."},
        {"name": "Gao Changgong", "tier": "B", "wr": "49.2%", "pr": "5.0%", "br": "1.0%", "counters": ["Clustered Enemies"], "synergies": ["Zhang Fei"], "desc": "Mage gitaris aura area damage."},
        {"name": "Wang Wei", "tier": "A", "wr": "52.2%", "pr": "16.0%", "br": "14.0%", "counters": ["Vision Heavy Comps"], "synergies": ["Dunshan"], "desc": "Mage kabut pemanipulasi jarak pandang baru S16."},
        {"name": "Yang Yuhuan", "tier": "A", "wr": "51.8%", "pr": "9.5%", "br": "4.0%", "counters": ["Continuous Fights"], "synergies": ["Sun Ce"], "desc": "Mage kecapi pemulih HP & invulnerable."},
        {"name": "Zhen Ji", "tier": "B", "wr": "50.1%", "pr": "22.0%", "br": "3.0%", "counters": ["Clustered Comps"], "synergies": ["Lian Po"], "desc": "Mage air pembeku gelombang rintangan."},
        {"name": "Xi Shi", "tier": "A", "wr": "52.0%", "pr": "12.0%", "br": "15.0%", "counters": ["Immobile Frontlines"], "synergies": ["Dharma"], "desc": "Mage pemikat pengendali arah musuh."}
    ],
    "Farm": [
        {"name": "Lady Sun", "tier": "S", "wr": "54.8%", "pr": "38.5%", "br": "25.0%", "counters": ["Low Mobility Tanks"], "synergies": ["Yaria", "Dharma", "Yao"], "desc": "MM S-Tier burst rolled-attack penghancur armor."},
        {"name": "Ao'yin (Loong)", "tier": "S", "wr": "55.2%", "pr": "31.0%", "br": "58.0%", "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia", "Zhang Fei"], "desc": "MM naga elemen ulti terbang untargetable."},
        {"name": "Arli", "tier": "S", "wr": "54.2%", "pr": "24.1%", "br": "41.0%", "counters": ["Skillshot Mages"], "synergies": ["Mozi", "Xiao Qiao", "Da Qiao"], "desc": "MM 3-dash parasut paling lincah penepis proyektil."},
        {"name": "Flowborn (MM)", "tier": "S", "wr": "53.9%", "pr": "20.5%", "br": "22.1%", "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce", "Heino"], "desc": "MM fleksibel 5-stack double cast skill barrage."},
        {"name": "Luara", "tier": "A", "wr": "52.1%", "pr": "18.2%", "br": "11.0%", "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun", "Mozi"], "desc": "MM pemanjat dinding pantulan panah bertubi-tubi."},
        {"name": "Marco Polo", "tier": "A", "wr": "51.5%", "pr": "29.0%", "br": "14.2%", "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei", "Yaria"], "desc": "MM pistol ganda true damage & ulti mutar."},
        {"name": "Consort Yu", "tier": "A", "wr": "51.0%", "pr": "19.5%", "br": "8.0%", "counters": ["Physical Assassins"], "synergies": ["Zhang Fei", "Biron"], "desc": "MM imun serangan fisik & sniper jarak jauh."},
        {"name": "Luban No.7", "tier": "B", "wr": "50.2%", "pr": "32.0%", "br": "5.1%", "counters": ["High HP Tanks"], "synergies": ["Zhang Fei", "Cai Yan"], "desc": "MM tembakan roket max HP % damage."},
        {"name": "Shouyue", "tier": "A", "wr": "51.8%", "pr": "21.0%", "br": "18.5%", "counters": ["Vision Comps"], "synergies": ["Mozi", "Nuwa"], "desc": "MM sniper jarak ekstra jauh & trap visi."},
        {"name": "Alessio", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "6.2%", "counters": ["Clustered Tanks"], "synergies": ["Yaria", "Dolia"], "desc": "MM meriam terbang & stealth asap."},
        {"name": "Hou Yi", "tier": "B", "wr": "50.0%", "pr": "28.0%", "br": "3.0%", "counters": ["Low CC Comps"], "synergies": ["Zhang Fei"], "desc": "MM burung matahari DPS tembakan beruntun."},
        {"name": "Meng Ya", "tier": "A", "wr": "51.4%", "pr": "16.0%", "br": "4.0%", "counters": ["Shield Heavy Comps"], "synergies": ["Dolia"], "desc": "MM senapan mesin peluru bertubi-tubi."},
        {"name": "Fang", "tier": "A", "wr": "51.1%", "pr": "12.0%", "br": "2.5%", "counters": ["Early Turrets"], "synergies": ["Dun"], "desc": "MM bom waktu penghancur turret kilat."},
        {"name": "Huang Zhong", "tier": "A", "wr": "51.6%", "pr": "14.0%", "br": "7.0%", "counters": ["Siege Comps"], "synergies": ["Zhang Fei", "Wang Zhaojun"], "desc": "MM meriam benteng serangan jarak jauh area."},
        {"name": "Garo", "tier": "A", "wr": "52.0%", "pr": "18.0%", "br": "16.0%", "counters": ["Shield Heavy Tanks"], "synergies": ["Zhang Fei", "Tai Yi"], "desc": "MM pemutus shield dengan kritikal slow gila."},
        {"name": "Daji (MM Build)", "tier": "B", "wr": "48.0%", "pr": "1.0%", "br": "0.5%", "counters": ["Fun Builds"], "synergies": ["Yaria"], "desc": "Off-meta MM build."},
        {"name": "Erin", "tier": "A", "wr": "51.3%", "pr": "11.0%", "br": "3.0%", "counters": ["Physical Armor Tanks"], "synergies": ["Dolia"], "desc": "MM peri damage sihir murni."},
        {"name": "Di Renjie", "tier": "A", "wr": "51.7%", "pr": "22.0%", "br": "4.0%", "counters": ["CC Heavy Comps"], "synergies": ["Zhang Fei"], "desc": "MM kartu merah pencabut efek CC."},
        {"name": "Cheng Gong", "tier": "B", "wr": "49.5%", "pr": "4.0%", "br": "1.0%", "counters": ["Tanks"], "synergies": ["Dun"], "desc": "MM peluncur tombak burst."},
        {"name": "Baili Shouyue", "tier": "A", "wr": "51.8%", "pr": "21.0%", "br": "18.5%", "counters": ["Vision Comps"], "synergies": ["Mozi"], "desc": "MM sniper jarak jauh trap visi."},
        {"name": "Solaris", "tier": "B", "wr": "49.0%", "pr": "3.0%", "br": "1.0%", "counters": ["Squishies"], "synergies": ["Yaria"], "desc": "MM fajar pemancar sinar laser."}
    ],
    "Roam": [
        {"name": "Zhang Fei", "tier": "S", "wr": "55.1%", "pr": "42.0%", "br": "21.0%", "counters": ["Heavy Dive Comps"], "synergies": ["Lady Sun", "Angela", "Augran"], "desc": "Roamer T0 pelindung carry raungan monster."},
        {"name": "Yaria", "tier": "S", "wr": "54.6%", "pr": "36.2%", "br": "45.0%", "counters": ["Single Target Burst"], "synergies": ["Lady Sun", "Lam", "Ao'yin (Loong)"], "desc": "Support penempel carry +15% gold & shield CC."},
        {"name": "Dolia", "tier": "S", "wr": "54.9%", "pr": "31.5%", "br": "52.0%", "counters": ["Short Cooldown Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"], "desc": "Support duyung pemutar waktu reset ulti."},
        {"name": "Devara", "tier": "A", "wr": "52.3%", "pr": "18.0%", "br": "14.1%", "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"], "desc": "Roamer pilar penjepit lokasi war."},
        {"name": "Mozi", "tier": "S", "wr": "53.8%", "pr": "28.4%", "br": "22.0%", "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Support meriam stun jarak jauh."},
        {"name": "Dun", "tier": "A", "wr": "51.9%", "pr": "20.1%", "br": "3.5%", "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "desc": "Roamer tank hook & knock-up."},
        {"name": "Da Qiao", "tier": "S", "wr": "54.0%", "pr": "25.0%", "br": "48.0%", "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli", "Han Xin"], "desc": "Support portal teleportasi markas global."},
        {"name": "Donghuang", "tier": "S", "wr": "53.5%", "pr": "22.0%", "br": "55.0%", "counters": ["Mobile Assassins"], "synergies": ["Lady Sun", "Angela"], "desc": "Tank kuncian suppress mutlak anti-gocek."},
        {"name": "Liang", "tier": "S", "wr": "53.2%", "pr": "19.0%", "br": "42.0%", "counters": ["High Mobility Divers"], "synergies": ["Augran", "Lady Sun"], "desc": "Support/Mid kuncian suppress ikatan emas."},
        {"name": "Cai Yan", "tier": "A", "wr": "52.1%", "pr": "30.0%", "br": "15.0%", "counters": ["Attrition Poke"], "synergies": ["Luban No.7", "Dian Wei"], "desc": "Support mobil heal & bouncing stun."},
        {"name": "Yao", "tier": "A", "wr": "52.0%", "pr": "18.5%", "br": "12.0%", "counters": ["Squishy Divers"], "synergies": ["Dharma", "Lady Sun"], "desc": "Support energi pelindung & pembalik serangan."},
        {"name": "Kui (Roam)", "tier": "A", "wr": "51.5%", "pr": "16.0%", "br": "15.0%", "counters": ["Immobile Carries"], "synergies": ["Li Bai"], "desc": "Tank kait pancing penarik buff/hero."},
        {"name": "Zhuangzi", "tier": "A", "wr": "52.2%", "pr": "24.0%", "br": "10.0%", "counters": ["CC Heavy Comps"], "synergies": ["Hou Yi", "Diao Chan"], "desc": "Support ikan pelepas efek CC seluruh tim."},
        {"name": "Sun Bin", "tier": "A", "wr": "52.5%", "pr": "17.0%", "br": "8.0%", "counters": ["Poke Comps"], "synergies": ["Biron", "Kaizer"], "desc": "Support waktu pembalik HP & speed boost."},
        {"name": "Agudo", "tier": "A", "wr": "51.8%", "pr": "8.0%", "br": "5.0%", "counters": ["Objective Push"], "synergies": ["Meng Ya"], "desc": "Support/Jungle beruang pemanggil monster."},
        {"name": "Guiguzi", "tier": "A", "wr": "52.8%", "pr": "11.0%", "br": "18.0%", "counters": ["No-Vision Comps"], "synergies": ["Lian Po", "Mulan"], "desc": "Roamer inisiator stealth tim & tarik magnet."},
        {"name": "Tai Yi", "tier": "S", "wr": "53.8%", "pr": "14.0%", "br": "25.0%", "counters": ["Burst Comps"], "synergies": ["Garo", "Lady Sun"], "desc": "Support tungku pembawa emas extra & resurrect."},
        {"name": "Dunshan", "tier": "S", "wr": "53.9%", "pr": "15.0%", "br": "38.0%", "counters": ["Ranged Projectiles"], "synergies": ["Wang Wei", "Lady Sun"], "desc": "Roamer tameng penepis proyektil & nempel turret."},
        {"name": "Ming Shiyin", "tier": "A", "wr": "51.6%", "pr": "16.0%", "br": "11.0%", "counters": ["Solo Carries"], "synergies": ["Sun Wukong", "Lady Sun"], "desc": "Support tali booster attack power/defense."},
        {"name": "Liu Bang", "tier": "A", "wr": "52.0%", "pr": "12.0%", "br": "6.0%", "counters": ["Split Push Focus"], "synergies": ["Nezha", "Lam"], "desc": "Tank ulti teleportasi shield ke rekan tim."},
        {"name": "Suxi", "tier": "B", "wr": "49.5%", "pr": "5.0%", "br": "1.0%", "counters": ["Melee Clustered"], "synergies": ["Xiao Qiao"], "desc": "Support boneka penarik target."},
        {"name": "Lu Bu (Roam)", "tier": "B", "wr": "49.2%", "pr": "8.0%", "br": "5.0%", "counters": ["Melee Tanks"], "synergies": ["Dharma"], "desc": "Off-meta tank ulti arena true damage."}
    ]
}

# Flatten DB list
ALL_HEROES_LIST = []
for r, h_list in HERO_DB.items():
    for h in h_list:
        item = h.copy()
        item["role"] = r
        ALL_HEROES_LIST.append(item)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'used_heroes' not in st.session_state:
    st.session_state['used_heroes'] = []
if 'match_history' not in st.session_state:
    st.session_state['match_history'] = []
if 'game_number' not in st.session_state:
    st.session_state['game_number'] = 1

# ==========================================
# HEADER & TITLE BAR
# ==========================================
st.markdown("<div class='main-title'>⚔️ HOK PRO REAL-TIME DRAFT ENGINE V7</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>116 Heroes DB • 4 Bans Per Side • Dynamic Real-Time Strategy • Flex Counter Radar • Real-Time Item Advisor • By Siropkokop</div>", unsafe_allow_html=True)

# Top Settings Bar
col_top1, col_top2, col_top3, col_top4 = st.columns([2, 2, 2, 2])

with col_top1:
    draft_title = st.text_input("🏷️ Nama Strategy / Match", f"Game {st.session_state['game_number']} - Scrim Match")
with col_top2:
    match_series = st.selectbox("🏆 Format Seri Match", ["Best of 3 (Bo3)", "Best of 5 (Bo5)", "Best of 7 (Bo7)", "Single Match"])
with col_top3:
    our_side = st.radio("🔴🔵 Sisi Tim Kita", ["Blue Side (B1 First Pick)", "Red Side (R5 Counter Pick)"], horizontal=True)
with col_top4:
    st.write(f"🎮 **Fearless Game:** Game {st.session_state['game_number']}")
    if st.button("⏭️ Next Game (Lock Used Heroes)"):
        st.session_state['game_number'] += 1
        st.success("Hero terpakai berhasil di-lock ke Fearless Memory!")
        st.rerun()

st.markdown("---")

# ==========================================
# REAL-TIME DRAFT INPUT SECTION
# ==========================================
col_draft_left, col_draft_right = st.columns([5, 5])

with col_draft_left:
    st.subheader("🛡️ 1. Fase Banning (4 Bans Per Side)")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown("**🔵 BANS TIM KITA (OUR BANS)**")
        our_b1 = st.selectbox("Our Ban 1", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes']], key="ob1")
        our_b2 = st.selectbox("Our Ban 2", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes'] and h["name"] != our_b1], key="ob2")
        our_b3 = st.selectbox("Our Ban 3", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes'] and h["name"] not in [our_b1, our_b2]], key="ob3")
        our_b4 = st.selectbox("Our Ban 4", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes'] and h["name"] not in [our_b1, our_b2, our_b3]], key="ob4")
    
    with col_b2:
        st.markdown("**🔴 BANS TIM MUSUH (ENEMY BANS)**")
        enemy_b1 = st.selectbox("Enemy Ban 1", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes']], key="eb1")
        enemy_b2 = st.selectbox("Enemy Ban 2", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes'] and h["name"] != enemy_b1], key="eb2")
        enemy_b3 = st.selectbox("Enemy Ban 3", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes'] and h["name"] not in [enemy_b1, enemy_b2]], key="eb3")
        enemy_b4 = st.selectbox("Enemy Ban 4", ["None"] + [h["name"] for h in ALL_HEROES_LIST if h["name"] not in st.session_state['used_heroes'] and h["name"] not in [enemy_b1, enemy_b2, enemy_b3]], key="eb4")

    all_bans = [b for b in [our_b1, our_b2, our_b3, our_b4, enemy_b1, enemy_b2, enemy_b3, enemy_b4] if b != "None"]

    st.markdown("---")
    st.subheader("⚔️ 2. Fase Picking (Real-Time Picks per Role)")
    
    col_p1, col_p2 = st.columns(2)
    
    def get_pick_opts(role_name, current_selected=None):
        avail = [h["name"] for h in HERO_DB[role_name] if h["name"] not in st.session_state['used_heroes'] and h["name"] not in all_bans]
        if current_selected and current_selected != "None" and current_selected not in avail:
            avail.append(current_selected)
        return ["None"] + sorted(list(set(avail)))

    with col_p1:
        st.markdown("**💙 PICKS TIM KITA**")
        our_clash = st.selectbox("Clash Lane", get_pick_opts("Clash"), key="op_clash")
        our_jungle = st.selectbox("Jungle", get_pick_opts("Jungle"), key="op_jungle")
        our_mid = st.selectbox("Mid Lane", get_pick_opts("Mid"), key="op_mid")
        our_farm = st.selectbox("Farm Lane (MM)", get_pick_opts("Farm"), key="op_farm")
        our_roam = st.selectbox("Roam / Support", get_pick_opts("Roam"), key="op_roam")

    with col_p2:
        st.markdown("**❤️ PICKS TIM MUSUH**")
        enemy_clash = st.selectbox("Enemy Clash", get_pick_opts("Clash"), key="ep_clash")
        enemy_jungle = st.selectbox("Enemy Jungle", get_pick_opts("Jungle"), key="ep_jungle")
        enemy_mid = st.selectbox("Enemy Mid", get_pick_opts("Mid"), key="ep_mid")
        enemy_farm = st.selectbox("Enemy Farm", get_pick_opts("Farm"), key="ep_farm")
        enemy_roam = st.selectbox("Enemy Roam", get_pick_opts("Roam"), key="ep_roam")

    our_picks = [p for p in [our_clash, our_jungle, our_mid, our_farm, our_roam] if p != "None"]
    enemy_picks = [p for p in [enemy_clash, enemy_jungle, enemy_mid, enemy_farm, enemy_roam] if p != "None"]

    st.markdown(" ")
    if st.button("🔒 Save Current Picks to Fearless Memory"):
        for p in our_picks:
            if p not in st.session_state['used_heroes']:
                st.session_state['used_heroes'].append(p)
        st.success("Hero berhasil disimpan ke memori Fearless!")
        st.rerun()

# ==========================================
# REAL-TIME INSTANT CALCULATOR & TACTICAL DASHBOARD
# ==========================================
with col_draft_right:
    st.subheader("📊 3. Real-Time Calculation & Flex Radar")

    # INSTANT CALCULATIONS
    base_score = 50.0
    
    # Tier bonuses for our picks
    for p in our_picks:
        h_info = next((item for item in ALL_HEROES_LIST if item["name"] == p), None)
        if h_info:
            if h_info["tier"] == "S":
                base_score += 4.5
            elif h_info["tier"] == "A":
                base_score += 2.5
            
            if "Red Side" in our_side and p in ["Haya", "Ao'yin (Loong)", "Zhang Fei", "Florentino", "Augran"]:
                base_score += 3.5

    # Deduct enemy picks power
    for ep in enemy_picks:
        eh_info = next((item for item in ALL_HEROES_LIST if item["name"] == ep), None)
        if eh_info:
            if eh_info["tier"] == "S":
                base_score -= 4.0
            elif eh_info["tier"] == "A":
                base_score -= 2.0

    # Extended Synergy Calculations
    active_synergies = []
    
    if "Dolia" in our_picks and "Heino" in our_picks:
        base_score += 5.0
        active_synergies.append("⏳ **Dolia + Heino**: Celestial Reset / Time Rewind Ultimate!")
    if "Mozi" in our_picks and ("Xiao Qiao" in our_picks or "Arli" in our_picks):
        base_score += 4.0
        active_synergies.append("⚡ **Mozi + Xiao Qiao/Arli**: Unli CC Stun Lock & Long-range Poke!")
    if "Yaria" in our_picks and ("Lady Sun" in our_picks or "Ao'yin (Loong)" in our_picks or "Lam" in our_picks):
        base_score += 4.0
        active_synergies.append("🛡️ **Yaria + Carry**: Support Revamp +15% Gold & Anti-Dive Shield!")
    if "Zhang Fei" in our_picks and ("Lady Sun" in our_picks or "Angela" in our_picks or "Biron" in our_picks):
        base_score += 3.5
        active_synergies.append("🦁 **Zhang Fei + Angela/Lady Sun**: Anti-Dive Rage Shield & Counter Engage!")
    if "Da Qiao" in our_picks and ("Sun Ce" in our_picks or "Arli" in our_picks or "Han Xin" in our_picks):
        base_score += 4.0
        active_synergies.append("🚀 **Da Qiao + Sun Ce/Arli**: Global Teleportation Portal & Fast Rotations!")
    if "Dharma" in our_picks and ("Yixing" in our_picks or "Yao" in our_picks):
        base_score += 3.5
        active_synergies.append("🥊 **Dharma + Yixing**: Wall Slam Cage & Instant Chokepoint Burst!")
    if "Kui" in our_picks and ("Li Bai" in our_picks or "Feyd" in our_picks or "Nuwa" in our_picks):
        base_score += 3.5
        active_synergies.append("🪝 **Kui + Li Bai/Feyd**: Hook Isolation & Fog of War Execution!")
    if "Wang Zhaojun" in our_picks and ("Biron" in our_picks or "Allain" in our_picks):
        base_score += 3.0
        active_synergies.append("❄️ **Wang Zhaojun + Biron/Allain**: Freeze Area & Melee Knockup Layering!")
    if "Pei" in our_picks and ("Devara" in our_picks or "Biron" in our_picks):
        base_score += 3.5
        active_synergies.append("🐯 **Pei + Devara/Biron**: Early Invade Domination (0:30 Buff Rush)!")
    if "Shangguan" in our_picks and ("Yaria" in our_picks or "Lam" in our_picks):
        base_score += 3.5
        active_synergies.append("🖌️ **Shangguan + Yaria**: Untargetable Fly Dive & Shield Protection!")

    our_win_rate = min(max(round(base_score, 1), 20.0), 85.0)
    enemy_win_rate = round(100.0 - our_win_rate, 1)

    # 1. Real-Time Gauge Display
    st.markdown(f"#### 📈 Estimated Win Probability: **{our_win_rate}%** (Kita) vs **{enemy_win_rate}%** (Musuh)")
    st.progress(int(our_win_rate))

    # Active Synergies Display
    if active_synergies:
        st.markdown("##### 🟢 Active Real-Time Synergies Detected:")
        for syn in active_synergies:
            st.markdown(f"<div class='flex-synergy-card'>{syn}</div>", unsafe_allow_html=True)

    # 2. FLEX REAL-TIME ENEMY COUNTER RADAR
    st.markdown("#### 🎯 Flex Real-Time Counter Radar (Enemy Response)")
    if not enemy_picks:
        st.info("💡 Belum ada hero musuh yang dipilih. Radar akan aktif secara instan begitu musuh memilih hero!")
    else:
        for ep in enemy_picks:
            eh_info = next((item for item in ALL_HEROES_LIST if item["name"] == ep), None)
            if eh_info:
                e_role = eh_info["role"]
                # Find top 3 available counters from DB for this enemy hero
                suggested_counters = []
                for db_h in HERO_DB[e_role]:
                    if db_h["name"] not in st.session_state['used_heroes'] and db_h["name"] not in all_bans and db_h["name"] not in our_picks and db_h["name"] not in enemy_picks:
                        suggested_counters.append(f"**{db_h['name']}** ({db_h['tier']}-Tier)")
                    if len(suggested_counters) >= 3:
                        break
                
                c_str = ", ".join(suggested_counters) if suggested_counters else "Lihat DB / Hero Terpakai"
                
                st.markdown(f"""
                <div class='flex-radar-card'>
                    <b>❤️ Target Musuh Picked:</b> <span class='badge-s'>{ep}</span> ({e_role} • {eh_info['tier']}-Tier)<br/>
                    <b>💡 Recommended Counter Picks (Tersedia):</b> {c_str}<br/>
                    <b>📝 Spesialisasi / Taktik Counter:</b> {eh_info['desc']}
                </div>
                """, unsafe_allow_html=True)

    # 3. REAL-TIME ITEM COUNTER ADVISOR
    st.markdown("#### 🛡️ Real-Time Item Counter Advisor")
    item_recoms = []
    
    # Check enemy composition traits
    enemy_names_str = " ".join(enemy_picks)
    
    # Anti-heal condition
    if any(h in enemy_picks for h in ["Cheng Yaojin", "Cai Yan", "Yaria", "Yang Jian", "Lian Po", "Dr Bian", "Ata"]):
        item_recoms.append("🩸 **Mortal Punishment / Venomous Strike / Nightmare Fang**: WAJIB dibuat sebelum menit ke-6 untuk memotong 50% HP regen/heal musuh!")
    
    # Heavy Phys Burst / Crit condition
    if any(h in enemy_picks for h in ["Wukong", "Ake", "Lady Sun", "Consort Yu", "Consort Yu", "Luban No.7", "Hou Yi"]):
        item_recoms.append("🛡️ **Ominous Premonition / Cuirass of Savagery**: Menurunkan attack speed & movement speed musuh saat diserang fisikal burst!")
        
    # Heavy Magic Burst / CC condition
    if any(h in enemy_picks for h in ["Haya", "Mai Shiranui", "Shangguan", "Xiao Qiao", "Angela", "Wang Zhaojun"]):
        item_recoms.append("🔮 **Witch's Cloak / Glacial Buckler / Holy Grail**: Menyuplai magic shield tebal & mengurangi durasi crowd control!")
        
    # Heavy Tank / Armor condition
    if any(h in enemy_picks for h in ["Dun", "Zhang Fei", "Biron", "Kaizer", "Lian Po", "Arthur"]):
        item_recoms.append("⚔️ **Shadow Blade / Star-Breaker / Void Staff**: Penembus armor fisikal & sihir persentase max HP damage!")
        
    # Lock-on Dive / Execution condition
    if any(h in enemy_picks for h in ["Nezha", "Lam", "Jing", "Prince of Lanling", "Guan Yu"]):
        item_recoms.append("🛡️ **Pure Sky / Splendor / Sage's Sanctuary**: Aktifkan damage reduction 35%-50% / stasis untargetable / efek hidup kembali pas war!")

    if item_recoms:
        for itm in item_recoms:
            st.markdown(f"<div class='flex-item-card'>{itm}</div>", unsafe_allow_html=True)
    else:
        st.caption("Pilih hero musuh untuk memicu rekomendasi item counter wajib!")

st.markdown("---")

# ==========================================
# REAL-TIME DYNAMIC IN-GAME STRATEGY SCHEME
# ==========================================
st.subheader("🧭 4. Dynamic Real-Time In-Game Macro Strategy")

schema_col1, schema_col2 = st.columns(2)

with schema_col1:
    st.markdown("#### ⚡ 1. Early Game Dynamic Plan (Menit 0:00 - 4:00)")
    
    if any(p in our_picks for p in ["Pei", "Biron", "Ukyo", "Fatih"]):
        st.write("• **INVADE AGGRESSION (Menit 0:30):** Kita punya hero early invade kuat! Roamer & Mid dampingi Jungle langsung sergap Babi/Buff Merah musuh di menit 0:30.")
    else:
        st.write("• **STANDARD WAVE CLEAR & MID PRIO:** Roamer bantu Mid sapu wave pertama minion. Amankan visi sungai & curi babi kecil musuh jika memungkinkan.")
        
    st.write("• **SPACE SPRITE CONTEST (Menit 1:00):** Clash Lane wajib amankan bunga teleportasi buat gank kilat ke Farm Lane.")
    st.write("• **LEVEL 4 POWER SPIKE (Menit 1:20 - 2:00):** Jungle selesai clear hutan pertama. Lakukan gank pertama ke lane musuh yang overextend.")

    st.markdown("#### ⚔️ 2. Mid Game Dynamic Plan (Menit 4:00 - 10:00)")
    st.write("• **TURRET PLATE COLLAPSE (Menit 4:00):** Pelat turret rontok. Alihkan prioritas ke **Tyrant pertama** buat dapet buff damage serangan!")
    st.write("• **GOLD SHARING RULES:** Terapkan 2-player wave sharing (160% total gold) di Mid Lane buat ngeboost ekonomi MM & Jungle.")
    st.write("• **PRIMAL BOND AWARENESS:** Jangan bunuh Overlord & Tyrant bersamaan! Kena debuff -50% damage ke naga kedua selama 90 detik.")

with schema_col2:
    st.markdown("#### 🏆 3. Late Game & Teamfight Execution (Menit 10:00 - 20:00+)")
    
    if any(p in our_picks for p in ["Lady Sun", "Ao'yin (Loong)", "Luban No.7"]):
        st.write("• **CORE PROTECTION (Peel Carry):** Marksman kita adalah finisher utama late game. Roamer & Tank wajib pasang badan di depan.")
    elif any(p in our_picks for p in ["Arli", "Marco Polo"]):
        st.write("• **KITING & FLANK STRATEGY:** Marksman gocek dari semak samping, tumpukan CC Roamer pemicu ruang bebas hit.")
        
    if any(p in enemy_picks for p in ["Nezha", "Lam", "Mai Shiranui", "Jing"]):
        st.write("• **DIVE DEFENSE FORMATION:** Musuh punya hero dive mematikan! Mid & MM dilarang jalan sendirian tanpa kawalan Roamer.")
        
    if any(p in our_picks for p in ["Angela", "Wang Zhaojun", "Xiao Qiao", "Yixing"]):
        st.write("• **CHOKEPOINT STUN LOCK:** Pancing war di area sempit dekat sungai/naga biar AoE skill Mid hit 3-5 orang instan.")
        
    st.write("• **TEMPEST DRAGON PENENTU (Menit 20:00+):** Peringatan keras! **Dilarang bunuh naga biasa di menit 18:30-19:00** biar tidak kena debuff Primal Bond (-60% damage) pas Tempest Dragon muncul di menit 20:00!")

st.markdown("---")

# ==========================================
# EXPORT, HISTORY LOG & DATABASE TABS
# ==========================================
tab_export, tab_history, tab_database = st.tabs(["📲 Export to WhatsApp", "📊 Recent Match Analysis", "📚 Complete 116 Hero Database S16"])

with tab_export:
    st.subheader("📋 WhatsApp Copy-Paste Summary")
    
    wa_text = f"""*BLUEPRINT DRAFT HOK V7* 🎮🔥
*Title:* {draft_title}
*Series:* {match_series} | *Side:* {our_side}
*Win Probability Engine:* {our_win_rate}% (Our Team)

🚫 *BANS:*
• *Our Bans:* {', '.join([h for h in [our_b1, our_b2, our_b3, our_b4] if h != 'None']) or 'None'}
• *Enemy Bans:* {', '.join([h for h in [enemy_b1, enemy_b2, enemy_b3, enemy_b4] if h != 'None']) or 'None'}

🛡️ *OUR PICKS:*
• *Clash:* {our_clash} | *Jungle:* {our_jungle} | *Mid:* {our_mid} | *Farm:* {our_farm} | *Roam:* {our_roam}

🔴 *ENEMY PICKS:*
• *Clash:* {enemy_clash} | *Jungle:* {enemy_jungle} | *Mid:* {enemy_mid} | *Farm:* {enemy_farm} | *Roam:* {enemy_roam}

⚡ *REAL-TIME STRATEGY & ITEM COUNTERS:*
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

    if st.session_state['match_history']:
        st.markdown("#### 📜 History Match Logged")
        df_hist = pd.DataFrame(st.session_state['match_history'])
        st.dataframe(df_hist, use_container_width=True)

with tab_database:
    st.subheader("📚 Complete 116 Hero Database & Stats (Season 16)")
    
    search_q = st.text_input("🔍 Search Hero Name / Skill / Trait:", "")
    role_filter = st.radio("Filter Role:", ["All", "Clash", "Jungle", "Mid", "Farm", "Roam"], horizontal=True)
    
    filtered_db = []
    for r, h_list in HERO_DB.items():
        if role_filter == "All" or role_filter == r:
            for h in h_list:
                if not search_q or search_q.lower() in h["name"].lower() or search_q.lower() in h["desc"].lower():
                    item = h.copy()
                    item["Role"] = r
                    filtered_db.append(item)
                
    df_db = pd.DataFrame(filtered_db)[["name", "Role", "tier", "wr", "pr", "br", "desc"]]
    df_db.columns = ["Hero Name", "Role", "Tier", "Win Rate", "Pick Rate", "Ban Rate", "Specialization / Description"]
    st.dataframe(df_db, use_container_width=True)

# Footer Credit
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>HOK Draft & Strategy Engine V7 • Built for Esports Analytics • Credit: <b>By Siropkokop</b></div>", unsafe_allow_html=True)
