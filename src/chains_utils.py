# chains_utils.py

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


def _get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )


def get_responce(user_query: str) -> str:
    vectorstore = st.session_state.vector_store

    # ✅ Modern retrieval (FIXED)
    docs = vectorstore.similarity_search(user_query, k=4)

    if not docs:
        return "❌ Not found on this website."

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You must answer ONLY from the provided website context below. "
         "If the answer does not exist in the context, say: "
         "'Not found on this website.'\n\n"
         "Website Context:\n{context}"
        ),
        ("user", "{input}")
    ])

    chain = prompt | _get_llm() | StrOutputParser()

    response = chain.invoke({
        "context": context,
        "input": user_query
    })

    return response
