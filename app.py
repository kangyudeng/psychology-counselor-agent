import streamlit as st
from agent_logic import analyze_and_respond, format_response_markdown, generate_chat_reply


st.set_page_config(page_title="心理咨询智能体", page_icon="🫶", layout="wide")

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 0;
    }
    
    /* 主容器 */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* 顶部导航栏 */
    .top-nav {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 15px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .nav-title {
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .nav-status {
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    .nav-actions {
        display: flex;
        gap: 10px;
    }
    
    .nav-button {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* 标题样式 */
    .main-title {
        text-align: center;
        color: #2d3748;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    
    /* 功能卡片区域 */
    .feature-cards {
        display: flex;
        gap: 15px;
        margin: 20px 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        cursor: pointer;
        min-width: 120px;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 5px;
    }
    
    .feature-desc {
        font-size: 0.8rem;
        color: #718096;
    }
    
    /* 聊天消息容器 */
    .chat-messages {
        background: #f7fafc;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #e2e8f0;
    }
    
    /* 用户消息样式 */
    .user-message {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 15px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
        position: relative;
    }
    
    .user-message::before {
        content: '';
        position: absolute;
        right: -8px;
        top: 20px;
        width: 0;
        height: 0;
        border-left: 8px solid #3182ce;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
    }
    
    /* 助手消息样式 */
    .assistant-message {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        color: #2d3748;
        padding: 20px 25px;
        border-radius: 20px 20px 20px 5px;
        margin: 15px 0;
        max-width: 85%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        position: relative;
    }
    
    .assistant-message::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 20px;
        width: 0;
        height: 0;
        border-right: 8px solid #edf2f7;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
    }
    
    /* 助手头像 */
    .assistant-avatar {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        color: white;
        font-size: 18px;
        margin-right: 15px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* 输入框样式 */
    .chat-input-container {
        background: white;
        border-radius: 25px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 2px solid #e2e8f0;
        margin-top: 20px;
    }
    
    .chat-input {
        border: none;
        outline: none;
        width: 100%;
        padding: 15px 20px;
        border-radius: 20px;
        background: #f7fafc;
        font-size: 16px;
        resize: none;
        min-height: 60px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .chat-input:focus {
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 按钮样式 */
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 20px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        margin: 5px;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .clear-button {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);
    }
    
    .clear-button:hover {
        box-shadow: 0 6px 20px rgba(245, 101, 101, 0.4);
    }
    
    /* 工具栏样式 */
    .toolbar {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
        gap: 15px;
    }
    
    /* 底部导航栏 */
    .bottom-nav {
        background: white;
        border-radius: 20px;
        padding: 15px 20px;
        margin-top: 20px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 0 -4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 10px;
        border-radius: 10px;
    }
    
    .nav-item:hover {
        background: #f7fafc;
    }
    
    .nav-item.active {
        color: #667eea;
        background: #f0f4ff;
    }
    
    .nav-icon {
        font-size: 1.5rem;
    }
    
    .nav-label {
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .chat-container {
            margin: 10px;
            padding: 20px;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .user-message, .assistant-message {
            max-width: 90%;
        }
        
        .feature-cards {
            flex-direction: column;
            align-items: center;
        }
    }
    
    /* 滚动条样式 */
    .chat-messages::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="chat-container">
        <div class="top-nav">
            <div class="nav-left">
                <div>☰</div>
                <div class="nav-title">心理咨询智能体</div>
                <div class="nav-status">• 在线</div>
            </div>
            <div class="nav-actions">
                <button class="nav-button">📥</button>
                <button class="nav-button">⚙️</button>
            </div>
        </div>
        
        <div class="main-title">🫶 心理咨询智能体</div>
        <div class="subtitle">
            温暖、鼓励、专业的心理支持助手<br>
            以下建议不构成诊断或治疗，若有安全风险请立即寻求线下帮助
        </div>
        
        <div class="feature-cards">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">情绪识别</div>
                <div class="feature-desc">智能分析</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💡</div>
                <div class="feature-title">专业建议</div>
                <div class="feature-desc">个性化方案</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤗</div>
                <div class="feature-title">温暖陪伴</div>
                <div class="feature-desc">24/7支持</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title">便捷使用</div>
                <div class="feature-desc">随时随地</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "chat"


def render_chat_ui():
    # 聊天消息容器
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # 显示历史消息
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="assistant-message">
                    <div class="assistant-avatar">💬</div>
                    <div style="display: inline-block; width: calc(100% - 60px); vertical-align: top;">
                        {msg["content"]}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入区域
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    # 使用 st.text_area 作为聊天输入
    prompt = st.text_area(
        "请描述你的情况、情绪或问题。我会一步步帮助你。",
        height=80,
        placeholder="例如：最近总是焦虑，晚上睡不着，工作压力大...",
        key="chat_input"
    )
    
    # 输入按钮行
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("发送", key="send_button", use_container_width=True):
            if prompt.strip():
                process_user_input(prompt)
                st.rerun()
    
    with col2:
        if st.button("清空会话", key="clear_button", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col3:
        if st.button("示例问题", key="example_button", use_container_width=True):
            example_questions = [
                "我最近总是很焦虑，晚上睡不着觉",
                "工作压力很大，感觉快要崩溃了",
                "和男朋友吵架了，感觉很孤独",
                "对未来很迷茫，不知道该怎么办"
            ]
            import random
            example = random.choice(example_questions)
            st.session_state.example_text = example
            st.rerun()
    
    with col4:
        if st.button("导出对话", key="export_button", use_container_width=True):
            export_conversation()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部导航栏
    render_bottom_nav()


def render_bottom_nav():
    st.markdown("""
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-icon">🏠</div>
            <div class="nav-label">首页</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">💬</div>
            <div class="nav-label">聊天</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">🎯</div>
            <div class="nav-label">目标</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">📅</div>
            <div class="nav-label">预约</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def process_user_input(user_text):
    if not user_text.strip():
        return
    
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    # 生成助手回复
    reply = generate_chat_reply(user_text)
    st.session_state.messages.append({"role": "assistant", "content": reply})


def export_conversation():
    if not st.session_state.messages:
        st.warning("暂无对话内容可导出")
        return
    
    # 生成对话文本
    conversation_text = "心理咨询智能体 - 对话记录\n"
    conversation_text += "=" * 50 + "\n\n"
    
    for msg in st.session_state.messages:
        role = "用户" if msg["role"] == "user" else "智能体"
        conversation_text += f"{role}：{msg['content']}\n\n"
    
    # 创建下载按钮
    st.download_button(
        label="📥 下载对话记录",
        data=conversation_text,
        file_name=f"心理咨询对话_{st.session_state.get('session_id', 'session')}.txt",
        mime="text/plain"
    )


def render_response(_user_text: str):
    # 兼容旧函数，不再使用
    pass


def main():
    render_header()
    init_chat_state()
    render_chat_ui()


if __name__ == "__main__":
    main()


