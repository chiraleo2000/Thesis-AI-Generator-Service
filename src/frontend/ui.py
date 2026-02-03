import gradio as gr
from src.backend.auth import authenticate_user, register_user
from src.backend.database import get_user_history
from src.backend.processor import (
    phase1_process_files,
    phase2_generate_outline,
    phase3_write_content,
    phase4_evaluate_and_export,
    GEMINI_MODEL
)

def create_ui():
    """
    Constructs the UI with Login, Register, Main App, and History.
    """
    with gr.Blocks(title="Thesis AI Generator", theme=gr.themes.Soft(primary_hue="indigo")) as demo:
        
        # State variables
        current_username = gr.State("")
        context_state = gr.State("") # To hold the extracted text context

        # --- Authentication Screens ---
        with gr.Group(visible=True) as auth_group:
            gr.Markdown("# 🔐 Thesis AI Generator: Secure Access")
            
            with gr.Tabs() as auth_tabs:
                with gr.TabItem("Login"):
                    login_user = gr.Textbox(label="Email / Username")
                    login_pass = gr.Textbox(label="Password", type="password")
                    login_btn = gr.Button("Login", variant="primary")
                    login_msg = gr.Textbox(label="Status", interactive=False)
                
                with gr.TabItem("Register"):
                    reg_user = gr.Textbox(label="New Email / Username")
                    reg_pass = gr.Textbox(label="New Password", type="password")
                    reg_confirm = gr.Textbox(label="Confirm Password", type="password")
                    reg_btn = gr.Button("Register New Account (Firebase/Local)")
                    reg_msg = gr.Textbox(label="Registration Status", interactive=False)

        # --- Main Application Interface (Hidden by default) ---
        with gr.Group(visible=False) as app_group:
            with gr.Row():
                gr.Markdown(f"# 🎓 Thesis AI Generator\n**Powered by Google Cloud & {GEMINI_MODEL}**")
                
                with gr.Column(scale=0, min_width=150):
                    user_display = gr.Markdown("User: ...")
                    logout_btn = gr.Button("Logout", size="sm", variant="secondary")
            
            with gr.Tabs():
                # Phase 1
                with gr.TabItem("1. Digital Capture"):
                    gr.Markdown("### Phase 1: Data Ingestion & Structuring")
                    file_input = gr.File(label="Upload Research/Data (PDF, Docx)", file_count="multiple")
                    p1_btn = gr.Button("Process with Document AI", variant="primary")
                    p1_status = gr.Textbox(label="Processing Log", lines=4)
                    p1_files = gr.JSON(label="Indexed Knowledge Base")
                    
                    p1_btn.click(phase1_process_files, inputs=[file_input, current_username], outputs=[p1_status, p1_files, context_state])

                # Phase 2
                with gr.TabItem("2. Outline"):
                    gr.Markdown(f"### Phase 2: Generate Outline ({GEMINI_MODEL})")
                    topic_input = gr.Textbox(label="Research Topic")
                    p2_btn = gr.Button("Generate Outline", variant="primary")
                    outline_output = gr.Code(label="Thesis Structure", language="markdown", lines=15, interactive=True)
                    
                    p2_btn.click(phase2_generate_outline, inputs=[topic_input, context_state, current_username], outputs=[outline_output])

                # Phase 3
                with gr.TabItem("3. Synthesis"):
                    gr.Markdown(f"### Phase 3: Writing ({GEMINI_MODEL} + RAG)")
                    with gr.Row():
                        chapter_sel = gr.Dropdown(["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5"], label="Select Chapter")
                        instr_input = gr.Textbox(label="Instruction")
                    
                    p3_btn = gr.Button("Write Draft", variant="primary")
                    content_output = gr.Markdown(label="Drafted Content")
                    
                    p3_btn.click(phase3_write_content, inputs=[chapter_sel, outline_output, instr_input, current_username], outputs=[content_output])

                # Phase 4
                with gr.TabItem("4. Export"):
                    gr.Markdown("### Phase 4: Finalize")
                    p4_btn = gr.Button("Evaluate & Export", variant="secondary")
                    eval_output = gr.Textbox(label="Quality Report", lines=3)
                    download_file = gr.File(label="Download")
                    
                    p4_btn.click(phase4_evaluate_and_export, inputs=[content_output, current_username], outputs=[eval_output, download_file])

                # History Tab
                with gr.TabItem("🕰️ Service History"):
                     gr.Markdown("### Your Activity Log (Cloud SQL)")
                     history_btn = gr.Button("Refresh History")
                     history_table = gr.Dataframe(headers=["Time", "Action", "Status", "Details"])
                     
                     history_btn.click(get_user_history, inputs=[current_username], outputs=[history_table])

        # --- Interactions ---
        
        def try_login(u, p):
            success, msg = authenticate_user(u, p)
            if success:
                return {
                    auth_group: gr.update(visible=False),
                    app_group: gr.update(visible=True),
                    login_msg: msg,
                    current_username: u,
                    user_display: f"User: {u}"
                }
            return {login_msg: msg}

        def try_register(u, p, c):
            success, msg = register_user(u, p, c)
            return msg

        def do_logout():
            return {
                auth_group: gr.update(visible=True),
                app_group: gr.update(visible=False),
                login_user: "",
                login_pass: "",
                current_username: ""
            }

        login_btn.click(
            try_login, 
            inputs=[login_user, login_pass], 
            outputs=[auth_group, app_group, login_msg, current_username, user_display]
        )
        
        reg_btn.click(
            try_register,
            inputs=[reg_user, reg_pass, reg_confirm],
            outputs=[reg_msg]
        )
        
        logout_btn.click(
            do_logout,
            inputs=None,
            outputs=[auth_group, app_group, login_user, login_pass, current_username]
        )

    return demo
