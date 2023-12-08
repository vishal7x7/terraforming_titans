import csv
import json

with open('TrainingDataShuffled.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open('output_file.jsonl', mode='w', encoding='utf-8') as jsonl_file:
        for row in csv_reader:
            json.dump(row, jsonl_file)
            jsonl_file.write('\n')

print("CSV file has been converted to JSONL.")


"""
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl

# finetune lora
accelerate launch -m axolotl.cli.train yml_conf.yml


export LD_LIBRARY_PATH=/usr/local/cuda-12.0/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-12.0

ls /usr/local/cuda-12.0/lib64/libcudnn.so.8*

uvicorn test:app --host 0.0.0.0 --port 8503
"""