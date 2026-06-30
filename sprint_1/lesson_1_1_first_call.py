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


def build_payload(prompt: str) -> dict:
    return {
        "model": "poolside/laguna-m.1:free",
        "messages": [{"role": "user", "content": prompt}],
    }


def send_openrouter_request(payload: dict) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in environment or .env file.")

    url = "https://openrouter.ai/api/v1/chat/completions"
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(f"OpenRouter request failed: {exc.code} {exc.reason} {error_body}") from exc


def extract_text(response: dict) -> str:
    if not response:
        return ""
    choices = response.get("choices")
    if not choices:
        return json.dumps(response, indent=2)
    message = choices[0].get("message") or {}
    return message.get("content", json.dumps(response, indent=2))


def main() -> None:
    load_dotenv()
    prompt = input("Enter a prompt for OpenRouter: ").strip()
    if not prompt:
        print("Prompt cannot be empty.")
        return

    payload = build_payload(prompt)
    response = send_openrouter_request(payload)
    output = extract_text(response)
    print("\n--- OpenRouter response ---\n")
    print(output)


if __name__ == "__main__":
    main()
