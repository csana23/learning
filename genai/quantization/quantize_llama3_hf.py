from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, QuantoConfig, pipeline
import torch
import os

HF_TOKEN = os.getenv("HF_TOKEN")

device = "cuda:0"

# quantization_config = BitsAndBytesConfig(load_in_4bit=True)
quantization_config = QuantoConfig(weights="int4")

models = [
    "nvidia/Llama3-ChatQA-1.5-8B",
    "SweatyCrayfish/llama-3-8b-quantized",
    "meta-llama/Meta-Llama-3-8B"
]

tokenizer = AutoTokenizer.from_pretrained(
    models[2],
    device_map="auto",
    quantization_config=quantization_config,
    token=HF_TOKEN
)
model = AutoModelForCausalLM.from_pretrained(
    models[2],
    device_map="auto",
    quantization_config=quantization_config,
    token=HF_TOKEN
)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

def get_formatted_input(message):
    system = "System: This is a chat between a user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."
    instruction = "Please give a full and complete answer for the question."

    message['content'] = instruction + " " + message['content']

    conversation = '\n\n'.join("User: " + message["content"] if message["role"] == "user" else "Assistant: " + message["content"]) + "\n\nAssistant:"
    formatted_input = system + "\n\n"  + conversation
    
    return formatted_input

while True:
    query = input("User: ")

    if query == "/bye":
        exit(1)
    else:
        message_template = {"role": "user", "content": query}
        formatted_input = get_formatted_input(message_template)

        tokenized_prompt = tokenizer(tokenizer.bos_token + formatted_input, return_tensors="pt").to(model.device)

        outputs = model.generate(
            input_ids=tokenized_prompt.input_ids, 
            attention_mask=tokenized_prompt.attention_mask, 
            max_new_tokens=128, 
            eos_token_id=terminators
        )

        response = outputs[0][tokenized_prompt.input_ids.shape[-1]:]

        answer = tokenizer.decode(response, skip_special_tokens=True)

        print("LLM:", answer)









