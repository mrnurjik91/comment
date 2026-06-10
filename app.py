import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# =====================================================
# БЕТ БАПТАУЛАРЫ
# =====================================================

st.set_page_config(
    page_title="Python кодын түсіндіргіш",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Python кодын суреттен оқу және түсіндіру")

st.markdown("""
### 📌 Қалай қолдану керек:
- 📁 Батырманы басыңыз
- Телефон өзі сізге таңдауды ұсынады:
  - 📷 Камера
  - 🖼️ Галерея
- Сурет жіберіңіз
- Жүйе Python кодын оқиды және түсіндіреді
""")

# =====================================================
# OCR МОДЕЛІ
# =====================================================

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

# =====================================================
# КОММЕНТАРИЙ ҚОСУ ФУНКЦИЯСЫ
# =====================================================

def generate_comments(raw_code):
    lines = raw_code.split("\n")
    result = []

    for line in lines:
        s = line.strip()
        comment = ""

        if not s:
            result.append(line)
            continue

        if s.startswith("import ") or s.startswith("from "):
            comment = "# 📦 Кітапхана қосу"

        elif s.startswith("def "):
            comment = "# ⚙️ Функция құру"

        elif s.startswith("class "):
            comment = "# 🏗️ Класс анықтау"

        elif s.startswith("print("):
            comment = "# 🖥️ Экранға шығару"

        elif s.startswith("input("):
            comment = "# ⌨️ Дерек енгізу"

        elif s.startswith("if "):
            comment = "# 🔀 Шарт тексеру"

        elif s.startswith("elif "):
            comment = "# 🔀 Қосымша шарт"

        elif s.startswith("else"):
            comment = "# 🔁 Әйтпесе"

        elif s.startswith("for "):
            comment = "# 🔄 Цикл (for)"

        elif s.startswith("while "):
            comment = "# 🔄 Цикл (while)"

        elif s.startswith("return"):
            comment = "# ↩️ Нәтиже қайтару"

        elif "=" in s and not s.startswith("#"):
            comment = "# 💾 Айнымалыға мән беру"

        if comment:
            result.append(comment)

        result.append(line)

    return "\n".join(result)

# =====================================================
# СУРЕТ ЖҮКТЕУ (КАМЕРА + ГАЛЕРЕЯ БІРДЕ)
# =====================================================

st.subheader("📁 Суретті таңдаңыз (Камера немесе Галерея)")

uploaded_file = st.file_uploader(
    "Файл таңдаңыз",
    type=["jpg", "jpeg", "png"]
)

# =====================================================
# ӨҢДЕУ
# =====================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Таңдалған сурет", use_container_width=True)

    image_np = np.array(image)

    with st.spinner("⏳ Код оқылуда..."):

        result = reader.readtext(
            image_np,
            detail=0,
            paragraph=False
        )

        raw_code = "\n".join(result)

    if raw_code.strip():

        commented = generate_comments(raw_code)

        st.success("✅ Код табылды")

        st.subheader("📄 OCR нәтижесі")
        st.code(raw_code, language="python")

        st.subheader("🤖 Түсіндірмесі бар код")
        st.code(commented, language="python")

        st.download_button(
            "💾 Python файлын жүктеу",
            commented,
            file_name="commented_code.py",
            mime="text/plain"
        )

    else:
        st.warning("⚠️ Суреттен код табылмады")
