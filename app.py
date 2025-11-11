import os
import re
import json
import markdown
import requests
from flask import Flask, render_template, request, jsonify, send_file, session
from io import BytesIO
from dotenv import load_dotenv
from fpdf import FPDF
from docx import Document
import csv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

def generate_blog(title, details="", api_key=None):
    """Generate a blog using Gemini or Perplexity API."""
    print(f"Generating blog for topic: {title}")

    # Get Gemini API key from environment
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not found in environment variables")

    # Prepare URL
    url = f"https://generativelanguage.googleapis.com/v1beta2/models/gemini-2.5-flash:generateText?key={GEMINI_API_KEY}"

    # Build prompt
    prompt = f"Write a detailed, SEO-friendly blog post about {title}."
    if details:
        prompt += f" Include these details: {details}."
    prompt += " Format the output in markdown."

    # Create payload
    payload = {
        "prompt": {"text": prompt}
    }

    # Make API request
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print("Gemini API Error:", response.text)
            raise ValueError(f"Gemini API returned {response.status_code}: {response.text}")

        data = response.json()
        blog_content = data["candidates"][0]["output"]

        # Store generated blog in session
        session["last_blog"] = {"title": title, "content": blog_content}
        return blog_content

    except Exception as e:
        print("Error generating blog:", str(e))
        return f"❌ Error generating blog '{title}': {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        details = request.form.get("details")
        api_key = request.form.get("api_key")
        result = generate_blog(topic, details, api_key)
        html_content = markdown.markdown(result)
        return render_template("index.html", topic=topic, blog=html_content, raw=result)
    return render_template("index.html")


@app.route("/download/<format>")
def download(format):
    blog_data = session.get("last_blog")
    if not blog_data:
        return "No blog generated yet."

    title = blog_data["title"]
    content = blog_data["content"]

    if format == "txt":
        return send_file(BytesIO(content.encode()), as_attachment=True, download_name=f"{title}.txt")

    elif format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)
        output = BytesIO()
        pdf.output(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{title}.pdf")

    elif format == "docx":
        doc = Document()
        doc.add_heading(title, 0)
        doc.add_paragraph(content)
        output = BytesIO()
        doc.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{title}.docx")

    elif format == "csv":
        output = BytesIO()
        writer = csv.writer(output)
        writer.writerow(["Title", "Content"])
        writer.writerow([title, content])
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{title}.csv", mimetype="text/csv")

    elif format == "json":
        data = json.dumps(blog_data, indent=4)
        return send_file(BytesIO(data.encode()), as_attachment=True, download_name=f"{title}.json")

    else:
        return "❌ Unsupported format."


@app.route("/clear")
def clear_session():
    session.clear()
    return "Session cleared."


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "AI Blog Generator is running!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
