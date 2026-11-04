"""Prompt registry: versioned Jinja2 templates loaded from YAML files."""
from dataclasses import dataclass
from typing import Any
from pathlib import Path

import yaml
from jinja2 import Template


@dataclass
class PromptTemplate:
    template_str: str
    system_prompt: str

    def render(self, **kwargs: Any) -> list[dict]:
        user_content = Template(self.template_str).render(**kwargs)
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]


class PromptRegistry:
    def __init__(self, prompts_dir: str):
        self.templates: dict[str, PromptTemplate] = {}
        for file in Path(prompts_dir).glob("*.yaml"):
            data = yaml.safe_load(open(file))
            self.templates[data["name"]] = PromptTemplate(
                template_str=data["template"], system_prompt=data["system"]
            )

    def get(self, name: str) -> PromptTemplate:
        if name not in self.templates:
            raise KeyError(f"Prompt template '{name}' not found")
        return self.templates[name]
