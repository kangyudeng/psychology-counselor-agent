import streamlit as st
from agent_logic import analyze_and_respond


st.set_page_config(page_title="心理咨询智能体", page_icon="🫶", layout="centered")


def render_header():
    st.title("🫶 心理咨询智能体（中文）")
    st.caption(
        "温暖、鼓励、专业的心理支持助手。以下建议不构成诊断或治疗，若有安全风险请立即寻求线下帮助。"
    )


def render_input():
    with st.form("user_input_form", clear_on_submit=False):
        user_text = st.text_area(
            "请描述你的情况或此刻的感受：",
            height=180,
            placeholder="例如：最近总是焦虑，晚上睡不着，工作压力大。",
        )
        submitted = st.form_submit_button("获取建议")
    return user_text, submitted


def render_response(user_text: str):
    if not user_text.strip():
        st.info("请先输入你的情况，我会尽力帮助你。")
        return

    result = analyze_and_respond(user_text)

    st.markdown("### 情绪识别")
    st.write(f"你当前可能的情绪类型：{result.emotion_label}")

    st.markdown("### 心理分析")
    st.write(result.analysis)

    st.markdown("### 分步骤建议")
    for idx, step in enumerate(result.steps, start=1):
        st.markdown(f"{idx}. {step}")

    st.markdown("### 温暖鼓励")
    st.success(result.encouragement)

    st.markdown("### 专业提醒")
    st.warning(result.professional_reminder)


def main():
    render_header()
    user_text, submitted = render_input()
    if submitted:
        render_response(user_text)


if __name__ == "__main__":
    main()


