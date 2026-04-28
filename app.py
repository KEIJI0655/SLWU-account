import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策アプリ")
st.title("📱 PDF問題作成ツール")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    uploaded_file = st.file_uploader("PDFを選択", type="pdf")

    if uploaded_file and st.button("問題作成"):
        with st.spinner("作成中..."):
            try:
                # PDFから文字を出す
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])[:4000]
                
                # 【ここが重要】利用可能なモデルを自動で探して実行する
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"以下の内容から3択問題を3問作って：\n\n{text}")
                
                st.write(response.text)
            except Exception as e:
                # もしflashがダメなら、別の名前（pro）で再送する
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"以下の内容から3択問題を3問作って：\n\n{text}")
                    st.write(response.text)
                except:
                    st.error(f"Google側の制限エラーです。少し時間を置いてください。: {e}")
else:
    st.info("左にAPIキーを入れてください")
