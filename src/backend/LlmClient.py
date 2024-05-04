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


def history_to_prompt(history):
    prompt = ""
    for m in history:
        if m["role"] == "system":
            prompt += generate_system_prompt(m["content"])
        if m["role"] == "user":
            prompt += generate_user_prompt(m["content"])
        elif m["role"] == "assistant":
            prompt += generate_assistant_prompt(m["content"])

    prompt += f"{ASSISTENT}\n\n"

    return prompt

class LLM():
    def __init__(self, model_name):
        model, tokenizer = load(model_name)
        self.model = model
        self.tokenizer = tokenizer


class MlxLlama(LLM):
    def run(self, history):
        response = generate(
            self.model,
            self.tokenizer,
            prompt=history_to_prompt(history),
            # verbose=True,
            max_tokens=10000,
        )

        return response

class MlxPhi(LLM):
    def run(self, history):
        response = generate(self.model, self.tokenizer, prompt="hello", verbose=True)

        return response


# if __name__ == "__main__":
#     # llm = MlxLlama(model_name="mlx-community/Llama-3-8b-64k-PoSE-4bit")
#     # llm = MlxLlama(model_name="mlx-community/Meta-Llama-3-8B-Instruct-8bit")
#     llm = MlxLlama("mlx-community/dolphin-2.9-llama3-8b-1m-4bit")

#     # llm = MlxPhi("mlx-community/Phi-3-mini-128k-instruct-8bit")

#     prompt = Prompter(system_prompt="You are a helpful assistant. Be proffesional and think before you answer.")



#     start = time.time()
#     q = "Gegeven de volgende vijf onderwerpen, welke past er niet bij? Appel, Coca cola, Pepsi, Water, Appelsap"
#     prompt.add_question(q)
#     a = llm.run(prompt.prompt)
#     prompt.add_answer(a)
#     print(f"Prompt took {time.time()-start} seconds")

#     # start = time.time()
#     # q = "What is a famous dish with this flavour?"
#     # prompt.add_question(q)
#     # a = llm.run(prompt.prompt)
#     # prompt.add_answer(a)
#     # print(f"Prompt took {time.time()-start} seconds")

#     # start = time.time()
#     # q = "Give me the instructions to make it."
#     # prompt.add_message(q)
#     # a = llm.run(prompt.prompt)
#     # prompt.add_message(a)

#     # print(a)
#     # print(f"Prompt took {time.time()-start} seconds")

#     # start = time.time()
#     prompt.pretty_print()
#     # print(f"Printing prompt took {time.time()-start} seconds")
