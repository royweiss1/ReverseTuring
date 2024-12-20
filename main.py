import argparse
from colorama import Fore, Style, init

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
    return parser.parse_args()

def parse_entity(entity: str):
    """Parse the entity string and extract the type and optional API key."""
    parts = entity.split("::")
    entity_type = parts[0]
    api_key = parts[1] if len(parts) > 1 else None
    return entity_type, api_key


def run_conversation(interrogator, interrogated, num_questions):
    print(Fore.BLUE + Style.BRIGHT + "The conversation begins!\n" + Style.RESET_ALL)
    
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

        # Determine the state and get next question from the interrogator
        state = "end" if round == num_questions - 1 else "middle"
        interrogator_response = interrogator.send_message_interrogator(interrogated_response, state)

    print(Fore.MAGENTA + Style.BRIGHT + "The conversation has ended.")
    print(Fore.RED + Style.BRIGHT + f"Final verdict from the interrogator: {interrogator_response}\n")



def main():
    args = parse_args()
    # Parse interrogator
    interrogator_type, interrogator_key = parse_entity(args.interrogator)
    # Parse interrogated
    interrogated_type, interrogated_key = parse_entity(args.interrogated)
    test_mode = args.test # Test mode flag - use cheap models for testing

    # Create interrogator handler
    match interrogator_type.lower():
        case "gemini":
            from models.gemini import GeminiHandler
            interrogator = GeminiHandler("interrogator", test_mode, api_key=interrogator_key)
        case "llama":
            from models.llama import LlamaHandler
            interrogator = LlamaHandler("interrogator", api_key=interrogator_key) # llama is free so no test mode
        case "claude":
            from models.claude import ClaudeSonnetHandler
            interrogator = ClaudeSonnetHandler("interrogator", test_mode, api_key=interrogator_key)
        case "openai":
            from models.openai_Handler import OpenAIGPTHandler
            interrogator = OpenAIGPTHandler("interrogator", test_mode, api_key=interrogator_key)
        case _:
            raise ValueError(f"Unknown interrogator type: {interrogator_type}. Please use gemini/llama/claude/openai::<API_KEY>.")
    
    match interrogated_type.lower():
        case "gemini":
            from models.gemini import GeminiHandler
            interrogated = GeminiHandler("interrogated", test_mode, api_key=interrogated_key)
        case "llama":
            from models.llama import LlamaHandler
            interrogated = LlamaHandler("interrogated", api_key=interrogated_key) # llama is free so no test mode
        case "claude":
            from models.claude import ClaudeSonnetHandler
            interrogated = ClaudeSonnetHandler("interrogated", test_mode, api_key=interrogated_key)
        case "openai":
            from models.openai_Handler import OpenAIGPTHandler
            interrogated = OpenAIGPTHandler("interrogated", test_mode, api_key=interrogated_key)
        case "human":
            from models.llm import HumanHandler
            interrogated = HumanHandler()
        case _:
            raise ValueError(f"Unknown interrogated type: {interrogated_type}. Please use gemini/llama/claude/openai/human::<API_KEY>.")

    run_conversation(interrogator, interrogated, NUMBER_OF_QUESTIONS)


if __name__ == "__main__":
    main()