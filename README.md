# La Jornada Maya - Web Scraping & Analytics Pipeline

An ETL pipeline designed to ingest, parse, and analyze bilingual news data from the *K'iintsil* section of **La Jornada Maya**. The project automates content retrieval using randomized headers to prevent anti-bot throttling, features structured feature extraction with robust exception handling, and includes an NLP computational linguistics layer for Spanish and Yucatec Maya token classification.

💡 **Project Presentation:** [Canva Link](https://www.canva.com/design/DAGgjol0fKg/XDfiXU9-gvmju_lxl_8qoQ/edit?utm_content=DAGgjol0fKg&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

## Getting Started & Quick Setup

Follow these operational steps to build and spin up the environment isolation pipelines locally.

1. Prerequisites
Ensure you have Python 3.10+ installed on your system architecture.

2. Environment Configuration
Clone the repository and spin up a pristine isolated virtual environment:

```bash
# Clone the repository
git clone https://github.com/Maricharmen/WebScraping_JornadaMaya.git
cd WebScraping_JornadaMaya

# Instantiate and activate the environment container
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install explicit runtime dependencies
pip install -r requirements.txt
```

3. Pipeline Execution
Run the scraping ingestion module to populate target arrays:

```bash
python src/scraper_pipeline.py
```
