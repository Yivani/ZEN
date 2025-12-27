import os
import shutil
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import List, Dict, Callable, Any

# --- CONFIGURATION MANAGER ---
class ConfigManager:
    """
    Handles loading and saving configuration to config.json.
    """
    CONFIG_FILE = "config.json"
    
    DEFAULT_CONFIG = {
        "extension_map": {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".psd", ".ai", ".eps", ".webp", ".tiff", ".ico"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".odt", ".rtf", ".csv", ".xls"],
            "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
            "Video": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".m4v"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Developer": [".py", ".js", ".json", ".html", ".css", ".java", ".cpp", ".ts", ".tsx", ".jsx", ".php", ".rb", ".go", ".rs"]
        },
        "enabled_categories": {
            "Images": True, "Documents": True, "Installers": True, 
            "Audio": True, "Video": True, "Archives": True, "Developer": True
        },
        "custom_rules": [],
        "enable_unsorted": False,
        "user_settings": {
            "default_path": os.path.join(os.path.expanduser("~"), "Downloads"),
            "log_font_size": 11,
            "auto_save": True
        }
    }

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Loads config from JSON or returns defaults if not found/invalid."""
        if not os.path.exists(ConfigManager.CONFIG_FILE):
            ConfigManager.save_config(ConfigManager.DEFAULT_CONFIG)
            return ConfigManager.DEFAULT_CONFIG.copy()
        
        try:
            with open(ConfigManager.CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Merge with defaults to ensure all keys exist (simple migration)
                config = ConfigManager.DEFAULT_CONFIG.copy()
                # Deep update for dictionaries
                for key, value in data.items():
                    if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
                return config
        except Exception:
            return ConfigManager.DEFAULT_CONFIG.copy()

    @staticmethod
    def save_config(config: Dict[str, Any]):
        """Saves current config to JSON."""
        try:
            with open(ConfigManager.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")


# --- LOGIC CLASS ---
class FileOrganizer:
    """
    Handles the core logic for file organization:
    - Scanning directories
    - Moving files based on extensions
    - Applying custom filename rules
    """
    
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.extension_map = self.config["extension_map"]
        self.enabled_categories = self.config["enabled_categories"]
        self.custom_rules = self.config["custom_rules"]
        self.enable_unsorted = self.config.get("enable_unsorted", False)

    def save_state(self):
        """Persist current state to config."""
        self.config["extension_map"] = self.extension_map
        self.config["enabled_categories"] = self.enabled_categories
        self.config["custom_rules"] = self.custom_rules
        self.config["enable_unsorted"] = self.enable_unsorted
        ConfigManager.save_config(self.config)

    def set_category_enabled(self, category: str, enabled: bool):
        """Enable or disable a specific file category."""
        if category in self.enabled_categories:
            self.enabled_categories[category] = enabled
            self.save_state()

    def set_unsorted_enabled(self, enabled: bool):
        """Enable or disable moving unsorted files."""
        self.enable_unsorted = enabled
        self.save_state()

    def add_custom_rule(self, keyword: str, target_folder: str):
        """Add a custom rule based on filename keyword."""
        if keyword and target_folder:
            self.custom_rules.append({"keyword": keyword, "target_folder": target_folder})
            self.save_state()

    def remove_custom_rule(self, index: int):
        """Remove a custom rule by index."""
        if 0 <= index < len(self.custom_rules):
            self.custom_rules.pop(index)
            self.save_state()

    def add_extension_to_category(self, category: str, extension: str):
        """Adds a new extension to a category."""
        if category in self.extension_map:
            if not extension.startswith("."):
                extension = "." + extension
            if extension.lower() not in self.extension_map[category]:
                self.extension_map[category].append(extension.lower())
                self.save_state()

    def organize_files(self, source_path: str, log_callback: Callable[[str], None]):
        """
        Main function to organize files in the source_path.
        """
        if not os.path.exists(source_path):
            log_callback(f"ERROR: PATH NOT FOUND: {source_path}")
            return

        files_moved = 0
        
        try:
            for filename in os.listdir(source_path):
                file_path = os.path.join(source_path, filename)

                if os.path.isdir(file_path):
                    continue

                target_folder_name = None

                # 1. Check Custom Rules
                for rule in self.custom_rules:
                    if rule["keyword"].lower() in filename.lower():
                        target_folder_name = rule["target_folder"]
                        break
                
                # 2. Check Extension Rules
                if not target_folder_name:
                    name, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    
                    for category, extensions in self.extension_map.items():
                        if self.enabled_categories.get(category, False) and ext in extensions:
                            target_folder_name = category
                            break
                
                # 3. Check Unsorted Fallback
                if not target_folder_name and self.enable_unsorted:
                    target_folder_name = "Unsorted"

                # 4. Move file
                if target_folder_name:
                    target_dir = os.path.join(source_path, target_folder_name)
                    
                    try:
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                        
                        destination = os.path.join(target_dir, filename)
                        if os.path.exists(destination):
                            base, extension = os.path.splitext(filename)
                            counter = 1
                            while os.path.exists(os.path.join(target_dir, f"{base}_{counter}{extension}")):
                                counter += 1
                            destination = os.path.join(target_dir, f"{base}_{counter}{extension}")

                        shutil.move(file_path, destination)
                        log_callback(f"MOVED: {filename} >> {target_folder_name}")
                        files_moved += 1
                    except Exception as e:
                        log_callback(f"ERROR: {filename}: {str(e)}")

            if files_moved == 0:
                log_callback("NO MATCHING FILES FOUND.")
            else:
                log_callback(f"SUCCESS! {files_moved} FILES ORGANIZED.")
                
        except Exception as e:
            log_callback(f"SYSTEM ERROR: {str(e)}")


# --- DESIGN CONFIGURATION (The "Lumen" Style) ---
COL_BG_MAIN      = "#121212"
COL_BG_PANEL     = "#1E1E1E"
COL_ACCENT       = "#00E676"
COL_ACCENT_HOVER = "#00C853"
COL_ACCENT_SEC   = "#FF4081"
COL_TEXT_WHITE   = "#ECEFF1"
COL_TEXT_GRAY    = "#B0BEC5"
COL_INPUT_BG     = "#263238"
COL_BORDER       = "#37474F"


class CustomMessagePopup(ctk.CTkToplevel):
    """
    Custom message popup to replace messagebox.
    """
    def __init__(self, parent, title: str, message: str, msg_type: str = "info"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.configure(fg_color=COL_BG_MAIN)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass
        
        # Determine colors based on type
        if msg_type == "error":
            accent_color = COL_ACCENT_SEC
            icon_text = "✗"
        elif msg_type == "warning":
            accent_color = "#FFA726"
            icon_text = "⚠"
        else:  # info/success
            accent_color = COL_ACCENT
            icon_text = "✓"
        
        # Header
        header = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, height=50)
        header.pack(fill="x", padx=0, pady=0)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            title_frame, 
            text=icon_text, 
            font=("Arial", 24), 
            text_color=accent_color
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame, 
            text=title.upper(), 
            font=("Impact", 16), 
            text_color=COL_TEXT_WHITE
        ).pack(side="left")
        
        # Message
        msg_frame = ctk.CTkFrame(self, fg_color="transparent")
        msg_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            msg_frame,
            text=message,
            font=("Arial", 12),
            text_color=COL_TEXT_GRAY,
            wraplength=350,
            justify="left"
        ).pack(anchor="w", pady=10)
        
        # Button
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="[ OK ]",
            fg_color=accent_color,
            hover_color=COL_ACCENT_HOVER if msg_type != "error" else "#B00020",
            text_color=COL_BG_MAIN,
            command=self.destroy,
            width=100
        ).pack(side="right")
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class SettingsPopup(ctk.CTkToplevel):
    """
    Modal window to edit category extensions.
    """
    def __init__(self, parent, organizer: FileOrganizer):
        super().__init__(parent)
        self.organizer = organizer
        self.title("SYSTEM CONFIGURATION")
        self.geometry("400x350")
        self.configure(fg_color=COL_BG_MAIN)
        self.attributes("-topmost", True)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header
        ctk.CTkLabel(self, text="EDIT EXTENSIONS", font=("Impact", 18), text_color=COL_TEXT_WHITE).pack(pady=15)

        # Category Selection
        self.cat_var = ctk.StringVar(value=list(organizer.extension_map.keys())[0])
        self.cat_dropdown = ctk.CTkOptionMenu(
            self, 
            values=list(organizer.extension_map.keys()), 
            variable=self.cat_var,
            fg_color=COL_INPUT_BG,
            button_color=COL_ACCENT,
            button_hover_color=COL_ACCENT_HOVER,
            text_color=COL_TEXT_WHITE,
            command=self.update_extensions_view
        )
        self.cat_dropdown.pack(fill="x", padx=20, pady=(0, 10))

        # Add Extension Input
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=5)
        
        self.ext_entry = ctk.CTkEntry(input_frame, placeholder_text=".ext", width=100, fg_color=COL_INPUT_BG, border_width=1, border_color=COL_BORDER, text_color=COL_TEXT_WHITE)
        self.ext_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_add = ctk.CTkButton(input_frame, text="+ ADD", width=60, fg_color=COL_ACCENT, hover_color=COL_ACCENT_HOVER, text_color=COL_BG_MAIN, command=self.add_extension)
        self.btn_add.pack(side="right")

        # Extensions List Display
        self.ext_textbox = ctk.CTkTextbox(self, fg_color=COL_BG_PANEL, text_color=COL_TEXT_GRAY, font=("Consolas", 12))
        self.ext_textbox.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.update_extensions_view()

    def update_extensions_view(self, _=None):
        cat = self.cat_var.get()
        exts = self.organizer.extension_map.get(cat, [])
        self.ext_textbox.configure(state="normal")
        self.ext_textbox.delete("0.0", "end")
        self.ext_textbox.insert("0.0", ", ".join(exts))
        self.ext_textbox.configure(state="disabled")

    def add_extension(self):
        cat = self.cat_var.get()
        ext = self.ext_entry.get().strip()
        if ext:
            self.organizer.add_extension_to_category(cat, ext)
            self.ext_entry.delete(0, "end")
            self.update_extensions_view()


class UserSettingsPopup(ctk.CTkToplevel):
    """
    User settings window for preferences.
    """
    def __init__(self, parent, organizer: FileOrganizer):
        super().__init__(parent)
        self.organizer = organizer
        self.parent_app = parent
        self.title("USER SETTINGS")
        self.geometry("500x600")
        self.configure(fg_color=COL_BG_MAIN)
        self.attributes("-topmost", True)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass
        
        # Get current user settings
        user_settings = self.organizer.config.get("user_settings", ConfigManager.DEFAULT_CONFIG["user_settings"])
        
        # Header
        header = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, height=60)
        header.pack(fill="x", padx=0, pady=0)
        ctk.CTkLabel(header, text="USER PREFERENCES", font=("Impact", 20), text_color=COL_ACCENT).pack(pady=15)
        
        # Scrollable content
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Default Path Setting
        path_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        path_frame.pack(fill="x", pady=10)
        path_inner = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_inner.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(path_inner, text="DEFAULT FOLDER PATH", font=("Arial", 12, "bold"), text_color=COL_TEXT_WHITE).pack(anchor="w", pady=(0, 5))
        path_input_frame = ctk.CTkFrame(path_inner, fg_color="transparent")
        path_input_frame.pack(fill="x")
        
        self.path_entry = ctk.CTkEntry(
            path_input_frame, 
            placeholder_text="Select default folder...",
            fg_color=COL_INPUT_BG,
            border_width=1,
            border_color=COL_BORDER,
            text_color=COL_TEXT_WHITE
        )
        self.path_entry.insert(0, user_settings.get("default_path", ""))
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            path_input_frame, 
            text="BROWSE", 
            width=80,
            fg_color=COL_ACCENT,
            hover_color=COL_ACCENT_HOVER,
            text_color=COL_BG_MAIN,
            command=self.browse_default_path
        ).pack(side="right")
        
        # Log Font Size
        font_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        font_frame.pack(fill="x", pady=10)
        font_inner = ctk.CTkFrame(font_frame, fg_color="transparent")
        font_inner.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(font_inner, text="LOG FONT SIZE", font=("Arial", 12, "bold"), text_color=COL_TEXT_WHITE).pack(anchor="w", pady=(0, 5))
        self.font_size_entry = ctk.CTkEntry(font_inner, width=100, fg_color=COL_INPUT_BG, border_width=1, border_color=COL_BORDER, text_color=COL_TEXT_WHITE)
        self.font_size_entry.insert(0, str(user_settings.get("log_font_size", 11)))
        self.font_size_entry.pack(anchor="w")
        
        # Auto Save
        autosave_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        autosave_frame.pack(fill="x", pady=10)
        autosave_inner = ctk.CTkFrame(autosave_frame, fg_color="transparent")
        autosave_inner.pack(fill="x", padx=15, pady=15)
        
        self.autosave_var = ctk.BooleanVar(value=user_settings.get("auto_save", True))
        ctk.CTkCheckBox(
            autosave_inner,
            text="AUTO SAVE SETTINGS",
            variable=self.autosave_var,
            font=("Arial", 11, "bold"),
            text_color=COL_TEXT_WHITE,
            fg_color=COL_ACCENT,
            checkmark_color=COL_BG_MAIN,
            hover_color=COL_ACCENT_HOVER
        ).pack(anchor="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="[ CANCEL ]",
            fg_color="transparent",
            border_width=1,
            border_color=COL_BORDER,
            text_color=COL_TEXT_GRAY,
            hover_color=COL_BG_PANEL,
            command=self.destroy
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="[ SAVE & APPLY ]",
            fg_color=COL_ACCENT,
            hover_color=COL_ACCENT_HOVER,
            text_color=COL_BG_MAIN,
            command=self.save_and_apply
        ).pack(side="right")
    
    def browse_default_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)
    
    def save_and_apply(self):
        """Save settings and apply changes."""
        try:
            user_settings = {
                "default_path": self.path_entry.get().strip(),
                "log_font_size": int(self.font_size_entry.get()),
                "auto_save": self.autosave_var.get()
            }
            
            # Validate inputs
            if not os.path.exists(user_settings["default_path"]):
                CustomMessagePopup(self, "Error", "Default path does not exist!", "error")
                return
            
            if user_settings["log_font_size"] < 8 or user_settings["log_font_size"] > 20:
                CustomMessagePopup(self, "Error", "Font size must be between 8 and 20!", "error")
                return
            
            # Save to config
            self.organizer.config["user_settings"] = user_settings
            ConfigManager.save_config(self.organizer.config)
            
            # Apply font size to log box
            self.parent_app.log_box.configure(font=("Consolas", user_settings["log_font_size"]))
            
            # Update default path in entry if it's still the old default
            if self.parent_app.path_entry.get() == os.path.join(os.path.expanduser("~"), "Downloads"):
                self.parent_app.path_entry.delete(0, "end")
                self.parent_app.path_entry.insert(0, user_settings["default_path"])
            
            CustomMessagePopup(self, "Success", "Settings saved and applied!", "info")
            self.destroy()
            
        except ValueError:
            CustomMessagePopup(self, "Error", "Invalid numeric values!", "error")
        except Exception as e:
            CustomMessagePopup(self, "Error", f"Failed to save settings: {str(e)}", "error")


class ZenCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Logic Handler
        self.organizer = FileOrganizer()
        
        # Window Setup
        self.title("ZEN // CLEANER")
        self.geometry("1100x850")
        self.configure(fg_color=COL_BG_MAIN)
        
        # Set window icon (for window title bar and taskbar)
        icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass  # Icon loading failed, continue without icon

        # UI Layout
        self._create_ui()
        
        # Ensure icon is set after window is fully created (for Windows taskbar)
        if os.path.exists(icon_path):
            self.after_idle(lambda: self._set_icon(icon_path))

    def _set_icon(self, icon_path):
        """Set window icon for taskbar (called after window is created)."""
        try:
            # Set icon for window and taskbar
            self.iconbitmap(icon_path)
            # Force update for Windows taskbar
            if hasattr(self, 'wm_iconbitmap'):
                self.wm_iconbitmap(icon_path)
        except Exception:
            pass

    def _create_section_header(self, parent, text, icon_color=COL_ACCENT, right_widget=None):
        """
        Creates a LUMEN-style header with a colored vertical bar.
        Optionally accepts a widget to place on the right side.
        """
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", pady=(0, 10))
        
        # Colored bar
        bar = ctk.CTkFrame(container, width=4, height=20, corner_radius=0, fg_color=icon_color)
        bar.pack(side="left", padx=(0, 10))
        
        # Header text
        label = ctk.CTkLabel(container, text=text.upper(), font=("Impact", 18), text_color=COL_TEXT_WHITE)
        label.pack(side="left")
        
        if right_widget:
            right_widget.pack(side="right", in_=container)
        
        # Thin line below
        line = ctk.CTkFrame(parent, height=1, fg_color=COL_BORDER)
        line.pack(fill="x", pady=(0, 15))

    def _create_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER AREA ---
        self.header_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, corner_radius=0, height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        title_lbl = ctk.CTkLabel(self.header_frame, text="ZEN // CLEANER", font=("Impact", 28), text_color=COL_ACCENT)
        title_lbl.pack(side="left", padx=30, pady=20)

        path_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        path_container.pack(side="right", padx=30, fill="x", expand=True)

        # Load default path from user settings
        user_settings = self.organizer.config.get("user_settings", ConfigManager.DEFAULT_CONFIG["user_settings"])
        default_path = user_settings.get("default_path", os.path.join(os.path.expanduser("~"), "Downloads"))
        
        self.path_entry = ctk.CTkEntry(
            path_container, 
            placeholder_text="SELECT TARGET FOLDER",
            font=("Consolas", 12),
            fg_color=COL_INPUT_BG, 
            border_color=COL_BORDER, 
            text_color=COL_TEXT_GRAY
        )
        self.path_entry.insert(0, default_path)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))

        self.btn_browse = ctk.CTkButton(
            path_container, 
            text="[ BROWSE ]", 
            command=self.browse_folder, 
            width=100,
            fg_color="transparent", 
            border_width=1, 
            border_color=COL_ACCENT, 
            text_color=COL_ACCENT,
            hover_color=COL_BG_MAIN
        )
        self.btn_browse.pack(side="right")
        
        # Settings button
        self.btn_user_settings = ctk.CTkButton(
            path_container,
            text="[ SETTINGS ]",
            command=self.open_user_settings,
            width=100,
            fg_color="transparent",
            border_width=1,
            border_color=COL_ACCENT_SEC,
            text_color=COL_ACCENT_SEC,
            hover_color=COL_BG_MAIN
        )
        self.btn_user_settings.pack(side="right", padx=(0, 10))

        # --- MAIN CONTENT AREA ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Create main view and settings view containers
        self.main_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.main_view.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_columnconfigure(1, weight=2)
        self.main_view.grid_rowconfigure(0, weight=1)

        self.settings_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.settings_view.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.settings_view.grid_columnconfigure(0, weight=1)
        self.settings_view.grid_rowconfigure(0, weight=1)
        self.settings_view.grid_remove()  # Hide initially

        # LEFT COLUMN: CATEGORIES
        self.left_panel = ctk.CTkFrame(self.main_view, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        left_inner = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        left_inner.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Button for Edit
        btn_edit = ctk.CTkButton(
            left_inner, # temp parent, repacked in header
            text="[ EDIT ]", 
            width=60, 
            height=20, 
            fg_color="transparent", 
            border_width=1, 
            border_color=COL_TEXT_GRAY, 
            text_color=COL_TEXT_GRAY,
            font=("Arial", 9, "bold"),
            hover_color=COL_BORDER,
            command=self.open_settings
        )
        self._create_section_header(left_inner, "SYSTEM TARGETS", COL_ACCENT, right_widget=btn_edit)

        # Category Checkboxes
        self.check_vars = {}
        for cat in self.organizer.extension_map.keys():
            var = ctk.BooleanVar(value=self.organizer.enabled_categories.get(cat, True))
            self.check_vars[cat] = var
            chk = ctk.CTkCheckBox(
                left_inner, 
                text=f"MOVE {cat.upper()}", 
                variable=var,
                font=("Arial", 11, "bold"),
                text_color=COL_TEXT_GRAY,
                fg_color=COL_ACCENT,
                checkmark_color=COL_BG_MAIN,
                hover_color=COL_ACCENT_HOVER,
                command=lambda c=cat, v=var: self.organizer.set_category_enabled(c, v.get())
            )
            chk.pack(anchor="w", pady=8)

        # Unsorted Checkbox (Separator first)
        ctk.CTkFrame(left_inner, height=1, fg_color=COL_BORDER).pack(fill="x", pady=15)
        
        self.unsorted_var = ctk.BooleanVar(value=self.organizer.enable_unsorted)
        chk_unsorted = ctk.CTkCheckBox(
            left_inner,
            text="MOVE UNSORTED",
            variable=self.unsorted_var,
            font=("Arial", 11, "bold"),
            text_color=COL_TEXT_WHITE,
            fg_color=COL_ACCENT_SEC,
            checkmark_color=COL_BG_MAIN,
            hover_color=COL_ACCENT_SEC, # Pink hover
            command=lambda: self.organizer.set_unsorted_enabled(self.unsorted_var.get())
        )
        chk_unsorted.pack(anchor="w", pady=8)

        # RIGHT COLUMN: RULES & LOG
        self.right_panel = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        # -- RULES SECTION --
        self.rules_container = ctk.CTkFrame(self.right_panel, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, height=200)
        self.rules_container.pack(fill="x", pady=(0, 15))
        
        rules_inner = ctk.CTkFrame(self.rules_container, fg_color="transparent")
        rules_inner.pack(fill="both", padx=20, pady=20)

        self._create_section_header(rules_inner, "CUSTOM PROTOCOLS", COL_ACCENT_SEC)

        input_row = ctk.CTkFrame(rules_inner, fg_color="transparent")
        input_row.pack(fill="x", pady=(0, 10))

        self.entry_keyword = ctk.CTkEntry(input_row, placeholder_text="KEYWORD (e.g. Invoice, Receipt, Project)", fg_color=COL_INPUT_BG, border_width=0, text_color=COL_TEXT_WHITE)
        self.entry_keyword.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.entry_folder = ctk.CTkEntry(input_row, placeholder_text="TARGET FOLDER", fg_color=COL_INPUT_BG, border_width=0, text_color=COL_TEXT_WHITE)
        self.entry_folder.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_add_rule = ctk.CTkButton(input_row, text="+", width=40, fg_color=COL_INPUT_BG, hover_color=COL_BORDER, command=self.add_rule_ui)
        self.btn_add_rule.pack(side="left")

        self.rules_list_frame = ctk.CTkScrollableFrame(
            rules_inner, 
            height=100, 
            fg_color=COL_BG_MAIN,
            scrollbar_button_color=COL_BORDER
        )
        self.rules_list_frame.pack(fill="x")
        self.refresh_rules_list()

        # -- LOG / STATUS SECTION --
        self.log_container = ctk.CTkFrame(self.right_panel, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        self.log_container.pack(fill="both", expand=True)
        
        log_inner = ctk.CTkFrame(self.log_container, fg_color="transparent")
        log_inner.pack(fill="both", padx=20, pady=20)

        # Info note about undo
        info_frame = ctk.CTkFrame(log_inner, fg_color=COL_INPUT_BG, border_width=1, border_color=COL_BORDER)
        info_frame.pack(fill="x", pady=(0, 10))
        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            info_inner,
            text="ℹ",
            font=("Arial", 16),
            text_color=COL_ACCENT
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            info_inner,
            text="You can undo your current settings anytime by going to Settings → Revert to Defaults",
            font=("Arial", 10),
            text_color=COL_TEXT_GRAY,
            wraplength=500,
            justify="left"
        ).pack(side="left", fill="x", expand=True)

        self._create_section_header(log_inner, "SYSTEM LOG", COL_TEXT_GRAY)

        # Load font size from user settings
        user_settings = self.organizer.config.get("user_settings", ConfigManager.DEFAULT_CONFIG["user_settings"])
        log_font_size = user_settings.get("log_font_size", 11)
        
        self.log_box = ctk.CTkTextbox(
            log_inner, 
            font=("Consolas", log_font_size), 
            text_color=COL_ACCENT, 
            fg_color=COL_BG_MAIN,
            activate_scrollbars=True
        )
        self.log_box.pack(fill="both", expand=True)

        # --- FOOTER / ACTION AREA ---
        self.footer = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, height=80, corner_radius=0)
        self.footer.grid(row=2, column=0, sticky="ew")

        self.status_lbl = ctk.CTkLabel(self.footer, text="SYSTEM READY", font=("Arial", 10, "bold"), text_color=COL_ACCENT)
        self.status_lbl.pack(side="left", padx=30)

        self.btn_clean = ctk.CTkButton(
            self.footer, 
            text="[ INITIALIZE CLEANUP ]", 
            font=("Arial", 14, "bold"), 
            height=50, 
            width=250,
            fg_color=COL_ACCENT, 
            text_color=COL_BG_MAIN,
            hover_color=COL_ACCENT_HOVER,
            corner_radius=2,
            command=self.run_cleanup
        )
        self.btn_clean.pack(side="right", padx=30, pady=15)

        # Create settings view
        self._create_settings_view()

    def _create_settings_view(self):
        """Create the integrated settings view."""
        # Container (no scrollbar)
        scroll_frame = ctk.CTkFrame(self.settings_view, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Header with back button
        header_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, height=60)
        header_frame.pack(fill="x", pady=(0, 20))
        header_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(
            header_inner,
            text="[ ← BACK ]",
            command=self.show_main_view,
            width=100,
            fg_color="transparent",
            border_width=1,
            border_color=COL_ACCENT,
            text_color=COL_ACCENT,
            hover_color=COL_BG_MAIN
        ).pack(side="left")

        ctk.CTkLabel(
            header_inner,
            text="USER PREFERENCES",
            font=("Impact", 24),
            text_color=COL_ACCENT
        ).pack(side="left", padx=20)

        # Get current user settings
        user_settings = self.organizer.config.get("user_settings", ConfigManager.DEFAULT_CONFIG["user_settings"])

        # Default Path Setting
        path_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        path_frame.pack(fill="x", pady=10)
        path_inner = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_inner.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(path_inner, text="DEFAULT FOLDER PATH", font=("Arial", 14, "bold"), text_color=COL_TEXT_WHITE).pack(anchor="w", pady=(0, 10))
        path_input_frame = ctk.CTkFrame(path_inner, fg_color="transparent")
        path_input_frame.pack(fill="x")

        self.settings_path_entry = ctk.CTkEntry(
            path_input_frame,
            placeholder_text="Select default folder...",
            fg_color=COL_INPUT_BG,
            border_width=1,
            border_color=COL_BORDER,
            text_color=COL_TEXT_WHITE,
            font=("Consolas", 12)
        )
        self.settings_path_entry.insert(0, user_settings.get("default_path", ""))
        self.settings_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            path_input_frame,
            text="BROWSE",
            width=100,
            fg_color=COL_ACCENT,
            hover_color=COL_ACCENT_HOVER,
            text_color=COL_BG_MAIN,
            command=self.browse_settings_path
        ).pack(side="right")

        # Log Font Size
        font_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        font_frame.pack(fill="x", pady=10)
        font_inner = ctk.CTkFrame(font_frame, fg_color="transparent")
        font_inner.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(font_inner, text="LOG FONT SIZE", font=("Arial", 14, "bold"), text_color=COL_TEXT_WHITE).pack(anchor="w", pady=(0, 10))
        self.settings_font_size_entry = ctk.CTkEntry(
            font_inner,
            width=150,
            fg_color=COL_INPUT_BG,
            border_width=1,
            border_color=COL_BORDER,
            text_color=COL_TEXT_WHITE,
            font=("Consolas", 12)
        )
        self.settings_font_size_entry.insert(0, str(user_settings.get("log_font_size", 11)))
        self.settings_font_size_entry.pack(anchor="w")

        # Auto Save
        autosave_frame = ctk.CTkFrame(scroll_frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        autosave_frame.pack(fill="x", pady=10)
        autosave_inner = ctk.CTkFrame(autosave_frame, fg_color="transparent")
        autosave_inner.pack(fill="x", padx=20, pady=20)

        self.settings_autosave_var = ctk.BooleanVar(value=user_settings.get("auto_save", True))
        ctk.CTkCheckBox(
            autosave_inner,
            text="AUTO SAVE SETTINGS",
            variable=self.settings_autosave_var,
            font=("Arial", 12, "bold"),
            text_color=COL_TEXT_WHITE,
            fg_color=COL_ACCENT,
            checkmark_color=COL_BG_MAIN,
            hover_color=COL_ACCENT_HOVER
        ).pack(anchor="w")

        # Save and Revert Buttons
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        ctk.CTkButton(
            button_frame,
            text="[ REVERT TO DEFAULTS ]",
            fg_color="transparent",
            border_width=1,
            border_color=COL_ACCENT_SEC,
            text_color=COL_ACCENT_SEC,
            hover_color=COL_BG_PANEL,
            font=("Arial", 12, "bold"),
            height=50,
            width=200,
            command=self.revert_settings
        ).pack(side="left")

        ctk.CTkButton(
            button_frame,
            text="[ SAVE & APPLY ]",
            fg_color=COL_ACCENT,
            hover_color=COL_ACCENT_HOVER,
            text_color=COL_BG_MAIN,
            font=("Arial", 14, "bold"),
            height=50,
            command=self.save_settings
        ).pack(side="right")

    def browse_settings_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.settings_path_entry.delete(0, "end")
            self.settings_path_entry.insert(0, folder)

    def show_main_view(self):
        """Switch to main view."""
        self.settings_view.grid_remove()
        self.main_view.grid()

    def show_settings_view(self):
        """Switch to settings view."""
        self.main_view.grid_remove()
        self.settings_view.grid()
        # Refresh settings values
        user_settings = self.organizer.config.get("user_settings", ConfigManager.DEFAULT_CONFIG["user_settings"])
        self.settings_path_entry.delete(0, "end")
        self.settings_path_entry.insert(0, user_settings.get("default_path", ""))
        self.settings_font_size_entry.delete(0, "end")
        self.settings_font_size_entry.insert(0, str(user_settings.get("log_font_size", 11)))
        self.settings_autosave_var.set(user_settings.get("auto_save", True))

    def revert_settings(self):
        """Revert all settings to default values."""
        default_settings = ConfigManager.DEFAULT_CONFIG["user_settings"]
        
        # Update UI fields
        self.settings_path_entry.delete(0, "end")
        self.settings_path_entry.insert(0, default_settings["default_path"])
        
        self.settings_font_size_entry.delete(0, "end")
        self.settings_font_size_entry.insert(0, str(default_settings["log_font_size"]))
        
        self.settings_autosave_var.set(default_settings["auto_save"])
        
        # Save to config
        self.organizer.config["user_settings"] = default_settings.copy()
        ConfigManager.save_config(self.organizer.config)
        
        # Apply changes immediately
        self.log_box.configure(font=("Consolas", default_settings["log_font_size"]))
        
        # Update main path entry if needed
        if self.path_entry.get() != default_settings["default_path"]:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, default_settings["default_path"])
        
        CustomMessagePopup(self, "Success", "Settings reverted to defaults and applied!", "info")

    def save_settings(self):
        """Save settings and apply changes."""
        try:
            user_settings = {
                "default_path": self.settings_path_entry.get().strip(),
                "log_font_size": int(self.settings_font_size_entry.get()),
                "auto_save": self.settings_autosave_var.get()
            }

            # Validate inputs
            if not os.path.exists(user_settings["default_path"]):
                CustomMessagePopup(self, "Error", "Default path does not exist!", "error")
                return

            if user_settings["log_font_size"] < 8 or user_settings["log_font_size"] > 20:
                CustomMessagePopup(self, "Error", "Font size must be between 8 and 20!", "error")
                return

            # Save to config
            self.organizer.config["user_settings"] = user_settings
            ConfigManager.save_config(self.organizer.config)

            # Apply font size to log box
            self.log_box.configure(font=("Consolas", user_settings["log_font_size"]))

            # Update default path in entry if it's still the old default
            if self.path_entry.get() == os.path.join(os.path.expanduser("~"), "Downloads"):
                self.path_entry.delete(0, "end")
                self.path_entry.insert(0, user_settings["default_path"])

            CustomMessagePopup(self, "Success", "Settings saved and applied!", "info")
            self.show_main_view()

        except ValueError:
            CustomMessagePopup(self, "Error", "Invalid numeric values!", "error")
        except Exception as e:
            CustomMessagePopup(self, "Error", f"Failed to save settings: {str(e)}", "error")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_selected)

    def open_settings(self):
        SettingsPopup(self, self.organizer)
    
    def open_user_settings(self):
        self.show_settings_view()

    def add_rule_ui(self):
        keyword = self.entry_keyword.get().strip()
        folder = self.entry_folder.get().strip()
        if keyword and folder:
            self.organizer.add_custom_rule(keyword, folder)
            self.entry_keyword.delete(0, "end")
            self.entry_folder.delete(0, "end")
            self.refresh_rules_list()

    def refresh_rules_list(self):
        for widget in self.rules_list_frame.winfo_children(): widget.destroy()
        for idx, rule in enumerate(self.organizer.custom_rules):
            row = ctk.CTkFrame(self.rules_list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"📂 IF '{rule['keyword']}' >> {rule['target_folder']}", text_color=COL_TEXT_GRAY, font=("Consolas", 11)).pack(side="left")
            ctk.CTkButton(row, text="DEL", width=30, height=20, fg_color=COL_ACCENT_SEC, hover_color="#B00020", font=("Arial", 8), command=lambda i=idx: self.delete_rule(i)).pack(side="right")

    def delete_rule(self, index):
        self.organizer.remove_custom_rule(index)
        self.refresh_rules_list()

    def log(self, message: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f">> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def run_cleanup(self):
        path = self.path_entry.get()
        if not path:
            self.log("ERROR: NO PATH SELECTED")
            return
        self.status_lbl.configure(text="PROCESSING...", text_color=COL_ACCENT_SEC)
        self.log("--- SEQUENCE STARTED ---")
        self.organizer.organize_files(path, self.log)
        self.log("--- SEQUENCE COMPLETE ---")
        self.status_lbl.configure(text="SYSTEM READY", text_color=COL_ACCENT)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = ZenCleanerApp()
    app.mainloop()
