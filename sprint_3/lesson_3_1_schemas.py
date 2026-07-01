TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for relevant facts and return a summary of the top results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to execute.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "The maximum number of results to return.",
                    "default": 3,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    }
]
