from utils.prompts import system_message_prompt
from utils.retrieval_db import run_search
from config_app.model_config  import LoadConfig
from utils import Rule_schema
from utils.model_settings import Model_Settings
from utils.convert_file import find_table
from utils import timing_decorator
from logs.logger import set_logging_error, set_logging_terminal
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import json
model_settings = Model_Settings()
APP_CONFIG = LoadConfig()
logging_error = set_logging_error()
logging_terminal = set_logging_terminal()
# class Chain:
@timing_decorator
def run_text(query_text: str):
    logging_terminal.info(f"Query User: {query_text}")
    # search similarity from data -> prompt for llm
    examples = run_search(query_text, APP_CONFIG.retrieval_top_k, APP_CONFIG.threshold)
    prompt_final = system_message_prompt.format(question=query_text, context=examples)
    logging_terminal.info(f"\n{examples}")
    rag_model =  ChatOpenAI(model= model_settings.MODEL_NAME,
            temperature=model_settings.TEMPERATURE,
            max_tokens=model_settings.MAX_TOKEN,
            # top_k=model_settings.TOP_K, 
            top_p=model_settings.TOP_P,
            verbose=True,
        )
    llm_model = rag_model.with_structured_output(Rule_schema)
    response = llm_model.invoke(prompt_final).type
    logging_terminal.info(f"Answer: {response}")
    return response

@timing_decorator
def run_pdf(path_pdf):
    print("====input file pdf====")
    # find_table(path_pdf[0])
    json_file = {
    "1": "12. P.SPCV TC RB Phòng sản phẩm cho vay tín chấp – Khối bán lẻ",
    "2": "13. Phòng KSTT Phòng Kiểm soát tuân thủ",
    "3": "14. P.QLRRDN Phòng quản lý rủi ro doanh nghiệp – Khối quản lý rủi ro tín dụng",
    "4": "15. TCTD Tổ chức tín dụng",
    "5": "16. TSBĐ Tài sản bảo đảm",
    "6": "17. TTBL Trung tâm bán lẻ - Khối bán lẻ",
    "7": "18. TT TTĐ&PDTD Trung tâm tái thẩm định và phê duyệt tín dụng – Khối Quản lý tín dụng",
    "8": "19. TT XLGDTD Trung tâm xử lý giao dịch tín dụng – Khối Quản lý tín dụng",
    "9": "20. Hệ thống T24 Là hệ thống phần mềm dùng để nhập liệu và quản lý dữ liệu của OCB.",
    "10": "21. Hệ thống BPM Là hệ thống phần mềm dùng để trả kết quả KH thỏa/không thỏa điều kiện vay theo chương trình này; thông tin về hạn mức thấu chi và thời hạn của hạn mức thấu chi của KH. Đồng thời, lưu trữ các thông tin này tại hệ thống.",
    "11": "1. Đối tượng khách hàng và phạm vi áp dụng  "}
    
    # search similarity from data -> prompt for llm
    results = []
    for key, query_text in json_file.items():
        examples = run_search(query_text, APP_CONFIG.retrieval_top_k, APP_CONFIG.threshold)
        prompt_final = system_message_prompt.format(question=query_text, context=examples)
        rag_model =  ChatOpenAI(model= model_settings.MODEL_NAME,
                temperature=model_settings.TEMPERATURE,
                max_tokens=model_settings.MAX_TOKEN,
                # top_k=model_settings.TOP_K, 
                top_p=model_settings.TOP_P,
                verbose=True,
            )
        llm_model = rag_model.with_structured_output(Rule_schema)
        response = llm_model.invoke(prompt_final).type
        logging_terminal.info(f"Query text: {query_text} \n")
        logging_terminal.info(f"Answer: {response} \n")
        results.append((query_text, response))
    return results