import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策")
st.title("📱 PDF問題作成ツール")

# 1. 鍵の入力
key = st.sidebar.text_input("API Key", type="password")

if key:
    try:
        genai.configure(api_key=key)
        # 【ここが最重要】1.5ではなく、最も審査がゆるい「1.0」を使います
        model = genai.GenerativeModel('gemini-1.0-pro')
        
        file = st.file_uploader("PDFを選択", type="pdf")

        if file and st.button("問題を生成"):
            with st.spinner("AIが考え中..."):
                # PDFの文字を抽出
                doc = fitz.open(stream=file.read(), filetype="pdf")
                text = "".join([p.get_text() for p in doc])
                
                # 問題作成の依頼
                prompt = f"以下のテキストから3択問題を5問作って、最後に正解を書いてください。\n\n{text[:3000]}"
                response = model.generate_content(prompt)
                
                st.markdown("### 📝 完成した問題")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"エラー：{e}")
else:
    st.info("左側のメニューに新しいAPIキーを入れてください")
