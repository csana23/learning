from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, QuantoConfig
import torch

device = "cuda:0"

# quantization_config = BitsAndBytesConfig(load_in_4bit=True)
quantization_config = QuantoConfig(weights="int4")

models = [
    "nvidia/Llama3-ChatQA-1.5-8B",
    "SweatyCrayfish/llama-3-8b-quantized"
]

tokenizer = AutoTokenizer.from_pretrained(
    models[0], 
    device_map=device, 
    load_in_4bit=True
)
model = AutoModelForCausalLM.from_pretrained(
    models[0], 
    device_map=device, 
    load_in_4bit=True
)

print("model footprint:", model.get_memory_footprint())

while True:
    query = input("User: ")

    if query == "/bye":
        exit(1)

    else:
        model_inputs = tokenizer(str(query), return_tensors="pt").to(device)
        gen_tokens = model.generate(**model_inputs, max_new_tokens=40)
        answer = tokenizer.batch_decode(gen_tokens)
        print("LLM:", answer)
