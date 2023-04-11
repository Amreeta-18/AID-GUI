# !pip install openai
import os
import openai
import pandas as pd

# Set up the openai API key
openai.api_key = "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 "
# Load the GPT-3 model
model = openai.Model("text-davinci-003")
# from google.colab import files
# uploaded = files.upload()

df = pd.read_csv("sentences.csv", header = None)
df[0] = df[0].str.replace('\n', ' ')
print(df)
sentences = df.iloc[:, 0].tolist()
# print(sentences)

# Define the prompt template
prompt_template = "Please classify the following sentence as an instruction or not-instruction:\nSentence: '{}'\nClassification:"

# Define the model and parameters
model = "text-davinci-003"
parameters = {
    "temperature": 0,
    "max_tokens": 15,
}

# Generate the prompts
prompts = [prompt_template.format(sentence) for sentence in sentences]

# # Define the model and parameters
model = "text-davinci-003"
parameters = {
    "prompt": prompts,
    "temperature": 0.5,
    "max_tokens": 1,
}

# Make the request to the GPT-3 API
response = openai.Completion.create(
    engine=model,
    prompt=prompts,
    temperature=parameters["temperature"],
    max_tokens=parameters["max_tokens"],
)


# Create empty data frame
df = pd.DataFrame(columns=['Sentence', 'Label'])


# Iterate through the lists and add values to the data frame
for i in range(len(sentences)):
    new_row = pd.DataFrame({'Sentence': [sentences[i]], 'Label':[response.choices[i].text.strip()]})
    df = pd.concat([df, new_row], ignore_index=True)

# # Display the updated data frame
print("\nUpdated Data Frame:")
print(df)

# Specify the file path and name for saving the CSV file
file_path = 'data_frame.csv'

# Write the data frame to a CSV file
df.to_csv(file_path, index=False)