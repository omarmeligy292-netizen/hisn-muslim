import base64
import html
import requests
import streamlit as st

# ==========================================
# إعداد التطبيق
# ==========================================
st.set_page_config(
    page_title="حصن المسلم - الوضع الليلي",
    page_icon="📿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE = "https://alquran.cloud"

# ==========================================
# العلامة المائية
# ==========================================
watermark_svg = """
<svg xmlns="http://w3.org"
     width="500" height="220" viewBox="0 0 500 220">
  <g fill="#D4AF37">
    <circle cx="250" cy="55" r="30"
            fill="none" stroke="#D4AF37" stroke-width="4"/>
    <path d="M250 32 L257 48 L274 49 L261 60
             L265 77 L250 68 L235 77 L239 60
             L226 49 L243 48 Z"/>
    <text x="250" y="135" text-anchor="middle"
          font-family="Arial, sans-serif" font-size="30"
          font-weight="bold">
      Hisn al-Muslim
    </text>
    <text x="250" y="170" text-anchor="middle"
          font-family="Arial, sans-serif" font-size="22">
      OMAR MELIGY
    </text>
  </g>
</svg>
"""

svg_encoded = base64.b64encode(watermark_svg.encode("utf-8")).decode("utf-8")

# ==========================================
# التصميم والـ CSS
# ==========================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #122419 !important;
        background-image: url(
            "data:image/svg+xml;base64,{svg_encoded}"
        ) !important;
        background-repeat: no-repeat !important;
        background-position: center 65% !important;
        background-size: 300px auto !important;
        background-attachment: fixed !important;
    }}

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    .app-title {{
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #e6c673;
        margin-bottom: 0.2rem;
    }}

    .app-subtitle {{
        text-align: center;
        font-size: 1.05rem;
        color: #b5a476;
        margin-bottom: 1.5rem;
    }}

    .section-heading {{
        text-align: center;
        color: #e6c673;
        font-size: 1.7rem;
        font-weight: bold;
        margin: 0.7rem 0 1rem 0;
    }}

    div.stButton > button {{
        border-radius: 50%;
        width: 105px;
        height: 105px;
        min-width: 105px;
        padding: 0;
        white-space: pre-wrap;
        font-size: 0.95rem;
        font-weight: bold;
        background-color: #1b3827;
        color: #e6c673;
        border: 2px solid #b99746;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: 0.2s ease;
        margin: 0 !important;
    }}

    div.stButton > button:hover {{
        background-color: #244b34;
        border-color: #e6c673;
        color: #fff;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 0.35rem !important;
    }}

    .quran-text {{
        direction: rtl;
        text-align: justify;
        line-height: 2.3;
        font-size: 1.45rem;
        color: #e1edd9;
        background: rgba(23, 43, 31, 0.95);
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid #365c43;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}

    .zekr-card {{
        direction: rtl;
        text-align: right;
        line-height: 2;
        font-size: 1.25rem;
        color: #e1edd9;
        background: rgba(23, 43, 31, 0.95);
        border: 1px solid #365c43;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }}
    
    .zekr-card strong {{
        color: #e6c673;
    }}

    .tasbeeh-count {{
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        color: #e6c673;
        padding: 1rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }}

    .stSelectbox label {{
        color: #e6c673 !important;
    }}

    @media (max-width: 600px) {{
        div.stButton > button {{
            width: 82px;
            height: 82px;
            min-width: 82px;
            font-size: 0.8rem;
        }}

        .app-title {{
            font-size: 2rem;
        }}

        .quran-text {{
            font-size: 1.2rem;
        }}

        .stApp {{
            background-size: 240px auto !important;
            background-position: center 70% !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# بيانات القرآن الكريم
# ==========================================
@st.cache_data(ttl=3600)
def get_surahs():
    response = requests.get(f"{API_BASE}/surah", timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 200:
        raise ValueError("تعذر تحميل قائمة السور")
    return data["data"]


@st.cache_data(ttl=3600)
def get_surah_text(surah_number):
    response = requests.get(
        f"{API_BASE}/surah/{surah_number}/quran-uthmani", timeout=30
    )
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 200:
        raise ValueError("تعذر تحميل آيات السورة")
    return data["data"]


# ==========================================
# حالة التطبيق (Session State)
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "tasbeeh_count" not in st.session_state:
    st.session_state.tasbeeh_count = 0


def go_to(page):
    st.session_state.page = page


def render_header():
    st.markdown('<div class="app-title">حصن المسلم</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">أذكارك ووردك اليومي في مكان واحد</div>',
        unsafe_allow_html=True,
    )


def render_back_button(key):
    if st.button("⬅️ الرئيسية", key=key):
        go_to("home")
        st.rerun()


# ==========================================
# 1. الصفحة الرئيسية
# ==========================================
def render_home():
    render_header()
    st.markdown(
        '<div class="section-heading">اختر القسم</div>', unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 3, 1])
    with center:
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            if st.button("📿\nالأذكار", key="home_azkar"):
                go_to("azkar")
                st.rerun()
        with col2:
            if st.button("📖\nالقرآن", key="home_quran"):
                go_to("quran")
                st.rerun()
        with col3:
            if st.button("🔢\nالتسبيح", key="home_tasbeeh"):
                go_to("tasbeeh")
                st.rerun()


# ==========================================
# 2. قسم الأذكار
# ==========================================
def render_azkar():
    render_back_button("azkar_back")
    st.markdown(
        '<div class="section-heading">أذكار مختارة</div>', unsafe_allow_html=True
    )

    st.info("هذه أذكار مختارة كبداية، وليست مجموعة كاملة من الأذكار المأثورة.")

    azkar = [
        (
            "ذكر الصباح",
            "أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له.",
        ),
        ("الاستغفار", "أستغفر الله وأتوب إليه."),
        ("التسبيح", "سبحان الله وبحمده، سبحان الله العظيم."),
        ("التوكل", "حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم."),
        (
            "الصلاة على النبي ﷺ",
            "اللهم صلِّ وسلم وبارك على نبينا محمد وعلى آله وصحبه أجمعين.",
        ),
    ]

    for title, text in azkar:
        st.markdown(
            f"""
            <div class="zekr-card">
                <strong>{title}:</strong><br>{text}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================
# 3. قسم القرآن الكريم
# ==========================================
def render_quran():
    render_back_button("quran_back")
    st.markdown(
        '<div class="section-heading">القرآن الكريم</div>', unsafe_allow_html=True
    )

    try:
        surahs = get_surahs()
        surah_names = [f"{s['number']}. {s['name']}" for s in surahs]

        selected_surah_name = st.selectbox("اختر السورة:", surah_names)
        surah_num = int(selected_surah_name.split(".")[0])

        surah_data = get_surah_text(surah_num)

        ayahi_text = ""
        for ayah in surah_data["ayahs"]:
            ayahi_text += f"{ayah['text']} ﴿{ayah['numberInSurah']}﴾ "

        st.markdown(
            f'<div class="quran-text">{ayahi_text}</div>', unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")


# ==========================================
# 4. قسم عداد التسبيح
# ==========================================
def render_tasbeeh():
    render_back_button("tasbeeh_back")
    st.markdown(
        '<div class="section-heading">عداد التسبيح</div>', unsafe_allow_html=True
    )

    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        st.markdown(
            f'<div class="tasbeeh-count">{st.session_state.tasbeeh_count}</div>',
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("➕\nاضغط", key="click_tasbeeh"):
                st.session_state.tasbeeh_count += 1
                st.rerun()
        with btn_col2:
            if st.button("🔄\nتصفير", key="reset_tasbeeh"):
                st.session_state.tasbeeh_count = 0
                st.rerun()


# ==========================================
# منطق توجيه الصفحات
# ==========================================
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "azkar":
    render_azkar()
elif st.session_state.page == "quran":
    render_quran()
