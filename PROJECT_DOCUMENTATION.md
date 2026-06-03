# Company Intelligence Tool - Project Documentation

## 1. Problem Statement & Solution

### Problem
Organizations need efficient ways to gather, analyze, and document company intelligence from multiple web sources. Manually scraping websites, extracting key information, and generating reports is time-consuming and error-prone.

### Solution
An automated pipeline that:
- **Discovers** relevant pages via XML sitemaps
- **Scrapes** web content from multiple pages
- **Analyzes** extracted content using AI (LLM)
- **Validates** data against strict schema (Pydantic models)
- **Generates** formatted markdown reports automatically

---

## 2. Tech Stack Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.13 | Core programming language |
| **Web Scraping** | BeautifulSoup4 | Parse HTML/XML content |
| **HTTP Requests** | Requests | Fetch web pages |
| **AI/LLM** | Ollama (phi3 model) | Analyze content & extract insights |
| **Data Validation** | Pydantic | Schema validation & type safety |
| **JSON Processing** | Python json + regex | Parse & validate API responses |
| **File I/O** | PathLib | Handle file operations cross-platform |
| **XML Parsing** | BeautifulSoup (xml) | Extract URLs from sitemaps |

---

## 3. Methods Used (Detailed Tech Stack & Why)

### Pipeline Architecture

```
Sitemap Discovery → URL Filtering → Web Scraping → Content Analysis → Data Validation → Report Generation
```

### 3.1 Sitemap Discovery & URL Filtering
**What:** `sitemap.py` - Fetches and parses XML sitemaps
**Tech:** BeautifulSoup4 with `features="xml"`
**Why:**
- Sitemaps provide complete list of publicly available pages
- XML parser is more reliable than HTML parser for structured data
- Scalable: can handle large websites with thousands of URLs
- Efficient: avoids crawling entire site

**Implementation:**
```
- Constructs sitemap URL: {website}/sitemap.xml
- Parses with BeautifulSoup XML parser
- Extracts all <loc> tags containing URLs
- Filters by keywords: about, company, team, products, careers, etc.
- Returns max 15 most relevant URLs
```

### 3.2 Web Content Scraping
**What:** `Scrape_Context.py` - Extracts text from web pages
**Tech:** Requests library + BeautifulSoup4
**Why:**
- Requests: Lightweight, reliable HTTP client with timeout handling
- BeautifulSoup: Robust HTML parsing, removes noise (scripts, styles)
- Separation of concerns: scraping logic isolated from analysis

**Implementation:**
```
- Sets Mozilla User-Agent header (avoids blocking)
- 15-second timeout (prevents hangs on slow servers)
- Removes: <script>, <style>, <noscript> tags
- Extracts plain text with `get_text(separator=" ")`
- Limits to 15,000 chars (balances context & token limits)
```

### 3.3 AI Analysis with LLM
**What:** `Analyze_Report.py` - Processes content with AI
**Tech:** Ollama (local LLM) + phi3 model + Pydantic schema enforcement
**Why:**
- **Ollama:** Local execution (privacy), no API costs, offline-capable
- **phi3:** Fast, small model (~3-7B params), runs on modest hardware
- **Schema-based prompting:** Forces structured output (JSON)
- **Error resilience:** Regex fallback for malformed JSON responses

**Implementation:**
```
- Sends system prompt defining analysis role
- Uses Pydantic JSON schema as format constraint
- LLM must extract: mission, products, launches, hiring signals
- Fallback JSON parsing with regex if direct parsing fails
- Creates default values if extraction completely fails
```

### 3.4 Data Validation & Type Safety
**What:** `pydantic_models.py` - Schema definition
**Tech:** Pydantic BaseModel
**Why:**
- **Type hints:** Catches data errors early
- **Validation:** Enforces required fields
- **Serialization:** Easy conversion to JSON/dict
- **Auto-documentation:** Schema serves as API contract

**Schema:**
```python
class CompanyReport(BaseModel):
    company_name: str
    website: str
    mission: str
    products: list[str]
    recent_launches: list[str]
    hiring_signals: list[str]
```

### 3.5 Report Generation & Formatting
**What:** `main.py` - Orchestrates pipeline & generates reports
**Tech:** Python f-strings, regex sanitization, PathLib
**Why:**
- **Markdown format:** Human-readable, version-control friendly, GitHub-compatible
- **Filename sanitization:** Removes invalid characters (`< > : " \ | ? *`)
- **Timestamp:** Prevents overwriting, tracks when analysis ran
- **Directory management:** Auto-creates `reports/` folder

**Implementation:**
```
- Converts Pydantic model to formatted markdown
- Sanitizes company name for filesystem (50 char limit)
- Creates timestamped filename: {company}_{timestamp}.md
- Saves to reports/ directory
```

### 3.6 Error Handling & Resilience
**Features:**
- **JSON parsing fallback:** Regex extraction if direct parse fails
- **HTTP timeout:** 15s prevents hanging on unresponsive servers
- **User-Agent headers:** Mimics browser, reduces blocking
- **Character limits:** Prevents token overflow in LLM
- **Warning suppression:** Filters XMLParsedAsHTMLWarning

---

## 4. Pipeline Flow Diagram

```
┌─────────────────────────────────────────┐
│  INPUT: Company Name + Website URL      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 1: Fetch & Parse Sitemap          │
│  - Construct {website}/sitemap.xml      │
│  - Parse with BeautifulSoup XML parser  │
│  - Extract all URLs                     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 2: Filter URLs by Keywords        │
│  - about, company, team, products, etc. │
│  - Return top 15 most relevant          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 3: Scrape All Selected URLs       │
│  - Fetch page content (15s timeout)     │
│  - Remove scripts/styles                │
│  - Extract text (limit 15k chars)       │
│  - Combine into single context          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 4: AI Analysis (Ollama)           │
│  - Send combined text + schema to LLM   │
│  - Extract: mission, products, etc.     │
│  - Fallback: regex JSON extraction      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 5: Validate with Pydantic         │
│  - Enforce schema structure             │
│  - Type checking                        │
│  - Raise errors if invalid              │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 6: Format to Markdown             │
│  - Convert to human-readable format     │
│  - Add timestamp & metadata             │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  STEP 7: Save Report                    │
│  - Sanitize filename (remove invalid)   │
│  - Add timestamp to prevent overwrites  │
│  - Save to reports/ directory (.md)     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  OUTPUT: Markdown Report File           │
│  reports/company_report_YYYYMMDD.md     │
└─────────────────────────────────────────┘
```

---

## 5. Key Design Decisions

| Decision | Why |
|----------|-----|
| **Local Ollama vs Cloud API** | Privacy, cost, offline capability, no rate limits |
| **Pydantic Schema** | Type safety, validation, serialization, documentation |
| **Sitemap-first approach** | Efficient, scalable, respects robots.txt structure |
| **Markdown output** | Human-readable, version-control friendly, GitHub integration |
| **Filename sanitization** | Cross-platform compatibility, prevents file system errors |
| **Error resilience** | Handles malformed LLM responses gracefully with fallbacks |

---

## 6. Usage

### Test Mode (Quick Demo)
```bash
python main.py --test
```

### Interactive Mode (Custom Companies)
```bash
python main.py
# Then enter company name and website when prompted
```

### Output
Generated reports saved to: `reports/company_name_report_YYYYMMDD_HHMMSS.md`

