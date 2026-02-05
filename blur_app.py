import streamlit as st
from PIL import Image, ImageFilter
from io import BytesIO
import zipfile

st.set_page_config(page_title="画像ツール", layout="wide")

col1, col2 = st.columns([0.08, 0.92])
with col1:
    try:
        logo = Image.open("logo.jpg")
        logo_resized = logo.resize((40, 40), Image.Resampling.LANCZOS)
        st.image(logo_resized, width=40)
    except:
        pass
with col2:
    st.title("📸 画像ツール")

tab1, tab2 = st.tabs(["画像ぼかし", "4分割+合成"])

# ===== タブ1：画像ぼかし =====
with tab1:
    st.subheader("画像をぼかす")
    
    st.write("アップロードされた画像を、指定した強度でぼかします。")
    
    uploaded_files = st.file_uploader("画像をアップロード", type=['png', 'jpg', 'jpeg', 'bmp', 'gif'], key="blur_upload", accept_multiple_files=True)
    
    if uploaded_files:
        # ぼかしの種類を選択
        blur_type = st.selectbox(
            "ぼかしの種類を選択",
            ["ガウシアンブラー", "ボックスブラー", "メディアンフィルタ"],
            key="blur_type"
        )
        
        # スライダーで強度を指定（0～100）
        strength = st.slider("ぼかしの強度", min_value=0, max_value=100, value=10, step=1, key="blur_strength")
        
        if strength > 0:
            st.subheader("プレビュー")
            cols = st.columns(min(4, len(uploaded_files)))
            
            blurred_images = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                img = Image.open(uploaded_file)
                
                if blur_type == "ガウシアンブラー":
                    blur_radius = int((strength / 100) * 50)
                    if blur_radius % 2 == 0:
                        blur_radius += 1
                    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                
                elif blur_type == "ボックスブラー":
                    blur_radius = int((strength / 100) * 50)
                    if blur_radius % 2 == 0:
                        blur_radius += 1
                    blurred_img = img.filter(ImageFilter.BoxBlur(blur_radius))
                
                elif blur_type == "メディアンフィルタ":
                    blur_radius = int((strength / 100) * 50)
                    if blur_radius % 2 == 0:
                        blur_radius += 1
                    blurred_img = img.filter(ImageFilter.MedianFilter(size=blur_radius))
                
                blurred_images.append(blurred_img)
                
                with cols[idx % len(cols)]:
                    st.image(blurred_img, width=200)
            
            st.subheader("ダウンロード")
            
            # ZIP形式で一括ダウンロード
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for i, blurred_img in enumerate(blurred_images):
                    buf = BytesIO()
                    blurred_img.save(buf, format='PNG')
                    zipf.writestr(f'{i+1}.png', buf.getvalue())
            zip_buffer.seek(0)
            
            st.download_button(
                label="📦 ZIP一括ダウンロード",
                data=zip_buffer.getvalue(),
                file_name="blurred_images.zip",
                mime="application/zip",
                key="blur_zip_download"
            )
            
            # 個別ダウンロード
            st.write("**個別ダウンロード**")
            download_cols = st.columns(min(4, len(blurred_images)), gap="small")
            for i, blurred_img in enumerate(blurred_images):
                buf = BytesIO()
                blurred_img.save(buf, format='PNG')
                buf.seek(0)
                
                with download_cols[i % len(download_cols)]:
                    st.download_button(
                        label=f"{i+1}.png",
                        data=buf.getvalue(),
                        file_name=f"{i+1}.png",
                        mime="image/png",
                        key=f"blur_download_{i}",
                        use_container_width=True
                    )
        else:
            st.info("強度を0より大きい値に設定してください")
    else:
        st.info("👆 画像をアップロードしてください")

# ===== タブ2：4分割+合成 =====
with tab2:
    st.info("このタブは統合予定です")
