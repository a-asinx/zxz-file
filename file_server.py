import streamlit as st
import os
import shutil

# --- 页面配置 ---
st.set_page_config(page_title="云端文件中转站", page_icon="☁️", layout="centered")

# --- 核心设置 ---
# 在云端，只能保存到当前项目目录下的文件夹中
UPLOAD_DIR = "temp_storage"

# 确保目录存在
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- 功能函数 ---
def save_uploaded_file(uploaded_file):
    try:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        return False

def get_files():
    if not os.path.exists(UPLOAD_DIR):
        return []
    files = os.listdir(UPLOAD_DIR)
    # 过滤掉隐藏文件
    files = [f for f in files if not f.startswith('.')]
    # 按时间倒序排列（最新的在最上面）
    files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_DIR, x)), reverse=True)
    return files

# --- 主程序 ---
def main():
    st.title("☁️ 云端文件中转站")
    st.info("⚠️ 注意：部署在免费云端时，文件是临时的。长时间不访问或代码更新后，文件会被清空。")

    tab1, tab2 = st.tabs(["📤 上传 (手机/电脑)", "📥 下载列表"])

    # === 上传部分 ===
    with tab1:
        uploaded_files = st.file_uploader("点击上传文件", accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("确认上传"):
                progress_bar = st.progress(0)
                for i, file in enumerate(uploaded_files):
                    save_uploaded_file(file)
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                st.success(f"成功上传 {len(uploaded_files)} 个文件！请切换到“下载”标签页查看。")

    # === 下载部分 ===
    with tab2:
        if st.button("🔄 刷新文件列表"):
            st.rerun()
            
        files = get_files()
        
        if not files:
            st.write("📂 暂无文件，快去上传吧。")
        else:
            st.write(f"共 {len(files)} 个文件：")
            for filename in files:
                filepath = os.path.join(UPLOAD_DIR, filename)
                
                # 布局：文件名 + 下载按钮
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.text(f"📄 {filename}")
                    
                with col2:
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="⬇️ 下载",
                            data=f,
                            file_name=filename,
                            mime="application/octet-stream",
                            key=f"dl_{filename}"
                        )
                st.divider()

if __name__ == "__main__":
    main()
