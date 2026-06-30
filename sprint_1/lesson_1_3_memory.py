import json
import os
import urllib.error
import urllib.request
from pathlib import Path


def load_dotenv(env_path=".env"):
    env_file = Path(env_path)
    if not env_file.exists():
        return

    with env_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def send_openrouter_request(messages: list) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in environment or .env file.")

    payload = {
        "model": "poolside/laguna-m.1:free",
        "messages": messages,
    }

    url = "https://openrouter.ai/api/v1/chat/completions"
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(f"OpenRouter request failed: {exc.code} {exc.reason} {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Unable to reach OpenRouter. Check your internet connection, DNS settings, and OPENROUTER_API_KEY."
        ) from exc


def extract_text(response: dict) -> str:
    choices = response.get("choices")
    if not choices:
        return json.dumps(response, indent=2)
    return choices[0].get("message", {}).get("content", "")


def main() -> None:
    load_dotenv()
    messages = []
    print("Conversation memory chat. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nInterrupted by user. Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        try:
            response = send_openrouter_request(messages)
        except RuntimeError as exc:
            print(f"Error: {exc}\n")
            continue

        assistant_text = extract_text(response)
        print("Assistant:\n" + assistant_text + "\n")
        messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    main()
