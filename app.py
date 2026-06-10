import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="Суреттегі кодты түсіндіргіш",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Python кодына автоматты түсіндірме")

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

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
            comment = "# Кітапхананы қосу"

        elif stripped.startswith("def "):
            comment = "# Функцияны анықтау"

        elif stripped.startswith("class "):
            comment = "# Класс құру"

        elif stripped.startswith("print("):
            comment = "# Нәтижені экранға шығару"

        elif stripped.startswith("if "):
            comment = "# Шартты тексеру"

        elif stripped.startswith("elif "):
            comment = "# Қосымша шарт"

        elif stripped.startswith("else"):
            comment = "# Әйтпесе"

        elif stripped.startswith("for "):
            comment = "# For циклі"

        elif stripped.startswith("while "):
            comment = "# While циклі"

        elif stripped.startswith("return"):
            comment = "# Нәтижені қайтару"

        elif "=" in stripped and not stripped.startswith("#"):
            comment = "# Айнымалыға мән беру"

        if comment:
            commented_lines.append(comment)

        commented_lines.append(line)

    return "\n".join(commented_lines)

st.subheader("📷 Кодтың суретін түсіріңіз")

photo = st.camera_input("Камераны ашу")

if photo is not None:

    image = Image.open(photo)

    st.image(image, caption="Түсірілген сурет")

    image_np = np.array(image)

    with st.spinner("Код оқылуда..."):

        result = reader.readtext(
            image_np,
            detail=0,
            paragraph=False
        )

        raw_code = "\n".join(result)

    if raw_code.strip():

        commented_code = generate_comments(raw_code)

        st.success("Код табылды")

        st.subheader("Оқылған код")
        st.code(raw_code, language="python")

        st.subheader("Комментарий қосылған код")
        st.code(commented_code, language="python")

        st.download_button(
            "💾 Python файлын жүктеу",
            commented_code,
            file_name="commented_code.py",
            mime="text/plain"
        )

    else:
        st.warning("Суреттен код табылмады")
