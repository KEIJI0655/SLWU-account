import streamlit as st
import fitz
import google.generativeai as genai

st.title("📱 PDF問題作成ツール")

# 1. 鍵を入れる
key = st.sidebar.text_input("API Key", type="password")

if key:
    genai.configure(api_key=key)
    
    # 2. PDFを選ぶ
    file = st.file_uploader("PDFを選択", type="pdf")

    if file and st.button("問題を生成"):
        try:
            # 3. PDFの中身を読む
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join([p.get_text() for p in doc])
            
            # 4. モデル名を「gemini-1.5-flash」に固定（/などは一切入れない）
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 5. AIに頼む
            res = model.generate_content(f"以下から3択問題を5問作って。最後に正解を書いて。\n\n{text[:5000]}")
            st.write(res.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました。時間を置いて試すか、別のAPIキーを試してください：{e}")
else:
    st.info("左にAPIキーを入れてください")
