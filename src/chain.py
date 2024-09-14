from src.utils.prompts import system_message_prompt
from src.retrieval_db import run_search
from config_app.model_config  import LoadConfig
from src.utils.base_model import Rule_schema
from src.utils.model_settings import Model_Settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

model_settings = Model_Settings()
APP_CONFIG = LoadConfig()
# class Chain:
def run(query_text: str):
    
    # search similarity from data -> prompt for llm
    examples = run_search(query_text, APP_CONFIG.retrieval_top_k, APP_CONFIG.threshold)
    prompt_final = system_message_prompt.format(question=query_text, context=examples)
    print('Question: ', query_text)
    rag_model =  ChatOpenAI(model= model_settings.MODEL_NAME,
            temperature=model_settings.TEMPERATURE,
            max_tokens=model_settings.MAX_TOKEN,
            # top_k=model_settings.TOP_K, 
            top_p=model_settings.TOP_P,
            verbose=True,
        )
    llm_model = rag_model.with_structured_output(Rule_schema)
    response = llm_model.invoke(prompt_final).type
    print('Answer: ', response)
    return response
        