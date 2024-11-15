
import json
from transformers import AutoTokenizer, AutoModel

def process_spec_file(file_path, output_path):
    # Load spec file
    with open(file_path, "r") as file:
        spec_text = file.read()

    # Segment and summarize (you might adjust for your spec file structure)
    sections = {
        "Overview": "Summary of the project’s main goal.",
        "Requirements": "Summary of required features or functionalities.",
        "Methods": "Summary of key methods to implement."
    }

    # Generate embeddings
    tokenizer = AutoTokenizer.from_pretrained("code-embedding-model")
    model = AutoModel.from_pretrained("code-embedding-model")

    embedded_sections = {}
    for section_name, summary in sections.items():
        inputs = tokenizer(summary, return_tensors="pt")
        embedding = model(**inputs).last_hidden_state.mean(dim=1).tolist()
        embedded_sections[section_name] = {"summary": summary, "embedding": embedding}

    # Save vectorized spec to JSON
    with open(output_path, "w") as json_file:
        json.dump(embedded_sections, json_file)

    print(f"Vectorized spec saved to {output_path}")

# Usage example:
# process_spec_file("path/to/spec_file.txt", "vectorized_output.json")
