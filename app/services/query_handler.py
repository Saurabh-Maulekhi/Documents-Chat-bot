from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from dotenv import load_dotenv

def answer_question(vectordb, question):
    docs = vectordb.similarity_search(question, k=6)

    llm = HuggingFaceEndpoint(
    model="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation",
    temperature = 0.9
)

    chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return response["output_text"]
