import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# =====================================================
# БЕТ БАПТАУЛАРЫ
# =====================================================

st.set_page_config(
    page_title="Суреттегі кодты түсіндіргіш",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Python кодына автоматты түсіндірме жазу панелі")

st.write("""
🧑‍🏫 **Нұсқаулық:**
1. Камераны қосыңыз немесе файл жүктеңіз.
2. Код жазылған парақты түсіріңіз.
3. Жүйе кодты оқып, әр жолына қазақша түсіндірме қосады.
""")

# =====================================================
# OCR МОДЕЛІ
# =====================================================

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['en'])

try:
    reader = load_ocr_model()
except Exception as e:
    st.error(f"OCR моделін жүктеу қатесі: {e}")
    st.stop()

# =====================================================
# КОММЕНТАРИЙ ҚОСУ ФУНКЦИЯСЫ
# =====================================================

def generate_comments(raw_code):
    lines = raw_code.split('\n')
    commented_lines = []

    for line in lines:
        stripped = line.strip()
        comment = ""

        if not stripped:
            commented_lines.append(line)
            continue

        if stripped.startswith("import ") or stripped.startswith("from "):
            comment = "# 📦 Қажетті кітапхананы қосу"

        elif stripped.startswith("def "):
            comment = "# ⚙️ Функцияны жариялау"

        elif stripped.startswith("class "):
            comment = "# 🏗️ Класс құру"

        elif stripped.startswith("print("):
            comment = "# 🖥️ Нәтижені экранға шығару"

        elif stripped.startswith("input("):
            comment = "# ⌨️ Пайдаланушыдан мәлімет енгізу"

        elif stripped.startswith("if "):
            comment = "# 🔀 Шартты тексеру"

        elif stripped.startswith("elif "):
            comment = "# 🔀 Қосымша шартты тексеру"

        elif stripped.startswith("else:"):
            comment = "# 🔁 Әйтпесе"

        elif stripped.startswith("for "):
            comment = "# 🔄 For циклін орындау"

        elif stripped.startswith("while "):
            comment = "# 🔄 While циклін орындау"

        elif stripped.startswith("return "):
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

source = st.radio(
    "Сурет көзін таңдаңыз:",
    ["📷 Камера", "📁 Файл"]
)

uploaded_file = None

if source == "📷 Камера":
    uploaded_file = st.camera_input(
        "Код жазылған парақты түсіріңіз"
    )

else:
    uploaded_file = st.file_uploader(
        "Код суретін таңдаңыз",
        type=["jpg", "jpeg", "png"]
    )

# =====================================================
# ӨҢДЕУ
# =====================================================

if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Жүктелген сурет",
            use_container_width=True
        )

        with st.spinner("⏳ Код оқылып жатыр..."):

            image_np = np.array(image)

            result = reader.readtext(
                image_np,
                detail=0,
                paragraph=False
            )

            raw_code = "\n".join(result)

            if not raw_code.strip():
                st.warning(
                    "⚠️ Суреттен код табылмады. Анық сурет жүктеп көріңіз."
                )

            else:

                final_code = generate_comments(raw_code)

                st.success(
                    "✅ Код сәтті оқылды және комментарий қосылды!"
                )

                st.subheader("📄 OCR арқылы оқылған код")

                st.code(
                    raw_code,
                    language="python"
                )

                st.subheader(
                    "🤖 Автоматты түсіндірме қосылған нұсқа"
                )

                st.code(
                    final_code,
                    language="python"
                )

                st.download_button(
                    label="💾 .py файлын жүктеу",
                    data=final_code,
                    file_name="commented_code.py",
                    mime="text/x-python"
                )

    except Exception as e:
        st.error(
            f"❌ Өңдеу барысында қате пайда болды: {e}"
        )
