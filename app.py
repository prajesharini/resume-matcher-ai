import gradio as gr
import os
import tempfile
import pandas as pd
from utils import extract_resume_text, get_match_score

def process(jd_text, jd_file, resumes):
    if not jd_text and not jd_file:
        return "❌ Please provide a job description.", None, None

    if jd_file:
        jd_text = jd_file.decode("utf-8")

    result_str = ""
    csv_data = []

    for resume in resumes:
        # resume is a byte object with filename metadata
        resume_name = getattr(resume, "name", "uploaded_resume")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(resume)
            temp_path = temp.name

        try:
            resume_text = extract_resume_text(temp_path)
            score = get_match_score(jd_text, resume_text)
            percentage = round(score * 100, 2)
            suggestion = "✅ Suggested" if score >= 70 else "❌ Not strong"

            result_str += f"\n\n📄 **{resume_name}**\nMatch Score: {percentage}%\nRecommendation: {suggestion}\n"

            csv_data.append({
                "Filename": resume_name,
                "Match Score (%)": percentage,
                "Recommendation": suggestion
            })

        except Exception as e:
            result_str += f"\n\n⚠️ Error processing {resume_name}: {str(e)}\n"

    df = pd.DataFrame(csv_data)
    csv_path = "results.csv"
    df.to_csv(csv_path, index=False)

    return result_str.strip(), csv_path

with gr.Blocks(title="Resume Matcher AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧠 Resume Matcher AI by Bruhh")
    gr.Markdown("Match multiple resumes with a job description and get smart insights!")

    with gr.Row():
        jd_input = gr.Textbox(label="Paste Job Description", lines=8, placeholder="Or upload as .txt")
        jd_file = gr.File(label="Or Upload JD (.txt)", file_types=[".txt"], type="binary")
        resumes = gr.File(label="Upload Resumes (.pdf, .doc, .docx)", file_types=[".pdf", ".doc", ".docx"], file_count="multiple", type="binary")

    submit_btn = gr.Button("🔍 Match Now")

    output_box = gr.Textbox(label="Results", lines=10, interactive=False)
    download_btn = gr.File(label="📥 Download CSV")

    submit_btn.click(
        fn=process,
        inputs=[jd_input, jd_file, resumes],
        outputs=[output_box, download_btn]
    )

if __name__ == "__main__":
    demo.launch()
