"""Typed output via responses.parse and a Pydantic text_format."""
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Person(BaseModel):
    name: str
    age: int
    email: str
    skills: list[str]


def extract() -> Person:
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "Extract person information."},
            {
                "role": "user",
                "content": "Jane Smith, 28, jane@test.com. Skills: Python, SQL, Docker.",
            },
        ],
        text_format=Person,
    )
    return response.output_parsed


if __name__ == "__main__":
    person = extract()
    print(f"Name: {person.name}, Age: {person.age}, Skills: {person.skills}")
