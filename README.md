# ZEN // CLEANER

## // SYSTEM OVERVIEW

**ZEN CLEANER** is an advanced desktop organization tool designed for automated file management and directory cleanup. It provides intelligent file sorting capabilities, custom rule protocols, and real-time system monitoring for efficient workspace organization.

This software operates locally on your system, automatically organizing files based on extension mapping, custom keyword rules, and user-defined preferences without requiring network connectivity.

> **OPEN SOURCE:** This application is fully open source. You can use the pre-built `ZEN.exe` executable for convenience, or run the Python source code (`ZEN.py`) directly if you prefer to inspect or modify the code.

---

## // SECURITY & ANTIVIRUS NOTE

> **FALSE POSITIVE WARNING:** Security scans may flag `ZEN.exe` as potentially malicious.

**This is a known false positive caused by PyInstaller packaging.**
VirusTotal analysis shows **5/72 security vendors** flagging the executable, which is typical for PyInstaller-compiled applications without code signing certificates.

**Verification & Safety:**
* **FULL SOURCE CODE AVAILABLE:** The complete source code (`ZEN.py`) is available in this repository for inspection
* **NO NETWORK ACTIVITY:** This tool operates entirely locally and makes zero network connections
* **OPEN SOURCE:** You can review, modify, and compile the code yourself if you prefer
* **ACTION REQUIRED:** If your antivirus blocks the file, add an **Exclusion/Exception** for `ZEN.exe` or the application directory

**Note:** 67/72 security vendors report the file as clean/undetected. The flagged detections are generic heuristics, not specific malware signatures.

---

## // OPERATIONAL CAPABILITIES

### AUTOMATED FILE ORGANIZATION
* **EXTENSION-BASED SORTING:** Automatically categorizes files by type (Images, Documents, Audio, Video, Archives, Developer files, Installers)
* **CUSTOM KEYWORD RULES:** Create custom protocols that move files containing specific keywords to designated folders
* **PRIORITY SYSTEM:** Custom rules take precedence over extension-based sorting
* **DUPLICATE HANDLING:** Automatic filename conflict resolution with incremental numbering

### CATEGORY MANAGEMENT
Flexible category system with enable/disable toggles for each file type:
* **IMAGES:** JPG, PNG, GIF, BMP, SVG, PSD, AI, EPS, WebP, TIFF, ICO
* **DOCUMENTS:** PDF, DOCX, DOC, TXT, XLSX, PPTX, ODT, RTF, CSV, XLS
* **INSTALLERS:** EXE, MSI, DMG, PKG, DEB, RPM
* **AUDIO:** MP3, WAV, FLAC, AAC, OGG, M4A, WMA
* **VIDEO:** MP4, MOV, AVI, MKV, FLV, WMV, WebM, M4V
* **ARCHIVES:** ZIP, RAR, 7Z, TAR, GZ, BZ2, XZ
* **DEVELOPER:** PY, JS, JSON, HTML, CSS, Java, C++, TS, TSX, JSX, PHP, Ruby, Go, Rust

### CUSTOM PROTOCOLS
* **KEYWORD MATCHING:** Files containing specified keywords are moved to custom folders
* **CASE-INSENSITIVE:** Rules work regardless of filename capitalization
* **MULTIPLE RULES:** Create unlimited custom rules for different file patterns

### EXTENSION CONFIGURATION
Add new file extensions to existing categories via the extension editor.

### USER PREFERENCES
* **DEFAULT FOLDER PATH:** Set default target directory for file operations
* **AUTO-SAVE:** Automatic configuration persistence
* **REVERT TO DEFAULTS:** One-click restoration of all settings to factory defaults

---

## // DEPLOYMENT INSTRUCTIONS

### **EXECUTABLE LAUNCH (RECOMMENDED)**
1. Download the latest **`ZEN.exe`** release (if available)
2. Run **`ZEN.exe`** - no Python installation required
3. The application will start immediately

### **PYTHON SCRIPT LAUNCH (OPEN SOURCE)**
The full source code is available in `ZEN.py` for inspection and modification.

1. Ensure Python 3.7+ is installed on your system
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python ZEN.py
   ```

### **BUILDING YOUR OWN EXECUTABLE**
**Quick Build (Windows):**
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `build_exe.bat`
3. Find `ZEN.exe` in the `dist` folder


### **USAGE WORKFLOW**
1. Select target folder to organize
2. Configure categories (enable/disable file types)
3. Add custom rules (optional) for keyword-based sorting
4. Initialize cleanup to start the organization process
5. Monitor progress in the system log

---

## // TROUBLESHOOTING

| ERROR MESSAGE | CAUSE | SOLUTION |
| :--- | :--- | :--- |
| **"ERROR: PATH NOT FOUND"** | The selected directory does not exist | Verify the path is correct and the directory exists |
| **"ERROR: NO PATH SELECTED"** | No target folder has been specified | Enter a valid folder path |
| **"NO MATCHING FILES FOUND"** | No files match the enabled categories or rules | Check that categories are enabled and verify file extensions match configured types |
| **"SYSTEM ERROR"** | An unexpected error occurred | Check file permissions, ensure files aren't locked by other applications, and verify disk space |

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
* Files are moved (not copied) to preserve disk space
* Automatic filename conflict resolution
* Target folders are created automatically if they don't exist
* Comprehensive error catching and logging

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
✅ **No Network Required** - Fully local operation
