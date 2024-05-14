from huggingface_hub import hf_hub_download
import transformers
import llama_cpp
from llama_cpp import Llama

print(llama_cpp.__version__)

model = Llama.from_pretrained(
    repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
    filename="Phi-3-mini-4k-instruct-q4.gguf",
    n_gpu_layers=-1,
    verbose=True,
)

while True:
    query = input("User: ")

    if query == "/bye":
        exit(1)
    else:
        answer = model(
        f"<|user|>\n{query}<|end|>\n<|assistant|>",
        max_tokens=256,  # Generate up to 256 tokens
        stop=["<|end|>"], 
        echo=False,  # Whether to echo the prompt
        )

        print(answer['choices'][0]['text'])
