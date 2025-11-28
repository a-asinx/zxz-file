import streamlit as st
import os

# 1. 基础配置
st.set_page_config(page_title="局域网文件中转站", page_icon="📂", layout="centered")

# 2. 定义电脑上保存文件的文件夹（就在脚本同级目录下）
UPLOAD_FOLDER = 'shared_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

st.title("📂 手机 <-> 电脑 文件传输")
st.info(f"文件将永久保存在你电脑的文件夹: {os.path.abspath(UPLOAD_FOLDER)}")

# --- 功能区1：上传 (手机端操作) ---
st.subheader("⬆️ 上传文件 (手机/电脑)")
uploaded_files = st.file_uploader("选择文件（支持多文件）", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # 拼接保存路径
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        # 写入硬盘
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ {uploaded_file.name} 已保存到电脑硬盘！")

# --- 功能区2：文件列表 (电脑/手机端查看) ---
st.divider()
st.subheader("⬇️ 现有文件列表")

# 强制刷新按钮（有时候文件传完了列表没更新，点一下这个）
if st.button("🔄 刷新文件列表"):
    st.rerun()

# 读取文件夹里的真实文件
files = os.listdir(UPLOAD_FOLDER)

if not files:
    st.write("📂 文件夹是空的，快用手机上传点东西吧。")
else:
    for filename in files:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 **{filename}**")
            with col2:
                # 提供下载功能
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="下载",
                        data=f,
                        file_name=filename,
                        mime="application/octet-stream",
                        key=filename
                    )
            st.divider()
