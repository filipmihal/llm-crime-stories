from dataclasses import dataclass
from typing import List, Optional

@dataclass
class StoryPayload:
    """
    Represents a container for a context needed to generate the description of a location.
    """
    
    """
    Describes the general atmosphere of a story.
    """
    atmosphere: Optional[List[str]] = None
    
    """
    When something goes wrong e.g. player tries to move in a forbidden direction, this contains the information.
    """
    error: Optional[str] = None
    
    """
    "Just print this".
    """
    text: Optional[str] = None