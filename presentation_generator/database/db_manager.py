import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from ..models.presentation import Presentation, Section, Slide

class DatabaseManager:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / "config"
        self.config_dir.mkdir(exist_ok=True)
        self.db_path = self.config_dir / "presentations.db"
        self._init_database()
    
    def _init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS presentations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    summary TEXT,
                    language TEXT DEFAULT 'русский',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    presentation_id INTEGER,
                    title TEXT NOT NULL,
                    order_index INTEGER,
                    FOREIGN KEY (presentation_id) REFERENCES presentations (id) ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS slides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT,
                    order_index INTEGER,
                    FOREIGN KEY (section_id) REFERENCES sections (id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
    
    def save_presentation(self, presentation: Presentation) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO presentations (title, summary, language)
                VALUES (?, ?, ?)
            ''', (presentation.title, presentation.summary, presentation.language))
            
            presentation_id = cursor.lastrowid
            
            for section_index, section in enumerate(presentation.sections):
                cursor.execute('''
                    INSERT INTO sections (presentation_id, title, order_index)
                    VALUES (?, ?, ?)
                ''', (presentation_id, section.title, section_index))
                
                section_id = cursor.lastrowid
                
                for slide_index, slide in enumerate(section.slides):
                    cursor.execute('''
                        INSERT INTO slides (section_id, title, content, order_index)
                        VALUES (?, ?, ?, ?)
                    ''', (section_id, slide.title, slide.content, slide_index))
            
            conn.commit()
            return presentation_id
    
    def get_presentation(self, presentation_id: int) -> Optional[Presentation]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, summary, language FROM presentations WHERE id = ?
            ''', (presentation_id,))
            
            presentation_row = cursor.fetchone()
            if not presentation_row:
                return None
            
            title, summary, language = presentation_row
            
            cursor.execute('''
                SELECT id, title, order_index FROM sections 
                WHERE presentation_id = ? ORDER BY order_index
            ''', (presentation_id,))
            
            sections_data = cursor.fetchall()
            sections = []
            
            for section_id, section_title, order_index in sections_data:
                cursor.execute('''
                    SELECT title, content, order_index FROM slides 
                    WHERE section_id = ? ORDER BY order_index
                ''', (section_id,))
                
                slides_data = cursor.fetchall()
                slides = []
                
                for slide_title, slide_content, slide_order in slides_data:
                    slides.append(Slide(title=slide_title, content=slide_content))
                
                sections.append(Section(title=section_title, slides=slides))
            
            return Presentation(
                title=title,
                summary=summary,
                language=language,
                sections=sections
            )
    
    def update_presentation(self, presentation_id: int, presentation: Presentation):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE presentations 
                SET title = ?, summary = ?, language = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (presentation.title, presentation.summary, presentation.language, presentation_id))
            
            cursor.execute('DELETE FROM sections WHERE presentation_id = ?', (presentation_id,))
            
            for section_index, section in enumerate(presentation.sections):
                cursor.execute('''
                    INSERT INTO sections (presentation_id, title, order_index)
                    VALUES (?, ?, ?)
                ''', (presentation_id, section.title, section_index))
                
                section_id = cursor.lastrowid
                
                for slide_index, slide in enumerate(section.slides):
                    cursor.execute('''
                        INSERT INTO slides (section_id, title, content, order_index)
                        VALUES (?, ?, ?, ?)
                    ''', (section_id, slide.title, slide.content, slide_index))
            
            conn.commit()
    
    def list_presentations(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, summary, language, created_at, updated_at
                FROM presentations ORDER BY updated_at DESC
            ''')
            
            presentations = []
            for row in cursor.fetchall():
                presentations.append({
                    'id': row[0],
                    'title': row[1],
                    'summary': row[2],
                    'language': row[3],
                    'created_at': row[4],
                    'updated_at': row[5]
                })
            
            return presentations
    
    def delete_presentation(self, presentation_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM presentations WHERE id = ?', (presentation_id,))
            if not cursor.fetchone():
                return False
            
            cursor.execute('DELETE FROM presentations WHERE id = ?', (presentation_id,))
            conn.commit()
            return True
    
    def clear_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM presentations')
            conn.commit()