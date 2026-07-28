import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()


@dataclass
class LinkedInDeps:
    client_id: str = field(
        default_factory=lambda: os.getenv("LINKEDIN_CLIENT_ID", "")
    )
    client_secret: str = field(
        default_factory=lambda: os.getenv("LINKEDIN_CLIENT_SECRET", "")
    )
    redirect_uri: str = field(
        default_factory=lambda: os.getenv(
            "LINKEDIN_REDIRECT_URI", "https://www.linkedin.com/jobs/"
        )
    )