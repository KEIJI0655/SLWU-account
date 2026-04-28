import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策アプリ")
st.title("📱 PDF問題作成ツール")

# 鍵を入力する場所
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # ここを「gemini-1.5-flash」だけにします（余計な/などをつけない）
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    uploaded_file = st.file_uploader("PDFを選択", type="pdf")

    if uploaded_file and st.button("問題を生成"):
        with st.spinner("作成中..."):
            try:
                # PDFから文字を出す
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])
                
                # AIに頼む
                response = model.generate_content(f"以下の内容から3択問題を5問作って。最後に正解を書いて。\n\n{text[:5000]}")
                
                st.markdown("### 📝 完成した問題")
                st.write(response.text)
            except Exception as e:
                st.error(f"エラー：{e}")
else:
    st.info("左にAPIキーを入れてください")
