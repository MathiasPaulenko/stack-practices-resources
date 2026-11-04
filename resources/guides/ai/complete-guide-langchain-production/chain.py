"""Basic LCEL chain: prompt -> model -> parser.

Usage:
    OPENAI_API_KEY=... python chain.py
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4o", temperature=0.7)
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful coding assistant."),
    ("user", "{input}"),
])

chain = prompt | model | parser

if __name__ == "__main__":
    result = chain.invoke({"input": "Explain async/await in Python"})
    print(result)
