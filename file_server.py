import streamlit as st
import os
import shutil

# --- 配置 ---
# 设置保存文件的本地目录
UPLOAD_DIR = "shared_files"

# 页面基础设置
st.set_page_config(page_title="局域网文件传输助手", page_icon="📂", layout="centered")

# --- 功能函数 ---
def init_storage():
    """如果目录不存在，则创建"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def save_uploaded_file(uploaded_file):
    """保存上传的文件到本地硬盘"""
    try:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"保存失败: {e}")
        return False

def get_file_list():
    """获取文件列表，按修改时间排序"""
    files = os.listdir(UPLOAD_DIR)
    # 获取完整路径并按时间排序 (最新的在前面)
    files = [f for f in files if not f.startswith('.')] # 忽略隐藏文件
    files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_DIR, x)), reverse=True)
    return files

# --- 主程序 ---
def main():
    init_storage()
    
    st.title("📂 简易文件传输站")
    st.caption("手机上传 -> 电脑下载 | 电脑上传 -> 手机下载")

    # 使用 Tab 分隔功能，界面更整洁
    tab1, tab2 = st.tabs(["📤 上传文件", "📥 下载/查看文件"])

    # === Tab 1: 上传区域 ===
    with tab1:
        st.header("上传文件")
        uploaded_files = st.file_uploader("选择文件 (支持多文件)", accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("确认保存到服务器"):
                progress_bar = st.progress(0)
                for idx, file in enumerate(uploaded_files):
                    if save_uploaded_file(file):
                        # 更新进度条
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                
                st.success(f"成功上传 {len(uploaded_files)} 个文件！")
                st.info("请切换到“下载”标签页查看。")

    # === Tab 2: 下载区域 ===
    with tab2:
        st.header("文件库")
        
        # 添加刷新按钮，因为Streamlit不会自动检测文件夹变化
        if st.button("🔄 刷新列表"):
            st.rerun()

        files = get_file_list()

        if not files:
            st.info("暂无文件，请先去上传。")
        else:
            st.write(f"共 {len(files)} 个文件：")
            
            # 使用列表展示文件
            for filename in files:
                file_path = os.path.join(UPLOAD_DIR, filename)
                col1, col2, col3 = st.columns([6, 2, 2])
                
                with col1:
                    # 显示文件名和大小
                    file_size = os.path.getsize(file_path) / 1024 / 1024 # MB
                    st.text(f"📄 {filename} ({file_size:.2f} MB)")
                
                with col2:
                    # 读取文件用于下载
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                        st.download_button(
                            label="⬇️ 下载",
                            data=file_bytes,
                            file_name=filename,
                            mime="application/octet-stream",
                            key=f"dl_{filename}"
                        )
                
                with col3:
                    # 删除功能
                    if st.button("🗑️ 删除", key=f"del_{filename}"):
                        os.remove(file_path)
                        st.rerun()
                
                st.divider()

if __name__ == "__main__":
    main()
