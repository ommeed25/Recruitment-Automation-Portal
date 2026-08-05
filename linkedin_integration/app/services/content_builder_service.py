
def build_title(job):

    return (
        f"🚀 We're Hiring | "
        f"{job.job_posting_title} 🚀"
    )

def build_job_overview(job):

 return f"""We're looking for an experienced {job.job_posting_title} to join our growing team.

📍 Location: {job.job_work_location}
💼 Experience: {job.experience_slab}
🕒 Employment Type: {job.job_type}
👥 Open Positions: {job.no_of_position}
📅 Notice Period: {job.notice_period}
"""

def build_skills(job):

    description = (
        job.job_description
        if job.job_description
        else job.job_posting_skills
    )

    return f"""
✅ Key Skills & Responsibilities

{description}
"""

COMPANY_NAME = "UnionSys Technologies"

COMPANY_BENEFITS = [

    "Work with global clients",

    "Career growth opportunities",

    "Collaborative work culture",

    "Learning-driven environment"

]


def build_company_section():

    lines = [

        f"✨ Why Join {COMPANY_NAME}?",

        ""

    ]

    for benefit in COMPANY_BENEFITS:

        lines.append(f"• {benefit}")

    return "\n".join(lines) 


RECRUITMENT_EMAIL = "careers@unionsystechnologies.com"


def build_footer():

    return f"""
📩 Interested candidates can share their updated resume at:

📧 {RECRUITMENT_EMAIL}

Know someone who would be a great fit?

🔁 Tag them in the comments or share this opportunity with your network.

Only shortlisted candidates will be contacted.
"""


def build_hashtags(job):

    title = (
        job.job_posting_title
        .replace(" ", "")
        .replace("-", "")
    )

    return (
        f"#Hiring "
        f"#{title} "
        f"#Jobs "
        f"#Career "
        f"#UnionSysTechnologies"
    )

def build_recruitment_post(job):

    sections = [

        build_title(job),

        build_job_overview(job),

        build_skills(job),

        build_company_section(),

        build_footer(),

        build_hashtags(job)

    ]

    return "\n\n".join(sections)