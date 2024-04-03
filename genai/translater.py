import pandas as pd
import os
import shutil
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def get_xlsx_files(folder_path) -> list:
    xlsx_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.xlsx')]
    return xlsx_files

def read_excel_to_dataframe(file_path: str, sheet_name: str = None, usecols: list = None) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=usecols)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def copy_excel_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        return f"Excel file copied from '{source_path}' to '{destination_path}' successfully."
    except Exception as e:
        return f"Error: {str(e)}"

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang="hun_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

def translate(df: pd.DataFrame, column_name: str):
    translated_texts = []

    for text in df[column_name]:
        model_inputs = tokenizer(str(text), return_tensors="pt")
        gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"])
        translated_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)
        translated_texts.append(translated_text)

    df['translated_' + column_name] = translated_texts

    return df

def run_translater_on_folder(folder_path: str):
    # get all excel files inside folder
    excel_files = get_xlsx_files(folder_path=folder_path)

    for excel_file in excel_files:
        # get all the sheets inside the current excel file
        df_dict = pd.read_excel(excel_file, sheet_name=None)

        sheet_names = list(df_dict.keys())

        # go through all sheets
        for sheet in sheet_names:
            print('Working on', str(excel_file), ', sheet:', str(sheet))
            df = df_dict[sheet]
            
            # get column name
            column_name = df.columns[0]

            # inference model
            translated_df = translate(df=df, column_name=column_name)
            translated_sheet = 'Translated_' + str(sheet)

            # write result to new Translated_* sheet
            try:
                with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
                    translated_df.to_excel(writer, sheet_name=translated_sheet, index=False, header=False)
                    print("Data written to sheet '{translated_sheet}' in '{excel_file}' successfully.")
            except Exception as e:
                print("Error: {str(e)}")
            
# run the whole thing
folder_path = "C:\\Users\\richa\\Source\\Repos\\learning\\genai\\"
run_translater_on_folder(folder_path=folder_path)






# inference
'''
folder_path = "C:\\Users\\richa\\Source\\Repos\\learning\\genai\\text.xlsx"
sheet_name = "Sheet1"
usecols = ["hun"]

df = translate(
        read_excel_to_dataframe(file_path=file_path, sheet_name=sheet_name, usecols=usecols),
        column_name="hun"
    )

print(df)
'''




'''
# tokenizer = NllbTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", source_language="hun_Latn")
def translate_1(text: str, source_language: str, target_language: str):
    text_to_translate = "Life is like a box of chocolates"
    model_inputs = tokenizer(text_to_translate, return_tensors="pt")

    # translate to French
    gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids("fr_Latn"))
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

# df = read_excel_to_dataframe(file_path=file_path, sheet_name=sheet_name, usecols=usecols)
# print(df)

# translated = translate(text=text, source_language=source_language, target_language=target_language)
# print(translate_2())
'''