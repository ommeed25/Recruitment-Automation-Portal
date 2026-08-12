
import re


COMPANY_NAME = "UnionSys Technologies"
RECRUITMENT_EMAIL = "careers@unionsystechnologies.com"

COMPANY_BENEFITS = [
    "Work with global clients",
    "Career growth opportunities",
    "Collaborative work culture",
    "Learning-driven environment",
]

COMMON_HASHTAGS = [
    "Hiring",
    "JobOpening",
    "CareerOpportunity",
    "Recruitment",
    "TalentAcquisition",
    "JobSearch",
    "CareerGrowth",
    "ProfessionalGrowth",
    "TechJobs",
    "WorkWithUs",
    "ApplyNow",
    "NowHiring",
    "FullTimeJobs",
    "JobSeekers",
    "CareerDevelopment",
    "LinkedInJobs",
    "Employment",
    "TeamGrowth",
    "Innovation",
    "FutureOfWork",
    "UnionSysTechnologies",
]


def _clean_text(value):
    return str(value or "").strip()


def _hashtag_words(value, include_compound=True):
    words = re.findall(r"[A-Za-z0-9]+", _clean_text(value))
    if not words:
        return []

    ignored_words = {
        "a",
        "an",
        "and",
        "for",
        "full",
        "in",
        "of",
        "or",
        "the",
        "time",
        "to",
        "with",
    }
    hashtags = ["".join(words)] if include_compound else []

    hashtags.extend(
        word
        for word in words
        if word.lower() not in ignored_words and len(word) > 1
    )

    return hashtags


def build_title(job):
    return f"We're Hiring: {_clean_text(job.job_posting_title)}"


def build_job_overview(job):
    return f"""We're looking for an experienced {_clean_text(job.job_posting_title)} to join our growing team.

Role details
- Location: {_clean_text(job.job_work_location)}
- Experience: {_clean_text(job.experience_slab)}
- Employment type: {_clean_text(job.job_type)}
- Open positions: {_clean_text(job.no_of_position)}
- Notice period: {_clean_text(job.notice_period)}"""


def build_skills(job):
    description = _clean_text(job.job_description or job.job_posting_skills)

    return f"""What you'll work on

{description}"""


def build_company_section():
    lines = [f"Why join {COMPANY_NAME}?", ""]
    lines.extend(f"- {benefit}" for benefit in COMPANY_BENEFITS)
    return "\n".join(lines)


def build_footer():
    return f"""Ready for your next opportunity?

Share your updated resume at {RECRUITMENT_EMAIL}.

Know someone who would be a great fit? Tag them or share this opportunity with your network.

Only shortlisted candidates will be contacted."""


def build_hashtags(job):
    job_values = [
        (job.job_posting_title, True),
        (job.job_posting_skills, False),
        (job.job_type, True),
        (job.job_work_location, True),
    ]

    hashtags = []
    seen = set()
    for value, include_compound in job_values:
        for word in _hashtag_words(value, include_compound):
            if word.lower() not in seen:
                hashtags.append(word)
                seen.add(word.lower())

    for hashtag in COMMON_HASHTAGS:
        if hashtag.lower() not in seen:
            hashtags.append(hashtag)
            seen.add(hashtag.lower())

        if len(hashtags) == 25:
            break

    return " ".join(f"#{hashtag}" for hashtag in hashtags)


def build_recruitment_post(job):
    sections = [
        build_title(job),
        build_job_overview(job),
        build_skills(job),
        build_company_section(),
        build_footer(),
        build_hashtags(job),
    ]

    return "\n\n".join(sections)