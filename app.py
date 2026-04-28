import streamlit as st
import fitz  # PDF読み込み用
import google.generativeai as genai

# --- アプリの設定 ---
st.set_page_config(page_title="試験対策アプリ", layout="centered")
st.title("📱 PDF問題作成ツール")

# APIキーの設定（後でアプリの設定画面に入力します）
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # PDFのアップロード
    uploaded_file = st.file_uploader("試験の資料(PDF)を選択", type="pdf")

    if uploaded_file:
        with st.spinner("PDFを読み込んでいます..."):
            # PDFからテキストを抽出
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            full_text = "".join([page.get_text() for page in doc])
            
        if st.button("問題を5問作成する"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            # AIへの具体的な指示
            prompt = f"""
            以下のテキストに基づいて、会社の試験対策用問題を5問作成してください。
            【条件】
            ・3択形式にすること
            ・最後にまとめて正解を記載すること
            ・専門用語も適切に含めること
            
            テキスト：
            {full_text[:10000]}  # 読み込みすぎ防止
            """
            
            with st.spinner("AIが問題を考えています..."):
                response = model.generate_content(prompt)
                st.markdown("### 📝 作成された問題")
                st.write(response.text)
else:
    st.warning("左側のメニューからAPIキーを入力してください。")
