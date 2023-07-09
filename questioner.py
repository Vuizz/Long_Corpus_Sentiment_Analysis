from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

class QuestionText:
    
    def __init__(self):
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        self.tokenizer = T5Tokenizer.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering")
        self.model = T5ForConditionalGeneration.from_pretrained("MaRiOrOsSi/t5-base-finetuned-question-answering").to(self.device)

    def ask_questions(self, text, questions):
        answers = {}
        for question in questions:
            input = f"question: {question} context: {text}"
            encoded_input = self.tokenizer([input],
                                 return_tensors='pt',
                                 max_length=512,
                                 truncation=True)
            output = self.model.generate(input_ids = encoded_input.input_ids,
                                        attention_mask = encoded_input.attention_mask)
            output = self.tokenizer.decode(output[0], skip_special_tokens=True)
            answers[question] = output
        return answers
            