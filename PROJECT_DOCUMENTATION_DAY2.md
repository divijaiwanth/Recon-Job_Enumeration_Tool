# Company Intelligence Tool - Project Documentation (Day 2)

## 1. Problem Statement & Solution (Day 2 Focus)

### Problem
While the foundation of the pipeline was established on Day 1, Day 2 focused on resolving execution crashes, system integration gaps, output formatting inconsistencies, and memory-bound AI bottlenecks that prevented the application from functioning correctly end-to-end. 

### Solution
A complete sweep of the repository to:
- **Debug & Fix** API schema mismatches and Unicode crashes.
- **Integrate** standalone web scraping modules deeply into the main pipeline.
- **Optimize** AI model usage to prevent Out-Of-Memory (OOM) hangs.
- **Enhance** report generation to accurately reflect all data structures in final `.md` files.
- **Format** the core execution code for better readability and maintainability.

---

## 2. Issues Addressed & Tech Solutions

| Component | Issue | Technical Solution |
|-----------|-------|--------------------|
| **Firecrawl API v2** | `AttributeError` during page scraping | Added safe property extraction for the Firecrawl v2 `Document` object (`content.markdown`) instead of treating it as a raw dictionary. |
| **Pydantic Models** | `ValidationError` on `RepeatedQuestion` | Corrected `Repeated_DSA.py` to format extracted LLM data into a strict `list[RepeatedQuestion]` rather than returning a raw dict to `main.py`. |
| **Ollama (AI)** | Execution hangs & Server OOM crashes | Replaced a hardcoded `qwen2.5:14b` model call in `Analyze_Report.py` with `structured_chat`, leveraging the lightweight `.env` configured model (`phi3:latest`). |
| **Windows OS** | `UnicodeEncodeError` in terminal output | Removed `cp1252` incompatible Unicode checkmark characters (`✓`) in `main.py`, replacing them with ASCII equivalents. |
| **Report Engine** | Incomplete Markdown rendering | Rewrote `save_markdown` to dynamically render every Pydantic field, generating rich tables, headers, and bulleted lists. |

---

## 3. Key Enhancements Detailed

### 3.1 Company-Specific Research Integration
**What:** Connected the previously isolated `Company_Specific` modules directly into the `main.py` execution flow.
**Why:**
- On Day 1, `main.py` used placeholder text (`"Mission not collected yet"`) for company data. 
- The pipeline now natively invokes `build_company_context()` and `analyze_company()` during the `[0/6] Company Research...` phase, allowing the tool to autonomously scrape the company website provided in the input, analyze its contents with the LLM, and inject live data (Mission, Products, Competitors, Hiring Signals) straight into the final report.

### 3.2 Advanced Markdown Generation
**What:** `report_engine.py` `save_markdown()` method overhaul.
**Why:**
- The old implementation only grabbed a fraction of the JSON fields and ignored nested arrays and complex structures.
- The new implementation maps the entire `ReconReport` Pydantic model directly to Markdown. It auto-generates tables for `Repeated_DSA` questions and dynamically handles varying lists (like Recommended Projects, Missing Skills, and System Design Topics).

### 3.3 LLM Client Standardization
**What:** Refactored `Analyze_Report.py`.
**Why:**
- A massive bottleneck occurred when the application tried to pull `qwen2.5:14b` dynamically.
- Refactored the code to use the centralized `Utils.ollama_client.structured_chat` method. This enforces the usage of the predefined `OLLAMA_MODEL` environment variable (e.g., `phi3:latest`), drastically reducing latency and completely stopping memory-related socket hangs.

### 3.4 Code Formatting & Tidy Up
**What:** Fixed jagged code formatting across the repository.
**Why:**
- Multiple files (`main.py`, `JD_Analyzer.py`) had extremely fragmented structures with line breaks separating function parameters over 10-15 lines.
- Manually collapsed and organized function calls, standardizing imports and dramatically improving developer readability without needing heavy third-party dependencies.

---

## 4. Final Data Flow Integrations

```
┌─────────────────────────────────────────┐
│  INPUT: Company Name, Role, JD, Resume  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  [0/6] Company Research (INTEGRATED)    │
│  - Scrapes input website                │
│  - Extracts Mission, Products, etc.     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  [1/6] - [4/6] Analysis Pipeline        │
│  - JD, Resume, Mission Alignment,       │
│  - Interview Research (Using phi3)      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  [5/6] Repeated DSA (FIXED)             │
│  - Firecrawl v2 Parsing fixed           │
│  - Schema maps to RepeatedQuestion[]    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  [6/6] Final Validation & Export        │
│  - Strict Pydantic ReconReport schema   │
│  - JSON output saved                    │
│  - (NEW) Rich Markdown rendering saved  │
└─────────────────────────────────────────┘
```

---

## 5. Next Steps (Day 3 Considerations)
- **Error Resiliency**: Implement better retry logic for Firecrawl API limits.
- **Multi-threading**: Allow `[0/6] Company Research` and `[1/6] JD Analysis` to run asynchronously since they don't depend on each other initially.
- **Frontend / UI**: Begin wrapping the console tool into a lightweight web interface (Streamlit or FastAPI) for better user experience.
