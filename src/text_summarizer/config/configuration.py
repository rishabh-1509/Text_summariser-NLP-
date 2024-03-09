from text_summarizer.constants  import *
from text_summarizer.utlis.common import read_yaml,create_directories
from text_summarizer.utlis.common import (DataIngestionConfig)

class configurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH
            ):

            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            create_directories([self.config.artifacts_root])
    