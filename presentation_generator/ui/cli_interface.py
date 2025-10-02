import os
import sys
import subprocess
import platform
import asyncio
import time
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
from ..database.settings_manager import SettingsManager
from ..config.api_config import ApiKeyManager
from .settings_interface import SettingsInterface

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class CLIInterface:
    def __init__(self):
        self.console = Console()
        self.settings = SettingsManager()
        self.loc = get_localization_manager()
        
        interface_lang = self.settings.get("interface_language", self.loc.t('language_russian'))
        self.loc.set_language(interface_lang)
        
        self.api_manager = ApiKeyManager()
        api_key = self.api_manager.get_api_key()
        self.service = PresentationService(api_key, interface_language=self.loc.current_language)
        self.settings_ui = SettingsInterface(self.settings, self.loc)
        
    def show_header(self):
        app_title_lines = self.loc.t("app_title").split('\n')
        header_text = Text()
        
        if len(app_title_lines) > 1:
            header_text.append(app_title_lines[0], style="bold cyan")
            header_text.append("\n")
            header_text.append(app_title_lines[1], style="dim white")
        else:
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
        menu_table.add_row("2", self.loc.t("menu_manage"))
        menu_table.add_row("3", self.loc.t("menu_settings"))
        menu_table.add_row("4", self.loc.t("menu_exit"))
        
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
            default=self.loc.t('language_russian')
        )
        
        if language_choice not in [self.loc.t('language_russian'), self.loc.t('language_english')]:
            language_choice = self.loc.t('language_russian')
        
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
        
        self.console.print()
        self.console.print(Panel(
            f"[cyan]{self.loc.t('web_search_info')}[/cyan]",
            title=f"[bold white]{self.loc.t('enable_web_search')}[/bold white]",
            border_style="cyan"
        ))
        
        enable_web_search = Confirm.ask(
            f"[bold cyan]{self.loc.t('enable_web_search')}[/bold cyan]",
            default=False
        )
        
        return {
            'title': title,
            'language': language_choice,
            'max_sections': max_sections,
            'max_slides': max_slides,
            'enable_web_search': enable_web_search
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
            
            try:
                presentation = asyncio.run(self.service.generate_presentation(
                    progress_callback=progress_callback,
                    **kwargs
                ))
                
                progress.update(task, description=self.loc.t("generation_complete"), completed=1, total=1)
            except Exception as e:
                progress.update(task, description=self.loc.t("generation_failed"), completed=1, total=1)
                self.console.print(f"\n[bold red]{self.loc.t('generation_error')}: {e}[/bold red]")
                return None
            
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
            self.console.print(f"2. {self.loc.t('skip')}")
            
            choice = Prompt.ask(
                self.loc.t("choose_option")
            )
            
            if choice not in ["1", "2"]:
                self.console.print(f"[bold red]{self.loc.t('invalid_choice_3')}[/bold red]")
                choice = "1"
            
            if choice == "1":
                self.open_file(file_path)
                
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
    
    def manage_presentations(self):
        while True:
            
            menu_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
            menu_table.add_column(self.loc.t("option_column"), style="bold cyan", width=3)
            menu_table.add_column(self.loc.t("description_column"), style="white")
            
            menu_table.add_row("1", self.loc.t("menu_show"))
            menu_table.add_row("2", self.loc.t("menu_delete"))
            menu_table.add_row("3", self.loc.t("back_to_main"))
            
            menu_panel = Panel(
                menu_table,
                title=f"[bold white]{self.loc.t('manage_presentations')}[/bold white]",
                border_style="bright_yellow",
                padding=(1, 2)
            )
            self.console.print(menu_panel)
            
            choice = Prompt.ask(f"\n{self.loc.t('choose_option')}", choices=["1", "2", "3"])
            
            if choice == "1":
                self.show_saved_presentations()
            elif choice == "2":
                self.delete_presentation()
            elif choice == "3":
                break
    
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
    
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_header()
        
        try:
            while True:
                self.show_menu()
                
                choice = Prompt.ask(
                    f"\n[bold cyan]{self.loc.t('choose_option')}[/bold cyan]"
                )
                
                if choice not in ["1", "2", "3", "4", "5"]:
                    self.console.print(f"[bold red]{self.loc.t('invalid_choice')}[/bold red]")
                    continue
                
                self.console.print()
                
                if choice == "1":
                    try:
                        details = self.get_presentation_details()
                        self.console.print()
                        
                        presentation = self.generate_presentation_with_progress(**details)
                        
                        if presentation:
                            self.console.print()
                            self.show_presentation_summary(presentation)
                            self.save_and_open_presentation(presentation)
                        else:
                            self.console.print(f"\n[bold red]{self.loc.t('generation_stopped')}[/bold red]")
                        
                    except KeyboardInterrupt:
                        self.console.print(f"\n[bold yellow]{self.loc.t('generation_cancelled')}[/bold yellow]")
                    except Exception as e:
                        self.console.print(f"\n[bold red]{self.loc.t('generation_error')} {e}[/bold red]")
                        
                elif choice == "2":
                    self.manage_presentations()
                    
                elif choice == "3":
                    self.show_settings_menu()
                    
                elif choice == "4":
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
                    self.restart_program()
                else:
                    self.console.print(f"[bold red]{self.loc.t('error')}[/bold red]")
            else:
                self.console.print(f"[bold red]{self.loc.t('invalid_number')}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red]{self.loc.t('error')} {e}[/bold red]")
    
    def show_settings_menu(self):
        self.settings_ui.show_settings_menu()
    
    def restart_program(self):
        self.console.print(f"[bold yellow]{self.loc.t('restart_note')}[/bold yellow]")
        self.console.print(f"[bold cyan]{self.loc.t('restarting')}[/bold cyan]")
        time.sleep(1.5)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        python = sys.executable
        os.execv(python, [python] + sys.argv)
