import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Pro Draft & Strategy Engine S16 | By Siropkokop",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Esports Dark Theme & Compact Ergonomic UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFD700;
        text-align: center;
        margin-bottom: 0px;
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
        margin-bottom: 8px;
    }
    .metric-box {
        background-color: #11111B;
        border-left: 4px solid #FFD700;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .badge-s { background-color: #E74C3C; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-a { background-color: #F39C12; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-b { background-color: #3498DB; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-counter { background-color: #8E44AD; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-role { background-color: #2980B9; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .alert-danger { background-color: #421212; border: 1px solid #E74C3C; color: #FF9999; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
    .alert-success { background-color: #123318; border: 1px solid #2ECC71; color: #99FFBB; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
    .counter-card { background-color: #2A1B3D; border: 1px solid #9B59B6; color: #F1A9A0; padding: 10px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# COMPLETE 116 HEROES DATABASE (SEASON 16)
# ==========================================
HERO_DB = {
    "Clash": [
        {"name": "Biron", "tier": "S", "wr": "54.2%", "pr": "28.5%", "br": "15.2%", "counters": ["Physical Fighters", "Nezha", "Kaizer"], "synergies": ["Zhang Fei", "Dun", "Angela"], "desc": "Frontline shield & sustain badak."},
        {"name": "Florentino", "tier": "S", "wr": "53.8%", "pr": "18.2%", "br": "42.1%", "counters": ["Tank Heavy", "Arthur", "Dun"], "synergies": ["Yaria", "Dolia"], "desc": "Duelis 1v1 gocekan bunga frame-perfect."},
        {"name": "Dharma", "tier": "S", "wr": "53.5%", "pr": "22.1%", "br": "25.0%", "counters": ["Immobile Squishies", "Xiao Qiao", "Lady Sun"], "synergies": ["Lady Sun", "Yao", "Yixing"], "desc": "Inisiator wall-slam pembuka war sempit."},
        {"name": "Charlotte", "tier": "S", "wr": "53.1%", "pr": "17.5%", "br": "18.4%", "counters": ["Attack Speed Carries", "Marco Polo", "Wukong", "Allain"], "synergies": ["Zhang Fei", "Wang Zhaojun"], "desc": "Counter alami hero fisik & attack speed."},
        {"name": "Allain", "tier": "A", "wr": "51.8%", "pr": "19.4%", "br": "10.5%", "counters": ["Squishy Carries", "Luban No.7"], "synergies": ["Wang Zhaojun", "Dolia"], "desc": "Duelist hybrid damage untargetable ulti."},
        {"name": "Sun Ce", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "8.2%", "counters": ["Split Pushers", "Shouyue", "Hou Yi"], "synergies": ["Da Qiao", "Nuwa"], "desc": "Penguasa kapal rotasi global gank kilat."},
        {"name": "Fatih", "tier": "A", "wr": "50.8%", "pr": "12.3%", "br": "5.1%", "counters": ["Melee Fighters"], "synergies": ["Devara", "Kui"], "desc": "Fighter crowd control perusak formasi."},
        {"name": "Li Xin", "tier": "A", "wr": "50.5%", "pr": "16.8%", "br": "6.0%", "counters": ["Immobile Mages", "Angela"], "synergies": ["Dolia", "Zhang Fei"], "desc": "Dual form: Light AoE & Dark Split Push."},
        {"name": "Guan Yu", "tier": "A", "wr": "51.0%", "pr": "11.2%", "br": "14.1%", "counters": ["No-CC Comps", "Wang Zhaojun"], "synergies": ["Da Qiao", "Yixing"], "desc": "Inisiator kuda pendorong formasi musuh."},
        {"name": "Mulan", "tier": "A", "wr": "50.9%", "pr": "13.4%", "br": "9.2%", "counters": ["Squishy Mages", "Xiao Qiao"], "synergies": ["Lam", "Lorion"], "desc": "Assassin dual blade & heavy sword combo."},
        {"name": "Mayene", "tier": "A", "wr": "51.5%", "pr": "14.2%", "br": "12.0%", "counters": ["Solo Laners"], "synergies": ["Augran", "Dolia"], "desc": "Fighter silat mobilitas tinggi."},
        {"name": "Dun", "tier": "A", "wr": "52.0%", "pr": "21.0%", "br": "4.5%", "counters": ["Dive Assassins", "Lam", "Nezha"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Tank pasak bumi true damage & regen."},
        {"name": "Nezha", "tier": "A", "wr": "51.4%", "pr": "10.1%", "br": "7.8%", "counters": ["Healers", "Cai Yan", "Shouyue"], "synergies": ["Pei", "Nuwa"], "desc": "Global lock-on target & anti-heal."},
        {"name": "Ata", "tier": "B", "wr": "49.5%", "pr": "8.0%", "br": "2.1%", "counters": ["Non-dash Heroes"], "synergies": ["Lady Sun", "Angela"], "desc": "Tank pembangun tembok penghalang."},
        {"name": "Arthur", "tier": "B", "wr": "49.8%", "pr": "18.0%", "br": "1.0%", "counters": ["High Mobility", "Arli", "Li Bai"], "synergies": ["Cai Yan"], "desc": "Fighter simpel penekan silence."},
        {"name": "Wuyan", "tier": "B", "wr": "50.1%", "pr": "9.5%", "br": "2.0%", "counters": ["Melee Clustered"], "synergies": ["Zhang Fei"], "desc": "Fighter palu efek petrik pasif."},
        {"name": "Kaizer (Clash)", "tier": "A", "wr": "51.5%", "pr": "12.0%", "br": "3.5%", "counters": ["Burst Damage"], "synergies": ["Lady Sun"], "desc": "Fighter wujud iblis penahan gempuran."},
        {"name": "Sun Wukong (Clash)", "tier": "B", "wr": "49.2%", "pr": "5.0%", "br": "2.0%", "counters": ["Squishies"], "synergies": ["Yaria"], "desc": "Crit burst melee fighter."},
        {"name": "Lian Po", "tier": "A", "wr": "51.3%", "pr": "10.5%", "br": "3.0%", "counters": ["CC Comps"], "synergies": ["Xiao Qiao"], "desc": "Tank super immune CC inisiator 3-step knockup."},
        {"name": "Meng Ya (Clash)", "tier": "B", "wr": "48.9%", "pr": "3.0%", "br": "1.0%", "counters": ["Melee Tanks"], "synergies": ["Dolia"], "desc": "Off-meta clash lane heavy sustain."},
        {"name": "Yang Jian", "tier": "B", "wr": "49.6%", "pr": "6.2%", "br": "1.5%", "counters": ["Low HP Targets"], "synergies": ["Kui"], "desc": "Fighter anjing pelacak true damage laser."},
        {"name": "Sima Yi (Clash)", "tier": "B", "wr": "49.0%", "pr": "4.1%", "br": "3.0%", "counters": ["Magic Damage", "Xiao Qiao", "Angela"], "synergies": ["Feyd"], "desc": "Anti-mage silence diver."},
        {"name": "Cheng Yaojin", "tier": "B", "wr": "50.0%", "pr": "11.0%", "br": "2.5%", "counters": ["Low Anti-heal"], "synergies": ["Dolia"], "desc": "Tank regen HP gila splitter lane."}
    ],
    "Jungle": [
        {"name": "Augran", "tier": "S", "wr": "55.8%", "pr": "32.1%", "br": "58.4%", "counters": ["Wall Huggers", "Tanks", "Kaizer"], "synergies": ["Biron", "Zhang Fei", "Angela"], "desc": "Jungler T0 soul absorber HP drain."},
        {"name": "Lam", "tier": "S", "wr": "54.9%", "pr": "29.8%", "br": "62.0%", "counters": ["Low HP Squishies", "Lady Sun", "Shouyue"], "synergies": ["Yaria", "Angela", "Wang Zhaojun"], "desc": "Assassin hiu pasif true damage <30% HP."},
        {"name": "Feyd", "tier": "S", "wr": "53.9%", "pr": "21.4%", "br": "35.2%", "counters": ["Backline MM", "Luban No.7", "Hou Yi"], "synergies": ["Kui", "Devara", "Haya"], "desc": "Assassin bayangan penyergap fog of war."},
        {"name": "Jing", "tier": "S", "wr": "54.1%", "pr": "15.2%", "br": "48.0%", "counters": ["Clustered Comps", "Wang Zhaojun"], "synergies": ["Yixing", "Dolia"], "desc": "Assassin cermin infinite swap dash."},
        {"name": "Luna", "tier": "S", "wr": "53.9%", "pr": "11.8%", "br": "52.1%", "counters": ["No-Hard-CC", "Marco Polo"], "synergies": ["Da Qiao", "Zhang Fei"], "desc": "Mage-Assassin mark reset ulti tanpa batas."},
        {"name": "Li Bai", "tier": "A", "wr": "52.1%", "pr": "18.5%", "br": "11.2%", "counters": ["Skillshot Mages", "Angela"], "synergies": ["Kui", "Nuwa", "Devara"], "desc": "Assassin 2 untargetable & dash shadow return."},
        {"name": "Pei", "tier": "A", "wr": "51.8%", "pr": "14.2%", "br": "19.0%", "counters": ["Slow Early Junglers", "Wukong"], "synergies": ["Biron", "Devara", "Nezha"], "desc": "Jungler harimau invade menit 0:30."},
        {"name": "Musashi", "tier": "A", "wr": "51.5%", "pr": "16.1%", "br": "8.4%", "counters": ["Healers", "Cai Yan", "Shields", "Yaria"], "synergies": ["Dolia", "Xiao Qiao"], "desc": "Pendekar pemotong shield single target lock."},
        {"name": "Kaizer", "tier": "A", "wr": "52.2%", "pr": "24.0%", "br": "5.1%", "counters": ["Burst Assassins", "Prince of Lanling"], "synergies": ["Zhang Fei", "Lady Sun"], "desc": "Jungler Tank/Fighter wujud iblis."},
        {"name": "Ukyo", "tier": "A", "wr": "51.1%", "pr": "12.0%", "br": "3.2%", "counters": ["Early Squishies"], "synergies": ["Mozi", "Xiao Qiao"], "desc": "Samurai burst damage lifesteal cepat."},
        {"name": "Xuance", "tier": "A", "wr": "52.0%", "pr": "13.5%", "br": "15.1%", "counters": ["No-escape Carries", "Lady Sun"], "synergies": ["Mozi", "Dun", "Xiao Qiao"], "desc": "Assassin hook pancing pembalik posisi."},
        {"name": "Wukong", "tier": "A", "wr": "51.2%", "pr": "22.5%", "br": "12.3%", "counters": ["Squishy Backlines", "Xiao Qiao"], "synergies": ["Yaria", "Diao Chan"], "desc": "Raja kera critical burst instan."},
        {"name": "Dian Wei", "tier": "B", "wr": "49.8%", "pr": "14.1%", "br": "2.0%", "counters": ["CC Heavy Comps"], "synergies": ["Cai Yan"], "desc": "Berserker pembersih CC stack true damage."},
        {"name": "Liu Bei", "tier": "B", "wr": "50.1%", "pr": "9.2%", "br": "1.5%", "counters": ["Melee Tanks"], "synergies": ["Yaria"], "desc": "Marksman-Jungle pembantai naga."},
        {"name": "Nakoruru", "tier": "A", "wr": "51.6%", "pr": "13.1%", "br": "6.2%", "counters": ["High HP Tanks"], "synergies": ["Yaria"], "desc": "Assassin burung burst max HP % damage."},
        {"name": "Mai Shiranui (Jungle)", "tier": "B", "wr": "49.5%", "pr": "3.2%", "br": "12.0%", "counters": ["Squishies"], "synergies": ["Dolia"], "desc": "Off-meta mage assassin jungle."},
        {"name": "Prince of Lanling", "tier": "A", "wr": "51.0%", "pr": "16.0%", "br": "22.1%", "counters": ["Immobile Carries", "Luban No.7", "Angela"], "synergies": ["Biron"], "desc": "Assassin stealth permanen penculik awal game."},
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
        {"name": "Haya", "tier": "S", "wr": "56.2%", "pr": "28.0%", "br": "45.1%", "counters": ["Cluster Formations", "Angela"], "synergies": ["Feyd", "Li Bai", "Augran"], "desc": "Mage S-Tier Red Side Win Rate 80% badai bulan."},
        {"name": "Wang Zhaojun", "tier": "S", "wr": "54.1%", "pr": "31.2%", "br": "22.0%", "counters": ["Dive Comps", "Lam", "Nezha"], "synergies": ["Biron", "Lady Sun", "Zhang Fei"], "desc": "Mage es pembeku area & shield pasif slow."},
        {"name": "Xiao Qiao", "tier": "S", "wr": "53.8%", "pr": "35.1%", "br": "18.2%", "counters": ["Chokepoints", "Luban No.7"], "synergies": ["Mozi", "Dun", "Arli"], "desc": "Mage poke & knock-up instan kipas raksasa."},
        {"name": "Lorion", "tier": "S", "wr": "53.5%", "pr": "19.2%", "br": "28.0%", "counters": ["Tight Formations"], "synergies": ["Pei", "Devara", "Lam"], "desc": "Mage bola elektrik perusak formasi udara."},
        {"name": "Heino", "tier": "S", "wr": "53.7%", "pr": "22.1%", "br": "31.0%", "counters": ["Attrition Comps"], "synergies": ["Dolia", "Flowborn (MM)"], "desc": "Mage pemutar waktu reset HP & tower combo Dolia."},
        {"name": "Mai Shiranui", "tier": "S", "wr": "54.5%", "pr": "18.0%", "br": "55.0%", "counters": ["Squishy Backlines", "Xiao Qiao", "Lady Sun"], "synergies": ["Feyd", "Augran"], "desc": "Mage-Assassin energi combo sekali putar."},
        {"name": "Yixing", "tier": "S", "wr": "54.0%", "pr": "17.8%", "br": "24.5%", "counters": ["No-escape Comps", "Marco Polo"], "synergies": ["Dharma", "Lady Sun", "Dolia"], "desc": "Mage papan catur pengurung area raksasa."},
        {"name": "Nuwa", "tier": "A", "wr": "52.4%", "pr": "11.5%", "br": "9.1%", "counters": ["Long-range Siege"], "synergies": ["Sun Ce", "Nezha", "Li Bai"], "desc": "Mage tembok matriks & teleportasi peta."},
        {"name": "Angela", "tier": "A", "wr": "51.9%", "pr": "38.0%", "br": "8.5%", "counters": ["Frontline Tanks", "Dun", "Arthur"], "synergies": ["Lam", "Zhang Fei", "Biron"], "desc": "Mage laser burst shield CC-immunity."},
        {"name": "Kui", "tier": "A", "wr": "51.1%", "pr": "16.4%", "br": "15.0%", "counters": ["Immobile Carries", "Shouyue"], "synergies": ["Li Bai", "Feyd", "Nuwa"], "desc": "Mage kait pengisolasi 1 target jarak jauh."},
        {"name": "Diao Chan", "tier": "A", "wr": "52.0%", "pr": "21.5%", "br": "29.1%", "counters": ["Skillshot Comps", "Angela", "Biron"], "synergies": ["Zhang Fei", "Wukong"], "desc": "Mage penari cooldown reset & true damage."},
        {"name": "Shangguan", "tier": "A", "wr": "52.8%", "pr": "14.2%", "br": "38.2%", "counters": ["Immobile Mages", "Xiao Qiao"], "synergies": ["Lam", "Yaria"], "desc": "Mage kuas terbang untargetable backline."},
        {"name": "Milady", "tier": "A", "wr": "51.5%", "pr": "15.0%", "br": "12.0%", "counters": ["Slow Wave Clear"], "synergies": ["Liu Bei"], "desc": "Mage robot penekan push turret instan."},
        {"name": "Ganning", "tier": "A", "wr": "51.2%", "pr": "10.0%", "br": "4.0%", "counters": ["Dive Mages"], "synergies": ["Zhang Fei"], "desc": "Mage zonasi ombak laut."},
        {"name": "Princess Frost", "tier": "S", "wr": "54.0%", "pr": "28.0%", "br": "20.0%", "counters": ["Melee Inisiators", "Nezha"], "synergies": ["Biron"], "desc": "Mage kontrol es pendukung defense."},
        {"name": "Mozi (Mid)", "tier": "A", "wr": "52.1%", "pr": "12.0%", "br": "8.0%", "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao"], "desc": "Mage canon stun jarak jauh."},
        {"name": "Zhou Yu", "tier": "A", "wr": "51.8%", "pr": "11.2%", "br": "3.1%", "counters": ["Immobile Tanks"], "synergies": ["Dun"], "desc": "Mage api penyebar karpet pembakar."},
        {"name": "Zhuge Liang", "tier": "A", "wr": "51.4%", "pr": "18.0%", "br": "10.0%", "counters": ["Low HP Targets"], "synergies": ["Yaria"], "desc": "Mage execution meteor ganda."},
        {"name": "Sima Yi", "tier": "A", "wr": "52.0%", "pr": "11.0%", "br": "14.0%", "counters": ["Squishy Mages"], "synergies": ["Lam"], "desc": "Mage assassin silence gank kilat."},
        {"name": "Gao Chian", "tier": "B", "wr": "50.0%", "pr": "8.0%", "br": "2.0%", "counters": ["Melee Formations"], "synergies": ["Zhang Fei"], "desc": "Mage musik burst damage area."},
        {"name": "Dr Bian", "tier": "B", "wr": "50.3%", "pr": "9.1%", "br": "1.5%", "counters": ["Attrition Fights"], "synergies": ["Cai Yan"], "desc": "Mage racun & heal bertahap."},
        {"name": "Zhen Ji", "tier": "A", "wr": "51.9%", "pr": "22.0%", "br": "6.0%", "counters": ["Clustered Enemies"], "synergies": ["Lian Po"], "desc": "Mage pantulan bola es pembeku."},
        {"name": "Sun Bin (Mid)", "tier": "B", "wr": "49.5%", "pr": "4.0%", "br": "1.0%", "counters": ["Poke Comps"], "synergies": ["Marco Polo"], "desc": "Mage utility pemutar CD & speed boost."},
        {"name": "Wang Wei", "tier": "S", "wr": "53.6%", "pr": "16.0%", "br": "25.0%", "counters": ["Vision Comps"], "synergies": ["Augran"], "desc": "Mage kabut mistik pembuka S16."},
        {"name": "Xi Shi", "tier": "A", "wr": "52.0%", "pr": "12.0%", "br": "15.0%", "counters": ["Immobile Frontlines"], "synergies": ["Dharma"], "desc": "Mage pemikat pengendalikan arah jalan musuh."}
    ],
    "Farm": [
        {"name": "Lady Sun", "tier": "S", "wr": "54.8%", "pr": "38.5%", "br": "25.0%", "counters": ["Low Mobility Tanks", "Arthur"], "synergies": ["Yaria", "Dharma", "Yao"], "desc": "MM S-Tier burst rolled-attack penghancur armor."},
        {"name": "Ao'yin (Loong)", "tier": "S", "wr": "55.2%", "pr": "31.0%", "br": "58.0%", "counters": ["Dive Assassins", "Lam", "Nezha"], "synergies": ["Yaria", "Dolia", "Zhang Fei"], "desc": "MM naga elemen ulti terbang untargetable."},
        {"name": "Arli", "tier": "S", "wr": "54.2%", "pr": "24.1%", "br": "41.0%", "counters": ["Skillshot Mages", "Angela", "Xiao Qiao"], "synergies": ["Mozi", "Xiao Qiao", "Da Qiao"], "desc": "MM 3-dash parasut lincah penepis proyektil."},
        {"name": "Flowborn (MM)", "tier": "S", "wr": "53.9%", "pr": "20.5%", "br": "22.1%", "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce", "Heino"], "desc": "MM fleksibel 5-stack double cast skill."},
        {"name": "Luara", "tier": "A", "wr": "52.1%", "pr": "18.2%", "br": "11.0%", "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun", "Mozi"], "desc": "MM baru pemanjat dinding pantulan panah."},
        {"name": "Marco Polo", "tier": "A", "wr": "51.5%", "pr": "29.0%", "br": "14.2%", "counters": ["Heavy Armor Tanks", "Dun", "Kaizer"], "synergies": ["Dolia", "Zhang Fei", "Yaria"], "desc": "MM pistol ganda true damage & ulti mutar."},
        {"name": "Consort Yu", "tier": "A", "wr": "51.0%", "pr": "19.5%", "br": "8.0%", "counters": ["Physical Assassins", "Wukong", "Lam"], "synergies": ["Zhang Fei", "Biron"], "desc": "MM imun serangan fisik & sniper jarak jauh."},
        {"name": "Luban No.7", "tier": "B", "wr": "50.2%", "pr": "32.0%", "br": "5.1%", "counters": ["High HP Tanks", "Dun"], "synergies": ["Zhang Fei", "Cai Yan"], "desc": "MM tembakan roket max HP % damage."},
        {"name": "Shouyue", "tier": "A", "wr": "51.8%", "pr": "21.0%", "br": "18.5%", "counters": ["Vision Comps"], "synergies": ["Mozi", "Nuwa"], "desc": "MM sniper jarak ekstra jauh & trap visi."},
        {"name": "Alessio", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "6.2%", "counters": ["Clustered Tanks"], "synergies": ["Yaria", "Dolia"], "desc": "MM meriam terbang dengan stealth asap."},
        {"name": "Di Renjie", "tier": "A", "wr": "52.0%", "pr": "22.0%", "br": "5.0%", "counters": ["CC Heavy Comps"], "synergies": ["Zhang Fei"], "desc": "MM pasif attack speed & kartus purifier."},
        {"name": "Hou Yi", "tier": "B", "wr": "50.1%", "pr": "28.0%", "br": "3.0%", "counters": ["Immobile Comps"], "synergies": ["Cai Yan", "Zhang Fei"], "desc": "MM panah matahari stunned ulti global."},
        {"name": "Fang", "tier": "A", "wr": "51.4%", "pr": "12.0%", "br": "2.5%", "counters": ["Early Turrets"], "synergies": ["Dun"], "desc": "MM bom peledak turret & dash stealth."},
        {"name": "Huang Zhong", "tier": "B", "wr": "50.4%", "pr": "14.0%", "br": "4.0%", "counters": ["Siege Defense"], "synergies": ["Zhang Fei", "Lian Po"], "desc": "MM meriam artileri stasioner armor tebal."},
        {"name": "Meng Ya", "tier": "A", "wr": "51.6%", "pr": "16.0%", "br": "3.2%", "counters": ["Extended Fights"], "synergies": ["Sun Bin"], "desc": "MM senapan mesin peluru bertubi-tubi."},
        {"name": "Garon", "tier": "B", "wr": "49.8%", "pr": "10.0%", "br": "1.0%", "counters": ["Shield Tanks"], "synergies": ["Yaria"], "desc": "MM pemotong shield pasif pemicu burst."},
        {"name": "Erin", "tier": "A", "wr": "51.3%", "pr": "13.0%", "br": "5.0%", "counters": ["Physical Defenses"], "synergies": ["Yaria"], "desc": "MM magic damage peri terbang lincah."},
        {"name": "Cheng Gong", "tier": "B", "wr": "49.2%", "pr": "6.0%", "br": "1.0%", "counters": ["Chokepoints"], "synergies": ["Dun"], "desc": "MM jebakan pasir penahan gerakan."},
        {"name": "Penglai", "tier": "B", "wr": "49.0%", "pr": "5.0%", "br": "1.0%", "counters": ["Melee Fighters"], "synergies": ["Zhang Fei"], "desc": "MM pedang terbang ganda."},
        {"name": "Baili Shouyue", "tier": "A", "wr": "51.5%", "pr": "19.0%", "br": "15.0%", "counters": ["Low HP Carries"], "synergies": ["Mozi"], "desc": "MM sniper jarak jauh pengaman visi."},
        {"name": "Sima Yi (MM)", "tier": "B", "wr": "48.5%", "pr": "2.0%", "br": "1.0%", "counters": ["Squishy Mages"], "synergies": ["Dolia"], "desc": "Off-meta MM magic assassin."}
    ],
    "Roam": [
        {"name": "Zhang Fei", "tier": "S", "wr": "55.1%", "pr": "42.0%", "br": "21.0%", "counters": ["Heavy Dive Comps", "Nezha", "Lam"], "synergies": ["Lady Sun", "Angela", "Augran"], "desc": "Roamer T0 pelindung carry ulti monster & shield."},
        {"name": "Yaria", "tier": "S", "wr": "54.6%", "pr": "36.2%", "br": "45.0%", "counters": ["Single Target Burst", "Prince of Lanling"], "synergies": ["Lady Sun", "Lam", "Ao'yin (Loong)"], "desc": "Support penempel carry +15% gold & shield CC."},
        {"name": "Dolia", "tier": "S", "wr": "54.9%", "pr": "31.5%", "br": "52.0%", "counters": ["Short Cooldown Comps"], "synergies": ["Heino", "Marco Polo", "Yixing"], "desc": "Support duyung pemutar waktu reset cooldown ulti."},
        {"name": "Devara", "tier": "A", "wr": "52.3%", "pr": "18.0%", "br": "14.1%", "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"], "desc": "Roamer pilar penjepit lokasi war."},
        {"name": "Mozi", "tier": "S", "wr": "53.8%", "pr": "28.4%", "br": "22.0%", "counters": ["Immobile Carries", "Luban No.7"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Support meriam stun jarak jauh."},
        {"name": "Dun", "tier": "A", "wr": "51.9%", "pr": "20.1%", "br": "3.5%", "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "desc": "Roamer tank tahan banting hook & knock-up."},
        {"name": "Da Qiao", "tier": "S", "wr": "54.0%", "pr": "25.0%", "br": "48.0%", "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli", "Luna"], "desc": "Support kolam recall instan & summon ulti global."},
        {"name": "Cai Yan", "tier": "A", "wr": "52.2%", "pr": "30.0%", "br": "12.0%", "counters": ["Poke Comps"], "synergies": ["Hou Yi", "Luban No.7"], "desc": "Support hembusan musik heal HP bertubi-tubi."},
        {"name": "Yao", "tier": "A", "wr": "51.8%", "pr": "22.0%", "br": "18.0%", "counters": ["Immobile Squishies"], "synergies": ["Dharma", "Lady Sun"], "desc": "Support penambah MS & shield penumpas CC."},
        {"name": "Kui (Roam)", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "12.0%", "counters": ["No-dash Carries"], "synergies": ["Li Bai"], "desc": "Roamer hook penarik musuh ke turret."},
        {"name": "Zhuangzi", "tier": "A", "wr": "51.5%", "pr": "24.0%", "br": "15.0%", "counters": ["CC Heavy Comps", "Yixing", "Wang Zhaojun"], "synergies": ["Marco Polo"], "desc": "Roamer ikan pembebas efek CC area untuk tim."},
        {"name": "Sun Bin", "tier": "A", "wr": "51.7%", "pr": "19.0%", "br": "5.0%", "counters": ["Burst Damage Comps"], "synergies": ["Meng Ya", "Biron"], "desc": "Support pengembali HP & boost movement speed."},
        {"name": "Donghuang", "tier": "S", "wr": "53.5%", "pr": "18.0%", "br": "54.0%", "counters": ["Mobile Assassins", "Arli", "Jing", "Luna"], "synergies": ["Lady Sun"], "desc": "Roamer naga suppress CC kuncian mati."},
        {"name": "Liang", "tier": "A", "wr": "52.1%", "pr": "14.0%", "br": "32.0%", "counters": ["High Mobility Divers", "Lam"], "synergies": ["Augran"], "desc": "Support/Mid kuncian matos suppress CC tunggal."},
        {"name": "Liu Shan", "tier": "A", "wr": "51.0%", "pr": "16.0%", "br": "2.0%", "counters": ["Early Turrets"], "synergies": ["Fang"], "desc": "Roamer robot stun turret & pusher instan."},
        {"name": "Ming", "tier": "B", "wr": "50.2%", "pr": "12.0%", "br": "4.0%", "counters": ["Single Target Scaling"], "synergies": ["Lady Sun", "Hou Yi"], "desc": "Support tali penambah attack damage & HP buffer."},
        {"name": "Guiguzi", "tier": "A", "wr": "52.3%", "pr": "10.0%", "br": "8.0%", "counters": ["Immobile Backlines"], "synergies": ["Guan Yu", "Angela"], "desc": "Roamer stealth kelompok penculik area rapet."},
        {"name": "Agudo", "tier": "B", "wr": "49.8%", "pr": "5.0%", "br": "1.0%", "counters": ["Slow Clear"], "synergies": ["Meng Ya"], "desc": "Support/Jungle pemanggil monster beruang."},
        {"name": "Dunshan", "tier": "S", "wr": "53.2%", "pr": "12.0%", "br": "40.0%", "counters": ["Projectiles", "Xiao Qiao", "Lady Sun"], "synergies": ["Wang Zhaojun"], "desc": "Roamer tameng penepis proyektil & nempel turret S16."},
        {"name": "Su Lie", "tier": "A", "wr": "51.6%", "pr": "8.0%", "br": "2.0%", "counters": ["Clustered Comps"], "synergies": ["Dharma"], "desc": "Tank tiang pasif hidup kembali & slam Area."},
        {"name": "Yaria (Roam)", "tier": "S", "wr": "54.6%", "pr": "36.2%", "br": "45.0%", "counters": ["Single Target Burst"], "synergies": ["Lady Sun"], "desc": "Support penempel carry S-Tier."},
        {"name": "Niu Mo", "tier": "A", "wr": "51.9%", "pr": "11.0%", "br": "3.0%", "counters": ["Physical Burst"], "synergies": ["Lady Sun"], "desc": "Roamer banteng penambah defense pasif."}
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
st.markdown("<div class='main-title'>⚔️ HOK PRO REAL-TIME DRAFT ENGINE</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Database: {len(ALL_HEROES_LIST)} Heroes • 4 Bans Per Side • Instant Counter Radar • By Siropkokop</div>", unsafe_allow_html=True)

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
# REAL-TIME STRICT FILTERING & DRAFT INPUT
# ==========================================

col_draft_left, col_draft_right = st.columns([5, 5])

with col_draft_left:
    st.subheader("🛡️ 1. Fase Banning (4 Bans Per Side)")
    
    col_b1, col_b2 = st.columns(2)
    
    # Helper to get valid ban options
    def get_ban_options(already_selected_bans):
        used = set(st.session_state['used_heroes'])
        selected = set(already_selected_bans)
        return ["None"] + sorted([h["name"] for h in ALL_HEROES_LIST if h["name"] not in used and h["name"] not in selected])

    with col_b1:
        st.markdown("**🔵 BANS TIM KITA (OUR BANS)**")
        ob1_val = st.session_state.get("ob1", "None")
        ob2_val = st.session_state.get("ob2", "None")
        ob3_val = st.session_state.get("ob3", "None")
        ob4_val = st.session_state.get("ob4", "None")

        our_b1 = st.selectbox("Our Ban 1", get_ban_options([ob2_val, ob3_val, ob4_val]), key="ob1")
        our_b2 = st.selectbox("Our Ban 2", get_ban_options([our_b1, ob3_val, ob4_val]), key="ob2")
        our_b3 = st.selectbox("Our Ban 3", get_ban_options([our_b1, our_b2, ob4_val]), key="ob3")
        our_b4 = st.selectbox("Our Ban 4", get_ban_options([our_b1, our_b2, our_b3]), key="ob4")

    our_bans_active = [b for b in [our_b1, our_b2, our_b3, our_b4] if b != "None"]

    with col_b2:
        st.markdown("**🔴 BANS TIM MUSUH (ENEMY BANS)**")
        eb1_val = st.session_state.get("eb1", "None")
        eb2_val = st.session_state.get("eb2", "None")
        eb3_val = st.session_state.get("eb3", "None")
        eb4_val = st.session_state.get("eb4", "None")

        enemy_b1 = st.selectbox("Enemy Ban 1", get_ban_options(our_bans_active + [eb2_val, eb3_val, eb4_val]), key="eb1")
        enemy_b2 = st.selectbox("Enemy Ban 2", get_ban_options(our_bans_active + [enemy_b1, eb3_val, eb4_val]), key="eb2")
        enemy_b3 = st.selectbox("Enemy Ban 3", get_ban_options(our_bans_active + [enemy_b1, enemy_b2, eb4_val]), key="eb3")
        enemy_b4 = st.selectbox("Enemy Ban 4", get_ban_options(our_bans_active + [enemy_b1, enemy_b2, enemy_b3]), key="eb4")

    enemy_bans_active = [b for b in [enemy_b1, enemy_b2, enemy_b3, enemy_b4] if b != "None"]
    all_bans = set(our_bans_active + enemy_bans_active)

    st.markdown("---")
    st.subheader("⚔️ 2. Fase Picking (Real-Time Picks per Role)")
    
    # Collect currently selected picks across all fields to enforce STRICT EXCLUSION
    curr_op_clash = st.session_state.get("op_clash", "None")
    curr_op_jungle = st.session_state.get("op_jungle", "None")
    curr_op_mid = st.session_state.get("op_mid", "None")
    curr_op_farm = st.session_state.get("op_farm", "None")
    curr_op_roam = st.session_state.get("op_roam", "None")

    curr_ep_clash = st.session_state.get("ep_clash", "None")
    curr_ep_jungle = st.session_state.get("ep_jungle", "None")
    curr_ep_mid = st.session_state.get("ep_mid", "None")
    curr_ep_farm = st.session_state.get("ep_farm", "None")
    curr_ep_roam = st.session_state.get("ep_roam", "None")

    all_current_picks = set([
        curr_op_clash, curr_op_jungle, curr_op_mid, curr_op_farm, curr_op_roam,
        curr_ep_clash, curr_ep_jungle, curr_ep_mid, curr_ep_farm, curr_ep_roam
    ]) - {"None"}

    def get_strict_pick_options(role_name, current_field_val):
        used = set(st.session_state['used_heroes'])
        # Exclude all bans, all used heroes, and all picked heroes EXCEPT the current field's own selected value
        other_picks = all_current_picks - ({current_field_val} if current_field_val != "None" else set())
        forbidden = all_bans | used | other_picks
        
        valid_heroes = [h["name"] for h in HERO_DB[role_name] if h["name"] not in forbidden]
        return ["None"] + sorted(valid_heroes)

    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("**💙 PICKS TIM KITA**")
        our_clash = st.selectbox("Clash Lane", get_strict_pick_options("Clash", curr_op_clash), key="op_clash")
        our_jungle = st.selectbox("Jungle", get_strict_pick_options("Jungle", curr_op_jungle), key="op_jungle")
        our_mid = st.selectbox("Mid Lane", get_strict_pick_options("Mid", curr_op_mid), key="op_mid")
        our_farm = st.selectbox("Farm Lane (MM)", get_strict_pick_options("Farm", curr_op_farm), key="op_farm")
        our_roam = st.selectbox("Roam / Support", get_strict_pick_options("Roam", curr_op_roam), key="op_roam")

    with col_p2:
        st.markdown("**❤️ PICKS TIM MUSUH**")
        enemy_clash = st.selectbox("Enemy Clash", get_strict_pick_options("Clash", curr_ep_clash), key="ep_clash")
        enemy_jungle = st.selectbox("Enemy Jungle", get_strict_pick_options("Jungle", curr_ep_jungle), key="ep_jungle")
        enemy_mid = st.selectbox("Enemy Mid", get_strict_pick_options("Mid", curr_ep_mid), key="ep_mid")
        enemy_farm = st.selectbox("Enemy Farm", get_strict_pick_options("Farm", curr_ep_farm), key="ep_farm")
        enemy_roam = st.selectbox("Enemy Roam", get_strict_pick_options("Roam", curr_ep_roam), key="ep_roam")

    our_picks = [p for p in [our_clash, our_jungle, our_mid, our_farm, our_roam] if p != "None"]
    enemy_picks = [p for p in [enemy_clash, enemy_jungle, enemy_mid, enemy_farm, enemy_roam] if p != "None"]

    if st.button("🔒 Lock Current Picks to Fearless Memory"):
        for p in our_picks:
            if p not in st.session_state['used_heroes']:
                st.session_state['used_heroes'].append(p)
        st.success("Hero terpakai berhasil disimpan ke memori Fearless!")
        st.rerun()

# ==========================================
# REAL-TIME INSTANT CALCULATOR & DASHBOARD
# ==========================================
with col_draft_right:
    st.subheader("📊 3. Real-Time Dashboard & Counter Radar")

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
            
            # Red side bias bonus
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

    # Synergy calculation
    if "Dolia" in our_picks and "Heino" in our_picks:
        base_score += 5.0
    if "Mozi" in our_picks and ("Xiao Qiao" in our_picks or "Arli" in our_picks):
        base_score += 4.0
    if "Yaria" in our_picks and ("Lady Sun" in our_picks or "Ao'yin (Loong)" in our_picks or "Lam" in our_picks):
        base_score += 4.0
    if "Zhang Fei" in our_picks and ("Lady Sun" in our_picks or "Angela" in our_picks):
        base_score += 3.0

    our_win_rate = min(max(round(base_score, 1), 20.0), 85.0)
    enemy_win_rate = round(100.0 - our_win_rate, 1)

    # 1. Real-Time Gauge Display
    st.markdown(f"#### 📈 Estimated Win Probability: **{our_win_rate}%** (Kita) vs **{enemy_win_rate}%** (Musuh)")
    st.progress(int(our_win_rate))

    # 2. REAL-TIME ENEMY COUNTER-PICK RADAR
    st.markdown("#### 🎯 REAL-TIME ENEMY COUNTER-PICK RADAR")
    
    if not enemy_picks:
        st.info("💡 Pilih hero musuh di sebelah kiri untuk melihat rekomendasi counter-pick instan secara real-time!")
    else:
        for ep in enemy_picks:
            eh_info = next((item for item in ALL_HEROES_LIST if item["name"] == ep), None)
            if eh_info:
                # Find available counters for this specific enemy hero
                suggested_counters = []
                for candidate in ALL_HEROES_LIST:
                    c_name = candidate["name"]
                    # Candidate must not be banned, used, or picked
                    if c_name not in all_bans and c_name not in st.session_state['used_heroes'] and c_name not in all_current_picks:
                        # Check if candidate lists ep in its counters or candidate matches role counter logic
                        if ep in candidate.get("counters", []) or any(term.lower() in ep.lower() for term in candidate.get("counters", [])):
                            suggested_counters.append(f"<b>{c_name}</b> ({candidate['role']} - {candidate['tier']} Tier)")
                
                counter_text = ", ".join(suggested_counters[:3]) if suggested_counters else "Biron, Zhang Fei, Charlotte (Sustain/Shield)"
                st.markdown(f"""
                <div class='counter-card'>
                    🎯 <b>Target Enemy Picked:</b> <span style='color:#FFD700;'><b>{ep}</b></span> ({eh_info['role']} - {eh_info['tier']} Tier)<br>
                    🛡️ <b>Recommended Counter Picks:</b> {counter_text}<br>
                    💡 <i>Taktik Counter:</i> Utamakan CC/Peel atau pancing war saat skill cooldown musuh habis.
                </div>
                """, unsafe_allow_html=True)

    # 3. Synergy Alerts
    st.markdown("#### 💡 Active Synergy & Threat Highlights")
    if "Nezha" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT:</b> Musuh pick <b>Nezha</b> (Global Lock)! Wajib siapkan Zhang Fei / Biron buat shield/peel Mid & MM.</div>", unsafe_allow_html=True)
    if "Lam" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT:</b> Musuh pick <b>Lam</b> (True Damage Execution)! Utamakan Wang Zhaojun / Donghuang / Liang buat kuncian CC.</div>", unsafe_allow_html=True)
    if "Dolia" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT:</b> Musuh pick <b>Dolia</b>! Wajib BAN / Pick Heino & Marco Polo biar musuh ga dapet Celestial Reset.</div>", unsafe_allow_html=True)

    if "Dolia" in our_picks and "Heino" in our_picks:
        st.markdown("<div class='alert-success'>✨ <b>ACTIVE SYNERGY:</b> Combo <b>Dolia + Heino</b> Aktif! (Celestial Reset Tower & Unlimited HP).</div>", unsafe_allow_html=True)
    if "Mozi" in our_picks and ("Xiao Qiao" in our_picks or "Arli" in our_picks):
        st.markdown("<div class='alert-success'>✨ <b>ACTIVE SYNERGY:</b> Combo <b>Mozi + Xiao Qiao / Arli</b> Aktif! (Unli Stun Lock & Poke Burst).</div>", unsafe_allow_html=True)
    if "Yaria" in our_picks and ("Lady Sun" in our_picks or "Ao'yin (Loong)" in our_picks):
        st.markdown("<div class='alert-success'>✨ <b>ACTIVE SYNERGY:</b> Combo <b>Yaria + Carry</b> Aktif! (+15% Gold Boost & Anti-CC Shield).</div>", unsafe_allow_html=True)

    # 4. Dynamic In-Game Scheme
    st.markdown("#### ⚔️ Dynamic In-Game Strategy & Timers")
    st.write("• **Early Game (0:00 - 4:00):** Roamer bantu Mid clear wave 1. Amankan Space Sprite (Menit 1:00) & Power Spike Level 4 (Menit 1:20-2:00).")
    st.write("• **Mid Game (4:00 - 10:00):** Pelat turret hancur. Utamakan **Tyrant** > Overlord. Terapkan 2-Player Wave Sharing (160% Gold). Awas debuff Primal Bond (-50% damage naga)!")
    st.write("• **Late Game (10:00 - 20:00+):** Protect Carry (Lady Sun / Loong). **Dilarang bunuh naga biasa di menit 18:30-19:00** agar tidak debuff pas Tempest Dragon muncul di menit 20:00!")

st.markdown("---")

# ==========================================
# EXPORT & MATCH HISTORY LOG TABS
# ==========================================
tab_export, tab_history, tab_database = st.tabs(["📲 Export to WhatsApp", "📊 Recent Match Analysis", "📚 Complete 116 Hero Database S16"])

with tab_export:
    st.subheader("📋 WhatsApp Copy-Paste Summary")
    
    wa_text = f"""*BLUEPRINT DRAFT HOK* 🎮🔥
*Title:* {draft_title}
*Series:* {match_series} | *Side:* {our_side}
*Win Probability Engine:* {our_win_rate}% (Kita) vs {enemy_win_rate}% (Musuh)

🚫 *BANS:*
• *Our Bans:* {', '.join(our_bans_active) or 'None'}
• *Enemy Bans:* {', '.join(enemy_bans_active) or 'None'}

🛡️ *OUR PICKS:*
• *Clash:* {our_clash} | *Jungle:* {our_jungle} | *Mid:* {our_mid} | *Farm:* {our_farm} | *Roam:* {our_roam}

🔴 *ENEMY PICKS:*
• *Clash:* {enemy_clash} | *Jungle:* {enemy_jungle} | *Mid:* {enemy_mid} | *Farm:* {enemy_farm} | *Roam:* {enemy_roam}

⚡ *KEY GAME PLAN:*
• Early Prio Mid & Space Sprite (Min 1:00)
• Tyrant First Priority (Min 4:00)
• Beware Primal Bond Debuff on Double Dragon!

*Gaspol, Bantai Semuanya! Let's Go!* 🚀🔥"""

    st.code(wa_text, language="markdown")
    st.info("💡 Klik ikon 'Copy' di pojok kanan atas kotak di atas, lalu paste ke WhatsApp tim!")

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
    st.subheader("📚 Complete 116 Hero Database & Stats (Season 16)")
    
    role_filter = st.radio("Filter Role:", ["All", "Clash", "Jungle", "Mid", "Farm", "Roam"], horizontal=True)
    search_query = st.text_input("🔍 Cari Nama Hero / Spesialisasi Skill:", "")
    
    filtered_db = []
    for r, h_list in HERO_DB.items():
        if role_filter == "All" or role_filter == r:
            for h in h_list:
                if not search_query or search_query.lower() in h["name"].lower() or search_query.lower() in h["desc"].lower():
                    item = h.copy()
                    item["Role"] = r
                    filtered_db.append(item)
                
    if filtered_db:
        df_db = pd.DataFrame(filtered_db)[["name", "Role", "tier", "wr", "pr", "br", "desc"]]
        df_db.columns = ["Hero Name", "Role", "Tier", "Win Rate", "Pick Rate", "Ban Rate", "Specialization / Description"]
        st.dataframe(df_db, use_container_width=True)
    else:
        st.warning("Hero tidak ditemukan.")

# Footer Credit
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>HOK Draft & Strategy Engine S16 • Built for Esports Analytics • Credit: <b>By Siropkokop</b></div>", unsafe_allow_html=True)
