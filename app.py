import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策")
st.title("📱 PDF問題作成ツール")

# 鍵の入力
key = st.sidebar.text_input("API Key", type="password")

if key:
    genai.configure(api_key=key)
    # 【ここが重要】絶対に拒否されない最も古いモデル名にします
    model = genai.GenerativeModel('gemini-pro')
    
    file = st.file_uploader("PDFを選択", type="pdf")

    if file and st.button("問題を生成"):
        with st.spinner("作成中..."):
            try:
                # PDFを読み込む
                doc = fitz.open(stream=file.read(), filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text()
                
                # AIに指示
                prompt = f"以下の内容から3択問題を3問作って。最後に正解を書いて。\n\n{text[:3000]}"
                response = model.generate_content(prompt)
                
                st.write(response.text)
            except Exception as e:
                # エラーが出たら内容を出す
                st.error(f"エラー：{e}")
else:
    st.info("左にAPIキーを入れてください")
