from pydantic import BaseModel


class VendorHashtagBulkCreate(BaseModel):
    hashtags: list[str]