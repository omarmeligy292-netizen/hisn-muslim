
import streamlit as st

# =====================================
# إعدادات التطبيق
# =====================================
st.set_page_config(
    page_title="حصن المسلم",
    page_icon="🌙",
    layout="centered"
)

# =====================================
# الألوان
# =====================================
GREEN = "#123F35"
LIGHT_GREEN = "#1C5949"
GOLD = "#E8C878"
CREAM = "#F7F4EA"

# =====================================
# الأذكار
# =====================================
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

# =====================================
# حالة التطبيق
# =====================================
DEFAULTS = {
    "page": "home",
    "items": [],
    "index": 0,
    "count": 0,
    "current_name": "",
    "tasbeeh_count": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================
# التصميم
# =====================================
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
    max-width: 750px;
    padding-top: 2rem;
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
.zikr-card {
    background: #FFFFFF;
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
    min-height: 48px;
    width: 100%;
    font-size: 18px;
}
.stButton > button:hover {
    background-color: #E8C878;
    color: #123F35;
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


# =====================================
# وظائف التنقل والعداد
# =====================================
def home():
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

    if not isinstance(index, int) or not isinstance(count, int):
        return

    if index < 0 or index >= len(items):
        return

    zikr, target = items[index]

    if count + 1 >= target:
        st.session_state["index"] = index + 1
        st.session_state["count"] = 0
    else:
        st.session_state["count"] = count + 1


# =====================================
# عنوان التطبيق
# =====================================
st.markdown(
    "<h1>🌙 حِصْنُ المُسْلِم</h1>",
    unsafe_allow_html=True
)


# =====================================
# الصفحة الرئيسية
# =====================================
page = st.session_state.get("page", "home")

if page == "home":

    st.markdown("### أذكارك اليومية وطمأنينة قلبك")

    for name in AZKAR:
        if st.button(
            name,
            key=f"open_{name}",
            use_container_width=True
        ):
            open_azkar(name)

    if st.button(
        "📿 السبحة الإلكترونية",
        key="open_tasbeeh",
        use_container_width=True
    ):
        st.session_state["page"] = "tasbeeh"
        st.rerun()

    st.markdown(
        '<div class="footer">نسأل الله أن ينفعنا وإياكم 🤍</div>',
        unsafe_allow_html=True
    )


# =====================================
# صفحة الأذكار
# =====================================
elif page == "azkar":

    items = st.session_state.get("items", [])
    index = st.session_state.get("index", 0)
    count = st.session_state.get("count", 0)
    current_name = st.session_state.get("current_name", "")

    st.subheader(current_name)

    # فحص البيانات قبل عرض الذكر
    if not isinstance(items, list):
        st.error("بيانات الأذكار غير صالحة. ارجع للرئيسية.")
        if st.button("العودة للرئيسية"):
            home()

    elif not isinstance(index, int) or isinstance(index, bool):
        st.session_state["index"] = 0
        st.session_state["count"] = 0
        st.rerun()

    elif not items:

        st.warning("مفيش أذكار للعرض حاليًا.")

        if st.button("العودة للرئيسية", key="empty_back"):
            home()

    elif index < 0:

        st.session_state["index"] = 0
        st.session_state["count"] = 0
        st.rerun()

    elif index >= len(items):

        st.success("أحسنت! أتممت هذه الأذكار 🌿")

        if st.button("العودة للرئيسية", key="finished_back"):
            home()

        if st.button("تكرار الأذكار من البداية", key="restart_azkar"):
            open_azkar(current_name)

    else:

        zikr, target = items[index]

        if not isinstance(count, int) or isinstance(count, bool):
            st.session_state["count"] = 0
            st.rerun()

        st.markdown(
            f'<div class="zikr-card">{zikr}</div>',
            unsafe_allow_html=True
        )

        st.progress(min(count / target, 1.0))

        st.markdown(f"**التكرار: {count} / {target}**")
        st.caption(f"الذكر {index + 1} من {len(items)}")

        if st.button(
            "✓ تم الذكر",
            key="repeat_zikr",
            use_container_width=True
        ):
            repeat_zikr()
            st.rerun()

        if st.button("العودة للرئيسية", key="back_from_azkar"):
            home()


# =====================================
# صفحة السبحة الإلكترونية
# =====================================
elif page == "tasbeeh":

    st.subheader("📿 السبحة الإلكترونية")

    tasbeeh_count = st.session_state.get("tasbeeh_count", 0)

    if not isinstance(tasbeeh_count, int) or isinstance(tasbeeh_count, bool):
        tasbeeh_count = 0
        st.session_state["tasbeeh_count"] = 0

    st.markdown(
        f'<div class="counter">{tasbeeh_count}</div>',
        unsafe_allow_html=True
    )

    st.markdown("### سبحان الله")

    if st.button(
        "تسبيح +1",
        key="increment_tasbeeh",
        use_container_width=True
    ):
        st.session_state["tasbeeh_count"] += 1
        st.rerun()

    if st.button(
        "تصفير العداد",
        key="reset_tasbeeh",
        use_container_width=True
    ):
        st.session_state["tasbeeh_count"] = 0
        st.rerun()

    if st.button("العودة للرئيسية", key="back_from_tasbeeh"):
        home()


# =====================================
# أي صفحة غير معروفة
# =====================================
else:
    st.session_state["page"] = "home"
    st.rerun()
