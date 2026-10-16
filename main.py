
import streamlit as st

st.set_page_config(
    page_title="حصن المسلم",
    page_icon="🌙",
    layout="centered"
)

GREEN = "#123F35"
LIGHT_GREEN = "#1C5949"
GOLD = "#E8C878"
CREAM = "#F7F4EA"

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
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3, p, div, label {
    text-align: center;
}
h1 {
    color: #E8C878 !important;
    background: #123F35;
    padding: 22px 10px;
    border-radius: 15px;
}
.zikr-card {
    background: white;
    border: 2px solid #E8C878;
    border-radius: 18px;
    padding: 28px 20px;
    margin: 20px 0;
    color: #123F35;
    font-size: 25px;
    line-height: 2;
    text-align: center;
    direction: rtl;
}
.stButton > button {
    background-color: #1C5949;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    min-height: 48px;
    width: 100%;
    font-size: 18px;
}
.stButton > button:hover {
    background-color: #E8C878;
    color: #123F35;
    border: none;
}
.counter {
    color: #123F35;
    font-size: 56px;
    font-weight: bold;
    text-align: center;
    padding: 15px;
}
.footer {
    color: #1C5949;
    text-align: center;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)

# تهيئة حالة التطبيق
defaults = {
    "page": "home",
    "items": [],
    "index": 0,
    "count": 0,
    "current_name": "",
    "tasbeeh_count": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def home():
    st.session_state.page = "home"
    st.rerun()


def open_azkar(name):
    st.session_state.current_name = name
    st.session_state.items = AZKAR[name]
    st.session_state.index = 0
    st.session_state.count = 0
    st.session_state.page = "azkar"
    st.rerun()


def repeat_zikr():
    _, target = st.session_state.items[
        st.session_state.index
    ]

    if st.session_state.count + 1 >= target:
        st.session_state.index += 1
        st.session_state.count = 0
    else:
        st.session_state.count += 1


# عنوان التطبيق
st.markdown("<h1>🌙 حِصْنُ المُسْلِم</h1>",
            unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown("### أذكارك اليومية وطمأنينة قلبك")

    for name in AZKAR:
        if st.button(name, key=f"azkar_{name}",
                     use_container_width=True):
            open_azkar(name)

    if st.button("📿 السبحة الإلكترونية",
                 use_container_width=True):
        st.session_state.page = "tasbeeh"
        st.rerun()

    st.markdown(
        '<div class="footer">نسأل الله أن ينفعنا وإياكم 🤍</div>',
        unsafe_allow_html=True
    )

elif st.session_state.page == "azkar":
    items = st.session_state.items
    index = st.session_state.index

    st.subheader(st.session_state.current_name)

    if index >= len(items):
        st.success("أحسنت! أتممت هذه الأذكار 🌿")

        if st.button("العودة للرئيسية"):
            home()
    else:
        zikr, target = items[index]

        st.markdown(
            f'<div class="zikr-card">{zikr}</div>',
            unsafe_allow_html=True
        )

        st.progress(st.session_state.count / target)

        st.markdown(
            f"**التكرار: {st.session_state.count} / {target}**"
        )

        st.caption(f"الذكر {index + 1} من {len(items)}")

        if st.button("✓ تم الذكر", use_container_width=True):
            repeat_zikr()
            st.rerun()

        if st.button("العودة للرئيسية"):
            home()

elif st.session_state.page == "tasbeeh":
    st.subheader("📿 السبحة الإلكترونية")

    st.markdown(
        f'<div class="counter">{st.session_state.tasbeeh_count}</div>',
        unsafe_allow_html=True
    )

    st.markdown("### سبحان الله")

    if st.button("تسبيح +1", use_container_width=True):
        st.session_state.tasbeeh_count += 1
        st.rerun()

    if st.button("تصفير العداد", use_container_width=True):
        st.session_state.tasbeeh_count = 0
        st.rerun()

    if st.button("العودة للرئيسية"):
        home()
