import json
from sprint_2.lesson_2_1_web_search import web_search


def parse_tool_call(choice: dict) -> dict:
    tool_calls = choice.get("tool_calls") or []
    if not tool_calls:
        return {}

    tool_call = tool_calls[0]
    return {
        "name": tool_call.get("name"),
        "arguments": tool_call.get("arguments"),
        "tool_call_id": tool_call.get("tool_call_id"),
    }


def execute_tool(name: str, arguments: str) -> str:
    if name != "web_search":
        raise ValueError(f"Unsupported tool: {name}")

    try:
        parsed_args = json.loads(arguments)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid tool arguments JSON: {exc.msg}") from exc

    query = parsed_args.get("query")
    max_results = parsed_args.get("max_results", 3)
    return web_search(query, max_results)
