from sprint_4.lesson_4_1_base_agent import Agent
from sprint_3.lesson_3_1_schemas import TOOLS


class ResearcherAgent(Agent):
    def __init__(self):
        system_instruction = (
            "You are an expert ResearcherAgent. Use the web_search tool if you need live facts, "
            "and return concise research notes."
        )
        super().__init__("ResearcherAgent", system_instruction, tools=TOOLS)
