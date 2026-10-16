"""Composable LCEL chains — each function returns a Runnable you can pipe together."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI


def basic_chain(model: ChatOpenAI):
    """Minimal chain: prompt -> model -> string."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise technical writer."),
        ("user", "Explain {topic} in under 100 words."),
    ])
    return prompt | model | StrOutputParser()


def summarize_then_translate_chain(model: ChatOpenAI):
    """Two-step chain: the summary feeds the translation prompt."""
    summarize_prompt = ChatPromptTemplate.from_template(
        "Summarize this text in 3 bullet points:\n\n{text}"
    )
    translate_prompt = ChatPromptTemplate.from_template(
        "Translate to Spanish:\n\n{summary}"
    )
    summarize_chain = summarize_prompt | model | StrOutputParser()
    return {"summary": summarize_chain} | translate_prompt | model | StrOutputParser()


def parallel_analysis_chain(model: ChatOpenAI):
    """Runs classification and sentiment on the same input at once."""
    classification_prompt = ChatPromptTemplate.from_template(
        "Classify this text as 'technical', 'marketing', or 'other':\n\n{text}"
    )
    sentiment_prompt = ChatPromptTemplate.from_template(
        "What is the sentiment of this text? (positive, neutral, negative):\n\n{text}"
    )
    return RunnableParallel(
        classification=classification_prompt | model | StrOutputParser(),
        sentiment=sentiment_prompt | model | StrOutputParser(),
    )


def _extract_keywords(text: str) -> list[str]:
    stop_words = {"the", "a", "an", "is", "are", "and", "or", "in", "on"}
    words = [w.lower().strip(".,!?") for w in text.split()]
    return [w for w in words if w not in stop_words and len(w) > 3][:10]


def _format_output(data: dict) -> str:
    return f"Keywords: {', '.join(data['keywords'])}\nSummary: {data['summary']}"


def custom_components_chain(model: ChatOpenAI):
    """Mixes plain Python functions (RunnableLambda) with LLM steps."""
    summarize_prompt = ChatPromptTemplate.from_template(
        "Summarize this text in one sentence:\n\n{text}"
    )
    summarize_chain = summarize_prompt | model | StrOutputParser()
    return (
        RunnableParallel(
            keywords=RunnableLambda(_extract_keywords),
            summary=summarize_chain,
        )
        | RunnableLambda(_format_output)
    )


def resilient_chain(fast_model: ChatOpenAI, strong_model: ChatOpenAI):
    """Retries transient failures, then falls back to a stronger model."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise technical writer."),
        ("user", "Explain {topic} in under 100 words."),
    ])
    fast_chain = prompt | fast_model | StrOutputParser()
    strong_chain = prompt | strong_model | StrOutputParser()
    return fast_chain.with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True,
    ).with_fallbacks([strong_chain])


def routing_chain(model: ChatOpenAI):
    """Routes the input to a specialized chain based on keywords."""
    default_chain = (
        ChatPromptTemplate.from_template("Summarize briefly:\n\n{text}")
        | model
        | StrOutputParser()
    )
    technical_chain = (
        ChatPromptTemplate.from_template(
            "Write a technical summary preserving jargon:\n\n{text}"
        )
        | model
        | StrOutputParser()
    )
    marketing_chain = (
        ChatPromptTemplate.from_template(
            "Write a marketing-friendly summary:\n\n{text}"
        )
        | model
        | StrOutputParser()
    )
    return RunnableBranch(
        (lambda x: "technical" in x["text"].lower(), technical_chain),
        (lambda x: "marketing" in x["text"].lower(), marketing_chain),
        default_chain,
    )
