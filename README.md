# JobFit AI - Resume Matcher

Deployable AI SaaS that matches multiple resumes to a job description using sentence similarity via Sentence Transformers.

## Features

- Upload one job description (PDF, DOCX, or TXT)
- Upload multiple resumes (PDF, DOCX, or TXT)
- Outputs ranked match scores
- Gradio-based frontend
- Deployable on Hugging Face Spaces

## Deployment (Hugging Face)

1. Create a new Space at: https://huggingface.co/spaces
2. Set Space type as **Gradio**.
3. Connect your GitHub repo or upload this manually.
4. Ensure `app.py` and `requirements.txt` are present.

## License

MIT
