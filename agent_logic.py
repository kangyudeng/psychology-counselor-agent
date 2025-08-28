"""
心理咨询智能体核心逻辑模块（中文输出）。

功能：
- 情绪识别（基于关键词的启发式）
- 心理分析（结合常见心理学原理）
- 分步骤建议（实操、日常行为、放松训练）
- 温暖鼓励与专业提醒（含风险信号识别）

说明：
- 该模块不提供医疗诊断或治疗，仅提供一般性心理学建议。
- 若检测到危机相关词汇，会优先返回紧急求助建议。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional
import os

# 尝试读取 Streamlit Secrets（在 Cloud 上常用）
try:
    import streamlit as st  # type: ignore
    _st_available = True
except Exception:
    st = None  # type: ignore
    _st_available = False

try:
    # 兼容 openai>=1.0 的新客户端
    from openai import OpenAI  # type: ignore
    _openai_available = True
except Exception:
    OpenAI = None  # type: ignore
    _openai_available = False


@dataclass
class AgentResponse:
    emotion_label: str
    analysis: str
    steps: List[str]
    encouragement: str
    professional_reminder: str


def format_response_markdown(resp: AgentResponse) -> str:
    """将结构化响应渲染为对话可读的 Markdown 文本。"""
    parts: List[str] = []
    parts.append(f"### 情绪识别\n你当前可能的情绪类型：{resp.emotion_label}")
    parts.append("### 心理分析\n" + resp.analysis)
    # 步骤建议
    steps_lines = "\n".join([f"{idx}. {s}" for idx, s in enumerate(resp.steps, start=1)])
    parts.append("### 分步骤建议\n" + steps_lines)
    parts.append("### 温暖鼓励\n" + resp.encouragement)
    parts.append("### 专业提醒\n" + resp.professional_reminder)
    return "\n\n".join(parts)


def generate_chat_reply(user_text: str) -> str:
    """面向聊天的自然回复：优先调用 OpenAI，对应模型不可用时回退到本地规则。"""
    # 读取密钥与模型：优先 st.secrets，其次环境变量
    api_key = None
    model = "gpt-4o-mini"
    if _st_available:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", None)  # type: ignore
            model = st.secrets.get("OPENAI_MODEL", model)  # type: ignore
        except Exception:
            pass
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    env_model = os.getenv("OPENAI_MODEL")
    if env_model:
        model = env_model

    if _openai_available and api_key:
        try:
            client = OpenAI(api_key=api_key)
            system_prompt = (
                "你是一名温暖、鼓励、专业的中文心理咨询助理。"
                "目标：帮助用户缓解心理困扰、提供心理学建议。"
                "要求：共情、自然对话风格；不做医疗诊断；发现风险要提醒求助；"
                "尽量给出具体、可执行的小步骤建议（但以对话口吻表达，而非清单）。"
            )
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=0.7,
                max_tokens=700,
            )
            content = completion.choices[0].message.content or ""
            if content.strip():
                return content
        except Exception:
            # 回退到本地规则
            pass

    resp = analyze_and_respond(user_text)

    opening = (
        f"听起来你正经历{resp.emotion_label}的感受。我能理解这对你来说不容易，"
        "愿意在这里陪你一起看看能做些什么。"
    )

    analysis = resp.analysis

    # 将步骤转为对话式表述
    steps_sentences = []
    for idx, s in enumerate(resp.steps, start=1):
        steps_sentences.append(f"{idx}）{s}")
    steps_text = "试着从这些小步骤开始：" + "；".join(steps_sentences) + "。"

    encouragement = resp.encouragement
    reminder = resp.professional_reminder

    reply = (
        f"{opening}\n\n"
        f"{analysis}\n\n"
        f"{steps_text}\n\n"
        f"{encouragement}\n\n"
        f"{reminder}"
    )
    return reply


def _contains_crisis_signal(text: str) -> bool:
    if not text:
        return False
    crisis_keywords = [
        "自杀", "轻生", "活不下去", "结束生命", "伤害自己", "割腕", "跳楼", "想死",
        "杀了我", "不想活", "毁灭自己",
    ]
    lowered = text.lower()
    return any(k in text or k in lowered for k in crisis_keywords)


def classify_emotion(user_text: str) -> str:
    if not user_text or not user_text.strip():
        return "情绪混合或困惑"

    text = user_text.strip()

    anxiety_keys = ["焦虑", "紧张", "担心", "恐惧", "不安", "慌", "心慌", "害怕", "担忧"]
    depression_keys = ["抑郁", "低落", "沮丧", "无助", "孤独", "空虚", "没动力", "绝望"]
    stress_keys = ["压力", "疲惫", "累", "倦怠", "忙不过来", "崩溃", "顶不住"]
    confusion_keys = ["困惑", "迷茫", "混乱", "不知道", "分不清", "无方向"]

    score = {
        "焦虑、紧张、恐惧": 0,
        "抑郁、低落、孤独": 0,
        "压力大、疲惫": 0,
        "情绪混合或困惑": 0,
    }

    lowered = text.lower()
    for k in anxiety_keys:
        if k in text or k in lowered:
            score["焦虑、紧张、恐惧"] += 1
    for k in depression_keys:
        if k in text or k in lowered:
            score["抑郁、低落、孤独"] += 1
    for k in stress_keys:
        if k in text or k in lowered:
            score["压力大、疲惫"] += 1
    for k in confusion_keys:
        if k in text or k in lowered:
            score["情绪混合或困惑"] += 1

    # 选择最高分的情绪；若全部为 0，则默认困惑
    label = max(score.items(), key=lambda x: x[1])[0]
    if all(v == 0 for v in score.values()):
        label = "情绪混合或困惑"
    return label


def _analysis_by_emotion(label: str, user_text: str) -> str:
    base = (
        "以下分析基于常见心理学原则，并非个体化诊断，仅供参考。"
    )
    if label == "焦虑、紧张、恐惧":
        return (
            f"你描述中包含紧张/担忧等线索，可能存在对未来不确定性的高估与对自身能力的低估。"
            f"从认知行为视角，负性自动想法容易放大威胁、忽略资源，这会让身体产生警觉反应（心跳加快、肌肉紧绷）。{base}"
        )
    if label == "抑郁、低落、孤独":
        return (
            f"你的内容呈现出情绪低落与动力不足的迹象。心理学上，这可能与长期压力、失落事件、社会支持不足或完美主义倾向有关。"
            f"行为激活与自我同情练习有助于逐步恢复能量与自我价值感。{base}"
        )
    if label == "压力大、疲惫":
        return (
            f"你似乎承受着持续的负荷与角色要求，可能出现身心资源透支。"
            f"从压力—恢复的框架看，缺乏有效休息与界限设置会让疲惫持续累积，影响专注与情绪稳定。{base}"
        )
    return (
        f"当前信息较为模糊或包含多种情绪线索。可先澄清主要困扰与目标，"
        f"再结合当下最想解决的一件事开始尝试。{base}"
    )


def _steps_by_emotion(label: str) -> List[str]:
    if label == "焦虑、紧张、恐惧":
        return [
            "呼吸练习：进行 4-4-6 深呼吸（吸气 4 秒、停留 4 秒、呼气 6 秒）5 分钟。",
            "认知记录：写下令你担心的事件、最担心的后果、证据与反证，并给出更平衡的替代想法。",
            "行为暴露：将回避的事项拆成小步，每天完成一个最容易的步骤，累积可控感。",
            "作息与运动：固定起卧时间，每周 3 次 20 分钟中低强度运动（散步/拉伸）。",
            "正念练习：每天 5-10 分钟专注当下感受（呼吸、触感、环境声音）。",
        ]
    if label == "抑郁、低落、孤独":
        return [
            "小目标行为激活：列 3 件可在 15 分钟内完成的小事，完成后做标记。",
            "情绪—事件—想法记录：识别情绪触发点，练习更温和、现实的自我对话。",
            "亲密联系：向一位可信赖的人发消息或约一次简短见面，增强支持感。",
            "规律作息与日照：每天固定起床时间，白天接触自然光 20 分钟以上。",
            "自我同情：给当下的自己写一段鼓励话语，承认困难与努力并存。",
        ]
    if label == "压力大、疲惫":
        return [
            "番茄工作法：25 分钟专注 + 5 分钟休息，连续 3 轮后进行 20 分钟较长休息。",
            "优先级四象限：区分重要/紧急，先处理重要且紧急的 1-2 件事。",
            "界限设置：为工作与个人时间设定明确边界，并与相关人沟通预期。",
            "身体放松：睡前进行 10 分钟伸展或渐进性肌肉放松，提升睡眠质量。",
            "微恢复：白天每 90 分钟进行 2-3 分钟走动或呼吸，避免能量枯竭。",
        ]
    return [
        "澄清困扰：用一两句话写下此刻最想改变的一件事。",
        "设定下一步：把这件事拆成一个最小可执行动作，并在 24 小时内完成。",
        "信息收集：列出 2-3 个你已有的资源与可能的支持者。",
        "放松练习：用 5 分钟做腹式呼吸或正念观察，让身心回到当下。",
    ]


def _encouragement(label: str) -> str:
    return (
        "你已经在认真面对自己的感受，这本身就是勇气与力量。"
        "请给自己一些时间，循序渐进地尝试，上述建议会在实践中逐渐显效。"
    )


def _professional_reminder(user_text: str, label: str) -> str:
    if _contains_crisis_signal(user_text):
        return (
            "若你此刻有伤害自己或他人的念头，或难以保证自身安全，请立刻寻求紧急帮助："
            "联系当地的紧急救援电话或身边可信赖的人陪伴你前往就近医院急诊/心理科。"
            "同时，尽量保持与他人的连接，避免单独一人。"
        )
    return (
        "以上建议不替代医疗诊断或治疗。若困扰持续两周以上或明显影响学习/工作/社交/睡眠，"
        "建议尽快咨询专业心理咨询师或精神科医生，获取个性化评估与支持。"
    )


def analyze_and_respond(user_text: str) -> AgentResponse:
    label = classify_emotion(user_text)
    analysis = _analysis_by_emotion(label, user_text)
    steps = _steps_by_emotion(label)
    encouragement = _encouragement(label)
    reminder = _professional_reminder(user_text, label)
    return AgentResponse(
        emotion_label=label,
        analysis=analysis,
        steps=steps,
        encouragement=encouragement,
        professional_reminder=reminder,
    )


