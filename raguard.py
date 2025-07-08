#!/usr/bin/env python3
"""
RAGuard: A CLI Retrieval-Augmented Generation (RAG) QA system with hallucination detection.
Uses OpenRouter's DeepSeek-R1-70B model for answering and verification.
"""
import json
import sys

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI

import config

def main():
    # Check for API key
    api_key = getattr(config, "OPENROUTER_API_KEY", None)
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY":
        print("Error: Please set your OpenRouter API key in config.py (OPENROUTER_API_KEY).")
        sys.exit(1)
    # Determine input file (use sample_input.json by default)
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "sample_input.json"
    # Load input JSON
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        print("Usage: python RAGuard.py <input.json>")
        sys.exit(1)
    # Validate input format
    if "question" not in data or "documents" not in data:
        print("Input JSON must contain 'question' and 'documents' fields.")
        sys.exit(1)
    question = data["question"]
    documents = data["documents"]
    if not isinstance(documents, list) or len(documents) == 0:
        print("Input 'documents' must be a non-empty list of text strings.")
        sys.exit(1)

    # Embed documents and question for retrieval
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    doc_embeddings = embed_model.encode(documents, convert_to_tensor=True)
    question_embedding = embed_model.encode(question, convert_to_tensor=True)
    # Normalize embeddings and compute cosine similarity
    doc_embeddings = doc_embeddings / torch.linalg.norm(doc_embeddings, dim=1, keepdim=True)
    question_embedding = question_embedding / torch.linalg.norm(question_embedding)
    scores = (doc_embeddings * question_embedding).sum(dim=1).cpu().numpy()
    # Get top 2 documents
    top_k = min(len(documents), 2)
    top_indices = np.argsort(scores)[::-1][:top_k]
    top_docs = [documents[i] for i in top_indices]

    # Prepare context from top documents
    context = ""
    for idx, doc in enumerate(top_docs):
        context += f"Document {idx+1}: {doc}\\n"
    # Initialize OpenRouter client (DeepSeek model)
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    # Create RAG prompt and get answer
    system_prompt = ("You are a helpful assistant that answers questions using ONLY the provided context. "
                     "If the answer is not contained in the context, say 'I don't know'.")
    user_prompt = f"{context}Question: {question}"
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during generation: {e}")
        sys.exit(1)

    # Verification prompt: check for hallucinations
    verif_system = ("You are a fact-checking assistant. Using ONLY the provided context documents, "
                    "identify any parts of the answer that are NOT supported by the context. "
                    "List these unsupported statements as 'hallucinations'. "
                    "If all statements are supported by the context, reply 'No hallucinations'.")
    verif_user = f"{context}Question: {question}\\nAnswer: {answer}"
    try:
        verif_response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": verif_system},
                {"role": "user", "content": verif_user}
            ]
        )
        verification = verif_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)

    # Output results
    print("Original Answer:\\n", answer)
    # Interpret verification
    if verification.lower().startswith("no hallucinations"):
        print("\\nNo hallucinations detected.")
    else:
        print("\\n⚠️ Hallucinations flagged:", verification)

if __name__ == "__main__":
    main()
