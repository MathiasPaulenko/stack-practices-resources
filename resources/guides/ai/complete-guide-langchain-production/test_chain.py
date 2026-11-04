"""Unit tests with FakeListChatModel — no API calls in CI.

Run:  pytest test_chain.py -v
"""
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


def test_chain_returns_canned_response():
    fake = FakeListChatModel(responses=["This is a summary."])
    chain = (
        ChatPromptTemplate.from_template("Summarize: {text}")
        | fake
        | StrOutputParser()
    )
    assert chain.invoke({"text": "Long article..."}) == "This is a summary."


def test_json_parser_shape():
    fake = FakeListChatModel(responses=['{"topics": ["a", "b"]}'])
    chain = (
        ChatPromptTemplate.from_template("Extract topics: {text}")
        | fake
        | JsonOutputParser()
    )
    result = chain.invoke({"text": "anything"})
    assert result["topics"] == ["a", "b"]


def test_fallback_triggers_on_error():
    class BrokenModel(FakeListChatModel):
        def _call(self, *a, **k):
            raise RuntimeError("provider down")

    primary = ChatPromptTemplate.from_template("Q: {q}") | BrokenModel(responses=[])
    backup = ChatPromptTemplate.from_template("Q: {q}") | FakeListChatModel(
        responses=["backup answer"]
    )
    chain = primary.with_fallbacks([backup])
    assert chain.invoke({"q": "hi"}).content == "backup answer"
