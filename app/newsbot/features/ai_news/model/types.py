from enum import Enum

class AISummaryType(str, Enum):
    """Enumeration for AI news summary time periods."""
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    
    @classmethod
    def values(cls):
        """Get all enum values as a list."""
        return [member.value for member in cls]