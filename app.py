import os
import csv
import json
import requests
import markdown as _markdown
try:
    # google-genai client (optional dependency)
    from google import genai
    _HAS_GOOGLE_GENAI = True
except Exception:
    genai = None
    _HAS_GOOGLE_GENAI = False
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, flash, session
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
from flask import Response, make_response
import re
import io
import time
from uuid import uuid4

# Force load the .env file (allow override so local .env takes precedence here)
load_dotenv(override=True)

# LLM provider configuration. Set LLM_PROVIDER=GEMINI to use Gemini, otherwise PERPLEXITY is used.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "PERPLEXITY").upper()

# Keys for different providers (optional at import time; validated when used)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Endpoints and model defaults (can be overridden via env)
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL", "https://api.perplexity.ai/chat/completions")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta2/models/gemini-2.5-flash:generateText?key={GEMINI_API_KEY}")
MODEL = os.getenv("LLM_MODEL", "sonar-medium-online")
BLOGS_PER_PAGE = int(os.getenv("BLOGS_PER_PAGE", "5"))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

def generate_blog(title, details="", api_key=None):
    """Generate a blog using the configured LLM provider.

    This function supports two providers:
    - PERPLEXITY (default): expects PERPLEXITY_API_KEY and uses PERPLEXITY_API_URL
    - GEMINI: expects GEMINI_API_KEY and calls the Gemini REST endpoint (GCP Generative API)

    The function will raise a descriptive ValueError if the required API key for the
    selected provider is missing.
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    provider = LLM_PROVIDER

    # Decide whether the requested topic is technical/programming-focused or general.
    # This influences the wording of system prompts so we don't force a programming
    # perspective for non-technical topics (e.g., 'skincare blog').
    tech_keywords = [
        'program', 'programming', 'python', 'java', 'javascript', 'developer', 'software', 'engineer',
        'code', 'coding', 'api', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'react',
        'django', 'flask', 'node', 'rust', 'go', 'c++', 'c#'
    ]
    combined = (title or '') + ' ' + (details or '')
    lc = combined.lower()
    is_technical = any(k in lc for k in tech_keywords)

    # GEMINI provider path
    if provider == "GEMINI":
        key = api_key or GEMINI_API_KEY
        if not key:
            raise ValueError("GEMINI_API_KEY is not configured. Set LLM_PROVIDER=GEMINI and provide GEMINI_API_KEY in .env")

        # Prefer the official google-genai client when available.
        model = MODEL or "text-bison-001"
        if is_technical:
            prompt_text = f"Write a high-quality programming blog article titled '{title}'. {details}"
        else:
            prompt_text = f"Write a high-quality blog article titled '{title}'. {details}"

        if _HAS_GOOGLE_GENAI:
            # The google-genai client reads the API key from env by default, but allow explicit key.
            try:
                # create client and call models.generate_content (matches user's snippet)
                client = genai.Client() if getattr(genai, 'Client', None) else None
                if client is None:
                    # fallback to module-level helper if provided
                    response = genai.generate_text(model=model, prompt=prompt_text)
                    return getattr(response, 'text', str(response))

                # If client supports passing api_key at construction, prefer env or key
                # Client typically pulls key from environment variable, so ensure it's present.
                # We still allow constructing with key if the client supports it.
                try:
                    # some versions accept api_key parameter
                    client = genai.Client(api_key=key)
                except TypeError:
                    # older/newer versions may not accept api_key; rely on env
                    pass

                # Use models.generate_content if available (per snippet). Fallback to generate or generate_text.
                if hasattr(client.models, 'generate_content'):
                    resp = client.models.generate_content(model=model, contents=prompt_text)
                    return getattr(resp, 'text', str(resp))
                if hasattr(client.models, 'generate'):
                    resp = client.models.generate(model=model, prompt=prompt_text)
                    # various client versions return different shapes
                    return getattr(resp, 'text', getattr(resp, 'output', str(resp)))

                # last-resort: raise if client present but no known method
                raise RuntimeError('google-genai client present but no supported generate method found')
            except Exception as e:
                raise RuntimeError(f"Failed to generate blog via Gemini (google-genai): {str(e)}")

        # If google-genai is not installed, fall back to REST call
        url = f"{GEMINI_API_URL}/{model}:generateText"
        headers = {"Content-Type": "application/json"}
        if key.lower().startswith("ya29") or key.startswith("AIza") or key.startswith("GCP-"):
            url = f"{url}?key={key}"
        else:
            headers["Authorization"] = f"Bearer {key}"

        payload = {
            "prompt": {"text": prompt_text},
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            j = resp.json()
            if isinstance(j, dict):
                if "candidates" in j and j["candidates"]:
                    return j["candidates"][0].get("output", j["candidates"][0].get("content", ""))
                if "output" in j:
                    return j.get("output")
                if "content" in j:
                    return j.get("content")
            return json.dumps(j)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to generate blog via Gemini REST: {str(e)}")

    # Default: PERPLEXITY provider path
    else:
        key = api_key or PERPLEXITY_API_KEY
        if not key:
            raise ValueError("PERPLEXITY_API_KEY is not configured. Set LLM_PROVIDER=PERPLEXITY or provide PERPLEXITY_API_KEY in .env")

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {key}"
        }
        if is_technical:
            prompt = f"Write a high-quality programming blog article titled '{title}'. {details}"
            system_msg = "You are a professional technical writer."
        else:
            prompt = f"Write a high-quality blog article titled '{title}'. {details}"
            system_msg = "You are a professional writer and content creator. Write in a clear, engaging, audience-appropriate style."

        payload = {
            "model": MODEL,
            "messages": [{"role": "system", "content": system_msg},
                         {"role": "user", "content": prompt}],
            "max_tokens": 1024,
            "temperature": 0.7
        }
        try:
            resp = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to generate blog via Perplexity: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            inputs = request.form.get("blog_inputs", "").strip()
            if not inputs:
                flash("Please enter at least one blog title", "error")
                return redirect(url_for("index"))

            # default to inline display (we provide downloads after generation)
            save_format = request.form.get("save_format", "inline")
            blogs = []
            
            # Expect titles in lines, option for details as "Title | Details"
            for line in inputs.splitlines():
                if not line.strip():
                    continue
                components = line.split('|', 1)
                title = components[0].strip()
                details = components[1].strip() if len(components) > 1 else ""

                try:
                    body = generate_blog(title, details)
                    # Convert plain/markdown text into safe HTML for rendering
                    try:
                        body_html = _markdown.markdown(body, extensions=["fenced_code", "tables"])
                    except Exception:
                        # Fallback: simple newline -> paragraphs
                        paragraphs = [f"<p>{p.strip()}</p>" for p in body.split('\n\n') if p.strip()]
                        body_html = "\n".join(paragraphs)

                    blog = {
                        "title": title,
                        "details": details,
                        "body": body,
                        "body_html": body_html,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    # filename base for downloads
                    try:
                        blog["filename_base"] = _slugify(title)
                    except Exception:
                        blog["filename_base"] = _slugify(str(title))
                    blogs.append(blog)
                except Exception as e:
                    flash(f"Error generating blog '{title}': {str(e)}", "error")
                    continue

            if not blogs:
                flash("No blogs were generated successfully", "error")
                return redirect(url_for("index"))

            # Save as requested
            try:
                if save_format == "csv":
                    with open("blogs.csv", "w", newline="", encoding="utf-8") as f:
                        w = csv.DictWriter(f, fieldnames=["title", "details", "body", "date"])
                        w.writeheader()
                        w.writerows(blogs)
                    flash("Blogs saved successfully as CSV", "success")
                    return redirect(url_for("show_blog", format="csv"))
                elif save_format == "json":
                    with open("blogs.json", "w", encoding="utf-8") as f:
                        json.dump(blogs, f, ensure_ascii=False, indent=2)
                    flash("Blogs saved successfully as JSON", "success")
                    return redirect(url_for("show_blog", format="json"))
                else:  # Just show on page
                    # Persist generated blogs server-side to avoid exceeding cookie size.
                    try:
                        os.makedirs('data', exist_ok=True)
                        fname = f"last_blogs_{int(time.time())}_{uuid4().hex}.json"
                        fpath = os.path.join('data', fname)
                        with open(fpath, 'w', encoding='utf-8') as fh:
                            json.dump(blogs, fh, ensure_ascii=False, indent=2)
                        session['last_blogs_file'] = fpath
                    except Exception:
                        # fallback to session (may fail for large content)
                        try:
                            session['last_blogs'] = json.dumps(blogs)
                        except Exception:
                            pass

                    # annotate inline-generated blogs with _idx for downloads
                    for i, b in enumerate(blogs):
                        if isinstance(b, dict):
                            b['_idx'] = i

                    return render_template("blog_list.html", blogs=blogs)
            except IOError as e:
                flash(f"Error saving blogs: {str(e)}", "error")
                return render_template("blog_list.html", blogs=blogs)

        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "error")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/blog/<format>")
def show_blog(format):
    try:
        page = request.args.get('page', 1, type=int)
        blogs = []
        
        try:
            if format == "csv":
                with open("blogs.csv", encoding="utf-8") as f:
                    r = csv.DictReader(f)
                    blogs = list(r)
            elif format == "json":
                with open("blogs.json", encoding="utf-8") as f:
                    blogs = json.load(f)
        except FileNotFoundError:
            flash(f"No {format.upper()} file found", "error")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error reading {format.upper()} file: {str(e)}", "error")
            return redirect(url_for("index"))

        # Sort blogs by date if available
        if blogs and "date" in blogs[0]:
            blogs.sort(key=lambda x: x["date"], reverse=True)

        # annotate global index for each blog so download links can reference the original index
        for i, b in enumerate(blogs):
            try:
                b["_idx"] = i
            except Exception:
                # if b is not a dict (unlikely), skip
                pass
        # ensure filename_base exists for each blog
        for b in blogs:
            if isinstance(b, dict) and "filename_base" not in b:
                try:
                    b["filename_base"] = _slugify(b.get("title", "blog"))
                except Exception:
                    b["filename_base"] = _slugify(str(b.get("title", "blog")))

        # Implement pagination
        total_pages = (len(blogs) + BLOGS_PER_PAGE - 1) // BLOGS_PER_PAGE
        page = max(1, min(page, total_pages))
        start_idx = (page - 1) * BLOGS_PER_PAGE
        end_idx = start_idx + BLOGS_PER_PAGE
        current_blogs = blogs[start_idx:end_idx]

        return render_template(
            "blog_list.html",
            blogs=current_blogs,
            format=format,
            page=page,
            total_pages=total_pages,
            total_blogs=len(blogs)
        )
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "error")
        return redirect(url_for("index"))

@app.errorhandler(Exception)
def handle_error(e):
    error_msg = "An unexpected error occurred"
    if isinstance(e, HTTPException):
        error_msg = e.description
    elif str(e):
        error_msg = str(e)
    flash(error_msg, "error")
    return redirect(url_for("index"))


def _slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\-\_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:120] or "blog"


@app.route('/download/<fmt>/<int:idx>')
def download_blog(fmt, idx):
    # Load last generated blogs from server-side file (preferred) or session
    blogs = []
    fpath = session.get('last_blogs_file')
    if fpath and os.path.exists(fpath):
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                blogs = json.load(fh)
        except Exception:
            blogs = []
    else:
        # fallback to session data
        try:
            blogs = json.loads(session.get('last_blogs', '[]'))
        except Exception:
            blogs = []
    try:
        blog = blogs[idx]
    except Exception:
        flash("Requested blog not found", "error")
        return redirect(url_for('index'))

    title = blog.get('title', 'blog')
    filename_base = _slugify(title)

    if fmt == 'html':
        content = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>{title}</title></head><body>{blog.get('body_html','')}</body></html>"
        mimetype = 'text/html'
        filename = f"{filename_base}.html"
    elif fmt == 'pdf':
        # generate PDF bytes
        text = blog.get('body', '')
        # prefer HTML if available for better PDF fidelity
        html_content = blog.get('body_html') or None
        pdf_bytes = _render_text_to_pdf_bytes(title, text, html=html_content)
        resp = make_response(pdf_bytes)
        # respect custom download_name if provided
        download_name = request.args.get('download_name')
        out_name = filename_base + '.pdf'
        if download_name:
            # sanitize: strip path separators
            safe = os.path.basename(download_name)
            # if extension missing, add .pdf
            if not os.path.splitext(safe)[1]:
                safe = safe + '.pdf'
            out_name = safe
        resp.headers.set('Content-Type', 'application/pdf')
        resp.headers.set('Content-Disposition', f'attachment; filename="{out_name}"')
        return resp
    elif fmt == 'docx':
        docx_bytes = _render_text_to_docx_bytes(title, blog.get('body', ''))
        resp = make_response(docx_bytes)
        download_name = request.args.get('download_name')
        out_name = filename_base + '.docx'
        if download_name:
            safe = os.path.basename(download_name)
            if not os.path.splitext(safe)[1]:
                safe = safe + '.docx'
            out_name = safe
        resp.headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        resp.headers.set('Content-Disposition', f'attachment; filename="{out_name}"')
        return resp
    elif fmt == 'md' or fmt == 'markdown':
        content = blog.get('body', '')
        mimetype = 'text/markdown'
        filename = f"{filename_base}.md"
    elif fmt == 'txt':
        content = blog.get('body', '')
        mimetype = 'text/plain'
        filename = f"{filename_base}.txt"
    elif fmt == 'json':
        content = json.dumps(blog, ensure_ascii=False, indent=2)
        mimetype = 'application/json'
        filename = f"{filename_base}.json"
    elif fmt == 'csv':
        # single-row CSV
        out = 'title,details,body,date\n'
        def esc(s):
            return '"' + (s or '').replace('"', '""') + '"'
        out += f"{esc(blog.get('title'))},{esc(blog.get('details'))},{esc(blog.get('body'))},{esc(blog.get('date'))}\n"
        content = out
        mimetype = 'text/csv'
        filename = f"{filename_base}.csv"
    else:
        flash('Unsupported download format', 'error')
        return redirect(url_for('index'))

    resp = make_response(content)
    # allow user-specified filename via query param for non-binary formats too
    download_name = request.args.get('download_name')
    out_name = filename
    if download_name:
        safe = os.path.basename(download_name)
        # ensure extension matches desired format
        ext = os.path.splitext(filename)[1]
        if not os.path.splitext(safe)[1]:
            safe = safe + ext
        out_name = safe

    resp.headers.set('Content-Type', mimetype + '; charset=utf-8')
    resp.headers.set('Content-Disposition', f'attachment; filename="{out_name}"')
    return resp


def _render_text_to_pdf_bytes(title: str, text: str, html: str = None) -> bytes:
    """Render PDF bytes.

    Prefer WeasyPrint (HTML -> PDF) for highest fidelity if available. If WeasyPrint
    is not installed, fall back to the existing reportlab-based renderer.

    Accepts either raw markdown/text in `text` or pre-rendered HTML in `html`.
    """
    # First try WeasyPrint (best fidelity from HTML)
    try:
        from weasyprint import HTML, CSS
        have_weasy = True
    except Exception:
        have_weasy = False

    if have_weasy:
        # Build HTML content: prefer provided html, otherwise convert markdown
        try:
            if not html:
                html = _markdown.markdown(text or '', extensions=["fenced_code", "tables", "nl2br"])
            # Basic stylesheet for nicer output
            css_text = '''
                @page { size: A4; margin: 1in; }
                body { font-family: Arial, Helvetica, sans-serif; font-size: 12pt; color: #222; }
                h1, h2, h3 { color: #111; }
                pre { background: #f5f5f5; padding: 8px; border-radius:4px; }
                code { font-family: "Courier New", monospace; }
                table { border-collapse: collapse; }
                table, th, td { border: 1px solid #ccc; }
                th, td { padding: 6px; }
            '''
            # Ensure title included at top
            full_html = f"<html><head><meta charset=\"utf-8\"><title>{title}</title></head><body><h1>{title}</h1>{html}</body></html>"
            pdf_bytes = HTML(string=full_html).write_pdf(stylesheets=[CSS(string=css_text)])
            return pdf_bytes
        except Exception as e:
            # Fall back to reportlab if weasy fails at runtime
            # continue on to the fallback below
            pass

    # Fallback: reportlab-based renderer (keeps previous behavior)
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except Exception:
        raise RuntimeError('reportlab is required to generate PDFs when WeasyPrint is not available: pip install reportlab or weasyprint')

    # We'll render markdown-aware content by converting to HTML and walking the nodes
    from bs4 import BeautifulSoup
    html_content = html or _markdown.markdown(text or '', extensions=["fenced_code", "tables", "nl2br"])
    soup = BeautifulSoup(html_content, "html.parser")

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    left_margin = 72
    right_margin = 72
    top_margin = 72
    bottom_margin = 72
    usable_width = width - left_margin - right_margin
    y = height - top_margin

    def ensure_space(h):
        nonlocal y
        if y - h < bottom_margin:
            c.showPage()
            # reset y on new page
            y = height - top_margin

    def draw_wrapped(text, font_name='Helvetica', font_size=10, indent=0, leading=None):
        """Draw `text` wrapped to the usable width using the given font and size.

        This measures string widths and builds lines that fit the available width.
        """
        nonlocal y
        if leading is None:
            leading = int(font_size * 1.2)

        # set font
        try:
            c.setFont(font_name, font_size)
        except Exception:
            c.setFont('Helvetica', font_size)

        words = text.split()
        if not words:
            return

        cur_line = ''
        for word in words:
            test_line = (cur_line + ' ' + word).strip() if cur_line else word
            width_px = pdfmetrics.stringWidth(test_line, font_name, font_size)
            if width_px + indent > usable_width:
                # emit cur_line
                ensure_space(leading)
                c.drawString(left_margin + indent, y, cur_line)
                y -= leading
                cur_line = word
            else:
                cur_line = test_line

        # emit last line
        if cur_line:
            ensure_space(leading)
            c.drawString(left_margin + indent, y, cur_line)
            y -= leading

    # Title
    title_font = 'Helvetica-Bold'
    title_size = 16
    ensure_space(title_size + 6)
    c.setFont(title_font, title_size)
    c.drawString(left_margin, y, title)
    y -= title_size + 12

    # Walk simple tags and use measured wrapping
    for node in soup.children:
        name = getattr(node, 'name', None)
        if name in ('h1', 'h2', 'h3'):
            size = 14 if name == 'h2' else 12 if name == 'h3' else 16
            c.setFont('Helvetica-Bold', size)
            draw_wrapped(node.get_text(), font_name='Helvetica-Bold', font_size=size, indent=0, leading=int(size * 1.3))
            y -= 6
            c.setFont('Helvetica', 10)
        elif name == 'pre' or name == 'code':
            # code block: use monospace and preserve indentation
            code_text = node.get_text()
            c.setFont('Courier', 9)
            # handle lines individually, wrapping long lines by splitting
            for line in code_text.split('\n'):
                # split long continuous lines into chunks that fit
                if not line:
                    ensure_space(12)
                    y -= 12
                    continue
                # try to wrap by words; if still too long, hard-split
                parts = []
                cur = ''
                for ch in line:
                    test = cur + ch
                    if pdfmetrics.stringWidth(test, 'Courier', 9) > usable_width - 24:
                        parts.append(cur)
                        cur = ch
                    else:
                        cur = test
                if cur:
                    parts.append(cur)
                for p in parts:
                    ensure_space(12)
                    c.drawString(left_margin + 12, y, p)
                    y -= 12
            y -= 8
            c.setFont('Helvetica', 10)
        elif name in ('ul', 'ol'):
            for li in node.find_all('li', recursive=False):
                bullet = '\u2022' if name == 'ul' else f"{li.parent.index(li)+1}."
                text = f"{bullet} {li.get_text()}"
                draw_wrapped(text, font_name='Helvetica', font_size=10, indent=8)
            y -= 6
        else:
            # paragraphs or other text
            text_val = node.get_text().strip()
            if not text_val:
                continue
            draw_wrapped(text_val, font_name='Helvetica', font_size=10, indent=0)
            y -= 6

    c.save()
    buf.seek(0)
    return buf.read()


def _render_text_to_docx_bytes(title: str, text: str) -> bytes:
    try:
        from docx import Document
        from docx.shared import Pt
    except Exception:
        raise RuntimeError('python-docx is required to generate DOCX: pip install python-docx')

    # Convert markdown to HTML and parse
    html = _markdown.markdown(text, extensions=["fenced_code", "tables"])
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    doc = Document()
    doc.add_heading(title, level=1)

    def add_paragraph_from_tag(tag):
        if tag.name in ('p', None):
            p = doc.add_paragraph()
            for item in tag.children:
                if getattr(item, 'name', None) == 'code':
                    run = p.add_run(item.get_text())
                    run.font.name = 'Courier New'
                    run.font.size = Pt(10)
                else:
                    run = p.add_run(item.get_text())
            return
        if tag.name == 'pre':
            p = doc.add_paragraph()
            run = p.add_run(tag.get_text())
            run.font.name = 'Courier New'
            run.font.size = Pt(9)
            return
        if tag.name in ('h1','h2','h3','h4'):
            level = 1 if tag.name=='h1' else 2 if tag.name=='h2' else 3
            doc.add_heading(tag.get_text(), level=level)
            return
        if tag.name == 'ul':
            for li in tag.find_all('li', recursive=False):
                p = doc.add_paragraph(li.get_text(), style='List Bullet')
            return
        if tag.name == 'ol':
            for li in tag.find_all('li', recursive=False):
                p = doc.add_paragraph(li.get_text(), style='List Number')
            return

    for el in soup.contents:
        # handle text node
        if getattr(el, 'name', None) is None:
            txt = el.strip()
            if txt:
                doc.add_paragraph(txt)
        else:
            add_paragraph_from_tag(el)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()


@app.route('/download/all/<fmt>')
def download_all(fmt):
    # Read blogs from server-side file if available
    blogs = []
    fpath = session.get('last_blogs_file')
    if fpath and os.path.exists(fpath):
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                blogs = json.load(fh)
        except Exception:
            blogs = []
    else:
        try:
            blogs = json.loads(session.get('last_blogs', '[]'))
        except Exception:
            blogs = []
    filename = f"blogs.{fmt}"
    if fmt == 'json':
        content = json.dumps(blogs, ensure_ascii=False, indent=2)
        mimetype = 'application/json'
    elif fmt == 'csv':
        out_lines = []
        header = ['title', 'details', 'body', 'date']
        out_lines.append(','.join(header))
        for b in blogs:
            def esc(s):
                return '"' + (s or '').replace('"', '""') + '"'
            out_lines.append(','.join([esc(b.get('title')), esc(b.get('details')), esc(b.get('body')), esc(b.get('date'))]))
        content = '\n'.join(out_lines)
        mimetype = 'text/csv'
    else:
        # For other formats, concatenate files separated by a divider
        parts = []
        for i, b in enumerate(blogs, start=1):
            title = b.get('title','')
            if fmt in ('md','markdown'):
                parts.append(f"# {title}\n\n{b.get('body','')}\n\n---\n")
            elif fmt == 'html':
                parts.append(f"<h1>{title}</h1>\n{b.get('body_html','')}<hr/>")
            else:
                parts.append(f"{title}\n\n{b.get('body','')}\n\n---\n")
        content = '\n'.join(parts)
        mimetype = 'text/plain' if fmt in ('txt','md') else 'text/html'

    resp = make_response(content)
    resp.headers.set('Content-Type', mimetype + '; charset=utf-8')
    resp.headers.set('Content-Disposition', f'attachment; filename="{filename}"')
    return resp


@app.route("/_debug_config")
def _debug_config():
    """Temporary debug endpoint to inspect LLM-related configuration."""
    cfg = {
        "LLM_PROVIDER": LLM_PROVIDER,
        "MODEL": MODEL,
        "PERPLEXITY_API_KEY_present": bool(PERPLEXITY_API_KEY),
        "GEMINI_API_KEY_present": bool(GEMINI_API_KEY),
        "PERPLEXITY_API_URL": PERPLEXITY_API_URL,
        "GEMINI_API_URL": GEMINI_API_URL,
    }
    # Mask keys for safety
    return json.dumps(cfg, indent=2)

if __name__ == "__main__":
    app.run(debug=True)
