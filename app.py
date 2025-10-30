import os
import gradio as gr
from interview import generate_question, give_feedback

with gr.Blocks() as demo:
    gr.Markdown("# 🧑‍🏫 AI 模擬面試官互動系統")
    
    with gr.Row():
        # 左側
        with gr.Column():
            position = gr.Textbox(label="應徵職位", placeholder="例如：AI 工程師")
            intro = gr.Textbox(label="自我介紹", placeholder="簡短背景", lines=3)
            skills = gr.Textbox(label="技能", placeholder="Python / ML / RAG ...")
            project = gr.Textbox(label="專案經驗", placeholder="重點專案", lines=3)
            
            difficulty = gr.Radio(
                choices=["初級", "中級", "高級"],
                value="中級",
                label="難度"
            )
            question_type = gr.Radio(
                choices=["技術問題", "情境問題", "混合"],
                value="技術問題",
                label="題型"
            )
            
            generate_btn = gr.Button("📌 生成面試問題")
        
        # 右側
        with gr.Column():
            question_output = gr.Textbox(label="AI 生成的面試問題", lines=5)
            answer_input = gr.Textbox(label="你的回答", lines=6)
            feedback_btn = gr.Button("📋 送出回答並獲得回饋")
            feedback_output = gr.Textbox(label="AI 給你的回饋", lines=10)
            
            with gr.Row():
                next_btn = gr.Button("下一題")
                end_btn = gr.Button("結束")
    
    generate_btn.click(
        generate_question,
        inputs=[position, intro, skills, project, difficulty, question_type],
        outputs=question_output
    ).then(
        lambda: "",
        outputs=feedback_output
    )
    
    feedback_btn.click(
        give_feedback,
        inputs=answer_input,
        outputs=feedback_output
    )
    
    next_btn.click(
        generate_question,
        inputs=[position, intro, skills, project, difficulty, question_type],
        outputs=[question_output]
    ).then(
        lambda: ("", ""),
        outputs=[answer_input, feedback_output]
    )
    
    end_btn.click(
        lambda: ("面試已結束，感謝您的練習！", "", ""),
        outputs=[question_output, answer_input, feedback_output]
    )

demo.launch(server_name="127.0.0.1", server_port=7861, inbrowser=True, show_error=True, debug=True)