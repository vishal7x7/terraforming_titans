from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, logging
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from peft import PeftModel, PeftConfig

peft_model_id = "/home/hacker/axolotl/qlora-out"  # Fine Tuned Tensors generated after Finetuning
model_name_or_path = "NousResearch/Llama-2-7b-hf"  # Base Model (Non-Quantized)
config = PeftConfig.from_pretrained(peft_model_id)

use_triton = False

load_in_4bit = True,
bnb_4bit_quant_type = "nf4",
bnb_4bit_compute_dtype = torch.float16

model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                             torch_dtype=torch.float16,
                                             load_in_4bit=True,
                                             bnb_4bit_quant_type="nf4",
                                             bnb_4bit_compute_dtype=torch.float16,
                                             device_map="auto",
                                             revision="main")

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = PeftModel.from_pretrained(model, peft_model_id)
print("*** Pipeline:")
pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=2000,
        temperature=1,
        top_p=0.95,
        repetition_penalty=1.15
    )

app = FastAPI()

class Details(BaseModel) :
    title: str
    description: str
    jira_link: str
    tags: str


@app.post("/chat")
def chat(prompt_input: Details) :
    print("prompt_input", prompt_input.__dict__)
    input_prompt = f"{prompt_input}"
    print("input_prompt", input_prompt)

    response = pipe(input_prompt)
    print("response ", response)
    return response
