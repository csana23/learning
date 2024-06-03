from datasets import load_dataset, Dataset, concatenate_datasets
import numpy as np
import pandas as pd
import random

def prepare_data():
    rd_ds = load_dataset("xiyuez/red-dot-design-award-product-description")
    rd_df = pd.DataFrame(rd_ds['train'])
    print(rd_df.info())

    rd_df['instruction'] = "Create a detailed description for the following product: " + rd_df['product'] + " , belonging to category: " + rd_df["category"]
    rd_df = rd_df[["instruction", "description"]]

    rd_df_sample = rd_df.sample(n=5000, random_state=42)

    template = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

    ### Instruction:
    {}

    ### Response:\n"""

    rd_df_sample["prompt"] = rd_df_sample["instruction"].apply(lambda x: template.format(x))

    rd_df_sample = rd_df_sample.rename(columns={"description": "response"})

    rd_df_sample["response"] = rd_df_sample["response"] + "\n### End"
    rd_df_sample = rd_df_sample[["prompt", "response"]]
