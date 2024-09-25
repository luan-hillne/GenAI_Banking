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
    current_key = None
    output_file = 'data/output.txt'
    with open(output_file, 'w') as f:
        for row in result:
            if is_new_title(row[0]) or is_new_title(row[1]):
                if current_row:
                    text_dict[current_key] = " ".join(current_row)
                    current_row = None
                if is_new_title(row[0]):
                    current_key = row[0]
                elif is_new_title(row[1]):
                    current_key = row[1]
                    
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
    
# path = '/home/luanhille/Documents/LLM_bank/llm_ver1/data/237.01_P.SPCVTC_ Quyết định Sản phẩm cho vay tieu dung khong TSBD cho KHCN nhan luong qua tai khoan ngan hang (1) 1.pdf'
# print(find_table(path))