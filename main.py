
import streamlit as st
import requests
import html
import base64

# ==========================================
# إعداد التطبيق
# ==========================================
st.set_page_config(
    page_title="حصن المسلم",
    page_icon="📿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE = "https://api.alquran.cloud/v1"

# ==========================================
# العلامة المائية
# نستخدم صورة خلفية مباشرة بدون طبقات z-index
# ==========================================
watermark_svg = """
<svg xmlns="http://www.w3.org/2000/svg"
     width="500" height="220" viewBox="0 0 500 220">
  <g opacity="0.18" fill="#B99746">
    <circle cx="250" cy="55" r="30"
            fill="none" stroke="#B99746" stroke-width="4"/>
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

svg_encoded = base64.b64encode(
    watermark_svg.encode("utf-8")
).decode("utf-8")

# ==========================================
# تصميم التطبيق
# ==========================================
st.markdown(
    f"""
    <style>
    /* الخلفية والعلامة المائية بدون pseudo-elements */
    .stApp {{
        background-color: #fbf9f2 !important;
        background-image: url(
            "data:image/svg+xml;base64,{svg_encoded}"
        ) !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        background-size: min(500px, 75vw) auto !important;
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
        color: #244b36;
        margin-bottom: 0.2rem;
    }}

    .app-subtitle {{
        text-align: center;
        font-size: 1.05rem;
        color: #78683e;
        margin-bottom: 1.5rem;
    }}

    .section-heading {{
        text-align: center;
        color: #244b36;
        font-size: 1.7rem;
        font-weight: bold;
        margin: 0.7rem 0 1rem 0;
    }}

    div.stButton > button {{
        border-radius: 50%;
        width: 105px;
        height: 105px;
        min-width: 105px;
        white-space: pre-wrap;
        font-size: 1rem;
        font-weight: bold;
        background-color: #e8dfc5;
        color: #244b36;
        border: 2px solid #b99746;
        box-shadow: 0 3px 9px rgba(0, 0, 0, 0.08);
        transition: 0.2s ease;
    }}

    div.stButton > button:hover {{
        background-color: #d9c99f;
        border-color: #244b36;
        color: #183625;
    }}

    .quran-text {{
        direction: rtl;
        text-align: justify;
        line-height: 2.3;
        font-size: 1.45rem;
        color: #203c2d;
        background: rgba(255, 255, 255, 0.94);
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid #e0d4b4;
    }}

    .zekr-card {{
        direction: rtl;
        text-align: right;
        line-height: 2;
        font-size: 1.25rem;
        color: #203c2d;
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid #e0d4b4;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }}

    .tasbeeh-count {{
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #244b36;
        padding: 1rem;
    }}

    @media (max-width: 600px) {{
        div.stButton > button {{
            width: 85px;
            height: 85px;
            min-width: 85px;
            font-size: 0.85rem;
        }}

        .app-title {{
            font-size: 2rem;
        }}

        .quran-text {{
            font-size: 1.2rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# بيانات القرآن
# ==========================================
@st.cache_data(ttl=3600)
def get_surahs():
    response = requests.get(
        f"{API_BASE}/surah",
        timeout=20,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        raise ValueError("تعذر تحميل قائمة السور.")

    return result["data"]


@st.cache_data(ttl=3600)
def get_surah_text(surah_number):
    response = requests.get(
        f"{API_BASE}/surah/{surah_number}/quran-uthmani",
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        raise ValueError("تعذر تحميل آيات السورة.")

    return result["data"]


@st.cache_data(ttl=3600)
def get_audio_editions():
    response = requests.get(
        f"{API_BASE}/edition/format/audio",
        timeout=20,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        return []

    return result.get("data", [])


# ==========================================
# حالة التطبيق
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "tasbeeh_count" not in st.session_state:
    st.session_state.tasbeeh_count = 0

if "quran_page" not in st.session_state:
    st.session_state.quran_page = 0

if "last_surah" not in st.session_state:
    st.session_state.last_surah = 1


def go_to(page):
    st.session_state.page = page


def render_header():
    st.markdown(
        '<div class="app-title">حصن المسلم</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="app-subtitle">'
        "أذكارك ووردك اليومي في مكان واحد"
        "</div>",
        unsafe_allow_html=True,
    )


def render_back_button(key):
    if st.button("⬅️ الرئيسية", key=key):
        go_to("home")
        st.rerun()


# ==========================================
# الرئيسية
# ==========================================
def render_home():
    render_header()

    st.markdown(
        '<div class="section-heading">اختر القسم</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📿\nالأذكار", key="home_azkar"):
            go_to("azkar")
            st.rerun()

    with col2:
        if st.button("📖\nالقرآن الكريم", key="home_quran"):
            go_to("quran")
            st.session_state.quran_page = 0
            st.rerun()

    with col3:
        if st.button("🔢\nالتسبيح", key="home_tasbeeh"):
            go_to("tasbeeh")
            st.rerun()


# ==========================================
# الأذكار
# ==========================================
def render_azkar():
    render_back_button("azkar_back")

    st.markdown(
        '<div class="section-heading">أذكار مختارة</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "هذه أذكار مختارة كبداية، وليست مجموعة كاملة "
        "من الأذكار المأثورة."
    )

    azkar = [
        (
            "ذكر الصباح",
            "أصبحنا وأصبح الملك لله، والحمد لله، "
            "لا إله إلا الله وحده لا شريك له.",
        ),
        ("الاستغفار", "أستغفر الله وأتوب إليه."),
        (
            "التسبيح",
            "سبحان الله وبحمده، سبحان الله العظيم.",
        ),
        (
            "التوكل",
            "حسبي الله لا إله إلا هو عليه توكلت "
            "وهو رب العرش العظيم.",
        ),
        (
            "الصلاة على النبي ﷺ",
            "اللهم صل وسلم على نبينا محمد.",
        ),
    ]

    for title, text in azkar:
        st.markdown(
            f"""
            <div class="zekr-card">
                <strong>{html.escape(title)}</strong>
                <hr>
                {html.escape(text)}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================
# القرآن الكريم
# ==========================================
def render_quran():
    render_back_button("quran_back")

    st.markdown(
        '<div class="section-heading">القرآن الكريم</div>',
        unsafe_allow_html=True,
    )

    try:
        surahs = get_surahs()
    except Exception:
        st.error(
            "تعذر تحميل السور. تحقق من الإنترنت وحاول مرة أخرى."
        )
        return

    surah_labels = [
        f"{surah['number']}. {surah['name']}"
        for surah in surahs
    ]

    selected_label = st.selectbox(
        "اختر السورة",
        surah_labels,
        key="selected_surah",
    )

    surah_index = surah_labels.index(selected_label)
    surah = surahs[surah_index]
    surah_number = surah["number"]

    if st.session_state.last_surah != surah_number:
        st.session_state.quran_page = 0
        st.session_state.last_surah = surah_number

    st.caption(
        f"عدد الآيات: {surah['numberOfAyahs']} "
        f"• النوع: {surah['revelationType']}"
    )

    try:
        surah_data = get_surah_text(surah_number)
        ayahs = surah_data["ayahs"]
    except Exception:
        st.error("تعذر تحميل آيات السورة.")
        return

    page_size = 20
    total_pages = max(
        1,
        (len(ayahs) + page_size - 1) // page_size,
    )

    current_page = min(
        st.session_state.quran_page,
        total_pages - 1,
    )
    st.session_state.quran_page = current_page

    start = current_page * page_size
    page_ayahs = ayahs[start:start + page_size]

    if surah_number not in (1, 9) and start == 0:
        st.markdown(
            """
            <div class="quran-text" style="text-align:center">
                بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

    ayah_text = " ".join(
        f"{ayah['text']} ﴿{ayah['numberInSurah']}﴾"
        for ayah in page_ayahs
    )

    st.markdown(
        f'<div class="quran-text">{html.escape(ayah_text)}</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        f"الصفحة {current_page + 1} من {total_pages}"
    )

    prev_col, page_col, next_col = st.columns([1, 2, 1])

    with prev_col:
        if st.button(
            "السابق",
            disabled=current_page == 0,
            key="quran_previous",
        ):
            st.session_state.quran_page -= 1
            st.rerun()

    with page_col:
        selected_page = st.selectbox(
            "رقم الصفحة",
            options=list(range(1, total_pages + 1)),
            index=current_page,
            key="quran_page_selector",
        )

        if selected_page - 1 != current_page:
            st.session_state.quran_page = selected_page - 1
            st.rerun()

    with next_col:
        if st.button(
            "التالي",
            disabled=current_page >= total_pages - 1,
            key="quran_next",
        ):
            st.session_state.quran_page += 1
            st.rerun()

    st.divider()
    st.subheader("استماع إلى السورة")

    try:
        editions = get_audio_editions()
    except Exception:
        editions = []

    audio_editions = [
        edition for edition in editions
        if edition.get("identifier")
        and edition.get("format") == "audio"
    ]

    if not audio_editions:
        st.info("لا توجد إصدارات صوتية متاحة حاليًا.")
        return

    reader_labels = [
        edition.get("englishName")
        or edition.get("name")
        or edition["identifier"]
        for edition in audio_editions
    ]

    reader_index = st.selectbox(
        "اختر القارئ",
        options=list(range(len(audio_editions))),
        format_func=lambda i: reader_labels[i],
        key="quran_reader_index",
    )

    reader_id = audio_editions[reader_index]["identifier"]

    if st.button("تشغيل التلاوة", key="play_audio"):
        try:
            response = requests.get(
                f"{API_BASE}/surah/{surah_number}/{reader_id}",
                timeout=30,
            )
            response.raise_for_status()
            audio_result = response.json()

            if audio_result.get("code") == 200:
                st.audio(audio_result["data"]["audio"])
            else:
                st.warning("لم يتم العثور على رابط صوتي للسورة.")
        except Exception:
            st.warning(
                "تعذر تشغيل التلاوة الآن. حاول مرة أخرى لاحقًا."
            )


# ==========================================
# السبحة الإلكترونية
# ==========================================
def render_tasbeeh():
    render_back_button("tasbeeh_back")

    st.markdown(
        '<div class="section-heading">السبحة الإلكترونية</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="tasbeeh-count">'
        f'{st.session_state.tasbeeh_count}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='text-align:center'>"
        "سبحان الله • الحمد لله • الله أكبر"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")
    left, middle, right = st.columns(3)

    with middle:
        if st.button("📿\nسبّح", key="tasbeeh_increment"):
            st.session_state.tasbeeh_count += 1
            st.rerun()

    reset_col, minus_col = st.columns(2)

    with reset_col:
        if st.button("تصفير العداد", key="tasbeeh_reset"):
            st.session_state.tasbeeh_count = 0
            st.rerun()

    with minus_col:
        if st.button("ناقص واحد", key="tasbeeh_decrement"):
            st.session_state.tasbeeh_count = max(
                0,
                st.session_state.tasbeeh_count - 1,
            )
            st.rerun()


# ==========================================
# تشغيل الصفحة
# ==========================================
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "azkar":
    render_azkar()
elif st.session_state.page == "quran":
    render_quran()
elif st.session_state.page == "tasbeeh":
    render_tasbeeh()
else:
    st.session_state.page = "home"
    render_home()
