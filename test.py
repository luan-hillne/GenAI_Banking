from pypdf import PdfReader
import camelot
import time
import json 
# The first extract all -> filter -> llm
# pdf_path = "/home/luanhille/Documents/LLM_bank/llm_ver1/data/237.1quydinhtindung.pdf"
# reader = PdfReader(pdf_path)
# page_len = len(reader.pages)
# print(page_len)
# table_list = camelot.read_pdf(pdf_path, pages=str(6))
# print(table_list[0].df)
"""
    Extracts all tables from a PDF file.

    Parameters:
    path (str): The path to the PDF file.
    page_len (int): The number of pages in the PDF to process.

    Returns:
    list: A list of pandas DataFrames for each table extracted from the PDF.
    """
                
def get_table_from_pdf(path: str, page_len: int):
    table_dfs = []
    not_table = []
    for page in range(5, page_len + 1):
        table_list = camelot.read_pdf(path, pages=str(page))
        
        if len(table_list) == 0:
            print(f"No tables found on page {page}.")
            not_table.append(page)
            # continue
        else:
        # Append each table from the page to the result list
            for i in range(len(table_list)):
                table_df = table_list[i].df
                table_dfs.append(table_df)
    
    return table_dfs

def table2list(table_dfs):
    '''
    row -> list
    '''
    # k table
    result = []
    output_file = "data/doc.txt"
    with open(output_file, 'w') as f:
        for k in range(len(table_dfs)):
            table_df = table_dfs[k]
            # row
            for i in range(len(table_df[0])):
                # column
                s = []
                for j in table_df.columns:
                    s.append(table_df[j][i].replace("\n", ''))
                print("====", s)
                f.write(f"{' '.join(s)}\n")
                result.append(s)
    return result

import re

def is_new_title(row):
    # Check for numeric patterns like '2.3' or '2.'
    if re.match(r'^\d+(\.\d+)?\.?$', row):
        return True
    # Check for Roman numerals (I, II, III, ...)
    elif re.match(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\.?$', row):
        return True
    # Check for patterns like '2.3   Xếp'
    elif re.match(r'^\d+(\.\d+)?\s+\w+', row):
        return True
    else:
        return False
 

def find_text(table_dfs):
    result = table2list(table_dfs)
    text = []
    current_row = None
    key_found = False
    text_dict = {}
    current_key = 0
    output_file = 'data/output.json'
    for row in result:
        if is_new_title(row[0]) or is_new_title(row[1]):
            if current_row:
                text_dict[current_key] = " ".join(current_row)
                current_row = None
            current_key += 1
            current_row = row
            key_found = True
        elif len(row[0]) == 0 and current_row and key_found:
            try:
                # Đảm bảo rằng các hàng có cùng độ dài trước khi gộp
                if len(current_row) == len(row):
                    if row[0].strip() == '' and row[1]:
                        new_row = row[1:] + ['']
                        current_row = [current_row[i] + ' ' + new_row[i] if new_row[i] else current_row[i] for i in range(len(row))]
                    else:
                        current_row = [current_row[i] + ' ' + row[i] if row[i] else current_row[i] for i in range(len(row))]
                
                elif len(current_row) < len(row):
                    current_row = [current_row[i] + ' ' + row[i] if row[i] else current_row[i] for i in range(len(current_row))]
                
                elif len(current_row) > len(row):
                    current_row = [current_row[i] + ' ' + row[i] if row[i] else current_row[i] for i in range(len(row))]
                
                else:
                    print("Warning: current_row and row have different lengths.")
            except IndexError as e:
                print(f"IndexError: {e}. Skipping row.")
                    
        if current_row:
            # f.write(" ".join(current_row) + "\n")
            text_dict[current_key] = " ".join(current_row)
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(text_dict, f, ensure_ascii=False, indent=4)
    return ''

def find_table(path_pdf):
    reader = PdfReader(path_pdf)
    page_len = len(reader.pages)
    t1 = time.time()
    table_dfs = get_table_from_pdf(path_pdf, page_len)
    print('------Upload file sucessful-----',find_text(table_dfs))
    print(time.time() - t1)
    
path = '/home/luanhille/Documents/LLM_bank/llm_ver1/data/237.01_P.SPCVTC_ Quyết định Sản phẩm cho vay tieu dung khong TSBD cho KHCN nhan luong qua tai khoan ngan hang (1) 1.pdf'
print(find_table(path))

# ├── app.py                              # demo on gradio app
# ├── configs
# │   ├── config_fewshot                  # config cho elastic search và các ví dụ fewshot
# │   │   ├── enum.py
# │   │   ├── example_fewshot.yml
# │   ├── config.yml
# │   ├── __init__.py
# │   ├── load_config.py
# ├── data
# │   ├── Cau_hoi_thuong_gap.csv          # file chứa các câu hỏi thường gặp của khách hàng
# │   ├── dieu_hoa.csv                    # file sản phẩm điều hòa
# │   ├── product_final_300_extract.xlsx  # file tất cả các sản phẩm
# │   └── vector_db                       # folder lưu embedding của sản phẩm và câu hỏi thường gặp
# │       ├── Cau_hoi_thuong_gap
# │       │   └── chroma.sqlite3
# │       └── dieu_hoa
# │           └── chroma.sqlite3
# ├── elastic_search                      # folder chưa code sử dụng elastic search để search thông tin sp
# │   ├── few_shot_sentence.py
# │   ├── indexing_db.py
# │   └── retrieval.py
# ├── images                              # ảnh giao diện app
# │   ├── avt_bot.png
# │   ├── avt_vcc.png
# │   └── image.png
# ├── logs                                # chứa 3 loại log: thông tin, lỗi, thời gian
# │   ├── error
# │   ├── logger.py
# │   ├── terminal
# │   └── times
# ├── README.md                       
# ├── requirements.txt                    # các thư viện yêu cầu của project
# ├── source
# │   ├── generater.py                    # file chat chính 
# │   ├── load_db.py                      # load vector embedding
# │   ├── retriever.py                    # file khởi tạo retrieval và lấy context 
# │   └── router.py                       # router điều hướng: elastic search, chroma db, tương tự, tồn kho
# ├── test_code.py
# └── utils                               # các file code sử dụng cho cho các file khác
#     ├── base_model.py                   # base model        
#     ├── caculate_time.py                # tính thời gian
#     ├── data_process.py                 # convert csv to text
#     ├── __init__.py                     # import các thư viện từ module utils
#     └── prompt.py                       # chưa toàn bộ prompt cho LLM

# |___ 