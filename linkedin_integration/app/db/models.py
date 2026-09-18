from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, Date
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


class SalesLinkedInAccount(Base):
    __tablename__ = "sales_linkedin_accounts"

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

class VendorImage(Base):
    __tablename__ = "vendor_images"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)

    is_active = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

class SalesImage(Base):
    __tablename__ = "sales_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())




class VendorHashtag(Base):
    __tablename__ = "vendor_hashtags"

    id = Column(Integer, primary_key=True, index=True)

    hashtag = Column(String(255), nullable=False)

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )


class SalesHashtag(Base):
    __tablename__ = "sales_hashtags"

    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    
class VendorSettings(Base):
    __tablename__ = "vendor_settings"

    id = Column(Integer, primary_key=True, index=True)

    is_enabled = Column(
        Boolean,
        default=True,
        nullable=False
    )

    posting_time = Column(
        String(10),
        nullable=False,
        default="10:00"
    )

    active_image_id = Column(
        Integer,
        ForeignKey("vendor_images.id"),
        nullable=True
    )

    rotation_index = Column(
        Integer,
        nullable=False,
        default=0
    )

    last_rotation_date = Column(
        TIMESTAMP,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    active_image = relationship(
        "VendorImage"
    )

class SalesSettings(Base):
    __tablename__ = "sales_settings"

    id = Column(Integer, primary_key=True, index=True)
    is_enabled = Column(Boolean, default=True, nullable=False)
    posting_time = Column(String(10), nullable=False, default="10:00")
    active_image_id = Column(
        Integer,
        ForeignKey("sales_images.id"),
        nullable=True
    )
    rotation_index = Column(Integer, nullable=False, default=0)
    last_rotation_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    active_image = relationship("SalesImage")


class VendorPostHistory(Base):
    __tablename__ = "vendor_post_history"

    id = Column(Integer, primary_key=True, index=True)

    linkedin_account_id = Column(
        Integer,
        ForeignKey("linkedin_accounts.id"),
        nullable=False
    )

    linkedin_post_id = Column(String(255))

    post_status = Column(
        String(50),
        nullable=False
    )

    error_message = Column(Text)

    posted_at = Column(TIMESTAMP)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    linkedin_account = relationship(
        "LinkedInAccount"
    )

class SalesPostHistory(Base):
    __tablename__ = "sales_post_history"

    id = Column(Integer, primary_key=True, index=True)
    sales_linkedin_account_id = Column(
        Integer,
        ForeignKey("sales_linkedin_accounts.id"),
        nullable=False
    )
    linkedin_post_id = Column(String(255), nullable=True)
    post_status = Column(String(50), nullable=False)
    error_message = Column(Text, nullable=True)
    posted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    sales_linkedin_account = relationship("SalesLinkedInAccount")