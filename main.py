
import streamlit as st
import requests
import math

# =====================================
# إعدادات التطبيق
# =====================================

st.set_page_config(
    page_title="حصن المسلم",
    page_icon="📿",
    layout="wide",
)

# =====================================
# التصميم الذهبي والأبيض والأزرار المدورة
# =====================================

st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
        direction: rtl;
        text-align: right;
    }

    [data-testid="stHeader"] {
        background-color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background-color: #fffdf5;
    }

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        color: #b8860b;
        margin: 12px 0;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #8a6d1d;
        margin-bottom: 25px;
    }

    .ayah-card, .zikr-card {
        background-color: #ffffff;
        color: #333333;
        padding: 22px;
        border: 1px solid #d4af37;
        border-radius: 18px;
        margin: 12px 0;
        font-size: 23px;
        line-height: 2;
        text-align: center;
        box-shadow: 0 3px 10px rgba(184, 134, 11, 0.10);
    }

    h1, h2, h3 {
        color: #b8860b !important;
    }

    /* أزرار مدورة */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37, #b8860b);
        color: #ffffff;
        border: 1px solid #b8860b;
        border-radius: 50px;
        min-height: 48px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.25s ease;
        box-shadow: 0 4px 10px rgba(184, 134, 11, 0.18);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #b8860b, #9c7209);
        color: #ffffff;
        border: 1px solid #9c7209;
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(184, 134, 11, 0.28);
    }

    div.stButton > button:active {
        transform: scale(0.97);
    }

    div.stButton > button:disabled {
        background: #eee8d5;
        color: #888888;
        border: 1px solid #e2d7b6;
        box-shadow: none;
    }

    /* القوائم */
    div[data-baseweb="select"] > div {
        border-radius: 14px;
        border-color: #d4af37;
    }

    /* حقول الإدخال */
    div[data-baseweb="input"] > div {
        border-radius: 14px;
        border-color: #d4af37;
    }

    hr {
        border-color: #d4af37;
    }

    [data-testid="stProgressBar"] > div > div {
        background-color: #d4af37;
    }

    [data-testid="stMetricValue"] {
        color: #b8860b;
    }
