from sprint_4.lesson_4_1_base_agent import Agent


class DeveloperAgent(Agent):
    def __init__(self):
        system_instruction = (
            "You are an expert Front-End Web Developer. Read the essay text and design JSON, "
            "then compile a single-file HTML page with glassmorphic styling and responsive layout. "
            "Return only the HTML content."
        )
        super().__init__("DeveloperAgent", system_instruction, tools=None)
