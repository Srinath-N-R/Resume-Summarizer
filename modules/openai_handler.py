from openai import OpenAI
from config import Config

# Initialize the OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def extract_information_with_gpt(text):
    """
    Use OpenAI GPT to extract structured information like name, location, nationality, organization, 
    education, skills, projects, tools, and other relevant info.
    This version also extracts the last two jobs, their timelines, and responsibilities.
    """
    prompt = (
        "You are a resume parser. Extract the following information from the resume text: "
        "1. The full name of the person. "
        "2. Their current location and nationality. "
        "3. Any useful links (LinkedIn, personal website, GitHub, etc.). "
        "4. The two most recent jobs, including the organization, organization location, job title, timeline (start and end dates)"
        "5. Their education details (schools, degrees, and dates if available). "
        "6. A list of hard skills. "
        "7. A list of soft skills. "
        "8. Tools and technologies they are familiar with. "
        "9. A list of their major projects. "
        "10. Any other relevant details (certifications, awards, etc.). "
        "Return the results in the following structured format:\n\n"
        "Name: <person's name>\n"
        "Location: <location>\n"
        "Nationality: <nationality>\n"
        "Useful Links: <useful links>\n"
        "Job 1: <organization>, <job title>, <start date> - <end date>\n"
        "Responsibilities 1: <list of responsibilities for job 1>\n"
        "Job 2: <organization>, <job title>, <start date> - <end date>\n"
        "Responsibilities 2: <list of responsibilities for job 2>\n"
        "Education: <education details>\n"
        "Hard Skills: <list of hard skills>\n"
        "Soft Skills: <list of soft skills>\n"
        "Tools: <list of tools>\n"
        "Projects: <list of projects>\n"
        "Other Relevant Info: <certifications, awards, etc.>\n\n"
        f"Resume Text: {text}"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

def generate_summary(name, job1, job2, education, hard_skills, soft_skills, tools, projects, other_info):
    """
    Use OpenAI GPT to generate a professional summary based on extracted details, including the last two jobs.
    """
    prompt = (
        f"Generate a professional summary based on the following details:\n"
        f"Name: {name}\n"
        f"Most Recent Job: {job1['organization']}, {job1['job_title']}, {job1['start_date']} - {job1['end_date']}\n"
        f"Responsibilities: {', '.join(job1['responsibilities'])}\n"
        f"Second Most Recent Job: {job2['organization']}, {job2['job_title']}, {job2['start_date']} - {job2['end_date']}\n"
        f"Responsibilities: {', '.join(job2['responsibilities'])}\n"
        f"Education: {', '.join(education)}\n"
        f"Hard Skills: {', '.join(hard_skills)}\n"
        f"Soft Skills: {', '.join(soft_skills)}\n"
        f"Tools: {', '.join(tools)}\n"
        f"Projects: {', '.join(projects)}\n"
        f"Other Info: {other_info}"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()