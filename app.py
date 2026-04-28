import streamlit as st
import fitz
import google.generativeai as genai

# アプリの基本設定
st.set_page_config(page_title="試験対策アプリ", layout="centered")
st.title("📱 PDF問題作成ツール")

# APIキーの入力
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    try:
        # APIの初期設定
        genai.configure(api_key=api_key)
        
        # 【重要】最も安定している旧モデル名を直接指定
        model = genai.GenerativeModel('gemini-pro')
        
        uploaded_file = st.file_uploader("試験の資料(PDF)を選択", type="pdf")

        if uploaded_file:
            if st.button("問題を5問作成する"):
                with st.spinner("PDFを解析中..."):
                    # PDF読み込み
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    text_list = []
                    for page in doc:
                        text_list.append(page.get_text())
                    full_text = "\n".join(text_list)
                
                # AIへの指示（プロンプト）
                prompt = f"以下のテキストの内容から、3択のクイズを5問作成してください。最後に正解を一覧で表示してください。\n\n資料テキスト:\n{full_text[:3000]}"
                
                with st.spinner("AIが問題を生成中..."):
                    # 生成の実行
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.markdown("### 📝 作成された問題")
                        st.write(response.text)
                    else:
                        st.error("AIからの返答が空でした。もう一度お試しください。")

    except Exception as e:
        # エラーが出た場合に原因を表示
        st.error(f"動作エラーが発生しました: {e}")
else:
    st.info("左側のサイドメニューからAPIキーを入力してください。")
