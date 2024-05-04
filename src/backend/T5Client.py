from transformers import T5Tokenizer, T5ForConditionalGeneration

class T5:
    def __init__(self, model_name="google-t5/t5-large"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def run(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def dutch_to_english(self, text):
        translate_prompt = "translate Dutch to English"

        return self.run(f"{translate_prompt}: {text}")

    def english_to_dutch(self, text):
        translate_prompt = "translate English to Dutch"

        return self.run(f"{translate_prompt}: {text}")
