from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import box


class SettingsInterface:
    def __init__(self, settings_manager, loc_manager):
        self.console = Console()
        self.settings = settings_manager
        self.loc = loc_manager
        
        self.ai_models = {
            "1": ("deepseek-ai/DeepSeek-R1-0528", "Deepseek R1"),
            "2": ("Apertus-70B-Instruct-2509", "Swiss AI Apertus"),
            "3": ("meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", "Meta Llama 4 Maverick"),
            "4": ("gpt-oss-120b", "OpenAI GPT OSS 120B"),
            "5": ("Intel/Qwen3-Coder-480B-A35B-Instruct-int4-mixed-ar", "Qwen3 Coder"),
            "6": ("Qwen3-Next-80B-A3B-Instruct", "Qwen3 Next"),
            "7": ("gpt-oss-20b", "OpenAI GPT OSS 20B"),
            "8": ("Qwen3-235B-A22B-Thinking-2507", "Qwen3 Thinking"),
            "9": ("Mistral-Nemo-Instruct-2407", "Mistral Nemo"),
            "10": ("mistralai/Magistral-Small-2506", "Mistral Magistral Small"),
            "11": ("mistralai/Devstral-Small-2505", "Mistral Devstral Small"),
            "12": ("K2-Think", "LLM360 K2-Think"),
            "13": ("meta-llama/Llama-3.3-70B-Instruct", "Meta Llama 3.3"),
            "14": ("mistralai/Mistral-Large-Instruct-2411", "Mistral Large"),
            "15": ("Qwen/Qwen2.5-VL-32B-Instruct", "Qwen2.5 Vision-Language"),
            "16": ("meta-llama/Llama-3.2-90B-Vision-Instruct", "Meta Llama 3.2 Vision"),
            "17": ("BAAI/bge-multilingual-gemma2", "BAAI BGE Multilingual")
        }
    
    def show_settings_menu(self):
        while True:
            
            menu_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
            menu_table.add_column(self.loc.t("option_column"), style="bold green", width=3)
            menu_table.add_column(self.loc.t("description_column"), style="white")
            
            menu_table.add_row("1", f"● {self.loc.t('settings_interface')}")
            menu_table.add_row("2", f"● {self.loc.t('settings_presentation')}")
            menu_table.add_row("3", f"● {self.loc.t('settings_ai')}")
            menu_table.add_row("4", f"● {self.loc.t('settings_search')}")
            menu_table.add_row("5", f"● {self.loc.t('clear_database')}")
            menu_table.add_row("6", f"{self.loc.t('back_to_main')}")
            
            menu_panel = Panel(
                menu_table,
                title=f"[bold white]{self.loc.t('general_settings')}[/bold white]",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(menu_panel)
            
            choice = Prompt.ask(f"\n{self.loc.t('choose_option')}", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self.show_interface_settings()
            elif choice == "2":
                self.show_presentation_settings()
            elif choice == "3":
                self.show_ai_settings()
            elif choice == "4":
                self.show_search_settings()
            elif choice == "5":
                self.show_clear_database()
            elif choice == "6":
                break
    
    def show_interface_settings(self):
        current_lang = self.settings.get("interface_language", self.loc.t('language_russian'))
        
        self.console.print(f"\n[bold cyan]{self.loc.t('settings_interface')}[/bold cyan]")
        self.console.print(f"{self.loc.t('current_value')}: [yellow]{current_lang}[/yellow]")
        self.console.print(f"\n1. {self.loc.t('language_russian')}")
        self.console.print(f"2. {self.loc.t('language_english')}")
        
        choice = Prompt.ask(f"\n{self.loc.t('choose_option')}", choices=["1", "2"], default="1")
        
        new_lang = self.loc.t('language_russian') if choice == "1" else self.loc.t('language_english')
        self.settings.set("interface_language", new_lang)
        self.loc.set_language(new_lang)
        
        current_dev_mode = self.settings.get("developer_mode", False)
        self.console.print(f"\n{self.loc.t('developer_mode')}: [yellow]{'✓' if current_dev_mode else '✗'}[/yellow]")
        self.console.print(f"{self.loc.t('developer_mode_info')}")
        
        dev_mode = Confirm.ask(f"{self.loc.t('developer_mode')}", default=current_dev_mode)
        self.settings.set("developer_mode", dev_mode)
        
        if dev_mode:
            self.console.print(f"\n[bold green]{self.loc.t('dev_mode_enabled')}[/bold green]")
        else:
            self.console.print(f"\n[bold green]{self.loc.t('dev_mode_disabled')}[/bold green]")
        
        self.console.print(f"\n[bold green]✓ {self.loc.t('settings_saved')}[/bold green]")
    
    def show_presentation_settings(self):
        current_size = self.settings.get("slide_size", "16:9")
        
        self.console.print(f"\n[bold cyan]{self.loc.t('settings_presentation')}[/bold cyan]")
        self.console.print(f"{self.loc.t('current_value')}: [yellow]{current_size}[/yellow]")
        self.console.print("\n1. 16:9 (HD)")
        self.console.print("2. 4:3 (Standard)")
        
        choice = Prompt.ask(f"\n{self.loc.t('choose_option')}", choices=["1", "2"], default="1")
        
        new_size = "16:9" if choice == "1" else "4:3"
        self.settings.set("slide_size", new_size)
        
        current_auto_open = self.settings.get("auto_open_presentation", True)
        self.console.print(f"\n{self.loc.t('auto_open')}: [yellow]{'✓' if current_auto_open else '✗'}[/yellow]")
        
        auto_open = Confirm.ask(f"{self.loc.t('auto_open')}?", default=current_auto_open)
        self.settings.set("auto_open_presentation", auto_open)
        
        self.console.print(f"\n[bold green]✓ {self.loc.t('settings_saved')}[/bold green]")
    
    def show_ai_settings(self):
        current_model = self.settings.get("ai_model", "deepseek-ai/DeepSeek-R1-0528")
        
        self.console.print(f"\n[bold cyan]{self.loc.t('settings_ai')}[/bold cyan]")
        self.console.print(f"{self.loc.t('current_value')}: [yellow]{current_model}[/yellow]\n")
        
        table = Table(show_header=True, box=box.ROUNDED)
        table.add_column("№", style="cyan", width=4)
        table.add_column(self.loc.t('ai_model'), style="white", width=50)
        
        for key in sorted(self.ai_models.keys(), key=lambda x: int(x)):
            model_id, model_name = self.ai_models[key]
            marker = "✓" if model_id == current_model else " "
            table.add_row(key, f"{marker} {model_name}")
        
        self.console.print(table)
        
        try:
            choice = Prompt.ask(f"\n{self.loc.t('choose_option')} (1-17)", default="1")
            
            if choice in self.ai_models:
                model_id, model_name = self.ai_models[choice]
                self.settings.set("ai_model", model_id)
                self.console.print(f"\n[bold green]✓ {self.loc.t('settings_saved')}: {model_name}[/bold green]")
            else:
                self.console.print(f"\n[bold red]{self.loc.t('invalid_choice')}[/bold red]")
        except:
            self.console.print(f"\n[bold red]{self.loc.t('invalid_input')}[/bold red]")
    
    def show_search_settings(self):
        current_engine = self.settings.get("search_engine", "DuckDuckGo")
        current_results = self.settings.get("search_results_count", 5)
        current_region = self.settings.get("search_region", "ru-ru")
        
        self.console.print(f"\n[bold cyan]{self.loc.t('settings_search')}[/bold cyan]")
        
        self.console.print(f"\n{self.loc.t('search_engine')}: [yellow]{current_engine}[/yellow]")
        
        self.console.print(f"\n{self.loc.t('search_results')}: [yellow]{current_results}[/yellow]")
        results_count = IntPrompt.ask(
            f"{self.loc.t('search_results')} (3-6)",
            default=current_results,
            show_default=True
        )
        if 3 <= results_count <= 6:
            self.settings.set("search_results_count", results_count)
        
        region_map = {
            "1": ("ru-ru", self.loc.t("russia")),
            "2": ("us-en", self.loc.t("usa")),
            "3": ("wt-wt", self.loc.t("global"))
        }
        
        current_region_name = next((name for code, name in region_map.values() if code == current_region), self.loc.t("russia"))
        
        self.console.print(f"\n{self.loc.t('search_region')}: [yellow]{current_region_name}[/yellow]")
        self.console.print("1. " + self.loc.t("russia"))
        self.console.print("2. " + self.loc.t("usa"))
        self.console.print("3. " + self.loc.t("global"))
        
        region_choice = Prompt.ask(f"\n{self.loc.t('choose_option')}", choices=["1", "2", "3"], default="1")
        
        new_region_code, new_region_name = region_map[region_choice]
        self.settings.set("search_region", new_region_code)
        
        self.console.print(f"\n[bold green]✓ {self.loc.t('settings_saved')}[/bold green]")
    
    def show_clear_database(self):
        self.console.print(f"\n[bold cyan]{self.loc.t('clear_database')}[/bold cyan]")
        
        menu_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        menu_table.add_column(self.loc.t("option_column"), style="bold red", width=3)
        menu_table.add_column(self.loc.t("description_column"), style="white")
        
        menu_table.add_row("1", f"● {self.loc.t('clear_settings_db')}")
        menu_table.add_row("2", f"● {self.loc.t('clear_presentations_db')}")
        menu_table.add_row("3", f"● {self.loc.t('clear_all_databases')}")
        menu_table.add_row("4", f"{self.loc.t('back_to_main')}")
        
        menu_panel = Panel(
            menu_table,
            title=f"[bold red]{self.loc.t('clear_database')}[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        self.console.print(menu_panel)
        
        choice = Prompt.ask(f"\n{self.loc.t('choose_option')}", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            self._clear_settings_database()
        elif choice == "2":
            self._clear_presentations_database()
        elif choice == "3":
            self._clear_all_databases()
        elif choice == "4":
            return
    
    def _clear_settings_database(self):
        if Confirm.ask(f"\n{self.loc.t('confirm_clear_settings')}"):
            try:
                import os
                import time
                import psutil
                
                settings_db_path = "config/settings.db"
                if os.path.exists(settings_db_path):
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            for file in proc.open_files():
                                if settings_db_path in file.path:
                                    proc.terminate()
                                    time.sleep(0.5)
                        except:
                            pass
                    
                    time.sleep(1)
                    os.remove(settings_db_path)
                    self.console.print(f"\n[bold green]{self.loc.t('database_cleared')}[/bold green]")
                    self.console.print(f"\n[bold blue]⟳ {self.loc.t('restarting_program')}[/bold blue]")
                    time.sleep(2)
                    os._exit(0)
                else:
                    self.console.print(f"\n[yellow]{self.loc.t('settings_db_not_found')}[/yellow]")
            except Exception as e:
                self.console.print(f"\n[bold red]{self.loc.t('clear_error')}: {e}[/bold red]")
    
    def _clear_presentations_database(self):
        if Confirm.ask(f"\n{self.loc.t('confirm_clear_presentations')}"):
            try:
                import os
                import time
                
                presentations_db_path = "presentation_generator/config/presentations.db"
                if os.path.exists(presentations_db_path):
                    os.remove(presentations_db_path)
                    self.console.print(f"\n[bold green]{self.loc.t('database_cleared')}[/bold green]")
                    self.console.print(f"\n[bold blue]⟳ {self.loc.t('restarting_program')}[/bold blue]")
                    time.sleep(2)
                    import subprocess
                    import sys
                    subprocess.Popen([sys.executable, "run.py"])
                    os._exit(0)
                else:
                    self.console.print(f"\n[yellow]{self.loc.t('presentations_db_not_found')}[/yellow]")
            except Exception as e:
                self.console.print(f"\n[bold red]{self.loc.t('clear_error')}: {e}[/bold red]")
    
    def _clear_all_databases(self):
        if Confirm.ask(f"\n{self.loc.t('confirm_clear_all')}"):
            try:
                import os
                import time
                
                settings_db_path = "config/settings.db"
                presentations_db_path = "presentation_generator/config/presentations.db"
                
                if hasattr(self, 'settings') and self.settings:
                    try:
                        self.settings.close_connection()
                    except:
                        pass
                
                import gc
                gc.collect()
                
                cleared_count = 0
                
                def force_remove_file(file_path):
                    if not os.path.exists(file_path):
                        return False
                    try:
                        os.remove(file_path)
                        return True
                    except (PermissionError, OSError):
                        try:
                            time.sleep(2)
                            os.remove(file_path)
                            return True
                        except (PermissionError, OSError):
                            return False
                
                success_settings = force_remove_file(settings_db_path)
                success_presentations = force_remove_file(presentations_db_path)
                
                if success_settings:
                    cleared_count += 1
                if success_presentations:
                    cleared_count += 1
                
                if not success_settings or not success_presentations:
                    cleanup_script = '''
import os
import time
time.sleep(3)
try:
    if os.path.exists("config/settings.db"):
        os.remove("config/settings.db")
    if os.path.exists("presentation_generator/config/presentations.db"):
        os.remove("presentation_generator/config/presentations.db")
except:
    pass
os.remove("cleanup_db.py")
'''
                    with open("cleanup_db.py", "w", encoding="utf-8") as f:
                        f.write(cleanup_script)
                
                if cleared_count > 0 or (not success_settings or not success_presentations):
                    self.console.print(f"\n[bold green]{self.loc.t('database_cleared')}[/bold green]")
                    self.console.print(f"\n[bold blue]⟳ {self.loc.t('restarting_program')}[/bold blue]")
                    time.sleep(2)
                    import subprocess
                    import sys
                    if os.path.exists("cleanup_db.py"):
                        subprocess.Popen([sys.executable, "cleanup_db.py"])
                    subprocess.Popen([sys.executable, "run.py"])
                    os._exit(0)
                else:
                    self.console.print(f"\n[yellow]{self.loc.t('databases_not_found')}[/yellow]")
            except Exception as e:
                self.console.print(f"\n[bold red]{self.loc.t('clear_error')}: {e}[/bold red]")
