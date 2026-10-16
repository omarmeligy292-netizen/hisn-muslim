
import streamlit as st
import requests

# ======================================
# إعدادات التطبيق
# ======================================
st.set_page_config(
    page_title="حصن المسلم والقرآن الكريم",
    page_icon="🌙",
    layout="centered",
)

GREEN = "#123F35"
LIGHT_GREEN = "#1C5949"
GOLD = "#E8C878"
CREAM = "#F7F4EA"

API = "https://api.alquran.cloud/v1"

# ======================================
# الأذكار
# ======================================
AZKAR = {
    "أذكار الصباح": [
        ("أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.", 1),
        ("سبحان الله وبحمده", 100),
        ("أستغفر الله وأتوب إليه", 100),
    ],
    "أذكار المساء": [
        ("أمسينا وأمسى الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.", 1),
        ("سبحان الله وبحمده", 100),
        ("أستغفر الله وأتوب إليه", 100),
    ],
    "أذكار النوم": [
        ("باسمك اللهم أموت وأحيا", 1),
        ("سبحان الله", 33),
        ("الحمد لله", 33),
        ("الله أكبر", 34),
    ],
}

# ======================================
# الحالة
# ======================================
DEFAULTS = {
    "page": "home",
    "items": [],
    "index": 0,
    "count": 0,
    "current_name": "",
    "tasbeeh_count": 0,
    "surah_number": 1,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ======================================
# التصميم
# ======================================
st.markdown("""
<style>
.stApp {
    background-color: #F7F4EA;
    color: #123F35;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 850px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
h1 {
    background: #123F35;
    color: #E8C878 !important;
    text-align: center;
    padding: 22px 10px;
    border-radius: 16px;
}
h2, h3 {
    color: #123F35 !important;
    text-align: center;
}
.zikr-card, .ayah-card {
    background: #FFFFFF;
    border: 1px solid #E8C878;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    color: #123F35;
    line-height: 2.1;
    text-align: center;
    direction: rtl;
}
.zikr-card {
    font-size: 24px;
}
.ayah-card {
    font-size: 25px;
}
.counter {
    color: #123F35;
    font-size: 54px;
    font-weight: bold;
    text-align: center;
    padding: 16px;
}
.stButton > button {
    background-color: #1C5949;
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 46px;
    width: 100%;
    font-size: 17px;
}
.stButton > button:hover {
    background-color: #E8C878;
    color: #123F35;
}
.footer {
    text-align: center;
    color: #1C5949;
    margin-top: 28px;
}
</style>
""", unsafe_allow_html=True)


# ======================================
# جلب بيانات القرآن
# ======================================
@st.cache_data(ttl=3600)
def get_surahs():
    response = requests.get(f"{API}/surah", timeout=20)
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        raise ValueError("تعذر تحميل قائمة السور")

    return result["data"]


@st.cache_data(ttl=3600)
def get_surah(number):
    response = requests.get(
        f"{API}/surah/{number}/quran-uthmani",
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 200:
        raise ValueError("تعذر تحميل السورة")

    return result["data"]


# ======================================
# التنقل
# ======================================
def go_home():
    st.session_state["page"] = "home"
    st.rerun()


def open_azkar(name):
    st.session_state["current_name"] = name
    st.session_state["items"] = list(AZKAR[name])
    st.session_state["index"] = 0
    st.session_state["count"] = 0
    st.session_state["page"] = "azkar"
    st.rerun()


def repeat_zikr():
    items = st.session_state.get("items", [])
    index = st.session_state.get("index", 0)
    count = st.session_state.get("count", 0)

    if not isinstance(items, list):
        return
    if not isinstance(index, int) or isinstance(index, bool):
        return
    if not isinstance(count, int) or isinstance(count, bool):
        return
    if index < 0 or index >= len(items):
        return

    _, target = items[index]

    if count + 1 >= target:
        st.session_state["index"] = index + 1
        st.session_state["count"] = 0
    else:
        st.session_state["count"] = count + 1


# ======================================
# العنوان
# ======================================
st.markdown(
    "<h1>🌙 حِصْنُ المُسْلِم</h1>",
    unsafe_allow_html=True,
)

# ======================================
# الرئيسية
# ======================================
page = st.session_state.get("page", "home")

if page == "home":
    st.markdown("### أذكارك اليومية وطمأنينة قلبك")

    st.markdown("#### 📿 الأذكار")

    for name in AZKAR:
        if st.button(name, key=f"open_{name}"):
            open_azkar(name)

    st.markdown("#### 📖 القرآن الكريم")

    if st.button("فتح القرآن الكريم", key="open_quran"):
        st.session_state["page"] = "quran"
        st.rerun()

    if st.button("📿 السبحة الإلكترونية", key="open_tasbeeh"):
        st.session_state["page"] = "tasbeeh"
        st.rerun()

    st.markdown(
        '<div class="footer">نسأل الله أن ينفعنا وإياكم 🤍</div>',
        unsafe_allow_html=True,
    )


# ======================================
# صفحة الأذكار
# ======================================
elif page == "azkar":
    st.subheader(st.session_state.get("current_name", "الأذكار"))

    items = st.session_state.get("items", [])
    index = st.session_state.get("index", 0)
    count = st.session_state.get("count", 0)

    if not isinstance(items, list):
        st.error("بيانات الأذكار غير صالحة.")
        if st.button("العودة للرئيسية", key="azkar_error_home"):
            go_home()

    elif not isinstance(index, int) or isinstance(index, bool):
        st.session_state["index"] = 0
        st.session_state["count"] = 0
        st.rerun()

    elif not items:
        st.info("مفيش أذكار للعرض حاليًا.")
        if st.button("العودة للرئيسية", key="azkar_empty_home"):
            go_home()

    elif index < 0:
        st.session_state["index"] = 0
        st.session_state["count"] = 0
        st.rerun()

    elif index >= len(items):
        st.success("أحسنت! أتممت هذه الأذكار 🌿")

        if st.button("تكرار الأذكار", key="azkar_restart"):
            open_azkar(st.session_state["current_name"])

        if st.button("العودة للرئيسية", key="azkar_done_home"):
            go_home()

    else:
        zikr, target = items[index]

        if not isinstance(count, int) or isinstance(count, bool):
            count = 0
            st.session_state["count"] = 0

        st.markdown(
            f'<div class="zikr-card">{zikr}</div>',
            unsafe_allow_html=True,
        )

        st.progress(min(count / target, 1.0))
        st.markdown(f"**التكرار: {count} / {target}**")
        st.caption(f"الذكر {index + 1} من {len(items)}")

        if st.button("✓ تم الذكر", key="zikr_repeat"):
            repeat_zikr()
            st.rerun()

        if st.button("العودة للرئيسية", key="zikr_home"):
            go_home()


# ======================================
# صفحة القرآن الكريم
# ======================================
elif page == "quran":
    st.subheader("📖 القرآن الكريم")

    try:
        surahs = get_surahs()

        # قائمة السور
        current_number = st.session_state.get("surah_number", 1)
        if not isinstance(current_number, int) or not 1 <= current_number <= 114:
            current_number = 1
            st.session_state["surah_number"] = 1

        selected_surah = st.selectbox(
            "اختار السورة",
            options=surahs,
            index=current_number - 1,
            format_func=lambda s: (
                f'{s["number"]}. {s["name"]} '
                f'— {s["numberOfAyahs"]} آية'
            ),
            key="surah_selector",
        )

        number = selected_surah["number"]
        st.session_state["surah_number"] = number

        data = get_surah(number)

        st.markdown(f"### {data['name']}")
        st.caption(
            f'{data["englishName"]} · '
            f'{data["numberOfAyahs"]} آية · '
            f'{"مكية" if data["revelationType"] == "Meccan" else "مدنية"}'
        )

        # مشغل تلاوة السورة
        st.markdown("#### 🎧 استمع للتلاوة")

        audio_url = (
            "https://cdn.islamic.network/quran/audio-surah/"
            f'128/ar.alafasy/{number}.mp3'
        )

        st.audio(audio_url, format="audio/mp3")

        st.caption(
            "التلاوة تُحمّل من مصدر خارجي؛ تحتاج اتصالًا بالإنترنت."
        )

        st.divider()
        st.markdown("#### 📖 قراءة الآيات")

        # تقسيم العرض لتسهيل القراءة
        per_page = 20
        ayahs = data.get("ayahs", [])
        total_pages = max(1, (len(ayahs) + per_page - 1) // per_page)

        page_key = f"quran_page_{number}"
        if page_key not in st.session_state:
            st.session_state[page_key] = 1

        current_page = st.session_state[page_key]
        if not isinstance(current_page, int):
            current_page = 1

        current_page = max(1, min(current_page, total_pages))
        st.session_state[page_key] = current_page

        new_page = st.select_slider(
            "صفحة القراءة",
            options=list(range(1, total_pages + 1)),
            value=current_page,
            key=f"quran_page_selector_{number}",
        )
        st.session_state[page_key] = new_page

        start = (new_page - 1) * per_page
        end = start + per_page

        for ayah in ayahs[start:end]:
            st.markdown(
                f'<div class="ayah-card">'
                f'{ayah["text"]}'
                f'<br><span style="color:{LIGHT_GREEN};'
                f'font-size:16px;">۞ {ayah["numberInSurah"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "⬅️ الصفحة السابقة",
                disabled=(new_page <= 1),
                key=f"quran_prev_{number}",
            ):
                st.session_state[page_key] = new_page - 1
                st.rerun()

        with col2:
            if st.button(
                "الصفحة التالية ➡️",
                disabled=(new_page >= total_pages),
                key=f"quran_next_{number}",
            ):
                st.session_state[page_key] = new_page + 1
                st.rerun()

    except requests.RequestException:
        st.error(
            "مش قادرين نوصل لمصدر القرآن دلوقتي. "
            "تأكد من الإنترنت وجرب تاني."
        )

    except (ValueError, KeyError, TypeError):
        st.error(
            "حصلت مشكلة في تحميل بيانات السورة. "
            "جرب تحديث الصفحة بعد شوية."
        )

    if st.button("العودة للرئيسية", key="quran_home"):
        go_home()


# ======================================
# السبحة الإلكترونية
# ======================================
elif page == "tasbeeh":
    st.subheader("📿 السبحة الإلكترونية")

    count = st.session_state.get("tasbeeh_count", 0)
    if not isinstance(count, int) or isinstance(count, bool):
        count = 0
        st.session_state["tasbeeh_count"] = 0

    st.markdown(
        f'<div class="counter">{count}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### سبحان الله")

    if st.button("تسبيح +1", key="tasbeeh_add"):
        st.session_state["tasbeeh_count"] += 1
        st.rerun()

    if st.button("تصفير العداد", key="tasbeeh_reset"):
        st.session_state["tasbeeh_count"] = 0
        st.rerun()

    if st.button("العودة للرئيسية", key="tasbeeh_home"):
        go_home()


# ======================================
# معالجة أي صفحة غير معروفة
# ======================================
else:
    st.session_state["page"] = "home"
    st.rerun()
