import json

from Utils.helpers import (
    ensure_directory,
    sanitize_filename,
    timestamp
)


class ReportEngine:

    def __init__(self):

        ensure_directory(
            "reports"
        )

    def save_json(
        self,
        report
    ):

        filename = (
            f"reports/"
            f"{sanitize_filename(report.company_name)}"
            f"_{timestamp()}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report.model_dump(),
                f,
                indent=2,
                ensure_ascii=False
            )

        return filename

    def save_markdown(
        self,
        report
    ):
        md = f"# Recon Report: {report.company_name} - {report.role_title}\n\n"
        
        md += "## 1. Company Overview\n\n"
        md += f"**Website:** {report.company_overview.website}\n\n"
        md += f"**Mission:** {report.company_overview.mission}\n\n"
        if report.company_overview.market_position:
            md += f"**Market Position:** {report.company_overview.market_position}\n\n"
        
        def add_list(title, items):
            res = ""
            if items:
                res += f"### {title}\n"
                for item in items:
                    res += f"- {item}\n"
                res += "\n"
            return res

        md += add_list("Products", report.company_overview.products)
        md += add_list("Recent Launches", report.company_overview.recent_launches)
        md += add_list("Hiring Signals", report.company_overview.hiring_signals)
        md += add_list("Competitors", report.company_overview.competitors)
        
        md += "---\n\n## 2. Role Analysis\n\n"
        if report.role_analysis.estimated_team_size:
            md += f"**Estimated Team Size:** {report.role_analysis.estimated_team_size}\n\n"
        if report.role_analysis.estimated_team_type:
            md += f"**Estimated Team Type:** {report.role_analysis.estimated_team_type}\n\n"
        if report.role_analysis.mission_alignment:
            md += f"**Mission Alignment:**\n{report.role_analysis.mission_alignment}\n\n"
        
        md += add_list("Responsibilities", report.role_analysis.responsibilities)
        md += add_list("Requirements", report.role_analysis.requirements)
        md += add_list("Preferred Qualifications", report.role_analysis.preferred_qualifications)
        md += add_list("Competencies", report.role_analysis.competencies)
        md += add_list("Evaluation Criteria", report.role_analysis.evaluation_criteria)
        
        md += "---\n\n## 3. Interview Intelligence\n\n"
        if report.interview_intelligence.interview_difficulty:
            md += f"**Interview Difficulty:** {report.interview_intelligence.interview_difficulty}\n\n"
        
        md += add_list("Interview Rounds", report.interview_intelligence.interview_rounds)
        md += add_list("Behavioral Topics", report.interview_intelligence.behavioral_topics)
        md += add_list("DSA Topics", report.interview_intelligence.dsa_topics)
        md += add_list("System Design Topics", report.interview_intelligence.system_design_topics)
        
        if report.interview_intelligence.repeated_questions:
            md += "### Repeated Questions\n\n"
            md += "| Question | Category | Difficulty | Frequency Score | Source Count |\n"
            md += "| --- | --- | --- | --- | --- |\n"
            for q in report.interview_intelligence.repeated_questions:
                md += f"| {q.question_name} | {q.category} | {q.difficulty} | {q.frequency_score}/10 | {q.source_count} |\n"
            md += "\n"
            
        md += "---\n\n## 4. Resume Analysis\n\n"
        md += f"**Match Score:** {report.resume_analysis.match_score}%\n\n"
        
        md += add_list("Matching Skills", report.resume_analysis.matching_skills)
        md += add_list("Missing Skills", report.resume_analysis.missing_skills)
        md += add_list("Resume Gaps", report.resume_analysis.resume_gaps)
        md += add_list("Recommended Projects", report.resume_analysis.recommended_projects)

        filename = (
            f"reports/"
            f"{sanitize_filename(report.company_name)}"
            f"_{timestamp()}.md"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(md)

        return filename