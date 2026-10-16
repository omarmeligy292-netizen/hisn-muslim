
import streamlit as st
import requests
import math

st.set_page_config(
    page_title="حصن المسلم",
    page_icon="📿",
    layout="wide",
)

# ----------------------------
# إعدادات التطبيق
# ----------------------------

st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #16856b;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }
    .ayah-card {
        background-color: rgba(100, 150, 120, 0.10);
        padding: 18px;
        border-radius: 12px;
        margin: 10px 0;
        font-size: 23px;
        line-height: 2;
        text-align: center;
    }
    .zikr-card {
        background-color: rgba(100, 150, 120, 0.10);
        padding: 22px;
        border-radius: 12px;
        margin: 15px 0;
        font-size: 23px;
        line-height: 2;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# الأذكار
# تقدر تزود الأذكار من هنا
# ----------------------------

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

# ----------------------------
# القراء
# ----------------------------

READERS = {
    "مشاري العفاسي": "ar.alafasy",
    "محمود خليل الحصري": "ar.husary",
    "محمد صديق المنشاوي": "ar.minshawi",
    "عبدالرحمن السديس": "ar.sudais",
    "سعود الشريم": "ar.shuraim",
    "عبدالباسط عبدالصمد": "ar.abdulbasit",
    "أحمد العجمي": "ar.ajamy",
    "علي الحذيفي": "ar.hudhaify",
}

# ----------------------------
# الحالة المحفوظة
# ----------------------------

defaults = {
    "page": "الرئيسية",
    "zikr_category": "أذكار الصباح",
    "zikr_index": 0,
    "zikr_count": 0,
    "tasbeeh_count": 0,
    "surah_number": 1,
    "reader_name": "مشاري العفاسي",
    "quran_page": 1,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------
# جلب بيانات القرآن
# ----------------------------

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


# ----------------------------
# القائمة الرئيسية
# ----------------------------

st.markdown(
    '<div class="main-title">📿 حصن المسلم</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">الأذكار والقرآن الكريم والسبحة الإلكترونية</div>',
    unsafe_allow_html=True,
)

st.subheader("🎙️ اختار القارئ المفضل")

reader_names = list(READERS.keys())

st.selectbox(
    "القارئ",
    reader_names,
    key="reader_name",
)

st.caption(
    f"القارئ المختار: {st.session_state.reader_name}"
)

st.divider()

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

# ----------------------------
# قسم الأذكار
# ----------------------------

if st.session_state.page == "الأذكار":
    st.header("📿 قسم الأذكار")

    category = st.selectbox(
        "اختار نوع الأذكار",
        list(AZKAR.keys()),
        index=list(AZKAR.keys()).index(
            st.session_state.zikr_category
        ),
    )

    if category != st.session_state.zikr_category:
        st.session_state.zikr_category = category
        st.session_state.zikr_index = 0
        st.session_state.zikr_count = 0
        st.rerun()

    items = AZKAR[category]

    if st.session_state.zikr_index >= len(items):
        st.success("أحسنت! خلصت الأذكار الموجودة في القسم ده.")

        if st.button("ابدأ الأذكار من جديد"):
            st.session_state.zikr_index = 0
            st.session_state.zikr_count = 0
            st.rerun()

    else:
        item = items[st.session_state.zikr_index]

        st.caption(
            f"الذكر {st.session_state.zikr_index + 1} "
            f"من {len(items)}"
        )

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
                "سبّح ✓",
                use_container_width=True,
                disabled=current >= target,
            ):
                st.session_state.zikr_count += 1

                if st.session_state.zikr_count >= target:
                    st.session_state.zikr_count = 0
                    st.session_state.zikr_index += 1

                st.rerun()

        with col2:
            if st.button("الذكر التالي ⏭️", use_container_width=True):
                st.session_state.zikr_index += 1
                st.session_state.zikr_count = 0
                st.rerun()

        if st.button("🔄 إعادة الذكر الحالي"):
            st.session_state.zikr_count = 0
            st.rerun()

    if st.button("🏠 الرئيسية", key="home_azkar"):
        st.session_state.page = "الرئيسية"
        st.rerun()

# ----------------------------
# قسم القرآن الكريم
# ----------------------------

elif st.session_state.page == "القرآن":
    st.header("📖 القرآن الكريم")

    try:
        surahs = get_surahs()

        surah_options = {
            f'{s["number"]}. {s["name"]} — {s["englishName"]}': s["number"]
            for s in surahs
        }

        option_labels = list(surah_options.keys())

        current_label = next(
            (
                label
                for label, number in surah_options.items()
                if number == st.session_state.surah_number
            ),
            option_labels[0],
        )

        selected_label = st.selectbox(
            "اختار السورة",
            option_labels,
            index=option_labels.index(current_label),
        )

        number = surah_options[selected_label]

        if number != st.session_state.surah_number:
            st.session_state.surah_number = number
            st.session_state.quran_page = 1
            st.rerun()

        surah = get_surah(number)

        st.subheader(
            f'{surah["name"]} — {surah["englishName"]}'
        )

        st.caption(
            f'عدد الآيات: {surah["numberOfAyahs"]} | '
            f'رقم السورة: {surah["number"]}'
        )

        # صوت السورة حسب القارئ المختار
        reader_id = READERS[st.session_state.reader_name]

        audio_url = (
            "https://cdn.islamic.network/quran/audio-surah/"
            f"128/{reader_id}/{number}.mp3"
        )

        st.markdown(
            f'**🎙️ تلاوة السورة بصوت {st.session_state.reader_name}**'
        )
        st.audio(audio_url)

        # تقسيم القراءة إلى مجموعات من 20 آية
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
            f"عرض الآيات {start + 1} إلى {end} "
            f"من {len(ayahs)}"
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
            "حصلت مشكلة أثناء تحميل القرآن. "
            "اتأكد إن الإنترنت شغال وحاول تاني."
        )
        st.caption(f"تفاصيل الخطأ: {error}")

    if st.button("🏠 الرئيسية", key="home_quran"):
        st.session_state.page = "الرئيسية"
        st.rerun()

# ----------------------------
# قسم السبحة الإلكترونية
# ----------------------------

elif st.session_state.page == "السبحة":
    st.header("🔢 السبحة الإلكترونية")

    st.markdown(
        '<div class="zikr-card">سُبْحَانَ اللَّهِ وَبِحَمْدِهِ</div>',
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

    st.caption("تقدر تستخدم العداد للتسبيح والاستغفار.")

    if st.button("🏠 الرئيسية", key="home_tasbeeh"):
        st.session_state.page = "الرئيسية"
        st.rerun()

# ----------------------------
# تذييل التطبيق
# ----------------------------

st.divider()
st.caption("حصن المسلم — تقبّل الله منا ومنكم صالح الأعمال 🤍")
