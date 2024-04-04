from transformers import AutoModelForSeq2Seq , AutoTokenizer
from datasets import load_dataset , load_from_disk
import torch
import pandas as pd
from tqdm import tqdm 
from text_summarizer.entity import ModelEvalutionConfig

class ModelEvalution:
    def __init__(self, config: ModelEvalutionConfig):
        self.config = config
    
    def generate_batch_size_chunks(self, list_of_element, batch_size):
        """ split the dataset into smaller batches that we process simultanes vield  succusive batch-sized chunks from list_of_element """
        for i in range(0, len(list_of_element), batch_size):
            yield list_of_element[i:i + batch_size]
    
    def calculate_metric_on_test_ds(self, dataset,metric, model,tokenizer, batch_size = 16 , device  = "cuda" if torch.cuda.is_available() else "cpu ",
                                    column_text = "article",column_summary = "highlights"):
        article_batch = list(self.generate_batch_size_chunks(dataset[column_text],batch_size))
        target_batch = list(self.generate_batch_size_chunks(dataset[column_summary],batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batch,target_batch),total=len(article_batch)):

            input =  tokenizer(article_batch,max_length = 1024 ,  truncation = True , padding = "max_length", return_tensors = "pt")


            summaries =  model.genrate(input_ids = input["input_ads"].to(device),
                                       attention_mask = input["attention_mask"].to(device),
                                       length_penalty =0.8 , num_beams = 8 , max_length = 128)
        '''parameter for length penalty ensure that the model does not genrate sequence that are too long '''

        #finaly we decode the genrated texts,
        #replacee the token, and add the decoded text with refrence to the metric .

        decoded_summaries = [tokenizer.decode(s, skip_special_tokens = True,
                                              clean_up_tokenisation =True)
                                              for s in summaries]
        decoded_summaries = [d.relace("" , " ") for d in decoded_summaries ]


        metric.add_batch(prediction =  decoded_summaries , refrences = target_batch )
    #finaly compute and return the Rouge score.
        score =  metric.compute()
        return score
 
    def evalute(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus = AutoModelForSeq2Seq.from_pretrained(self.config.model_path).to(device)
        # loading data
        dataset_samsum_pt =  load_from_disk(self.config.data_path)

        rouge_names = ["rough1", "rough2", "rough3"]

        rouge_metric = load_metric('rouge')

        score = self.calculate_metric_on_test_ds(dataset_samsum_pt['test'][0:10], rouge_metric, model_pegasus,tokenizer,batch_size = 2 ,column_text= 5)

        rouge_dict =  dict((rn,score[rn].mid.fmeasure) for rn in rouge_names)

        df = pd.DataFrame(rouge_dict,index =['pegasus'])
        df.to_csv(self.config.metric_file_name ,  index= False )
            