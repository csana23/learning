from datasets import load_dataset, Dataset, concatenate_datasets
import numpy as np
import pandas as pd
import random

from peft import get_peft_config, PeftModel, PeftConfig, get_peft_model, LoraConfig, TaskType
from transformers import AutoModelForCausalLM
from transformers import LlamaTokenizer, LlamaForCausalLM
import torch
from transformers.trainer_callback import TrainerCallback
import os
from transformers import BitsAndBytesConfig
from trl import SFTTrainer
import mlflow

def prepare_data(dataset_name: str) -> pd.DataFrame:
    rd_ds = load_dataset(dataset_name)
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

    return rd_df_sample

def qlora_fine_tune(model_name: str, df: pd.DataFrame):
    pass

dataset_name = "xiyuez/red-dot-design-award-product-description"

print(prepare_data(dataset_name=dataset_name).iloc[0].prompt)


