import os
import sys
import subprocess
import platform
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich import box
from ..services.presentation_service import PresentationService
from ..localization.manager import get_localization_manager

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class CLIInterface:
    def __init__(self):
        self.console = Console()
        self.loc = get_localization_manager()
        self.service = PresentationService(interface_language=self.loc.current_language)
        
    def show_header(self):
        header_text = Text()
        header_text.append(self.loc.t("app_title"), style="bold cyan")
        
        header_panel = Panel(
            header_text,
            box=box.DOUBLE,
            style="bold cyan",
            padding=(1, 2)
        )
        self.console.print(header_panel)
        self.console.print()
    
    def show_menu(self):
        menu_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        menu_table.add_column(self.loc.t("option_column"), style="bold cyan", width=3)
        menu_table.add_column(self.loc.t("description_column"), style="white")
        
        menu_table.add_row("1", self.loc.t("menu_create"))
        menu_table.add_row("2", self.loc.t("menu_show"))
        menu_table.add_row("3", self.loc.t("menu_correct"))
        menu_table.add_row("4", self.loc.t("menu_delete"))
        menu_table.add_row("5", self.loc.t("menu_language"))
        menu_table.add_row("6", self.loc.t("menu_exit"))
        
        menu_panel = Panel(
            menu_table,
            title=f"[bold white]{self.loc.t('main_menu')}[/bold white]",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(menu_panel)
    
    def get_presentation_details(self) -> dict:
        self.console.print(Panel(
            f"[bold white]{self.loc.t('new_presentation')}[/bold white]",
            style="cyan"
        ))
        self.console.print()
        
        title = Prompt.ask(
            f"[bold cyan]{self.loc.t('enter_title')}[/bold cyan]",
            default=self.loc.t("default_title")
        )
        
        language_choice = Prompt.ask(
            f"[bold cyan]{self.loc.t('choose_language')}[/bold cyan]",
            choices=["русский", "english"],
            default="русский"
        )
        
        max_sections = IntPrompt.ask(
            f"[bold cyan]{self.loc.t('section_count')}[/bold cyan]",
            default=1,
            show_default=True
        )
        
        max_slides = IntPrompt.ask(
            f"[bold cyan]{self.loc.t('slide_count')}[/bold cyan]",
            default=4,
            show_default=True
        )
        
        return {
            'title': title,
            'language': language_choice,
            'max_sections': max_sections,
            'max_slides': max_slides
        }
    
    def generate_presentation_with_progress(self, **kwargs):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            console=self.console,
            transient=False
        ) as progress:
            
            task = progress.add_task(self.loc.t("initializing"), total=1)
            
            def progress_callback(description: str, current: int, total: int):
                progress.update(task, description=description, completed=current, total=total)
            
            presentation = self.service.generate_presentation(
                progress_callback=progress_callback,
                **kwargs
            )
            
            progress.update(task, description=self.loc.t("generation_complete"), completed=1, total=1)
            
        return presentation
    
    def show_presentation_summary(self, presentation):
        stats = self.service.get_presentation_stats(presentation)
        
        summary_table = Table(show_header=False, box=box.SIMPLE)
        summary_table.add_column(self.loc.t("parameter_column"), style="bold cyan", width=20)
        summary_table.add_column(self.loc.t("value_column"), style="white")
        
        summary_table.add_row(self.loc.t("title"), stats['title'])
        summary_table.add_row(self.loc.t("sections"), str(stats['sections_count']))
        summary_table.add_row(self.loc.t("total_slides"), str(stats['total_slides']))
        summary_table.add_row(self.loc.t("language"), stats['language'])
        summary_table.add_row(self.loc.t("created"), stats['created_at'])
        
        summary_panel = Panel(
            summary_table,
            title=f"[bold white]{self.loc.t('presentation_info')}[/bold white]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(summary_panel)
    
    def save_and_open_presentation(self, presentation):
        self.console.print(f"\n[bold cyan]{self.loc.t('saving')}[/bold cyan]")
        
        try:
            presentation_id = self.service.save_to_database(presentation)
            file_path = self.service.save_presentation(presentation)
            
            self.console.print(f"[bold green]{self.loc.t('saved')} {file_path}[/bold green]")
            self.console.print(f"[bold green]{self.loc.t('db_id')} {presentation_id}[/bold green]")
            
            self.console.print(f"\n[bold cyan]{self.loc.t('what_next')}[/bold cyan]")
            self.console.print(f"1. {self.loc.t('open_pres')}")
            self.console.print(f"2. {self.loc.t('correct_pres')}")
            self.console.print(f"3. {self.loc.t('skip')}")
            
            choice = Prompt.ask(
                self.loc.t("choose_option"),
                choices=["1", "2", "3"],
                default="1"
            )
            
            if choice == "1":
                self.open_file(file_path)
            elif choice == "2":
                self.correct_presentation_dialog(presentation_id, presentation.language)
                
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('save_error')} {e}[/bold red]")
    
    def open_file(self, file_path: str):
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":
                subprocess.run(["open", file_path])
            elif system == "Linux":
                subprocess.run(["xdg-open", file_path])
            
            self.console.print(f"[bold green]{self.loc.t('opened')}[/bold green]")
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('open_error')} {e}[/bold red]")
    
    def show_saved_presentations(self):
        presentations = self.service.list_saved_presentations()
        
        if not presentations:
            self.console.print(Panel(
                f"[yellow]{self.loc.t('no_saved')}[/yellow]",
                style="yellow"
            ))
            return
        
        table = Table(title=self.loc.t("saved_presentations"), box=box.ROUNDED)
        table.add_column("№", style="cyan", width=5)
        table.add_column(self.loc.t("filename"), style="white")
        
        for i, filename in enumerate(presentations, 1):
            table.add_row(str(i), filename)
        
        self.console.print(table)
        self.console.print()
        
        if Confirm.ask(f"[bold cyan]{self.loc.t('open_question')}[/bold cyan]"):
            try:
                choice = IntPrompt.ask(
                    self.loc.t("enter_presentation_number"),
                    show_default=False
                )
                if 1 <= choice <= len(presentations):
                    filename = presentations[choice - 1]
                    file_path = os.path.join("output", filename)
                    self.open_file(file_path)
                else:
                    self.console.print(f"[bold red]{self.loc.t('invalid_number')}[/bold red]")
            except Exception as e:
                self.console.print(f"[bold red]{self.loc.t('error')} {e}[/bold red]")
    
    def delete_presentation(self):
        presentations = self.service.list_saved_presentations()
        
        if not presentations:
            self.console.print(Panel(
                f"[yellow]{self.loc.t('no_delete')}[/yellow]",
                style="yellow"
            ))
            return
        
        table = Table(title=self.loc.t("delete_presentation"), box=box.ROUNDED)
        table.add_column("№", style="cyan", width=5)
        table.add_column(self.loc.t("filename"), style="white")
        
        for i, filename in enumerate(presentations, 1):
            table.add_row(str(i), filename)
        
        self.console.print(table)
        
        try:
            choice = IntPrompt.ask(
                self.loc.t("enter_delete_number"),
                show_default=False
            )
            
            if 1 <= choice <= len(presentations):
                filename = presentations[choice - 1]
                
                if Confirm.ask(f"[bold red]{self.loc.t('confirm_delete').format(filename)}[/bold red]"):
                    if self.service.delete_saved_presentation(filename):
                        self.console.print(f"[bold green]{self.loc.t('deleted').format(filename)}[/bold green]")
                    else:
                        self.console.print(f"[bold red]{self.loc.t('delete_error').format(filename)}[/bold red]")
            else:
                self.console.print(f"[bold red]{self.loc.t('invalid_number')}[/bold red]")
                
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('error')} {e}[/bold red]")
    
    def correct_presentation_dialog(self, presentation_id: int, language: str = "русский"):
        self.console.print(Panel(
            f"[bold white]{self.loc.t('correction_title')}[/bold white]",
            style="yellow"
        ))
        
        correction_prompt = Prompt.ask(
            f"[bold cyan]{self.loc.t('describe_changes')}[/bold cyan]"
        )
        
        progress_text = ""
        
        def progress_callback(text: str):
            nonlocal progress_text
            progress_text = text
            self.console.print(f"[bold cyan]↻ {text}[/bold cyan]")
        
        try:
            corrected_presentation = self.service.apply_correction(
                presentation_id, correction_prompt, language, progress_callback
            )
            
            if corrected_presentation:
                self.console.print(f"[bold green]{self.loc.t('correction_applied')}[/bold green]")
                
                if Confirm.ask(f"\n[bold cyan]{self.loc.t('save_corrected')}[/bold cyan]"):
                    file_path = self.service.save_presentation(corrected_presentation)
                    self.console.print(f"[bold green]{self.loc.t('saved')} {file_path}[/bold green]")
                    
                    if Confirm.ask(f"\n[bold cyan]{self.loc.t('open_question')}[/bold cyan]"):
                        self.open_file(file_path)
                
                if Confirm.ask(f"\n[bold cyan]{self.loc.t('more_changes')}[/bold cyan]"):
                    self.correct_presentation_dialog(presentation_id, language)
            else:
                self.console.print(f"[bold red]{self.loc.t('correction_failed')}[/bold red]")
                
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('correction_error')} {e}[/bold red]")
    
    def show_correction_menu(self):
        presentations = self.service.get_database_presentations()
        
        if not presentations:
            self.console.print(Panel(
                f"[yellow]{self.loc.t('no_corrections')}[/yellow]",
                style="yellow"
            ))
            return
        
        table = Table(title=self.loc.t("correction_menu"), box=box.ROUNDED)
        table.add_column("ID", style="cyan", width=5)
        table.add_column(self.loc.t("title"), style="white")
        table.add_column(self.loc.t("language"), style="green", width=10)
        table.add_column(self.loc.t("created"), style="blue", width=15)
        
        for pres in presentations:
            created_at = pres['created_at'][:16] if pres['created_at'] else self.loc.t("unknown_date")
            table.add_row(
                str(pres['id']),
                pres['title'],
                pres['language'],
                created_at
            )
        
        self.console.print(table)
        self.console.print()
        
        try:
            choice = IntPrompt.ask(
                self.loc.t("enter_correction_id"),
                show_default=False
            )
            
            selected_pres = next((p for p in presentations if p['id'] == choice), None)
            if selected_pres:
                self.correct_presentation_dialog(choice, selected_pres['language'])
            else:
                self.console.print(f"[bold red]{self.loc.t('id_not_found')}[/bold red]")
                
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('error')} {e}[/bold red]")
    
    def run(self):
        self.console.clear()
        self.show_header()
        
        try:
            while True:
                self.show_menu()
                
                choice = Prompt.ask(
                    f"\n[bold cyan]{self.loc.t('choose_option')}[/bold cyan]",
                    choices=["1", "2", "3", "4", "5", "6"],
                    show_choices=False
                )
                
                self.console.print()
                
                if choice == "1":
                    try:
                        details = self.get_presentation_details()
                        self.console.print()
                        
                        presentation = self.generate_presentation_with_progress(**details)
                        
                        self.console.print()
                        self.show_presentation_summary(presentation)
                        self.save_and_open_presentation(presentation)
                        
                    except KeyboardInterrupt:
                        self.console.print(f"\n[bold yellow]{self.loc.t('generation_cancelled')}[/bold yellow]")
                    except Exception as e:
                        self.console.print(f"\n[bold red]{self.loc.t('generation_error')} {e}[/bold red]")
                        
                elif choice == "2":
                    self.show_saved_presentations()
                    
                elif choice == "3":
                    self.show_correction_menu()
                    
                elif choice == "4":
                    self.delete_presentation()
                    
                elif choice == "5":
                    self.show_language_menu()
                    
                elif choice == "6":
                    self.console.print(Panel(
                        f"[bold white]{self.loc.t('goodbye')}[/bold white]",
                        style="cyan"
                    ))
                    break
                
                self.console.print("\n" + "─" * 50 + "\n")
                
        finally:
            self.service.cleanup_database()
    
    def show_language_menu(self):
        self.console.print(Panel(
            f"[bold white]{self.loc.t('language_settings')}[/bold white]",
            style="yellow"
        ))
        
        current_lang = self.loc.get_language()
        self.console.print(f"\n[bold cyan]{self.loc.t('current_language')} {current_lang}[/bold cyan]")
        
        languages = self.loc.get_available_languages()
        
        self.console.print(f"\n[bold cyan]{self.loc.t('choose_interface_lang')}[/bold cyan]")
        for i, lang in enumerate(languages, 1):
            self.console.print(f"{i}. {lang}")
        
        try:
            choice = IntPrompt.ask(
                self.loc.t("choose_option"),
                show_default=False
            )
            
            if 1 <= choice <= len(languages):
                new_language = languages[choice - 1]
                if self.loc.set_language(new_language):
                    self.console.print(f"[bold green]{self.loc.t('language_changed')}[/bold green]")
                    self.console.print(f"[bold yellow]{self.loc.t('restart_note')}[/bold yellow]")
                else:
                    self.console.print(f"[bold red]{self.loc.t('error')}[/bold red]")
            else:
                self.console.print(f"[bold red]{self.loc.t('invalid_number')}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('error')} {e}[/bold red]")
