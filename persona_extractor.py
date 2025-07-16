import tiktoken
import json
import textwrap

def chunk_iter(rows, tokens_per_batch=2500):
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    batch, tokens = [], 0

    for row in rows:
        text = f"{row['text']}\n(URL: {row['permalink']})"
        t = len(enc.encode(text))
        if tokens + t > tokens_per_batch and batch:
            yield batch
            batch, tokens = [], 0
        batch.append(text)
        tokens += t

    if batch:
        yield batch

def extract_traits(batch, model_pipeline, tokenizer):
    SYSTEM_PROMPT = """
You are an analyst building a marketing persona.
Given Reddit posts/comments below, extract clues for:
- possible_age
- occupation
- hobbies_or_interests
- motivations
- frustrations

Return a JSON list like:
[{"trait":"occupation","value":"teacher","cite_url":"https://..."}, ...]
"""
    prompt = SYSTEM_PROMPT + "\n\n" + "\n\n-----\n\n".join(batch)
    result = model_pipeline(
        textwrap.dedent(prompt),
        max_new_tokens=512,
        pad_token_id=tokenizer.eos_token_id
    )[0]['generated_text']

    try:
        json_part = result.rsplit("```", 1)[-1] if "```" in result else result
        return json.loads(json_part.strip())
    except:
        print("Failed to parse:\n", result)
        return []
