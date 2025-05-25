from datasets import load_dataset
import json

raw_data = load_dataset("lpj990/haiguitang")

raw_data = raw_data['train'].to_list()

soups = []
for line in raw_data:
    soups.append({
        "soup": line['Riddle'],
        "story": line['Solution']
    })

with open('soup.jsonl', 'w', encoding='utf-8') as f:
    for soup in soups:
       f.write(json.dumps(soup, ensure_ascii=False) + '\n')