import json
import ollama

MODEL = "gemma3:1b"

def main():
    response = ollama.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": 'How many states are there in the United States of America? '
                       'Respond in JSON format: {"answer": "your response here"}'
        }],
        format="json",
    )

    result = json.loads(response["message"]["content"])
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
