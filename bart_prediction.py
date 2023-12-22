import torch
import string
from transformers import BartTokenizer, BartForConditionalGeneration

def decode(tokenizer, pred_idx, top_clean):
    ignore_tokens = string.punctuation + '[PAD]'
    tokens = []
    for w in pred_idx:
        token = ''.join(tokenizer.decode(w).split())
        if token not in ignore_tokens:
            tokens.append(token.replace('##', ''))
    return '\n'.join(tokens[:top_clean])

def encode(tokenizer, text_sentence, add_special_tokens=True):
    input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
    mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
    return input_ids, mask_idx

def get_prediction(text, bart_model, bart_tokenizer):
    text += " <mask> ."
    input_ids, mask_idx = encode(bart_tokenizer, text, add_special_tokens=True)
    with torch.no_grad():
        predict = bart_model(input_ids)[0]
    bart = decode(bart_tokenizer, predict[0, mask_idx, :].topk(5).indices.tolist(), 5)
    return bart

def load():
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
    bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large").eval()
    return bart_model, tokenizer