import os
from pathlib import Path
from typing import Callable, Optional

from sprint_2.lesson_2_1_web_search import web_search
from sprint_2.lesson_2_2_file_io import write_secure_file
from sprint_2.lesson_2_3_guardrails import input_shield, truncate_text
from sprint_2.lesson_2_4_json_validation import validate_layout_json
from sprint_4.lesson_4_2_researcher import ResearcherAgent
from sprint_4.lesson_4_3_writer import WriterAgent
from sprint_4.lesson_4_4_designer import DesignerAgent
from sprint_4.lesson_4_5_developer import DeveloperAgent
from sprint_4.lesson_4_6_reviewer import ReviewerAgent


def run_publication_pipeline(prompt: str, log_callback: Optional[Callable[[str], None]] = None) -> str:
    if log_callback is None:
        log_callback = print

    prompt = input_shield(prompt)
    log_callback("Input shield passed.")

    researcher = ResearcherAgent()
    writer = WriterAgent()
    designer = DesignerAgent()
    developer = DeveloperAgent()
    reviewer = ReviewerAgent()

    log_callback("Starting researcher agent...")
    researcher_result = researcher.execute(prompt)
    researcher_notes = researcher_result.get("content", "")
    log_callback("Researcher completed.")

    log_callback("Starting writer agent...")
    writer_result = writer.execute(researcher_notes)
    essay_text = writer_result.get("content", "")
    log_callback("Writer completed.")

    log_callback("Starting designer agent...")
    designer_result = designer.execute(essay_text)
    design_json = designer_result.get("validated")
    log_callback("Designer completed.")

    for attempt in range(3):
        log_callback(f"Starting developer attempt {attempt + 1}...")
        developer_input = f"Essay:\n{essay_text}\n\nDesign JSON:\n{design_json}"
        developer_result = developer.execute(developer_input)
        html_output = developer_result.get("content", "")

        log_callback("Starting reviewer agent...")
        reviewer_result = reviewer.execute(html_output)
        review_text = reviewer_result.get("content", "")

        if review_text.strip().upper().startswith("PASS"):
            log_callback("Review passed.")
            slug = "+".join(prompt.lower().split())[:50]
            target_file = f"output/essays/{slug}.html"
            write_secure_file(target_file, html_output)
            log_callback(f"Saved HTML to {target_file}")
            return html_output

        log_callback(f"Review failed: {review_text}")
        developer_input += f"\n\nReviewer feedback:\n{review_text}"

    raise RuntimeError("Failed to compile a passing HTML page after 3 attempts.")


def main() -> None:
    while True:
        prompt = input("Enter a project prompt (or type exit): ").strip()
        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            result_html = run_publication_pipeline(prompt)
            print("Pipeline finished successfully.")
            print(result_html[:400] + "...\n")
        except Exception as exc:
            print(f"Pipeline error: {exc}")


if __name__ == "__main__":
    main()
