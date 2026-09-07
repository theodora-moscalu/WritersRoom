import json


def parse_json_object(text: str) -> dict:
    """Parse a JSON object from a model reply, tolerating fences and stray prose."""

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.lstrip().lower().startswith("json"):
            cleaned = cleaned.lstrip()[4:]

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError(
            "The model reply did not contain a JSON object."
        )

    return json.loads(cleaned[start : end + 1])
