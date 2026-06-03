import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pydantic_models import CompanyOverview, ReconReport
from report_engine import ReportEngine
from Utils.resume_loader import load_resume
from Job_Specific.JD_Analyzer import analyze_jd
from Job_Specific.Resume_Match import analyze_resume_match
from Job_Specific.Role_Context import generate_mission_alignment
from Job_Specific.Interview_Research import research_interviews
from Job_Specific.Repeated_DSA import find_repeated_dsa
from Job_Specific.Team_Research import estimate_team

def main():
    print("\n=== JOB INTELLIGENCE TOOL ===\n")

    company_name = input("Company Name: ")
    website = input("Company Website: ")
    role_title = input("Role Title: ")
    jd_file = input("JD File Path: ")
    resume_file = input("Resume File Path: ")

    # ---------------------
    # Load Files
    # ---------------------
    jd_text = load_resume(jd_file)
    resume_text = load_resume(resume_file)

    from Company_Specific.Analyze_Report import analyze_company
    from Company_Specific.Scrape_Context import build_company_context
    
    print("\n[0/6] Company Research...")
    company_text = build_company_context([website])
    company_overview = analyze_company(company_name, website, company_text)

    print("\n[1/6] JD Analysis...")
    role_analysis = analyze_jd(role_title, jd_text)

    print("[2/6] Resume Match...")
    resume_analysis = analyze_resume_match(resume_text, jd_text)

    print("[3/6] Mission Alignment...")
    role_analysis.mission_alignment = generate_mission_alignment(
        company_overview.mission,
        role_title,
        role_analysis.responsibilities
    )

    print("[4/6] Interview Research...")
    interview_data, sources = research_interviews(company_name, role_title)

    print("[5/6] Repeated DSA...")
    repeated_questions, _ = find_repeated_dsa(company_name, role_title)
    interview_data["repeated_questions"] = repeated_questions

    print("[6/6] Team Research...")
    team_data = estimate_team(company_name, role_title)
    role_analysis.estimated_team_size = team_data.get("estimated_team_size", "")
    role_analysis.estimated_team_type = team_data.get("estimated_team_type", "")

    report = ReconReport(
        company_name=company_name,
        role_title=role_title,
        company_overview=company_overview,
        role_analysis=role_analysis,
        interview_intelligence=interview_data,
        resume_analysis=resume_analysis
    )

    engine = ReportEngine()
    json_file = engine.save_json(report)
    md_file = engine.save_markdown(report)

    print("\nDone!")
    print(f"\nJSON: {json_file}")
    print(f"Markdown: {md_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # ============================================
        # TEST MODE - Modify these example inputs
        # ============================================
        
        print("\n=== JOB INTELLIGENCE TOOL (TEST MODE) ===\n")
        
        # Load from actual files in Resumes&JD folder
        resumes_jd_path = Path(__file__).parent / "Resumes&JD"
        
        jd_file_path = resumes_jd_path / "JD_Intern GEN-AI.pdf"
        resume_file_path = resumes_jd_path / "Divi_Jaiwanth_Resume_2_0.pdf"
        
        print(f"Loading JD from: {jd_file_path}")
        print(f"Loading Resume from: {resume_file_path}\n")
        
        jd_text = load_resume(str(jd_file_path))
        resume_text = load_resume(str(resume_file_path))
        
        # Manual inputs
        company_name = "Swiggy"
        website = "https://careers.swiggy.com/#/"
        role_title = "Intern GEN-AI"
        
        
        from Company_Specific.Analyze_Report import analyze_company
        from Company_Specific.Scrape_Context import build_company_context
        
        print("\n[0/6] Company Research...")
        company_text = build_company_context([website])
        company_overview = analyze_company(company_name, website, company_text)

        print("[1/6] JD Analysis...")
        role_analysis = analyze_jd(role_title, jd_text)

        print("[2/6] Resume Match...")
        resume_analysis = analyze_resume_match(resume_text, jd_text)

        print("[3/6] Mission Alignment...")
        role_analysis.mission_alignment = generate_mission_alignment(
            company_overview.mission,
            role_title,
            role_analysis.responsibilities
        )

        print("[4/6] Interview Research...")
        interview_data, sources = research_interviews(company_name, role_title)

        print("[5/6] Repeated DSA...")
        repeated_questions, _ = find_repeated_dsa(company_name, role_title)
        interview_data["repeated_questions"] = repeated_questions

        print("[6/6] Team Research...")
        team_data = estimate_team(company_name, role_title)
        role_analysis.estimated_team_size = team_data.get("estimated_team_size", "")
        role_analysis.estimated_team_type = team_data.get("estimated_team_type", "")

        report = ReconReport(
            company_name=company_name,
            role_title=role_title,
            company_overview=company_overview,
            role_analysis=role_analysis,
            interview_intelligence=interview_data,
            resume_analysis=resume_analysis
        )

        engine = ReportEngine()
        json_file = engine.save_json(report)
        md_file = engine.save_markdown(report)

        print("\n" + "="*50)
        print("= ANALYSIS COMPLETE =")
        print("="*50)
        print(f"\nCompany: {company_name}")
        print(f"Role: {role_title}")
        print(f"JSON Report: {json_file}")
        print(f"Markdown Report: {md_file}\n")
    else:
        main()