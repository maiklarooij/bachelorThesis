import platform
import re

from dotenv import load_dotenv
from openai import OpenAI
if platform.system() == "Darwin":
    from mlx_lm import load, generate

from UserTypes import LLMReturnCodes

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
    def run(self, history):
        print("run method not implemented!")
        return LLMReturnCodes.NOT_IMPLEMENTED


class MlxLlama(LLM):
    def __init__(self, model_name):
        model, tokenizer = load(model_name)
        self.model = model
        self.tokenizer = tokenizer

    def run(self, history):
        response = generate(
            self.model,
            self.tokenizer,
            prompt=history_to_prompt(history),
            # verbose=True,
            max_tokens=10000,
        )

        return response


class OpenAiLlama(LLM):
    def __init__(self, model_name):
        load_dotenv()
        self.client = OpenAI()
        # Recommended to use 'gpt-3.5-turbo' or 'gpt-4o'
        self.model_name = model_name

    def run(self, history):
        response = self.client.chat.completions.create(
            model=self.model_name,
            # history is a list of objects with role and content keys, OpenAI
            # expects history in this format so no further processing is needed
            messages=history,
        )

        return response.choices[0].message.content
