from dataclasses import dataclass


@dataclass
class DATABOARD_COLLECTIONS:
    USERS: str = "organization"
    TAGS: str = "tags"


@dataclass
class CLOCKER_COLLECTIONS:
    USERS: str = "users"
    PROFESSIONAL_CARD: str = "professionalCard"
    STUDENT_CARD: str = "studentCard"
    PERSONAL_CARD: str = "personalCard"
    CONTACTS: str = "contacts"
    NOTIFICATIONS: str = "notifications"
