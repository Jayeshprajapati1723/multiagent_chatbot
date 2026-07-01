from sprint_4.lesson_4_1_base_agent import Agent
from sprint_2.lesson_2_4_json_validation import validate_layout_json


class DesignerAgent(Agent):
    def __init__(self):
        system_instruction = (
            "You are an expert UI/UX Designer. Analyze the essay text and return only a single valid JSON block. "
            "The JSON must include detected_sentiment, theme, and layout_style exactly."
        )
        super().__init__("DesignerAgent", system_instruction, tools=None)

    def execute(self, user_prompt: str) -> dict:
        message = super().execute(user_prompt)
        content = message.get("content", "")
        validated = validate_layout_json(content)
        return {"content": content, "validated": validated}
