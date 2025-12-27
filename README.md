# ZEN // CLEANER

![ZEN CLEANER INTERFACE](https://i.imgur.com/placeholder.png)

## // SYSTEM OVERVIEW

**ZEN CLEANER** is an advanced desktop organization tool designed for automated file management and directory cleanup. It provides users with intelligent file sorting capabilities, custom rule protocols, and real-time system monitoring for efficient workspace organization.

This software operates locally on your system, automatically organizing files based on extension mapping, custom keyword rules, and user-defined preferences without requiring network connectivity.

> **OPEN SOURCE:** This application is fully open source. You can use the pre-built `ZEN.exe` executable for convenience, or run the Python source code (`ZEN.py`) directly if you prefer to inspect or modify the code.

---

## // SECURITY & ANTIVIRUS NOTE

> **FALSE POSITIVE WARNING:** Some antivirus software may flag `ZEN.exe` or `ZEN.py` as generic malware.

**This is a known false positive caused by PyInstaller (if compiled) or Python script heuristics.**
Because this tool operates on local file systems and performs file operations, some security engines may misidentify it.

* **VERIFICATION:** The full source code is available in this repository (`ZEN.py`) for inspection.
* **ACTION:** If your antivirus blocks the file, please add an **Exclusion/Exception** for the application directory.
* **SAFETY:** This tool operates entirely locally and makes no network connections. All file operations are performed on your local machine.

---

## // OPERATIONAL CAPABILITIES

### [ 1 ] AUTOMATED FILE ORGANIZATION
Intelligent file sorting based on extension mapping and custom protocols.
* **EXTENSION-BASED SORTING:** Automatically categorizes files by type (Images, Documents, Audio, Video, Archives, Developer files, Installers).
* **CUSTOM KEYWORD RULES:** Create custom protocols that move files containing specific keywords to designated folders.
* **PRIORITY SYSTEM:** Custom rules take precedence over extension-based sorting for precise control.
* **DUPLICATE HANDLING:** Automatic filename conflict resolution with incremental numbering.

### [ 2 ] CATEGORY MANAGEMENT
Flexible category system with enable/disable toggles for each file type.
* **IMAGES:** JPG, PNG, GIF, BMP, SVG, PSD, AI, EPS, WebP, TIFF, ICO
* **DOCUMENTS:** PDF, DOCX, DOC, TXT, XLSX, PPTX, ODT, RTF, CSV, XLS
* **INSTALLERS:** EXE, MSI, DMG, PKG, DEB, RPM
* **AUDIO:** MP3, WAV, FLAC, AAC, OGG, M4A, WMA
* **VIDEO:** MP4, MOV, AVI, MKV, FLV, WMV, WebM, M4V
* **ARCHIVES:** ZIP, RAR, 7Z, TAR, GZ, BZ2, XZ
* **DEVELOPER:** PY, JS, JSON, HTML, CSS, Java, C++, TS, TSX, JSX, PHP, Ruby, Go, Rust

### [ 3 ] CUSTOM PROTOCOLS
Advanced rule-based file organization system.
* **KEYWORD MATCHING:** Files containing specified keywords are moved to custom folders.
* **CASE-INSENSITIVE:** Rules work regardless of filename capitalization.
* **MULTIPLE RULES:** Create unlimited custom rules for different file patterns.
* **RULE MANAGEMENT:** Add, view, and delete custom rules with intuitive interface.

### [ 4 ] UNSORTED FILE HANDLING
Optional fallback system for files that don't match any rules.
* **UNSORTED FOLDER:** Enable automatic moving of unmatched files to "Unsorted" folder.
* **TOGGLE CONTROL:** Enable or disable unsorted file handling as needed.

### [ 5 ] EXTENSION CONFIGURATION
Customize file type associations for each category.
* **EXTENSION EDITOR:** Add new file extensions to existing categories via Settings.
* **CATEGORY SELECTOR:** Choose which category to modify from dropdown menu.
* **REAL-TIME UPDATES:** Changes are saved immediately to configuration.

### [ 6 ] USER PREFERENCES
Comprehensive settings management system.
* **DEFAULT FOLDER PATH:** Set default target directory for file operations.
* **LOG FONT SIZE:** Adjust system log display font size (8-20px).
* **AUTO-SAVE:** Automatic configuration persistence.
* **REVERT TO DEFAULTS:** One-click restoration of all settings to factory defaults.

### [ 7 ] SYSTEM LOG
Real-time operation monitoring and feedback.
* **LIVE LOGGING:** See every file operation as it happens.
* **STATUS UPDATES:** Track moved files, errors, and completion status.
* **SCROLLABLE HISTORY:** Review past operations in scrollable log window.
* **CUSTOMIZABLE DISPLAY:** Adjustable font size for optimal readability.

---

## // VISUAL INTELLIGENCE

### **INTERFACE: ZEN ELITE UI**
Custom-engineered GUI with dark theme aesthetic featuring:
* **LUMEN-STYLE DESIGN:** Modern dark interface with accent colors
* **CLEAR VISUAL HIERARCHY:** Organized sections with distinct headers
* **REAL-TIME FEEDBACK:** Live system log with color-coded status messages
* **INTUITIVE NAVIGATION:** Seamless switching between main view and settings

---

## // DEPLOYMENT INSTRUCTIONS

### **EXECUTABLE LAUNCH (RECOMMENDED)**
1. Download the latest **`ZEN.exe`** release (if available).
2. Run **`ZEN.exe`** - no Python installation required.
3. The application will start immediately.

> **NOTE:** This application is **open source**. You can use the pre-built `.exe` file for convenience, or run the Python source code directly if you prefer.

### **PYTHON SCRIPT LAUNCH (OPEN SOURCE)**
The full source code is available in `ZEN.py` for inspection and modification.

1. Ensure Python 3.7+ is installed on your system.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python ZEN.py
   ```

### **BUILDING YOUR OWN EXECUTABLE**
See `BUILD_INSTRUCTIONS.md` for detailed instructions on creating an executable from the source code.

**Quick Build (Windows):**
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `build_exe.bat`
3. Find `ZEN.exe` in the `dist` folder

### **USAGE WORKFLOW**
1. **SELECT TARGET FOLDER:** Use the path entry or browse button to select the directory you want to organize.
2. **CONFIGURE CATEGORIES:** Enable/disable file type categories using the checkboxes in the left panel.
3. **ADD CUSTOM RULES (OPTIONAL):** Create keyword-based rules in the "CUSTOM PROTOCOLS" section.
4. **REVIEW SETTINGS:** Access Settings via the header button to configure default paths and preferences.
5. **INITIALIZE CLEANUP:** Click "[ INITIALIZE CLEANUP ]" to start the organization process.
6. **MONITOR PROGRESS:** Watch the system log for real-time operation feedback.

### **SETTINGS CONFIGURATION**
Access settings via the **[ SETTINGS ]** button in the header:
* **Default Folder Path:** Set the default target directory for file operations.
* **Log Font Size:** Adjust the system log display size (8-20px range).
* **Auto Save:** Enable automatic configuration persistence.
* **Revert to Defaults:** Restore all settings to factory defaults.

### **EXTENSION MANAGEMENT**
1. Click **[ EDIT ]** button next to "SYSTEM TARGETS" in the left panel.
2. Select a category from the dropdown menu.
3. Enter a new extension (with or without dot prefix).
4. Click **[ + ADD ]** to add the extension to the selected category.

---

## // TROUBLESHOOTING

| ERROR MESSAGE | CAUSE | SOLUTION |
| :--- | :--- | :--- |
| **"ERROR: PATH NOT FOUND"** | The selected directory does not exist. | Verify the path is correct and the directory exists. Use the browse button to select a valid folder. |
| **"ERROR: NO PATH SELECTED"** | No target folder has been specified. | Enter a valid folder path in the path entry field or use the browse button. |
| **"NO MATCHING FILES FOUND"** | No files in the directory match the enabled categories or rules. | Check that categories are enabled and verify file extensions match configured types. |
| **"SYSTEM ERROR"** | An unexpected error occurred during file operations. | Check file permissions, ensure files aren't locked by other applications, and verify disk space. |

---

## // TECHNICAL SPECIFICATIONS

### **REQUIREMENTS**
* Python 3.7 or higher
* CustomTkinter library
* Tkinter (usually included with Python)

### **CONFIGURATION FILES**
* `config.json`: Stores user preferences, category settings, and custom rules
* `logo.ico`: Application icon file

### **FILE OPERATIONS**
* **SAFE MOVING:** Files are moved (not copied) to preserve disk space
* **DUPLICATE PROTECTION:** Automatic filename conflict resolution
* **DIRECTORY CREATION:** Target folders are created automatically if they don't exist
* **ERROR HANDLING:** Comprehensive error catching and logging

---

## // DISCLAIMER

> **WARNING:** This tool moves files on your local system. While the application includes safety features, usage is at the operator's own risk. Always backup important files before running cleanup operations on critical directories.

* **DEVELOPER:** Custom Development
* **VERSION:** 1.0
* **STATUS:** ACTIVE
* **LICENSE:** Use at your own discretion

---

## // FEATURES SUMMARY

✅ **Automated File Organization** - Sort files by type automatically  
✅ **Custom Keyword Rules** - Create your own file organization protocols  
✅ **Category Management** - Enable/disable file type categories  
✅ **Extension Customization** - Add new file types to categories  
✅ **Real-Time Logging** - Monitor operations as they happen  
✅ **Settings Management** - Customize default paths and preferences  
✅ **Revert to Defaults** - Restore factory settings with one click  
✅ **Modern UI** - Dark theme interface with intuitive design  
✅ **Windows Taskbar Icon** - Proper icon display in Windows taskbar  
✅ **No Network Required** - Fully local operation

