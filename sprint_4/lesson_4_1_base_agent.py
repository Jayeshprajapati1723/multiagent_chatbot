import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


class Agent:
    def __init__(
        self,
        name: str,
        system_instruction: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        model: str = "poolside/laguna-m.1:free",
    ):
        self.name = name
        self.system_instruction = system_instruction
        self.tools = tools
        self.model = model
        self.messages: List[Dict[str, Any]] = []
        self.load_dotenv()

    def load_dotenv(self, env_path: str = ".env") -> None:
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

    def send_openrouter_request(self, payload: dict) -> dict:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set in environment.")

        url = "https://openrouter.ai/api/v1/chat/completions"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8")
            raise RuntimeError(
                f"OpenRouter request failed: {exc.code} {exc.reason} {error_body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Unable to reach OpenRouter. Check network connectivity and API access."
            ) from exc

    def extract_message(self, response: dict) -> dict:
        choices = response.get("choices") or []
        if not choices:
            return {}
        return choices[0].get("message") or {}

    def execute(self, user_prompt: str) -> dict:
        self.messages = [
            {"role": "system", "content": self.system_instruction}
        ]
        self.messages.append({"role": "user", "content": user_prompt})

        payload = {
            "model": self.model,
            "messages": self.messages,
        }
        if self.tools is not None:
            payload["tools"] = self.tools

        response = self.send_openrouter_request(payload)
        message = self.extract_message(response)
        self.messages.append({"role": "assistant", "content": message.get("content", "")})
        return message
