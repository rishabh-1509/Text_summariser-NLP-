from text_summarizer.config.configuration import ConfigurationManager
from text_summarizer.compnents.data_validation import DataValidation
from text_summarizer.logging import logger 



class DataValidationTrainingPipeline:
    def __init__(self):
        pass 
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataValidation(config= data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()

