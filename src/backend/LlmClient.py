import re
import time
from mlx_lm import load, generate

SYSTEM = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"
USER   = "<|start_header_id|>user<|end_header_id|>"
ASSISTENT = "<|start_header_id|>assistant<|end_header_id|>"

class Prompter():
    def __init__(
        self,
        system_prompt="You are a helpful assistant.",
        newest_message="",
        history=[],
    ):
        self.prompt = generate_history(system_prompt, newest_message, history)

    def add_question(self, question):
        self.prompt += generate_user_prompt(question)
        self.prompt = generate_final_prompt(self.prompt)

    def add_answer(self, answer):
        self.prompt += answer
        self.prompt += "\n\n"

    def pretty_print(self):
        # cleaned = self.prompt
        cleaned = re.sub(r"<\|.*?\|>", "", self.prompt)

        print(cleaned)
        return cleaned


def generate_system_prompt(prompt):
    return f"{SYSTEM}\n\n{prompt}<|eot_id|>\n"

def generate_user_prompt(prompt):
    return f"{USER}\n\n{prompt}<|eot_id|>\n"

def generate_assistant_prompt(prompt):
    return f"{ASSISTENT}\n\n{prompt}<|eot_id|>\n"

def generate_final_prompt(prompt):
    return f"{prompt}\n\n{ASSISTENT}\n\n"

def generate_final_prompt_no_assistent(prompt):
    return f"{prompt}\n\n"

# History is a dictionary in the form:
# History: [{user: <user>, assistent: <assistent>}, ...]
def generate_history(system_prompt, newest_message, history):
    prompt = generate_system_prompt(system_prompt)
    for qa_pair in history:
        prompt += generate_user_prompt(qa_pair["user"])
        prompt += generate_assistant_prompt(qa_pair["assistant"])

    if newest_message != "":
        prompt += generate_user_prompt(newest_message)
        prompt = generate_final_prompt(prompt)

    return prompt

class MlxLlama():
    def __init__(self, model_name="mlx-community/Meta-Llama-3-8B-Instruct-4bit"):
        model, tokenizer = load(model_name)
        self.model = model
        self.tokenizer = tokenizer

    def run(self, complete_prompt):
        response = generate(
            self.model,
            self.tokenizer,
            prompt=complete_prompt,
            # verbose=True,
            max_tokens=99999,
        )

        return response



if __name__ == "__main__":
    llm = MlxLlama(model_name="mlx-community/Meta-Llama-3-8B-Instruct-8bit")
    prompt = Prompter(system_prompt="You are a helpful assistant. Be proffesional and think before you answer.")

    # start = time.time()
    q = "What flavour does not fit in the following sequence? chocolate, ice cream, apple, bubble gum, lollypop"
    prompt.add_question(q)
    a = llm.run(prompt.prompt)
    prompt.add_answer(a)
    # print(f"Prompt took {time.time()-start} seconds")

    # start = time.time()
    q = "What is a famous dish with this flavour?"
    prompt.add_question(q)
    a = llm.run(prompt.prompt)
    prompt.add_answer(a)
    # print(f"Prompt took {time.time()-start} seconds")

    # start = time.time()
    # q = "Give me the instructions to make it."
    # prompt.add_message(q)
    # a = llm.run(prompt.prompt)
    # prompt.add_message(a)

    # print(a)
    # print(f"Prompt took {time.time()-start} seconds")

    # start = time.time()
    prompt.pretty_print()
    # print(f"Printing prompt took {time.time()-start} seconds")
