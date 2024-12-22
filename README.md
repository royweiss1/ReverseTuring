# Reverse Turing Test

Simulate a conversation between two entities: an **interrogator** (LLM or human) and an **interrogated** (LLM or human). The goal is for the interrogator to determine whether the other entity is an AI or a human.

## Setup

1. Install Python 3.8 or higher.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following arguments:

```bash
python3 main.py --interrogator=<TYPE>::<API_KEY> --interrogated=<TYPE>::<API_KEY> [--test]
```
TYPE = gemini, llama, claude, openai, human (only for interrogated)

--test: (Optional) - configures the usage of cheaper models to test around

## Docs
https://docs.google.com/document/d/1OyPKWEacg2ieDL0iyMTwHZOM-Att-8-IKPxDbzPlXsA/edit?tab=t.0#heading=h.5yu0gqe61ca
