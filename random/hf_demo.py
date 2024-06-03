from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("stabilityai/stablelm-3b-4e1t")
model = AutoModelForCausalLM.from_pretrained(
  "stabilityai/stablelm-3b-4e1t",
  torch_dtype="auto",
  attn_implementation="flash_attention_2",
)
model.cuda()
inputs = tokenizer("The weather is always wonderful", return_tensors="pt").to(model.device)
tokens = model.generate(
  **inputs,
  max_new_tokens=128,
  temperature=0.75,
  top_p=0.95,
  do_sample=True,
)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))


