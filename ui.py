import os
from flask import Flask, request, jsonify, render_template
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

app = Flask(__name__)

DB_FAISS_PATH = "vectorstore/db_faiss"
HF_TOKEN = os.environ.get("HF_TOKEN")

vectorstore = None

def get_vectorstore():
    global vectorstore
    if vectorstore is None:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return vectorstore


def set_custom_prompt():
    template = """
    Use the pieces of information provided in the context to answer the user's question.
    If you don't know the answer, just say that you don't know — don't make things up.
    Only answer from the given context.

    Context: {context}
    Question: {question}

    Start the answer directly. No small talk please.
    """
    return PromptTemplate(template=template, input_variables=["context", "question"])


def load_llm(temperature=0.5):
    return ChatGroq(
        api_key=HF_TOKEN,
        model="llama-3.1-8b-instant",
        temperature=temperature,
        max_tokens=512,
    )


def hybrid_retriever(vs, query, k=3):
    results = vs.as_retriever(search_kwargs={"k": k}).get_relevant_documents(query)
    csv_hits = [
        doc for doc in vs.similarity_search(query, k=5)
        if doc.metadata.get("source") == "self_care_tips.csv"
    ]
    if csv_hits:
        results.append(csv_hits[0])
    return results


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "").strip()
    temperature = float(data.get("temperature", 0.5))
    k_value = int(data.get("k", 3))
    show_sources = data.get("show_sources", True)

    if not prompt:
        return jsonify({"error": "Empty message"}), 400

    try:
        vs = get_vectorstore()
        qa_chain = RetrievalQA.from_chain_type(
            llm=load_llm(temperature),
            chain_type="stuff",
            retriever=vs.as_retriever(search_kwargs={"k": k_value}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": set_custom_prompt()},
        )

        docs = hybrid_retriever(vs, prompt, k_value)
        response = qa_chain.combine_documents_chain.run(input_documents=docs, question=prompt)

        sources = []
        if show_sources and docs:
            for doc in docs:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "-")
                doc_type = "Self-care Tip" if source.endswith(".csv") else f"Page {page}"
                sources.append({"source": source, "type": doc_type})

        return jsonify({"response": response, "sources": sources})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, use_reloader=False)