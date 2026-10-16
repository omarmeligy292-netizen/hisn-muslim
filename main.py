
import math
import requests
import streamlit as st

st.set_page_config(
    page_title="حصن المسلم",
    page_icon="📿",
    layout="centered",
)

# -------------------- تنسيق التطبيق --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fffdf5, #fff5d6);
    color: #5c4510;
}

h1, h2, h3, p, label {
    color: #72520c;
}

div.stButton > button {
    width: 112px;
    height: 112px;
    min-height: 112px;
    border-radius: 50%;
    border: 2px solid #d4af37;
    background: linear-gradient(145deg, #f9e7a0, #c99a18);
    color: #503900;
    font-weight: bold;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    margin: 8px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

div.stButton > button:hover {
    border-color: #8b6914;
    color: #342400;
}

.verse {
    background: #fffaf0;
    border: 1px solid #e6cf80;
    border-radius: 14px;
    padding: 16px;
    margin: 10px 0;
    font-size: 22px;
    line-height: 2;
    text-align: right;
    color: #46340a;
}

.counter {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #b8860b;
}

@media (max-width: 600px) {
    div.stButton > button {
        width: 88px;
        height: 88px;
        min-height: 88px;
        font-size: 12px;
        padding: 5px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- القراء --------------------


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

if "reader_name" not in st.session_state:
    st.session_state.reader_name = "مشاري العفاسي"

if "show_readers" not in st.session_state:
    st.session_state.show_readers = False

if "page" not in st.session_state:
    st.session_state.page = "home"

if "tasbeeh_count" not in st.session_state:
    st.session_state.tasbeeh_count = 0


# -------------------- العنوان --------------------

st.markdown(
    "<h1 style='text-align:center'>📿 حصن المسلم</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center'>أذكارك وقرآنك في مكان واحد</p>",
    unsafe_allow_html=True,
)


# -------------------- الصفحة الرئيسية --------------------

if st.session_state.page == "home":

    st.subheader("🌙 اختر القسم")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📿\nالأذكار", key="go_azkar"):
            st.session_state.page = "azkar"
            st.rerun()

    with col2:
        if st.button("📖\nالقرآن الكريم", key="go_quran"):
            st.session_state.page = "quran"
            st.rerun()

    with col3:
        if st.button("🔢\nالمسبحة", key="go_tasbeeh"):
            st.session_state.page = "tasbeeh"
            st.rerun()

    st.info("اختار قسم القرآن الكريم عشان تختار القارئ.")


# -------------------- قسم الأذكار --------------------

elif st.session_state.page == "azkar":

    st.subheader("📿 الأذكار")

    if st.button("⬅️\nالرئيسية", key="azkar_home"):
        st.session_state.page = "home"
        st.rerun()

    azkar = {
        "أذكار الصباح": [
            "أصبحنا وأصبح الملك لله، والحمد لله.",
            "اللهم بك أصبحنا وبك أمسينا وبك نحيا وبك نموت وإليك النشور.",
            "رضيت بالله ربًا، وبالإسلام دينًا، وبمحمد ﷺ نبيًا.",
        ],
        "أذكار المساء": [
            "أمسينا وأمسى الملك لله، والحمد لله.",
            "اللهم بك أمسينا وبك أصبحنا وبك نحيا وبك نموت وإليك المصير.",
            "رضيت بالله ربًا، وبالإسلام دينًا، وبمحمد ﷺ نبيًا.",
        ],
        "أذكار متنوعة": [
            "سبحان الله وبحمده.",
            "أستغفر الله وأتوب إليه.",
            "لا حول ولا قوة إلا بالله.",
            "اللهم صل وسلم على نبينا محمد.",
        ],
    }

    category = st.selectbox(
        "اختار نوع الأذكار",
        list(azkar.keys()),
    )

    for zekr in azkar[category]:
        st.markdown(
            f"<div class='verse'>{zekr}</div>",
            unsafe_allow_html=True,
        )


# -------------------- قسم القرآن الكريم --------------------

elif st.session_state.page == "quran":

    st.subheader("📖 القرآن الكريم")

    if st.button("⬅️\nالرئيسية", key="quran_home"):
        st.session_state.page = "home"
        st.rerun()

    # زر اختيار القارئ الدائري داخل قسم القرآن
    st.markdown(
        "<p style='text-align:center'>🎙️ اختار القارئ المفضل</p>",
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1, 1])

    with center:
        if st.button("🎙️\nاختيار القارئ", key="quran_reader_button"):
            st.session_state.show_readers = (
                not st.session_state.show_readers
            )

    if st.session_state.show_readers:
        selected_reader = st.selectbox(
            "اختار القارئ",
            options=list(READERS.keys()),
            index=list(READERS.keys()).index(
                st.session_state.reader_name
            ),
            key="quran_reader_select",
        )

        st.session_state.reader_name = selected_reader

        if st.button("تم الاختيار", key="quran_reader_done"):
            st.session_state.show_readers = False
            st.rerun()

    st.caption(f"القارئ الحالي: {st.session_state.reader_name}")

    st.divider()

    @st.cache_data(ttl=3600)
    def get_surahs():
        response = requests.get(
            "https://api.alquran.cloud/v1/surah",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["data"]

    @st.cache_data(ttl=3600)
    def get_surah(surah_number):
        response = requests.get(
            f"https://api.alquran.cloud/v1/surah/{surah_number}/quran-uthmani",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["data"]

    try:
        surahs = get_surahs()

        surah_options = {
            f'{s["number"]}. {s["name"]}': s["number"]
            for s in surahs
        }

        selected_surah = st.selectbox(
            "اختار السورة",
            list(surah_options.keys()),
            key="surah_select",
        )

        surah_number = surah_options[selected_surah]
        surah_data = get_surah(surah_number)
        ayahs = surah_data["ayahs"]

        st.markdown(
            f"<h3 style='text-align:center'>{surah_data['name']}</h3>",
            unsafe_allow_html=True,
        )

        # تشغيل السورة بصوت القارئ المختار
        reader_id = READERS[st.session_state.reader_name]

        audio_url = (
            "https://cdn.islamic.network/quran/audio-surah/128/"
            f"{reader_id}/{surah_number}.mp3"
        )

        st.markdown("**🎧 استمع للسورة كاملة**")
        st.audio(audio_url)

        st.divider()

        # تقسيم الآيات إلى صفحات
        page_size = 20
        total_pages = math.ceil(len(ayahs) / page_size)
        page_key = f"ayah_page_{surah_number}"

        if page_key not in st.session_state:
            st.session_state[page_key] = 1

        st.session_state[page_key] = max(
            1,
            min(st.session_state[page_key], total_pages),
        )

        current_page = st.session_state[page_key]

        start = (current_page - 1) * page_size
        end = min(start + page_size, len(ayahs))

        for ayah in ayahs[start:end]:
            st.markdown(
                f"<div class='verse'>{ayah['text']} "
                f"<span style='color:#b8860b'>۞ "
                f"{ayah['numberInSurah']}</span></div>",
                unsafe_allow_html=True,
            )

        prev_col, info_col, next_col = st.columns([1, 1, 1])

        with prev_col:
            if st.button(
                "⬅️\nالسابق",
                key=f"prev_{surah_number}",
                disabled=current_page <= 1,
            ):
                st.session_state[page_key] -= 1
                st.rerun()

        with info_col:
            st.markdown(
                f"<p style='text-align:center'>"
                f"صفحة {current_page} من {total_pages}</p>",
                unsafe_allow_html=True,
            )

        with next_col:
            if st.button(
                "التالي\n➡️",
                key=f"next_{surah_number}",
                disabled=current_page >= total_pages,
            ):
                st.session_state[page_key] += 1
                st.rerun()

    except requests.RequestException:
        st.error(
            "تعذر تحميل القرآن الكريم. اتأكد من اتصال الإنترنت "
            "وحاول تاني."
        )
    except (KeyError, ValueError, TypeError):
        st.error("حصل خطأ أثناء تحميل بيانات السورة. حاول تاني.")


# -------------------- قسم المسبحة --------------------

elif st.session_state.page == "tasbeeh":

    st.subheader("🔢 المسبحة الإلكترونية")

    if st.button("⬅️\nالرئيسية", key="tasbeeh_home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(
        "<p style='text-align:center'>عدد التسبيحات</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='counter'>{st.session_state.tasbeeh_count}</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📿\nسبّح", key="tasbeeh_add"):
            st.session_state.tasbeeh_count += 1
            st.rerun()

    with col2:
        if st.button("🔄\nتصفير", key="tasbeeh_reset"):
            st.session_state.tasbeeh_count = 0
            st.rerun()

    st.markdown(
        "<div class='verse'>سبحان الله، والحمد لله، "
        "ولا إله إلا الله، والله أكبر</div>",
        unsafe_allow_html=True,
    )
