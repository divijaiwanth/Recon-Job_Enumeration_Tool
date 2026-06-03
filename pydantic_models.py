from pydantic import BaseModel, Field


# COMPANY

class CompanyOverview(BaseModel):
    website: str
    mission: str
    products: list[str] = []
    recent_launches: list[str] = []
    hiring_signals: list[str] = []
    competitors: list[str] = []
    market_position: str = ""

# REPEATED QUESTIONS

class RepeatedQuestion(BaseModel):
    question_name: str
    category: str
    frequency_score: int
    difficulty: str
    source_count: int

# ROLE ANALYSIS

class RoleAnalysis(BaseModel):
    role_title: str
    requirements: list[str] = []
    preferred_qualifications: list[str] = []
    responsibilities: list[str] = []
    competencies: list[str] = []
    evaluation_criteria: list[str] = []
    mission_alignment: str = ""
    estimated_team_size: str = ""
    estimated_team_type: str = ""


# INTERVIEW INTELLIGENCE

class InterviewIntelligence(BaseModel):
    interview_difficulty: str = ""
    interview_rounds: list[str] = []
    behavioral_topics: list[str] = []
    dsa_topics: list[str] = []
    system_design_topics: list[str] = []
    repeated_questions: list[
        RepeatedQuestion
    ] = []


# RESUME ANALYSIS

class ResumeAnalysis(BaseModel):
    match_score: float = 0
    matching_skills: list[str] = []
    missing_skills: list[str] = []
    recommended_projects: list[str] = []
    resume_gaps: list[str] = []


# MASTER REPORT

class ReconReport(BaseModel):
    company_name: str
    role_title: str
    company_overview: CompanyOverview
    role_analysis: RoleAnalysis
    interview_intelligence: InterviewIntelligence
    resume_analysis: ResumeAnalysis