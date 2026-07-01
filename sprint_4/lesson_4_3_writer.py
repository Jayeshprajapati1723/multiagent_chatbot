from sprint_4.lesson_4_1_base_agent import Agent


class WriterAgent(Agent):
    def __init__(self):
        system_instruction = (
            "You are an expert Creative Writer. Read the research notes and write a Markdown essay "
            "with an H1 title, H2 subheadings, introduction, body, and conclusion."
        )
        super().__init__("WriterAgent", system_instruction, tools=None)
