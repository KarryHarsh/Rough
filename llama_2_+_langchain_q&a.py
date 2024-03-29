# -*- coding: utf-8 -*-
"""Llama 2 + Langchain Q&A

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14GQw8HW8TllB_S3enqotM3dXU7Pav9e_

Thanks to the starter code - https://huggingface.co/spaces/PyaeSoneK/chatchat
"""

!nvidia-smi

"""Install the libraries"""

!pip install -q langchain transformers accelerate bitsandbytes

"""Load the libraries"""

from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain import HuggingFacePipeline
from langchain import PromptTemplate,  LLMChain


from transformers import AutoModel
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

import json
import textwrap

"""Download the Model - We are using NousResearch's Llama2 which is the same as Meta AI's Llama 2, the only difference being "**Not requiring authentication to download**"
"""

tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")

model = AutoModelForCausalLM.from_pretrained("NousResearch/Llama-2-7b-chat-hf",
                                             device_map='auto',
                                             torch_dtype=torch.float16,
                                             load_in_4bit=True,
                                             bnb_4bit_quant_type="nf4",
                                             bnb_4bit_compute_dtype=torch.float16)

"""Define Transformers Pipeline which will be fed into Langchain"""

from transformers import pipeline

pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,
                torch_dtype=torch.float16,
                device_map="auto",
                max_new_tokens = 512,
                do_sample=True,
                top_k=30,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id
                )

"""Define the Prompt format for Llama 2 - This might change if you have a different model"""

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<>\n", "\n<>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are an advanced Life guru and mental health expert that excels at giving advice.
Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.Just say you don't know and you are sorry!"""

"""All the helper fucntions to generate prompt, prompt template, clean up output text"""

def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT, citation=None):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST

    if citation:
        prompt_template += f"\n\nCitation: {citation}"  # Insert citation here

    return prompt_template

def cut_off_text(text, prompt):
    cutoff_phrase = prompt
    index = text.find(cutoff_phrase)
    if index != -1:
        return text[:index]
    else:
        return text

def remove_substring(string, substring):
    return string.replace(substring, "")

def generate(text, citation=None):
    prompt = get_prompt(text, citation=citation)
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs,
                                 max_length=512,
                                 eos_token_id=tokenizer.eos_token_id,
                                 pad_token_id=tokenizer.eos_token_id,
                                 )
        final_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        final_outputs = cut_off_text(final_outputs, '')
        final_outputs = remove_substring(final_outputs, prompt)

    return final_outputs

def parse_text(text):
    wrapped_text = textwrap.fill(text, width=100)
    print(wrapped_text + '\n\n')

"""Defining Langchain LLM"""

llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0.7,'max_length': 256, 'top_k' :50})

system_prompt = "You are an advanced Life guru and mental health expert that excels at giving advice. "
instruction = "Convert the following input text from a stupid human to a well-reasoned and step-by-step throughout advice:\n\n {text}"
template = get_prompt(instruction, system_prompt)
print(template)

prompt = PromptTemplate(template=template, input_variables=["text"])

llm_chain = LLMChain(prompt=prompt, llm=llm, verbose = False)

text = "My life sucks, what do you suggest? Please don't tell me to medidate"

response = llm_chain.run(text)
print(response)

