# AI Website Brochure Generator

## Overview

This project is an AI-powered website brochure generator.

The user provides a company or organization website URL. The application:

1. Scrapes the landing page.
2. Finds links on the website.
3. Uses an LLM to identify the most relevant links.
4. Scrapes the selected pages.
5. Combines the website information.
6. Sends the information to an LLM.
7. Generates a short company/organization brochure in Markdown.

The project uses Python, web scraping, and Ollama.

---

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Ollama
- OpenAI-compatible API
- Jupyter Notebook
- JSON
- Markdown

---

## Project Flow

```text
User provides URL
        |
        v
Fetch landing page
        |
        v
Extract website links
        |
        v
LLM selects relevant links
        |
        v
Scrape selected pages
        |
        v
Combine website content
        |
        v
Send content to Ollama
        |
        v
Generate brochure
        |
        v
Display Markdown output