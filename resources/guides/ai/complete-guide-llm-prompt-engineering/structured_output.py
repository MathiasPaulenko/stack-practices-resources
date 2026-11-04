"""JSON mode + Pydantic validation + one repair retry.

Requires OPENAI_API_KEY. Run: python structured_output.py
"""
import json

from openai import OpenAI
from pydantic import BaseModel, ValidationError

client = OpenAI()


class Person(BaseModel):
    name: str
    age: int
    skills: list[str]


def extract_person(text: str) -> Person:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You extract entities and respond only with JSON."},
            {
                "role": "user",
                "content": (
                    'Extract name, age, and skills as JSON '
                    '{"name": "", "age": 0, "skills": []} from: ' + text
                ),
            },
        ],
    )
    raw = response.choices[0].message.content
    try:
        return Person.model_validate_json(raw)
    except ValidationError as e:
        repair = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Fix this JSON to match schema {json.dumps(Person.model_json_schema())}: "
                        f"{raw}. Validation errors: {e}"
                    ),
                }
            ],
        )
        return Person.model_validate_json(repair.choices[0].message.content)


if __name__ == "__main__":
    person = extract_person(
        "John is a 30-year-old software engineer who knows Python, JavaScript, and Go."
    )
    print(person)
