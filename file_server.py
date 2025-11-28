import streamlit as st
import os

# --- 页面设置 ---
st.set_page_config(page_title="zxz-文件传输助手", page_icon="📂")

def save_uploaded_file(uploaded_file, target_dir):
    """保存文件到指定目录"""
    try:
        # 确保目录存在，不存在则创建
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        file_path = os.path.join(target_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True, file_path
    except Exception as e:
        return False, str(e)

def main():
    st.title("📂 高级文件传输站")
    
    # === 侧边栏：设置保存位置 ===
    st.sidebar.header("⚙️ 设置")
    
    # 获取当前代码运行的目录作为默认值
    default_path = os.path.join(os.getcwd(), "shared_files")
    
    # 让用户输入保存路径
    save_path = st.sidebar.text_input("文件保存路径", value=default_path)
    
    # 检查路径状态
    if os.path.exists(save_path):
        st.sidebar.success(f"✅ 路径有效")
    else:
        st.sidebar.warning(f"⚠️ 路径不存在，上传时将自动创建")

    # === 主界面 ===
    tab1, tab2 = st.tabs(["📤 上传文件", "📂 查看文件列表"])

    # --- 上传功能 ---
    with tab1:
        st.header("上传文件")
        st.info(f"文件将保存到: `{save_path}`")
        
        uploaded_files = st.file_uploader("选择文件", accept_multiple_files=True)
        
        if uploaded_files and st.button("开始上传"):
            progress_bar = st.progress(0)
            success_count = 0
            
            for idx, file in enumerate(uploaded_files):
                success, msg = save_uploaded_file(file, save_path)
                if success:
                    success_count += 1
                else:
                    st.error(f"文件 {file.name} 保存失败: {msg}")
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            if success_count == len(uploaded_files):
                st.success(f"🎉 全部 {success_count} 个文件已保存到电脑指定目录！")
            else:
                st.warning(f"完成，但部分文件失败。成功: {success_count}/{len(uploaded_files)}")

    # --- 查看/下载功能 ---
    with tab2:
        st.header("当前目录文件")
        
        # 刷新按钮
        if st.button("🔄 刷新列表"):
            st.rerun()

        # 检查目录是否存在
        if os.path.exists(save_path):
            files = os.listdir(save_path)
            files = [f for f in files if not f.startswith('.')] # 忽略隐藏文件
            
            if not files:
                st.write("该目录下暂无文件。")
            else:
                st.write(f"目录 `{save_path}` 下的文件：")
                for filename in files:
                    file_p = os.path.join(save_path, filename)
                    
                    # 简单判断是否是文件（排除子文件夹）
                    if os.path.isfile(file_p):
                        col1, col2 = st.columns([0.8, 0.2])
                        with col1:
                            st.text(f"📄 {filename}")
                        with col2:
                            # 提供下载功能
                            with open(file_p, "rb") as f:
                                st.download_button(
                                    label="⬇️ 下载",
                                    data=f,
                                    file_name=filename,
                                    key=filename
                                )
                        st.divider()
        else:
            st.error("指定的目录不存在，请先上传文件或检查路径。")

if __name__ == "__main__":
    main()

