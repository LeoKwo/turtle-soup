from datasets import load_dataset
import json
from modelscope.msdatasets import MsDataset

ds =  MsDataset.load('Narcissuses/Turtle-Bench', subset_name='default', split='train')

raw_data = ds.to_list()

soups = []
stories = set()
for line in raw_data:
    if line['title'] not in stories:
        stories.add(line['title'])
        soups.append({
            "soup": line['surface'],
            "story": line['bottom']
        })

with open('soup2.jsonl', 'w', encoding='utf-8') as f:
    for soup in soups:
       f.write(json.dumps(soup, ensure_ascii=False) + '\n')
