from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Slide:
    title: str
    content: str
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'content': self.content
        }


@dataclass 
class Section:
    title: str
    slides: List[Slide] = field(default_factory=list)
    
    def add_slide(self, slide: Slide) -> None:
        self.slides.append(slide)
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'slides': [slide.to_dict() for slide in (self.slides or [])]
        }


@dataclass
class Presentation:
    title: str
    language: str = 'русский'
    summary: Optional[str] = None
    sections: List[Section] = field(default_factory=list)
    max_sections: int = 3
    max_slides: int = 4
    created_at: datetime = field(default_factory=datetime.now)
    generated: bool = False
    
    def add_section(self, section: Section) -> None:
        self.sections.append(section)
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'language': self.language,
            'summary': self.summary,
            'sections': [section.to_dict() for section in (self.sections or [])],
            'max_sections': self.max_sections,
            'max_slides': self.max_slides,
            'created_at': self.created_at.isoformat(),
            'generated': self.generated
        }
    
    def get_total_slides(self) -> int:
        if not self.sections:
            return 0
        return sum(len(section.slides) for section in self.sections)
