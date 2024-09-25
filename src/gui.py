import gradio as gr
from src.gui_action import *
from src.handler import run_text, run_pdf
from utils.custom_ui_style import UI_Style
# GUI ------------------------------------------------------------
def AI_assistant():
    default_ui = "gradio/default"
    
    with gr.Blocks(theme=default_ui) as GUI:
        with gr.Row():
            # First Column: Input Section (Left side)
            with gr.Column(scale=1):
                with gr.Row():
                    gr.HTML("<a href='http://127.0.0.1:7860/' target='_self' style='text-decoration: none;'>White</a> | <a href='http://127.0.0.1:7860/?__theme=dark' target='_self' style='text-decoration: none;'>Dark</a>")
                
                # with gr.Tab("Workspace"):
                    # with gr.Row():
                    #     with gr.Column(scale=1, min_width=400):
                            
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
                
                def process_input(user_input):
                    text = user_input['text']
                    print("input_:", user_input)
                    pdf_file = user_input.get('files', None)
                    bot_response = "No valid input received"
                    result = []
                    if text:
                        # query_text = user_input
                        bot_response = run_text(text)
                        print("---response---", bot_response)
                        result.append(("", bot_response))
                    elif pdf_file is not None:
                        bot_response = run_pdf(pdf_file)
                        result.extend(bot_response)
                    return result
                
                chatbot = gr.Chatbot(
                    elem_id="chatbot", 
                    bubble_full_width=False, 
                    min_width=600, 
                    height=700, 
                    show_copy_button=True,
                )
                chat_input = gr.MultimodalTextbox(
                                value={"text": ""}, 
                                interactive=True, 
                                file_types=[".pdf", ".txt"], 
                                file_count='multiple', 
                                placeholder="Enter message or upload file...", 
                                show_label=False
                            )
                chat_input.submit(fn=process_input, inputs=[chat_input], outputs=[chatbot])
                
        GUI.launch()
