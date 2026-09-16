import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="HOK Pro Draft & Strategy Engine (116 Heroes) | By Siropkokop",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Esports Dark Theme & Compact Ergonomic UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.0rem;
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
    .alert-danger { background-color: #421212; border: 1px solid #E74C3C; color: #FF9999; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
    .alert-success { background-color: #123318; border: 1px solid #2ECC71; color: #99FFBB; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# COMPLETE 116 HEROES DATABASE (SEASON 16)
# ==========================================
HERO_DB = {
    "Clash": [
        {"name": "Biron", "tier": "S", "wr": "54.2%", "pr": "28.5%", "br": "15.2%", "counters": ["Physical Fighters"], "synergies": ["Zhang Fei", "Dun", "Angela"], "desc": "Frontline shield & sustain badak."},
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
        {"name": "Wang Wei", "tier": "S", "wr": "54.0%", "pr": "16.0%", "br": "20.1%", "counters": ["Vision Dependent"], "synergies": ["Biron", "Devara"], "desc": "Mage baru kabut kegelapan penutup visi S16."},
        {"name": "Milady", "tier": "A", "wr": "51.8%", "pr": "24.0%", "br": "12.0%", "counters": ["Slow Clear Mages"], "synergies": ["Liu Bei"], "desc": "Mage mekanik robot penghancur turret kilat."},
        {"name": "Zhou Yu", "tier": "A", "wr": "51.5%", "pr": "15.0%", "br": "6.0%", "counters": ["Immobile Formations"], "synergies": ["Dun"], "desc": "Mage api penyebar area & push turret."},
        {"name": "Gan & Mo", "tier": "A", "wr": "52.1%", "pr": "13.0%", "br": "18.0%", "counters": ["Squishy Carries"], "synergies": ["Mozi"], "desc": "Mage pedang kembar sniper 1-hit KO."},
        {"name": "Mozi (Mid)", "tier": "A", "wr": "51.9%", "pr": "12.0%", "br": "5.0%", "counters": ["Long-range Poke"], "synergies": ["Xiao Qiao"], "desc": "Mage meriam stun jarak jauh."},
        {"name": "Princess Frost", "tier": "A", "wr": "51.2%", "pr": "10.0%", "br": "4.0%", "counters": ["Melee Diver"], "synergies": ["Lady Sun"], "desc": "Mage pemicu es kontrol area."},
        {"name": "Zhong Kui", "tier": "B", "wr": "49.8%", "pr": "11.2%", "br": "8.0%", "counters": ["Buff Dependent"], "synergies": ["Li Bai"], "desc": "Mage tarik penarik buff/hero."},
        {"name": "Dr Bian", "tier": "A", "wr": "52.3%", "pr": "14.1%", "br": "7.2%", "counters": ["Attrition Tank Comps"], "synergies": ["Biron", "Cai Yan"], "desc": "Mage racun & heal stack berkelanjutan."},
        {"name": "Gao Chong", "tier": "B", "wr": "49.2%", "pr": "5.1%", "br": "1.0%", "counters": ["Melee Comps"], "synergies": ["Zhang Fei"], "desc": "Mage gitaris AoE burst panggung."},
        {"name": "Sima Yi (Mid)", "tier": "A", "wr": "51.4%", "pr": "9.0%", "br": "11.0%", "counters": ["Squishy Mages"], "synergies": ["Lam"], "desc": "Mage bayangan silence pembantai mid."},
        {"name": "Zhen Ji", "tier": "A", "wr": "51.7%", "pr": "26.0%", "br": "8.0%", "counters": ["Clustered Enemies"], "synergies": ["Zhang Fei"], "desc": "Mage pantulan air es pemicu freeze."},
        {"name": "Yang Yuhuan", "tier": "A", "wr": "52.0%", "pr": "10.2%", "br": "5.0%", "counters": ["Poke Comps"], "synergies": ["Pei"], "desc": "Mage kecapi switcher heal & damage."},
        {"name": "Lady Zhen", "tier": "B", "wr": "49.9%", "pr": "12.0%", "br": "2.0%", "counters": ["Non-dash Enemies"], "synergies": ["Dun"], "desc": "Mage air ombak cc melimpah."}
    ],
    "Farm": [
        {"name": "Lady Sun", "tier": "S", "wr": "54.8%", "pr": "38.5%", "br": "25.0%", "counters": ["Low Mobility Tanks"], "synergies": ["Yaria", "Dharma", "Yao"], "desc": "MM S-Tier burst rolled-attack penembus armor."},
        {"name": "Ao'yin (Loong)", "tier": "S", "wr": "55.2%", "pr": "31.0%", "br": "58.0%", "counters": ["Dive Assassins"], "synergies": ["Yaria", "Dolia", "Zhang Fei"], "desc": "MM naga elemen ulti wujud terbang untargetable."},
        {"name": "Arli", "tier": "S", "wr": "54.2%", "pr": "24.1%", "br": "41.0%", "counters": ["Skillshot Mages"], "synergies": ["Mozi", "Xiao Qiao", "Da Qiao"], "desc": "MM 3-dash parasut penepis proyektil."},
        {"name": "Flowborn (MM)", "tier": "S", "wr": "53.9%", "pr": "20.5%", "br": "22.1%", "counters": ["Frontline Tanks"], "synergies": ["Dolia", "Sun Ce", "Heino"], "desc": "MM 5-stack double cast skill barrage."},
        {"name": "Luara", "tier": "A", "wr": "52.1%", "pr": "18.2%", "br": "11.0%", "counters": ["Terrain Chokepoints"], "synergies": ["Biron", "Dun", "Mozi"], "desc": "MM pemanjat dinding pantulan panah S16."},
        {"name": "Marco Polo", "tier": "A", "wr": "51.5%", "pr": "29.0%", "br": "14.2%", "counters": ["Heavy Armor Tanks"], "synergies": ["Dolia", "Zhang Fei", "Yaria"], "desc": "MM pistol ganda true damage & ulti mutar."},
        {"name": "Consort Yu", "tier": "A", "wr": "51.0%", "pr": "19.5%", "br": "8.0%", "counters": ["Physical Assassins"], "synergies": ["Zhang Fei", "Biron"], "desc": "MM imun fisik & sniper jarak jauh."},
        {"name": "Shouyue", "tier": "A", "wr": "51.8%", "pr": "21.0%", "br": "18.5%", "counters": ["Vision Dependent"], "synergies": ["Mozi", "Nuwa"], "desc": "MM sniper ekstra jauh & trap visi semak."},
        {"name": "Luban No.7", "tier": "B", "wr": "50.2%", "pr": "32.0%", "br": "5.1%", "counters": ["High HP Tanks"], "synergies": ["Zhang Fei", "Cai Yan"], "desc": "MM roket max HP % damage tanpa ampuni."},
        {"name": "Alessio", "tier": "A", "wr": "51.2%", "pr": "15.0%", "br": "6.2%", "counters": ["Clustered Tanks"], "synergies": ["Yaria", "Dolia"], "desc": "MM meriam terbang & stealth asap."},
        {"name": "Meng Ya", "tier": "A", "wr": "51.6%", "pr": "17.0%", "br": "4.0%", "counters": ["Low Mobility Comps"], "synergies": ["Zhang Fei"], "desc": "MM peluru terus menerus & bombardir ulti."},
        {"name": "Fang", "tier": "A", "wr": "51.4%", "pr": "14.2%", "br": "3.1%", "counters": ["Towers & Objectives"], "synergies": ["Dun"], "desc": "MM bom waktu peledak turret & naga."},
        {"name": "Hou Yi", "tier": "B", "wr": "50.4%", "pr": "28.0%", "br": "4.0%", "counters": ["No-CC Frontlines"], "synergies": ["Zhang Fei", "Ming"], "desc": "MM panah matahari attack speed gila."},
        {"name": "Huang Zhong", "tier": "A", "wr": "51.9%", "pr": "13.5%", "br": "7.5%", "counters": ["Siege & Defend"], "synergies": ["Zhang Fei", "Wang Zhaojun"], "desc": "MM meriam tancap kincir pertahanan."},
        {"name": "Gara", "tier": "B", "wr": "49.5%", "pr": "11.0%", "br": "2.0%", "counters": ["Melee Fighters"], "synergies": ["Cai Yan"], "desc": "MM jebakan pasir penahan gerakan."},
        {"name": "Kahn", "tier": "B", "wr": "49.2%", "pr": "8.0%", "br": "1.0%", "counters": ["Short Range MM"], "synergies": ["Yaria"], "desc": "MM kebal serangan kejutan."},
        {"name": "Eir", "tier": "B", "wr": "49.0%", "pr": "6.0%", "br": "1.0%", "counters": ["Shield Tanks"], "synergies": ["Dolia"], "desc": "MM energi penembus benteng es."},
        {"name": "Baili Shouyue (Farm)", "tier": "A", "wr": "51.5%", "pr": "18.0%", "br": "15.0%", "counters": ["Long Range Poke"], "synergies": ["Mozi"], "desc": "Sniper vision provider."},
        {"name": "Di Renjie", "tier": "A", "wr": "52.0%", "pr": "22.0%", "br": "5.0%", "counters": ["CC Heavy Comps"], "synergies": ["Zhang Fei"], "desc": "MM kartu pasif cleanse & yellow card stun."},
        {"name": "Solaris", "tier": "B", "wr": "49.8%", "pr": "7.2%", "br": "1.1%", "counters": ["Melee Dive"], "synergies": ["Yaria"], "desc": "MM cahaya penembus armor."},
        {"name": "Erin", "tier": "A", "wr": "51.3%", "pr": "14.0%", "br": "3.5%", "counters": ["Physical Armor Tanks"], "synergies": ["Yaria", "Dun"], "desc": "MM magic damage tarian peri lincah."}
    ],
    "Roam": [
        {"name": "Zhang Fei", "tier": "S", "wr": "55.1%", "pr": "42.0%", "br": "21.0%", "counters": ["Heavy Dive Comps"], "synergies": ["Lady Sun", "Angela", "Augran"], "desc": "Roamer T0 raungan ulti monster & shield tebal."},
        {"name": "Yaria", "tier": "S", "wr": "54.6%", "pr": "36.2%", "br": "45.0%", "counters": ["Single Target Burst"], "synergies": ["Lady Sun", "Lam", "Ao'yin (Loong)"], "desc": "Support penempel carry +15% gold & shield CC."},
        {"name": "Dolia", "tier": "S", "wr": "54.9%", "pr": "31.5%", "br": "52.0%", "counters": ["Short Cooldowns"], "synergies": ["Heino", "Marco Polo", "Yixing"], "desc": "Support duyung reset cooldown ultimate tim."},
        {"name": "Devara", "tier": "A", "wr": "52.3%", "pr": "18.0%", "br": "14.1%", "counters": ["Flanking Assassins"], "synergies": ["Fatih", "Dharma", "Feyd"], "desc": "Roamer arena kuncian lokasi war."},
        {"name": "Mozi", "tier": "S", "wr": "53.8%", "pr": "28.4%", "br": "22.0%", "counters": ["Immobile Carries"], "synergies": ["Xiao Qiao", "Arli", "Xuance"], "desc": "Support meriam stun jarak jauh."},
        {"name": "Dun", "tier": "A", "wr": "51.9%", "pr": "20.1%", "br": "3.5%", "counters": ["Melee Inisiators"], "synergies": ["Biron", "Xiao Qiao", "Xuance"], "desc": "Roamer tank hook & knock-up."},
        {"name": "Da Qiao", "tier": "S", "wr": "54.0%", "pr": "21.0%", "br": "48.0%", "counters": ["Slow Rotations"], "synergies": ["Sun Ce", "Arli", "Han Xin"], "desc": "Support portal teleportasi base & panggilan tim."},
        {"name": "Dunshan", "tier": "S", "wr": "53.7%", "pr": "15.0%", "br": "32.0%", "counters": ["Projectile MM/Mages"], "synergies": ["Lady Sun", "Wang Zhaojun"], "desc": "Roamer perisai pemblokir proyektil & nempel tower S16."},
        {"name": "Cai Yan", "tier": "A", "wr": "52.1%", "pr": "25.0%", "br": "18.0%", "counters": ["Attrition Damage"], "synergies": ["Luban No.7", "Hou Yi"], "desc": "Support mobil heal melimpah & bounce stun."},
        {"name": "Ming", "tier": "A", "wr": "51.8%", "pr": "18.0%", "br": "12.0%", "counters": ["Solo Carries"], "synergies": ["Hou Yi", "Arli"], "desc": "Support tali penambah attack/defense carry."},
        {"name": "Zhuangzi", "tier": "A", "wr": "52.2%", "pr": "22.0%", "br": "10.0%", "counters": ["CC Heavy Comps"], "synergies": ["Marco Polo"], "desc": "Support ikan pembebas efek CC seluruh tim."},
        {"name": "Yao", "tier": "A", "wr": "51.5%", "pr": "16.0%", "br": "8.0%", "counters": ["Squishy Inisiators"], "synergies": ["Dharma", "Lady Sun"], "desc": "Support penyerap damage & finisher CC."},
        {"name": "Sun Bin", "tier": "A", "wr": "52.0%", "pr": "19.0%", "br": "6.0%", "counters": ["Burst Damage Comps"], "synergies": ["Biron", "Pei"], "desc": "Support waktu pembalik HP & speed boost tim."},
        {"name": "Kui (Roam)", "tier": "A", "wr": "51.2%", "pr": "14.0%", "br": "12.0%", "counters": ["No-dash Carries"], "synergies": ["Li Bai"], "desc": "Roamer hook penculik."},
        {"name": "Guan Yu (Roam)", "tier": "B", "wr": "49.8%", "pr": "5.0%", "br": "8.0%", "counters": ["No CC"], "synergies": ["Da Qiao"], "desc": "Roamer kuda inisiator pendorong."},
        {"name": "Liu Bang", "tier": "A", "wr": "51.6%", "pr": "11.0%", "br": "4.0%", "counters": ["Single Target Focus"], "synergies": ["Lam", "Jing"], "desc": "Tank teleportasi shield langsung ke rekan tim."},
        {"name": "Nezha (Roam)", "tier": "B", "wr": "49.1%", "pr": "3.0%", "br": "2.0%", "counters": ["Healers"], "synergies": ["Pei"], "desc": "Roamer disrupsi anti-heal global."},
        {"name": "Agudo", "tier": "A", "wr": "51.4%", "pr": "8.0%", "br": "3.0%", "counters": ["Slow Clear Tanks"], "synergies": ["Meng Ya"], "desc": "Support panda pemanggil monster hutan."},
        {"name": "Donghuang", "tier": "S", "wr": "53.5%", "pr": "20.0%", "br": "55.0%", "counters": ["High Mobility Assassins"], "synergies": ["Lady Sun"], "desc": "Tank suppress kuncian mati tak bisa di-cleanse."},
        {"name": "Liang", "tier": "S", "wr": "53.2%", "pr": "17.0%", "br": "42.0%", "counters": ["Dash Assassins"], "synergies": ["Augran"], "desc": "Mage/Roam suppress kuncian mati tunggal."},
        {"name": "Su Lie", "tier": "A", "wr": "51.7%", "pr": "9.5%", "br": "2.0%", "counters": ["Clustered Enemies"], "synergies": ["Xiao Qiao"], "desc": "Tank nyawa dua pemicu knockup tiang raksasa."},
        {"name": "Xi Shi", "tier": "A", "wr": "52.0%", "pr": "12.0%", "br": "15.0%", "counters": ["Immobile Frontlines"], "synergies": ["Dharma"], "desc": "Mage/Roam pemikat pengendalikan arah jalan musuh."}
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
st.markdown(f"<div class='sub-title'>Database: {len(ALL_HEROES_LIST)} Heroes • 4 Bans Per Side • Instant Real-Time Calculations • By Siropkokop</div>", unsafe_allow_html=True)

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
# REAL-TIME FILTERING & DRAFT INPUT SECTION
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
    
    def get_pick_opts(role_name):
        return ["None"] + [h["name"] for h in HERO_DB[role_name] if h["name"] not in st.session_state['used_heroes'] and h["name"] not in all_bans]

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

    if st.button("🔒 Lock Current Picks to Fearless Memory"):
        for p in our_picks:
            if p not in st.session_state['used_heroes']:
                st.session_state['used_heroes'].append(p)
        st.success("Hero berhasil disimpan ke memori Fearless!")
        st.rerun()

# ==========================================
# REAL-TIME INSTANT CALCULATOR & TACTICAL DASHBOARD
# ==========================================
with col_draft_right:
    st.subheader("📊 3. Real-Time Instant Calculation & Scheme")

    # INSTANT CALCULATIONS (NO WAITING FOR ALL 5 PICKS)
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

    # Synergy & Counter calculation
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

    # 2. Instant Threat & Synergy Alerts
    st.markdown("#### 🚨 Real-Time Alerts & Synergy Highlights")
    
    danger_detected = False
    if "Nezha" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT ALERT:</b> Musuh pick <b>Nezha</b> (Lock-On Global)! Utamakan Cover/Peel untuk Mid/MM kita dengan Zhang Fei/Biron.</div>", unsafe_allow_html=True)
        danger_detected = True
    if "Dolia" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT ALERT:</b> Musuh pick <b>Dolia</b>! Waspada reset cooldown ultimate dua kali (Awas Heino/Marco Polo combo).</div>", unsafe_allow_html=True)
        danger_detected = True
    if "Mai Shiranui" in enemy_picks or "Shangguan" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT ALERT:</b> Musuh pick <b>Mage-Assassin Lincah</b>! Pasang vision semak sungai rapat-rapat.</div>", unsafe_allow_html=True)
        danger_detected = True
    if "Donghuang" in enemy_picks or "Liang" in enemy_picks:
        st.markdown("<div class='alert-danger'>⚠️ <b>ENEMY THREAT ALERT:</b> Musuh punya <b>Suppress CC Kuncian Mati</b>! Jangan dive solo tanpa backup.</div>", unsafe_allow_html=True)
        danger_detected = True

    if not danger_detected:
        st.markdown("<div class='alert-success'>✅ Belum terdeteksi ancaman combo spesifik musuh. Draf berjalan stabil.</div>", unsafe_allow_html=True)

    # Active Synergies
    if "Dolia" in our_picks and "Heino" in our_picks:
        st.markdown("<div class='alert-success'>🔥 <b>ACTIVE COMBO:</b> <i>Celestial Reset (Dolia + Heino)</i> Aktif! Reset HP & Tower area terjamin.</div>", unsafe_allow_html=True)
    if "Mozi" in our_picks and "Xiao Qiao" in our_picks:
        st.markdown("<div class='alert-success'>🔥 <b>ACTIVE COMBO:</b> <i>Unli CC Poke (Mozi + Xiao Qiao)</i> Aktif! Stun jarak jauh + Knock-up instan.</div>", unsafe_allow_html=True)
    if "Yaria" in our_picks and ("Lady Sun" in our_picks or "Ao'yin (Loong)" in our_picks):
        st.markdown("<div class='alert-success'>🔥 <b>ACTIVE COMBO:</b> <i>Support Revamp +15% Gold (Yaria + Carry)</i> Aktif! Hyper-carry gold boost.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 3. DYNAMIC REAL-TIME IN-GAME SCHEME
    st.markdown("#### ⚡ Dynamic In-Game Strategy Scheme")
    
    st.write("• **Early Game (0:00 - 4:00):** Roamer bantu Mid sapu wave minion 1. Amankan *Space Sprite* (Bunga Teleportasi Clash Lane) menit 1:00. Hati-hati gank Jungler musuh Level 4 menit 1:20-2:00.")
    st.write("• **Mid Game (4:00 - 10:00):** Pelat turret runtuh menit 4:00. Prioritaskan **Tyrant Pertama** untuk buff damage. Terapkan 2-player wave sharing (160% gold). Awas debuff *Primal Bond* (-50% damage ke naga kedua).")
    st.write("• **Late Game (10:00 - 20:00+):** Pertahankan formasi dekat choke points. **Dilarang bunuh naga biasa di menit 18:30-19:00** agar bebas debuff *Primal Bond* (-60% damage) saat **Tempest Dragon** muncul di menit 20:00!")

st.markdown("---")

# ==========================================
# TABS: EXPORT, MATCH LOG, & COMPLETE 116 HERO DB
# ==========================================
tab_export, tab_history, tab_database = st.tabs(["📲 Export to WhatsApp", "📊 Recent Match Analysis", "📚 Complete 116 Hero Database S16"])

with tab_export:
    st.subheader("📋 WhatsApp Copy-Paste Summary")
    
    wa_text = f"""*BLUEPRINT DRAFT HOK PRO* 🎮🔥
*Title:* {draft_title}
*Series:* {match_series} | *Side:* {our_side}
*Win Probability:* {our_win_rate}% (Our Team) vs {enemy_win_rate}% (Enemy)

🚫 *BANS:*
• *Our Bans:* {', '.join([b for b in [our_b1, our_b2, our_b3, our_b4] if b != 'None']) or 'None'}
• *Enemy Bans:* {', '.join([b for b in [enemy_b1, enemy_b2, enemy_b3, enemy_b4] if b != 'None']) or 'None'}

🛡️ *OUR PICKS:*
• *Clash:* {our_clash} | *Jungle:* {our_jungle}
• *Mid:* {our_mid} | *Farm:* {our_farm} | *Roam:* {our_roam}

🔴 *ENEMY PICKS:*
• *Clash:* {enemy_clash} | *Jungle:* {enemy_jungle}
• *Mid:* {enemy_mid} | *Farm:* {enemy_farm} | *Roam:* {enemy_roam}

⚡ *KEY TACTICAL SCHEME:*
• Early Prio Mid & Space Sprite (Min 1:00)
• First Tyrant Priority at Turret Collapse (Min 4:00)
• Beware Primal Bond Debuff & Tempest Dragon Setup (Min 20:00)

*Bantai Semuanya! Let's Go!* 🚀🔥"""

    st.code(wa_text, language="markdown")
    st.info("💡 Klik ikon 'Copy' di pojok kanan atas kotak teks di atas, lalu paste langsung ke WhatsApp tim!")

with tab_history:
    st.subheader("📊 Recent Match Logger & Analyst Notes")
    
    with st.form("match_log_form_v5"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            m_opp = st.text_input("Opponent Team", "EVOS / RRQ / Scrim Match")
            m_res = st.selectbox("Hasil Match", ["WIN 🏆", "LOSS ❌"])
        with col_m2:
            m_kda = st.text_input("Score KDA", "18 - 10")
            m_dur = st.text_input("Durasi Match", "14:25")
        with col_m3:
            m_mvp = st.text_input("MVP Player & Hero", "Dapid (Augran) / Reyhan (Lady Sun)")
            
        m_notes = st.text_area("Catatan Evaluasi Coach / Analyst", "Disiplin cover Mid jalan rapi. Inisiasi Late Game pas.")
        
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
    st.subheader(f"📚 Complete Hero Database S16 ({len(ALL_HEROES_LIST)} Heroes)")
    
    role_filter = st.radio("Filter Role:", ["All", "Clash", "Jungle", "Mid", "Farm", "Roam"], horizontal=True)
    search_query = st.text_input("🔍 Cari Hero berdasarkan Nama atau Deskripsi:", "")
    
    filtered_db = []
    for item in ALL_HEROES_LIST:
        if role_filter == "All" or role_filter == item["role"]:
            if search_query.lower() in item["name"].lower() or search_query.lower() in item["desc"].lower():
                filtered_db.append({
                    "Hero Name": item["name"],
                    "Role": item["role"],
                    "Tier": item["tier"],
                    "Win Rate": item["wr"],
                    "Pick Rate": item["pr"],
                    "Ban Rate": item["br"],
                    "Description": item["desc"]
                })
                
    df_db = pd.DataFrame(filtered_db)
    st.dataframe(df_db, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>HOK Pro Draft Engine v5 • Built for Esports Analysts • Credit: <b>By Siropkokop</b></div>", unsafe_allow_html=True)
