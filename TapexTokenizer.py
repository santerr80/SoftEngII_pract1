from transformers import TapexTokenizer, BartForConditionalGeneration
import pandas as pd

def tapex_tokenizer(my_table, my_query):
    
      
    tokenizer = TapexTokenizer.from_pretrained("microsoft/tapex-large-finetuned-wtq")
    
    model = BartForConditionalGeneration.from_pretrained("microsoft/tapex-large-finetuned-wtq")
    
    encoding = tokenizer(table=my_table, query=my_query, return_tensors="pt")
    
    outputs = model.generate(**encoding)
    
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)

