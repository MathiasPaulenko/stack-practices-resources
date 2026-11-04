"""RunnableParallel fan-out: summary, keywords and sentiment in one call."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

model = ChatOpenAI(model="gpt-4o")

summary_chain = ChatPromptTemplate.from_template(
    "Write a 2-sentence summary about: {input}"
) | model | StrOutputParser()

keyword_chain = ChatPromptTemplate.from_template(
    "Extract keywords from: {input}"
) | model | StrOutputParser()

sentiment_chain = ChatPromptTemplate.from_template(
    "Sentiment (positive/negative/neutral) of: {input}"
) | model | StrOutputParser()

parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
    sentiment=sentiment_chain,
)

if __name__ == "__main__":
    print(parallel_chain.invoke({"input": "LangChain makes LLM orchestration fast but adds abstraction overhead."}))
