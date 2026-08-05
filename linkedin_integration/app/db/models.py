from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True)
    
    job_posting_title = Column(String(255), nullable=False)
    job_posting_date = Column(TIMESTAMP)
    job_description = Column(Text)
    additional_information = Column(Text)

    job_posting_skills = Column(Text)
    job_type = Column(String(255))
    experience_slab = Column(String(255))

    min_exp = Column(Integer)
    max_exp = Column(Integer)

    job_work_location = Column(String(255))
    job_mode = Column(String(50))

    job_budget = Column(String(255))
    notice_period = Column(String(255))

    priority = Column(String(255))
    status = Column(String(255))
    assign_status = Column(String(255))

    no_of_position = Column(Integer)

    created_by = Column(String(255))
    created_on = Column(TIMESTAMP)

    updated_by = Column(String(255))
    updated_on = Column(TIMESTAMP)

    linkedin_posted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    synced_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
   

    posts = relationship(
    "LinkedInPost",
    back_populates="job"
)


class LinkedInAccount(Base):
    __tablename__ = "linkedin_accounts"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, nullable=True)

    linkedin_sub = Column(String(255), unique=True, nullable=True)

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    access_token = Column(Text, nullable=True)
    token_type = Column(String(20), nullable=True)
    expires_in = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    posts = relationship(
        "LinkedInPost",
        back_populates="linkedin_account"
    )

class LinkedInPost(Base):
    __tablename__ = "linkedin_posts"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.job_id"),
        nullable=False
    )

    linkedin_account_id = Column(
        Integer,
        ForeignKey("linkedin_accounts.id"),
        nullable=False
    )

    linkedin_post_id = Column(String(255))

    post_status = Column(String(50), nullable=False)

    error_message = Column(Text)

    posted_at = Column(TIMESTAMP)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    job = relationship(
        "Job",
        back_populates="posts"
    )

    linkedin_account = relationship(
        "LinkedInAccount",
        back_populates="posts"
    )