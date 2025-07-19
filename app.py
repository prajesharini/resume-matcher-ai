import gradio as gr
import os
import tempfile
import pandas as pd
from utils import extract_resume_text, get_match_score

def process(jd_text, jd_file, resumes):
    if not jd_text and not jd_file:
        return "❌ Please provide a job description (text or file).", None

    # Load JD
    if jd_file:
        jd_text = jd_file.read().decode("utf-8")

    results = []
    for resume in resumes:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(resume.read())
            temp_path = temp.name

        try:
            resume_text = extract_resume_text(temp_path)
            score = get_match_score(jd_text, resume_text)
            percentage = round(score * 100, 2)
            results.append({
                "Filename": resume.name,
                "Match Score (%)": percentage,
                "Recommendation": "✅ Suggested" if score >= 0.7 else "❌ Not strong"
            })
        except Exception as e:
            results.append({
                "Filename": resume.name,
                "Match Score (%)": "Error",
                "Recommendation": f"⚠️ {e}"
            })

    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    return df, "results.csv"

# UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Resume Matcher AI")
    
    with gr.Row():
        jd_input = gr.Textbox(label="Job Description (or leave empty if uploading)", lines=8, placeholder="Paste your JD here...")
        jd_file = gr.File(label="OR Upload JD as .txt", file_types=[".txt"], type="binary")
    
    resumes = gr.File(label="Upload Resumes (.pdf, .doc, .docx)", file_types=[".pdf", ".doc", ".docx"], file_count="multiple")
    submit_btn = gr.Button("🔍 Match Resumes")

    output_df = gr.Dataframe(headers=["Filename", "Match Score (%)", "Recommendation"], label="Results")
    download_link = gr.File(label="📥 Download Results (CSV)")

    submit_btn.click(fn=process, inputs=[jd_input, jd_file, resumes], outputs=[output_df, download_link])

if __name__ == "__main__":
    demo.launch()
