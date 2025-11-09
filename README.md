# AI-BLOG-GENERATOR

A full-stack web app to generate high-quality programming blog articles using the Google Gemini AI API. Easily provide your own topics, customize prompts, and output to CSV, JSON, or view results in a beautiful web interface.

***

## Features

- **AI-Powered Blog Generation** – Enter your own blog topics and optionally add extra instructions.
- **Gemini API Integration** – Uses Google Gemini API for high-quality, context-aware content.
- **Multiple Output Formats** – Download generated blogs as CSV or JSON, or view directly in your browser.
- **User-Friendly Web UI** – Simple, clean, and responsive design (HTML/CSS/Bootstrap).
- **Customizable & Extensible** – Easy to adapt, add more providers, or enhance the frontend.

***

## Project Structure

```
AI-BLOG-GENERATOR/
├── app.py                # Main Flask backend
├── templates/
│   ├── index.html        # Blog prompt form and homepage
│   └── blog_list.html    # Result display page
├── static/
│   └── style.css         # CSS styling for app
├── blogs.csv             # (example) blog output in CSV
├── blogs.json            # (example) blog output in JSON
├── .env                  # Contains your Gemini API Key (not included in repo)
├── requirements.txt      # Python deps: flask, requests, etc.
└── README.md
```

***

## Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/deebak4064/AI-BLOG-GENERATOR.git
   cd AI-BLOG-GENERATOR
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Gemini API Key**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Generate and copy your Gemini API key.

4. **Configure API Key**
   - Create a file named `.env` in your project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

5. **Run the App**
   ```bash
   python app.py
   ```
   - Visit [http://localhost:5000](http://localhost:5000) in your browser.

***

## Usage

1. Enter your blog titles (one per line, optionally add "| extra details" after the title for a custom prompt).
2. Choose your preferred output (Show on Page, CSV, or JSON).
3. Click **Generate Blogs** and view/download results!

**Example Input:**
```
Understanding Python Decorators | Give practical use-cases and examples
Deploying ML Models with FastAPI | Should address REST and Docker deployment
Top Libraries for Natural Language Processing in 2025
```

***

## Security

- **Never commit your `.env` or any API keys to the repo!** Use `.gitignore` to keep secrets local.
- See the sample `.env` instructions above to set up your environment.

***

## Customization & Extensibility

- Replace Gemini API with other providers (OpenAI, local LLMs) by editing `app.py`
- Add support for Markdown output, image generation, etc!
- Style and extend the frontend as you like.

***

## License

This project is for educational and portfolio use.

***

**Questions?**  
Open an issue on GitHub or contact the maintainer :
linkedin: linkedin.com/in/deebak-kumar-k-632b96285
email : deebakintern@gmai.com

***

[1](https://github.com/deebak4064/AI-BLOG-GENERATOR)
