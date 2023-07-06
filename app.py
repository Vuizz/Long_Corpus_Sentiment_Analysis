from transformers import BertForSequenceClassification, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

def get_sentiment(tokens):
    output = model(**tokens)
    probabilties = torch.nn.functional.softmax(output[0], dim=-1)
    return probabilties

text = """
     We assess [Costco s] forward PEG ratio to be around 2.9, while [Home Depot s] is near 2.1,  Rogovy
said.  Lower PEGs are better, and 1.0 is a good target for typical stocks; however, very stable
businesses can justify higher PEGs, particularly if they pay a consistent dividend. Both [Home
Depot] and [Costco] qualify. While neither looks compelling from this valuation metric, the market
prices them as safe, stable and still-growing businesses.  The PEG ratio is a useful tool for
weighing the investment value of a company, but it s not a magic tool that definitively answers
whether a company is a smart investment or not.  If it were that easy, a simple spreadsheet would be
the best investment manager,  Rogovy said.  Both companies exhibit numerous qualitative measures of
investment quality.   Costco s economic moat is unmatched, with its massive scale allowing it to
control negotiations with suppliers and pass on cost savings to customers,  Allen said.  Its global
membership renewal rate is impressive at 90.5%, and its revenue has increased at a compound annual
rate of 12% over the past five years. However, its current price-to-earnings (P/E) ratio of 38 is
quite high.  On the other hand, Home Depot is the undisputed leader in the home improvement market,
with half of its revenue coming from DIY customers and the other half from professional customers,
Allen said.  Despite recent inflationary pressures, there s a huge opportunity for the business to
continue expanding. Its shares trade at a P/E multiple of 18, a meaningful discount to its rival
Lowe s.  If pricing is a concern, it s worth noting that Home Depot shares ($308.96 a share as of
the morning of June 28, 2023) are currently much more affordable than Costco shares (priced at
$533.92 as of the morning of June 28, 2023 ). But in the opinion of Rogovy, Costco appears to have
the edge in market structure, which could, arguably, make it a better buy than Home Depot.  [Costco]
is in a league of its own,  Rogovy said.  [Its] business really is unique. I don t see any serious
competitors.  Charlie Munger, who works with Warren Buffett, has also publicly expressed his
appreciation of Costco as an investor   despite its presently pricey bar to entry.  Last year Munger
said,  I m not saying I m buying Costco at this price. But I m certainly not selling any,'  Rogovy
noted. Munger went on to say of Costco,  I think it s going to be a big, powerful company as far
ahead as you can see. And I think it deserves its success. I think it has a good culture and a good
moral ethos. And so I wish everything else in America was working as well as Costco does. Think what
a blessing that would be for us all.  Despite all this, there s a case to be made that based on
their sky-high prices at the moment, neither Costco or Home Depot are necessarily smart buys right
now.  At the current prices, I would not recommend either,  said Merry, who owns stock in both
companies.  It will take some time for either to recover, and the stock market is really volatile
right now.  More From GOBankingRates
"""

tokens = tokenizer(text, add_special_tokens=False)

input_ids = tokens['input_ids']
attention_mask = tokens['attention_mask']


def chunk_text_and_predict_probs(input_ids, attention_mask):
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
            'input_ids' : torch.Tensor([window_input_ids]).long(),
            'attention_mask' : torch.Tensor([window_attention_mask]).int()
        }

        outpus = model(**input_dict)

        probability = torch.nn.functional.softmax(outpus[0], dim=-1)
        probabilties.append(probability)
    
    return probabilties

probabilties = chunk_text_and_predict_probs(input_ids, attention_mask)

def get_mean_from_proba(proba_list):
    with torch.no_grad():
        stacks = torch.stack(proba_list)
        stacks = stacks.resize(stacks.shape[0], stacks.shape[2])
        mean = stacks.mean(dim=0)
    return mean

mean = get_mean_from_proba(probabilties)

torch.argmax(mean).item()