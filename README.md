# 🫶 心理咨询智能体（Streamlit）

一个可直接运行与发布的中文心理咨询智能体应用，提供：
- 情绪识别（焦虑/抑郁/压力/困惑）
- 心理分析（结合常见心理学原理）
- 分步骤建议（实操、日常行为、放松训练）
- 温暖鼓励与专业提醒（含危机信号优先提示）

> 说明：本应用仅提供一般性心理学建议，不构成医疗诊断或治疗。

## 目录结构

```
/心理咨询智能体
├── app.py              # Streamlit 主程序
├── agent_logic.py      # 核心逻辑模块
├── requirements.txt    # 依赖
└── README.md           # 使用说明
```

## 本地运行（Cursor/终端）

1. 创建并激活虚拟环境（可选）
```bash
python3 -m venv .venv && source .venv/bin/activate
```

2. 安装依赖（如需调用 OpenAI 接口将 .env 或环境变量中配置 OPENAI_API_KEY）
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=你的密钥  # 或使用 macOS: echo 'export OPENAI_API_KEY=xxxx' >> ~/.zshrc
# 可选：指定模型（默认 gpt-4o-mini）
export OPENAI_MODEL=gpt-4o-mini
```

3. 启动应用
```bash
streamlit run app.py
```

启动后在浏览器访问提示的本地地址即可使用。

## 在 Cursor 中发布

- 直接运行上述命令进行本地预览。
- 若需在云端/容器中部署，确保安装 `requirements.txt`，并以 `streamlit run app.py` 作为启动命令。
- 可用平台：Streamlit Community Cloud、Railway、Render 等。

## 使用建议

- 尽量具体描述情境、想法与身体反应，便于更准确的识别与建议。
- 若存在安全风险（如自伤/自杀念头），请立即寻求线下紧急帮助，应用会优先给出求助指引。
- 若配置 `OPENAI_API_KEY`，对话将由 OpenAI 模型生成（自然对话风格）；未配置时使用本地启发式规则生成建议。

## 声明

- 本应用不替代专业诊疗。
- 若困扰持续两周以上或显著影响功能，建议尽快咨询心理咨询师或精神科医生。
