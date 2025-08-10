from groq import AsyncGroq
from dotenv import load_dotenv
import os

from app.utils.pdf_maker import save_summary_to_pdf

load_dotenv()
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

def clean_field(value):
    """
    Cleans up placeholder/dummy values from DB and replaces with 'Not provided'.
    """
    if not value or str(value).strip().lower() in ["string", "n/a", "none", "null"]:
        return "Not provided"
    return str(value).strip()

async def generate_ai_summary(application_data):
    print(application_data)
    job_research = application_data.job_research
    company_research = job_research.company_research if job_research else None

    research_text = f"""
    📌 Job Application Summary

    📝 Job Details
    - Job Title: {clean_field(job_research.job_title) if job_research else 'Not provided'}
    - Detailed Description: {clean_field(job_research.detailed_description) if job_research else 'Not provided'}
    - Required Skills: {clean_field(job_research.required_skills) if job_research else 'Not provided'}
    - Tech Stack: {clean_field(job_research.tech_stack) if job_research else 'Not provided'}
    - Team Structure: {clean_field(job_research.team_structure) if job_research else 'Not provided'}
    - Challenges: {clean_field(job_research.challenges) if job_research else 'Not provided'}

    🏢 Company Research
    - Company Name: {clean_field(company_research.company_name) if company_research else 'Not provided'}
    - Mission: {clean_field(company_research.mission) if company_research else 'Not provided'}
    - Vision: {clean_field(company_research.vision) if company_research else 'Not provided'}
    - Values: {clean_field(company_research.values) if company_research else 'Not provided'}
    - Culture: {clean_field(company_research.culture) if company_research else 'Not provided'}
    - Recent News: {clean_field(company_research.recent_news) if company_research else 'Not provided'}
    - Competitors: {clean_field(company_research.competitors) if company_research else 'Not provided'}
    - CEO Name: {clean_field(company_research.ceo_name) if company_research else 'Not provided'}
    - Location: {clean_field(company_research.location) if company_research else 'Not provided'}
    - Services: {clean_field(company_research.services) if company_research else 'Not provided'}
    - Total Members: {clean_field(company_research.total_members) if company_research else 'Not provided'}
    - Expected Salary Range: {clean_field(company_research.expected_salary_range) if company_research else 'Not provided'}
    - HR Contact Names: {clean_field(company_research.hr_contact_names) if company_research else 'Not provided'}

    📂 Application Notes
    - Notes: {clean_field(application_data.notes)}
    - Application Date: {application_data.application_date.strftime("%Y-%m-%d") if application_data.application_date else 'Not provided'}
    - Status: {clean_field(application_data.status)}
    """

    prompt = (
        "Summarize the following job and company research into a structured, "
        "professional report suitable for career tracking:\n\n" + research_text
    )

    response = await client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a career research assistant that generates clear, concise summaries with key highlights and actionable insights. Make it in paragraph form. Make it a report — don't give any meta-messages to the user."},
            {"role": "user", "content": prompt}
        ]
    )
    summary = response.choices[0].message.content
    save_summary_to_pdf(summary, f"application_{application_data.id}_report.pdf")
    return summary