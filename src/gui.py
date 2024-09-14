import gradio as gr
from src.gui_action import *
from src.chain import run
from src.utils.custom_ui_style import UI_Style
# GUI ------------------------------------------------------------
def AI_assistant():
    ui_style = UI_Style()
    
    with gr.Blocks(theme=ui_style) as GUI:
        with gr.Row():
            # First Column: Input Section (Left side)
            with gr.Column(scale=1):
                with gr.Tab("Workspace"):
                    with gr.Row():
                        with gr.Column(scale=1, min_width=400):
                            chat_input = gr.MultimodalTextbox(
                                value={"text": ""}, 
                                interactive=True, 
                                file_types=[".pdf", ".txt"], 
                                file_count='multiple', 
                                placeholder="Enter message or upload file...", 
                                show_label=False
                            )
                # System prompt tab
                with gr.Tab("System prompt"):
                    with gr.Row():
                        txt_system_prompt = gr.Textbox(value=system_message_prompt, label="System prompt", lines=23, min_width=400)
    
                        with gr.Row():
                            with gr.Column(scale=1, min_width=100):
                                btn_save = gr.Button(value="Save")
                                btn_save.click(fn=btn_save_click, inputs=[txt_system_prompt])

                            with gr.Column(scale=1, min_width=100):
                                btn_reset = gr.Button(value="Reset")
                                btn_reset.click(fn=btn_reset_click, inputs=txt_system_prompt, outputs=txt_system_prompt)

            # Second Column: Output Section (Right side)
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(
                    elem_id="chatbot", 
                    bubble_full_width=False, 
                    min_width=600, 
                    height=560, 
                    show_copy_button=True,
                )

                # Kết hợp hàm run để xử lý đầu vào
                def process_input(query):
                    # Nhận input từ user
                    user_message = query["text"]
                    # Chạy hàm run để nhận phản hồi từ AI
                    bot_response = run(user_message)
                    # Trả về dưới dạng một cặp [user_message, bot_response]
                    return [("", bot_response)]
                
                chat_input.submit(fn=process_input, inputs=[chat_input], outputs=[chatbot])

        GUI.launch()
