import tiktoken


def count_tokens(model, prompt):
    encoding = tiktoken.encoding_for_model(model)
    tokens = len(encoding.encode(prompt))
    print(f"{tokens} tokens")
    return tokens