</style>
""", unsafe_allow_html=True)


# =====================================
# الأذكار
# =====================================

AZKAR = {
    "أذكار الصباح": [
        {
            "text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ.",
            "count": 1,
        },
        {
            "text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ.",
            "count": 100,
        },
        {
            "text": "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ.",
            "count": 100,
        },
    ],
    "أذكار المساء": [
        {
            "text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ.",
            "count": 1,
        },
        {
            "text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ.",
            "count": 100,
        },
        {
            "text": "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ.",
            "count": 100,
        },
    ],
    "أذكار متنوعة": [
        {
            "text": "سُبْحَانَ اللَّهِ.",
            "count": 33,
        },
        {
            "text": "الْحَمْدُ لِلَّهِ.",
            "count": 33,
        },
        {
            "text": "اللَّهُ أَكْبَرُ.",
            "count": 34,
        },
        {
            "text": "لَا إِلَهَ إِلَّا اللَّهُ.",
            "count": 100,
        },
    ],
}


# =====================================
# القراء
# =====================================

READERS = {
    "مشاري العفاسي": "ar.alafasy",
    "محمود خليل الحصري": "ar.husary",
    "محمد صديق المنشاوي": "ar.minshawi",
    "عبدالرحمن السديس": "ar.abdurrahmaansudais",
    "سعود الشريم": "ar.saoodshuraym",
    "عبدالباسط عبدالصمد": "ar.abdulbasitmurattal",
    "أحمد العجمي": "ar.ahmedajamy",
    "علي الحذيفي": "ar.hudhaify",
}


# =====================================
# حالة التطبيق
# =====================================

DEFAULTS = {
    "page": "الرئيسية",
    "zikr_category": "أذكار الصباح",
    "zikr_index": 0,
    "zikr_count": 0,
    "tasbeeh_count": 0,
    "surah_number": 1,
    "reader_name": "مشاري العفاسي",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================
# تحميل بيانات القرآن
# =====================================

@st.cache_data(ttl=3600)
def get_surahs():
    response = requests.get(
        "https://api.alquran.cloud/v1/surah",
        timeout=20,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        raise ValueError("تعذر تحميل قائمة السور")

    return result["data"]


@st.cache_data(ttl=3600)
def get_surah(surah_number):
    response = requests.get(
        f"https://api.alquran.cloud/v1/surah/{surah_number}/quran-uthmani",
        timeout=20,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        raise ValueError("تعذر تحميل السورة")

    return result["data"]


# =====================================
# عنوان التطبيق
# =====================================

st.markdown(
    '<div class="main-title">📿 حصن المسلم</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'القرآن الكريم • الأذكار • السبحة الإلكترونية'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# =====================================
# اختيار القارئ
# =====================================

st.subheader("🎙️ اختار القارئ المفضل")

st.selectbox(
    "قارئ القرآن الكريم",
    options=list(READERS.keys()),
    key="reader_name",
)

st.caption(f'القارئ المختار: {st.session_state.reader_name}')

st.divider()


# =====================================
# القائمة الرئيسية
# =====================================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📿 الأذكار", use_container_width=True):
        st.session_state.page = "الأذكار"
        st.rerun()

with col2:
    if st.button("📖 القرآن الكريم", use_container_width=True):
        st.session_state.page = "القرآن"
        st.rerun()

with col3:
    if st.button("🔢 السبحة الإلكترونية", use_container_width=True):
        st.session_state.page = "السبحة"
        st.rerun()

st.divider()


# =====================================
# قسم الأذكار
# =====================================

if st.session_state.page == "الأذكار":

    st.header("📿 الأذكار")

    categories = list(AZKAR.keys())

    selected_category = st.selectbox(
        "اختار قسم الأذكار",
        categories,
        index=categories.index(st.session_state.zikr_category),
    )

    if selected_category != st.session_state.zikr_category:
        st.session_state.zikr_category = selected_category
        st.session_state.zikr_index = 0
        st.session_state.zikr_count = 0
        st.rerun()

    items = AZKAR[st.session_state.zikr_category]
    index = st.session_state.zikr_index

    if index >= len(items):

        st.success("أحسنت! انتهيت من الأذكار الموجودة في هذا القسم.")

        if st.button("🔄 ابدأ من جديد", use_container_width=True):
            st.session_state.zikr_index = 0
            st.session_state.zikr_count = 0
            st.rerun()

    else:

        item = items[index]

        st.caption(f"الذكر {index + 1} من {len(items)}")

        st.markdown(
            f'<div class="zikr-card">{item["text"]}</div>',
            unsafe_allow_html=True,
        )

        target = item["count"]
        current = st.session_state.zikr_count

        st.progress(min(current / target, 1.0))
        st.write(f"عدد التكرارات: {current} من {target}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "📿 تسبيح",
                use_container_width=True,
                disabled=current >= target,
            ):
                st.session_state.zikr_count += 1

                if st.session_state.zikr_count >= target:
                    st.session_state.zikr_count = 0
                    st.session_state.zikr_index += 1

                st.rerun()

        with col2:
            if st.button("⏭️ الذكر التالي", use_container_width=True):
                st.session_state.zikr_index += 1
                st.session_state.zikr_count = 0
                st.rerun()

        if st.button("🔄 إعادة عداد الذكر", use_container_width=True):
            st.session_state.zikr_count = 0
            st.rerun()

    if st.button("🏠 الرئيسية", key="home_azkar"):
        st.session_state.page = "الرئيسية"
        st.rerun()


# =====================================
# قسم القرآن الكريم
# =====================================

elif st.session_state.page == "القرآن":

    st.header("📖 القرآن الكريم")

    try:
        surahs = get_surahs()

        surah_options = {
            f'{surah["number"]}. {surah["name"]}': surah["number"]
            for surah in surahs
        }

        labels = list(surah_options.keys())

        selected_label = st.selectbox(
            "اختار السورة",
            labels,
            index=next(
                (
                    i for i, label in enumerate(labels)
                    if surah_options[label] == st.session_state.surah_number
                ),
                0,
            ),
        )

        number = surah_options[selected_label]

        if number != st.session_state.surah_number:
            st.session_state.surah_number = number
            st.rerun()

        surah = get_surah(number)

        st.subheader(surah["name"])

        st.caption(
            f'عدد الآيات: {surah["numberOfAyahs"]} | '
            f'رقم السورة: {surah["number"]}'
        )

        # صوت السورة حسب القارئ المختار
        reader_id = READERS[st.session_state.reader_name]

        audio_url = (
            "https://cdn.islamic.network/quran/audio-surah/128/"
            f"{reader_id}/{number}.mp3"
        )

        st.markdown(
            f'**🎧 تلاوة سورة {surah["name"]} '
            f'بصوت {st.session_state.reader_name}**'
        )

        st.audio(audio_url)

        st.divider()

        # عرض الآيات في مجموعات من 20 آية
        ayahs = surah["ayahs"]
        per_page = 20
        total_pages = max(1, math.ceil(len(ayahs) / per_page))

        page_key = f"quran_page_{number}"

        if page_key not in st.session_state:
            st.session_state[page_key] = 1

        st.session_state[page_key] = min(
            max(1, st.session_state[page_key]),
            total_pages,
        )

        st.number_input(
            "مجموعة الآيات",
            min_value=1,
            max_value=total_pages,
            step=1,
            key=page_key,
        )

        current_page = st.session_state[page_key]

        start = (current_page - 1) * per_page
        end = min(start + per_page, len(ayahs))

        st.caption(
            f"الآيات من {start + 1} إلى {end} "
            f"من أصل {len(ayahs)}"
        )

        for ayah in ayahs[start:end]:
            st.markdown(
                f'<div class="ayah-card">'
                f'{ayah["text"]}'
                f'<br><small>﴿ {ayah["numberInSurah"]} ﴾</small>'
                f'</div>',
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "⬅️ المجموعة السابقة",
                use_container_width=True,
                disabled=current_page <= 1,
                on_click=lambda k=page_key: st.session_state.update(
                    {k: max(1, st.session_state[k] - 1)}
                ),
            )

        with col2:
            st.button(
                "المجموعة التالية ➡️",
                use_container_width=True,
                disabled=current_page >= total_pages,
                on_click=lambda k=page_key, total=total_pages: st.session_state.update(
                    {k: min(total, st.session_state[k] + 1)}
                ),
            )

    except (requests.RequestException, ValueError, KeyError) as error:
        st.error(
            "تعذر تحميل القرآن الكريم. تأكد من اتصال الإنترنت وحاول مرة أخرى."
        )
        st.caption(f"تفاصيل الخطأ: {error}")

    if st.button("🏠 الرئيسية", key="home_quran"):
        st.session_state.page = "الرئيسية"
        st.rerun()


# =====================================
# قسم السبحة الإلكترونية
# =====================================

elif st.session_state.page == "السبحة":

    st.header("🔢 السبحة الإلكترونية")

    st.markdown(
        '<div class="zikr-card">'
        'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="main-title">'
        f'{st.session_state.tasbeeh_count}'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📿 تسبيح", use_container_width=True):
            st.session_state.tasbeeh_count += 1
            st.rerun()

    with col2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.tasbeeh_count = 0
            st.rerun()

    st.caption("استخدم العداد للتسبيح والاستغفار.")

    if st.button("🏠 الرئيسية", key="home_tasbeeh"):
        st.session_state.page = "الرئيسية"
        st.rerun()


# =====================================
# تذييل التطبيق
# =====================================

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        color: #b8860b;
        padding: 12px;
        font-size: 16px;
    ">
        حصن المسلم 🤍
        <br>
        تقبّل الله منا ومنكم صالح الأعمال
    </div>
    """,
    unsafe_allow_html=True,
)
