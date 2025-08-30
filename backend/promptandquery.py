import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_prompt(question, chunks):
    context_text = "\n".join([chunk['chunk_text'] for chunk in chunks])
    prompt = f"""
You are a helpful assistant. Answer the question based on the context provided.

Context:
{context_text}

Question:
{question}
Answer:
"""
    return prompt

def get_answer_from_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    answer = response.choices[0].message.content
    print(f"Successfully retrieved answer ✅: {answer}")
    return answer