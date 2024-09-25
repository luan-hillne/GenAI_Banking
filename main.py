'''
build gradio
'''
from src.gui import AI_assistant
# from src.chain import run
# query_text = '''
# - KH có Hợp đồng lao động không xác định thời hạn/Hợp đồng lao động có thời hạn từ 12 tháng trở lên, và
# - Thời gian làm việc tối thiểu tại đơn vị hiện tại (không bao gồm thời gian thử việc): 06 tháng và có kinh nghiệm công tác tối thiểu 12 tháng tại tất cả các Đơn vị KH đã từng công tác. Cơ sở xác định kinh nghiệm căn cứ vào HĐLĐ/Quyết định bổ nhiệm/Nâng bậc, nâng lương hoặc các chứng từ khác thể hiện được thời gian làm việc của KH.
# '''

# print(run(query_text))
if __name__ == "__main__":
    try:
        AI_assistant()  
    except Exception as e:
        # Handle maintenance error or other exceptions
        print("System is under maintenance. Please try again later.")