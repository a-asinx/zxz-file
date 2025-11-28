import streamlit as st
import os

# 1. 设置页面标题和布局
st.set_page_config(page_title="文件传输站", page_icon="📂", layout="centered")
st.title("📂 局域网文件传输助手")

# 定义保存文件的文件夹
UPLOAD_FOLDER = 'shared_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- 上传区域 ---
st.header("⬆️ 上传文件")
uploaded_file = st.file_uploader("选择文件（支持任意格式）", accept_multiple_files=False)

if uploaded_file is not None:
    # 保存文件到本地
    save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"成功上传: {uploaded_file.name}")
    # 为了刷新文件列表，可以用 st.rerun() (新版) 或 实验性功能，但简单起见用户手动刷新即可

# --- 下载区域 ---
st.divider()  # 分割线
st.header("⬇️ 下载文件")

# 获取文件夹内的文件列表
files = os.listdir(UPLOAD_FOLDER)

if not files:
    st.info("暂无文件，请上传。")
else:
    # 遍历显示文件和下载按钮
    for filename in files:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # 排除文件夹，只显示文件
        if os.path.isfile(file_path):
            col1, col2 = st.columns([3, 1])  # 分两列，左边显示文件名，右边显示按钮

            with col1:
                st.write(f"📄 **{filename}**")
                # 显示文件大小 (可选优化)
                size = os.path.getsize(file_path) / (1024 * 1024)
                st.caption(f"{size:.2f} MB")

            with col2:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="下载",
                        data=f,
                        file_name=filename,
                        mime="application/octet-stream",
                        key=filename  # 每个按钮需要唯一的 key
                    )
            st.divider()