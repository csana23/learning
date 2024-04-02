from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, NllbTokenizer
import ctranslate2
import pandas as pd

def read_excel_to_dataframe(file_path: str, sheet_name: str = None, usecols: list = None) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=usecols)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang="hun_Latn")
# tokenizer = NllbTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", source_language="hun_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

def translate_1(text: str, source_language: str, target_language: str):
    text_to_translate = "Life is like a box of chocolates"
    model_inputs = tokenizer(text_to_translate, return_tensors="pt")

    # translate to French
    gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids("hun_Latn"))
    translated_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)

    return translated_text

def translate_2():
    text_to_translate = "Ez egy mondat."
    model_inputs = tokenizer(text_to_translate, return_tensors="pt")

    # translate to English
    # gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids("eng_Latn"))
    gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"])
    translated_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)

    return translated_text

def translate_3() -> str:
    src_lang = "hun_Latn"  # Language code for Hungarian
    tgt_lang = "eng_Latn"  # Language code for English

    text_to_translate = "Ez egy mondat."

    # Load the NLLB-200 Distilled 600M model
    translator = ctranslate2.Translator("facebook/nllb-200-distilled-600M", device="cuda")

    # Tokenize the input text
    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(text_to_translate))

    # Translate
    target_prefix = [tgt_lang]
    results = translator.translate_batch([source], target_prefix=[target_prefix])
    translated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(results.hypotheses[0]))

    return translated_text

def translate_4(text_to_translate: str):
    model_inputs = tokenizer(text_to_translate, return_tensors="pt")

    # translate to English
    # gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids("eng_Latn"))
    gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"])
    translated_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)

    return translated_text
    
file_path = "text.xlsx"
sheet_name = "Sheet1"
usecols = ["hun"]

# df = read_excel_to_dataframe(file_path=file_path, sheet_name=sheet_name, usecols=usecols)
# print(df)

text = "alma"
source_language = "hu"
target_language = "en"

# translated = translate(text=text, source_language=source_language, target_language=target_language)
print(translate_2())