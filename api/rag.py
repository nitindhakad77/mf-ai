import os
import json
import boto3
from db import search


def build_context(question: str) -> str:
    top_k = int(os.getenv("TOP_K", "4"))
    rows = search(question, limit=top_k)
    if not rows:
        return ""
    parts = []
    for r in rows:
        parts.append(
            f"FILENAME: {r.get('filename')}"
            f"SUMMARY: {r.get('summary')}"
            "---"
        )
    return "".join(parts)


def call_bedrock(prompt: str) -> str:
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    max_tokens = int(os.getenv("BEDROCK_MAX_TOKENS", "600"))
    temperature = float(os.getenv("BEDROCK_TEMPERATURE", "0.2"))

    client = boto3.client("bedrock-runtime", region_name=region)

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    })

    resp = client.invoke_model(
        modelId=model_id,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    data = json.loads(resp["body"].read())
    return data.get("content", [{}])[0].get("text", "")


def answer(question: str) -> str:
    context = build_context(question)
    system = (
        "You are a mainframe log assistant. Use the provided context to answer. "
        "If context is missing, say so and suggest what to check next."
    )
    if context:
        prompt = f"SYSTEM:{system}CONTEXT:{context}QUESTION:{question}"
    else:
        prompt = f"SYSTEM:{system}QUESTION:{question}"
    return call_bedrock(prompt)
