from sprint_4.lesson_4_1_base_agent import Agent


class ReviewerAgent(Agent):
    def __init__(self):
        system_instruction = (
            "You are a QA Code Auditor. Inspect the HTML page and return exactly PASS if it compiles cleanly, "
            "or FAIL followed by a bulleted list of issues."
        )
        super().__init__("ReviewerAgent", system_instruction, tools=None)
