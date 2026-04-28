import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策アプリ", layout="centered")
st.title("📱 PDF問題作成ツール")

api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    genai.configure(api_key=api_key)
    uploaded_file = st.file_uploader("試験の資料(PDF)を選択", type="pdf")

    if uploaded_file:
        if st.button("問題を5問作成する"):
            with st.spinner("PDFを読み込んでいます..."):
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = "".join([page.get_text() for page in doc])
            
            # 最もエラーが出にくい安定版のモデル名に変更
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"以下のテキストに基づいて、3択形式の試験問題を5問作成し、最後に正解を書いてください。\n\nテキスト：\n{full_text[:10000]}"
            
            with st.spinner("AIが問題を考えています..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 作成された問題")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"エラーが発生しました。APIキーを確認してください: {e}")
else:
    st.warning("左側のメニューからAPIキーを入力してください。")
