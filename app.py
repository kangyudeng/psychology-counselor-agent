import streamlit as st
from agent_logic import generate_chat_reply

st.set_page_config(page_title="心理咨询智能体", page_icon="🫶", layout="wide")

# 轻量、清晰的样式
st.markdown("""
<style>
  .main { background: #f5f7fb; }
  .shell { max-width: 1200px; margin: 20px auto; }
  .panel { background: #ffffff; border: 1px solid #e6e9ef; border-radius: 12px; }
  .left { padding: 18px; height: 78vh; }
  .right { padding: 0; height: 78vh; display: flex; flex-direction: column; }
  .title { font-size: 22px; font-weight: 700; color: #2d3748; }
  .sub { color: #6b7280; font-size: 13px; line-height: 1.6; margin-top: 6px; }
  .sep { height: 1px; background: #eef1f6; margin: 14px 0; }

  .tag { display: inline-block; padding: 6px 10px; border-radius: 8px; background:#f3f6ff; color:#4154f1; font-weight:600; font-size:12px; margin-right:8px; }
  .quick { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px; }
  .qbtn { background:#f8fafc; border:1px solid #e6e9ef; border-radius:10px; padding:10px; text-align:center; cursor:pointer; }
  .qbtn:hover { background:#f1f5f9; }

  .chat-head { padding:16px 18px; border-bottom:1px solid #eef1f6; }
  .chat-title { font-weight:700; color:#334155; }
  .chat-area { flex:1; overflow:auto; padding:18px; background:#fafbff; }
  .msg { max-width: 72%; padding:12px 14px; border-radius:10px; margin:10px 0; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
  .me { background:#3b82f6; color:white; margin-left:auto; border-top-right-radius:4px; }
  .bot { background:#ffffff; color:#374151; border:1px solid #eef1f6; border-top-left-radius:4px; }
  .input-bar { padding:12px; border-top:1px solid #eef1f6; background:white; display:flex; gap:10px; }
  .ta { flex:1; resize:none; height:70px; border:1px solid #e6e9ef; border-radius:10px; padding:10px; background:#fbfdff; }
  .send { background:#4154f1; color:white; border:none; border-radius:10px; padding:0 18px; cursor:pointer; }
  .send:hover { background:#2f44eb; }
</style>
""", unsafe_allow_html=True)


def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "draft" not in st.session_state:
        st.session_state.draft = ""


def sidebar(col):
    with col:
        st.markdown('<div class="panel left">', unsafe_allow_html=True)
        st.markdown('<div class="title">🫶 心理咨询智能体</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub">温暖、鼓励、专业。建议仅作自助支持，若有安全风险请立即线下求助。</div>', unsafe_allow_html=True)
        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

        st.markdown('<span class="tag">情绪识别</span><span class="tag">对话陪伴</span><span class="tag">分步建议</span>', unsafe_allow_html=True)

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
        st.markdown('<div class="title" style="font-size:16px;">快捷示例</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("总是焦虑睡不着", use_container_width=True):
                push_user("最近总是焦虑，晚上睡不着，工作压力大")
        with c2:
            if st.button("压力大容易崩溃", use_container_width=True):
                push_user("最近工作任务很多，感觉要崩溃了，情绪很紧张")
        c3, c4 = st.columns(2)
        with c3:
            if st.button("与伴侣冲突低落", use_container_width=True):
                push_user("和伴侣争吵后很低落，很害怕关系变差")
        with c4:
            if st.button("对未来迷茫", use_container_width=True):
                push_user("对未来很迷茫，不知道方向在哪里")

        st.markdown('</div>', unsafe_allow_html=True)


def chat(col):
    with col:
        # 头部
        st.markdown('<div class="panel right">', unsafe_allow_html=True)
        st.markdown('<div class="chat-head"><span class="chat-title">对话</span></div>', unsafe_allow_html=True)

        # 消息区
        st.markdown('<div class="chat-area">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            cls = "me" if msg["role"] == "user" else "bot"
            st.markdown(f'<div class="msg {cls}">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 输入区
        st.markdown('<div class="input-bar">', unsafe_allow_html=True)
        draft = st.text_area("", key="draft", label_visibility="collapsed", placeholder="请描述你的情况…", height=70)
        send = st.button("发送", key="send", help="发送消息")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if send and draft.strip():
            push_user(draft)
            st.session_state.draft = ""
            st.rerun()


def push_user(text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    reply = generate_chat_reply(text)
    st.session_state.messages.append({"role": "assistant", "content": reply})


def main():
    init_state()
    st.markdown('<div class="shell">', unsafe_allow_html=True)
    left, right = st.columns([4, 8], gap="large")
    sidebar(left)
    chat(right)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()


