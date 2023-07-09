from transformers import BertForSequenceClassification, BertTokenizer
import torch

class ScoreText:
    
    def __init__(self):
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        self.tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        self.model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone').to(self.device)
        
        
    def chunk_text_and_predict_probs(self, text):
        tokens = self.tokenizer(text, add_special_tokens=False)
        input_ids = tokens['input_ids']
        attention_mask = tokens['attention_mask']
        probabilties = []
        start = 0
        window_size = 510
        total_len = len(input_ids)
        loop = True
        
        while loop:
            end = start + window_size
            if end >= total_len:
                loop = False
                end = total_len
                
            # 1 - Get the tokens for the window
            window_input_ids = input_ids[start:end]
            window_attention_mask = attention_mask[start:end]
            
            # 2 - Append the special tokens [CLS] and [SEP]
            window_input_ids = [101] + window_input_ids + [102]
            window_attention_mask = [1] + window_attention_mask + [1]
            
            # 3 - Convert list to PyTorch tensors
            input_dict = {
                'input_ids' : torch.Tensor([window_input_ids]).long().to(self.device),
                'attention_mask' : torch.Tensor([window_attention_mask]).int().to(self.device)
            }
            
            outpus = self.model(**input_dict)
            
            probability = torch.nn.functional.softmax(outpus[0], dim=-1)
            probabilties.append(probability)
            
            del input_dict, outpus
            torch.cuda.empty_cache()
            
            start = end
        
        return probabilties
    
    def get_mean_from_proba(self, probabilities):
        with torch.no_grad():
            stacks = torch.stack(probabilities)
            stacks = stacks.reshape(stacks.shape[0], stacks.shape[2])
            mean = stacks.mean(dim=0)
        return mean
    
    def get_sentiment(self, text):
        probabilities = self.chunk_text_and_predict_probs(text)
        mean = self.get_mean_from_proba(probabilities)
        sentiment = torch.argmax(mean).item()
        meaning = 'Positive' if sentiment == 1 else 'Negative' if sentiment == 2 else 'Neutral'
        return (sentiment, meaning)
    

if __name__ == '__main__':
    text = 'Tesla got the approval from the Chinese government to sell its Model Y SUV in the country.'
    text2 = 'Tesla did not get the approval from the Chinese government to sell its Model Y SUV in the country.'
    analyzer = ScoreText()
    sentiment_1 = analyzer.get_sentiment(text)
    print(f'Sentiment for text 1 is : {sentiment_1[1]}')
    sentiment_2 = analyzer.get_sentiment(text2)
    print(f'Sentiment for text 2 is : {sentiment_2[1]}')