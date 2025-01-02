import argparse
from colorama import Fore, Style, init
import os
import datetime
import json

init(autoreset=True)

NUMBER_OF_QUESTIONS = 5


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulate a conversation between two entities (LLM or human).",
        epilog="Example:\n"
               "  python3 main.py --interrogator=openai::API_KEY --interrogated=human\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--interrogator",
        required=True,
        help="Specify the interrogator in the format: gemini/llama/claude/openai::<API_KEY>. "
             "If it's a human, use 'human'.",
    )
    parser.add_argument(
        "--interrogated",
        required=True,
        help="Specify the interrogated in the format: gemini/llama/claude/openai/human::<API_KEY>. "
             "If it's a human, use 'human'.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the script in test mode. Use this flag to enable test configurations.",
    )

    parser.add_argument(
        "--evasion",
        action="store_true",
        help="Run the script in evasion mode. The interrogated is aware that it's a test, and tries to actively evade.",
    )
    return parser.parse_args()


def parse_entity(entity: str):
    """Parse the entity string and extract the type and optional API key."""
    parts = entity.split("::")
    entity_type = parts[0]
    api_key = parts[1] if len(parts) > 1 else None
    return entity_type, api_key


def save_conversation_log(interrogator_type, interrogated_type, history):
    """Save the conversation history to a log file."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}/conversation_{interrogator_type}_vs_{interrogated_type}_{timestamp}.json"

    log_data = {
        "timestamp": timestamp,
        "interrogator": interrogator_type,
        "interrogated": interrogated_type,
        "history": history,
    }

    with open(log_filename, "w") as log_file:
        json.dump(log_data, log_file, indent=4)

    print(Fore.GREEN + f"Conversation log saved to {log_filename}")


def run_conversation(interrogator, interrogated, num_questions):
    print(Fore.BLUE + Style.BRIGHT + "The conversation begins!\n" + Style.RESET_ALL)
    history = []  # Store conversation history

    # Start the conversation
    interrogator_response = interrogator.send_message_interrogator(
        "What is your first question for the interrogated?", "start"
    )
    state = "middle"

    for round in range(num_questions):
        print(Fore.YELLOW + f"[Round {round + 1}]")
        print(Fore.CYAN + f"Interrogator has asked:\n {interrogator_response}\n")

        # Get response from the interrogated
        interrogated_response = interrogated.send_message_interrogated(interrogator_response)
        print(Fore.GREEN + f"Interrogated has responded:\n {interrogated_response}\n")

        # Save the round to history
        history.append({
            "round": round + 1,
            "interrogator_question": interrogator_response,
            "interrogated_response": interrogated_response
        })

        # Determine the state and get next question from the interrogator
        state = "end" if round == num_questions - 1 else "middle"
        interrogator_response = interrogator.send_message_interrogator(interrogated_response, state)

    print(Fore.MAGENTA + Style.BRIGHT + "The conversation has ended.")
    print(Fore.RED + Style.BRIGHT + f"Final verdict from the interrogator: {interrogator_response}\n")
    history.append({"final_verdict": interrogator_response})

    return history


def main():
    args = parse_args()
    # Parse interrogator
    interrogator_type, interrogator_key = parse_entity(args.interrogator)
    # Parse interrogated
    interrogated_type, interrogated_key = parse_entity(args.interrogated)
    test_mode = args.test  # Test mode flag - use cheap models for testing
    evasion_mode = args.evasion  # Evasion mode flag - interrogated tries to evade

    # Create interrogator handler
    match interrogator_type.lower():
        case "gemini":
            from models.gemini import GeminiHandler
            interrogator = GeminiHandler("interrogator", test_mode, evasion_mode, api_key=interrogator_key)
        case "llama":
            from models.llama import LlamaHandler
            interrogator = LlamaHandler("interrogator", evasion_mode)
        case "claude":
            from models.claude import ClaudeSonnetHandler
            interrogator = ClaudeSonnetHandler("interrogator", test_mode, evasion_mode, api_key=interrogator_key)
        case "openai":
            from models.openai import OpenAIGPTHandler
            interrogator = OpenAIGPTHandler("interrogator", test_mode, evasion_mode, api_key=interrogator_key)
        case _:
            raise ValueError(
                f"Unknown interrogator type: {interrogator_type}. Please use gemini/llama/claude/openai::<API_KEY>.")

    match interrogated_type.lower():
        case "gemini":
            from models.gemini import GeminiHandler
            interrogated = GeminiHandler("interrogated", test_mode, evasion_mode, api_key=interrogated_key)
        case "llama":
            from models.llama import LlamaHandler
            interrogated = LlamaHandler("interrogated", evasion_mode)
        case "claude":
            from models.claude import ClaudeSonnetHandler
            interrogated = ClaudeSonnetHandler("interrogated", test_mode, evasion_mode, api_key=interrogated_key)
        case "openai":
            from models.openai import OpenAIGPTHandler
            interrogated = OpenAIGPTHandler("interrogated", test_mode, evasion_mode, api_key=interrogated_key)
        case "human":
            from models.llm import HumanHandler
            interrogated = HumanHandler()
        case _:
            raise ValueError(
                f"Unknown interrogated type: {interrogated_type}. Please use gemini/llama/claude/openai/human::<API_KEY>.")

    # Run conversation and save history
    history = run_conversation(interrogator, interrogated, NUMBER_OF_QUESTIONS)
    save_conversation_log(interrogator_type, interrogated_type, history)


if __name__ == "__main__":
    main()