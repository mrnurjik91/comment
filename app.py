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

st.title("🤖 Python кодына автоматты түсіндірме")
st.markdown("""
### Нұсқаулық
- 📷 Камерамен сурет түсіруге болады
- 📁 Дайын суретті жүктеуге болады
- Жүйе Python кодын оқиды
- Әр жолға қазақша түсіндірме қосады
- Дайын .py файлын жүктеп алуға болады
""")

# =====================================================
# OCR МОДЕЛІ
# =====================================================

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

try:
    reader = load_ocr()
except Exception as e:
    st.error(f"OCR моделін жүктеу қатесі: {e}")
    st.stop()

# =====================================================
# КОММЕНТАРИЙ ҚОСУ ФУНКЦИЯСЫ
# =====================================================

def generate_comments(raw_code):
    lines = raw_code.split("\n")
    commented_lines = []

    for line in lines:

        stripped = line.strip()
        comment = ""

        if not stripped:
            commented_lines.append(line)
            continue

        if stripped.startswith("import ") or stripped.startswith("from "):
            comment = "# 📦 Кітапхананы бағдарламаға қосу"

        elif stripped.startswith("class "):
            comment = "# 🏗️ Класс жариялау"

        elif stripped.startswith("def "):
            comment = "# ⚙️ Функция жариялау"

        elif stripped.startswith("print("):
            comment = "# 🖥️ Нәтижені экранға шығару"

        elif stripped.startswith("input("):
            comment = "# ⌨️ Пайдаланушыдан дерек енгізу"

        elif stripped.startswith("if "):
            comment = "# 🔀 Шартты тексеру"

        elif stripped.startswith("elif "):
            comment = "# 🔀 Қосымша шартты тексеру"

        elif stripped.startswith("else"):
            comment = "# 🔁 Әйтпесе"

        elif stripped.startswith("for "):
            comment = "# 🔄 For циклі"

        elif stripped.startswith("while "):
            comment = "# 🔄 While циклі"

        elif stripped.startswith("return"):
            comment = "# ↩️ Нәтижені қайтару"

        elif "=" in stripped and not stripped.startswith("#"):
            comment = "# 💾 Айнымалыға мән беру"

        if comment:
            commented_lines.append(comment)

        commented_lines.append(line)

    return "\n".join(commented_lines)

# =====================================================
# СУРЕТ КӨЗІН ТАҢДАУ
# =====================================================

st.subheader("📥 Код суретін енгізу")

source = st.radio(
    "Тәсілді таңдаңыз:",
    ["📷 Камера", "📁 Файл жүктеу"]
)

uploaded_file = None

if source == "📷 Камера":
    uploaded_file = st.camera_input(
        "Кодтың суретін түсіріңіз"
    )

elif source == "📁 Файл жүктеу":
    uploaded_file = st.file_uploader(
        "Суретті таңдаңыз",
        type=["jpg", "jpeg", "png"]
    )

# =====================================================
# OCR ӨҢДЕУ
# =====================================================

if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Жүктелген сурет",
            use_container_width=True
        )

        image_np = np.array(image)

        with st.spinner("⏳ Код оқылып жатыр..."):

            result = reader.readtext(
                image_np,
                detail=0,
                paragraph=False
            )

            raw_code = "\n".join(result)

        if raw_code.strip() == "":
            st.warning(
                "⚠️ Суреттен код анықталмады."
            )

        else:

            commented_code = generate_comments(raw_code)

            st.success(
                "✅ Код сәтті оқылды!"
            )

            st.subheader("📄 OCR арқылы анықталған код")

            st.code(
                raw_code,
                language="python"
            )

            st.subheader(
                "🤖 Қазақша түсіндірмелері бар код"
            )

            st.code(
                commented_code,
                language="python"
            )

            st.download_button(
                label="💾 .py файлын жүктеу",
                data=commented_code,
                file_name="commented_code.py",
                mime="text/x-python"
            )

    except Exception as e:
        st.error(
            f"❌ Қате пайда болды: {e}"
        )

# =====================================================
# АЯҚТАЛДЫ
# =====================================================

st.markdown("---")
st.caption("Python кодтарын автоматты түсіндіру жүйесі")
