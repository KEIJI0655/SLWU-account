import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="試験対策アプリ", layout="centered")
st.title("📱 PDF問題作成ツール")

# 以前のAPIキーを入力してください
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 【重要】無料枠で最も確実に動くフルネーム指定に変更
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        
        uploaded_file = st.file_uploader("試験の資料(PDF)を選択", type="pdf")

        if uploaded_file:
            if st.button("問題を5問作成する"):
                with st.spinner("PDFを読み込み中..."):
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    full_text = "".join([page.get_text() for page in doc])
                
                prompt = f"以下のテキストから3択問題を5問作り、最後に正解を書いてください。\n\n{full_text[:5000]}"
                
                with st.spinner("AIが考え中..."):
                    # 安全に生成を実行
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 作成された問題")
                    st.write(response.text)
                    
    except Exception as e:
        # 404が出る場合はここに理由が表示されます
        st.error(f"エラーが発生しました。APIキーまたはモデル設定を確認してください：\n{e}")
else:
    st.info("左側のメニューにAPIキーを入力してください。")
