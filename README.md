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

![reverse_turing](https://github.com/user-attachments/assets/d4462545-0010-415f-a9f3-c892366110c3)


## Docs
