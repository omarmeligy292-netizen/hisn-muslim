
import streamlit as st
import requests
import html
import base64

# =========================
# إعدادات التطبيق
# =========================
st.set_page_config(
    page_title="حصن المسلم",
    page_icon="📿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE = "https://api.alquran.cloud/v1"
CDN_BASE = "https://cdn.islamic.network/quran"

# =========================
# العلامة المائية والتصميم
# =========================
watermark_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="420" height="160"
     viewBox="0 0 420 160">
  <g fill="none" stroke="#B99746" stroke-width="3">
    <circle cx="210" cy="38" r="24"/>
    <path d="M210 17 L216 31 L231 32 L220 42 L223 56
             L210 49 L197 56 L200 42 L189 32 L204 31 Z"
          fill="#B99746" stroke="none"/>
  </g>
  <text x="210" y="91" text-anchor="middle"
        font-family="Arial, sans-serif" font-size="23"
        font-weight="bold" fill="#B99746">Hisn al-Muslim</text>
  <text x="210" y="120" text-anchor="middle"
        font-family="Arial, sans-serif" font-size="17"
        fill="#B99746">OMAR MELIGY</text>
</svg>
"""

svg_encoded = base64.b64encode(
    watermark_svg.encode("utf-8")
).decode("utf-8")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #fbf9f2;
        position: relative;
    }}

    /* علامة مائية مستقيمة أفقيًا */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background-image: url("data:image/svg+xml;base64,{svg_encoded}");
        background-repeat: repeat;
        background-position: center center;
        background-size: 420px 160px;
        opacity: 0.35;
    }}

    /* محتوى التطبيق يظهر فوق العلامة المائية */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    [data-testid="stVerticalBlock"],
    section.main {{
        position: relative;
    }}

    [data-testid="stAppViewContainer"] {{
        background: transparent;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3, p, label {{
        color: #26382d;
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

    /* الأزرار الدائرية */
    div.stButton > button {{
        border-radius: 50%;
        width: 105px;
        height: 105px;
        min-width: 105px;
        white-space: normal;
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

    div.stButton > button:focus {{
        outline: 2px solid #b99746;
    }}

    .section-heading {{
        text-align: center;
        color: #244b36;
        font-size: 1.7rem;
        font-weight: bold;
        margin: 0.7rem 0 1rem 0;
    }}

    .quran-text {{
        direction: rtl;
        text-align: justify;
        line-height: 2.3;
        font-size: 1.45rem;
        color: #203c2d;
        background: rgba(255, 255, 255, 0.78);
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
        background: rgba(255, 255, 255, 0.8);
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

# =========================
# دوال الاتصال بالقرآن
# =========================
@st.cache_data(ttl=3600)
def get_surahs():
    response = requests.get(
        f"{API_BASE}/surah",
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 200:
        raise ValueError("تعذر تحميل قائمة السور.")

    return data["data"]


@st.cache_data(ttl=3600)
def get_surah_text(surah_number):
    response = requests.get(
        f"{API_BASE}/surah/{surah_number}/quran-uthmani",
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 200:
        raise ValueError("تعذر تحميل نص السورة.")

    return data["data"]


@st.cache_data(ttl=3600)
def get_audio_editions():
    response = requests.get(
        f"{API_BASE}/edition/format/audio",
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 200:
        return []

    return data.get("data", [])


# =========================
# الصفحة الرئيسية
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "tasbeeh_count" not in st.session_state:
    st.session_state.tasbeeh_count = 0

if "quran_page" not in st.session_state:
    st.session_state.quran_page = 0


def go_to(page):
    st.session_state.page = page


def back_home():
    st.session_state.page = "home"


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


def render_home():
    render_header()

    st.markdown(
        '<div class="section-heading">اختر القسم</div>',
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns(3)

    with left:
        st.markdown(
            "<div style='text-align:center'>",
            unsafe_allow_html=True,
        )
        if st.button("📿\nالأذكار", key="home_azkar"):
            go_to("azkar")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with middle:
        st.markdown(
            "<div style='text-align:center'>",
            unsafe_allow_html=True,
        )
        if st.button("📖\nالقرآن الكريم", key="home_quran"):
            go_to("quran")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            "<div style='text-align:center'>",
            unsafe_allow_html=True,
        )
        if st.button("🔢\nالتسبيح", key="home_tasbeeh"):
            go_to("tasbeeh")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# قسم الأذكار
# =========================
def render_azkar():
    if st.button("⬅️ الرئيسية", key="azkar_back"):
        back_home()
        st.rerun()

    st.markdown(
        '<div class="section-heading">أذكار مختارة</div>',
        unsafe_allow_html=True,
    )

    azkar = [
        (
            "أذكار الصباح",
            "أصبحنا وأصبح الملك لله، والحمد لله، "
            "لا إله إلا الله وحده لا شريك له.",
        ),
        (
            "ذكر الاستغفار",
            "أستغفر الله وأتوب إليه.",
        ),
        (
            "التسبيح",
            "سبحان الله وبحمده، سبحان الله العظيم.",
        ),
        (
            "ذكر التوكل",
            "حسبي الله لا إله إلا هو عليه توكلت "
            "وهو رب العرش العظيم.",
        ),
        (
            "الصلاة على النبي ﷺ",
            "اللهم صل وسلم على نبينا محمد.",
        ),
    ]

    st.info(
        "هذه أذكار مختارة كبداية، وليست مجموعة كاملة "
        "من الأذكار المأثورة."
    )

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


# =========================
# قسم القرآن الكريم
# =========================
def render_quran():
    if st.button("⬅️ الرئيسية", key="quran_back"):
        back_home()
        st.rerun()

    st.markdown(
        '<div class="section-heading">القرآن الكريم</div>',
        unsafe_allow_html=True,
    )

    try:
        surahs = get_surahs()
    except Exception as exc:
        st.error(f"تعذر تحميل السور. تحقق من اتصال الإنترنت. ({exc})")
        return

    surah_names = [
        f"{surah['number']}. {surah['name']}"
        for surah in surahs
    ]

    selected_name = st.selectbox(
        "اختر السورة",
        surah_names,
        key="selected_surah",
    )

    selected_index = surah_names.index(selected_name)
    selected_surah = surahs[selected_index]
    surah_number = selected_surah["number"]

    st.caption(
        f"عدد الآيات: {selected_surah['numberOfAyahs']} "
        f"• النوع: {selected_surah['revelationType']}"
    )

    try:
        surah_data = get_surah_text(surah_number)
        ayahs = surah_data["ayahs"]
    except Exception as exc:
        st.error(f"تعذر تحميل آيات السورة. ({exc})")
        return

    # عرض الآيات على صفحات، كل صفحة 20 آية
    page_size = 20
    total_pages = max(
        1,
        (len(ayahs) + page_size - 1) // page_size,
    )

    if st.session_state.quran_page >= total_pages:
        st.session_state.quran_page = 0

    current_page = st.session_state.quran_page
    start = current_page * page_size
    end = min(start + page_size, len(ayahs))
    page_ayahs = ayahs[start:end]

    if surah_number != 1 and surah_number != 9 and start == 0:
        st.markdown(
            '<div class="quran-text" style="text-align:center">'
            "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
            "</div>",
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

    previous_col, page_col, next_col = st.columns([1, 2, 1])

    with previous_col:
        if st.button(
            "السابق",
            disabled=current_page == 0,
            key="quran_previous",
        ):
            st.session_state.quran_page -= 1
            st.rerun()

    with page_col:
        st.selectbox(
            "رقم الصفحة",
            options=list(range(1, total_pages + 1)),
            index=current_page,
            key="quran_page_selector",
            on_change=lambda: setattr(
                st.session_state,
                "quran_page",
                st.session_state.quran_page_selector - 1,
            ),
        )

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

    # عرض القراء الذين توفر لهم إصدار صوتي
    audio_editions = [
        edition
        for edition in editions
        if edition.get("identifier")
        and edition.get("identifier", "").startswith("ar.")
    ]

    if audio_editions:
        reader_labels = [
            edition.get("englishName")
            or edition.get("name")
            or edition["identifier"]
            for edition in audio_editions
        ]

        selected_reader_label = st.selectbox(
            "اختر القارئ",
            reader_labels,
            key="quran_reader",
        )

        reader_index = reader_labels.index(selected_reader_label)
        reader = audio_editions[reader_index]
        reader_id = reader["identifier"]

        # هذه الإصدارات تستخدم API الخاص بالمصحف الصوتي
        audio_url = (
            f"{API_BASE}/surah/{surah_number}/{reader_id}"
        )

        if st.button("تحميل رابط التلاوة", key="load_audio"):
            try:
                audio_response = requests.get(
                    audio_url,
                    timeout=30,
                )
                audio_response.raise_for_status()
                audio_data = audio_response.json()

                if audio_data.get("code") == 200:
                    audio_file_url = audio_data["data"]["audio"]
                    st.audio(audio_file_url)
                else:
                    st.warning(
                        "لم يتوفر رابط صوتي لهذه السورة "
                        "من المصدر الحالي."
                    )
            except Exception:
                st.warning(
                    "تعذر جلب التلاوة الآن. جرّب مرة أخرى لاحقًا."
                )
    else:
        st.info(
            "لم يتم العثور على إصدارات صوتية متاحة حاليًا."
        )


# =========================
# قسم التسبيح
# =========================
def render_tasbeeh():
    if st.button("⬅️ الرئيسية", key="tasbeeh_back"):
        back_home()
        st.rerun()

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

    left_reset, right_reset = st.columns(2)

    with left_reset:
        if st.button("تصفير العداد", key="tasbeeh_reset"):
            st.session_state.tasbeeh_count = 0
            st.rerun()

    with right_reset:
        if st.button("ناقص واحد", key="tasbeeh_decrement"):
            st.session_state.tasbeeh_count = max(
                0,
                st.session_state.tasbeeh_count - 1,
            )
            st.rerun()


# =========================
# تشغيل الصفحة الحالية
# =========================
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
