import training.cramming
from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch
import time

def encode(tokenizer, text_sentence, add_special_tokens=True):
    input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
    mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
    return input_ids, mask_idx

def get_prediction(text):
    ultrafast_tokenizer = AutoTokenizer.from_pretrained("pbelcak/UltraFastBERT-1x11-long")
    model = AutoModelForMaskedLM.from_pretrained("pbelcak/UltraFastBERT-1x11-long").eval()
    text += " <mask> ."
    start_time = time.time()
    input_ids, mask_idx = encode(ultrafast_tokenizer, text)
    with torch.no_grad():
        predict = model(input_ids)['outputs']

    predict_words = ultrafast_tokenizer.convert_ids_to_tokens(predict[mask_idx, :].topk(5).indices.tolist())
    print(predict_words)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    return predict_words[0]

pred = get_prediction("The examination and testimony of the experts enabled the Commission")
print(pred)
