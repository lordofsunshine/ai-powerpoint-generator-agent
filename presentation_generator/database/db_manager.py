import sqlite3
import json
import sys
import atexit
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from ..models.presentation import Presentation, Section, Slide

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path
        
class DatabaseManager:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        atexit.register(self.cleanup)
    
    def _create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presentations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                language TEXT DEFAULT 'русский',
                summary TEXT,
                title_slide_header TEXT,
                max_sections INTEGER DEFAULT 3,
                max_slides INTEGER DEFAULT 4,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                generated BOOLEAN DEFAULT FALSE,
                data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                presentation_id INTEGER,
                title TEXT NOT NULL,
                position INTEGER DEFAULT 0,
                FOREIGN KEY (presentation_id) REFERENCES presentations (id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                position INTEGER DEFAULT 0,
                FOREIGN KEY (section_id) REFERENCES sections (id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
    
    def save_presentation(self, presentation: Presentation) -> int:
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO presentations (title, language, summary, title_slide_header, max_sections, max_slides, generated, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            presentation.title,
            presentation.language,
            presentation.summary,
            presentation.title_slide_header,
            presentation.max_sections,
            presentation.max_slides,
            presentation.generated,
            json.dumps(presentation.to_dict())
        ))
        
        presentation_id = cursor.lastrowid
        
        for section_pos, section in enumerate(presentation.sections):
            cursor.execute('''
                INSERT INTO sections (presentation_id, title, position)
                VALUES (?, ?, ?)
            ''', (presentation_id, section.title, section_pos))
            
            section_id = cursor.lastrowid
            
            for slide_pos, slide in enumerate(section.slides):
                cursor.execute('''
                    INSERT INTO slides (section_id, title, content, position)
                    VALUES (?, ?, ?, ?)
                ''', (section_id, slide.title, slide.content, slide_pos))
        
        self.conn.commit()
        return presentation_id
    
    def get_presentation(self, presentation_id: int) -> Optional[Presentation]:
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT * FROM presentations WHERE id = ?', (presentation_id,))
        pres_row = cursor.fetchone()
        
        if not pres_row:
            return None
        
        presentation = Presentation(
            title=pres_row['title'],
            language=pres_row['language'],
            summary=pres_row['summary'],
            title_slide_header=pres_row['title_slide_header'],
            max_sections=pres_row['max_sections'],
            max_slides=pres_row['max_slides'],
            generated=bool(pres_row['generated'])
        )
        
        cursor.execute('''
            SELECT * FROM sections WHERE presentation_id = ? ORDER BY position
        ''', (presentation_id,))
        sections = cursor.fetchall()
        
        for section_row in sections:
            section = Section(title=section_row['title'])
            
            cursor.execute('''
                SELECT * FROM slides WHERE section_id = ? ORDER BY position
            ''', (section_row['id'],))
            slides = cursor.fetchall()
            
            for slide_row in slides:
                slide = Slide(
                    title=slide_row['title'],
                    content=slide_row['content']
                )
                section.add_slide(slide)
            
            presentation.add_section(section)
        
        return presentation
    
    def update_presentation(self, presentation_id: int, presentation: Presentation) -> bool:
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE presentations 
                SET title = ?, language = ?, summary = ?, title_slide_header = ?, max_sections = ?, max_slides = ?, generated = ?, data = ?
                WHERE id = ?
            ''', (
                presentation.title,
                presentation.language,
                presentation.summary,
                presentation.title_slide_header,
                presentation.max_sections,
                presentation.max_slides,
                presentation.generated,
                json.dumps(presentation.to_dict()),
                presentation_id
            ))
            
            cursor.execute('DELETE FROM sections WHERE presentation_id = ?', (presentation_id,))
            
            for section_pos, section in enumerate(presentation.sections):
                cursor.execute('''
                    INSERT INTO sections (presentation_id, title, position)
                    VALUES (?, ?, ?)
                ''', (presentation_id, section.title, section_pos))
                
                section_id = cursor.lastrowid
                
                for slide_pos, slide in enumerate(section.slides):
                    cursor.execute('''
                        INSERT INTO slides (section_id, title, content, position)
                        VALUES (?, ?, ?, ?)
                    ''', (section_id, slide.title, slide.content, slide_pos))
            
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False
    
    def list_presentations(self) -> List[Dict]:
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT id, title, language, created_at, generated 
            FROM presentations 
            ORDER BY created_at DESC
        ''')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_presentation(self, presentation_id: int) -> bool:
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('DELETE FROM presentations WHERE id = ?', (presentation_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception:
            return False
    
    def cleanup(self):
        if self.conn:
            self.conn.close()
    
    def clear_all(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM presentations')
        cursor.execute('DELETE FROM sections') 
        cursor.execute('DELETE FROM slides')
        self.conn.commit()
