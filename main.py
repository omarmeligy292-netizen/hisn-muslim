
import math
import requests
import streamlit as st

st.set_page_config(
    page_title="Hisn al-Muslim | حصن المسلم",
    page_icon="📿",
    layout="centered",
)

API = "https://api.alquran.cloud/v1"
CDN_INFO = "https://cdn.islamic.network/quran/info/by-surah/info.json"

# -------------------- التصميم والعلامة المائية --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fffdf5, #fff5d6);
    color: #5c4510;
}

/* العلامة المائية: شعار درع + اسم التطبيق */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: 0.25;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='360' height='250' viewBox='0 0 360 250'%3E%3Cg transform='rotate(-24 180 125)' fill='none' stroke='%23b8860b' stroke-width='2'%3E%3Cpath d='M180 45 L207 56 L204 84 Q199 104 180 115 Q161 104 156 84 L153 56 Z'/%3E%3Cpath d='M167 78 L177 88 L194 68' stroke-width='3'/%3E%3C/g%3E%3Ctext x='180' y='145' font-family='Arial,sans-serif' font-size='17' font-weight='bold' text-anchor='middle' fill='%23b8860b' transform='rotate(-24 180 145)'%3EHisn al-Muslim%3C/text%3E%3Ctext x='180' y='170' font-family='Arial,sans-serif' font-size='12' text-anchor='middle' fill='%23b8860b' transform='rotate(-24 180 170)'%3EOMAR MELIGY%3C/text%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 360px 250px;
}

/* إبقاء محتوى التطبيق فوق العلامة المائية */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stBottom"],
[data-testid="stSidebar"] {
    position: relative;
    z-index: 1;
    background-color: transparent;
}

h1, h2, h3, p, label {
    color: #72520c;
}

