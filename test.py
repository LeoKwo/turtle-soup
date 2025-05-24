from datasets import load_dataset

# Load the dataset
dataset = load_dataset("neurostellar/haiguitang")

# Access splits (if any)
haiguitang = dataset["train"]

# Example: print one data point
print(haiguitang[0])
print(len(haiguitang))
