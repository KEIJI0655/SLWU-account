import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策アプリ", layout="centered")
st.title("📱 PDF問題作成ツール")

# 以前のAPIキーを入力
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    try:
        # APIの設定
        genai.configure(api_key=api_key)
        
        # 【重要】バージョンをbetaではなく安定版として扱う指定
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        
        uploaded_file = st.file_uploader("PDFを選択", type="pdf")

        if uploaded_file:
            if st.button("問題を生成する"):
                with st.spinner("PDF読み込み中..."):
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    full_text = ""
                    for page in doc:
                        full_text += page.get_text()
                
                prompt = f"以下のテキストから3択問題を5問作成し、最後に正解を書いてください。\n\n{full_text[:8000]}"
                
                with st.spinner("AIが考え中..."):
                    # 生成
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 完成！")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"エラー内容: {e}")
else:
    st.info("左側のメニューにAPIキーを貼り付けてください。")