div.stButton > button {
    width: 105px;
    height: 105px;
    min-height: 105px;
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
    background: rgba(255, 250, 240, 0.92);
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
        width: 85px;
        height: 85px;
        min-height: 85px;
        font-size: 12px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- بيانات القرآن والقراء --------------------

@st.cache_data(ttl=3600)
def get_surahs():
    response = requests.get(f"{API}/surah", timeout=20)
    response.raise_for_status()
    return response.json()["data"]


@st.cache_data(ttl=3600)
def get_audio_editions():
    response = requests.get(
        f"{API}/edition/format/audio",
        timeout=20,
    )
    response.raise_for_status()

    editions = response.json()["data"]
    return {
        edition["identifier"]: edition.get(
            "name", edition["identifier"]
        )
        for edition in editions
        if edition.get("language") == "ar"
    }


@st.cache_data(ttl=3600)
def get_surah_audio_availability():
    """يفهرس الملفات الصوتية المتاحة حسب القارئ والسورة."""
    response = requests.get(CDN_INFO, timeout=30)
    response.raise_for_status()
    tree = response.json()

    availability = {}

    def walk(node, bitrate=None, edition=None):
        if not isinstance(node, dict):
            return

        node_type = node.get("type")
        name = node.get("name", "")

        if node_type == "directory":
            new_bitrate = bitrate
            new_edition = edition

            if name.isdigit() and int(name) in (
                32, 40, 48, 64, 128, 192
            ):
                new_bitrate = int(name)
                new_edition = None
            elif new_bitrate is not None and name.startswith("ar."):
                new_edition = name

            for child in node.get("contents", []):
                walk(child, new_bitrate, new_edition)

        elif node_type == "file" and edition and bitrate:
            if name.endswith(".mp3"):
                try:
                    surah_number = int(name[:-4])
                except ValueError:
                    return

                if 1 <= surah_number <= 114:
                    files = availability.setdefault(edition, {})
                    old_bitrate = files.get(surah_number, 0)

                    if bitrate > old_bitrate:
                        files[surah_number] = bitrate

    if isinstance(tree, list):
        for item in tree:
            walk(item)
    else:
        walk(tree)

    return availability


@st.cache_data(ttl=3600)
def get_surah_text(number):
    response = requests.get(
        f"{API}/surah/{number}/quran-uthmani",
        timeout=20,
    )
    response.raise_for_status()
    return response.json()["data"]


# -------------------- حالة التطبيق --------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "show_readers" not in st.session_state:
    st.session_state.show_readers = False

if "reader_id" not in st.session_state:
    st.session_state.reader_id = "ar.alafasy"

if "tasbeeh_count" not in st.session_state:
    st.session_state.tasbeeh_count = 0


def home_button(key):
    if st.button("⬅️\nالرئيسية", key=key):
        st.session_state.page = "home"
        st.rerun()


# -------------------- العنوان --------------------

st.markdown(
    "<h1 style='text-align:center'>📿 حصن المسلم</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center'>"
    "أذكارك وقرآنك في مكان واحد"
    "</p>",
    unsafe_allow_html=True,
)


# -------------------- الرئيسية --------------------

if st.session_state.page == "home":
    st.subheader("🌙 اختر القسم")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("📿\nالأذكار", key="home_azkar"):
            st.session_state.page = "azkar"
            st.rerun()

    with c2:
        if st.button("📖\nالقرآن الكريم", key="home_quran"):
            st.session_state.page = "quran"
            st.rerun()

    with c3:
        if st.button("🔢\nالمسبحة", key="home_tasbeeh"):
            st.session_state.page = "tasbeeh"
            st.rerun()

    st.caption("Hisn al-Muslim • OMAR MELIGY")


# -------------------- الأذكار --------------------

elif st.session_state.page == "azkar":
    st.subheader("📿 الأذكار")
    home_button("azkar_home")

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


# -------------------- القرآن الكريم --------------------

elif st.session_state.page == "quran":
    st.subheader("📖 القرآن الكريم")
    home_button("quran_home")

    try:
        surahs = get_surahs()
        editions = get_audio_editions()
        availability = get_surah_audio_availability()

        surah_names = {
            f'{s["number"]}. {s["name"]}': s["number"]
            for s in surahs
        }

        selected_surah = st.selectbox(
            "اختار السورة",
            list(surah_names.keys()),
            key="quran_surah",
        )

        surah_number = surah_names[selected_surah]

        available_readers = {
            edition_id: editions[edition_id]
            for edition_id, files in availability.items()
            if surah_number in files and edition_id in editions
        }

        st.markdown("### 🎙️ القارئ المفضل")

        a, b, c = st.columns([1, 1, 1])

        with b:
            if st.button(
                "🎙️\nاختيار القارئ",
                key="reader_button",
            ):
                st.session_state.show_readers = (
                    not st.session_state.show_readers
                )

        if not available_readers:
            st.warning(
                "لم يتم العثور على تسجيل متاح لهذه السورة "
                "في مصدر الصوت الحالي."
            )
        else:
            reader_ids = list(available_readers.keys())

            if st.session_state.reader_id not in reader_ids:
                st.session_state.reader_id = reader_ids[0]

            if st.session_state.show_readers:
                selected_reader_id = st.selectbox(
                    "اختار القارئ المتاح للسورة",
                    options=reader_ids,
                    format_func=lambda rid: available_readers[rid],
                    index=reader_ids.index(st.session_state.reader_id),
                    key="reader_choice",
                )

                st.session_state.reader_id = selected_reader_id

                if st.button("تم الاختيار", key="reader_done"):
                    st.session_state.show_readers = False
                    st.rerun()

            reader_id = st.session_state.reader_id
            bitrate = availability[reader_id][surah_number]

            st.caption(
                f"القارئ الحالي: {available_readers[reader_id]}"
            )

            audio_url = (
                "https://cdn.islamic.network/quran/audio-surah/"
                f"{bitrate}/{reader_id}/{surah_number}.mp3"
            )

            st.markdown("**🎧 استمع للسورة كاملة**")
            st.audio(audio_url)

        st.divider()

        surah_data = get_surah_text(surah_number)
        ayahs = surah_data["ayahs"]

        st.markdown(
            f"<h3 style='text-align:center'>{surah_data['name']}</h3>",
            unsafe_allow_html=True,
        )

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

        p1, p2, p3 = st.columns([1, 1, 1])

        with p1:
            if st.button(
                "⬅️\nالسابق",
                key=f"prev_{surah_number}",
                disabled=current_page <= 1,
            ):
                st.session_state[page_key] -= 1
                st.rerun()

        with p2:
            st.markdown(
                f"<p style='text-align:center'>"
                f"{current_page} / {total_pages}</p>",
                unsafe_allow_html=True,
            )

        with p3:
            if st.button(
                "التالي\n➡️",
                key=f"next_{surah_number}",
                disabled=current_page >= total_pages,
            ):
                st.session_state[page_key] += 1
                st.rerun()

    except requests.RequestException:
        st.error(
            "تعذر الاتصال بمصدر القرآن أو الصوت. "
            "تأكد من الإنترنت وحاول مرة أخرى."
        )
    except (KeyError, ValueError, TypeError, IndexError):
        st.error(
            "حصل خطأ أثناء تحميل بيانات السورة أو القراء. "
            "جرّب تحديث الصفحة."
        )


# -------------------- المسبحة --------------------

elif st.session_state.page == "tasbeeh":
    st.subheader("🔢 المسبحة الإلكترونية")
    home_button("tasbeeh_home")

    st.markdown(
        "<p style='text-align:center'>عدد التسبيحات</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='counter'>{st.session_state.tasbeeh_count}</div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button("📿\nسبّح", key="tasbeeh_add"):
            st.session_state.tasbeeh_count += 1
            st.rerun()

    with c2:
        if st.button("🔄\nتصفير", key="tasbeeh_reset"):
            st.session_state.tasbeeh_count = 0
            st.rerun()

    st.markdown(
        "<div class='verse'>سبحان الله، والحمد لله، "
        "ولا إله إلا الله، والله أكبر</div>",
        unsafe_allow_html=True,
    )

    st.caption("Hisn al-Muslim • OMAR MELIGY")
