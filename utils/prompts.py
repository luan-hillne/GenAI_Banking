system_message_prompt = '''
NHIỆM VỤ: Bạn được yêu cầu chuyển đổi đoạn văn bản thành các quy tắc logic.

Bước 1: Phân tích nội dung và xác định các cụm từ có thể chuyển thành biến. 
    Ví dụ:
    - Quốc tịch: NATIONALITY
    - Phân khúc khách hàng: CUSTOMER_SEGMENT
    - Nguồn thu nhập: PAYMENT_SOURCE
    - Hình thức nhận thu nhập: PAYMENT_METHOD
    - Thời gian làm việc tại đơn vị hiện tại (không bao gồm thời gian thử việc): CURRENT_JOB_DURATION
    - Kinh nghiệm làm việc của khách hàng: WORK_EXPERIENCE
    - Thời hạn hợp đồng lao động: CONTRACT_TERM
    - Thời hạn hợp đồng lao động còn lại: REMAINING_CONTRACT_TERM
    - Giới tính khách hàng: CUSTOMER_GENDER
    - Tuổi khách hàng: CUSTOMER_AGE
    - Quốc gia thành phố thường trú: RESIDENT_CITY_COUNTRY
    - Chỉ báo nơi cư trú hiện tại và nơi phát sinh phương án vay vốn cùng địa bàn: FLAG_SAME_CITY
    - Thành phố đơn vị kinh doanh cho vay: BRANCH_CITY
    - Khoảng cách tới đơn vị kinh doanh cho vay: DISTANCE_TO_BRANCH_CITY
    - Xếp hạng tín dụng nội bộ: SCORECARD_RANK
    - Bảo hiểm xã hội liên tục: CONTINOUS_MONTHS_SOCIAL_INSURANCE
    - Không cấp, không: not in
    - Và: and
    - Tối thiểu: Min
    - Tối đa: Max
Bước 2: 
    - Tạo các quy tắc logic đầu ra dựa trên văn bản đầu vào, cố gắng sử dụng các biến đã xác định ở bước 1, các biến phải chuyển đổi về tiếng anh 
    - Biến và nội dung khởi tạo bắt buộc phải được kết nối với nhau bắng ["=", ">", "<", ">=", "<=", "in", "not in"] hoặc <and>, <thn>, <eor> tùy vào ngữ cảnh
    - Kết luận <then> 1 trong các điều kiện sau:
        - Điều kiện khách hàng: CUSTOMER_CONDITION
        - Điều kiện việc làm: JOB_CONDITION
        - Điều kiện nơi cư trú: RESIDENT_CONDITION
        - Điều kiện độ tuổi: AGE_CONDITION
        - Điều kiện xếp hạng tín dụng: SCORECARD_RANK
    
    Ví dụ:\n\n{context}

Bước 3: 
    - Kiểm tra kỹ rằng quy tắc bạn tạo ra là đúng và hợp lệ trước khi đưa ra câu trả lời cuối cùng.
    - Khi tạo quy tắc, nếu có từ khóa không hợp lệ như <or>, <else>, cần thay thế chúng bằng các từ khóa hợp lệ là <and>, <thn>, <eor>. Cố gắng tạo quy tắc mà không sử dụng các từ khóa <or>, <else>.
    - Các toán tử phải là một trong những toán tử sau: ["=", ">", "<", ">=", "<=", "in", "not in"].
\nCâu hỏi: {question}:


'''