from pypdf import PdfReader
import camelot
# The first extract all -> filter -> llm
# pdf_path = "/home/luanhille/Documents/LLM_bank/llm_ver1/data/237.1quydinhtindung.pdf"
# reader = PdfReader(pdf_path)
# page_len = len(reader.pages)
# print(page_len)
# table_list = camelot.read_pdf(pdf_path, pages=str(6))
# print(table_list[0].df)
def find_page(pdf_path, keys, type):
    reader = PdfReader(pdf_path)
    page_i = []
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        
        check = True
        for key in keys:
            if key.lower() not in text.lower():
                check = False
        if check:
            # print(i)
            page_i.append(i)
    return page_i
                
def get_table_from_pdf(path: str, first_page, last_page, type):
    table_dfs = []
    if first_page + 3 < last_page:
        for page in range(first_page, first_page + 2):
            table_list = camelot.read_pdf(path, pages=str(page))
            
            if len(table_list) == 0:
                print('table_list', table_list)
                return table_list
            else:
                for i in range(len(table_list)):
                    # if i > 0 and type != 'Đối tượng KH':
                    #     break
                    table_df = table_list[i].df
                    # print(table_df)
                    table_dfs.append(table_df)
                    
    return table_dfs

def table2list(table_dfs):
    '''
    row -> list
    '''
    # k table
    result = []
    for k in range(len(table_dfs)):
        table_df = table_dfs[k]
        # row
        for i in range(len(table_df[0])):
            # column
            s = []
            for j in table_df.columns:
                s.append(table_df[j][i].replace("\n", ''))
        
            result.append(s)
    return result

import re
def is_new_title(row):
    return bool(re.match(r'^\d+(\.\d+)?\.?$', row[0]))

def find_text(table_dfs):
    result = table2list(table_dfs)
    text = []
    current_row = None
    for row in result:
        if is_new_title(row):
            current_row = row
        elif len(row[0]) == 0:
            # print('row none', row)
            if current_row:
                current_row = [current_row[i] + ' ' + row[i] if row[i] else current_row[i] for i in range(len(row))]
                text.extend(current_row)
    return text

def find_table(path_pdf, type):
    reader = PdfReader(path_pdf)
    page_len = len(reader.pages)
    # print(pape_len)
    if type == "Customer_object":
        page_location = find_page(path_pdf, ['Đối tượng KH'], type)
    result = []
    for page_i in page_location:
        table_dfs = get_table_from_pdf(path_pdf, page_i+1, page_len+1, type)
        # print(table_dfs, ' ----- ', page_i)
        # result.append(find_text(table_dfs))
        print('------result-----',find_text(table_dfs))
    print(result)
    # return result
        
def main_pdf(path):
    result = {
        'Customer_object': {},
        'Age': {},
        'Residence': {}
    }
    
    result['Customer_object'] = find_table(path, 'Customer_object')
    # result['Age'] = find_table(path, "Age")
    # result['Residence'] = find_table(path, "Residence")
    
    return result

path = '/home/luanhille/Documents/LLM_bank/llm_ver1/data/237.01_P.SPCVTC_ Quyết định Sản phẩm cho vay tieu dung khong TSBD cho KHCN nhan luong qua tai khoan ngan hang (1) 1.pdf'
print(main_pdf(path))