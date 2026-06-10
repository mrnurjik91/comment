import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# 1. Веб-беттің негізгі баптаулары
st.set_page_config(
    page_title="Суреттегі кодты түсіндіргіш", 
    page_icon="🤖", 
    layout="centered"
)

st.title("🤖 Python Кодына Автоматты Түсіндірме Жазу Панелі")
st.write("🧑‍🏫 **Нұсқаулық:** Оқушының код жазылған 1 суретін жүктеңіз. Жүйе кодты оқып, оның әр жолына қазақша түсіндірме (комментарий) қосып береді.")

# 2. OCR модельді іске қосу (Кэштеледі)
@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['en'])

try:
    reader = load_ocr_model()
except Exception as e:
    st.error(f"OCR Моделін жүктеу қатесі: {e}")

# 3. Код жолдарын автоматты талдау және түсіндіру функциясы
def generate_comments(raw_code):
    lines = raw_code.split('\n')
    commented_lines = []
    
    # Қарапайым ережелер жинағы (Кодты талдау үшін)
    for line in lines:
        stripped = line.strip()
        comment = ""
        
        if not stripped:
            commented_lines.append(line)
            continue
            
        # Кодтың мағынасына қарай қазақша түсініктеме таңдау
        if stripped.startswith("import ") or stripped.startswith("from "):
            comment = "# 📦 Қажетті кітапхананы (модульді) бағдарламаға қосу"
        elif stripped.startswith("def "):
            comment = "# ⚙️ Жаңа функция жариялау (құру)"
        elif stripped.startswith("print("):
            comment = "# 🖥️ Нәтижені немесе мәтінді экранға шығару"
        elif stripped.startswith("if ") or stripped.startswith("elif "):
            comment = "# 🔀 Шартты тексеру (Егер шарт орындалса...)"
        elif stripped.startswith("else:"):
            comment = "# 🔁 Әйтпесе (жоғарыдағы шарттар орындалмаған жағдайда)"
        elif stripped.startswith("for ") or stripped.startswith("while "):
            comment = "# 🔄 Циклды іске қосу (әрекетті бірнеше рет қайталау)"
        elif "=" in stripped and not stripped.startswith("#"):
            comment = "# 💾 Айнымалы мәнін беру немесе есептеу жүргізу"
        elif stripped.startswith("return "):
            comment = "# ↩️ Функцияның жұмыс нәтижесін кері қайтару"
        elif stripped.startswith("#"):
            comment = "" # Егер кодта онсыз да комментарий болса, тиіспейміз
            
        # Егер түсіндірме табылса, оны код жолының үстіне қосамыз
        if comment:
            commented_lines.append(comment)
        commented_lines.append(line)
        
    return "\n".join(commented_lines)

# 4. Файлды қабылдау бөлімі
uploaded_file = st.file_uploader(
    "Оқушының код түсірілген суретін таңдаңыз (1 сурет)", 
    type=["jpg", "png", "jpeg"]
)

# 5. Басты логика
if uploaded_file:
    st.image(uploaded_file, caption="Жүктелген сурет", use_container_width=True)
    
    with st.spinner("⏳ Суреттен код оқылып, түсіндірме дайындалуда..."):
        try:
            # Суретті өңдеу
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            # OCR арқылы кодты мәтінге айналдыру
            result = reader.readtext(image_np, detail=0)
            raw_code = "\n".join(result)
            
            if raw_code.strip() == "":
                st.warning("⚠️ Суреттен ешқандай код табылмады. Суреттің анық екеніне көз жеткізіңіз.")
            else:
                # Оқушының атын файл атауынан алу
                student_name = uploaded_file.name.split('.')[0]
                
                # Түсіндірме қосылған кодты жасау
                final_code = generate_comments(raw_code)
                
                # Нәтижені көрсету
                st.success("✅ Код сәтті оқылды және түсіндірме дайын болды!")
                
                st.subheader(f"👤 {student_name} коды (Автоматты комментариймен):")
                st.code(final_code, language="python")
                
                # Дайын файлды жүктеп алу батырмасы
                st.download_button(
                    label="💾 Комментарийленген кодты (.py) жүктеп алу",
                    data=final_code,
                    file_name=f"{student_name}_commented.py",
                    mime="text/x-python"
                )
                
        except Exception as e:
            st.error(f"❌ Файлды өңдеу барысында қате кетті: {e}")
