import json
import os
import urllib.error
import urllib.request


def web_search(query: str, max_results: int = 3) -> str:
    """Run a web search via Tavily and return a text summary."""
    if not query:
        raise ValueError("Query must not be empty.")

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set in the environment.")

    url = "https://api.tavily.com/search"
    payload = {"query": query, "max_results": max_results}
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            response_text = response.read().decode("utf-8")
            results = json.loads(response_text)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"Web search request failed: {exc.code} {exc.reason} {error_body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Unable to reach the web search service. Check network connectivity and Tavily API access."
        ) from exc

    if not isinstance(results, dict):
        return str(results)

    hits = results.get("results") or results.get("items") or []
    if not hits:
        return "No search results returned."

    summary_lines = [f"Search results for: {query}"]
    for index, hit in enumerate(hits[:max_results], start=1):
        title = hit.get("title") or hit.get("name") or "(no title)"
        url_text = hit.get("url") or hit.get("link") or "(no url)"
        snippet = hit.get("snippet") or hit.get("description") or ""
        summary_lines.append(f"{index}. {title}")
        summary_lines.append(f"   URL: {url_text}")
        if snippet:
            summary_lines.append(f"   Summary: {snippet}")

    return "\n".join(summary_lines)
