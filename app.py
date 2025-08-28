import streamlit as st
from agent_logic import analyze_and_respond, format_response_markdown, generate_chat_reply


st.set_page_config(page_title="心理咨询智能体", page_icon="🫶", layout="centered")


def render_header():
    st.title("🫶 心理咨询智能体（中文）")
    st.caption(
        "温暖、鼓励、专业的心理支持助手。以下建议不构成诊断或治疗，若有安全风险请立即寻求线下帮助。"
    )


def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []  # [{"role": "user"|"assistant", "content": str}]


def render_chat_ui():
    # 历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 输入区
    prompt = st.chat_input("描述你的情况、情绪或问题。我会一步步帮助你。")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 生成回复
        md = generate_chat_reply(prompt)
        with st.chat_message("assistant"):
            st.markdown(md)
        st.session_state.messages.append({"role": "assistant", "content": md})

    # 工具栏
    cols = st.columns(2)
    if cols[0].button("清空会话"):
        st.session_state.messages = []
        st.experimental_rerun()


def render_response(_user_text: str):
    # 兼容旧函数，不再使用
    pass


def main():
    render_header()
    init_chat_state()
    render_chat_ui()


if __name__ == "__main__":
    main()


