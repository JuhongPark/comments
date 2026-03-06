import json
import sys
import ollama

MODEL = "gemma3:270m"
MAX_RETRIES = 2
DEFAULT = {"angry": False, "negative": False, "response": False, "spam": False}


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1")
    return bool(value)


def classify(text, prompt_template):
    prompt = prompt_template.replace("{comment}", text)
    for attempt in range(MAX_RETRIES):
        try:
            resp = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0.3, "num_predict": 30},
            )
            raw = json.loads(resp["message"]["content"])
            return {k: normalize_bool(raw.get(k, False)) for k in DEFAULT}
        except (json.JSONDecodeError, KeyError):
            continue
    return dict(DEFAULT)


def main():
    prompt_file = sys.argv[1] if len(sys.argv) > 1 else "prompt.txt"
    with open(prompt_file, "r") as f:
        prompt_template = f.read()

    with open("sample_data.json", "r") as f:
        samples = json.load(f)

    with open("sample_expected.json", "r") as f:
        expected = json.load(f)

    total = len(samples)
    correct_per_field = {k: 0 for k in DEFAULT}
    wrong = []

    for i, comment in enumerate(samples):
        cid = comment["cid"]
        text = comment["text"]
        pred = classify(text, prompt_template)
        exp = expected[cid]

        for k in DEFAULT:
            if pred[k] == exp[k]:
                correct_per_field[k] += 1
            else:
                wrong.append((i + 1, text[:60], k, pred[k], exp[k]))

        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{total}...", flush=True)

    print(f"\n{'='*60}")
    print(f"Prompt: {prompt_file}")
    print(f"Model: {MODEL} | Sample size: {total}")
    print(f"{'='*60}")

    total_checks = total * 4
    total_correct = sum(correct_per_field.values())
    print(f"  Overall accuracy: {total_correct}/{total_checks} ({total_correct*100//total_checks}%)")
    print()
    for k in DEFAULT:
        acc = correct_per_field[k] * 100 // total
        print(f"  {k:>10}: {correct_per_field[k]}/{total} ({acc}%)")

    if wrong:
        print(f"\n{'='*60}")
        print(f"Misclassifications ({len(wrong)}):")
        for idx, text, field, pred_val, exp_val in wrong:
            print(f"  #{idx:2d} [{field}] pred={pred_val} exp={exp_val} | {text}")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
