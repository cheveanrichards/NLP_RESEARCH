import torch
import sentencepiece as spm

# Load the tokenizer
tokenizer = spm.SentencePieceProcessor()
tokenizer.load(r'C:\Users\richa\.llama\checkpoints\Meta-Llama3.1-8B\tokenizer.model')

# Load the model
model = torch.load(r'C:\Users\richa\.llama\checkpoints\Meta-Llama3.1-8B\consolidated.00.pth', map_location=torch.device('cpu'))
model.eval()

# Prepare the prompt
prompt = "how to cook Peruvian chicken"
input_ids = tokenizer.encode_as_ids(prompt)
input_ids_tensor = torch.tensor([input_ids])

# Generate text
with torch.no_grad():
    output = model.generate(input_ids_tensor, max_length=50)

# Decode and print the generated text
output_ids = output[0].tolist()
generated_text = tokenizer.decode(output_ids)
print(f"Generated Text: {generated_text}")


# import transformers
# import torch
# from transformers import AutoTokenizer


# model_id = "meta-llama/Meta-Llama-3.1-8B"
# tokenizer = AutoTokenizer.from_pretrained(model_id)


# pipeline = transformers.pipeline(
#   "text-generation",
#   model="meta-llama/Meta-Llama-3.1-8B",
#   model_kwargs={"torch_dtype": torch.bfloat16},
#   device_map="auto",
# )


# sequences = pipeline(
#     "Provide a recommendation of crash prevention",
#     do_sample = True,
#     top_k = 10,
#     num_return_sequences = 1,
#     eos_token_id = tokenizer.eos_token_id,
#     truncation = True,
#     max_length = 400
# )


# for seq in sequences:
#     print(f"Result: {seq['generated_text']}")

