import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog

# --- 页面基础设置 ---
st.set_page_config(page_title="局域网文件传输助手", page_icon="📂")

# --- 初始化 Session State (用于记住选择的路径) ---
if 'save_path' not in st.session_state:
    # 默认路径为当前代码所在文件夹下的 shared_files
    st.session_state['save_path'] = os.path.join(os.getcwd(), "shared_files")

# --- 功能函数 ---
def select_folder_on_server():
    """在服务器端（电脑）打开文件夹选择框"""
    try:
        # 创建隐藏的 tkinter 主窗口
        root = tk.Tk()
        root.withdraw() # 隐藏主窗口
        root.wm_attributes('-topmost', 1) # 尝试让窗口置顶
        
        # 弹出文件夹选择框
        folder_selected = filedialog.askdirectory()
        
        # 销毁窗口
        root.destroy()
        
        return folder_selected
    except Exception as e:
        st.error(f"无法打开文件夹选择器: {e}")
        return None

def save_uploaded_file(uploaded_file, target_dir):
    """保存文件"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    try:
        file_path = os.path.join(target_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except:
        return False

# --- 主程序 ---
def main():
    st.title("📂 极简文件传输 (路径选择版)")

    # === 路径选择区域 ===
    st.sidebar.header("⚙️ 保存位置设置")
    
    # 显示当前路径
    st.sidebar.info(f"当前路径:\n\n`{st.session_state['save_path']}`")

    # 两个按钮：一个手动输入，一个点击选择
    col_input, col_btn = st.sidebar.columns([1, 1])
    
    with col_btn:
        # 核心功能：点击按钮调用电脑的文件夹选择器
        if st.button("📂 选择文件夹"):
            selected = select_folder_on_server()
            if selected:
                # 更新 Session State
                st.session_state['save_path'] = selected
                st.rerun() # 立即刷新页面显示新路径

    # 允许用户手动修正路径（可选）
    new_path = st.sidebar.text_input("或手动修改路径", value=st.session_state['save_path'])
    if new_path != st.session_state['save_path']:
        st.session_state['save_path'] = new_path

    st.divider()

    # === 上传区域 ===
    st.header("📤 上传文件")
    uploaded_files = st.file_uploader("选择文件（支持批量）", accept_multiple_files=True)

    if uploaded_files:
        if st.button(f"保存 {len(uploaded_files)} 个文件到电脑"):
            # 进度条
            progress_text = "文件传输中..."
            my_bar = st.progress(0, text=progress_text)
            
            success_count = 0
            for idx, file in enumerate(uploaded_files):
                if save_uploaded_file(file, st.session_state['save_path']):
                    success_count += 1
                my_bar.progress((idx + 1) / len(uploaded_files))
            
            my_bar.empty()
            
            if success_count == len(uploaded_files):
                st.success(f"✅ 成功！文件已保存到：{st.session_state['save_path']}")
                # 列出刚刚上传的文件
                with st.expander("查看本次上传的文件详情"):
                    for file in uploaded_files:
                        st.write(f"- {file.name}")
            else:
                st.error("部分文件保存失败，请检查路径权限。")

if __name__ == "__main__":
    main()
