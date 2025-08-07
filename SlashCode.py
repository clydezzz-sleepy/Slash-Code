### SlashCode

import tkinter as tk
import re
import keyword
import builtins
import os
import json
import subprocess
import tempfile
import sys
import random
import platform
import threading
import shutil
import psutil # type: ignore
from pathlib import Path
try:
    import requests # type: ignore
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests # type: ignore
    except (Exception, subprocess.CalledProcessError) as e:
        requests = None
try:
    from PIL import Image, ImageTk # type: ignore
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageTk # type: ignore
    except (Exception, subprocess.CalledProcessError) as e:
        PIL = None
from tkinter import filedialog, scrolledtext, messagebox, ttk, font
current_file = ""
FOLDER = ""
open_folder_btn = None

root = tk.Tk()

encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']

def get_tcl_tk_env():
    env = os.environ.copy()
    python_base = os.path.dirname(sys.executable)
    tcl_library = os.path.join(python_base, "tcl", "tcl8.6")
    tk_library = os.path.join(python_base, "tcl", "tk8.6")

    if os.path.isdir(tcl_library):
        env["TCL_LIBRARY"] = tcl_library
    if os.path.isdir(tk_library):
        env["TK_LIBRARY"] = tk_library
    return env
tcltk_env = get_tcl_tk_env()

GUILANGS = {
    "en": {
    "gui_lang": "GUI Language",
    "msys_install": "MSYS2 installed. Please install MinGW via MSYS2 shell: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Failed to install MinGW-w64:",
    "gcc_used": "GCC used:",
    "gcc_error_a1": "Installing G++ failed.",
    "gcc_error_a2": "Failed to check G++ version:",
    "gcc_error_b1": "G++ compiler not found. Aborting C++ run.",
    "gcc_error_b2": "Failed to install MinGW compiler.\n",
    "cpp_usercode_written": "User's C++ code written to ***.",
    "gcc_check_a1": "Checking for existing G++ compiler...",
    "gcc_check_a2": "Downloading and installing MinGW-w64...",
    "gcc_check_a3": "Downloading MinGW-w64 from ***...", # This will eventually be f"{translate.get("gcc_check_a3").replace("***", mingw_url)}".
    "gcc_check_a4": "Downloaded *** MB so far...", # The same with this one, as specified above (and also all the other ones that contain '***').
    "gcc_check_a4_5": "Downloaded *** MB in total.",
    "gcc_check_b1": "Extracting MinGW-w64 archive...",
    "gcc_check_b2": "Attempting to install/update G++ compiler...",
    "gcc_compilation_attempt": "Attempting compilation with flag ***:",
    "gcc_compilation_success": "Compilation succeeded, running executable...",
    "gcc_compilation_failed": "Compilation failed for *** with errors:",
    "gcc_execution_finished": "Execution finished successfully.",
    "gcc_execution_error_a1": "An error has occurred while attempting to run the executable:",
    "gcc_mingw_addpath": "MinGW-w64 bin folder added to PATH:",
    "gcc_compiler_installed": "G++ installed/updated successfully.",
    "gcc_found_compiler_ver": "Found G++ version:",
    "gcc_sufficient_compiler_ver": "The G++ version is sufficient.",
    "gcc_old_compiler_ver": "Your G++ version is too old and needs to be upgraded.",
    "gcc_mingw_extracted": "Extraction complete. MinGW installed at:",
    "py7zr_installed": "The py7zr package was successfully installed.",
    "py7zr_error_a1": "The package py7zr was not found, installing py7zr package...",
    "csc_compiler": "C# Compiler (csc)",
    "cs_usercode_written": "User C# code written to ***.",
    "csc_error_a1": "C# Compiler (csc) not found. Attempting to install...\n",
    "csc_error_a2": "CSC compiler not found and installation failed. Aborting C# run.",
    "csc_autoinst_fail": "Failed to auto-install C# compiler. Please install the .NET SDK manually.\n",
    "csc_compiler_installed": "C# Compiler (csc) installed successfully.\n",
    "csc_compiling_with": "Compiling with:",
    "csc_compilation_success": "Compilation succeeded.\n",
    "csc_execution_finished": "Execution finished successfully.",
    "csc_execution_error_a1": "An error has occurred while attempting to run the executable:",
    "sh_platform_not_supported": "Your platform isn't supported to run Shell Script scripts.",
    "py_error_a1_title": "Insufficient Python Version",
    "py_error_a1": "Please install Python 3.13+.",
    "py_error_a2": "Python interpreter not found.",
    "py_error_a3": "Could not parse Python version.",
    "error_a1": "Error",
    "error_a2": "Could not open file",
    "error_a3": "Could not open file:\n",
    "error_a4": "Could not write to file:\n",
    "error_a5": "Could not load the Slash Code source file. Reason:\n\n",
    "error_c0": "Folder button update error:",
    "error_c1": "Menu label update error:",
    "error_c2": "File label update error:",
    "error_c3": "Edit label update error:",
    "error_c4": "Theme label update error:",
    "error_c5": "Run label update error:",
    "error_c6": "View label update error:",
    "error_c7": "Language label update error:",
    "error_c8": "GUI language label update error:",
    "error_d1": "An exception has occurred while attempting to execute the document's code. The reason for this is:\n\n",
    "error_d1_5": "An exception has occurred while attempting to write to and execute the document. The reason for this is:\n\n",
    "error_d2": "The compiler failed to install properly.",
    "error_e1": "pip failed to install py7z. Reason:",
    "deleting_dirs": "Deleting director(y/ies): ",
    "directory_del_not_found": "No director(y/ies) was/were found to delete.",
    "find": "Find",
    "find_query": "Find:",
    "find_all": "Find All",
    "replace": "Replace",
    "replace_query": "Replace:",
    "replace_all": "Replace All",
    "runner_not_found": " not found!\n",
    "install_suggest": "Please install it first.\n",
    "instructions": "Instructions: ",
    "compilation_error": "Compilation Error:\n",
    "opened_in_browser": "Opened in default browser.",
    "language_not_supported": "Language not supported for execution.",
    "process_error": "Process Error: ",
    "unexpected_error": "Unexpected Error: ",
    "cleanup_failed": "Cleanup failed: ",
    "file": "File",
    "new": "New",
    "open": "Open",
    "save": "Save",
    "toggle_new_file_saving": "Toggle New File Saving",
    "clean_temp_files": "Clean Temporary Files",
    "clean_temp_directories": "Clean Temporary Directories",
    "fully_wipe_directories": "Fully Wipe Temporary Directories",
    "reboot_consolemode": "Reboot In Console Mode",
    "exit": "Exit",
    "edit": "Edit",
    "undo": "Undo",
    "redo": "Redo",
    "language": "Language",
    "theme": "Theme",
    "theme_light": "Light",
    "theme_dark": "Dark",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Night Owl",
    "theme_shades_of_purple": "Shades Of Purple",
    "theme_high_contrast": "High Contrast",
    "open_folder": "Open Folder",
    "changed_language_to": "Changed language to ",
    "view": "View",
    "zoom_in": "Zoom In",
    "zoom_out": "Zoom Out",
    "show_sidebar": "Show Sidebar",
    "hide_sidebar": "Hide Sidebar",
    "show_minimap": "Show Minimap",
    "hide_minimap": "Hide Minimap",
    "show_debug_info": "Show Debug Info",
    "hide_debug_info": "Hide Debug Info",
    "toggle_fullscreen": "Toggle Fullscreen",
    "exit_fullscreen": "Exit Fullscreen",
    "run": "Run",
    "run_file": "Run File",
    "sc_output": "SC-Output",
    "output_sc_title": "-- Slash Code Text Editor | SC-Output for File Execution --",
    "save_output_text": "Save Output Text",
    "highlighting_as": "Highlighting as: ",
    "plaintext": "Plain Text",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell Script",
    "python_files": "Python Files",
    "javascript_files": "JavaScript Files",
    "html_files": "HTML Files",
    "c_files": "C Files",
    "cpp_files": "C++ Files",
    "header_files": "Header Files",
    "text_files": "Text Files",
    "cs_files": "C# Files",
    "css_files": "CSS Files",
    "markdown_files": "Markdown Files",
    "renpy_files": "Ren'Py Files",
    "shell_files": "Shell Files",
    "all_files": "All Files",
    "binary_file_title": "Binary File Detected",
    "binary_file": "Unusual characters have been detected in this document, would you like to open it and have Slash Code read raw data?\nWarning, this likely will slow down Slash Code.",
    "session_loaded": "Session loaded:",
    "error_b1": "Error loading file: ",
    "error_b2": "Error loading directory: "
    },
    
    "nl": {
    "gui_lang": "GUI Taal",
    "msys_install": "MSYS2 is geinstalleerd. Installeer alstublieft MinGW via de MSYS2 shell: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Kon niet MinGW-w64 succesvol installeren:",
    "gcc_used": "GCC gebruikt:",
    "gcc_error_a1": "Installatie van G++ mislukt.",
    "gcc_error_a2": "Controleren van G++ versie mislukt:",
    "gcc_error_b1": "G++ compiler niet gevonden. C++ uitvoering geannuleerd.",
    "gcc_error_b2": "Installatie van MinGW compiler mislukt.\n",
    "cpp_usercode_written": "Gebruikers C++ code weggeschreven naar ***.",
    "gcc_check_a1": "Controleren op bestaande G++ compiler...",
    "gcc_check_a2": "MinGW-w64 wordt gedownload en geïnstalleerd...",
    "gcc_check_a3": "MinGW-w64 wordt gedownload van ***...",
    "gcc_check_a4": "Tot nu toe *** MB gedownload...",
    "gcc_check_a4_5": "In totaal *** MB gedownload.",
    "gcc_check_b1": "MinGW-w64 archief wordt uitgepakt...",
    "gcc_check_b2": "Poging tot installatie/update van G++ compiler...",
    "gcc_compilation_attempt": "Proberen te compileren met vlag ***:",
    "gcc_compilation_success": "Compilatie geslaagd, uitvoerbaar bestand wordt gestart...",
    "gcc_compilation_failed": "Compilatie mislukt voor *** met foutmeldingen:",
    "gcc_execution_finished": "Uitvoering succesvol afgerond.",
    "gcc_execution_error_a1": "Er is een fout opgetreden bij het uitvoeren van het programma:",
    "gcc_mingw_addpath": "MinGW-w64 bin map toegevoegd aan PATH:",
    "gcc_compiler_installed": "G++ succesvol geïnstalleerd/geüpdatet.",
    "gcc_found_compiler_ver": "G++ versie gevonden:",
    "gcc_sufficient_compiler_ver": "De G++ versie is voldoende.",
    "gcc_old_compiler_ver": "Je G++ versie is te oud en moet worden bijgewerkt.",
    "gcc_mingw_extracted": "Uitpakken voltooid. MinGW geïnstalleerd op:",
    "py7zr_installed": "Het py7zr pakket is succesvol geïnstalleerd.",
    "csc_compiler": "C# Compiler (csc)",
    "cs_usercode_written": "Gebruiker's C# code weggeschreven naar ***.",
    "csc_error_a1": "C# Compiler (csc) niet gevonden. Poging tot installatie...\n",
    "csc_error_a2": "CSC compiler niet gevonden en installatie mislukt. C# uitvoering afgebroken.",
    "csc_autoinst_fail": "Automatische installatie van C# compiler mislukt. Installeer de .NET SDK handmatig.\n",
    "csc_compiler_installed": "C# Compiler (csc) succesvol geïnstalleerd.\n",
    "csc_compiling_with": "Compileren met:",
    "csc_compilation_success": "Compilatie geslaagd.\n",
    "csc_execution_finished": "Uitvoering succesvol afgerond.",
    "csc_execution_error_a1": "Er is een fout opgetreden bij het uitvoeren van het programma:",
    "sh_platform_not_supported": "Uw platform wordt niet ondersteund voor het uitvoeren van Shell Script scripts.",
    "py_error_a1_title": "Onvoldoende Python-versie",
    "py_error_a1": "Installeer Python 3.13+.",
    "py_error_a2": "Python-interpreter niet gevonden.",
    "py_error_a3": "Kan Python-versie niet parseren.",
    "error_a1": "Fout",
    "error_a2": "Kon niet bestand openen",
    "error_a3": "Kon niet bestand openen:\n",
    "error_a4": "Kon niet schrijven naar bestand:\n",
    "error_a5": "Kan het bronbestand van Slash Code niet laden. Reden:\n\n",
    "error_c0": "Fout bij het bijwerken van de mapknop:",
    "error_c1": "Fout bij het bijwerken van het menulabel:",
    "error_c2": "Fout bij het bijwerken van het bestandslabel:",
    "error_c3": "Fout bij het bijwerken van het label:",
    "error_c4": "Fout bij het bijwerken van het themalabel:",
    "error_c5": "Fout bij het uitvoeren van de labelupdate:",
    "error_c6": "Fout bij het bijwerken van het label weergeven:",
    "error_c7": "Fout bij het bijwerken van het taallabel:",
    "error_c8": "Fout bij het bijwerken van het GUI-taallabel:",
    "error_d1": "Er is een exceptie opgetreden bij het uitvoeren van de code in het document. De reden hiervoor is:\n\n",
    "error_d1_5": "Er is een fout opgetreden tijdens het schrijven naar en uitvoeren van het document. De reden hiervoor is:\n\n",
    "error_d2": "De compiler is niet correct geïnstalleerd.",
    "deleting_dirs": "Map(pen) verwijderen:",
    "error_e1": "pip kon py7z niet installeren. Reden:",
    "directory_del_not_found": "Er is/zijn geen map(pen) gevonden om te verwijderen.",
    "find": "Vind",
    "find_query": "Vind:",
    "find_all": "Vind Alle",
    "replace": "Vervang",
    "replace_query": "Vervang:",
    "replace_all": "Vervang Alle",
    "runner_not_found": " niet gevonden!\n",
    "install_suggest": "Installeer het alstublieft eerst.\n",
    "instructions": "Instructies: ",
    "compilation_error": "Compilatie fout:\n",
    "opened_in_browser": "Geopend in de standaard browser.",
    "language_not_supported": "Taal niet gesteund voor executie.",
    "process_error": "Proces fout: ",
    "unexpected_error": "Onverwachte fout: ",
    "cleanup_failed": "Schoonmaking gefaald: ",
    "file": "Bestand",
    "new": "Nieuw",
    "open": "Open",
    "save": "Opslaan",
    "toggle_new_file_saving": "Nieuw Bestand Opslaan Inschakelen",
    "clean_temp_files": "Temporaire Bestanden Wissen",
    "clean_temp_directories": "Temporaire Mappen Volledig Wissen",
    "fully_wipe_directories": "Temporaire Mappen Wissen",
    "reboot_consolemode": "Opnieuw Opstarten In Consolemodus",
    "exit": "Verlaten",
    "edit": "Bewerken",
    "undo": "Ongedaan Maken",
    "redo": "Opnieuw Doen",
    "language": "Taal",
    "theme": "Thema",
    "theme_light": "Licht",
    "theme_dark": "Donker",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Nacht Uil",
    "theme_shades_of_purple": "Tinten Van Paars",
    "theme_high_contrast": "Hoog Contrast",
    "open_folder": "Open Map",
    "changed_language_to": "Taal veranderd naar ",
    "view": "Kijken",
    "zoom_in": "Inzoomen",
    "zoom_out": "Uitzoomen",
    "show_sidebar": "Maak Zijbalk Zichtbaar",
    "hide_sidebar": "Maak Zijbalk Onzichtbaar",
    "show_minimap": "Maak Minikaart Zichtbaar",
    "hide_minimap": "Maak Minikaart Onzichtbaar",
    "show_debug_info": "Toon foutopsporingsinfo",
    "hide_debug_info": "Verberg foutopsporingsinfo",
    "toggle_fullscreen": "Volledig Scherm Inschakelen",
    "exit_fullscreen": "Volledig Scherm Verlaten",
    "run": "Uitvoeren",
    "run_file": "Bestand Uitvoeren",
    "sc_output": "SC-Uitvoer",
    "output_sc_title": "-- Slash Code Teksteditor | SC-Uitvoer voor bestandsuitvoering --",
    "save_output_text": "Uitvoertekst opslaan",
    "highlighting_as": "Wordt gemarkeerd als: ",
    "plaintext": "Platte Text",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell Script",
    "python_files": "Python Bestanden",
    "javascript_files": "JavaScript Bestanden",
    "html_files": "HTML Bestanden",
    "c_files": "C Bestanden",
    "cpp_files": "C++ Bestanden",
    "header_files": "Headerbestanden",
    "text_files": "Tekstbestanden",
    "cs_files": "C# Bestanden",
    "css_files": "CSS Bestanden",
    "markdown_files": "Markdown Bestanden",
    "renpy_files": "Ren'Py Bestanden",
    "shell_files": "Shell Bestanden",
    "all_files": "Alle Bestanden",
    "binary_file_title": "Binair Bestand Gedetecteerd",
    "binary_file": "Er zijn ongebruikelijke tekens in dit document gedetecteerd. Wilt u het openen en de ruwe data door Slash Code laten lezen?\nWaarschuwing: dit zal Slash Code waarschijnlijk vertragen.",
    "session_loaded": "Sessie geladen:",
    "error_b1": "Fout gedurend bestand laden: ",
    "error_b2": "Fout gedurend map laden: "
    },
    "de": {
    "gui_lang": "GUI-Sprache",
    "msys_install": "MSYS2 installiert. Bitte MinGW über die MSYS2-Shell installieren: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Installation von MinGW-w64 fehlgeschlagen:",
    "gcc_used": "Genutztes GCC:",
    "gcc_error_a1": "Installation von G++ fehlgeschlagen.",
    "gcc_error_a2": "Überprüfung der G++-Version fehlgeschlagen:",
    "gcc_error_b1": "G++-Compiler nicht gefunden. Abbruch des C++-Laufs.",
    "gcc_error_b2": "Installation des MinGW-Compilers fehlgeschlagen.\n",
    "cpp_usercode_written": "C++-Code des Benutzers geschrieben nach ***.",
    "gcc_check_a1": "Suche nach vorhandenem G++-Compiler...",
    "gcc_check_a2": "Herunterladen und Installieren von MinGW-w64...",
    "gcc_check_a3": "MinGW-w64 wird von *** heruntergeladen...",
    "gcc_check_a4": "Bisher *** MB heruntergeladen...",
    "gcc_check_a4_5": "Insgesamt *** MB heruntergeladen.",
    "gcc_check_b1": "Entpacke MinGW-w64-Archiv...",
    "gcc_check_b2": "Versuche, G++-Compiler zu installieren/aktualisieren...",
    "gcc_compilation_attempt": "Versuch der Kompilierung mit Flag ***:",
    "gcc_compilation_success": "Kompilierung erfolgreich, führe ausführbare Datei aus...",
    "gcc_compilation_failed": "Kompilierung für *** mit Fehlern fehlgeschlagen:",
    "gcc_execution_finished": "Ausführung erfolgreich beendet.",
    "gcc_execution_error_a1": "Beim Ausführen der ausführbaren Datei ist ein Fehler aufgetreten:",
    "gcc_mingw_addpath": "MinGW-w64 bin-Ordner wurde PATH hinzugefügt:",
    "gcc_compiler_installed": "G++ erfolgreich installiert/aktualisiert.",
    "gcc_found_compiler_ver": "Gefundene G++-Version:",
    "gcc_sufficient_compiler_ver": "Die G++-Version ist ausreichend.",
    "gcc_old_compiler_ver": "Deine G++-Version ist zu alt und muss aktualisiert werden.",
    "gcc_mingw_extracted": "Entpackung abgeschlossen. MinGW installiert in:",
    "py7zr_installed": "Das py7zr-Paket wurde erfolgreich installiert.",
    "py7zr_error_a1": "Das Paket py7zr wurde nicht gefunden, installiere py7zr...",
    "csc_compiler": "C#-Compiler (csc)",
    "cs_usercode_written": "C#-Code des Benutzers geschrieben nach ***.",
    "csc_error_a1": "C#-Compiler (csc) nicht gefunden. Versuche zu installieren...\n",
    "csc_error_a2": "CSC-Compiler nicht gefunden und Installation fehlgeschlagen. C#-Lauf abgebrochen.",
    "csc_autoinst_fail": "Automatische Installation des C#-Compilers fehlgeschlagen. Bitte installiere das .NET SDK manuell.\n",
    "csc_compiler_installed": "C#-Compiler (csc) erfolgreich installiert.\n",
    "csc_compiling_with": "Kompiliere mit:",
    "csc_compilation_success": "Kompilierung erfolgreich.\n",
    "csc_execution_finished": "Ausführung erfolgreich beendet.",
    "csc_execution_error_a1": "Beim Versuch, die ausführbare Datei auszuführen, ist ein Fehler aufgetreten:",
    "sh_platform_not_supported": "Deine Plattform unterstützt das Ausführen von Shell-Skripten nicht.",
    "py_error_a1_title": "Unzureichende Python-Version",
    "py_error_a1": "Bitte installiere Python 3.13+.",
    "py_error_a2": "Python-Interpreter nicht gefunden.",
    "py_error_a3": "Python-Version konnte nicht analysiert werden.",
    "error_a1": "Fehler",
    "error_a2": "Datei konnte nicht geöffnet werden",
    "error_a3": "Datei konnte nicht geöffnet werden:\n",
    "error_a4": "Datei konnte nicht beschrieben werden:\n",
    "error_a5": "Quellcode-Datei von Slash Code konnte nicht geladen werden. Grund:\n\n",
    "error_c0": "Fehler beim Aktualisieren des Ordner-Buttons:",
    "error_c1": "Fehler beim Aktualisieren des Menü-Labels:",
    "error_c2": "Fehler beim Aktualisieren des Datei-Labels:",
    "error_c3": "Fehler beim Aktualisieren des Editier-Labels:",
    "error_c4": "Fehler beim Aktualisieren des Theme-Labels:",
    "error_c5": "Fehler beim Aktualisieren des Ausführungs-Labels:",
    "error_c6": "Fehler beim Aktualisieren des Ansicht-Labels:",
    "error_c7": "Fehler beim Aktualisieren des Sprach-Labels:",
    "error_c8": "Fehler beim Aktualisieren des GUI-Sprach-Labels:",
    "error_d1": "Beim Ausführen des Dokumentcodes ist eine Ausnahme aufgetreten. Grund:\n\n",
    "error_d1_5": "Beim Schreiben und Ausführen des Dokuments ist eine Ausnahme aufgetreten. Grund:\n\n",
    "error_d2": "Der Compiler wurde nicht korrekt installiert.",
    "error_e1": "pip konnte py7z nicht installieren. Grund:",
    "deleting_dirs": "Lösche Verzeichnis(se): ",
    "directory_del_not_found": "Keine Verzeichnisse zum Löschen gefunden.",
    "find": "Suchen",
    "find_query": "Suchen:",
    "find_all": "Alle suchen",
    "replace": "Ersetzen",
    "replace_query": "Ersetzen:",
    "replace_all": "Alle ersetzen",
    "runner_not_found": " nicht gefunden!\n",
    "install_suggest": "Bitte zuerst installieren.\n",
    "instructions": "Anleitung: ",
    "compilation_error": "Kompilierfehler:\n",
    "opened_in_browser": "Im Standardbrowser geöffnet.",
    "language_not_supported": "Sprache wird für Ausführung nicht unterstützt.",
    "process_error": "Prozessfehler: ",
    "unexpected_error": "Unerwarteter Fehler: ",
    "cleanup_failed": "Bereinigung fehlgeschlagen: ",
    "file": "Datei",
    "new": "Neu",
    "open": "Öffnen",
    "save": "Speichern",
    "toggle_new_file_saving": "Neues Dateispeichern umschalten",
    "clean_temp_files": "Temporäre Dateien bereinigen",
    "clean_temp_directories": "Temporäre Verzeichnisse bereinigen",
    "fully_wipe_directories": "Temporäre Verzeichnisse vollständig löschen",
    "reboot_consolemode": "Im Konsolenmodus neu starten",
    "exit": "Beenden",
    "edit": "Bearbeiten",
    "undo": "Rückgängig",
    "redo": "Wiederholen",
    "language": "Sprache",
    "theme": "Thema",
    "theme_light": "Hell",
    "theme_dark": "Dunkel",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Nacht-Eule",
    "theme_shades_of_purple": "Lila Nuancen",
    "theme_high_contrast": "Hoher Kontrast",
    "open_folder": "Ordner öffnen",
    "changed_language_to": "Sprache geändert zu ",
    "view": "Ansicht",
    "zoom_in": "Vergrößern",
    "zoom_out": "Verkleinern",
    "show_sidebar": "Seitenleiste anzeigen",
    "hide_sidebar": "Seitenleiste ausblenden",
    "show_minimap": "Minikarte anzeigen",
    "hide_minimap": "Minikarte ausblenden",
    "show_debug_info": "Debug-Informationen anzeigen",
    "hide_debug_info": "Debug-Informationen ausblenden",
    "toggle_fullscreen": "Vollbild umschalten",
    "exit_fullscreen": "Vollbild verlassen",
    "run": "Ausführen",
    "run_file": "Datei ausführen",
    "sc_output": "SC-Ausgabe",
    "output_sc_title": "-- Slash Code Texteditor | SC-Ausgabe für Dateiausführung --",
    "save_output_text": "Ausgabetext speichern",
    "highlighting_as": "Markierung als: ",
    "plaintext": "Klartext",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell-Skript",
    "python_files": "Python-Dateien",
    "javascript_files": "JavaScript-Dateien",
    "html_files": "HTML-Dateien",
    "c_files": "C-Dateien",
    "cpp_files": "C++-Dateien",
    "header_files": "Header-Dateien",
    "text_files": "Textdateien",
    "cs_files": "C#-Dateien",
    "css_files": "CSS-Dateien",
    "markdown_files": "Markdown-Dateien",
    "renpy_files": "Ren'Py-Dateien",
    "shell_files": "Shell-Skriptdateien",
    "all_files": "Alle Dateien",
    "binary_file_title": "Binärdatei erkannt",
    "binary_file": "Ungewöhnliche Zeichen wurden in diesem Dokument erkannt. Möchten Sie es öffnen und Slash Code die Rohdaten lesen lassen?\nWarnung: Dies wird Slash Code vermutlich verlangsamen.",
    "session_loaded": "Sitzung geladen:",
    "error_b1": "Fehler beim Laden der Datei: ",
    "error_b2": "Fehler beim Laden des Verzeichnisses: "
    },
    "es": {
    "gui_lang": "GUI Lenguaje",
    "msys_install": "MSYS2 instalado. Por favor instala MinGW desde la terminal de MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Error al instalar MinGW-w64:",
    "gcc_used": "GCC usado:",
    "gcc_error_a1": "Falló la instalación de G++.",
    "gcc_error_a2": "No se pudo verificar la versión de G++:",
    "gcc_error_b1": "Compilador G++ no encontrado. Abortando ejecución de C++.",
    "gcc_error_b2": "Falló la instalación del compilador MinGW.\n",
    "cpp_usercode_written": "Código C++ del usuario guardado en ***.",
    "gcc_check_a1": "Verificando existencia de compilador G++...",
    "gcc_check_a2": "Descargando e instalando MinGW-w64...",
    "gcc_check_a3": "Descargando MinGW-w64 desde ***...",
    "gcc_check_a4": "Descargados *** MB hasta ahora...",
    "gcc_check_a4_5": "Descargados *** MB en total.",
    "gcc_check_b1": "Extrayendo archivo MinGW-w64...",
    "gcc_check_b2": "Intentando instalar/actualizar compilador G++...",
    "gcc_compilation_attempt": "Intentando compilar con la bandera ***:",
    "gcc_compilation_success": "Compilación exitosa, ejecutando programa...",
    "gcc_compilation_failed": "Compilación fallida para *** con errores:",
    "gcc_execution_finished": "Ejecución finalizada exitosamente.",
    "gcc_execution_error_a1": "Ocurrió un error al intentar ejecutar el programa:",
    "gcc_mingw_addpath": "Carpeta bin de MinGW-w64 añadida al PATH:",
    "gcc_compiler_installed": "G++ instalado/actualizado correctamente.",
    "gcc_found_compiler_ver": "Versión de G++ encontrada:",
    "gcc_sufficient_compiler_ver": "La versión de G++ es suficiente.",
    "gcc_old_compiler_ver": "Tu versión de G++ es demasiado antigua y debe actualizarse.",
    "gcc_mingw_extracted": "Extracción completa. MinGW instalado en:",
    "py7zr_installed": "El paquete py7zr se instaló correctamente.",
    "csc_compiler": "Compilador C# (csc)",
    "cs_usercode_written": "Código C# del usuario guardado en ***.",
    "csc_error_a1": "Compilador C# (csc) no encontrado. Intentando instalar...\n",
    "csc_error_a2": "Compilador CSC no encontrado y la instalación falló. Abortando ejecución de C#.",
    "csc_autoinst_fail": "Fallo al instalar automáticamente el compilador C#. Por favor, instala el SDK de .NET manualmente.\n",
    "csc_compiler_installed": "Compilador C# (csc) instalado correctamente.\n",
    "csc_compiling_with": "Compilando con:",
    "csc_compilation_success": "Compilación exitosa.\n",
    "csc_execution_finished": "Ejecución finalizada exitosamente.",
    "csc_execution_error_a1": "Se ha producido un error al intentar ejecutar el programa:",
    "sh_platform_not_supported": "Tu plataforma no es compatible para ejecutar scripts Shell Script.",
    "py_error_a1_title": "Versión de Python insuficiente",
    "py_error_a1": "Instale Python 3.13+.",
    "py_error_a2": "No se encontró el intérprete de Python.",
    "py_error_a3": "No se pudo analizar la versión de Python.",
    "error_a1": "Error",
    "error_a2": "No se pudo abrir el archivo",
    "error_a3": "No se pudo abrir el archivo:\n",
    "error_a4": "No se pudo escribir el archivo:\n",
    "error_a5": "No se pudo cargar el archivo fuente de Slash Code. Motivo:\n\n",
    "error_c0": "Error al actualizar el botón de carpeta:",
    "error_c1": "Error al actualizar la etiqueta del menú:",
    "error_c2": "Error al actualizar la etiqueta del archivo:",
    "error_c3": "Error al actualizar la etiqueta de edición:",
    "error_c4": "Error al actualizar la etiqueta del tema:",
    "error_c5": "Error al ejecutar la actualización de la etiqueta:",
    "error_c6": "Error al actualizar la etiqueta de la vista:",
    "error_c7": "Error al actualizar la etiqueta del idioma:",
    "error_c8": "Error al actualizar la etiqueta del idioma de la GUI:",
    "error_d1": "Se ha producido una excepción al intentar ejecutar el código del documento. La razón es:\n\n",
    "error_d1_5": "Se produjo una excepción al intentar escribir y ejecutar el documento. La razón es:\n\n",
    "error_d2": "El compilador no se instaló correctamente.",
    "error_e1": "pip no pudo instalar py7z. Motivo:",
    "deleting_dirs": "Eliminando directorio(s): ", 
    "directory_del_not_found": "No se encontraron directorio(s) para eliminar.",
    "find": "Buscar",
    "find_query": "Buscar:",
    "find_all": "Buscar todos",
    "replace": "Reemplazar", 
    "replace_query": "Reemplazar:", 
    "replace_all": "Reemplazar Todo",
    "runner_not_found": " no encontrado!\n",
    "install_suggest": "Por favor instálalo primero.\n",
    "instructions": "Instrucciones: ",
    "compilation_error": "Error de compilación:\n",
    "opened_in_browser": "Abierto en el navegador predeterminado.",
    "language_not_supported": "Idioma no compatible para ejecución.",
    "process_error": "Error del proceso: ",
    "unexpected_error": "Error inesperado: ",
    "cleanup_failed": "Fallo al limpiar: ",
    "file": "Archivo",
    "new": "Nuevo",
    "open": "Abrir",
    "save": "Guardar",
    "toggle_new_file_saving": "Activar el guardado de nuevos archivos",
    "clean_temp_files": "Limpiar archivos temporales",
    "clean_temp_directories": "Limpiar directorios temporales",
    "fully_wipe_directories": "Borrar completamente los directorios temporales",
    "reboot_consolemode": "Reiniciar en modo consola",
    "exit": "Salir",
    "edit": "Editar",
    "undo": "Deshacer",
    "redo": "Rehacer",
    "language": "Lenguaje",
    "theme": "Tema",
    "theme_light": "Claro",
    "theme_dark": "Oscuro",
    "theme_dracula": "Drácula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Búho Nocturno",
    "theme_shades_of_purple": "Tonos de Púrpura",
    "open_folder": "Abrir Carpeta",
    "changed_language_to": "Cambió de idioma a ",
    "view": "Vista",
    "zoom_in": "Acercar",
    "zoom_out": "Alejar",
    "show_sidebar": "Mostrar barra lateral",
    "hide_sidebar": "Ocultar barra lateral",
    "show_minimap": "Mostrar minimapa",
    "hide_minimap": "Ocultar minimapa",
    "show_debug_info": "Mostrar información de depuración",
    "hide_debug_info": "Ocultar información de depuración",
    "toggle_fullscreen": "Activar pantalla completa",
    "exit_fullscreen": "Salir de pantalla completa",
    "run": "Ejecutar",
    "run_file": "Ejecutar archivo",
    "sc_output": "SC-Producción",
    "output_sc_title": "-- Editor de texto de Slash Code | Salida SC para ejecución de archivos --",
    "save_output_text": "Guardar texto de salida",
    "highlighting_as": "Resaltado como: ",
    "plaintext": "Texto plano",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Script de Shell",
    "python_files": "Archivos de Python",
    "javascript_files": "Archivos de JavaScript",
    "html_files": "Archivos de HTML",
    "c_files": "Archivos de C",
    "cpp_files": "Archivos de C++",
    "header_files": "Archivos de Encabezado",
    "text_files": "Archivos de Texto",
    "cs_files": "Archivos de C#",
    "css_files": "Archivos de CSS",
    "markdown_files": "Archivos de Markdown",
    "renpy_files": "Archivos de Ren'Py",
    "shell_files": "Archivos de Shell",
    "all_files": "Todos Los Archivos",
    "binary_file_title": "Archivo binario detectado",
    "binary_file": "Se han detectado caracteres inusuales en este documento. ¿Desea abrirlo y que Slash Code lea los datos sin procesar?\nAdvertencia: esto probablemente ralentizará Slash Code.",
    "session_loaded": "Sesión cargada:",
    "error_b1": "Error al cargar el archivo: ",
    "error_b2": "Error al cargar el directorio: "
    },
    "it": {
    "gui_lang": "Lingua GUI",
    "msys_install": "MSYS2 installato. Per favore installa MinGW tramite la shell MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Installazione di MinGW-w64 fallita:",
    "gcc_used": "GCC utilizzato:",
    "gcc_error_a1": "Installazione di G++ fallita.",
    "gcc_error_a2": "Impossibile controllare la versione di G++:",
    "gcc_error_b1": "Compilatore G++ non trovato. Interruzione esecuzione C++.",
    "gcc_error_b2": "Installazione del compilatore MinGW fallita.\n",
    "cpp_usercode_written": "Codice C++ utente scritto in ***.",
    "gcc_check_a1": "Verifica della presenza di un compilatore G++ esistente...",
    "gcc_check_a2": "Download e installazione di MinGW-w64 in corso...",
    "gcc_check_a3": "Download di MinGW-w64 da *** in corso...",
    "gcc_check_a4": "*** MB scaricati finora...",
    "gcc_check_a4_5": "*** MB scaricati in totale.",
    "gcc_check_b1": "Estrazione dell'archivio MinGW-w64 in corso...",
    "gcc_check_b2": "Tentativo di installazione/aggiornamento del compilatore G++...",
    "gcc_compilation_attempt": "Tentativo di compilazione con flag ***:",
    "gcc_compilation_success": "Compilazione riuscita, esecuzione del file eseguibile...",
    "gcc_compilation_failed": "Compilazione fallita per *** con errori:",
    "gcc_execution_finished": "Esecuzione completata con successo.",
    "gcc_execution_error_a1": "Errore durante il tentativo di eseguire il file eseguibile:",
    "gcc_mingw_addpath": "Cartella bin di MinGW-w64 aggiunta al PATH:",
    "gcc_compiler_installed": "G++ installato/aggiornato con successo.",
    "gcc_found_compiler_ver": "Versione di G++ trovata:",
    "gcc_sufficient_compiler_ver": "La versione di G++ è sufficiente.",
    "gcc_old_compiler_ver": "La tua versione di G++ è troppo vecchia e deve essere aggiornata.",
    "gcc_mingw_extracted": "Estrazione completata. MinGW installato in:",
    "py7zr_installed": "Il pacchetto py7zr è stato installato con successo.",
    "py7zr_error_a1": "Pacchetto py7zr non trovato, installazione in corso...",
    "csc_compiler": "Compilatore C# (csc)",
    "cs_usercode_written": "Codice C# utente scritto in ***.",
    "csc_error_a1": "Compilatore C# (csc) non trovato. Tentativo di installazione in corso...\n",
    "csc_error_a2": "Compilatore CSC non trovato e installazione fallita. Interruzione esecuzione C#.",
    "csc_autoinst_fail": "Installazione automatica del compilatore C# fallita. Si prega di installare manualmente il .NET SDK.\n",
    "csc_compiler_installed": "Compilatore C# (csc) installato con successo.\n",
    "csc_compiling_with": "Compilazione con:",
    "csc_compilation_success": "Compilazione riuscita.\n",
    "csc_execution_finished": "Esecuzione completata con successo.",
    "csc_execution_error_a1": "Si è verificato un errore durante il tentativo di eseguire il file eseguibile:",
    "sh_platform_not_supported": "La tua piattaforma non supporta l'esecuzione di script Shell.",
    "py_error_a1_title": "Versione Python insufficiente",
    "py_error_a1": "Si prega di installare Python 3.13 o superiore.",
    "py_error_a2": "Interpreter Python non trovato.",
    "py_error_a3": "Impossibile analizzare la versione di Python.",
    "error_a1": "Errore",
    "error_a2": "Impossibile aprire il file",
    "error_a3": "Impossibile aprire il file:\n",
    "error_a4": "Impossibile scrivere nel file:\n",
    "error_a5": "Impossibile caricare il file sorgente di Slash Code. Motivo:\n\n",
    "error_c0": "Errore durante l'aggiornamento del pulsante cartella:",
    "error_c1": "Errore durante l'aggiornamento dell'etichetta del menu:",
    "error_c2": "Errore durante l'aggiornamento dell'etichetta del file:",
    "error_c3": "Errore durante l'aggiornamento dell'etichetta modifica:",
    "error_c4": "Errore durante l'aggiornamento dell'etichetta tema:",
    "error_c5": "Errore durante l'aggiornamento dell'etichetta esecuzione:",
    "error_c6": "Errore durante l'aggiornamento dell'etichetta visualizzazione:",
    "error_c7": "Errore durante l'aggiornamento dell'etichetta lingua:",
    "error_c8": "Errore durante l'aggiornamento dell'etichetta lingua GUI:",
    "error_d1": "Si è verificata un'eccezione durante il tentativo di eseguire il codice del documento. Il motivo è:\n\n",
    "error_d1_5": "Si è verificata un'eccezione durante il tentativo di scrivere e eseguire il documento. Il motivo è:\n\n",
    "error_d2": "Il compilatore non è stato installato correttamente.",
    "error_e1": "pip non è riuscito a installare py7z. Motivo:",
    "deleting_dirs": "Eliminazione della/e cartella/e: ",
    "directory_del_not_found": "Nessuna cartella trovata per l'eliminazione.",
    "find": "Trova",
    "find_query": "Trova:",
    "find_all": "Trova tutto",
    "replace": "Sostituisci",
    "replace_query": "Sostituisci con:",
    "replace_all": "Sostituisci tutto",
    "runner_not_found": " non trovato!\n",
    "install_suggest": "Si prega di installarlo prima.\n",
    "instructions": "Istruzioni: ",
    "compilation_error": "Errore di compilazione:\n",
    "opened_in_browser": "Aperto nel browser predefinito.",
    "language_not_supported": "Lingua non supportata per l'esecuzione.",
    "process_error": "Errore del processo: ",
    "unexpected_error": "Errore imprevisto: ",
    "cleanup_failed": "Pulizia fallita: ",
    "file": "File",
    "new": "Nuovo",
    "open": "Apri",
    "save": "Salva",
    "toggle_new_file_saving": "Attiva disattiva salvataggio nuovo file",
    "clean_temp_files": "Pulisci file temporanei",
    "clean_temp_directories": "Pulisci cartelle temporanee",
    "fully_wipe_directories": "Cancella completamente le cartelle temporanee",
    "reboot_consolemode": "Riavvia in modalità console",
    "exit": "Esci",
    "edit": "Modifica",
    "undo": "Annulla",
    "redo": "Ripristina",
    "language": "Lingua",
    "theme": "Tema",
    "theme_light": "Chiaro",
    "theme_dark": "Scuro",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Gufo Notturno",
    "theme_shades_of_purple": "Tonalità di Viola",
    "theme_high_contrast": "Alto Contrasto",
    "open_folder": "Apri cartella",
    "changed_language_to": "Lingua cambiata in ",
    "view": "Visualizza",
    "zoom_in": "Zoom in",
    "zoom_out": "Zoom out",
    "show_sidebar": "Mostra barra laterale",
    "hide_sidebar": "Nascondi barra laterale",
    "show_minimap": "Mostra minimappa",
    "hide_minimap": "Nascondi minimappa",
    "show_debug_info": "Mostra info debug",
    "hide_debug_info": "Nascondi info debug",
    "toggle_fullscreen": "Attiva/disattiva full screen",
    "exit_fullscreen": "Esci dal full screen",
    "run": "Esegui",
    "run_file": "Esegui file",
    "sc_output": "Output SC",
    "output_sc_title": "-- Editor di Testo Slash Code | Output SC per esecuzione file --",
    "save_output_text": "Salva testo output",
    "highlighting_as": "Evidenziando come: ",
    "plaintext": "Testo semplice",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Script di Shell",
    "python_files": "File Python",
    "javascript_files": "File JavaScript",
    "html_files": "File HTML",
    "c_files": "File C",
    "cpp_files": "File C++",
    "header_files": "File header",
    "text_files": "File di testo",
    "cs_files": "File C#",
    "css_files": "File CSS",
    "markdown_files": "File Markdown",
    "renpy_files": "File Ren'Py",
    "shell_files": "File Shell",
    "all_files": "Tutti i file",
    "binary_file_title": "File binario rilevato",
    "binary_file": "Caratteri insoliti sono stati rilevati in questo documento, vuoi aprirlo e lasciare che Slash Code legga i dati grezzi?\nAttenzione, questo probabilmente rallenterà Slash Code.",
    "session_loaded": "Sessione caricata:",
    "error_b1": "Errore nel caricamento del file: ",
    "error_b2": "Errore nel caricamento della cartella: "
    },
    "fr": {
    "gui_lang": "Langue de l'interface",
    "msys_install": "MSYS2 est installé. Veuillez installer MinGW via le terminal MSYS2 : pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Échec de l'installation de MinGW-w64:",
    "gcc_used": "GCC utilisé:",
    "gcc_error_a1": "Échec de l'installation de G++.",
    "gcc_error_a2": "Échec de la vérification de la version de G++:",
    "gcc_error_b1": "Compilateur G++ introuvable. Exécution C++ annulée.",
    "gcc_error_b2": "Échec de l'installation du compilateur MinGW.\n",
    "cpp_usercode_written": "Code C++ de l'utilisateur écrit dans ***.",
    "gcc_check_a1": "Vérification de l'existence du compilateur G++...",
    "gcc_check_a2": "Téléchargement et installation de MinGW-w64...",
    "gcc_check_a3": "Téléchargement de MinGW-w64 depuis ***...",
    "gcc_check_a4": "*** Mo téléchargés jusqu'à présent...",
    "gcc_check_a4_5": "*** Mo téléchargés en total.",
    "gcc_check_b1": "Extraction de l'archive MinGW-w64...",
    "gcc_check_b2": "Tentative d'installation/mise à jour du compilateur G++...",
    "gcc_compilation_attempt": "Tentative de compilation avec le drapeau ***:",
    "gcc_compilation_success": "Compilation réussie, exécution du programme...",
    "gcc_compilation_failed": "Échec de la compilation pour *** avec erreurs:",
    "gcc_execution_finished": "Exécution terminée avec succès.",
    "gcc_execution_error_a1": "Une erreur est survenue lors de l'exécution du programme:",
    "gcc_mingw_addpath": "Dossier bin de MinGW-w64 ajouté au PATH:",
    "gcc_compiler_installed": "G++ installé/mis à jour avec succès.",
    "gcc_found_compiler_ver": "Version de G++ trouvée:",
    "gcc_sufficient_compiler_ver": "La version de G++ est suffisante.",
    "gcc_old_compiler_ver": "Votre version de G++ est trop ancienne, une mise à jour est nécessaire.",
    "gcc_mingw_extracted": "Extraction terminée. MinGW installé à:",
    "py7zr_installed": "Le package py7zr a été installé avec succès.",
    "csc_compiler": "Compilateur C# (csc)",
    "cs_usercode_written": "Code C# de l'utilisateur écrit dans ***.",
    "csc_error_a1": "Compilateur C# (csc) introuvable. Tentative d'installation...\n",
    "csc_error_a2": "Compilateur CSC introuvable et échec de l'installation. Exécution C# annulée.",
    "csc_autoinst_fail": "Échec de l'installation automatique du compilateur C#. Veuillez installer le SDK .NET manuellement.\n",
    "csc_compiler_installed": "Compilateur C# (csc) installé avec succès.\n",
    "csc_compiling_with": "Compilation avec:",
    "csc_compilation_success": "Compilation réussie.\n",
    "csc_execution_finished": "Exécution terminée avec succès.",
    "csc_execution_error_a1": "Une erreur s'est produite lors de la tentative d'exécution du programme:",
    "sh_platform_not_supported": "Votre plateforme ne prend pas en charge l'exécution de scripts Shell.",
    "py_error_a1_title": "Version Python insuffisante",
    "py_error_a1": "Veuillez installer Python 3.13+.",
    "py_error_a2": "Interpréteur Python introuvable.", 
    "py_error_a3": "Impossible d'analyser la version Python.",
    "error_a1": "Erreur",
    "error_a2": "Impossible d'ouvrir le fichier",
    "error_a3": "Impossible d'ouvrir le fichier:\n",
    "error_a4": "Impossible d'écrire dans le fichier:\n",
    "error_a5": "Impossible de charger le fichier source du Slash Code. Motif:\n\n",
    "error_c0": "Erreur de mise à jour du bouton de dossier:",
    "error_c1": "Erreur de mise à jour du libellé du menu:",
    "error_c2": "Erreur de mise à jour du libellé du fichier:",
    "error_c3": "Erreur de mise à jour de l'étiquette de modification:",
    "error_c5": "Erreur de mise à jour de l'étiquette d'exécution:",
    "error_c6": "Erreur de mise à jour de l'étiquette d'affichage:",
    "error_c7": "Erreur de mise à jour du libellé de langue:",
    "error_c8": "Erreur de mise à jour du libellé de langue de l'interface graphique:",
    "error_d1": "Une exception s'est produite lors de l'exécution du code du document. La raison en est:\n\n",
    "error_d1_5": "Une exception s'est produite lors de la tentative d'écriture et d'exécution du document. La raison en est:\n\n",
    "error_d2": "Le compilateur n'a pas pu s'installer correctement.",
    "error_e1": "pip n'a pas réussi à installer py7z. Motif:",
    "deleting_dirs": "Suppression de répertoire(s): ", 
    "directory_del_not_found": "Aucun répertoire(s) à supprimer n'a été trouvé.",
    "find": "Rechercher",
    "find_query": "Rechercher:",
    "find_all": "Recherchez tout",
    "replace": "Remplacer", 
    "replace_query": "Remplacer:", 
    "replace_all": "Remplacer Tout",
    "runner_not_found": " introuvable!\n",
    "install_suggest": "Veuillez l'installer d'abord.\n",
    "instructions": "Instructions: ",
    "compilation_error": "Erreur de compilation:\n",
    "opened_in_browser": "Ouvert dans le navigateur par défaut.",
    "language_not_supported": "Langue non prise en charge pour l'exécution.",
    "process_error": "Erreur de processus: ",
    "unexpected_error": "Erreur inattendue: ",
    "cleanup_failed": "Échec du nettoyage: ",
    "file": "Fichier",
    "new": "Nouveau",
    "open": "Ouvrir",
    "save": "Enregistrer",
    "toggle_new_file_saving": "Activer l'enregistrement d'un nouveau fichier",
    "clean_temp_files": "Nettoyer les fichiers temporaires",
    "clean_temp_directories": "Nettoyer les dossiers temporaires",
    "fully_wipe_directories": "Effacer complètement les dossiers temporaires",
    "reboot_consolemode": "Redémarrer en mode console",
    "exit": "Quitter",
    "edit": "Éditer",
    "undo": "Annuler",
    "redo": "Rétablir",
    "language": "Langue",
    "theme": "Thème",
    "theme_light": "Clair",
    "theme_dark": "Sombre",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Chouette Nocturne",
    "theme_shades_of_purple": "Nuances de Violet",
    "theme_high_contrast": "Contraste Élevé",
    "open_folder": "Ouvrir le dossier",
    "changed_language_to": "Langue changée en ",
    "view": "Affichage",
    "zoom_in": "Agrandir",
    "zoom_out": "Rétrécir",
    "show_sidebar": "Afficher la barre latérale",
    "hide_sidebar": "Masquer la barre latérale",
    "show_minimap": "Afficher la minicarte",
    "hide_minimap": "Masquer la minicarte",
    "show_debug_info": "Afficher les informations de débogage",
    "hide_debug_info": "Masquer les informations de débogage",
    "toggle_fullscreen": "Activer le plein écran",
    "exit_fullscreen": "Quitter le plein écran",
    "run": "Exécuter",
    "run_file": "Exécuter le fichier",
    "sc_output": "SC-Sortir",
    "output_sc_title": "-- Éditeur de texte de Slash Code | Sortie SC pour l'exécution de fichiers --",
    "save_output_text": "Enregistrer le texte de sortie",
    "highlighting_as": "Surlignage comme: ",
    "plaintext": "Texte brut",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Script Shell",
    "python_files": "Fichiers Python",
    "javascript_files": "Fichiers JavaScript",
    "html_files": "Fichiers HTML",
    "c_files": "Fichiers C",
    "cpp_files": "Fichiers C++",
    "header_files": "Fichiers D'en-tête",
    "text_files": "fichiers texte",
    "cs_files": "Fichiers C#",
    "css_files": "Fichiers CSS",
    "markdown_files": "Fichiers Markdown",
    "renpy_files": "Fichiers Ren'Py",
    "shell_files": "Fichiers Shell",
    "all_files": "Tous Les Fichiers",
    "binary_file_title": "Fichier binaire détecté",
    "binary_file": "Des caractères inhabituels ont été détectés dans ce document. Souhaitez-vous l'ouvrir et laisser Slash Code lire les données brutes?\nAttention, cela risque de ralentir Slash Code.",
    "session_loaded": "Session chargé:",
    "error_b1": "Erreur lors du chargement du fichier: ",
    "error_b2": "Erreur lors du chargement du dossier: "
    },
    
    "jp": {
    "gui_lang": "GUI 言語",
    "msys_install": "MSYS2がインストールされました。MSYS2シェルでMinGWをインストールしてください: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "MinGW-w64のインストールに失敗しました:",
    "gcc_used": "使用中のGCC:",
    "gcc_error_a1": "G++のインストールに失敗しました。",
    "gcc_error_a2": "G++のバージョン確認に失敗しました:",
    "gcc_error_b1": "G++コンパイラが見つかりません。C++の実行を中止します。",
    "gcc_error_b2": "MinGWコンパイラのインストールに失敗しました。\n",
    "cpp_usercode_written": "ユーザーのC++コードが***に書き込まれました。",
    "gcc_check_a1": "既存のG++コンパイラを確認しています...",
    "gcc_check_a2": "MinGW-w64をダウンロードしてインストールしています...",
    "gcc_check_a3": "***からMinGW-w64をダウンロード中...",
    "gcc_check_a4": "これまでに*** MBをダウンロードしました...",
    "gcc_check_a4_5": "合計*** MBをダウンロードしました。",
    "gcc_check_b1": "MinGW-w64アーカイブを解凍中...",
    "gcc_check_b2": "G++コンパイラのインストール/更新を試みています...",
    "gcc_compilation_attempt": "*** フラグでのコンパイルを試みています:",
    "gcc_compilation_success": "コンパイル成功。実行ファイルを実行しています...",
    "gcc_compilation_failed": "*** のコンパイルに失敗しました。エラー内容:",
    "gcc_execution_finished": "実行が正常に終了しました。",
    "gcc_execution_error_a1": "実行ファイルの起動中にエラーが発生しました:",
    "gcc_mingw_addpath": "MinGW-w64のbinフォルダをPATHに追加しました:",
    "gcc_compiler_installed": "G++が正常にインストール/更新されました。",
    "gcc_found_compiler_ver": "検出されたG++バージョン:",
    "gcc_sufficient_compiler_ver": "G++のバージョンは十分です。",
    "gcc_old_compiler_ver": "G++のバージョンが古いため、アップグレードが必要です。",
    "gcc_mingw_extracted": "解凍完了。MinGWは以下にインストールされました:",
    "py7zr_installed": "py7zrパッケージが正常にインストールされました。",
    "csc_compiler": "C# コンパイラー (csc)",
    "cs_usercode_written": "ユーザーのC#コードが***に書き込まれました。",
    "csc_error_a1": "C# コンパイラー (csc) が見つかりません。インストールを試みています...\n",
    "csc_error_a2": "CSC コンパイラーが見つからず、インストールに失敗しました。C# 実行を中止します。",
    "csc_autoinst_fail": "C# コンパイラーの自動インストールに失敗しました。手動で .NET SDK をインストールしてください。\n",
    "csc_compiler_installed": "C# コンパイラー (csc) が正常にインストールされました。\n",
    "csc_compiling_with": "以下の環境でコンパイル中:",
    "csc_compilation_success": "コンパイル成功。\n",
    "csc_execution_finished": "実行が正常に終了しました。",
    "csc_execution_error_a1": "実行ファイルの起動中にエラーが発生しました:",
    "sh_platform_not_supported": "お使いのプラットフォームではシェルスクリプトの実行はサポートされていません。",
    "py_error_a1_title": "Pythonのバージョンが不十分です",
    "py_error_a1": "Python 3.13以降をインストールしてください。",
    "py_error_a2": "Pythonインタープリターが見つかりません。",
    "py_error_a3": "Pythonのバージョンを解析できませんでした。",
    "error_a1": "エラー",
    "error_a2": "ファイルを開けませんでした",
    "error_a3": "ファイルを開けませんでした:\n",
    "error_a4": "ファイルに書き込めませんでした:\n",
    "error_a5": "スラッシュコードのソースファイルを読み込めませんでした。理由:\n\n",
    "error_c0": "フォルダボタン更新エラー:",
    "error_c1": "メニューラベル更新エラー:",
    "error_c2": "ファイルラベル更新エラー:",
    "error_c3": "編集ラベル更新エラー:",
    "error_c4": "テーマラベル更新エラー:",
    "error_c5": "実行ラベル更新エラー:",
    "error_c6": "表示ラベル更新エラー:",
    "error_c7": "言語ラベル更新エラー:",
    "error_c8": "GUI言語ラベル更新エラー:",
    "error_d1": "ドキュメントのコードを実行中に例外が発生しました。理由は次の通りです:\n\n",
    "error_d1_5": "ドキュメントの書き込みと実行中に例外が発生しました。理由は次の通りです:\n\n",
    "error_d2": "コンパイラのインストールに失敗しました。",
    "error_e1": "pipはpy7zのインストールに失敗しました。理由:",
    "deleting_dirs": "ディレクトリを削除しています: ",
    "directory_del_not_found": "削除するディレクトリが見つかりません。",
    "find": "検索",
    "find_query": "検索:",
    "find_all": "すべてを検索ます",
    "replace": "交換", 
    "replace_query": "交換:", 
    "replace_all": "すべてを交換します",
    "runner_not_found": " が見つかりません！\n",
    "install_suggest": "まずインストールしてください。\n",
    "instructions": "使い方:",
    "compilation_error": "コンパイルエラー:\n",
    "opened_in_browser": "デフォルトのブラウザで開きました。",
    "language_not_supported": "この言語は実行に対応していません。",
    "process_error": "プロセスエラー: ",
    "unexpected_error": "予期しないエラー:",
    "cleanup_failed": "クリーンアップに失敗しました:",
    "file": "ファイル",
    "new": "新規",
    "open": "開く",
    "save": "保存",
    "toggle_new_file_saving": "新しいファイルの保存を切り替える",
    "clean_temp_files": "一時ファイルを消去する",
    "clean_temp_directories": "一時ディレクトリを消去する",
    "fully_wipe_directories": "一時ディレクトリを完全に消去する",
    "reboot_consolemode": "コンソールモードで再起動",
    "exit": "終了",
    "edit": "編集",
    "undo": "元に戻す",
    "redo": "やり直し",
    "language": "言語",
    "theme": "テーマ",
    "theme_light": "ライト",
    "theme_dark": "ダーク",
    "theme_dracula": "ドラキュラ",
    "theme_monokai": "モノカイ",
    "theme_night_owl": "ナイトアウル",
    "theme_shades_of_purple": "紫の影",
    "theme_high_contrast": "高コントラスト",
    "open_folder": "フォルダーを開く",
    "changed_language_to": "言語", # Japanese puts the topic in the middle, not the end, so we'll have to put the verb part to tbe end.
    "view": "表示",
    "zoom_in": "ズームイン",
    "zoom_out": "ズームアウト",
    "show_sidebar": "サイドバーを表示",
    "hide_sidebar": "サイドバーを非表示",
    "show_minimap": "ミニマップを表示",
    "hide_minimap": "ミニマップを非表示",
    "show_debug_info": "デバッグ情報を表示",
    "hide_debug_info": "デバッグ情報を非表示",
    "toggle_fullscreen": "全画面表示の切り替え",
    "exit_fullscreen": "全画面表示を終了",
    "run": "実行",
    "run_file": "ファイルを実行",
    "sc_output": "SC-出力",
    "output_sc_title": "-- スラッシュコードテキストエディター | ファイル実行用のSC出力 --",
    "save_output_text": "出力テキストを保存",
    "highlighting_as": "ハイライト:",
    "plaintext": "プレーンテキスト",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "シェルスクリプト",
    "python_files": "Python ファイル",
    "javascript_files": "JavaScript ファイル",
    "html_files": "HTML ファイル",
    "c_files": "C ファイル",
    "cpp_files": "C++ ファイル",
    "header_files": "ヘッダーファイル",
    "text_files": "テキストファイル",
    "cs_files": "C# ファイル",
    "css_files": "CSS ファイル",
    "markdown_files": "Markdown ファイル",
    "renpy_files": "Ren'Py ファイル",
    "shell_files": "Shell ファイル",
    "all_files": "全てのファイル",
    "binary_file_title": "バイナリファイルが検出されました",
    "binary_file": "このドキュメントで異常な文字が検出されました。ドキュメントを開いてSlash Codeに生データを読み取りますか?\n警告: これによりSlash Codeの速度が低下する可能性があります。",
    "session_loaded": "セッションロード:",
    "error_b1": "ファイルの読み込みエラー:",
    "error_b2": "ディレクトリの読み込みエラー:"
    },
    "zh": {
    "gui_lang": "界面语言",
    "msys_install": "已安装 MSYS2。请通过 MSYS2 终端安装 MinGW: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "安装 MinGW-w64 失败:",
    "gcc_used": "使用的 GCC:",
    "gcc_error_a1": "安装 G++ 失败。",
    "gcc_error_a2": "无法检查 G++ 版本:",
    "gcc_error_b1": "未找到 G++ 编译器。中止 C++ 运行。",
    "gcc_error_b2": "安装 MinGW 编译器失败。\n",
    "cpp_usercode_written": "用户的 C++ 代码已写入至 ***。",
    "gcc_check_a1": "检查现有的 G++ 编译器...",
    "gcc_check_a2": "正在下载并安装 MinGW-w64...",
    "gcc_check_a3": "正在从 *** 下载 MinGW-w64...",
    "gcc_check_a4": "已下载 *** MB...",
    "gcc_check_a4_5": "共下载 *** MB。",
    "gcc_check_b1": "正在解压 MinGW-w64 存档...",
    "gcc_check_b2": "尝试安装/更新 G++ 编译器...",
    "gcc_compilation_attempt": "尝试使用标志 *** 进行编译:",
    "gcc_compilation_success": "编译成功，正在运行可执行文件...",
    "gcc_compilation_failed": "*** 的编译失败，错误如下:",
    "gcc_execution_finished": "执行成功结束。",
    "gcc_execution_error_a1": "尝试运行可执行文件时发生错误:",
    "gcc_mingw_addpath": "已将 MinGW-w64 bin 文件夹添加到 PATH:",
    "gcc_compiler_installed": "G++ 安装/更新成功。",
    "gcc_found_compiler_ver": "找到的 G++ 版本:",
    "gcc_sufficient_compiler_ver": "G++ 版本足够。",
    "gcc_old_compiler_ver": "您的 G++ 版本过旧，需要升级。",
    "gcc_mingw_extracted": "提取完成。MinGW 安装路径为:",
    "py7zr_installed": "py7zr 软件包安装成功。",
    "py7zr_error_a1": "未找到 py7zr 软件包，正在安装 py7zr...",
    "csc_compiler": "C# 编译器 (csc)",
    "cs_usercode_written": "用户的 C# 代码已写入至 ***。",
    "csc_error_a1": "未找到 C# 编译器 (csc)。正在尝试安装...\n",
    "csc_error_a2": "未找到 CSC 编译器且安装失败。中止 C# 运行。",
    "csc_autoinst_fail": "自动安装 C# 编译器失败。请手动安装 .NET SDK。\n",
    "csc_compiler_installed": "C# 编译器 (csc) 安装成功。\n",
    "csc_compiling_with": "正在使用以下配置编译:",
    "csc_compilation_success": "编译成功。\n",
    "csc_execution_finished": "执行成功结束。",
    "csc_execution_error_a1": "尝试运行可执行文件时发生错误:",
    "sh_platform_not_supported": "您的平台不支持运行 Shell 脚本。",
    "py_error_a1_title": "Python 版本不足",
    "py_error_a1": "请安装 Python 3.13 及以上版本。",
    "py_error_a2": "未找到 Python 解释器。",
    "py_error_a3": "无法解析 Python 版本。",
    "error_a1": "错误",
    "error_a2": "无法打开文件",
    "error_a3": "无法打开文件:\n",
    "error_a4": "无法写入文件:\n",
    "error_a5": "无法加载 Slash Code 源文件。原因:\n\n",
    "error_c0": "更新文件夹按钮时出错:",
    "error_c1": "更新菜单标签时出错:",
    "error_c2": "更新文件标签时出错:",
    "error_c3": "更新编辑标签时出错:",
    "error_c4": "更新主题标签时出错:",
    "error_c5": "更新运行标签时出错:",
    "error_c6": "更新视图标签时出错:",
    "error_c7": "更新语言标签时出错:",
    "error_c8": "更新 GUI 语言标签时出错:",
    "error_d1": "尝试执行文档代码时发生异常。原因如下:\n\n",
    "error_d1_5": "尝试写入并执行文档时发生异常。原因如下:\n\n",
    "error_d2": "编译器未正确安装。",
    "error_e1": "pip 安装 py7z 失败。原因:",
    "deleting_dirs": "正在删除目录:",
    "directory_del_not_found": "未找到要删除的目录。",
    "find": "查找",
    "find_query": "查找:",
    "find_all": "查找全部",
    "replace": "替换",
    "replace_query": "替换为:",
    "replace_all": "全部替换",
    "runner_not_found": " 未找到！\n",
    "install_suggest": "请先安装它。\n",
    "instructions": "说明:",
    "compilation_error": "编译错误:\n",
    "opened_in_browser": "已在默认浏览器打开。",
    "language_not_supported": "不支持该语言的执行。",
    "process_error": "进程错误:",
    "unexpected_error": "意外错误:",
    "cleanup_failed": "清理失败:",
    "file": "文件",
    "new": "新建",
    "open": "打开",
    "save": "保存",
    "toggle_new_file_saving": "切换新文件保存",
    "clean_temp_files": "清理临时文件",
    "clean_temp_directories": "清理临时目录",
    "fully_wipe_directories": "完全清除临时目录",
    "reboot_consolemode": "控制台模式重启",
    "exit": "退出",
    "edit": "编辑",
    "undo": "撤销",
    "redo": "重做",
    "language": "语言",
    "theme": "主题",
    "theme_light": "浅色",
    "theme_dark": "深色",
    "theme_dracula": "德古拉",
    "theme_monokai": "Monokai",
    "theme_night_owl": "夜猫子",
    "theme_shades_of_purple": "紫色渐变",
    "theme_high_contrast": "高对比度",
    "open_folder": "打开文件夹",
    "changed_language_to": "语言切换至 ",
    "view": "查看",
    "zoom_in": "放大",
    "zoom_out": "缩小",
    "show_sidebar": "显示侧边栏",
    "hide_sidebar": "隐藏侧边栏",
    "show_minimap": "显示小地图",
    "hide_minimap": "隐藏小地图",
    "show_debug_info": "显示调试信息",
    "hide_debug_info": "隐藏调试信息",
    "toggle_fullscreen": "切换全屏",
    "exit_fullscreen": "退出全屏",
    "run": "运行",
    "run_file": "运行文件",
    "sc_output": "SC-输出",
    "output_sc_title": "-- Slash Code 文本编辑器 | 文件执行的 SC-输出 --",
    "save_output_text": "保存输出文本",
    "highlighting_as": "高亮为:",
    "plaintext": "纯文本",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell 脚本",
    "python_files": "Python 文件",
    "javascript_files": "JavaScript 文件",
    "html_files": "HTML 文件",
    "c_files": "C 文件",
    "cpp_files": "C++ 文件",
    "header_files": "头文件",
    "text_files": "文本文件",
    "cs_files": "C# 文件",
    "css_files": "CSS 文件",
    "markdown_files": "Markdown 文件",
    "renpy_files": "Ren'Py 文件",
    "shell_files": "Shell 文件",
    "all_files": "所有文件",
    "binary_file_title": "检测到二进制文件",
    "binary_file": "检测到文档中有异常字符，是否打开并让 Slash Code 读取原始数据？\n警告:这可能会降低 Slash Code 的速度。",
    "session_loaded": "会话已加载:",
    "error_b1": "加载文件时出错:",
    "error_b2": "加载目录时出错:"
    },
    "ko": {
    "gui_lang": "GUI 언어",
    "msys_install": "MSYS2가 설치되었습니다. MSYS2 셸에서 MinGW를 설치하십시오: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "MinGW-w64 설치 실패:",
    "gcc_used": "사용된 GCC:",
    "gcc_error_a1": "G++ 설치 실패.",
    "gcc_error_a2": "G++ 버전 확인 실패:",
    "gcc_error_b1": "G++ 컴파일러를 찾을 수 없습니다. C++ 실행 중단.",
    "gcc_error_b2": "MinGW 컴파일러 설치 실패.\n",
    "cpp_usercode_written": "사용자 C++ 코드가 ***에 작성되었습니다.",
    "gcc_check_a1": "기존 G++ 컴파일러 확인 중...",
    "gcc_check_a2": "MinGW-w64 다운로드 및 설치 중...",
    "gcc_check_a3": "***에서 MinGW-w64 다운로드 중...",
    "gcc_check_a4": "*** MB 다운로드 완료...",
    "gcc_check_a4_5": "총 *** MB 다운로드 완료.",
    "gcc_check_b1": "MinGW-w64 아카이브 압축 해제 중...",
    "gcc_check_b2": "G++ 컴파일러 설치/업데이트 시도 중...",
    "gcc_compilation_attempt": "*** 플래그로 컴파일 시도 중:",
    "gcc_compilation_success": "컴파일 성공, 실행 파일 실행 중...",
    "gcc_compilation_failed": "*** 컴파일 실패, 오류:",
    "gcc_execution_finished": "실행 성공적으로 완료.",
    "gcc_execution_error_a1": "실행 파일 실행 중 오류 발생:",
    "gcc_mingw_addpath": "MinGW-w64 bin 폴더가 PATH에 추가되었습니다:",
    "gcc_compiler_installed": "G++가 성공적으로 설치/업데이트되었습니다.",
    "gcc_found_compiler_ver": "발견된 G++ 버전:",
    "gcc_sufficient_compiler_ver": "G++ 버전이 충분합니다.",
    "gcc_old_compiler_ver": "G++ 버전이 너무 오래되어 업그레이드가 필요합니다.",
    "gcc_mingw_extracted": "압축 해제 완료. MinGW가 다음 위치에 설치되었습니다:",
    "py7zr_installed": "py7zr 패키지가 성공적으로 설치되었습니다.",
    "py7zr_error_a1": "py7zr 패키지를 찾을 수 없어 설치 중...",
    "csc_compiler": "C# 컴파일러 (csc)",
    "cs_usercode_written": "사용자 C# 코드가 ***에 작성되었습니다.",
    "csc_error_a1": "C# 컴파일러 (csc)를 찾을 수 없습니다. 설치 시도 중...\n",
    "csc_error_a2": "CSC 컴파일러를 찾을 수 없고 설치에 실패했습니다. C# 실행 중단.",
    "csc_autoinst_fail": "C# 컴파일러 자동 설치 실패. .NET SDK를 수동으로 설치하십시오.\n",
    "csc_compiler_installed": "C# 컴파일러 (csc) 설치 성공.\n",
    "csc_compiling_with": "다음으로 컴파일 중:",
    "csc_compilation_success": "컴파일 성공.\n",
    "csc_execution_finished": "실행 성공적으로 완료.",
    "csc_execution_error_a1": "실행 파일 실행 시 오류 발생:",
    "sh_platform_not_supported": "사용 중인 플랫폼은 Shell 스크립트 실행을 지원하지 않습니다.",
    "py_error_a1_title": "Python 버전 부족",
    "py_error_a1": "Python 3.13 이상을 설치하십시오.",
    "py_error_a2": "Python 인터프리터를 찾을 수 없습니다.",
    "py_error_a3": "Python 버전을 해석할 수 없습니다.",
    "error_a1": "오류",
    "error_a2": "파일을 열 수 없습니다",
    "error_a3": "파일을 열 수 없습니다:\n",
    "error_a4": "파일에 쓸 수 없습니다:\n",
    "error_a5": "Slash Code 소스 파일을 로드할 수 없습니다. 이유:\n\n",
    "error_c0": "폴더 버튼 업데이트 오류:",
    "error_c1": "메뉴 레이블 업데이트 오류:",
    "error_c2": "파일 레이블 업데이트 오류:",
    "error_c3": "편집 레이블 업데이트 오류:",
    "error_c4": "테마 레이블 업데이트 오류:",
    "error_c5": "실행 레이블 업데이트 오류:",
    "error_c6": "보기 레이블 업데이트 오류:",
    "error_c7": "언어 레이블 업데이트 오류:",
    "error_c8": "GUI 언어 레이블 업데이트 오류:",
    "error_d1": "문서 코드를 실행하는 동안 예외가 발생했습니다. 이유:\n\n",
    "error_d1_5": "문서를 쓰고 실행하는 동안 예외가 발생했습니다. 이유:\n\n",
    "error_d2": "컴파일러가 올바르게 설치되지 않았습니다.",
    "error_e1": "pip가 py7z 설치에 실패했습니다. 이유:",
    "deleting_dirs": "디렉터리 삭제 중: ",
    "directory_del_not_found": "삭제할 디렉터리를 찾을 수 없습니다.",
    "find": "찾기",
    "find_query": "찾기:",
    "find_all": "모두 찾기",
    "replace": "바꾸기",
    "replace_query": "바꿀 내용:",
    "replace_all": "모두 바꾸기",
    "runner_not_found": " 찾을 수 없습니다!\n",
    "install_suggest": "먼저 설치해 주세요.\n",
    "instructions": "설명: ",
    "compilation_error": "컴파일 오류:\n",
    "opened_in_browser": "기본 브라우저에서 열림.",
    "language_not_supported": "실행할 수 없는 언어입니다.",
    "process_error": "프로세스 오류: ",
    "unexpected_error": "예상치 못한 오류: ",
    "cleanup_failed": "정리 실패: ",
    "file": "파일",
    "new": "새 파일",
    "open": "열기",
    "save": "저장",
    "toggle_new_file_saving": "새 파일 저장 토글",
    "clean_temp_files": "임시 파일 정리",
    "clean_temp_directories": "임시 디렉터리 정리",
    "fully_wipe_directories": "임시 디렉터리 완전 삭제",
    "reboot_consolemode": "콘솔 모드에서 재부팅",
    "exit": "종료",
    "edit": "편집",
    "undo": "실행 취소",
    "redo": "다시 실행",
    "language": "언어",
    "theme": "테마",
    "theme_light": "라이트",
    "theme_dark": "다크",
    "theme_dracula": "드라큘라",
    "theme_monokai": "모노카이",
    "theme_night_owl": "나이트 아울",
    "theme_shades_of_purple": "보라색 계열",
    "theme_high_contrast": "고대비",
    "open_folder": "폴더 열기",
    "changed_language_to": "언어 변경됨: ",
    "view": "보기",
    "zoom_in": "확대",
    "zoom_out": "축소",
    "show_sidebar": "사이드바 표시",
    "hide_sidebar": "사이드바 숨기기",
    "show_minimap": "미니맵 표시",
    "hide_minimap": "미니맵 숨기기",
    "show_debug_info": "디버그 정보 표시",
    "hide_debug_info": "디버그 정보 숨기기",
    "toggle_fullscreen": "전체 화면 전환",
    "exit_fullscreen": "전체 화면 종료",
    "run": "실행",
    "run_file": "파일 실행",
    "sc_output": "SC-출력",
    "output_sc_title": "-- Slash Code 텍스트 에디터 | 파일 실행용 SC-출력 --",
    "save_output_text": "출력 텍스트 저장",
    "highlighting_as": "하이라이트 모드: ",
    "plaintext": "일반 텍스트",
    "python": "파이썬",
    "javascript": "자바스크립트",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "마크다운",
    "renpy": "Ren'Py",
    "shell": "Shell 스크립트",
    "python_files": "파이썬 파일",
    "javascript_files": "자바스크립트 파일",
    "html_files": "HTML 파일",
    "c_files": "C 파일",
    "cpp_files": "C++ 파일",
    "header_files": "헤더 파일",
    "text_files": "텍스트 파일",
    "cs_files": "C# 파일",
    "css_files": "CSS 파일",
    "markdown_files": "마크다운 파일",
    "renpy_files": "Ren'Py 파일",
    "shell_files": "Shell 파일",
    "all_files": "모든 파일",
    "binary_file_title": "바이너리 파일 감지됨",
    "binary_file": "이 문서에서 이상한 문자가 감지되었습니다. 열어서 Slash Code가 원시 데이터를 읽도록 하시겠습니까?\n경고: 이로 인해 Slash Code가 느려질 수 있습니다.",
    "session_loaded": "세션 로드됨:",
    "error_b1": "파일 로드 중 오류 발생: ",
    "error_b2": "디렉터리 로드 중 오류 발생: "
    },
    "ar": {
    "gui_lang": "لغة واجهة المستخدم",
    "msys_install": "تم تثبيت MSYS2. يرجى تثبيت MinGW عبر واجهة MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "فشل تثبيت MinGW-w64 بنجاح:",
    "gcc_used": "استخدام GCC:",
    "gcc_error_a1": "فشل تثبيت G++.",
    "gcc_error_a2": "فشل التحقق من إصدار G++:",
    "gcc_error_b1": "لم يتم العثور على مترجم G++. تم إلغاء تشغيل C++.",
    "gcc_error_b2": "فشل تثبيت مترجم MinGW.\n",
    "cpp_usercode_written": "تم كتابة كود C++ الخاص بالمستخدم إلى ***.",
    "gcc_check_a1": "التحقق من وجود مترجم G++ الحالي...",
    "gcc_check_a2": "جاري تنزيل وتثبيت MinGW-w64...",
    "gcc_check_a3": "جاري تنزيل MinGW-w64 من ***...",
    "gcc_check_a4": "*** ميجابايت تم تنزيلها حتى الآن...",
    "gcc_check_a4_5": "تم تنزيل *** ميجابايت إجمالاً.",
    "gcc_check_b1": "جاري استخراج أرشيف MinGW-w64...",
    "gcc_check_b2": "محاولة تثبيت/تحديث مترجم G++...",
    "gcc_compilation_attempt": "محاولة الترجمة مع الخيار ***:",
    "gcc_compilation_success": "تمت الترجمة بنجاح، يجري تشغيل الملف القابل للتنفيذ...",
    "gcc_compilation_failed": "فشلت الترجمة ل*** مع وجود أخطاء:",
    "gcc_execution_finished": "انتهى التنفيذ بنجاح.",
    "gcc_execution_error_a1": "حدث خطأ أثناء محاولة تشغيل الملف القابل للتنفيذ:",
    "gcc_mingw_addpath": "تمت إضافة مجلد MinGW-w64 bin إلى PATH:",
    "gcc_compiler_installed": "تم تثبيت/تحديث G++ بنجاح.",
    "gcc_found_compiler_ver": "تم العثور على إصدار G++:",
    "gcc_sufficient_compiler_ver": "إصدار G++ كافٍ.",
    "gcc_old_compiler_ver": "إصدار G++ لديك قديم جداً ويحتاج إلى التحديث.",
    "gcc_mingw_extracted": "اكتمل الاستخراج. تم تثبيت MinGW في:",
    "py7zr_installed": "تم تثبيت حزمة py7zr بنجاح.",
    "csc_compiler": "مترجم C# (csc)",
    "cs_usercode_written": "تم كتابة كود C# الخاص بالمستخدم إلى ***.",
    "csc_error_a1": "مترجم C# (csc) غير موجود. جارٍ المحاولة للتثبيت...\n",
    "csc_error_a2": "لم يتم العثور على مترجم CSC وفشل التثبيت. تم إيقاف تشغيل C#.",
    "csc_autoinst_fail": "فشل التثبيت التلقائي لمترجم C#. يرجى تثبيت .NET SDK يدوياً.\n",
    "csc_compiler_installed": "تم تثبيت مترجم C# (csc) بنجاح.\n",
    "csc_compiling_with": "جارٍ الترجمة باستخدام:",
    "csc_compilation_success": "تمت الترجمة بنجاح.\n",
    "csc_execution_finished": "انتهى التنفيذ بنجاح.",
    "csc_execution_error_a1": "حدث خطأ أثناء محاولة تشغيل الملف القابل للتنفيذ:",
    "sh_platform_not_supported": "منصتك غير مدعومة لتشغيل سكريبتات Shell Script.",
    "py_error_a1_title": "إصدار Python غير كافٍ",
    "py_error_a1": "يرجى تثبيت Python 3.13 أو أحدث.",
    "py_error_a2": "تعذر العثور على مفسر Python.",
    "py_error_a3": "تعذر تحليل إصدار Python.",
    "error_a1": "خطأ",
    "error_a2": "تعذر فتح الملف",
    "error_a3": "تعذر فتح الملف:\n",
    "error_a4": "تعذر الكتابة إلى الملف:\n",
    "error_a5": "تعذر تحميل ملف مصدر Slash Code. السبب:\n\n",
    "error_c0": "خطأ في تحديث زر المجلد:",
    "error_c1": "خطأ في تحديث وسم القائمة:",
    "error_c2": "خطأ في تحديث وسم الملف:",
    "error_c3": "خطأ في تحديث وسم التحرير:",
    "error_c4": "خطأ في تحديث وسم السمة:",
    "error_c5": "خطأ في تحديث وسم التشغيل:",
    "error_c6": "خطأ في تحديث وسم العرض:",
    "error_c7": "خطأ في تحديث وسم اللغة:",
    "error_c8": "خطأ في تحديث وسم لغة الواجهة:",
    "error_d1": "حدث استثناء أثناء محاولة تنفيذ كود المستند. السبب هو:\n\n",
    "error_d1_5": "حدث استثناء أثناء محاولة الكتابة والتنفيذ للمستند. السبب هو:\n\n",
    "error_d2": "فشل تثبيت المترجم بشكل صحيح.",
    "deleting_dirs": "جار حذف المجلد/المجلدات:",
    "error_e1": "فشل pip في تثبيت py7z. السبب:",
    "directory_del_not_found": "لم يتم العثور على أي مجلدات للحذف.",
    "find": "بحث",
    "find_query": "بحث عن:",
    "find_all": "البحث الكل",
    "replace": "استبدال",
    "replace_query": "استبدال بـ:",
    "replace_all": "استبدال الكل",
    "runner_not_found": " غير موجود!\n",
    "install_suggest": "يرجى تثبيته أولاً.\n",
    "instructions": "تعليمات: ",
    "compilation_error": "خطأ في الترجمة:\n",
    "opened_in_browser": "تم الفتح في المتصفح الافتراضي.",
    "language_not_supported": "اللغة غير مدعومة للتنفيذ.",
    "process_error": "خطأ في العملية: ",
    "unexpected_error": "خطأ غير متوقع: ",
    "cleanup_failed": "فشل التنظيف: ",
    "file": "ملف",
    "new": "جديد",
    "open": "فتح",
    "save": "حفظ",
    "toggle_new_file_saving": "تبديل حفظ الملف الجديد",
    "clean_temp_files": "تنظيف الملفات المؤقتة",
    "clean_temp_directories": "تنظيف الأدلة المؤقتة بالكامل",
    "fully_wipe_directories": "مسح الأدلة المؤقتة بالكامل",
    "reboot_consolemode": "إعادة التشغيل في وضع الكونسول",
    "exit": "خروج",
    "edit": "تحرير",
    "undo": "تراجع",
    "redo": "إعادة",
    "language": "اللغة",
    "theme": "الثيم",
    "theme_light": "فاتح",
    "theme_dark": "داكن",
    "theme_dracula": "دراكولا",
    "theme_monokai": "مونوكاي",
    "theme_night_owl": "البومة الليلية",
    "theme_shades_of_purple": "درجات اللون الأرجواني",
    "theme_high_contrast": "تباين عالي",
    "open_folder": "فتح المجلد",
    "changed_language_to": "تم تغيير اللغة إلى ",
    "view": "عرض",
    "zoom_in": "تكبير",
    "zoom_out": "تصغير",
    "show_sidebar": "إظهار الشريط الجانبي",
    "hide_sidebar": "إخفاء الشريط الجانبي",
    "show_minimap": "إظهار الخريطة المصغرة",
    "hide_minimap": "إخفاء الخريطة المصغرة",
    "show_debug_info": "إظهار معلومات التصحيح",
    "hide_debug_info": "إخفاء معلومات التصحيح",
    "toggle_fullscreen": "تبديل ملء الشاشة",
    "exit_fullscreen": "خروج من ملء الشاشة",
    "run": "تشغيل",
    "run_file": "تشغيل الملف",
    "sc_output": "مخرجات SC",
    "output_sc_title": "-- محرر نصوص Slash Code | مخرجات SC لتشغيل الملفات --",
    "save_output_text": "حفظ نص المخرجات",
    "highlighting_as": "تظليل كالتالي: ",
    "plaintext": "نص عادي",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "نص Shell",
    "python_files": "ملفات Python",
    "javascript_files": "ملفات JavaScript",
    "html_files": "ملفات HTML",
    "c_files": "ملفات C",
    "cpp_files": "ملفات C++",
    "header_files": "ملفات الرأس",
    "text_files": "ملفات نصية",
    "cs_files": "ملفات C#",
    "css_files": "ملفات CSS",
    "markdown_files": "ملفات Markdown",
    "renpy_files": "ملفات Ren'Py",
    "renpy_files": "ملفات Shell",
    "all_files": "جميع الملفات",
    "binary_file_title": "تم اكتشاف ملف ثنائي",
    "binary_file": "تم اكتشاف أحرف غير مألوفة في هذا المستند. هل ترغب في فتحه وقراءة البيانات الخام بواسطة Slash Code؟\nتحذير: قد يبطئ هذا البرنامج.",
    "session_loaded": "تم تحميل الجلسة:",
    "error_b1": "خطأ أثناء تحميل الملف: ",
    "error_b2": "خطأ أثناء تحميل الدليل: "
    }
}

class GUITranslate:
    def __init__(self, lang="en"):
        self.lang = lang
        self.load_lang()
        
    def load_lang(self):
        """
        Loads the language that's been saved from the previous session inside the `.json` language file.
        """
        slash_dir = os.path.expanduser('~/.slashcode')
        os.makedirs(os.path.join(slash_dir, "lang"), exist_ok=True)
        lang_file = os.path.join(slash_dir, f'lang/{self.lang}.json')
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding="utf-8") as f:
                    self.data = json.load(f)
                    return
            except Exception:
                pass
        self.data = GUILANGS.get(self.lang, {})
                
    def get(self, key):
        """
        Returns the key value for the current language key.
        """
        return self.data.get(key, key)
    
    def set_language(self, lang):
        """
        Sets the language using `load_lang()` and passes `self.lang` to the `lang` parameter.
        """
        self.lang = lang
        self.load_lang()
        
translate = GUITranslate()
lang_var = tk.StringVar(value=translate.lang)

def show_generror(exc):
    print(f"{translate.get('error_a1')}:\n\n{exc}")

url = "https://raw.githubusercontent.com/clydezzz-sleepy/Slash-Code/refs/heads/main/slash.ico"
alt_url = "https://i.imgur.com/HqnIx28.png"
filename = "slash.ico"
alt_filename = "slash.png"
icon_dir = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "ico")
icon_path = os.path.join(icon_dir, filename)
alt_icon_path = os.path.join(icon_dir, alt_filename)
if not os.path.exists(icon_path):
    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=header, timeout=5)
        response.raise_for_status()
        os.makedirs(icon_dir, exist_ok=True)
        with open(icon_path, "wb") as f:
            f.write(response.content)
        alt_response = requests.get(alt_url, headers=header, timeout=5)
        alt_response.raise_for_status()
    except Exception as e:
        show_generror(e)
lang_icons_dir = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "img")
os.makedirs(lang_icons_dir, exist_ok=True)
icon_meta = {
    'en': ("https://i.imgur.com/8dhbFPz.png", os.path.join(lang_icons_dir, "en.png")),
    'nl': ("https://i.imgur.com/YP1GxGK.png", os.path.join(lang_icons_dir, "nl.png")),
    'de': ("https://i.imgur.com/5U6hklL.png", os.path.join(lang_icons_dir, "de.png")),
    'es': ("https://i.imgur.com/6cmIOgg.png", os.path.join(lang_icons_dir, "es.png")),
    'it': ("https://i.imgur.com/bzHSS22.png", os.path.join(lang_icons_dir, "it.png")),
    'fr': ("https://i.imgur.com/21QFuei.png", os.path.join(lang_icons_dir, "fr.png")),
    'jp': ("https://i.imgur.com/vUE262x.png", os.path.join(lang_icons_dir, "jp.png")),
    'zh': ("https://i.imgur.com/2n6Mk8I.png", os.path.join(lang_icons_dir, "zh.png")),
    'ko': ("https://i.imgur.com/EsY4wrL.png", os.path.join(lang_icons_dir, "ko.png")),
    'ar': ("https://i.imgur.com/USSgURT.png", os.path.join(lang_icons_dir, "ar.png"))
}

language_icons = {}

for lang, (url, path) in icon_meta.items():
    if not os.path.exists(path):
        try:
            header = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=header, timeout=5)
            response.raise_for_status()
            with open(path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            language_icons[lang] = tk.PhotoImage(width=16, height=16)
            continue
    try:
        pil_img = Image.open(path)
        language_icons[lang] = ImageTk.PhotoImage(pil_img)
    except Exception as e:
        show_generror(e)
        language_icons[lang] = tk.PhotoImage(width=16, height=16)

if os.name == "nt":
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass
else:
    try:
        icon = tk.PhotoImage(file=os.path.abspath("slash.png"))
        root.iconphoto(True, icon)
    except Exception:
        pass

language_var = tk.StringVar(value='plaintext')
GUILANGS = {
    "en": {
    "gui_lang": "GUI Language",
    "msys_install": "MSYS2 installed. Please install MinGW via MSYS2 shell: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Failed to install MinGW-w64:",
    "gcc_used": "GCC used:",
    "gcc_error_a1": "Installing G++ failed.",
    "gcc_error_a2": "Failed to check G++ version:",
    "gcc_error_b1": "G++ compiler not found. Aborting C++ run.",
    "gcc_error_b2": "Failed to install MinGW compiler.\n",
    "cpp_usercode_written": "User's C++ code written to ***.",
    "gcc_check_a1": "Checking for existing G++ compiler...",
    "gcc_check_a2": "Downloading and installing MinGW-w64...",
    "gcc_check_a3": "Downloading MinGW-w64 from ***...", # This will eventually be f"{translate.get("gcc_check_a3").replace("***", mingw_url)}".
    "gcc_check_a4": "Downloaded *** MB so far...", # The same with this one, as specified above (and also all the other ones that contain '***').
    "gcc_check_a4_5": "Downloaded *** MB in total.",
    "gcc_check_b1": "Extracting MinGW-w64 archive...",
    "gcc_check_b2": "Attempting to install/update G++ compiler...",
    "gcc_compilation_attempt": "Attempting compilation with flag ***:",
    "gcc_compilation_success": "Compilation succeeded, running executable...",
    "gcc_compilation_failed": "Compilation failed for *** with errors:",
    "gcc_execution_finished": "Execution finished successfully.",
    "gcc_execution_error_a1": "An error has occurred while attempting to run the executable:",
    "gcc_mingw_addpath": "MinGW-w64 bin folder added to PATH:",
    "gcc_compiler_installed": "G++ installed/updated successfully.",
    "gcc_found_compiler_ver": "Found G++ version:",
    "gcc_sufficient_compiler_ver": "The G++ version is sufficient.",
    "gcc_old_compiler_ver": "Your G++ version is too old and needs to be upgraded.",
    "gcc_mingw_extracted": "Extraction complete. MinGW installed at:",
    "py7zr_installed": "The py7zr package was successfully installed.",
    "py7zr_error_a1": "The package py7zr was not found, installing py7zr package...",
    "csc_compiler": "C# Compiler (csc)",
    "cs_usercode_written": "User C# code written to ***.",
    "csc_error_a1": "C# Compiler (csc) not found. Attempting to install...\n",
    "csc_error_a2": "CSC compiler not found and installation failed. Aborting C# run.",
    "csc_autoinst_fail": "Failed to auto-install C# compiler. Please install the .NET SDK manually.\n",
    "csc_compiler_installed": "C# Compiler (csc) installed successfully.\n",
    "csc_compiling_with": "Compiling with:",
    "csc_compilation_success": "Compilation succeeded.\n",
    "csc_execution_finished": "Execution finished successfully.",
    "csc_execution_error_a1": "An error has occurred while attempting to run the executable:",
    "sh_platform_not_supported": "Your platform isn't supported to run Shell Script scripts.",
    "py_error_a1_title": "Insufficient Python Version",
    "py_error_a1": "Please install Python 3.13+.",
    "py_error_a2": "Python interpreter not found.",
    "py_error_a3": "Could not parse Python version.",
    "error_a1": "Error",
    "error_a2": "Could not open file",
    "error_a3": "Could not open file:\n",
    "error_a4": "Could not write to file:\n",
    "error_a5": "Could not load the Slash Code source file. Reason:\n\n",
    "error_c0": "Folder button update error:",
    "error_c1": "Menu label update error:",
    "error_c2": "File label update error:",
    "error_c3": "Edit label update error:",
    "error_c4": "Theme label update error:",
    "error_c5": "Run label update error:",
    "error_c6": "View label update error:",
    "error_c7": "Language label update error:",
    "error_c8": "GUI language label update error:",
    "error_d1": "An exception has occurred while attempting to execute the document's code. The reason for this is:\n\n",
    "error_d1_5": "An exception has occurred while attempting to write to and execute the document. The reason for this is:\n\n",
    "error_d2": "The compiler failed to install properly.",
    "error_e1": "pip failed to install py7z. Reason:",
    "deleting_dirs": "Deleting director(y/ies): ",
    "directory_del_not_found": "No director(y/ies) was/were found to delete.",
    "find": "Find",
    "find_query": "Find:",
    "find_all": "Find All",
    "replace": "Replace",
    "replace_query": "Replace:",
    "replace_all": "Replace All",
    "runner_not_found": " not found!\n",
    "install_suggest": "Please install it first.\n",
    "instructions": "Instructions: ",
    "compilation_error": "Compilation Error:\n",
    "opened_in_browser": "Opened in default browser.",
    "language_not_supported": "Language not supported for execution.",
    "process_error": "Process Error: ",
    "unexpected_error": "Unexpected Error: ",
    "cleanup_failed": "Cleanup failed: ",
    "file": "File",
    "new": "New",
    "open": "Open",
    "save": "Save",
    "toggle_new_file_saving": "Toggle New File Saving",
    "clean_temp_files": "Clean Temporary Files",
    "clean_temp_directories": "Clean Temporary Directories",
    "fully_wipe_directories": "Fully Wipe Temporary Directories",
    "reboot_consolemode": "Reboot In Console Mode",
    "exit": "Exit",
    "edit": "Edit",
    "undo": "Undo",
    "redo": "Redo",
    "language": "Language",
    "theme": "Theme",
    "theme_light": "Light",
    "theme_dark": "Dark",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Night Owl",
    "theme_shades_of_purple": "Shades Of Purple",
    "theme_high_contrast": "High Contrast",
    "open_folder": "Open Folder",
    "changed_language_to": "Changed language to ",
    "view": "View",
    "zoom_in": "Zoom In",
    "zoom_out": "Zoom Out",
    "show_sidebar": "Show Sidebar",
    "hide_sidebar": "Hide Sidebar",
    "show_minimap": "Show Minimap",
    "hide_minimap": "Hide Minimap",
    "show_debug_info": "Show Debug Info",
    "hide_debug_info": "Hide Debug Info",
    "toggle_fullscreen": "Toggle Fullscreen",
    "exit_fullscreen": "Exit Fullscreen",
    "run": "Run",
    "run_file": "Run File",
    "sc_output": "SC-Output",
    "output_sc_title": "-- Slash Code Text Editor | SC-Output for File Execution --",
    "save_output_text": "Save Output Text",
    "highlighting_as": "Highlighting as: ",
    "plaintext": "Plain Text",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell Script",
    "python_files": "Python Files",
    "javascript_files": "JavaScript Files",
    "html_files": "HTML Files",
    "c_files": "C Files",
    "cpp_files": "C++ Files",
    "header_files": "Header Files",
    "text_files": "Text Files",
    "cs_files": "C# Files",
    "css_files": "CSS Files",
    "markdown_files": "Markdown Files",
    "renpy_files": "Ren'Py Files",
    "shell_files": "Shell Files",
    "all_files": "All Files",
    "binary_file_title": "Binary File Detected",
    "binary_file": "Unusual characters have been detected in this document, would you like to open it and have Slash Code read raw data?\nWarning, this likely will slow down Slash Code.",
    "session_loaded": "Session loaded:",
    "error_b1": "Error loading file: ",
    "error_b2": "Error loading directory: "
    },
    
    "nl": {
    "gui_lang": "GUI Taal",
    "msys_install": "MSYS2 is geinstalleerd. Installeer alstublieft MinGW via de MSYS2 shell: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Kon niet MinGW-w64 succesvol installeren:",
    "gcc_used": "GCC gebruikt:",
    "gcc_error_a1": "Installatie van G++ mislukt.",
    "gcc_error_a2": "Controleren van G++ versie mislukt:",
    "gcc_error_b1": "G++ compiler niet gevonden. C++ uitvoering geannuleerd.",
    "gcc_error_b2": "Installatie van MinGW compiler mislukt.\n",
    "cpp_usercode_written": "Gebruikers C++ code weggeschreven naar ***.",
    "gcc_check_a1": "Controleren op bestaande G++ compiler...",
    "gcc_check_a2": "MinGW-w64 wordt gedownload en geïnstalleerd...",
    "gcc_check_a3": "MinGW-w64 wordt gedownload van ***...",
    "gcc_check_a4": "Tot nu toe *** MB gedownload...",
    "gcc_check_a4_5": "In totaal *** MB gedownload.",
    "gcc_check_b1": "MinGW-w64 archief wordt uitgepakt...",
    "gcc_check_b2": "Poging tot installatie/update van G++ compiler...",
    "gcc_compilation_attempt": "Proberen te compileren met vlag ***:",
    "gcc_compilation_success": "Compilatie geslaagd, uitvoerbaar bestand wordt gestart...",
    "gcc_compilation_failed": "Compilatie mislukt voor *** met foutmeldingen:",
    "gcc_execution_finished": "Uitvoering succesvol afgerond.",
    "gcc_execution_error_a1": "Er is een fout opgetreden bij het uitvoeren van het programma:",
    "gcc_mingw_addpath": "MinGW-w64 bin map toegevoegd aan PATH:",
    "gcc_compiler_installed": "G++ succesvol geïnstalleerd/geüpdatet.",
    "gcc_found_compiler_ver": "G++ versie gevonden:",
    "gcc_sufficient_compiler_ver": "De G++ versie is voldoende.",
    "gcc_old_compiler_ver": "Je G++ versie is te oud en moet worden bijgewerkt.",
    "gcc_mingw_extracted": "Uitpakken voltooid. MinGW geïnstalleerd op:",
    "py7zr_installed": "Het py7zr pakket is succesvol geïnstalleerd.",
    "csc_compiler": "C# Compiler (csc)",
    "cs_usercode_written": "Gebruiker's C# code weggeschreven naar ***.",
    "csc_error_a1": "C# Compiler (csc) niet gevonden. Poging tot installatie...\n",
    "csc_error_a2": "CSC compiler niet gevonden en installatie mislukt. C# uitvoering afgebroken.",
    "csc_autoinst_fail": "Automatische installatie van C# compiler mislukt. Installeer de .NET SDK handmatig.\n",
    "csc_compiler_installed": "C# Compiler (csc) succesvol geïnstalleerd.\n",
    "csc_compiling_with": "Compileren met:",
    "csc_compilation_success": "Compilatie geslaagd.\n",
    "csc_execution_finished": "Uitvoering succesvol afgerond.",
    "csc_execution_error_a1": "Er is een fout opgetreden bij het uitvoeren van het programma:",
    "sh_platform_not_supported": "Uw platform wordt niet ondersteund voor het uitvoeren van Shell Script scripts.",
    "py_error_a1_title": "Onvoldoende Python-versie",
    "py_error_a1": "Installeer Python 3.13+.",
    "py_error_a2": "Python-interpreter niet gevonden.",
    "py_error_a3": "Kan Python-versie niet parseren.",
    "error_a1": "Fout",
    "error_a2": "Kon niet bestand openen",
    "error_a3": "Kon niet bestand openen:\n",
    "error_a4": "Kon niet schrijven naar bestand:\n",
    "error_a5": "Kan het bronbestand van Slash Code niet laden. Reden:\n\n",
    "error_c0": "Fout bij het bijwerken van de mapknop:",
    "error_c1": "Fout bij het bijwerken van het menulabel:",
    "error_c2": "Fout bij het bijwerken van het bestandslabel:",
    "error_c3": "Fout bij het bijwerken van het label:",
    "error_c4": "Fout bij het bijwerken van het themalabel:",
    "error_c5": "Fout bij het uitvoeren van de labelupdate:",
    "error_c6": "Fout bij het bijwerken van het label weergeven:",
    "error_c7": "Fout bij het bijwerken van het taallabel:",
    "error_c8": "Fout bij het bijwerken van het GUI-taallabel:",
    "error_d1": "Er is een exceptie opgetreden bij het uitvoeren van de code in het document. De reden hiervoor is:\n\n",
    "error_d1_5": "Er is een fout opgetreden tijdens het schrijven naar en uitvoeren van het document. De reden hiervoor is:\n\n",
    "error_d2": "De compiler is niet correct geïnstalleerd.",
    "deleting_dirs": "Map(pen) verwijderen:",
    "error_e1": "pip kon py7z niet installeren. Reden:",
    "directory_del_not_found": "Er is/zijn geen map(pen) gevonden om te verwijderen.",
    "find": "Vind",
    "find_query": "Vind:",
    "find_all": "Vind Alle",
    "replace": "Vervang",
    "replace_query": "Vervang:",
    "replace_all": "Vervang Alle",
    "runner_not_found": " niet gevonden!\n",
    "install_suggest": "Installeer het alstublieft eerst.\n",
    "instructions": "Instructies: ",
    "compilation_error": "Compilatie fout:\n",
    "opened_in_browser": "Geopend in de standaard browser.",
    "language_not_supported": "Taal niet gesteund voor executie.",
    "process_error": "Proces fout: ",
    "unexpected_error": "Onverwachte fout: ",
    "cleanup_failed": "Schoonmaking gefaald: ",
    "file": "Bestand",
    "new": "Nieuw",
    "open": "Open",
    "save": "Opslaan",
    "toggle_new_file_saving": "Nieuw Bestand Opslaan Inschakelen",
    "clean_temp_files": "Temporaire Bestanden Wissen",
    "clean_temp_directories": "Temporaire Mappen Volledig Wissen",
    "fully_wipe_directories": "Temporaire Mappen Wissen",
    "reboot_consolemode": "Opnieuw Opstarten In Consolemodus",
    "exit": "Verlaten",
    "edit": "Bewerken",
    "undo": "Ongedaan Maken",
    "redo": "Opnieuw Doen",
    "language": "Taal",
    "theme": "Thema",
    "theme_light": "Licht",
    "theme_dark": "Donker",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Nacht Uil",
    "theme_shades_of_purple": "Tinten Van Paars",
    "theme_high_contrast": "Hoog Contrast",
    "open_folder": "Open Map",
    "changed_language_to": "Taal veranderd naar ",
    "view": "Kijken",
    "zoom_in": "Inzoomen",
    "zoom_out": "Uitzoomen",
    "show_sidebar": "Maak Zijbalk Zichtbaar",
    "hide_sidebar": "Maak Zijbalk Onzichtbaar",
    "show_minimap": "Maak Minikaart Zichtbaar",
    "hide_minimap": "Maak Minikaart Onzichtbaar",
    "show_debug_info": "Toon foutopsporingsinfo",
    "hide_debug_info": "Verberg foutopsporingsinfo",
    "toggle_fullscreen": "Volledig Scherm Inschakelen",
    "exit_fullscreen": "Volledig Scherm Verlaten",
    "run": "Uitvoeren",
    "run_file": "Bestand Uitvoeren",
    "sc_output": "SC-Uitvoer",
    "output_sc_title": "-- Slash Code Teksteditor | SC-Uitvoer voor bestandsuitvoering --",
    "save_output_text": "Uitvoertekst opslaan",
    "highlighting_as": "Wordt gemarkeerd als: ",
    "plaintext": "Platte Text",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell Script",
    "python_files": "Python Bestanden",
    "javascript_files": "JavaScript Bestanden",
    "html_files": "HTML Bestanden",
    "c_files": "C Bestanden",
    "cpp_files": "C++ Bestanden",
    "header_files": "Headerbestanden",
    "text_files": "Tekstbestanden",
    "cs_files": "C# Bestanden",
    "css_files": "CSS Bestanden",
    "markdown_files": "Markdown Bestanden",
    "renpy_files": "Ren'Py Bestanden",
    "shell_files": "Shell Bestanden",
    "all_files": "Alle Bestanden",
    "binary_file_title": "Binair Bestand Gedetecteerd",
    "binary_file": "Er zijn ongebruikelijke tekens in dit document gedetecteerd. Wilt u het openen en de ruwe data door Slash Code laten lezen?\nWaarschuwing: dit zal Slash Code waarschijnlijk vertragen.",
    "session_loaded": "Sessie geladen:",
    "error_b1": "Fout gedurend bestand laden: ",
    "error_b2": "Fout gedurend map laden: "
    },
    "de": {
    "gui_lang": "GUI-Sprache",
    "msys_install": "MSYS2 installiert. Bitte MinGW über die MSYS2-Shell installieren: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Installation von MinGW-w64 fehlgeschlagen:",
    "gcc_used": "Genutztes GCC:",
    "gcc_error_a1": "Installation von G++ fehlgeschlagen.",
    "gcc_error_a2": "Überprüfung der G++-Version fehlgeschlagen:",
    "gcc_error_b1": "G++-Compiler nicht gefunden. Abbruch des C++-Laufs.",
    "gcc_error_b2": "Installation des MinGW-Compilers fehlgeschlagen.\n",
    "cpp_usercode_written": "C++-Code des Benutzers geschrieben nach ***.",
    "gcc_check_a1": "Suche nach vorhandenem G++-Compiler...",
    "gcc_check_a2": "Herunterladen und Installieren von MinGW-w64...",
    "gcc_check_a3": "MinGW-w64 wird von *** heruntergeladen...",
    "gcc_check_a4": "Bisher *** MB heruntergeladen...",
    "gcc_check_a4_5": "Insgesamt *** MB heruntergeladen.",
    "gcc_check_b1": "Entpacke MinGW-w64-Archiv...",
    "gcc_check_b2": "Versuche, G++-Compiler zu installieren/aktualisieren...",
    "gcc_compilation_attempt": "Versuch der Kompilierung mit Flag ***:",
    "gcc_compilation_success": "Kompilierung erfolgreich, führe ausführbare Datei aus...",
    "gcc_compilation_failed": "Kompilierung für *** mit Fehlern fehlgeschlagen:",
    "gcc_execution_finished": "Ausführung erfolgreich beendet.",
    "gcc_execution_error_a1": "Beim Ausführen der ausführbaren Datei ist ein Fehler aufgetreten:",
    "gcc_mingw_addpath": "MinGW-w64 bin-Ordner wurde PATH hinzugefügt:",
    "gcc_compiler_installed": "G++ erfolgreich installiert/aktualisiert.",
    "gcc_found_compiler_ver": "Gefundene G++-Version:",
    "gcc_sufficient_compiler_ver": "Die G++-Version ist ausreichend.",
    "gcc_old_compiler_ver": "Deine G++-Version ist zu alt und muss aktualisiert werden.",
    "gcc_mingw_extracted": "Entpackung abgeschlossen. MinGW installiert in:",
    "py7zr_installed": "Das py7zr-Paket wurde erfolgreich installiert.",
    "py7zr_error_a1": "Das Paket py7zr wurde nicht gefunden, installiere py7zr...",
    "csc_compiler": "C#-Compiler (csc)",
    "cs_usercode_written": "C#-Code des Benutzers geschrieben nach ***.",
    "csc_error_a1": "C#-Compiler (csc) nicht gefunden. Versuche zu installieren...\n",
    "csc_error_a2": "CSC-Compiler nicht gefunden und Installation fehlgeschlagen. C#-Lauf abgebrochen.",
    "csc_autoinst_fail": "Automatische Installation des C#-Compilers fehlgeschlagen. Bitte installiere das .NET SDK manuell.\n",
    "csc_compiler_installed": "C#-Compiler (csc) erfolgreich installiert.\n",
    "csc_compiling_with": "Kompiliere mit:",
    "csc_compilation_success": "Kompilierung erfolgreich.\n",
    "csc_execution_finished": "Ausführung erfolgreich beendet.",
    "csc_execution_error_a1": "Beim Versuch, die ausführbare Datei auszuführen, ist ein Fehler aufgetreten:",
    "sh_platform_not_supported": "Deine Plattform unterstützt das Ausführen von Shell-Skripten nicht.",
    "py_error_a1_title": "Unzureichende Python-Version",
    "py_error_a1": "Bitte installiere Python 3.13+.",
    "py_error_a2": "Python-Interpreter nicht gefunden.",
    "py_error_a3": "Python-Version konnte nicht analysiert werden.",
    "error_a1": "Fehler",
    "error_a2": "Datei konnte nicht geöffnet werden",
    "error_a3": "Datei konnte nicht geöffnet werden:\n",
    "error_a4": "Datei konnte nicht beschrieben werden:\n",
    "error_a5": "Quellcode-Datei von Slash Code konnte nicht geladen werden. Grund:\n\n",
    "error_c0": "Fehler beim Aktualisieren des Ordner-Buttons:",
    "error_c1": "Fehler beim Aktualisieren des Menü-Labels:",
    "error_c2": "Fehler beim Aktualisieren des Datei-Labels:",
    "error_c3": "Fehler beim Aktualisieren des Editier-Labels:",
    "error_c4": "Fehler beim Aktualisieren des Theme-Labels:",
    "error_c5": "Fehler beim Aktualisieren des Ausführungs-Labels:",
    "error_c6": "Fehler beim Aktualisieren des Ansicht-Labels:",
    "error_c7": "Fehler beim Aktualisieren des Sprach-Labels:",
    "error_c8": "Fehler beim Aktualisieren des GUI-Sprach-Labels:",
    "error_d1": "Beim Ausführen des Dokumentcodes ist eine Ausnahme aufgetreten. Grund:\n\n",
    "error_d1_5": "Beim Schreiben und Ausführen des Dokuments ist eine Ausnahme aufgetreten. Grund:\n\n",
    "error_d2": "Der Compiler wurde nicht korrekt installiert.",
    "error_e1": "pip konnte py7z nicht installieren. Grund:",
    "deleting_dirs": "Lösche Verzeichnis(se): ",
    "directory_del_not_found": "Keine Verzeichnisse zum Löschen gefunden.",
    "find": "Suchen",
    "find_query": "Suchen:",
    "find_all": "Alle suchen",
    "replace": "Ersetzen",
    "replace_query": "Ersetzen:",
    "replace_all": "Alle ersetzen",
    "runner_not_found": " nicht gefunden!\n",
    "install_suggest": "Bitte zuerst installieren.\n",
    "instructions": "Anleitung: ",
    "compilation_error": "Kompilierfehler:\n",
    "opened_in_browser": "Im Standardbrowser geöffnet.",
    "language_not_supported": "Sprache wird für Ausführung nicht unterstützt.",
    "process_error": "Prozessfehler: ",
    "unexpected_error": "Unerwarteter Fehler: ",
    "cleanup_failed": "Bereinigung fehlgeschlagen: ",
    "file": "Datei",
    "new": "Neu",
    "open": "Öffnen",
    "save": "Speichern",
    "toggle_new_file_saving": "Neues Dateispeichern umschalten",
    "clean_temp_files": "Temporäre Dateien bereinigen",
    "clean_temp_directories": "Temporäre Verzeichnisse bereinigen",
    "fully_wipe_directories": "Temporäre Verzeichnisse vollständig löschen",
    "reboot_consolemode": "Im Konsolenmodus neu starten",
    "exit": "Beenden",
    "edit": "Bearbeiten",
    "undo": "Rückgängig",
    "redo": "Wiederholen",
    "language": "Sprache",
    "theme": "Thema",
    "theme_light": "Hell",
    "theme_dark": "Dunkel",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Nacht-Eule",
    "theme_shades_of_purple": "Lila Nuancen",
    "theme_high_contrast": "Hoher Kontrast",
    "open_folder": "Ordner öffnen",
    "changed_language_to": "Sprache geändert zu ",
    "view": "Ansicht",
    "zoom_in": "Vergrößern",
    "zoom_out": "Verkleinern",
    "show_sidebar": "Seitenleiste anzeigen",
    "hide_sidebar": "Seitenleiste ausblenden",
    "show_minimap": "Minikarte anzeigen",
    "hide_minimap": "Minikarte ausblenden",
    "show_debug_info": "Debug-Informationen anzeigen",
    "hide_debug_info": "Debug-Informationen ausblenden",
    "toggle_fullscreen": "Vollbild umschalten",
    "exit_fullscreen": "Vollbild verlassen",
    "run": "Ausführen",
    "run_file": "Datei ausführen",
    "sc_output": "SC-Ausgabe",
    "output_sc_title": "-- Slash Code Texteditor | SC-Ausgabe für Dateiausführung --",
    "save_output_text": "Ausgabetext speichern",
    "highlighting_as": "Markierung als: ",
    "plaintext": "Klartext",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell-Skript",
    "python_files": "Python-Dateien",
    "javascript_files": "JavaScript-Dateien",
    "html_files": "HTML-Dateien",
    "c_files": "C-Dateien",
    "cpp_files": "C++-Dateien",
    "header_files": "Header-Dateien",
    "text_files": "Textdateien",
    "cs_files": "C#-Dateien",
    "css_files": "CSS-Dateien",
    "markdown_files": "Markdown-Dateien",
    "renpy_files": "Ren'Py-Dateien",
    "shell_files": "Shell-Skriptdateien",
    "all_files": "Alle Dateien",
    "binary_file_title": "Binärdatei erkannt",
    "binary_file": "Ungewöhnliche Zeichen wurden in diesem Dokument erkannt. Möchten Sie es öffnen und Slash Code die Rohdaten lesen lassen?\nWarnung: Dies wird Slash Code vermutlich verlangsamen.",
    "session_loaded": "Sitzung geladen:",
    "error_b1": "Fehler beim Laden der Datei: ",
    "error_b2": "Fehler beim Laden des Verzeichnisses: "
    },
    "es": {
    "gui_lang": "GUI Lenguaje",
    "msys_install": "MSYS2 instalado. Por favor instala MinGW desde la terminal de MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Error al instalar MinGW-w64:",
    "gcc_used": "GCC usado:",
    "gcc_error_a1": "Falló la instalación de G++.",
    "gcc_error_a2": "No se pudo verificar la versión de G++:",
    "gcc_error_b1": "Compilador G++ no encontrado. Abortando ejecución de C++.",
    "gcc_error_b2": "Falló la instalación del compilador MinGW.\n",
    "cpp_usercode_written": "Código C++ del usuario guardado en ***.",
    "gcc_check_a1": "Verificando existencia de compilador G++...",
    "gcc_check_a2": "Descargando e instalando MinGW-w64...",
    "gcc_check_a3": "Descargando MinGW-w64 desde ***...",
    "gcc_check_a4": "Descargados *** MB hasta ahora...",
    "gcc_check_a4_5": "Descargados *** MB en total.",
    "gcc_check_b1": "Extrayendo archivo MinGW-w64...",
    "gcc_check_b2": "Intentando instalar/actualizar compilador G++...",
    "gcc_compilation_attempt": "Intentando compilar con la bandera ***:",
    "gcc_compilation_success": "Compilación exitosa, ejecutando programa...",
    "gcc_compilation_failed": "Compilación fallida para *** con errores:",
    "gcc_execution_finished": "Ejecución finalizada exitosamente.",
    "gcc_execution_error_a1": "Ocurrió un error al intentar ejecutar el programa:",
    "gcc_mingw_addpath": "Carpeta bin de MinGW-w64 añadida al PATH:",
    "gcc_compiler_installed": "G++ instalado/actualizado correctamente.",
    "gcc_found_compiler_ver": "Versión de G++ encontrada:",
    "gcc_sufficient_compiler_ver": "La versión de G++ es suficiente.",
    "gcc_old_compiler_ver": "Tu versión de G++ es demasiado antigua y debe actualizarse.",
    "gcc_mingw_extracted": "Extracción completa. MinGW instalado en:",
    "py7zr_installed": "El paquete py7zr se instaló correctamente.",
    "csc_compiler": "Compilador C# (csc)",
    "cs_usercode_written": "Código C# del usuario guardado en ***.",
    "csc_error_a1": "Compilador C# (csc) no encontrado. Intentando instalar...\n",
    "csc_error_a2": "Compilador CSC no encontrado y la instalación falló. Abortando ejecución de C#.",
    "csc_autoinst_fail": "Fallo al instalar automáticamente el compilador C#. Por favor, instala el SDK de .NET manualmente.\n",
    "csc_compiler_installed": "Compilador C# (csc) instalado correctamente.\n",
    "csc_compiling_with": "Compilando con:",
    "csc_compilation_success": "Compilación exitosa.\n",
    "csc_execution_finished": "Ejecución finalizada exitosamente.",
    "csc_execution_error_a1": "Se ha producido un error al intentar ejecutar el programa:",
    "sh_platform_not_supported": "Tu plataforma no es compatible para ejecutar scripts Shell Script.",
    "py_error_a1_title": "Versión de Python insuficiente",
    "py_error_a1": "Instale Python 3.13+.",
    "py_error_a2": "No se encontró el intérprete de Python.",
    "py_error_a3": "No se pudo analizar la versión de Python.",
    "error_a1": "Error",
    "error_a2": "No se pudo abrir el archivo",
    "error_a3": "No se pudo abrir el archivo:\n",
    "error_a4": "No se pudo escribir el archivo:\n",
    "error_a5": "No se pudo cargar el archivo fuente de Slash Code. Motivo:\n\n",
    "error_c0": "Error al actualizar el botón de carpeta:",
    "error_c1": "Error al actualizar la etiqueta del menú:",
    "error_c2": "Error al actualizar la etiqueta del archivo:",
    "error_c3": "Error al actualizar la etiqueta de edición:",
    "error_c4": "Error al actualizar la etiqueta del tema:",
    "error_c5": "Error al ejecutar la actualización de la etiqueta:",
    "error_c6": "Error al actualizar la etiqueta de la vista:",
    "error_c7": "Error al actualizar la etiqueta del idioma:",
    "error_c8": "Error al actualizar la etiqueta del idioma de la GUI:",
    "error_d1": "Se ha producido una excepción al intentar ejecutar el código del documento. La razón es:\n\n",
    "error_d1_5": "Se produjo una excepción al intentar escribir y ejecutar el documento. La razón es:\n\n",
    "error_d2": "El compilador no se instaló correctamente.",
    "error_e1": "pip no pudo instalar py7z. Motivo:",
    "deleting_dirs": "Eliminando directorio(s): ", 
    "directory_del_not_found": "No se encontraron directorio(s) para eliminar.",
    "find": "Buscar",
    "find_query": "Buscar:",
    "find_all": "Buscar todos",
    "replace": "Reemplazar", 
    "replace_query": "Reemplazar:", 
    "replace_all": "Reemplazar Todo",
    "runner_not_found": " no encontrado!\n",
    "install_suggest": "Por favor instálalo primero.\n",
    "instructions": "Instrucciones: ",
    "compilation_error": "Error de compilación:\n",
    "opened_in_browser": "Abierto en el navegador predeterminado.",
    "language_not_supported": "Idioma no compatible para ejecución.",
    "process_error": "Error del proceso: ",
    "unexpected_error": "Error inesperado: ",
    "cleanup_failed": "Fallo al limpiar: ",
    "file": "Archivo",
    "new": "Nuevo",
    "open": "Abrir",
    "save": "Guardar",
    "toggle_new_file_saving": "Activar el guardado de nuevos archivos",
    "clean_temp_files": "Limpiar archivos temporales",
    "clean_temp_directories": "Limpiar directorios temporales",
    "fully_wipe_directories": "Borrar completamente los directorios temporales",
    "reboot_consolemode": "Reiniciar en modo consola",
    "exit": "Salir",
    "edit": "Editar",
    "undo": "Deshacer",
    "redo": "Rehacer",
    "language": "Lenguaje",
    "theme": "Tema",
    "theme_light": "Claro",
    "theme_dark": "Oscuro",
    "theme_dracula": "Drácula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Búho Nocturno",
    "theme_shades_of_purple": "Tonos de Púrpura",
    "open_folder": "Abrir Carpeta",
    "changed_language_to": "Cambió de idioma a ",
    "view": "Vista",
    "zoom_in": "Acercar",
    "zoom_out": "Alejar",
    "show_sidebar": "Mostrar barra lateral",
    "hide_sidebar": "Ocultar barra lateral",
    "show_minimap": "Mostrar minimapa",
    "hide_minimap": "Ocultar minimapa",
    "show_debug_info": "Mostrar información de depuración",
    "hide_debug_info": "Ocultar información de depuración",
    "toggle_fullscreen": "Activar pantalla completa",
    "exit_fullscreen": "Salir de pantalla completa",
    "run": "Ejecutar",
    "run_file": "Ejecutar archivo",
    "sc_output": "SC-Producción",
    "output_sc_title": "-- Editor de texto de Slash Code | Salida SC para ejecución de archivos --",
    "save_output_text": "Guardar texto de salida",
    "highlighting_as": "Resaltado como: ",
    "plaintext": "Texto plano",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Script de Shell",
    "python_files": "Archivos de Python",
    "javascript_files": "Archivos de JavaScript",
    "html_files": "Archivos de HTML",
    "c_files": "Archivos de C",
    "cpp_files": "Archivos de C++",
    "header_files": "Archivos de Encabezado",
    "text_files": "Archivos de Texto",
    "cs_files": "Archivos de C#",
    "css_files": "Archivos de CSS",
    "markdown_files": "Archivos de Markdown",
    "renpy_files": "Archivos de Ren'Py",
    "shell_files": "Archivos de Shell",
    "all_files": "Todos Los Archivos",
    "binary_file_title": "Archivo binario detectado",
    "binary_file": "Se han detectado caracteres inusuales en este documento. ¿Desea abrirlo y que Slash Code lea los datos sin procesar?\nAdvertencia: esto probablemente ralentizará Slash Code.",
    "session_loaded": "Sesión cargada:",
    "error_b1": "Error al cargar el archivo: ",
    "error_b2": "Error al cargar el directorio: "
    },
    "it": {
    "gui_lang": "Lingua GUI",
    "msys_install": "MSYS2 installato. Per favore installa MinGW tramite la shell MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Installazione di MinGW-w64 fallita:",
    "gcc_used": "GCC utilizzato:",
    "gcc_error_a1": "Installazione di G++ fallita.",
    "gcc_error_a2": "Impossibile controllare la versione di G++:",
    "gcc_error_b1": "Compilatore G++ non trovato. Interruzione esecuzione C++.",
    "gcc_error_b2": "Installazione del compilatore MinGW fallita.\n",
    "cpp_usercode_written": "Codice C++ utente scritto in ***.",
    "gcc_check_a1": "Verifica della presenza di un compilatore G++ esistente...",
    "gcc_check_a2": "Download e installazione di MinGW-w64 in corso...",
    "gcc_check_a3": "Download di MinGW-w64 da *** in corso...",
    "gcc_check_a4": "*** MB scaricati finora...",
    "gcc_check_a4_5": "*** MB scaricati in totale.",
    "gcc_check_b1": "Estrazione dell'archivio MinGW-w64 in corso...",
    "gcc_check_b2": "Tentativo di installazione/aggiornamento del compilatore G++...",
    "gcc_compilation_attempt": "Tentativo di compilazione con flag ***:",
    "gcc_compilation_success": "Compilazione riuscita, esecuzione del file eseguibile...",
    "gcc_compilation_failed": "Compilazione fallita per *** con errori:",
    "gcc_execution_finished": "Esecuzione completata con successo.",
    "gcc_execution_error_a1": "Errore durante il tentativo di eseguire il file eseguibile:",
    "gcc_mingw_addpath": "Cartella bin di MinGW-w64 aggiunta al PATH:",
    "gcc_compiler_installed": "G++ installato/aggiornato con successo.",
    "gcc_found_compiler_ver": "Versione di G++ trovata:",
    "gcc_sufficient_compiler_ver": "La versione di G++ è sufficiente.",
    "gcc_old_compiler_ver": "La tua versione di G++ è troppo vecchia e deve essere aggiornata.",
    "gcc_mingw_extracted": "Estrazione completata. MinGW installato in:",
    "py7zr_installed": "Il pacchetto py7zr è stato installato con successo.",
    "py7zr_error_a1": "Pacchetto py7zr non trovato, installazione in corso...",
    "csc_compiler": "Compilatore C# (csc)",
    "cs_usercode_written": "Codice C# utente scritto in ***.",
    "csc_error_a1": "Compilatore C# (csc) non trovato. Tentativo di installazione in corso...\n",
    "csc_error_a2": "Compilatore CSC non trovato e installazione fallita. Interruzione esecuzione C#.",
    "csc_autoinst_fail": "Installazione automatica del compilatore C# fallita. Si prega di installare manualmente il .NET SDK.\n",
    "csc_compiler_installed": "Compilatore C# (csc) installato con successo.\n",
    "csc_compiling_with": "Compilazione con:",
    "csc_compilation_success": "Compilazione riuscita.\n",
    "csc_execution_finished": "Esecuzione completata con successo.",
    "csc_execution_error_a1": "Si è verificato un errore durante il tentativo di eseguire il file eseguibile:",
    "sh_platform_not_supported": "La tua piattaforma non supporta l'esecuzione di script Shell.",
    "py_error_a1_title": "Versione Python insufficiente",
    "py_error_a1": "Si prega di installare Python 3.13 o superiore.",
    "py_error_a2": "Interpreter Python non trovato.",
    "py_error_a3": "Impossibile analizzare la versione di Python.",
    "error_a1": "Errore",
    "error_a2": "Impossibile aprire il file",
    "error_a3": "Impossibile aprire il file:\n",
    "error_a4": "Impossibile scrivere nel file:\n",
    "error_a5": "Impossibile caricare il file sorgente di Slash Code. Motivo:\n\n",
    "error_c0": "Errore durante l'aggiornamento del pulsante cartella:",
    "error_c1": "Errore durante l'aggiornamento dell'etichetta del menu:",
    "error_c2": "Errore durante l'aggiornamento dell'etichetta del file:",
    "error_c3": "Errore durante l'aggiornamento dell'etichetta modifica:",
    "error_c4": "Errore durante l'aggiornamento dell'etichetta tema:",
    "error_c5": "Errore durante l'aggiornamento dell'etichetta esecuzione:",
    "error_c6": "Errore durante l'aggiornamento dell'etichetta visualizzazione:",
    "error_c7": "Errore durante l'aggiornamento dell'etichetta lingua:",
    "error_c8": "Errore durante l'aggiornamento dell'etichetta lingua GUI:",
    "error_d1": "Si è verificata un'eccezione durante il tentativo di eseguire il codice del documento. Il motivo è:\n\n",
    "error_d1_5": "Si è verificata un'eccezione durante il tentativo di scrivere e eseguire il documento. Il motivo è:\n\n",
    "error_d2": "Il compilatore non è stato installato correttamente.",
    "error_e1": "pip non è riuscito a installare py7z. Motivo:",
    "deleting_dirs": "Eliminazione della/e cartella/e: ",
    "directory_del_not_found": "Nessuna cartella trovata per l'eliminazione.",
    "find": "Trova",
    "find_query": "Trova:",
    "find_all": "Trova tutto",
    "replace": "Sostituisci",
    "replace_query": "Sostituisci con:",
    "replace_all": "Sostituisci tutto",
    "runner_not_found": " non trovato!\n",
    "install_suggest": "Si prega di installarlo prima.\n",
    "instructions": "Istruzioni: ",
    "compilation_error": "Errore di compilazione:\n",
    "opened_in_browser": "Aperto nel browser predefinito.",
    "language_not_supported": "Lingua non supportata per l'esecuzione.",
    "process_error": "Errore del processo: ",
    "unexpected_error": "Errore imprevisto: ",
    "cleanup_failed": "Pulizia fallita: ",
    "file": "File",
    "new": "Nuovo",
    "open": "Apri",
    "save": "Salva",
    "toggle_new_file_saving": "Attiva disattiva salvataggio nuovo file",
    "clean_temp_files": "Pulisci file temporanei",
    "clean_temp_directories": "Pulisci cartelle temporanee",
    "fully_wipe_directories": "Cancella completamente le cartelle temporanee",
    "reboot_consolemode": "Riavvia in modalità console",
    "exit": "Esci",
    "edit": "Modifica",
    "undo": "Annulla",
    "redo": "Ripristina",
    "language": "Lingua",
    "theme": "Tema",
    "theme_light": "Chiaro",
    "theme_dark": "Scuro",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Gufo Notturno",
    "theme_shades_of_purple": "Tonalità di Viola",
    "theme_high_contrast": "Alto Contrasto",
    "open_folder": "Apri cartella",
    "changed_language_to": "Lingua cambiata in ",
    "view": "Visualizza",
    "zoom_in": "Zoom in",
    "zoom_out": "Zoom out",
    "show_sidebar": "Mostra barra laterale",
    "hide_sidebar": "Nascondi barra laterale",
    "show_minimap": "Mostra minimappa",
    "hide_minimap": "Nascondi minimappa",
    "show_debug_info": "Mostra info debug",
    "hide_debug_info": "Nascondi info debug",
    "toggle_fullscreen": "Attiva/disattiva full screen",
    "exit_fullscreen": "Esci dal full screen",
    "run": "Esegui",
    "run_file": "Esegui file",
    "sc_output": "Output SC",
    "output_sc_title": "-- Editor di Testo Slash Code | Output SC per esecuzione file --",
    "save_output_text": "Salva testo output",
    "highlighting_as": "Evidenziando come: ",
    "plaintext": "Testo semplice",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Script di Shell",
    "python_files": "File Python",
    "javascript_files": "File JavaScript",
    "html_files": "File HTML",
    "c_files": "File C",
    "cpp_files": "File C++",
    "header_files": "File header",
    "text_files": "File di testo",
    "cs_files": "File C#",
    "css_files": "File CSS",
    "markdown_files": "File Markdown",
    "renpy_files": "File Ren'Py",
    "shell_files": "File Shell",
    "all_files": "Tutti i file",
    "binary_file_title": "File binario rilevato",
    "binary_file": "Caratteri insoliti sono stati rilevati in questo documento, vuoi aprirlo e lasciare che Slash Code legga i dati grezzi?\nAttenzione, questo probabilmente rallenterà Slash Code.",
    "session_loaded": "Sessione caricata:",
    "error_b1": "Errore nel caricamento del file: ",
    "error_b2": "Errore nel caricamento della cartella: "
    },
    "fr": {
    "gui_lang": "Langue de l'interface",
    "msys_install": "MSYS2 est installé. Veuillez installer MinGW via le terminal MSYS2 : pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "Échec de l'installation de MinGW-w64:",
    "gcc_used": "GCC utilisé:",
    "gcc_error_a1": "Échec de l'installation de G++.",
    "gcc_error_a2": "Échec de la vérification de la version de G++:",
    "gcc_error_b1": "Compilateur G++ introuvable. Exécution C++ annulée.",
    "gcc_error_b2": "Échec de l'installation du compilateur MinGW.\n",
    "cpp_usercode_written": "Code C++ de l'utilisateur écrit dans ***.",
    "gcc_check_a1": "Vérification de l'existence du compilateur G++...",
    "gcc_check_a2": "Téléchargement et installation de MinGW-w64...",
    "gcc_check_a3": "Téléchargement de MinGW-w64 depuis ***...",
    "gcc_check_a4": "*** Mo téléchargés jusqu'à présent...",
    "gcc_check_a4_5": "*** Mo téléchargés en total.",
    "gcc_check_b1": "Extraction de l'archive MinGW-w64...",
    "gcc_check_b2": "Tentative d'installation/mise à jour du compilateur G++...",
    "gcc_compilation_attempt": "Tentative de compilation avec le drapeau ***:",
    "gcc_compilation_success": "Compilation réussie, exécution du programme...",
    "gcc_compilation_failed": "Échec de la compilation pour *** avec erreurs:",
    "gcc_execution_finished": "Exécution terminée avec succès.",
    "gcc_execution_error_a1": "Une erreur est survenue lors de l'exécution du programme:",
    "gcc_mingw_addpath": "Dossier bin de MinGW-w64 ajouté au PATH:",
    "gcc_compiler_installed": "G++ installé/mis à jour avec succès.",
    "gcc_found_compiler_ver": "Version de G++ trouvée:",
    "gcc_sufficient_compiler_ver": "La version de G++ est suffisante.",
    "gcc_old_compiler_ver": "Votre version de G++ est trop ancienne, une mise à jour est nécessaire.",
    "gcc_mingw_extracted": "Extraction terminée. MinGW installé à:",
    "py7zr_installed": "Le package py7zr a été installé avec succès.",
    "csc_compiler": "Compilateur C# (csc)",
    "cs_usercode_written": "Code C# de l'utilisateur écrit dans ***.",
    "csc_error_a1": "Compilateur C# (csc) introuvable. Tentative d'installation...\n",
    "csc_error_a2": "Compilateur CSC introuvable et échec de l'installation. Exécution C# annulée.",
    "csc_autoinst_fail": "Échec de l'installation automatique du compilateur C#. Veuillez installer le SDK .NET manuellement.\n",
    "csc_compiler_installed": "Compilateur C# (csc) installé avec succès.\n",
    "csc_compiling_with": "Compilation avec:",
    "csc_compilation_success": "Compilation réussie.\n",
    "csc_execution_finished": "Exécution terminée avec succès.",
    "csc_execution_error_a1": "Une erreur s'est produite lors de la tentative d'exécution du programme:",
    "sh_platform_not_supported": "Votre plateforme ne prend pas en charge l'exécution de scripts Shell.",
    "py_error_a1_title": "Version Python insuffisante",
    "py_error_a1": "Veuillez installer Python 3.13+.",
    "py_error_a2": "Interpréteur Python introuvable.", 
    "py_error_a3": "Impossible d'analyser la version Python.",
    "error_a1": "Erreur",
    "error_a2": "Impossible d'ouvrir le fichier",
    "error_a3": "Impossible d'ouvrir le fichier:\n",
    "error_a4": "Impossible d'écrire dans le fichier:\n",
    "error_a5": "Impossible de charger le fichier source du Slash Code. Motif:\n\n",
    "error_c0": "Erreur de mise à jour du bouton de dossier:",
    "error_c1": "Erreur de mise à jour du libellé du menu:",
    "error_c2": "Erreur de mise à jour du libellé du fichier:",
    "error_c3": "Erreur de mise à jour de l'étiquette de modification:",
    "error_c5": "Erreur de mise à jour de l'étiquette d'exécution:",
    "error_c6": "Erreur de mise à jour de l'étiquette d'affichage:",
    "error_c7": "Erreur de mise à jour du libellé de langue:",
    "error_c8": "Erreur de mise à jour du libellé de langue de l'interface graphique:",
    "error_d1": "Une exception s'est produite lors de l'exécution du code du document. La raison en est:\n\n",
    "error_d1_5": "Une exception s'est produite lors de la tentative d'écriture et d'exécution du document. La raison en est:\n\n",
    "error_d2": "Le compilateur n'a pas pu s'installer correctement.",
    "error_e1": "pip n'a pas réussi à installer py7z. Motif:",
    "deleting_dirs": "Suppression de répertoire(s): ", 
    "directory_del_not_found": "Aucun répertoire(s) à supprimer n'a été trouvé.",
    "find": "Rechercher",
    "find_query": "Rechercher:",
    "find_all": "Recherchez tout",
    "replace": "Remplacer", 
    "replace_query": "Remplacer:", 
    "replace_all": "Remplacer Tout",
    "runner_not_found": " introuvable!\n",
    "install_suggest": "Veuillez l'installer d'abord.\n",
    "instructions": "Instructions: ",
    "compilation_error": "Erreur de compilation:\n",
    "opened_in_browser": "Ouvert dans le navigateur par défaut.",
    "language_not_supported": "Langue non prise en charge pour l'exécution.",
    "process_error": "Erreur de processus: ",
    "unexpected_error": "Erreur inattendue: ",
    "cleanup_failed": "Échec du nettoyage: ",
    "file": "Fichier",
    "new": "Nouveau",
    "open": "Ouvrir",
    "save": "Enregistrer",
    "toggle_new_file_saving": "Activer l'enregistrement d'un nouveau fichier",
    "clean_temp_files": "Nettoyer les fichiers temporaires",
    "clean_temp_directories": "Nettoyer les dossiers temporaires",
    "fully_wipe_directories": "Effacer complètement les dossiers temporaires",
    "reboot_consolemode": "Redémarrer en mode console",
    "exit": "Quitter",
    "edit": "Éditer",
    "undo": "Annuler",
    "redo": "Rétablir",
    "language": "Langue",
    "theme": "Thème",
    "theme_light": "Clair",
    "theme_dark": "Sombre",
    "theme_dracula": "Dracula",
    "theme_monokai": "Monokai",
    "theme_night_owl": "Chouette Nocturne",
    "theme_shades_of_purple": "Nuances de Violet",
    "theme_high_contrast": "Contraste Élevé",
    "open_folder": "Ouvrir le dossier",
    "changed_language_to": "Langue changée en ",
    "view": "Affichage",
    "zoom_in": "Agrandir",
    "zoom_out": "Rétrécir",
    "show_sidebar": "Afficher la barre latérale",
    "hide_sidebar": "Masquer la barre latérale",
    "show_minimap": "Afficher la minicarte",
    "hide_minimap": "Masquer la minicarte",
    "show_debug_info": "Afficher les informations de débogage",
    "hide_debug_info": "Masquer les informations de débogage",
    "toggle_fullscreen": "Activer le plein écran",
    "exit_fullscreen": "Quitter le plein écran",
    "run": "Exécuter",
    "run_file": "Exécuter le fichier",
    "sc_output": "SC-Sortir",
    "output_sc_title": "-- Éditeur de texte de Slash Code | Sortie SC pour l'exécution de fichiers --",
    "save_output_text": "Enregistrer le texte de sortie",
    "highlighting_as": "Surlignage comme: ",
    "plaintext": "Texte brut",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Script Shell",
    "python_files": "Fichiers Python",
    "javascript_files": "Fichiers JavaScript",
    "html_files": "Fichiers HTML",
    "c_files": "Fichiers C",
    "cpp_files": "Fichiers C++",
    "header_files": "Fichiers D'en-tête",
    "text_files": "fichiers texte",
    "cs_files": "Fichiers C#",
    "css_files": "Fichiers CSS",
    "markdown_files": "Fichiers Markdown",
    "renpy_files": "Fichiers Ren'Py",
    "shell_files": "Fichiers Shell",
    "all_files": "Tous Les Fichiers",
    "binary_file_title": "Fichier binaire détecté",
    "binary_file": "Des caractères inhabituels ont été détectés dans ce document. Souhaitez-vous l'ouvrir et laisser Slash Code lire les données brutes?\nAttention, cela risque de ralentir Slash Code.",
    "session_loaded": "Session chargé:",
    "error_b1": "Erreur lors du chargement du fichier: ",
    "error_b2": "Erreur lors du chargement du dossier: "
    },
    
    "jp": {
    "gui_lang": "GUI 言語",
    "msys_install": "MSYS2がインストールされました。MSYS2シェルでMinGWをインストールしてください: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "MinGW-w64のインストールに失敗しました:",
    "gcc_used": "使用中のGCC:",
    "gcc_error_a1": "G++のインストールに失敗しました。",
    "gcc_error_a2": "G++のバージョン確認に失敗しました:",
    "gcc_error_b1": "G++コンパイラが見つかりません。C++の実行を中止します。",
    "gcc_error_b2": "MinGWコンパイラのインストールに失敗しました。\n",
    "cpp_usercode_written": "ユーザーのC++コードが***に書き込まれました。",
    "gcc_check_a1": "既存のG++コンパイラを確認しています...",
    "gcc_check_a2": "MinGW-w64をダウンロードしてインストールしています...",
    "gcc_check_a3": "***からMinGW-w64をダウンロード中...",
    "gcc_check_a4": "これまでに*** MBをダウンロードしました...",
    "gcc_check_a4_5": "合計*** MBをダウンロードしました。",
    "gcc_check_b1": "MinGW-w64アーカイブを解凍中...",
    "gcc_check_b2": "G++コンパイラのインストール/更新を試みています...",
    "gcc_compilation_attempt": "*** フラグでのコンパイルを試みています:",
    "gcc_compilation_success": "コンパイル成功。実行ファイルを実行しています...",
    "gcc_compilation_failed": "*** のコンパイルに失敗しました。エラー内容:",
    "gcc_execution_finished": "実行が正常に終了しました。",
    "gcc_execution_error_a1": "実行ファイルの起動中にエラーが発生しました:",
    "gcc_mingw_addpath": "MinGW-w64のbinフォルダをPATHに追加しました:",
    "gcc_compiler_installed": "G++が正常にインストール/更新されました。",
    "gcc_found_compiler_ver": "検出されたG++バージョン:",
    "gcc_sufficient_compiler_ver": "G++のバージョンは十分です。",
    "gcc_old_compiler_ver": "G++のバージョンが古いため、アップグレードが必要です。",
    "gcc_mingw_extracted": "解凍完了。MinGWは以下にインストールされました:",
    "py7zr_installed": "py7zrパッケージが正常にインストールされました。",
    "csc_compiler": "C# コンパイラー (csc)",
    "cs_usercode_written": "ユーザーのC#コードが***に書き込まれました。",
    "csc_error_a1": "C# コンパイラー (csc) が見つかりません。インストールを試みています...\n",
    "csc_error_a2": "CSC コンパイラーが見つからず、インストールに失敗しました。C# 実行を中止します。",
    "csc_autoinst_fail": "C# コンパイラーの自動インストールに失敗しました。手動で .NET SDK をインストールしてください。\n",
    "csc_compiler_installed": "C# コンパイラー (csc) が正常にインストールされました。\n",
    "csc_compiling_with": "以下の環境でコンパイル中:",
    "csc_compilation_success": "コンパイル成功。\n",
    "csc_execution_finished": "実行が正常に終了しました。",
    "csc_execution_error_a1": "実行ファイルの起動中にエラーが発生しました:",
    "sh_platform_not_supported": "お使いのプラットフォームではシェルスクリプトの実行はサポートされていません。",
    "py_error_a1_title": "Pythonのバージョンが不十分です",
    "py_error_a1": "Python 3.13以降をインストールしてください。",
    "py_error_a2": "Pythonインタープリターが見つかりません。",
    "py_error_a3": "Pythonのバージョンを解析できませんでした。",
    "error_a1": "エラー",
    "error_a2": "ファイルを開けませんでした",
    "error_a3": "ファイルを開けませんでした:\n",
    "error_a4": "ファイルに書き込めませんでした:\n",
    "error_a5": "スラッシュコードのソースファイルを読み込めませんでした。理由:\n\n",
    "error_c0": "フォルダボタン更新エラー:",
    "error_c1": "メニューラベル更新エラー:",
    "error_c2": "ファイルラベル更新エラー:",
    "error_c3": "編集ラベル更新エラー:",
    "error_c4": "テーマラベル更新エラー:",
    "error_c5": "実行ラベル更新エラー:",
    "error_c6": "表示ラベル更新エラー:",
    "error_c7": "言語ラベル更新エラー:",
    "error_c8": "GUI言語ラベル更新エラー:",
    "error_d1": "ドキュメントのコードを実行中に例外が発生しました。理由は次の通りです:\n\n",
    "error_d1_5": "ドキュメントの書き込みと実行中に例外が発生しました。理由は次の通りです:\n\n",
    "error_d2": "コンパイラのインストールに失敗しました。",
    "error_e1": "pipはpy7zのインストールに失敗しました。理由:",
    "deleting_dirs": "ディレクトリを削除しています: ",
    "directory_del_not_found": "削除するディレクトリが見つかりません。",
    "find": "検索",
    "find_query": "検索:",
    "find_all": "すべてを検索ます",
    "replace": "交換", 
    "replace_query": "交換:", 
    "replace_all": "すべてを交換します",
    "runner_not_found": " が見つかりません！\n",
    "install_suggest": "まずインストールしてください。\n",
    "instructions": "使い方:",
    "compilation_error": "コンパイルエラー:\n",
    "opened_in_browser": "デフォルトのブラウザで開きました。",
    "language_not_supported": "この言語は実行に対応していません。",
    "process_error": "プロセスエラー: ",
    "unexpected_error": "予期しないエラー:",
    "cleanup_failed": "クリーンアップに失敗しました:",
    "file": "ファイル",
    "new": "新規",
    "open": "開く",
    "save": "保存",
    "toggle_new_file_saving": "新しいファイルの保存を切り替える",
    "clean_temp_files": "一時ファイルを消去する",
    "clean_temp_directories": "一時ディレクトリを消去する",
    "fully_wipe_directories": "一時ディレクトリを完全に消去する",
    "reboot_consolemode": "コンソールモードで再起動",
    "exit": "終了",
    "edit": "編集",
    "undo": "元に戻す",
    "redo": "やり直し",
    "language": "言語",
    "theme": "テーマ",
    "theme_light": "ライト",
    "theme_dark": "ダーク",
    "theme_dracula": "ドラキュラ",
    "theme_monokai": "モノカイ",
    "theme_night_owl": "ナイトアウル",
    "theme_shades_of_purple": "紫の影",
    "theme_high_contrast": "高コントラスト",
    "open_folder": "フォルダーを開く",
    "changed_language_to": "言語", # Japanese puts the topic in the middle, not the end, so we'll have to put the verb part to tbe end.
    "view": "表示",
    "zoom_in": "ズームイン",
    "zoom_out": "ズームアウト",
    "show_sidebar": "サイドバーを表示",
    "hide_sidebar": "サイドバーを非表示",
    "show_minimap": "ミニマップを表示",
    "hide_minimap": "ミニマップを非表示",
    "show_debug_info": "デバッグ情報を表示",
    "hide_debug_info": "デバッグ情報を非表示",
    "toggle_fullscreen": "全画面表示の切り替え",
    "exit_fullscreen": "全画面表示を終了",
    "run": "実行",
    "run_file": "ファイルを実行",
    "sc_output": "SC-出力",
    "output_sc_title": "-- スラッシュコードテキストエディター | ファイル実行用のSC出力 --",
    "save_output_text": "出力テキストを保存",
    "highlighting_as": "ハイライト:",
    "plaintext": "プレーンテキスト",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "シェルスクリプト",
    "python_files": "Python ファイル",
    "javascript_files": "JavaScript ファイル",
    "html_files": "HTML ファイル",
    "c_files": "C ファイル",
    "cpp_files": "C++ ファイル",
    "header_files": "ヘッダーファイル",
    "text_files": "テキストファイル",
    "cs_files": "C# ファイル",
    "css_files": "CSS ファイル",
    "markdown_files": "Markdown ファイル",
    "renpy_files": "Ren'Py ファイル",
    "shell_files": "Shell ファイル",
    "all_files": "全てのファイル",
    "binary_file_title": "バイナリファイルが検出されました",
    "binary_file": "このドキュメントで異常な文字が検出されました。ドキュメントを開いてSlash Codeに生データを読み取りますか?\n警告: これによりSlash Codeの速度が低下する可能性があります。",
    "session_loaded": "セッションロード:",
    "error_b1": "ファイルの読み込みエラー:",
    "error_b2": "ディレクトリの読み込みエラー:"
    },
    "zh": {
    "gui_lang": "界面语言",
    "msys_install": "已安装 MSYS2。请通过 MSYS2 终端安装 MinGW: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "安装 MinGW-w64 失败:",
    "gcc_used": "使用的 GCC:",
    "gcc_error_a1": "安装 G++ 失败。",
    "gcc_error_a2": "无法检查 G++ 版本:",
    "gcc_error_b1": "未找到 G++ 编译器。中止 C++ 运行。",
    "gcc_error_b2": "安装 MinGW 编译器失败。\n",
    "cpp_usercode_written": "用户的 C++ 代码已写入至 ***。",
    "gcc_check_a1": "检查现有的 G++ 编译器...",
    "gcc_check_a2": "正在下载并安装 MinGW-w64...",
    "gcc_check_a3": "正在从 *** 下载 MinGW-w64...",
    "gcc_check_a4": "已下载 *** MB...",
    "gcc_check_a4_5": "共下载 *** MB。",
    "gcc_check_b1": "正在解压 MinGW-w64 存档...",
    "gcc_check_b2": "尝试安装/更新 G++ 编译器...",
    "gcc_compilation_attempt": "尝试使用标志 *** 进行编译:",
    "gcc_compilation_success": "编译成功，正在运行可执行文件...",
    "gcc_compilation_failed": "*** 的编译失败，错误如下:",
    "gcc_execution_finished": "执行成功结束。",
    "gcc_execution_error_a1": "尝试运行可执行文件时发生错误:",
    "gcc_mingw_addpath": "已将 MinGW-w64 bin 文件夹添加到 PATH:",
    "gcc_compiler_installed": "G++ 安装/更新成功。",
    "gcc_found_compiler_ver": "找到的 G++ 版本:",
    "gcc_sufficient_compiler_ver": "G++ 版本足够。",
    "gcc_old_compiler_ver": "您的 G++ 版本过旧，需要升级。",
    "gcc_mingw_extracted": "提取完成。MinGW 安装路径为:",
    "py7zr_installed": "py7zr 软件包安装成功。",
    "py7zr_error_a1": "未找到 py7zr 软件包，正在安装 py7zr...",
    "csc_compiler": "C# 编译器 (csc)",
    "cs_usercode_written": "用户的 C# 代码已写入至 ***。",
    "csc_error_a1": "未找到 C# 编译器 (csc)。正在尝试安装...\n",
    "csc_error_a2": "未找到 CSC 编译器且安装失败。中止 C# 运行。",
    "csc_autoinst_fail": "自动安装 C# 编译器失败。请手动安装 .NET SDK。\n",
    "csc_compiler_installed": "C# 编译器 (csc) 安装成功。\n",
    "csc_compiling_with": "正在使用以下配置编译:",
    "csc_compilation_success": "编译成功。\n",
    "csc_execution_finished": "执行成功结束。",
    "csc_execution_error_a1": "尝试运行可执行文件时发生错误:",
    "sh_platform_not_supported": "您的平台不支持运行 Shell 脚本。",
    "py_error_a1_title": "Python 版本不足",
    "py_error_a1": "请安装 Python 3.13 及以上版本。",
    "py_error_a2": "未找到 Python 解释器。",
    "py_error_a3": "无法解析 Python 版本。",
    "error_a1": "错误",
    "error_a2": "无法打开文件",
    "error_a3": "无法打开文件:\n",
    "error_a4": "无法写入文件:\n",
    "error_a5": "无法加载 Slash Code 源文件。原因:\n\n",
    "error_c0": "更新文件夹按钮时出错:",
    "error_c1": "更新菜单标签时出错:",
    "error_c2": "更新文件标签时出错:",
    "error_c3": "更新编辑标签时出错:",
    "error_c4": "更新主题标签时出错:",
    "error_c5": "更新运行标签时出错:",
    "error_c6": "更新视图标签时出错:",
    "error_c7": "更新语言标签时出错:",
    "error_c8": "更新 GUI 语言标签时出错:",
    "error_d1": "尝试执行文档代码时发生异常。原因如下:\n\n",
    "error_d1_5": "尝试写入并执行文档时发生异常。原因如下:\n\n",
    "error_d2": "编译器未正确安装。",
    "error_e1": "pip 安装 py7z 失败。原因:",
    "deleting_dirs": "正在删除目录:",
    "directory_del_not_found": "未找到要删除的目录。",
    "find": "查找",
    "find_query": "查找:",
    "find_all": "查找全部",
    "replace": "替换",
    "replace_query": "替换为:",
    "replace_all": "全部替换",
    "runner_not_found": " 未找到！\n",
    "install_suggest": "请先安装它。\n",
    "instructions": "说明:",
    "compilation_error": "编译错误:\n",
    "opened_in_browser": "已在默认浏览器打开。",
    "language_not_supported": "不支持该语言的执行。",
    "process_error": "进程错误:",
    "unexpected_error": "意外错误:",
    "cleanup_failed": "清理失败:",
    "file": "文件",
    "new": "新建",
    "open": "打开",
    "save": "保存",
    "toggle_new_file_saving": "切换新文件保存",
    "clean_temp_files": "清理临时文件",
    "clean_temp_directories": "清理临时目录",
    "fully_wipe_directories": "完全清除临时目录",
    "reboot_consolemode": "控制台模式重启",
    "exit": "退出",
    "edit": "编辑",
    "undo": "撤销",
    "redo": "重做",
    "language": "语言",
    "theme": "主题",
    "theme_light": "浅色",
    "theme_dark": "深色",
    "theme_dracula": "德古拉",
    "theme_monokai": "Monokai",
    "theme_night_owl": "夜猫子",
    "theme_shades_of_purple": "紫色渐变",
    "theme_high_contrast": "高对比度",
    "open_folder": "打开文件夹",
    "changed_language_to": "语言切换至 ",
    "view": "查看",
    "zoom_in": "放大",
    "zoom_out": "缩小",
    "show_sidebar": "显示侧边栏",
    "hide_sidebar": "隐藏侧边栏",
    "show_minimap": "显示小地图",
    "hide_minimap": "隐藏小地图",
    "show_debug_info": "显示调试信息",
    "hide_debug_info": "隐藏调试信息",
    "toggle_fullscreen": "切换全屏",
    "exit_fullscreen": "退出全屏",
    "run": "运行",
    "run_file": "运行文件",
    "sc_output": "SC-输出",
    "output_sc_title": "-- Slash Code 文本编辑器 | 文件执行的 SC-输出 --",
    "save_output_text": "保存输出文本",
    "highlighting_as": "高亮为:",
    "plaintext": "纯文本",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "Shell 脚本",
    "python_files": "Python 文件",
    "javascript_files": "JavaScript 文件",
    "html_files": "HTML 文件",
    "c_files": "C 文件",
    "cpp_files": "C++ 文件",
    "header_files": "头文件",
    "text_files": "文本文件",
    "cs_files": "C# 文件",
    "css_files": "CSS 文件",
    "markdown_files": "Markdown 文件",
    "renpy_files": "Ren'Py 文件",
    "shell_files": "Shell 文件",
    "all_files": "所有文件",
    "binary_file_title": "检测到二进制文件",
    "binary_file": "检测到文档中有异常字符，是否打开并让 Slash Code 读取原始数据？\n警告:这可能会降低 Slash Code 的速度。",
    "session_loaded": "会话已加载:",
    "error_b1": "加载文件时出错:",
    "error_b2": "加载目录时出错:"
    },
    "ko": {
    "gui_lang": "GUI 언어",
    "msys_install": "MSYS2가 설치되었습니다. MSYS2 셸에서 MinGW를 설치하십시오: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "MinGW-w64 설치 실패:",
    "gcc_used": "사용된 GCC:",
    "gcc_error_a1": "G++ 설치 실패.",
    "gcc_error_a2": "G++ 버전 확인 실패:",
    "gcc_error_b1": "G++ 컴파일러를 찾을 수 없습니다. C++ 실행 중단.",
    "gcc_error_b2": "MinGW 컴파일러 설치 실패.\n",
    "cpp_usercode_written": "사용자 C++ 코드가 ***에 작성되었습니다.",
    "gcc_check_a1": "기존 G++ 컴파일러 확인 중...",
    "gcc_check_a2": "MinGW-w64 다운로드 및 설치 중...",
    "gcc_check_a3": "***에서 MinGW-w64 다운로드 중...",
    "gcc_check_a4": "*** MB 다운로드 완료...",
    "gcc_check_a4_5": "총 *** MB 다운로드 완료.",
    "gcc_check_b1": "MinGW-w64 아카이브 압축 해제 중...",
    "gcc_check_b2": "G++ 컴파일러 설치/업데이트 시도 중...",
    "gcc_compilation_attempt": "*** 플래그로 컴파일 시도 중:",
    "gcc_compilation_success": "컴파일 성공, 실행 파일 실행 중...",
    "gcc_compilation_failed": "*** 컴파일 실패, 오류:",
    "gcc_execution_finished": "실행 성공적으로 완료.",
    "gcc_execution_error_a1": "실행 파일 실행 중 오류 발생:",
    "gcc_mingw_addpath": "MinGW-w64 bin 폴더가 PATH에 추가되었습니다:",
    "gcc_compiler_installed": "G++가 성공적으로 설치/업데이트되었습니다.",
    "gcc_found_compiler_ver": "발견된 G++ 버전:",
    "gcc_sufficient_compiler_ver": "G++ 버전이 충분합니다.",
    "gcc_old_compiler_ver": "G++ 버전이 너무 오래되어 업그레이드가 필요합니다.",
    "gcc_mingw_extracted": "압축 해제 완료. MinGW가 다음 위치에 설치되었습니다:",
    "py7zr_installed": "py7zr 패키지가 성공적으로 설치되었습니다.",
    "py7zr_error_a1": "py7zr 패키지를 찾을 수 없어 설치 중...",
    "csc_compiler": "C# 컴파일러 (csc)",
    "cs_usercode_written": "사용자 C# 코드가 ***에 작성되었습니다.",
    "csc_error_a1": "C# 컴파일러 (csc)를 찾을 수 없습니다. 설치 시도 중...\n",
    "csc_error_a2": "CSC 컴파일러를 찾을 수 없고 설치에 실패했습니다. C# 실행 중단.",
    "csc_autoinst_fail": "C# 컴파일러 자동 설치 실패. .NET SDK를 수동으로 설치하십시오.\n",
    "csc_compiler_installed": "C# 컴파일러 (csc) 설치 성공.\n",
    "csc_compiling_with": "다음으로 컴파일 중:",
    "csc_compilation_success": "컴파일 성공.\n",
    "csc_execution_finished": "실행 성공적으로 완료.",
    "csc_execution_error_a1": "실행 파일 실행 시 오류 발생:",
    "sh_platform_not_supported": "사용 중인 플랫폼은 Shell 스크립트 실행을 지원하지 않습니다.",
    "py_error_a1_title": "Python 버전 부족",
    "py_error_a1": "Python 3.13 이상을 설치하십시오.",
    "py_error_a2": "Python 인터프리터를 찾을 수 없습니다.",
    "py_error_a3": "Python 버전을 해석할 수 없습니다.",
    "error_a1": "오류",
    "error_a2": "파일을 열 수 없습니다",
    "error_a3": "파일을 열 수 없습니다:\n",
    "error_a4": "파일에 쓸 수 없습니다:\n",
    "error_a5": "Slash Code 소스 파일을 로드할 수 없습니다. 이유:\n\n",
    "error_c0": "폴더 버튼 업데이트 오류:",
    "error_c1": "메뉴 레이블 업데이트 오류:",
    "error_c2": "파일 레이블 업데이트 오류:",
    "error_c3": "편집 레이블 업데이트 오류:",
    "error_c4": "테마 레이블 업데이트 오류:",
    "error_c5": "실행 레이블 업데이트 오류:",
    "error_c6": "보기 레이블 업데이트 오류:",
    "error_c7": "언어 레이블 업데이트 오류:",
    "error_c8": "GUI 언어 레이블 업데이트 오류:",
    "error_d1": "문서 코드를 실행하는 동안 예외가 발생했습니다. 이유:\n\n",
    "error_d1_5": "문서를 쓰고 실행하는 동안 예외가 발생했습니다. 이유:\n\n",
    "error_d2": "컴파일러가 올바르게 설치되지 않았습니다.",
    "error_e1": "pip가 py7z 설치에 실패했습니다. 이유:",
    "deleting_dirs": "디렉터리 삭제 중: ",
    "directory_del_not_found": "삭제할 디렉터리를 찾을 수 없습니다.",
    "find": "찾기",
    "find_query": "찾기:",
    "find_all": "모두 찾기",
    "replace": "바꾸기",
    "replace_query": "바꿀 내용:",
    "replace_all": "모두 바꾸기",
    "runner_not_found": " 찾을 수 없습니다!\n",
    "install_suggest": "먼저 설치해 주세요.\n",
    "instructions": "설명: ",
    "compilation_error": "컴파일 오류:\n",
    "opened_in_browser": "기본 브라우저에서 열림.",
    "language_not_supported": "실행할 수 없는 언어입니다.",
    "process_error": "프로세스 오류: ",
    "unexpected_error": "예상치 못한 오류: ",
    "cleanup_failed": "정리 실패: ",
    "file": "파일",
    "new": "새 파일",
    "open": "열기",
    "save": "저장",
    "toggle_new_file_saving": "새 파일 저장 토글",
    "clean_temp_files": "임시 파일 정리",
    "clean_temp_directories": "임시 디렉터리 정리",
    "fully_wipe_directories": "임시 디렉터리 완전 삭제",
    "reboot_consolemode": "콘솔 모드에서 재부팅",
    "exit": "종료",
    "edit": "편집",
    "undo": "실행 취소",
    "redo": "다시 실행",
    "language": "언어",
    "theme": "테마",
    "theme_light": "라이트",
    "theme_dark": "다크",
    "theme_dracula": "드라큘라",
    "theme_monokai": "모노카이",
    "theme_night_owl": "나이트 아울",
    "theme_shades_of_purple": "보라색 계열",
    "theme_high_contrast": "고대비",
    "open_folder": "폴더 열기",
    "changed_language_to": "언어 변경됨: ",
    "view": "보기",
    "zoom_in": "확대",
    "zoom_out": "축소",
    "show_sidebar": "사이드바 표시",
    "hide_sidebar": "사이드바 숨기기",
    "show_minimap": "미니맵 표시",
    "hide_minimap": "미니맵 숨기기",
    "show_debug_info": "디버그 정보 표시",
    "hide_debug_info": "디버그 정보 숨기기",
    "toggle_fullscreen": "전체 화면 전환",
    "exit_fullscreen": "전체 화면 종료",
    "run": "실행",
    "run_file": "파일 실행",
    "sc_output": "SC-출력",
    "output_sc_title": "-- Slash Code 텍스트 에디터 | 파일 실행용 SC-출력 --",
    "save_output_text": "출력 텍스트 저장",
    "highlighting_as": "하이라이트 모드: ",
    "plaintext": "일반 텍스트",
    "python": "파이썬",
    "javascript": "자바스크립트",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "마크다운",
    "renpy": "Ren'Py",
    "shell": "Shell 스크립트",
    "python_files": "파이썬 파일",
    "javascript_files": "자바스크립트 파일",
    "html_files": "HTML 파일",
    "c_files": "C 파일",
    "cpp_files": "C++ 파일",
    "header_files": "헤더 파일",
    "text_files": "텍스트 파일",
    "cs_files": "C# 파일",
    "css_files": "CSS 파일",
    "markdown_files": "마크다운 파일",
    "renpy_files": "Ren'Py 파일",
    "shell_files": "Shell 파일",
    "all_files": "모든 파일",
    "binary_file_title": "바이너리 파일 감지됨",
    "binary_file": "이 문서에서 이상한 문자가 감지되었습니다. 열어서 Slash Code가 원시 데이터를 읽도록 하시겠습니까?\n경고: 이로 인해 Slash Code가 느려질 수 있습니다.",
    "session_loaded": "세션 로드됨:",
    "error_b1": "파일 로드 중 오류 발생: ",
    "error_b2": "디렉터리 로드 중 오류 발생: "
    },
    "ar": {
    "gui_lang": "لغة واجهة المستخدم",
    "msys_install": "تم تثبيت MSYS2. يرجى تثبيت MinGW عبر واجهة MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "msys_error_a1": "فشل تثبيت MinGW-w64 بنجاح:",
    "gcc_used": "استخدام GCC:",
    "gcc_error_a1": "فشل تثبيت G++.",
    "gcc_error_a2": "فشل التحقق من إصدار G++:",
    "gcc_error_b1": "لم يتم العثور على مترجم G++. تم إلغاء تشغيل C++.",
    "gcc_error_b2": "فشل تثبيت مترجم MinGW.\n",
    "cpp_usercode_written": "تم كتابة كود C++ الخاص بالمستخدم إلى ***.",
    "gcc_check_a1": "التحقق من وجود مترجم G++ الحالي...",
    "gcc_check_a2": "جاري تنزيل وتثبيت MinGW-w64...",
    "gcc_check_a3": "جاري تنزيل MinGW-w64 من ***...",
    "gcc_check_a4": "*** ميجابايت تم تنزيلها حتى الآن...",
    "gcc_check_a4_5": "تم تنزيل *** ميجابايت إجمالاً.",
    "gcc_check_b1": "جاري استخراج أرشيف MinGW-w64...",
    "gcc_check_b2": "محاولة تثبيت/تحديث مترجم G++...",
    "gcc_compilation_attempt": "محاولة الترجمة مع الخيار ***:",
    "gcc_compilation_success": "تمت الترجمة بنجاح، يجري تشغيل الملف القابل للتنفيذ...",
    "gcc_compilation_failed": "فشلت الترجمة ل*** مع وجود أخطاء:",
    "gcc_execution_finished": "انتهى التنفيذ بنجاح.",
    "gcc_execution_error_a1": "حدث خطأ أثناء محاولة تشغيل الملف القابل للتنفيذ:",
    "gcc_mingw_addpath": "تمت إضافة مجلد MinGW-w64 bin إلى PATH:",
    "gcc_compiler_installed": "تم تثبيت/تحديث G++ بنجاح.",
    "gcc_found_compiler_ver": "تم العثور على إصدار G++:",
    "gcc_sufficient_compiler_ver": "إصدار G++ كافٍ.",
    "gcc_old_compiler_ver": "إصدار G++ لديك قديم جداً ويحتاج إلى التحديث.",
    "gcc_mingw_extracted": "اكتمل الاستخراج. تم تثبيت MinGW في:",
    "py7zr_installed": "تم تثبيت حزمة py7zr بنجاح.",
    "csc_compiler": "مترجم C# (csc)",
    "cs_usercode_written": "تم كتابة كود C# الخاص بالمستخدم إلى ***.",
    "csc_error_a1": "مترجم C# (csc) غير موجود. جارٍ المحاولة للتثبيت...\n",
    "csc_error_a2": "لم يتم العثور على مترجم CSC وفشل التثبيت. تم إيقاف تشغيل C#.",
    "csc_autoinst_fail": "فشل التثبيت التلقائي لمترجم C#. يرجى تثبيت .NET SDK يدوياً.\n",
    "csc_compiler_installed": "تم تثبيت مترجم C# (csc) بنجاح.\n",
    "csc_compiling_with": "جارٍ الترجمة باستخدام:",
    "csc_compilation_success": "تمت الترجمة بنجاح.\n",
    "csc_execution_finished": "انتهى التنفيذ بنجاح.",
    "csc_execution_error_a1": "حدث خطأ أثناء محاولة تشغيل الملف القابل للتنفيذ:",
    "sh_platform_not_supported": "منصتك غير مدعومة لتشغيل سكريبتات Shell Script.",
    "py_error_a1_title": "إصدار Python غير كافٍ",
    "py_error_a1": "يرجى تثبيت Python 3.13 أو أحدث.",
    "py_error_a2": "تعذر العثور على مفسر Python.",
    "py_error_a3": "تعذر تحليل إصدار Python.",
    "error_a1": "خطأ",
    "error_a2": "تعذر فتح الملف",
    "error_a3": "تعذر فتح الملف:\n",
    "error_a4": "تعذر الكتابة إلى الملف:\n",
    "error_a5": "تعذر تحميل ملف مصدر Slash Code. السبب:\n\n",
    "error_c0": "خطأ في تحديث زر المجلد:",
    "error_c1": "خطأ في تحديث وسم القائمة:",
    "error_c2": "خطأ في تحديث وسم الملف:",
    "error_c3": "خطأ في تحديث وسم التحرير:",
    "error_c4": "خطأ في تحديث وسم السمة:",
    "error_c5": "خطأ في تحديث وسم التشغيل:",
    "error_c6": "خطأ في تحديث وسم العرض:",
    "error_c7": "خطأ في تحديث وسم اللغة:",
    "error_c8": "خطأ في تحديث وسم لغة الواجهة:",
    "error_d1": "حدث استثناء أثناء محاولة تنفيذ كود المستند. السبب هو:\n\n",
    "error_d1_5": "حدث استثناء أثناء محاولة الكتابة والتنفيذ للمستند. السبب هو:\n\n",
    "error_d2": "فشل تثبيت المترجم بشكل صحيح.",
    "deleting_dirs": "جار حذف المجلد/المجلدات:",
    "error_e1": "فشل pip في تثبيت py7z. السبب:",
    "directory_del_not_found": "لم يتم العثور على أي مجلدات للحذف.",
    "find": "بحث",
    "find_query": "بحث عن:",
    "find_all": "البحث الكل",
    "replace": "استبدال",
    "replace_query": "استبدال بـ:",
    "replace_all": "استبدال الكل",
    "runner_not_found": " غير موجود!\n",
    "install_suggest": "يرجى تثبيته أولاً.\n",
    "instructions": "تعليمات: ",
    "compilation_error": "خطأ في الترجمة:\n",
    "opened_in_browser": "تم الفتح في المتصفح الافتراضي.",
    "language_not_supported": "اللغة غير مدعومة للتنفيذ.",
    "process_error": "خطأ في العملية: ",
    "unexpected_error": "خطأ غير متوقع: ",
    "cleanup_failed": "فشل التنظيف: ",
    "file": "ملف",
    "new": "جديد",
    "open": "فتح",
    "save": "حفظ",
    "toggle_new_file_saving": "تبديل حفظ الملف الجديد",
    "clean_temp_files": "تنظيف الملفات المؤقتة",
    "clean_temp_directories": "تنظيف الأدلة المؤقتة بالكامل",
    "fully_wipe_directories": "مسح الأدلة المؤقتة بالكامل",
    "reboot_consolemode": "إعادة التشغيل في وضع الكونسول",
    "exit": "خروج",
    "edit": "تحرير",
    "undo": "تراجع",
    "redo": "إعادة",
    "language": "اللغة",
    "theme": "الثيم",
    "theme_light": "فاتح",
    "theme_dark": "داكن",
    "theme_dracula": "دراكولا",
    "theme_monokai": "مونوكاي",
    "theme_night_owl": "البومة الليلية",
    "theme_shades_of_purple": "درجات اللون الأرجواني",
    "theme_high_contrast": "تباين عالي",
    "open_folder": "فتح المجلد",
    "changed_language_to": "تم تغيير اللغة إلى ",
    "view": "عرض",
    "zoom_in": "تكبير",
    "zoom_out": "تصغير",
    "show_sidebar": "إظهار الشريط الجانبي",
    "hide_sidebar": "إخفاء الشريط الجانبي",
    "show_minimap": "إظهار الخريطة المصغرة",
    "hide_minimap": "إخفاء الخريطة المصغرة",
    "show_debug_info": "إظهار معلومات التصحيح",
    "hide_debug_info": "إخفاء معلومات التصحيح",
    "toggle_fullscreen": "تبديل ملء الشاشة",
    "exit_fullscreen": "خروج من ملء الشاشة",
    "run": "تشغيل",
    "run_file": "تشغيل الملف",
    "sc_output": "مخرجات SC",
    "output_sc_title": "-- محرر نصوص Slash Code | مخرجات SC لتشغيل الملفات --",
    "save_output_text": "حفظ نص المخرجات",
    "highlighting_as": "تظليل كالتالي: ",
    "plaintext": "نص عادي",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
    "shell": "نص Shell",
    "python_files": "ملفات Python",
    "javascript_files": "ملفات JavaScript",
    "html_files": "ملفات HTML",
    "c_files": "ملفات C",
    "cpp_files": "ملفات C++",
    "header_files": "ملفات الرأس",
    "text_files": "ملفات نصية",
    "cs_files": "ملفات C#",
    "css_files": "ملفات CSS",
    "markdown_files": "ملفات Markdown",
    "renpy_files": "ملفات Ren'Py",
    "renpy_files": "ملفات Shell",
    "all_files": "جميع الملفات",
    "binary_file_title": "تم اكتشاف ملف ثنائي",
    "binary_file": "تم اكتشاف أحرف غير مألوفة في هذا المستند. هل ترغب في فتحه وقراءة البيانات الخام بواسطة Slash Code؟\nتحذير: قد يبطئ هذا البرنامج.",
    "session_loaded": "تم تحميل الجلسة:",
    "error_b1": "خطأ أثناء تحميل الملف: ",
    "error_b2": "خطأ أثناء تحميل الدليل: "
    }
}

class GUITranslate:
    def __init__(self, lang="en"):
        self.lang = lang
        self.load_lang()
        
    def load_lang(self):
        """
        Loads the language that's been saved from the previous session inside the `.json` language file.
        """
        slash_dir = os.path.expanduser('~/.slashcode')
        os.makedirs(os.path.join(slash_dir, "lang"), exist_ok=True)
        lang_file = os.path.join(slash_dir, f'lang/{self.lang}.json')
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding="utf-8") as f:
                    self.data = json.load(f)
                    return
            except Exception:
                pass
        self.data = GUILANGS.get(self.lang, {})
                
    def get(self, key):
        """
        Returns the key value for the current language key.
        """
        return self.data.get(key, key)
    
    def set_language(self, lang):
        """
        Sets the language using `load_lang()` and passes `self.lang` to the `lang` parameter.
        """
        self.lang = lang
        self.load_lang()
        
translate = GUITranslate()
lang_var = tk.StringVar(value=translate.lang)

menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
edit_menu = tk.Menu(menu, tearoff=0)
theme_menu = tk.Menu(menu, tearoff=0)
view_menu = tk.Menu(menu, tearoff=0)
run_menu = tk.Menu(menu, tearoff=0)
language_menu = tk.Menu(menu, tearoff=0)
guilang_menu = tk.Menu(menu, tearoff=0)
file_index = edit_index = theme_index = view_index = run_index = language_index = guilang_index = None

def highlight_language_change():
    print(translate.get("highlighting_as") + f"{language_var.get().replace("plaintext", translate.get('plaintext').lower())}")
    if os.path.getsize(current_file) > 80000:
        root.after(150, lambda: highlight_document_in_chunks(chunk_size=100))
    else:
        root.after(10, highlight_full_document)

class ToolTip:
    """
    Used for creating custom defined tooltips.
    """
    def __init__(self):
        self.tooltip_window = None
    
    def show(self, event, text):
        if self.tooltip_window:
            return
        x = event.x_root + 10
        y = event.y_root + 10
        self.tooltip_window = tk.Toplevel()
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip_window, text=text,
            background="lightgray" if theme_var == "dark" else "darkgray", relief="solid", borderwidth=1,
            font=("Consolas", 9), wraplength=300
        )
        label.pack()
    
    def hide(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
        
tooltip_manager = ToolTip()

ui_count = 0
def on_lang_change():
    global ui_count
    translate.set_language(lang_var.get())
    lang_map = {
        "en": "English",
        "nl": "Nederlands",
        "de": "Deutsch",
        "es": "Español",
        "it": "Italiano",
        "fr": "Français",
        "jp": "日本語",
        "zh": "中文",
        "ko": "한국인",
        "ar": "عربي"
    }
    lang = lang_var.get()
    lang_name = lang_map.get(lang, lang)
    message = translate.get("changed_language_to") + lang_name

    if lang == "jp":
        message += "に変更されました"

    print(message)
    if ui_count == 0:
        set_ui()
        ui_count += 1
    update_ui_text()

def update_ui_text():
    global open_folder_btn
    global file_menu, edit_menu, theme_menu, view_menu, run_menu, language_menu, guilang_menu
    global file_index, edit_index, theme_index, view_index, run_index, language_index, guilang_index
    try:
        menu.entryconfig(file_index, label=translate.get("file"))
        menu.entryconfig(edit_index, label=translate.get("edit"))
        menu.entryconfig(theme_index, label=translate.get("theme"))
        menu.entryconfig(view_index, label=translate.get("view"))
        menu.entryconfig(run_index, label=translate.get("run"))
        menu.entryconfig(language_index, label=translate.get("language"))
        menu.entryconfig(guilang_index, label=translate.get("gui_lang"))
    except Exception as e:
        print(translate.get("error_c1"), e)

    try:
        file_menu.entryconfig(0, label=translate.get("new"))
        file_menu.entryconfig(1, label=translate.get("open"))
        file_menu.entryconfig(2, label=translate.get("open_folder"))
        file_menu.entryconfig(3, label=translate.get("save"))
        file_menu.entryconfig(5, label=translate.get("toggle_new_file_saving"))
        file_menu.entryconfig(6, label=translate.get("clean_temp_files"))
        file_menu.entryconfig(7, label=translate.get("clean_temp_directories"))
        file_menu.entryconfig(8, label=translate.get("fully_wipe_directories"))
        file_menu.entryconfig(10, label=translate.get("reboot_consolemode"))
        file_menu.entryconfig(12, label=translate.get("exit"))
    except Exception as e:
        print(translate.get("error_c2"), e)

    try:
        edit_menu.entryconfig(0, label=translate.get("undo"))
        edit_menu.entryconfig(1, label=translate.get("redo"))
        edit_menu.entryconfig(3, label=translate.get("find"))
        edit_menu.entryconfig(4, label=translate.get("replace"))
    except Exception as e:
        print(translate.get("error_c3"), e)

    try:
        theme_menu.entryconfig(0, label=translate.get("theme_light"))
        theme_menu.entryconfig(1, label=translate.get("theme_dark"))
        theme_menu.entryconfig(2, label=translate.get("theme_dracula"))
        theme_menu.entryconfig(3, label=translate.get("theme_monokai"))
        theme_menu.entryconfig(4, label=translate.get("theme_night_owl"))
        theme_menu.entryconfig(5, label=translate.get("theme_shades_of_purple"))
        theme_menu.entryconfig(6, label=translate.get("theme_high_contrast"))
    except Exception as e:
        print(translate.get("error_c4"), e)

    try:
        view_menu.entryconfig(0, label=translate.get("zoom_in"))
        view_menu.entryconfig(1, label=translate.get("zoom_out"))
        view_menu.entryconfig(3, label=translate.get("show_sidebar"))
        view_menu.entryconfig(4, label=translate.get("hide_sidebar"))
        view_menu.entryconfig(5, label=translate.get("show_minimap"))
        view_menu.entryconfig(6, label=translate.get("hide_minimap"))
        view_menu.entryconfig(8, label=translate.get("show_debug_info"))
        view_menu.entryconfig(9, label=translate.get("hide_debug_info"))
        view_menu.entryconfig(11, label=translate.get("toggle_fullscreen"))
        view_menu.entryconfig(12, label=translate.get("exit_fullscreen"))
    except Exception as e:
        print(translate.get("error_c5"), e)

    try:
        run_menu.entryconfig(0, label=translate.get("run_file"))
    except Exception as e:
        print(translate.get("error_c6"), e)

    try:
        language_menu.entryconfig(0, label=translate.get("plaintext"))
        language_menu.entryconfig(1, label=translate.get("python"))
        language_menu.entryconfig(2, label=translate.get("javascript"))
        language_menu.entryconfig(3, label=translate.get("css"))
        language_menu.entryconfig(4, label=translate.get("html"))
        language_menu.entryconfig(5, label=translate.get("cpp"))
        language_menu.entryconfig(6, label=translate.get("cs"))
        language_menu.entryconfig(7, label=translate.get("markdown"))
        language_menu.entryconfig(8, label=translate.get("renpy"))
        language_menu.entryconfig(9, label=translate.get("shell"))
    except Exception as e:
        print(translate.get("error_c7"), e)
        
    if open_folder_btn:
        try:
            open_folder_btn.config(text=translate.get("open_folder"))
        except Exception as e:
            print(translate.get("error_c0"), e)
            
    try:
        guilang_menu.entryconfig(0, label="English")
        guilang_menu.entryconfig(1, label="Nederlands")
        guilang_menu.entryconfig(2, label="Deutsch")
        guilang_menu.entryconfig(3, label="Español")
        guilang_menu.entryconfig(4, label="Italiano")
        guilang_menu.entryconfig(5, label="Français")
        guilang_menu.entryconfig(6, label="日本語")
        guilang_menu.entryconfig(7, label="中文")
        guilang_menu.entryconfig(8, label="한국인")
        guilang_menu.entryconfig(9, label="عربي")
    except Exception as e:
        print(translate.get("error_c8"), e)

def create_sidebar_buttons():
    global open_folder_btn
    open_folder_btn = tk.Button(
        sidebar,
        text=translate.get("open_folder"),
        command=lambda: None,
        bg=themes[theme_var.get()]['bg'],
        fg=themes[theme_var.get()]['fg']
    )
    open_folder_btn.pack(fill=tk.X, pady=4)

py_keywords = set(keyword.kwlist)
py_keywords.add("match")
py_keywords.add("case")
renpy_kw = {
    'label', 'menu', 'jump', 'call', 'return', 'if', 'elif', 'else', 'while', 'for', 'init', 'python', 
    'screen', 'show', 'hide', 'scene', 'with', 'as', 'define', 'default', 'image', 'transform', 'style', 'window', 'say',
    'play', 'stop', 'pause', 'voice', 'queue', 'extend', 'narrator', 'character', 'set', 'add', 'remove', 'on',
    'at', 'from', 'to', 'block', 'pass', 'break', 'continue', 'early', 'all',
    'init', 'init', 'offset', 'init python', 'init python early', 'init python hide', 'init python in',
    'style_group', 'style_prefix', 'showif', 'hideif', 'onlayer', 'zorder', 'key', 'timer', 'viewport', 'vbox',
    'hbox', 'grid', 'textbutton', 'imagebutton', 'imagemap', 'bar', 'slider', 'input', 'hotspot', 'hotbar', 'fixed',
    'frame', 'button', 'action', 'xalign', 'yalign', 'align', 'pos', 'xpos', 'ypos', 'text', 'size', 'xsize', 'ysize', 'modal',
    'ground', 'selected', 'insensitive', 'idle', 'hover', 'activate', 'deactivate', 'selected_hover',
    'selected_idle', 'insensitive_hover', 'insensitive_idle', 'insensitive_selected', 'insensitive_selected_idle',
    'insensitive_selected_hover', 'selected_activate', 'selected_deactivate', 'selected_insensitive',
    'selected_insensitive_idle', 'selected_insensitive_hover', 'window show', 'window hide', 'window auto', 
    'window none', 'window', 'voice', 'queue', 'extend',
    'renpy', 'define', 'default', 'config', 'persistent', 'store', 'gui', 'style', 'theme', 'has'
    }
renpy_kw.update(py_keywords)

LANGUAGE_KEYWORDS = {
    'python': py_keywords,
    'javascript': {
    'await', 'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
    'default', 'delete', 'do', 'else', 'enum', 'export', 'extends', 'false',
    'finally', 'for', 'function', 'if', 'implements', 'import', 'in', 'instanceof',
    'interface', 'let', 'new', 'null', 'package', 'private', 'protected', 'public',
    'return', 'static', 'super', 'switch', 'this', 'throw', 'true', 'try', 'typeof',
    'var', 'void', 'while', 'with', 'yield', 'async', 'arguments', 'eval', '=>'
    },
    'cpp': {
        'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool',
        'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t', 'class', 'compl',
        'concept', 'const', 'consteval', 'constexpr', 'constinit', 'const_cast', 'continue',
        'co_await', 'co_return', 'co_yield', 'decltype', 'default', 'delete', 'do', 'double',
        'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern', 'false', 'final',
        'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable',
        'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or',
        'or_eq', 'override', 'private', 'protected', 'public', 'register', 'reinterpret_cast',
        'requires', 'return', 'short', 'signed', 'sizeof', 'static', 'static_assert',
        'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw',
        'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using',
        'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
    },
    'html': {
        'html', 'head', 'title', 'base', 'link', 'meta', 'style', 'body', 'address', 'article',
        'aside', 'footer', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'main', 'nav', 'section',
        'blockquote', 'dd', 'div', 'dl', 'dt', 'figcaption', 'figure', 'hr', 'li', 'ol', 'p', 'pre', 'ul',
        'a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em', 'i', 'kbd', 'mark',
        'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'small', 'span', 'strong', 'sub', 'sup',
        'time', 'u', 'var', 'wbr', 'del', 'ins', 'area', 'audio', 'img', 'map', 'track', 'video',
        'canvas', 'figcaption', 'figure', 'picture', 'svg', 'math', 'noscript', 'script', 'template',
        'caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'button',
        'datalist', 'fieldset', 'form', 'input', 'label', 'legend', 'meter', 'optgroup', 'option',
        'output', 'progress', 'select', 'textarea', 'details', 'dialog', 'menu', 'summary', 'slot',
        'acronym', 'applet', 'basefont', 'bgsound', 'big', 'blink', 'center', 'command', 'content',
        'dir', 'element', 'font', 'frame', 'frameset', 'image', 'isindex', 'keygen', 'listing', 'marquee',
        'menuitem', 'multicol', 'nextid', 'nobr', 'noembed', 'noframes', 'plaintext', 'rb', 'rtc',
        'shadow', 'spacer', 'strike', 'tt', 'xmp', 'object', 'param', 'source', 'embed', 'output'
    },
    'cs': {
    'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const', 'continue',
    'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern', 'false', 'finally',
    'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 'is', 'lock',
    'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params', 'private', 'protected',
    'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string',
    'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort',
    'using', 'virtual', 'void', 'volatile', 'while'
    },
    'renpy': renpy_kw,
    'shell': {
    '!', '[', ']', '{', '}', 'case', 'coproc', 'do', 'done', 'elif',
    'else', 'esac', 'fi', 'for', 'function', 'if', 'in', 'select',
    'then', 'until', 'while', 'time', 'declare', 'local', 'readonly', 'return', 'exit',
    'break', 'continue', 'export', 'readonly', 'shift', 'getopts', 'eval', 'exec', 'source', '.',
    'test', 'let', 'true', 'false', 'trap', 'kill', 'wait', 'read', 'pwd', 'cd',
    'pushd', 'popd', 'dirs', 'type', 'command', 'jobs', 'fg', 'bg', 'disown', 'echo',
    'help', 'alias', 'unalias', 'set', 'umask', 'ulimit', 'enable', ':', 'declare', 'typeset',
    'set', 'pushd', 'popd', 'dirs', 'jobs', 'fg', 'bg', 'disown', 'help', 'alias', 'unalias',
    'enable', 'umask', 'ulimit', 'type', 'command'
    }
}
SHELL_TEST_OPERATORS = {
    '-z', '-n', '-d', '-e', '-f', '-r', '-w', '-x', '-s', '-l', '-L', '-h',
    '-b', '-c', '-p', '-S', '-t', '-O', '-G', '-k', '-u', '-g', 
    '-nt', '-ot', '-ef', '-eq', '-ne', '-lt', '-le', '-gt', '-ge', '-a', '-o'
}

renpy_fn = {
        'renpy.say', 'renpy.scene', 'renpy.show', 'renpy.hide', 'renpy.jump', 'renpy.call',
        'renpy.pause', 'renpy.play', 'renpy.stop', 'renpy.notify', 'renpy.input',
        'renpy.open_url', 'renpy.queue_event', 'renpy.rollback', 'renpy.save', 'renpy.load',
        'renpy.quit', 'renpy.music.stop', 'renpy.music.play', 'renpy.music.set_volume',
        'renpy.music.get_pos', 'renpy.music.get_playing', 'renpy.music.get_queue',
        'renpy.music.set_pan', 'renpy.music.set_loop', 'renpy.music.set_fadein',
        'renpy.music.set_fadeout', 'renpy.show_screen', 'renpy.hide_screen',
        'renpy.get_screen', 'renpy.get_screen_variable', 'renpy.set_screen_variable',
        'renpy.invoke_in_thread', 'renpy.invoke_in_main_thread', 'renpy.restart_interaction',
        'renpy.get_mouse_pos', 'renpy.get_on_battery', 'renpy.get_physical_size',
        'renpy.get_refresh_rate', 'renpy.get_renderer_info', 'renpy.get_say_image_tag',
        'renpy.get_say_attributes', 'renpy.get_placement', 'renpy.get_registered_image',
        'renpy.get_return_stack', 'renpy.get_sdl_dll', 'renpy.get_sdl_window_pointer',
        'renpy.is_init_phase', 'renpy.is_mouse_visible', 'renpy.is_pixel_opaque',
        'renpy.is_seen', 'renpy.is_selected', 'renpy.is_sensitive', 'renpy.is_skipping',
        'renpy.is_start_interact', 'renpy.list_files', 'renpy.list_images', 'renpy.load_module',
        'renpy.load_string', 'renpy.maximum_framerate', 'renpy.notify', 'renpy.open_url',
        'renpy.predicting', 'renpy.queue_event', 'renpy.quit', 'renpy.rollback', 'renpy.run',
        'renpy.save', 'renpy.say', 'renpy.scene', 'renpy.screenshot', 'renpy.set_autoreload',
        'renpy.set_focus', 'renpy.set_mouse_pos', 'renpy.set_physical_size', 'renpy.set_return_stack',
        'renpy.set_screen_variable', 'renpy.show', 'renpy.show_layer_at', 'renpy.show_screen',
        'renpy.showing', 'renpy.shown_window', 'renpy.split_properties', 'renpy.stop_skipping',
        'renpy.transition', 'renpy.try_compile', 'renpy.try_eval', 'renpy.version', 'renpy.vibrate',
        'renpy.warp_to_line', 'renpy.watch', 'renpy.with_statement'
    }
renpy_fn.update(dir(builtins))

LANGUAGE_FUNCS = {
    'python': dir(builtins),
    'javascript': {
        'alert', 'prompt', 'confirm', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval',
        'parseInt', 'parseFloat', 'isNaN', 'isFinite', 'decodeURI', 'decodeURIComponent',
        'encodeURI', 'encodeURIComponent', 'escape', 'unescape', 'eval',
        'console.log', 'console.error', 'console.warn', 'console.info', 'console.debug',
        'map', 'filter', 'reduce', 'forEach', 'find', 'findIndex', 'some', 'every', 'includes',
        'slice', 'splice', 'sort', 'concat', 'push', 'pop', 'shift', 'unshift', 'join', 'reverse',
        'flat', 'flatMap', 'indexOf', 'lastIndexOf', 'copyWithin', 'fill', 'entries', 'keys', 'values',
        'charAt', 'charCodeAt', 'concat', 'includes', 'indexOf', 'lastIndexOf', 'match', 'replace',
        'search', 'slice', 'split', 'startsWith', 'endsWith', 'substring', 'toLowerCase',
        'toUpperCase', 'trim', 'padStart', 'padEnd', 'repeat',
        'Object.keys', 'Object.values', 'Object.entries', 'Object.assign', 'Object.hasOwn',
        'Object.create', 'Object.freeze', 'Object.seal', 'Object.defineProperty',
        'Math.abs', 'Math.ceil', 'Math.floor', 'Math.round', 'Math.max', 'Math.min', 'Math.pow',
        'Math.random', 'Math.sqrt', 'Math.trunc', 'Math.sign',
        'JSON.stringify', 'JSON.parse',
        'addEventListener', 'removeEventListener', 'querySelector', 'querySelectorAll',
        'getElementById', 'getElementsByClassName', 'getElementsByTagName', 'setAttribute',
        'getAttribute', 'fetch',
        'Promise', 'then', 'catch', 'finally', 'async', 'await'
    },
    'cpp': {
        'sort', 'find', 'find_if', 'copy', 'fill', 'accumulate', 'transform', 'count',
        'count_if', 'max', 'min', 'minmax', 'lower_bound', 'upper_bound', 'equal_range',
        'binary_search', 'merge', 'reverse', 'unique', 'remove', 'remove_if', 'swap',
        'replace', 'replace_if', 'rotate', 'partition', 'stable_partition', 'shuffle',
        'is_sorted', 'is_heap', 'all_of', 'any_of', 'none_of', 'for_each',
        'abs', 'sqrt', 'pow', 'exp', 'log', 'log10', 'sin', 'cos', 'tan', 'asin', 'acos',
        'atan', 'atan2', 'ceil', 'floor', 'round', 'fmod', 'remainder',
        'strlen', 'strcpy', 'strcat', 'strcmp', 'strncpy', 'strncat', 'strncmp',
        'strchr', 'strrchr', 'strstr', 'strtok',
        'substr', 'find', 'rfind', 'replace', 'erase', 'insert',
        'rand', 'srand', 'exit', 'malloc', 'free', 'calloc', 'realloc',
        'vector', 'push_back', 'string',
        'cout', 'cin', 'endl', 
        'printf', 'scanf', 'fopen' # C functions in case they're used.
    },
    'html': {}, # HTML doesn't have any functions (you'd need to use JavaScript).
    'cs': {
    'Console.WriteLine', 'Console.ReadLine', 'Math.Abs', 'Math.Pow', 'Math.Sqrt', 'ToString', 'Equals', 'GetHashCode', 'GetType', 'Parse'
    },
    'markdown': {
        '#', '##', '###', '####', '#####', '######', '-', '*', '+', '>', 
        '`', '```', '_', '__'
    },
    'renpy': renpy_fn,
    'shell': set()
}

LANGUAGE_TYPES = {
    "cpp": {
        "int", "float", "double", "char", "void", "bool", "short", "long", "unsigned", "signed",
        "size_t", "std::string", "std::vector", "std::map", "std::set", "std::array", "wchar_t",
        "auto", "decltype", "std::shared_ptr", "std::unique_ptr", "std::weak_ptr"
    },
    "python": {
        "int", "float", "str", "bool", "list", "tuple", "dict", "set", "object", "bytes"
    },
    "javascript": {
        "Number", "String", "Boolean", "Array", "Object", "Function", "Symbol", "BigInt"
    },
    "html": set(),
    "cs": {
    'int', 'float', 'double', 'decimal', 'string', 'char', 'bool', 'object', 'var', 'dynamic', 'long', 'short', 'byte', 'uint', 'ulong', 'ushort', 'sbyte'
    },
    "markdown": set(),
    "renpy": {
        "int", "float", "str", "bool", "list", "tuple", "dict", "set", "object", "bytes"
    },
    "shell": set()
}

html_attrs = {
    'id', 'class', 'style', 'src', 'href', 'alt', 'title', 'type', 'value', 'name',
    'placeholder', 'for', 'action', 'method', 'target', 'rel', 'disabled', 'checked',
    'selected', 'required', 'readonly', 'autofocus', 'maxlength', 'min', 'max'
} # Attributes like <div **style="...">.

TOOLTIP_INFO = {
    'python': {
        'keywords': {
            'def': 'Defines a function. This can be used in your script by calling it, using the name plus the parentheses -> (), that will execute the function.',
            'class': 'Defines a class that you can use as an instance by making a variable that holds the value of the class.', 
            'if': 'A conditional statement to check whether the condition after the if keyword is truthy or not.',
            'else': 'A conditional statement that runs only if the previous conditions did not run as the conditions weren\'t truthy.',
            'elif': 'An additional conditional statement to give a different conditional a chance to be run (if truthy) if the previous statement wasn\'t truthy.',
            'for': 'Creates a loop inside of an iterable that ends after there isn\'t any more elements inside of the iterable. The use of the for statement is \"for i in some_iterable:\".',
            'while': 'While a certain condition is truthy, the loop inside of the while block will keep running until it becomes false.',
            'return': 'Returns a certain value from a function. This is useful as you can get the result of the output of the function inside of a variable so you can use it for other things.',
            'import': 'Imports a module which you can use for different occurrences. People may import a module if something they need already exists in a public package/module.',
            'from': 'Imports specific items from a module, not the entire module.',
            'try': 'Attempts to run a code block while an exception doesn\'t occur.',
            'except': 'Handles an exception detected from a try block. If the try block did not succeed in fully executing, the except block will be executed instead.',
            'with': 'A context manager to execute code with.',
            'as': 'Gives a certain alias to an item which you can use as that name as well.',
            'lambda': 'An anonymous function that is not manually hardcoded by the user itself but more a function that has the purpose of just returning something.',
        },
        'functions': {
            'print': 'Outputs text to console and buffers to the stream if the flush parameter isn\'t truthy. The object inputted inside of the print function will get parsed, evaluated and get converted into a string to properly print the output to the console.',
            'len': 'Gets length of an object of an iterable, whether that may be an integer, list, set, etc. This can be used to check the amount of items in a huge list, for example.',
            'range': 'Generates a sequence of numbers and can be used in a for loop to do something every time a loop finishes.',
            'str': 'Converts an object to a string or may be used as an object type specifier.',
            'int': 'Converts an object to an integer or may be used as an object type specifier.',
            'list': 'May be used as an object type specifier or may be used with parentheses to convert an object to a list of iterables.',
            'dict': 'May be used as an object type specifier or may be used with parentheses to convert an object to a dictionary of key-value pairs.',
            'open': 'Opens a file object with the type of TextIOWrapper[_WrappedBuffer] to convert the content of a file to a string for reading and writing. It is most likely you\'ll use the as keyword to genuinely execute an action with the file itself.',
            'input': 'Gets user input and returns the text the user inputted into the stream. This may be used as a confirmation for something important or anything else.',
            'type': 'Checks the type of the object and returns it. In Python 3.13, this keyword can also indicate the beginning of a \'type statement\'.',
        }
    },
    'javascript': {
        'keywords': {
            'function': 'Defines a function. Example: function myFunc() {}',
            'var': 'Declares a variable (function-scoped).',
            'let': 'Declares a block-scoped variable.',
            'const': 'Declares a block-scoped, read-only variable.',
            'if': 'Conditional statement.',
            'else': 'Alternative block for if statement.',
            'for': 'Creates a loop. Example: for (let i=0; i<5; i++) {}',
            'while': 'Loop that runs while a condition is true.',
            'do': 'Used with while for do...while loops.',
            'switch': 'Selects among multiple cases.',
            'case': 'Defines a case in a switch statement.',
            'break': 'Exits a loop or switch.',
            'continue': 'Skips to next loop iteration.',
            'return': 'Returns a value from a function.',
            'try': 'Starts a try...catch error handling block.',
            'catch': 'Handles errors from try block.',
            'finally': 'Executes after try/catch, regardless of outcome.',
            'throw': 'Throws an exception.',
            'class': 'Defines a class.',
            'extends': 'Inherits from another class.',
            'import': 'Imports a module.',
            'export': 'Exports a module or function.',
            'new': 'Creates a new instance of an object.',
            'this': 'Refers to the current object.',
            'super': 'Calls parent class constructor or method.',
            'typeof': 'Returns the type of a variable.',
            'instanceof': 'Checks object type at runtime.',
            'delete': 'Deletes an object property.',
            'in': 'Checks if a property exists in an object.',
            'await': 'Waits for a Promise to resolve (async functions).',
            'async': 'Declares an async function.',
            'yield': 'Pauses and resumes a generator function.',
            'default': 'Specifies default case in switch or default export.',
            'with': 'Extends scope chain for a statement (deprecated).',
            'void': 'Evaluates an expression without returning value.',
            'enum': 'Defines an enumerated type.',
            'static': 'Defines a static method or property.',
            'public': 'Public class field (ES2022).',
            'private': 'Private class field (ES2022).',
            'protected': 'Protected class field (TypeScript/ES2022).',
            'package': 'Reserved for future use.',
            'interface': 'TypeScript: defines a contract for objects.'
        },
        'functions': {
            'alert': 'Displays an alert dialog.',
            'prompt': 'Displays a prompt dialog for user input.',
            'confirm': 'Displays a confirmation dialog.',
            'console.log': 'Logs output to the browser console.',
            'setTimeout': 'Calls a function after a delay.',
            'setInterval': 'Calls a function repeatedly at intervals.',
            'clearTimeout': 'Cancels a timeout set by setTimeout.',
            'clearInterval': 'Cancels an interval set by setInterval.',
            'parseInt': 'Parses a string and returns an integer.',
            'parseFloat': 'Parses a string and returns a floating-point number.',
            'isNaN': 'Checks if a value is NaN (Not a Number).',
            'isFinite': 'Checks if a value is a finite number.',
            'JSON.stringify': 'Converts a JavaScript object to a JSON string.',
            'JSON.parse': 'Parses a JSON string into a JavaScript object.',
            'fetch': 'Performs HTTP requests (returns a Promise).',
            'addEventListener': 'Adds an event listener to an element.',
            'removeEventListener': 'Removes an event listener from an element.',
            'querySelector': 'Selects the first element matching a CSS selector.',
            'querySelectorAll': 'Selects all elements matching a CSS selector.',
            'getElementById': 'Gets an element by its ID.',
            'getElementsByClassName': 'Gets elements by class name.',
            'getElementsByTagName': 'Gets elements by tag name.',
            'map': 'Creates a new array by applying a function to each element.',
            'filter': 'Creates a new array with elements that pass a test.',
            'reduce': 'Reduces an array to a single value.',
            'forEach': 'Executes a function for each array element.',
            'Math.random': 'Returns a random number between 0 and 1.',
            'Math.floor': 'Rounds a number down.',
            'Math.ceil': 'Rounds a number up.',
            'Math.round': 'Rounds a number to the nearest integer.',
            'Math.abs': 'Returns the absolute value.'
        }
    },
    'cpp': {
        'keywords': {
            'int': 'Integer data type.',
            'float': 'Floating-point data type.',
            'double': 'Double-precision floating-point.',
            'char': 'Character data type.',
            'void': 'No return value or type.',
            'bool': 'Boolean data type (true/false).',
            'class': 'Defines a class.',
            'struct': 'Defines a structure.',
            'enum': 'Defines an enumerated type.',
            'namespace': 'Defines a namespace.',
            'template': 'Defines a template for generic programming.',
            'public': 'Public access specifier.',
            'private': 'Private access specifier.',
            'protected': 'Protected access specifier.',
            'virtual': 'Declares a virtual function.',
            'override': 'Overrides a virtual function.',
            'const': 'Declares a constant value.',
            'static': 'Declares a static member.',
            'new': 'Allocates memory dynamically.',
            'delete': 'Deallocates memory.',
            'try': 'Begins a try-catch block.',
            'catch': 'Catches exceptions.',
            'throw': 'Throws an exception.',
            'using': 'Introduces a namespace or alias.',
            'return': 'Returns a value from a function.',
            'if': 'Conditional statement.',
            'else': 'Alternative block for if.',
            'for': 'Loop with initialization, condition, increment.',
            'while': 'Loop that runs while a condition is true.',
            'do': 'Used with while for do...while loops.',
            'break': 'Exits a loop.',
            'continue': 'Skips to next loop iteration.',
            'switch': 'Selects among multiple cases.',
            'case': 'Defines a case in a switch statement.',
            'default': 'Specifies default case in switch.',
            'sizeof': 'Returns the size of a type or variable.',
            'typedef': 'Creates a type alias.',
            'friend': 'Grants access to private/protected members.',
            'operator': 'Overloads an operator.',
            'this': 'Pointer to the current object.',
            'nullptr': 'Null pointer constant.',
            'true': 'Boolean true value.',
            'false': 'Boolean false value.'
        },
        'functions': {
            'std::cout': 'Outputs to standard output (console).',
            'std::cin': 'Inputs from standard input (console).',
            'printf': 'C function for formatted output.',
            'scanf': 'C function for formatted input.',
            'main': 'Entry point of a C++ program.',
            'sort': 'Sorts elements in a range.',
            'find': 'Finds an element in a range.',
            'push_back': 'Adds element to the end of a vector.',
            'pop_back': 'Removes last element from a vector.',
            'size': 'Returns the number of elements.',
            'begin': 'Returns iterator to beginning.',
            'end': 'Returns iterator to end.',
            'abs': 'Returns the absolute value.',
            'sqrt': 'Returns the square root.',
            'pow': 'Raises to a power.',
            'exit': 'Terminates the program.'
        }
    },
    'html': {
        'keywords': {
            'html': 'Root element of an HTML page.',
            'head': 'Container for metadata.',
            'body': 'Main content of the document.',
            'div': 'Generic container element.',
            'span': 'Inline container element.',
            'a': 'Defines a hyperlink.',
            'img': 'Embeds an image.',
            'script': 'Embeds or references JavaScript.',
            'style': 'Defines CSS styles.',
            'form': 'Defines an input form.',
            'input': 'Single-line text input field.',
            'button': 'Clickable button.',
            'table': 'Table element.',
            'tr': 'Table row.',
            'td': 'Table cell.',
            'th': 'Table header cell.',
            'ul': 'Unordered list.',
            'ol': 'Ordered list.',
            'li': 'List item.',
            'h1': 'Top-level heading.',
            'h2': 'Second-level heading.',
            'h3': 'Third-level heading.',
            'p': 'Paragraph.',
            'br': 'Line break.',
            'link': 'Defines relationship to external resource (usually CSS).',
            'meta': 'Specifies metadata.'
        },
        'functions': {}
    },
    'cs': {
        'keywords': {
            'class': 'Defines a class (blueprint for objects).',
            'struct': 'Defines a value type structure.',
            'interface': 'Defines a contract that classes/structs can implement.',
            'enum': 'Defines an enumeration of named constants.',
            'namespace': 'Declares a scope for identifiers.',
            'using': 'Imports namespaces or creates an alias.',
            'public': 'Access modifier: accessible from anywhere.',
            'private': 'Access modifier: accessible only within the class.',
            'protected': 'Access modifier: accessible in class and subclasses.',
            'internal': 'Access modifier: accessible within the same assembly.',
            'static': 'Belongs to the type itself, not an instance.',
            'void': 'Indicates no return value.',
            'int': '32-bit integer type.',
            'float': 'Single-precision floating point type.',
            'double': 'Double-precision floating point type.',
            'decimal': '128-bit precise decimal type.',
            'string': 'Sequence of characters.',
            'char': 'Single character type.',
            'bool': 'Boolean value (true/false).',
            'object': 'Base type for all objects.',
            'var': 'Implicitly typed local variable.',
            'new': 'Creates a new instance.',
            'return': 'Returns a value from a method.',
            'if': 'Conditional statement.',
            'else': 'Alternative block for if.',
            'switch': 'Selects among multiple cases.',
            'case': 'Defines a case in switch.',
            'default': 'Default case in switch.',
            'for': 'Loop with initializer, condition, increment.',
            'foreach': 'Loop over items in a collection.',
            'while': 'Loop while condition is true.',
            'do': 'Do-while loop.',
            'break': 'Exits a loop or switch.',
            'continue': 'Skips to next iteration of loop.',
            'try': 'Starts a try-catch-finally block.',
            'catch': 'Handles exceptions from try block.',
            'finally': 'Executes after try/catch, always runs.',
            'throw': 'Throws an exception.',
            'true': 'Boolean true value.',
            'false': 'Boolean false value.',
            'null': 'Represents no value.',
            'this': 'Reference to current instance.',
            'base': 'Reference to base class.',
            'override': 'Overrides a base class method.',
            'virtual': 'Allows method to be overridden.',
            'abstract': 'Declares an abstract class or method.',
            'sealed': 'Prevents a class from being inherited.',
            'readonly': 'Value can only be assigned in declaration or constructor.',
            'const': 'Constant value (must be assigned at declaration).',
            'params': 'Specifies a method parameter that takes a variable number of arguments.',
            'operator': 'Overloads an operator.',
            'implicit': 'Defines an implicit conversion.',
            'explicit': 'Defines an explicit conversion.',
            'get': 'Accessor for a property.',
            'set': 'Mutator for a property.',
            'partial': 'Defines a partial class, struct, or method.',
            'async': 'Defines an asynchronous method.',
            'await': 'Waits for an async operation to complete.',
            'lock': 'Ensures that one thread does not enter a critical section of code while another thread is in that section.',
            'yield': 'Returns each element one at a time.',
            'nameof': 'Returns the name of a variable, type, or member as a string.',
            'typeof': 'Gets the System.Type of a type.',
            'is': 'Checks if an object is compatible with a type.',
            'as': 'Performs conversions between compatible types.',
            'dynamic': 'Bypasses compile-time type checking.',
            'delegate': 'Defines a type that references methods.',
            'event': 'Declares an event.',
            'extern': 'Declares a method that is implemented externally.',
            'unsafe': 'Allows code that uses pointers.',
            'fixed': 'Prevents the garbage collector from relocating a variable.',
            'checked': 'Enables overflow checking for integral-type arithmetic operations.',
            'unchecked': 'Suppresses overflow checking.',
            'goto': 'Transfers control to a labeled statement.',
            'sizeof': 'Returns the size in bytes of a type.',
            'stackalloc': 'Allocates a block of memory on the stack.',
            'add': 'Defines a custom event accessor.',
            'remove': 'Defines a custom event accessor.',
        },
        'functions': {
            'Console.WriteLine': 'Writes a line of text to the console.',
            'Console.ReadLine': 'Reads a line of input from the console.',
            'Math.Abs': 'Returns the absolute value of a number.',
            'Math.Pow': 'Raises a number to a specified power.',
            'Math.Sqrt': 'Returns the square root of a number.',
            'ToString': 'Converts an object to its string representation.',
            'Equals': 'Determines whether two object instances are equal.',
            'GetHashCode': 'Returns a hash code for the object.',
            'GetType': 'Gets the type of the current instance.',
            'Parse': 'Converts a string to a numeric type.',
            'TryParse': 'Tries to convert a string to a numeric type, returns success as bool.',
            'Substring': 'Retrieves a substring from a string.',
            'IndexOf': 'Reports the zero-based index of the first occurrence of a string.',
            'Replace': 'Replaces all occurrences of a specified string.',
            'Split': 'Splits a string into an array of substrings.',
            'Join': 'Concatenates an array of strings.',
            'Trim': 'Removes all leading and trailing white-space characters.',
            'StartsWith': 'Determines whether the beginning of this string matches a specified string.',
            'EndsWith': 'Determines whether the end of this string matches a specified string.',
            'Contains': 'Checks if a string contains a specified substring.',
            'Add': 'Adds an object to the end of a collection.',
            'Remove': 'Removes the first occurrence of a specific object.',
            'Insert': 'Inserts an element into the collection at the specified index.',
            'Clear': 'Removes all elements from the collection.',
            'Count': 'Gets the number of elements in the collection.',
            'Sort': 'Sorts the elements in the collection.',
            'Reverse': 'Reverses the order of the elements in the collection.',
        }
    },
    'css': {
        'keywords': {
            '@import': 'Imports an external stylesheet into the current file.',
            '@media': 'Defines media queries for responsive design.',
            '@font-face': 'Allows custom fonts to be loaded.',
            '@keyframes': 'Defines CSS animations.',
            '@supports': 'Checks if the browser supports a CSS feature.',
            '@charset': 'Specifies the character encoding of the stylesheet.',
            '@namespace': 'Declares an XML namespace.',
            'color': 'Sets the text color of an element.',
            'background': 'Sets all background style properties at once.',
            'background-color': 'Specifies the background color of an element.',
            'font-family': 'Specifies the font for an element.',
            'font-size': 'Specifies the size of the font.',
            'font-weight': 'Specifies the weight (boldness) of the font.',
            'margin': 'Sets the outer margin of an element.',
            'padding': 'Sets the inner padding of an element.',
            'border': 'Sets the border properties of an element.',
            'width': 'Sets the width of an element.',
            'height': 'Sets the height of an element.',
            'display': 'Specifies how an element is displayed (block, inline, etc).',
            'position': 'Specifies the positioning method (static, relative, absolute, fixed, sticky).',
            'top': 'Specifies the top position of a positioned element.',
            'left': 'Specifies the left position of a positioned element.',
            'right': 'Specifies the right position of a positioned element.',
            'bottom': 'Specifies the bottom position of a positioned element.',
            'z-index': 'Sets the stack order of a positioned element.',
            'overflow': 'Specifies what happens if content overflows an element\'s box.',
            'opacity': 'Sets the transparency level of an element.',
            'cursor': 'Specifies the type of mouse cursor to be displayed.',
            'box-shadow': 'Attaches one or more shadows to an element.',
            'text-align': 'Specifies the horizontal alignment of text.',
            'vertical-align': 'Specifies the vertical alignment of an inline or table-cell box.',
            'float': 'Specifies whether or not an element should float.',
            'clear': 'Specifies what elements can float beside the cleared element and on which side.',
            'transition': 'Defines the transition between two states of an element.',
            'transform': 'Applies a 2D or 3D transformation to an element.',
            'animation': 'A shorthand property for all animation properties.',
            'visibility': 'Specifies whether an element is visible or hidden.',
            'background-image': 'Sets one or more background images for an element.',
            'background-size': 'Specifies the size of the background images.',
            'background-position': 'Specifies the starting position of a background image.',
            'background-repeat': 'Sets if/how a background image will be repeated.',
            'border-radius': 'Defines the radius of the element\'s corners.',
            'min-width': 'Sets the minimum width of an element.',
            'max-width': 'Sets the maximum width of an element.',
            'min-height': 'Sets the minimum height of an element.',
            'max-height': 'Sets the maximum height of an element.',
            'content': 'Used with ::before and ::after to insert generated content.',
            'outline': 'Sets the outline on elements.',
            'list-style': 'Sets all the properties for a list in one declaration.',
            'pointer-events': 'Defines whether or not an element reacts to pointer events.',
            'filter': 'Applies graphical effects like blur or color shift to an element.',
            'object-fit': 'Specifies how the content of a replaced element should be resized to fit its container.',
            'user-select': 'Controls the user\'s ability to select text.'
    },
        'functions': {
            'rgb': 'Defines a color using the Red-Green-Blue model. Example: rgb(255, 0, 0) for red.',
            'rgba': 'Defines a color using Red-Green-Blue-Alpha (opacity). Example: rgba(255, 0, 0, 0.5).',
            'url': 'Specifies a URL for loading external resources (images, fonts, etc).',
            'calc': 'Performs calculations to determine CSS property values.',
            'var': 'Used to insert the value of a custom property (CSS variable).',
            'hsl': 'Defines a color using the Hue-Saturation-Lightness model.',
            'hsla': 'Defines a color using Hue-Saturation-Lightness-Alpha (opacity).',
            'min': 'Returns the smallest (minimum) value from a list of comma-separated expressions.',
            'max': 'Returns the largest (maximum) value from a list of comma-separated expressions.',
            'clamp': 'Clamps a value between an upper and lower bound.',
            'TranslateY': 'Used for transforms to move a certain object an amount of pixels into the y-axis.',
            'TranslateX': 'Used for transforms to move a certain object an amount of pixels into the x-axis.',
            'Translate': 'Used for moving a certain object into both the x- and y-axis. This function has two parameters: x and y.'
    }
  }
}

def highlight_document_in_chunks(chunk_size=100):
    last_line = int(text.index(tk.END).split('.')[0]) - 1

    def highlight_chunk(start_line=1):
        end_line = min(start_line + chunk_size - 1, last_line)
        for line in range(start_line, end_line + 1):
            region_start = f"{line}.0"
            region_end = f"{line}.end"
            content = text.get(region_start, region_end)
            for tag in text.tag_names():
                text.tag_remove(tag, region_start, region_end)
            highlight(target=text, region_start=region_start, region_end=region_end, content=content)
        if end_line < last_line:
            root.after(10, lambda: highlight_chunk(end_line + 1))

    highlight_chunk()
    
def is_binary_file(filepath):
    with open(filepath, 'rb') as f:
        chunk = f.read(1024)
        if b'\0' in chunk: # If it contains any NUL bytes, it's likely binary.
            return True
        text_characters = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)))
        non_text = chunk.translate(bytearray.maketrans(b'', b''), text_characters)
        return bool(non_text)

current_file = ""

def new_file(event=None):
    text.delete(1.0, tk.END)
    language_var.set('plaintext')
    highlight_language_change()
    update_line_numbers()
    root.title("Slash Code")

def load_file(path):
    def worker():
        try:
            file_size = os.path.getsize(path)
            if is_binary_file(path):
                choice = messagebox.askokcancel(translate.get("binary_file_title"), translate.get("binary_file"), icon='warning')
                if choice:
                    with open(path, 'rb') as f:
                        if language_var.get() != "plaintext":
                            language_var.set('plaintext')
                            highlight_language_change()    
                        content = f.read()
                else:
                    content = ''
                    new_file()
                    root.title("Slash Code")
            else:
                for enc in encodings:
                    try:
                        with open(path, 'r', encoding=enc, errors='replace') as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        root.after(0, show_error, e)

            root.after(0, lambda: update_gui(path, content, file_size))
        except Exception as e:
            root.after(0, show_error, e)

    threading.Thread(target=worker, daemon=True).start()

def open_file(event=None):
    global current_file
    filetypes = [
        (translate.get("python_files"), "*.py"),
        (translate.get("javascript_files"), "*.js"),
        (translate.get("html_files"), "*.html"),
        (translate.get("c_files"), "*.c"),
        (translate.get("cpp_files"), "*.cpp *.hpp"),
        (translate.get("header_files"), "*.h"),
        (translate.get("text_files"), "*.txt"),
        (translate.get("cs_files"), "*.cs"),
        (translate.get("css_files"), "*.css"),
        (translate.get("markdown_files"), "*.md *.markdown"),
        (translate.get("renpy_files"), "*.rpy"),
        (translate.get("shell_files"), "*.sh *.bash *.zsh"),
        (translate.get("all_files"), "*.*"),
    ]
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    
    if file_path:
        current_file = file_path
        load_file(file_path)

def update_gui(file_path, content, file_size=None):
    text.delete(1.0, tk.END)
    text.insert(tk.END, content)
    text.edit_separator()
    root.title(f"Slash Code - {os.path.basename(file_path)}")
    lang = get_language(file_path)
    if lang == 'plaintext':
        lang = guess_language_from_content(content)
    language_var.set(lang)
    update_line_numbers()
    if file_size is not None and file_size > 80000:
        root.after(150, lambda: highlight_document_in_chunks(chunk_size=100))
    else:
        root.after(10, highlight_full_document)


def show_error(e):
    messagebox.showerror(
        translate.get("error_a1"),
        translate.get("error_a3") + str(e)
    )

def save_file(event=None):
    try:
        current_filename = root.title().split(" - ", 1)[1]
    except IndexError:
        current_filename = ""

    language = language_var.get()

    if not current_filename or current_filename.strip() == "":
        base_filename = "file"
    else:
        base_filename = os.path.splitext(current_filename)[0]

    if language == "python":
        ext = ".py"
        filetypes = [(translate.get("python_files"), "*.py"), (translate.get("all_files"), "*.*")]
    elif language == "javascript":
        ext = ".js"
        filetypes = [(translate.get("javascript_files"), "*.js"), (translate.get("all_files"), "*.*")]
    elif language == "css":
        ext = ".css"
        filetypes = [(translate.get("css_files"), "*.css"), (translate.get("all_files"), "*.*")]
    elif language == "html":
        ext = ".html"
        filetypes = [(translate.get("html_files"), "*.html"), (translate.get("all_files"), "*.*")]
    elif language == "cpp":
        ext = ".cpp"
        filetypes = [(translate.get("cpp_files"), "*.cpp"), (translate.get("all_files"), "*.*")]
    elif language == "markdown":
        ext = ".md"
        filetypes = [(translate.get("markdown_files"), "*.md *.markdown"), (translate.get("all_files"), "*.*")]
    elif language == "renpy":
        ext = ".rpy"
        filetypes = [(translate.get("renpy_files"), "*.rpy"), (translate.get("all_files"), "*.*")]
    elif language == "shell":
        ext = ".sh"
        filetypes = [(translate.get("shell_files"), "*.sh *.bash *.zsh"), (translate.get("all_files"), "*.*")]
    else:
        ext = ".txt"
        filetypes = [(translate.get("text_files"), "*.txt"), (translate.get("all_files"), "*.*")]

    file = filedialog.asksaveasfilename(
        title=translate.get("save_as"),
        defaultextension=ext,
        initialfile=base_filename + ext,
        filetypes=filetypes
    )

    if file:
        if os.path.isfile(file) and is_binary_file(file):
            with open(file, 'wb') as f:
                f.write(text.get(1.0, tk.END).encode('utf-8'))
        else:
            for enc in encodings:
                    try:
                        with open(file, 'w', encoding=enc, errors='replace') as f:
                            f.write(text.get(1.0, tk.END))
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        root.after(0, show_error, e)
        root.title(f"Slash Code - {os.path.basename(file)}")
        
def get_language(file_path):
    if file_path.endswith('.py'):
        return 'python'
    elif file_path.endswith('.js') or file_path.endswith('.json'):
        return 'javascript'
    elif file_path.endswith('.html'):
        return 'html'
    elif file_path.endswith('.cpp'):
        return 'cpp'
    elif file_path.endswith('.cs'):
        return 'cs'
    elif file_path.endswith('.css'):
        return 'css'
    elif file_path.endswith('.md') or file_path.endswith('.markdown'):
        return 'markdown'
    elif file_path.endswith('.rpy'):
        return 'renpy'
    elif file_path.endswith('.sh') or file_path.endswith('.bash') or file_path.endswith('.zsh'):
        return 'shell'
    else:
        return 'plaintext'
    
def guess_language_from_content(content):
    try:
        filename = root.title().split(" - ", 1)[1]
        lang_from_extension = get_language(filename)
        if lang_from_extension != 'plaintext':
            return lang_from_extension
    except IndexError:
        pass
    content_lower = content.lower()

    if any(tag in content_lower for tag in ('<html>', '<div>', '<head>', '<body>', '<p>')):
        return 'html'
    if any(keyword in content for keyword in ('#include', 'using namespace', 'std::', 'struct', '#define')):
        return 'cpp'
    if any(keyword in content for keyword in ('def ', 'import ', 'from ', 'class ', 'assert ')):
        return 'python'
    if any(keyword in content for keyword in ('function(', 'console.log', 'const ', 'let ', 'var ')):
        return 'javascript'  
    if any(keyword in content for keyword in ('{', '}', ';', ':', 'color', 'background', 'font', 'margin', 'padding')) and content.strip().endswith('}'):
        return 'css'
    if any(keyword in content for keyword in ('init', 'define', 'transform', 'style', 'jump', 'call')):
        return 'renpy'
    if any(keyword in content for keyword in ('kill', 'wait', 'echo', 'fi', 'esac', 'trap')):
        return 'shell'
    return 'plaintext'

def highlight_line(event=None, targ=None):
    line = text.index("insert").split('.')[0]
    region_start = f"{line}.0"
    region_end = f"{line}.end"
    content = text.get(region_start, region_end)
    for tag in text.tag_names():
        text.tag_remove(tag, region_start, region_end)
    highlight(target=targ, region_start=region_start, region_end=region_end, content=content)
    
def highlight_full_document():
    highlight(full_document=True)
    bind_tooltips()
    
def mask_comments(content, comment_spans):
    chars = list(content)
    for s, e in comment_spans:
        for i in range(s, e):
            chars[i] = " " 
    return "".join(chars)

def highlight(target=None, event=None, full_document=False, region_start=None, region_end=None, content=None):
    if target is None:
        target = text  # Default to main editor

    # Clear function signatures only if target has the attribute
    if hasattr(target, "function_signatures"):
        target.function_signatures.clear()
    
    language = language_var.get()
    keywords = LANGUAGE_KEYWORDS.get(language, set())
    funcs = LANGUAGE_FUNCS.get(language, set())
    html_attr_pattern = r'\b(' + '|'.join(html_attrs) + r')\s*='

    # Determine highlighting region
    if full_document:
        for tag in target.tag_names():
            target.tag_remove(tag, "1.0", tk.END)
        region_start = "1.0"
        region_end = tk.END
        content = target.get(region_start, region_end)
    elif region_start is None or region_end is None or content is None:
        for tag in target.tag_names():
            target.tag_remove(tag, "1.0", tk.END)
        line = target.index("insert").split('.')[0]
        region_start = f"{line}.0"
        region_end = f"{line}.end"
        content = target.get(region_start, region_end)

    if language == "plaintext":
        return

    comment_spans = []
    string_spans = []
    preproc_spans = []

    def is_in_string_or_comment(idx):
        return any(s <= idx < e for s, e in comment_spans + string_spans)
    
    def is_in_string(idx):
        return any(s <= idx < e for s, e in string_spans)

    # --- Comments ---
    if language in ("python", "renpy", "shell"):
        lines = content.split('\n')
        current_pos = 0
        for line in lines:
            hash_pos = line.find('#')
            if hash_pos != -1:
                string_spans_in_line = []
                for match in re.finditer(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', line):
                    string_spans_in_line.append((match.start(), match.end()))
                if not any(s <= hash_pos < e for s, e in string_spans_in_line):
                    comment_start = current_pos + hash_pos
                    comment_end = current_pos + len(line)
                    comment_spans.append((comment_start, comment_end))
                    target.tag_add("comment", f"{region_start}+{comment_start}c", f"{region_start}+{comment_end}c")
            current_pos += len(line) + 1

    elif language in ("javascript", "cpp", "cs", "css"):
        for match in re.finditer(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', content):
            s, e = match.start(), match.end()
            string_spans.append((s, e))

        for match in re.finditer(r'//.*', content):
            s, e = match.start(), match.end()
            if is_in_string(s):
                continue
            comment_spans.append((s, e))
            target.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        if language in ("cpp", "cs"):
            for match in re.finditer(r'/\*.*?\*/', content, re.DOTALL):
                s, e = match.start(), match.end()
                if is_in_string(s):
                    continue
                comment_spans.append((s, e))
                target.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        
    elif language in ("html", "markdown"):
        for match in re.finditer(r'<!--.*?-->', content, re.DOTALL):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            target.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")

    masked_content = mask_comments(content, comment_spans)

    if language == "css":
        # --- Strings ---
        for match in re.finditer(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', masked_content):
            s, e = match.start(), match.end()
            target.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- At-Rules (e.g. @font-face) ---
        for match in re.finditer(r'@[a-zA-Z_-]+', masked_content):
            s, e = match.start(), match.end()
            target.tag_add("preprocessor", f"{region_start}+{s}c", f"{region_start}+{e}c")
            
        # --- General Keywords ---
        css_keywords = {'none', 'auto', 'inherit', 'initial', 'unset', 'transparent', 'block', 'inline', 'flex', 'grid', 'center', 'normal'}
        for keyword in css_keywords:
            for match in re.finditer(rf'\b{re.escape(keyword)}\b', masked_content):
                s, e = match.start(), match.end()
                if not is_in_string_or_comment(s):
                    target.tag_add("keyword", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Selectors (before '{') ---
        for match in re.finditer(r'([^{}/][^{}/]*)\s*\{', masked_content):
            selector = match.group(1)
            s = match.start(1)
            e = match.end(1)
            target.tag_add("keyword", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Properties ---
        for match in re.finditer(r'([a-zA-Z-]+)\s*:', masked_content):
            s, e = match.start(1), match.end(1)
            target.tag_add("function", f"{region_start}+{s}c", f"{region_start}+{e}c")
 
        # --- Function Calls (e.g. url(), rgb(), clamp()) ---
        for match in re.finditer(r'(\b[a-zA-Z-]+)\s*\(', masked_content):
            s, e = match.start(1), match.end(1)
            target.tag_add("builtin", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Numbers/Units ---
        for match in re.finditer(r'(-?\d*\.?\d+)(px|em|rem|%|vh|vw|vmin|vmax|ex|ch|pt|cm|mm|in|Q|s|ms)?\b', masked_content):
            s, e = match.start(), match.end()
            target.tag_add("integer", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Hex Colors ---
        for match in re.finditer(r'#[0-9a-fA-F]{3,6}\b', masked_content):
            s, e = match.start(), match.end()
            target.tag_add("constant", f"{region_start}+{s}c", f"{region_start}+{e}c")
           
    # --- Strings ---
    if language != "markdown":
        for match in re.finditer(r'("""(?:.|\n)*?"""|\'\'\'(?:.|\n)*?\'\'\'|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', masked_content):
            s, e = match.start(), match.end()
            string_spans.append((s, e))
            target.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
            escape_pattern = r'\\ |\\(\\|[abfnrtv\'"0-9xuU])'
            for s, e in string_spans:
                string_text = content[s:e]
                for esc in re.finditer(escape_pattern, string_text):
                    esc_start = s + esc.start()
                    esc_end = s + esc.end()
                    target.tag_add("escape", f"{region_start}+{esc_start}c", f"{region_start}+{esc_end}c")
                    
    # --- Test Flags (-z, -n, -d, etc.) ---
    if language == "shell":
        for match in re.finditer(r"\b" + "|".join(map(re.escape, SHELL_TEST_OPERATORS)) + r"\b", content):
            if not is_in_string_or_comment(match.start()):
                target.tag_add("pointer", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
                 
    if language == "markdown":
        # --- Headings ---
        for match in re.finditer(r'^(#{1,6})\s.*$', content, re.MULTILINE):
            s, e = match.start(1), match.end(1)
            target.tag_add("keyword", f"{region_start}+{s}c", f"{region_start}+{e}c")
 
        # --- Blockquotes ---
        for match in re.finditer(r'^(>\s)', content, re.MULTILINE):
            s, e = match.start(1), match.end(1)
            target.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Lists ---
        for match in re.finditer(r'^(\s*[-*+])\s', content, re.MULTILINE):
            s, e = match.start(1), match.end(1)
            target.tag_add("keyword", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Inline Code (``) ---
        for match in re.finditer(r'`[^`]+`', content):
            s, e = match.start(), match.end()
            target.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")

        # --- Fenced Code Blocks (```) ---
        for match in re.finditer(r'``````', content, re.DOTALL):
            s, e = match.start(), match.end()
            target.tag_add("preprocessor", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Operators ---       
    if language in ("cpp", "python", "renpy", "javascript", "cs", "css"):
        operator_pattern = r'(<<=|>>=|->\*|->|&&|\|\||\+\+|\-\-|<=|>=|==|<<|>>|!=|\.\*|\+=|-=|\*=|/=|%=|\^=|\|=|&=|::|:|\?|\.|~|\+|\-|\*|/|%|<|>|\^|\|)'
        for match in re.finditer(operator_pattern, content):
            s, e = match.start(), match.end()
            if not any(is_in_string_or_comment(i) for i in range(s, e)):
                target.tag_add("operator", f"{region_start}+{s}c", f"{region_start}+{e}c")
                
    # --- Builtins ---
    if language in ("python", "renpy"):
        builtins = LANGUAGE_FUNCS.get(language, set())
        if builtins:
            for match in re.finditer(r"\b(" + "|".join(map(re.escape, builtins)) + r")\b", content):
                if not is_in_string_or_comment(match.start()):
                    target.tag_add("builtin", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    
    if language == "renpy":
        # --- Screen/Label Names (tag 'classname', because they use the same attributes as a Python class.)---
        for match in re.finditer(r'\bscreen\s+([A-Za-z_][A-Za-z0-9_]*)', content):
            name_start = match.start(1)
            name_end = match.end(1)
            if not is_in_string_or_comment(name_start):
                target.tag_add("classname", f"{region_start}+{name_start}c", f"{region_start}+{name_end}c")
        
        # --- One-line Python Statements ($ (...), used with the same tag as the semicolon) ---
        for match in re.finditer('$', content):
            s, e = match.start(), match.end()
            if not is_in_string_or_comment(s):
                target.tag_add("semicolon", f"{region_start}+{s}c", f"{region_start}+{e}c")
            
    # --- Semicolons (C++, C#, CSS, JavaScript) ---
    for match in re.finditer(r';', content):
        s, e = match.start(), match.end()
        if not is_in_string_or_comment(s):
            target.tag_add("semicolon", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Preprocessor (C++) ---
    if language == "cpp":
        pattern = r'^[ \t]*#(define|undef|include|if|ifdef|ifndef|else|elif|endif|error|pragma|line|using|import|module)\b([^\n]*)'
        for match in re.finditer(pattern, content, re.MULTILINE):
            s, e = match.start(), match.end()
            if not is_in_string_or_comment(s):
                directive = match.group(1)
                line = content[s:e]
                hash_pos = line.find('#')
                directive_start = s + hash_pos
                directive_end = directive_start + 1 + len(directive)
                target.tag_add("preprocessor", f"{region_start}+{directive_start}c", f"{region_start}+{directive_end}c")
                rest_start = directive_end
                rest_end = e
                if rest_start < rest_end:
                    target.tag_add("preprocessor_rest", f"{region_start}+{rest_start}c", f"{region_start}+{rest_end}c")
                preproc_spans.append((s, e))

    # --- Templates (C++) ---
    if language == "cpp":
        id_pattern = re.compile(r'\b([A-Za-z_][A-Za-z0-9_:]*)\s*<(?![<=])')
        for id_match in id_pattern.finditer(content):
            identifier = id_match.group(1)
            if identifier in keywords or identifier in funcs:
                continue 
            open_angle = id_match.end() - 1
            if is_in_string_or_comment(open_angle):
                continue
            max_search = min(len(content), open_angle + 200)
            depth = 0
            for i in range(open_angle, max_search):
                if content[i] == '<' and not is_in_string_or_comment(i):
                    depth += 1
                elif content[i] == '>' and not is_in_string_or_comment(i):
                    depth -= 1
                    if depth == 0:
                        target.tag_add("template", f"{region_start}+{open_angle}c", f"{region_start}+{i+1}c")
                        break

    # --- Pointers/References (C++) ---
    if language == "cpp":
        for match in re.finditer(r'\b([A-Za-z_:][\w:<>]*)\s*(\*+|&)(?=\s*\w)', content):
            ptr_start, ptr_end = match.start(2), match.end(2)
            if not is_in_string_or_comment(ptr_start):
                target.tag_add("pointer", f"{region_start}+{ptr_start}c", f"{region_start}+{ptr_end}c")
                
    # --- Members ---
    for match in re.finditer(r'(?<!\d)\.(\w+)\b(?!\s*\()', content):
        member_start = match.start(1)
        member_end = match.end(1)
        if not is_in_string_or_comment(member_start):
            target.tag_add("member", f"{region_start}+{member_start}c", f"{region_start}+{member_end}c")

    # --- Dunder Methods ---
    for match in re.finditer(r'\b(__(?=\w*[^_])[\w]+__)\b', content):
        s, e = match.start(), match.end()
        target.tag_add("dunder", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Integers ---
    for match in re.finditer(r'\b\d+\b', content):
        s, e = match.start(), match.end()
        if not is_in_string_or_comment(s):
            target.tag_add("integer", f"{region_start}+{s}c", f"{region_start}+{e}c")
            
    # --- f-strings (Python, Ren'Py for "[]" and C# for $"{}") ---
    if language in ("python", "renpy", "cs", "cpp"):
        if language == "python":
            string_pattern = r"(?P<prefix>[fF])?(?P<quote>'''|\"\"\"|'|\")(?P<body>(?:\\.|(?!\2).)*)(?P=quote)"
        elif language == "renpy":
            string_pattern = r"(?P<prefix>[fF]?)['\"](?P<body>(?:\\.|[^\\])*?)['\"]"
        elif language == "cs":
            string_pattern = r"(?P<prefix>\$@|@\$(?=['\"]))?(?P<quote>'|\")(?P<body>(?:\\.|(?!\3).)*)(?P=quote)"
        elif language == "cpp":
            string_pattern = r"(?P<quote>'|\")(?P<body>(?:\\.|(?!\1).)*)(?P=quote)"
                
        for f_match in re.finditer(string_pattern, content, re.DOTALL):
            if is_in_string_or_comment(f_match.start()):
                continue
  
            prefix = f_match.group('prefix') if 'prefix' in f_match.groupdict() and f_match.group('prefix') else ''
            quote = f_match.group('quote')
            body = f_match.group('body')

            prefix_start = f_match.start('prefix') if prefix else f_match.start('quote')
            quote_end = f_match.end('quote')
            body_start = f_match.start('body')
            body_end = f_match.end('body')

            string_spans.append((prefix_start, quote_end))
            target.tag_add("string", f"{region_start}+{prefix_start}c", f"{region_start}+{quote_end}c")
            if prefix:
                target.tag_add("prefix", f"{region_start}+{prefix_start}c", f"{region_start}+{f_match.end('prefix')}c")

            current_pos = body_start

            if language == "renpy":
                interpolation_pattern = r'(\[.*?\]|\{.*?\})'
            elif language == "python":
                if 'f' not in prefix.lower():
                    continue
                interpolation_pattern = r'\{(?:[^{}]|\{[^{}]*\})*\}'
            elif language == "cs":
                if '$' not in prefix:
                    continue
                interpolation_pattern = r'\{(?:[^{}]|\{[^{}]*\})*\}'
            elif language == "cpp":
                if not re.search(r'(std|fmt)::format\s*\(', content):
                    continue
                interpolation_pattern = r'\{(?:[^{}]|\{[^{}]*\})*\}'
            else:
                interpolation_pattern = ''

            if not interpolation_pattern:
                continue

            for part in re.finditer(r'(.*?)(%s|$)' % interpolation_pattern, body):
                literal = part.group(1)
                expr = part.group(2)

                if literal:
                    lit_start = current_pos
                    lit_end = lit_start + len(literal)
                    string_spans.append((lit_start, lit_end))
                    target.tag_add("string", f"{region_start}+{lit_start}c", f"{region_start}+{lit_end}c")
                    current_pos = lit_end
                    if language in ("renpy", "python"):
                        if expr.startswith('{{') and expr.endswith('}}'):
                            continue
    
                if expr and expr[0] in ('{', '['):
                    expr_start = current_pos
                    expr_end = current_pos + len(expr)
                    current_pos = expr_end
    
                    target.tag_remove("string", f"{region_start}+{expr_start}c", f"{region_start}+{expr_end}c")
                    inner_text = expr[1:-1]
                    inner_start = expr_start + 1
    
                    for str_match in re.finditer(r"(['\"])(?:\\.|[^\\])*?\1", inner_text):
                        s = inner_start + str_match.start()
                        e = inner_start + str_match.end()
                        target.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
    
                    for func_match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', inner_text):
                        f_start = inner_start + func_match.start(1)
                        f_end = inner_start + func_match.end(1)
                        target.tag_add("funccall", f"{region_start}+{f_start}c", f"{region_start}+{f_end}c")
   
                    target.tag_add("punctuation", f"{region_start}+{expr_start}c", f"{region_start}+{expr_start+1}c")
                    target.tag_add("punctuation", f"{region_start}+{expr_end-1}c", f"{region_start}+{expr_end}c")
  
                    for var_match in re.finditer(r'\b([a-zA-Z_]\w*)\b', inner_text):
                        v_start = inner_start + var_match.start(1)
                        v_end = inner_start + var_match.end(1)
                        if not any(target.tag_names(f"{region_start}+{v_start}c")):
                            target.tag_add("variable", f"{region_start}+{v_start}c", f"{region_start}+{v_end}c")

                    for num_match in re.finditer(r'\b\d+\b', inner_text):
                        n_start = inner_start + num_match.start()
                        n_end = inner_start + num_match.end()
                        target.tag_add("number", f"{region_start}+{n_start}c", f"{region_start}+{n_end}c")

                    for dunder_match in re.finditer(r'\b(__(?=\w*[^_])[\w]+__)\b|![rRsSaA]', inner_text):
                        d_start = inner_start + dunder_match.start()
                        d_end = inner_start + dunder_match.end()
                        target.tag_add("dunder", f"{region_start}+{d_start}c", f"{region_start}+{d_end}c")

                    if language in ("cpp", "python", "renpy", "javascript", "cs"):
                        operator_pattern = r'(<<=|>>=|->\*|->|&&|\|\||\+\+|\-\-|<=|>=|==|<<|>>|!=|\.\*|\+=|-=|\*=|/=|%=|\^=|\|=|&=|::|:|\?|\.|~|\+|\-|\*|/|%|<|>|\^|\|)'
                        for operator_match in re.finditer(operator_pattern, inner_text):
                            o_start = inner_start + operator_match.start()
                            o_end = inner_start + operator_match.end()
                            target.tag_add("operator", f"{region_start}+{o_start}c", f"{region_start}+{o_end}c")

    # --- Keywords, Functions, Class Names, Function Calls, Variables ---
    if keywords:
        for match in re.finditer(r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", content):
            if not is_in_string_or_comment(match.start()):
                tag_start = f"{region_start}+{match.start()}c"
                tag_end = f"{region_start}+{match.end()}c"
                target.tag_add("keyword", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
                target.tag_add(f"kw_{match.group(0)}", tag_start, tag_end)
    if language in ("python", "renpy", "cs", "cpp", "javascript"):
        for match in re.finditer(r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)', content):
            name_start = match.start(1)
            name_end = match.end(1)
            if not is_in_string_or_comment(name_start):
                target.tag_add("classname", f"{region_start}+{name_start}c", f"{region_start}+{name_end}c")
    if funcs:
        for match in re.finditer(r"\b(" + "|".join(map(re.escape, funcs)) + r")\b", content):
            if not is_in_string_or_comment(match.start()):
                target.tag_add("function", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
                target.tag_add(f"fn_{match.group(0)}", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', content):
        if not is_in_string_or_comment(match.start(1)):
            target.tag_add("funccall", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\b', content):
        if is_in_string_or_comment(match.start()):
            continue
        pos = f"{region_start}+{match.start()}c"
        if not any(target.tag_names(pos)):
            target.tag_add("variable", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    
    # --- Tooltips ---
    if language in ("python", "cpp", "cs", "renpy", "shell"):
        for match in re.finditer(
        r'\bdef\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(?:->\s*([^:]+?))?:', content
        ):
            func_name = match.group(1)
            params = match.group(2)
            return_type = match.group(3)
            name_start = match.start(1)
            name_end = match.end(1)
            tag_name = f"defsig_{func_name}"
            target.tag_add(tag_name, f"{region_start}+{name_start}c", f"{region_start}+{name_end}c")
            after_def = content[match.end():]
            docstring_match = re.match(r'\s*("""|\'\'\')(.*?)\1', after_def, re.DOTALL)
            docstring = docstring_match.group(2).strip() if docstring_match else ""
            signature = f"{func_name}({params})"
            if return_type:
                signature += f" -> {return_type}"
            else:
                signature += " -> UnanalyzableType"
            if docstring:
               signature += f"\n\n{docstring}"
            if hasattr(target, "function_signatures"):
                if not hasattr(target, "function_signatures"):
                    target.function_signatures = {}
                target.function_signatures[func_name] = signature

    # --- HTML tags/attributes ---
    if language == "html":
        for match in re.finditer(r'<(\/?\w+)', content):
            target.tag_add("html_tag", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
        for match in re.finditer(html_attr_pattern, content):
            target.tag_add("html_attr", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
    if language == "html":
        for match in re.finditer(r'=\s*(".*?"|\'.*?\')', content):
            s, e = match.start(1), match.end(1)
            target.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Constants (ALLCAPS) ---
    if language in ['python', 'renpy', 'javascript', 'cpp']:
        for match in re.finditer(r'\b([A-Z][A-Z0-9_]*[A-Z][A-Z0-9_]*)\b', content):
            if not is_in_string_or_comment(match.start()):
                target.tag_add("constant", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
    for s, e in comment_spans:
        target.tag_remove("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
    target.tag_raise("comment")

themes = {
    'light': {
    'bg': '#ffffff', 'fg': '#000000',
    'keyword': '#005cc5', 'string': "#d73a49", 'comment': '#6a737d',
    'function': '#6f42c1', 'funccall': '#005cc5', 'integer': '#22863a', 'member': '#e36209',
    'prefix': '#22863a', 'line_numbers': '#f0f0f0', 'cursor': '#000000', 'type': "#6f42c1",
    'variable': '#24292e', 'builtin': "#e36209", 'dunder': '#6a737d', 'pointer': "#005cc5", 'classname': "#6f42c1",
    'escape': '#24292e', 'semicolon': "#586069", 'preprocessor': "#d73a49", 'preprocessor_rest': "#586069",
    'html_tag': "#22863a", 'html_attr': "#6f42c1", 'constant': "#005cc5", 'template': "#22863a", 'operator': "#d73a49",
    },
    'dark': {
        'bg': '#1e1e1e', 'fg': '#d4d4d4',
        'keyword': '#569cd6', 'string': '#ce9178', 'comment': '#6a9955',
        'function': '#c586c0', 'funccall': '#4ec9b0', 'integer': '#b5cea8', 'member': '#bd4840',
        'prefix': '#9cdcfe', 'line_numbers': '#2d2d2d', 'cursor': '#d4d4d4', 'type': "#6316cf",
        'variable': '#ffffff', 'builtin': "#60abfc", 'dunder': '#b0b0b0', 'pointer': "#4282e1", 'classname': "#B14B15",
        'escape': "#7a7a7a", 'semicolon': "#a0a0a0", 'preprocessor': "#843E84", 'preprocessor_rest': "#636363",
        'html_tag': "#9625af", 'html_attr': "#0c79cd", 'constant': "#fc822b", 'template': "#2e7d71", 'operator': "#33c7c2",
    },
    'dracula': {
        'bg': '#282a36', 'fg': '#f8f8f2',
        'keyword': '#ff79c6', 'string': '#f1fa8c', 'comment': '#6272a4',
        'function': '#8be9fd', 'funccall': '#50fa7b', 'integer': '#bd93f9', 'member': '#ffb86c',
        'prefix': '#bd93f9', 'line_numbers': '#44475a', 'cursor': '#f8f8f2', 'type': "#8be9fd",
        'variable': '#f8f8f2', 'builtin': "#ffb86c", 'dunder': '#bd93f9', 'pointer': "#50fa7b", 'classname': "#ffb86c",
        'escape': '#ff5555', 'semicolon': "#44475a", 'preprocessor': "#ff79c6", 'preprocessor_rest': "#44475a",
        'html_tag': "#ff79c6", 'html_attr': "#8be9fd", 'constant': "#bd93f9", 'template': "#50fa7b", 'operator': "#ff79c6",
    },
    'monokai': {
        'bg': '#272822', 'fg': '#f8f8f2',
        'keyword': '#f92672', 'string': '#e6db74', 'comment': '#75715e',
        'function': '#a6e22e', 'funccall': '#fd971f', 'integer': '#ae81ff', 'member': '#66d9ef',
        'prefix': '#fd971f', 'line_numbers': '#3e3d32', 'cursor': '#f8f8f0', 'type': "#66d9ef",
        'variable': '#f8f8f2', 'builtin': "#fd971f", 'dunder': '#75715e', 'pointer': "#a6e22e", 'classname': "#a6e22e",
        'escape': '#fd5ff0', 'semicolon': "#75715e", 'preprocessor': "#f92672", 'preprocessor_rest': "#75715e",
        'html_tag': "#f92672", 'html_attr': "#a6e22e", 'constant': "#ae81ff", 'template': "#66d9ef", 'operator': "#f92672",
    },
    'night_owl': {
        'bg': '#011627', 'fg': '#d6deeb',
        'keyword': '#c792ea', 'string': '#ecc48d', 'comment': '#637777',
        'function': '#82aaff', 'funccall': '#7fdbca', 'integer': '#f78c6c', 'member': '#addb67',
        'prefix': '#7fdbca', 'line_numbers': '#1d3b53', 'cursor': '#d6deeb', 'type': "#21c7a8",
        'variable': '#d6deeb', 'builtin': "#7fdbca", 'dunder': '#637777', 'pointer': "#82aaff", 'classname': "#ffeb95",
        'escape': '#c792ea', 'semicolon': "#637777", 'preprocessor': "#c792ea", 'preprocessor_rest': "#637777",
        'html_tag': "#82aaff", 'html_attr': "#addb67", 'constant': "#f78c6c", 'template': "#21c7a8", 'operator': "#c792ea",
    },
    'shades_of_purple': {
        'bg': '#2d2b55', 'fg': '#ffffff',
        'keyword': '#a599e9', 'string': '#fcbf6b', 'comment': '#b362ff',
        'function': '#f97e72', 'funccall': '#43d9ad', 'integer': '#ff628c', 'member': '#fdfd97',
        'prefix': '#43d9ad', 'line_numbers': '#22223b', 'cursor': '#ffffff', 'type': "#a599e9",
        'variable': '#ffffff', 'builtin': "#43d9ad", 'dunder': '#b362ff', 'pointer': "#a599e9", 'classname': "#fcbf6b",
        'escape': '#b362ff', 'semicolon': "#a599e9", 'preprocessor': "#f97e72", 'preprocessor_rest': "#22223b",
        'html_tag': "#a599e9", 'html_attr': "#43d9ad", 'constant': "#fcbf6b", 'template': "#43d9ad", 'operator': "#a599e9",
    },
    'high_contrast': {
    'bg': '#000000', 'fg': '#FFFFFF',
    'keyword': '#00FFFF', 'string': "#FF4000", 'comment': '#FFFF00',
    'function': '#00FF00', 'funccall': '#00FFFF', 'integer': '#FFA500', 'member': '#FF4500',
    'prefix': '#00FFFF', 'line_numbers': '#333333', 'cursor': '#FFFFFF', 'type': '#00FF00',
    'variable': '#FFFFFF', 'builtin': '#FF4500', 'dunder': '#AAAAAA', 'pointer': '#00FFFF', 'classname': '#00FF00',
    'escape': '#FF0000', 'semicolon': '#FFFFFF', 'preprocessor': "#C800C8", 'preprocessor_rest': '#AAAAAA',
    'html_tag': '#00FFFF', 'html_attr': '#FFA500', 'constant': '#FF4500', 'template': '#00FF00', 'operator': '#FFFF00',
},
}
        
def auto_indent(event):
    text = event.widget
    line = text.get("insert linestart", "insert")
    code_part = line.split('#', 1)[0].rstrip()
    match = re.match(r'^(\s*)', line)
    whitespace = match.group(0) if match else ""
    
    if code_part.rstrip().endswith((":", "{", "{{")):
        whitespace += "    "
        
    if code_part.rstrip().endswith(("}", "}}")):
        whitespace = whitespace[:-4] if len(whitespace) >= 4 else ""
        
    text.insert("insert", f"\n{whitespace}")
    update_line_numbers()
    return "break"

def handle_closing_brace(event):
    text = event.widget
    line_start = text.index("insert linestart")
    line_end = text.index("insert lineend")
    line_text = text.get(line_start, line_end)
    
    if re.match(r'^\s*$', line_text):
        current_pos = text.index("insert")
        if line_text.startswith("    "):
            text.delete(line_start, f"{line_start}+4c")
        elif line_text.startswith("\t"):
            text.delete(line_start, f"{line_start}+1c")
            
        text.insert("insert", "}")
        return "break"
    return None

def undo_action(event=None):
    try:
        text.edit_undo()
    except tk.TclError:
        pass
    
def redo_action(event=None):
    try:
        text.edit_redo()
        if os.path.getsize(current_file) > 80000:
            root.after(100, lambda: highlight_document_in_chunks(chunk_size=100))
        else:
            root.after(50, highlight_full_document)
    except tk.TclError:
        pass

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

font_size = 12
jp_font = tk.font.Font(family="Noto Sans JP", size=font_size)
en_font = tk.font.Font(family="Consolas", size=font_size)
if lang_var.get() == "jp":
    font = jp_font
else:
    font = en_font

line_numbers = tk.Text(
    frame,
    font=font,
    width=4,
    padx=4,
    takefocus=0,
    border=0,
    background='#f0f0f0',
    state='disabled',
    wrap='none'
)

current_theme = 'light'
theme_var = tk.StringVar(value=current_theme)

def apply_font_tags():
    content = text.get("1.0", "end-1c")
    text.tag_remove("jp", "1.0", "end")
    text.tag_remove("en", "1.0", "end")

    for i, char in enumerate(content):
        index = f"1.0+{i}c"
        if re.match(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF]', char):
            text.tag_add("jp", index, f"{index}+1c")
        else:
            text.tag_add("en", index, f"{index}+1c")

line_numbers.pack(side=tk.LEFT, fill=tk.Y)
text = scrolledtext.ScrolledText(frame, font=font, undo=True, wrap=tk.WORD)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text.bind("<Return>", auto_indent)
text.bind("}", handle_closing_brace)

sidebar = tk.Frame(frame, width=200, bg=themes[theme_var.get()]['bg'])
sidebar.pack(side=tk.RIGHT, fill=tk.Y)

create_sidebar_buttons()

file_listbox = tk.Listbox(sidebar, width=30, bg=themes[theme_var.get()]['bg'], fg=themes[theme_var.get()]['fg'], selectbackground=themes[theme_var.get()]['keyword'])

minimap_frame = tk.Frame(sidebar, bg=themes[theme_var.get()]['bg'])
minimap_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
minimap_font = tk.font.Font(family="Consolas", size=4)
def set_minimap():
    global minimap
    minimap = tk.Text(minimap_frame, font=minimap_font, width=70, height=50, state='disabled', wrap=tk.NONE, bg=themes[theme_var.get()]['bg'], fg=themes[theme_var.get()]['fg'])
set_minimap()
minimap.pack(side=tk.RIGHT, fill=tk.BOTH)

tree = ttk.Treeview(sidebar)
tree.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
scrollbar = tk.Scrollbar(tree, orient="vertical", command=tree.yview)
scrollbar_h_container = tk.Frame(tree, height=15)
scrollbar_h_container.pack(side=tk.BOTTOM, fill=tk.X)
scrollbar_hz = tk.Scrollbar(scrollbar_h_container, orient="horizontal", command=tree.xview, width=15)
tree.configure(yscrollcommand=scrollbar.set)
tree.configure(xscrollcommand=scrollbar_hz.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_hz.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

for tag, color in themes[theme_var.get()].items():
    if tag in ["bg", "fg", "line_numbers", "cursor"]: continue
    minimap.tag_configure(tag, foreground=color)

minimap_visible = [True]
def hide_minimap():
    minimap_frame.pack_forget()
    minimap_visible[0] = True
    tree.pack_configure(expand=True)
    tree.update_idletasks()
    scrollbar_hz.pack_forget()
    scrollbar_hz.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
    tree.configure(xscrollcommand=scrollbar_hz.set)
    file_listbox.pack_configure(expand=True)

def show_minimap():
    file_listbox.pack(fill=tk.BOTH, expand=True)
    minimap_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, before=tree)
    tree.pack_configure(expand=True)
    tree.update_idletasks()
    scrollbar_hz.pack_forget()
    scrollbar_hz.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
    tree.configure(xscrollcommand=scrollbar_hz.set)
    minimap_visible[0] = False

def update_minimap(event=None):
    global minimap
    if not minimap:
        return
    minimap.config(state='normal')
    minimap.delete('1.0', tk.END)
    minimap.insert('1.0', text.get('1.0', tk.END))
    minimap.config(state='disabled')

def on_text_scroll(*args):
    line_numbers.yview_moveto(float(args[0]))
    
    text_lines = int(text.index('end-1c').split('.')[0])
    minimap_lines = int(minimap.index('end-1c').split('.')[0])
    if text_lines > 0 and minimap_lines > 0:
        ratio = minimap_lines / text_lines
        minimap.yview_moveto(float(args[0]) * ratio)
    text.vbar.set(*args)

text.config(yscrollcommand=on_text_scroll)

def on_scroll(*args):
    text.yview(*args)
    line_numbers.yview_moveto(text.yview()[0])
    minimap.yview_moveto(text.yview()[0])
    update_line_numbers()
    return "break"

def on_minimap_click(event):
    height = minimap.winfo_height()
    clicked_fraction = event.y / height
    text.yview_moveto(clicked_fraction)
    update_line_numbers()
    update_minimap()


minimap.bind("<Button-1>", on_minimap_click)
text.bind("<MouseWheel>", on_scroll)
text.bind("<Button-4>", on_scroll)
text.bind("<Button-5>", on_scroll)

def zoom_in(event=None):
    global font_size, font
    font_size = min(36, font_size + 2)
    sidebar.config(width=int(200 - font_size * 1.5))
    minimap.config(width=int(70 - font_size * 1.2))
    font = ("Consolas", font_size)
    print(f"Font size: {font_size}")
    text.config(font=font)
    line_numbers.config(font=font)
    update_line_numbers()

def zoom_out(event=None):
    global font_size, font
    font_size = max(8, font_size - 2)
    sidebar.config(width=int(200 - font_size * 1.2))
    minimap.config(width=int(70 - font_size * 1.5))
    font = ("Consolas", font_size)
    print(f"Font size: {font_size}")
    text.config(font=font)
    line_numbers.config(font=font)
    update_line_numbers()

text.bind('<<Modified>>', lambda e: (update_minimap(), text.edit_modified(0)))

def on_key_and_scroll(event=None):
    on_key_release()
    on_scroll()
    apply_font_tags()
    return None

def on_mousewheel(event=None):
    update_line_numbers()
    on_scroll()
    return None

def on_button_release(event=None):
    on_scroll()
    return None

def on_configure(event=None):
    update_line_numbers()
    return None

def on_paste(event=None):
    root.after(100, lambda: highlight_document_in_chunks(chunk_size=100))
    return None

def open_selected_file(event=None):
    sel = file_listbox.curselection()
    if sel:
        fname = file_listbox.get(sel[0])
        folder = getattr(file_listbox, 'folder_path', None)
        if folder:
            fpath = os.path.join(folder, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    text.delete("1.0", tk.END)
                    text.insert(tk.END, f.read())
                if os.path.getsize(fpath) > 80000:
                     root.after(150, lambda: highlight_document_in_chunks(chunk_size=100))
                else:
                    root.after(10, highlight_full_document)
            except Exception as e:
                try:
                    with open(fpath, "rb") as f:
                        text.delete("1.0", tk.END)
                        text.insert(tk.END, f.read())
                except Exception as e:
                    messagebox.showerror(translate.get("error_a1"), translate.get("error_a2") + f"\n{e}")
                    
file_listbox.bind("<<ListboxSelect>>", open_selected_file)
file_listbox.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

def insert_nodes(parent, path):
    try:
        for name in sorted(os.listdir(path)):
            abspath = os.path.join(path, name)
            isdir = os.path.isdir(abspath)
            node = tree.insert(parent, "end", text=name, open=False, values=[abspath])
            if isdir:
                tree.insert(node, "end")
    except Exception:
        pass

def get_full_path(node):
    return tree.item(node, "values")[0] if tree.item(node, "values") else ""

def on_open_node(event):
    node = tree.focus()
    path = get_full_path(node)
    children = tree.get_children(node)
    if children:
        first_child = children[0]
        if not tree.item(first_child, "values"):
            tree.delete(first_child)
            insert_nodes(node, path)

def on_tree_double_click(event=None):
    node = tree.focus()
    path = get_full_path(node)
    if os.path.isfile(path):
        try:
            load_file(path)
            highlight(target=minimap)
        except Exception as e:
            messagebox.showerror(translate.get("error_a1"), translate.get("error_a2") + f"\n{e}")

def open_folder(folder=None, skip_ask=False):
    if not folder and not skip_ask:
        folder = filedialog.askdirectory()
    if folder:
        tree.delete(*tree.get_children())
        root_node = tree.insert("", "end", text=os.path.basename(folder) + f" ({folder})", open=True, values=[folder])
        insert_nodes(root_node, folder)
        new_file()
        file_listbox.folder_path = folder
        globals()['FOLDER'] = folder

open_folder_btn.config(command=open_folder)

tree.bind("<<TreeviewOpen>>", on_open_node)
tree.bind("<Double-1>", on_tree_double_click)

update_ui_text()

def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[theme_name]
    text.config(bg=theme['bg'], fg=theme['fg'], insertbackground=theme['cursor'])
    line_numbers.config(bg=theme['line_numbers'], fg=theme['fg'])
    file_listbox.config(bg=theme['line_numbers'], fg=theme['fg'], selectbackground=theme['keyword'])
    if minimap:
        minimap.config(bg=theme['bg'], fg=theme['fg'])
        for tag, color in theme.items():
            if tag in ["bg", "fg", "line_numbers", "cursor"]: 
                continue
            minimap.tag_configure(tag, foreground=color)
    minimap_frame.configure(bg=theme['bg'])
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview",
        background=theme['bg'],
        foreground=theme['fg'],
        fieldbackground=theme['bg'],
        highlightthickness=0,
        borderwidth=0
    )
    style.map("Treeview",
        background=[('selected', theme['keyword'])],
        foreground=[('selected', theme['fg'])]
    )
    sidebar.config(bg=theme['bg'])

    text.tag_configure("keyword", foreground=theme['keyword'])
    text.tag_configure("comment", foreground=theme['comment'])
    text.tag_configure("string", foreground=theme['string'])
    text.tag_configure("function", foreground=theme['function'])
    text.tag_configure("funccall", foreground=theme['funccall'])
    text.tag_configure("integer", foreground=theme['integer'])
    text.tag_configure("prefix", foreground=theme['prefix'])
    text.tag_configure("builtin", foreground=theme['builtin'])
    text.tag_configure("dunder", foreground=theme['dunder'])
    text.tag_configure("variable", foreground=theme['variable'])
    text.tag_configure("escape", foreground=theme['escape'])
    text.tag_configure("brace", foreground=theme.get("brace", "#808080"))
    text.tag_configure("punctuation", foreground=theme.get("punctuation", "#808080"))
    text.tag_configure("number", foreground=theme.get("number", "#b5cea8"))
    text.tag_configure("html_tag", foreground=theme['html_tag'])
    text.tag_configure("html_attr", foreground=theme['html_attr'])
    text.tag_configure("semicolon", foreground=theme['semicolon'])
    text.tag_configure("constant", foreground=theme['constant'])
    text.tag_configure("preprocessor", foreground=theme['preprocessor'])
    text.tag_configure("preprocessor_rest", foreground=theme['preprocessor_rest'])
    text.tag_configure("template", foreground=theme['template'])
    text.tag_configure("operator", foreground=theme['operator'])
    text.tag_configure("pointer", foreground=theme['pointer'])
    text.tag_configure("type", foreground=theme['type'])
    text.tag_configure("classname", foreground=theme['classname'])
    text.tag_configure("member", foreground=theme['member'])
    text.tag_raise("preprocessor_rest")
    text.tag_raise("prefix")
    text.tag_raise("brace")
    text.tag_raise("punctuation")
    text.tag_raise("number")
    text.tag_raise("comment")

def find_text(event=None):
    def do_find(event=None):
        text.tag_remove('found', '1.0', tk.END)
        search_term = entry.get()
        if not search_term:
            return
        start_pos = '1.0'
        
        while True:
            start_pos = text.search(search_term, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            
            end_pos = f"{start_pos}+{len(search_term)}c"
            text.tag_add('found', start_pos, end_pos)
            start_pos = end_pos
            
        text.tag_config('found', background='yellow', foreground='black')

    find_win = tk.Toplevel(root)
    find_win.title(translate.get("find"))
    tk.Label(find_win, text=translate.get("find_query")).pack(side=tk.LEFT)
    entry = tk.Entry(find_win)
    entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tk.Button(find_win, text=translate.get("find_all"), command=do_find).pack(side=tk.LEFT)
    entry.focus_set()

def replace_text():
    replace_win = tk.Toplevel(root)
    replace_win.title(translate.get("replace"))
    replace_win.transient(root)
    replace_win.grab_set()

    tk.Label(replace_win, text=translate.get("find_query")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    find_entry = tk.Entry(replace_win, width=30)
    find_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(replace_win, text=translate.get("replace")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    replace_entry = tk.Entry(replace_win, width=30)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    def do_replace():
        find_text = find_entry.get()
        replace_text_val = replace_entry.get()
        content = text.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text_val)
        text.delete("1.0", tk.END)
        text.insert("1.0", new_content)
        highlight_full_document()
        replace_win.destroy()

    def do_replace_next():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
    
        if not find_text:
            return
    
        start_pos = text.index(tk.INSERT)
    
        found_pos = text.search(find_text, start_pos, 
                              stopindex=tk.END, 
                              nocase=0,
                              regexp=False)
    
        if found_pos:
            end_pos = f"{found_pos}+{len(find_text)}c"
        
            text.delete(found_pos, end_pos)
            text.insert(found_pos, replace_text)
        
            new_end = f"{found_pos}+{len(replace_text)}c"
            text.tag_remove('found', '1.0', tk.END)
            text.tag_add('found', found_pos, new_end)
            text.tag_config('found', background='yellow', foreground='black')

            text.mark_set(tk.INSERT, new_end)
            text.see(found_pos)
        
            root.after(50, highlight_document_in_chunks)
        else:
            if text.compare(start_pos, "!=", "1.0"):
                text.mark_set(tk.INSERT, "1.0")
                root.after(100, do_replace_next)
            else:
                text.bell()

    tk.Button(replace_win, text=translate.get("replace"), command=do_replace_next).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(replace_win, text=translate.get("replace_all"), command=do_replace).grid(row=2, column=1, padx=5, pady=5)

    find_entry.focus_set()

def bind_tooltips():
    lang = language_var.get()
    info = TOOLTIP_INFO.get(lang, {})
    kw_info = info.get('keywords', {})
    fn_info = info.get('functions', {})
    for tag in text.tag_names():
        try:
            text.tag_unbind(tag, "<Enter>")
            text.tag_unbind(tag, "<Leave>")
        except:
            pass

    for kw, desc in kw_info.items():
        tag_name = f"kw_{kw}"
        text.tag_bind(tag_name, "<Enter>", lambda e, desc=desc: tooltip_manager.show(e, desc))
        text.tag_bind(tag_name, "<Leave>", tooltip_manager.hide)

    for fn, desc in fn_info.items():
        tag_name = f"fn_{fn}"
        text.tag_bind(tag_name, "<Enter>", lambda e, desc=desc: tooltip_manager.show(e, desc))
        text.tag_bind(tag_name, "<Leave>", tooltip_manager.hide)
    if hasattr(text, "function_signatures"):
        for func_name, signature in text.function_signatures.items():
            tag_name = f"defsig_{func_name}"
            text.tag_bind(tag_name, "<Enter>", lambda e, sig=signature: tooltip_manager.show(e, sig))
            text.tag_bind(tag_name, "<Leave>", tooltip_manager.hide)
            
def save_tempdir_mkhistory(tmpdir):
    tempdirs_file = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave", ".tempdir_mkhistory")
    os.makedirs(os.path.dirname(tempdirs_file), exist_ok=True)
    if os.path.exists(tempdirs_file):
        with open(tempdirs_file, "r", encoding="utf-8") as f:
            all_dirs = set(line.strip() for line in f if line.strip())
    else:
        all_dirs = set()
    if tmpdir not in all_dirs:
        with open(tempdirs_file, "a", encoding="utf-8") as f:
            try:
                if os.path.getsize(tempdirs_file) > 0:
                    f.write(f"\n{tmpdir}")
                else:
                    f.write(tmpdir)
            except Exception as e:
                print(f"{translate.get('error_a4')}{e}")
                return
        
def del_mkhistory_tempdirs(explicit_search=False):
    tempdirs_file = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave", ".tempdir_mkhistory")
    if os.path.exists(tempdirs_file):
        with open(tempdirs_file, "r", encoding="utf-8") as f:
            dirs = [line.strip() for line in f if line.strip()]
            print(translate.get("deleting_dirs") + ', '.join(dirs))
            for _dir in dirs:
                try:
                    shutil.rmtree(_dir, ignore_errors=True)
                except Exception:
                    continue
        os.remove(tempdirs_file)
        return True
    else:
        print(translate.get("directory_del_not_found"))
    if explicit_search:
        _temp_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Temp") 
        for root, dirs, files in os.walk(_temp_dir):
            for dir_name in dirs[:]:
                if dir_name.startswith("sc_") or dir_name.startswith("sc_mingw_"):
                    full_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(full_path, ignore_errors=True)
                    except Exception:
                        pass
        
def install_runner(lang, return_temp_cppdir=False):
    if platform.system() != "Windows":
        # Planning to extend for other platform support later.
        return False

    def run_cmd(cmd):
        try:
            subprocess.run(cmd, capture_output=True, check=True, shell=False)
            return True
        except Exception:
            return False

    if lang == "javascript":
        if run_cmd(["node", "--version"]):
            return True
        try:
            subprocess.run(["winget", "install", "-e", "--id", "OpenJS.NodeJS"], check=True, shell=True)
            return True
        except Exception:
            try:
                subprocess.run(["choco", "install", "nodejs", "-y"], check=True, shell=True)
                return True
            except Exception:
                return False

    elif lang == "cpp":
        try:
            print(translate.get("gcc_check_a1"))
            result = subprocess.run(["g++", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version_str = result.stdout.split()[2]
                major_version = int(version_str.split('.')[0])
                print(f"{translate.get("gcc_found_compiler_ver")} {version_str}")
                if major_version >= 10:
                    print(f"{translate.get("gcc_sufficient_compiler_ver")} ({version_str})")
                    return True
                else:
                    print(f"{translate.get("gcc_old_compiler_ver")} ({version_str})")
        except Exception as e:
            print(f"{translate.get("gcc_error_a2")} {e}")

        try:
            print(translate.get("gcc_check_a2"))
            temp_dir = tempfile.mkdtemp(prefix="sc_mingw_")
            save_tempdir_mkhistory(temp_dir)
            mingw_url = "https://github.com/niXman/mingw-builds-binaries/releases/download/12.2.0-rt_v10-rev2/x86_64-12.2.0-release-posix-seh-msvcrt-rt_v10-rev2.7z"
            mingw_archive = os.path.join(temp_dir, "mingw.7z")
            print(f"{translate.get("gcc_check_a3").replace("***", mingw_url)}")
            with requests.get(mingw_url, stream=True) as r, open(mingw_archive, "wb") as f:
                total_bytes = 0
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    total_bytes += len(chunk)
                    print(f"{translate.get("gcc_check_a4").replace("***", f"{total_bytes / 1024 / 1024:.2f}")}", end='\r')
                print(f"{translate.get("gcc_check_a4_5").replace("***", f"{total_bytes / 1024 / 1024:.2f}")}")

            try:
                import py7zr # type: ignore (@UnresolvedImports)
                print(f"{translate.get("gcc_check_b1")}")
            except ImportError:
                print(f"{translate.get("pyzr_error_a1")}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
                import py7zr # type: ignore (@UnresolvedImports)
                print(f"{translate.get("py7zr_installed")}")

            with py7zr.SevenZipFile(mingw_archive, mode='r') as archive:
                archive.extractall(path=temp_dir)
            print(f"{translate.get("gcc_mingw_extracted")} {temp_dir}")

            mingw_bin = os.path.join(temp_dir, "mingw64", "bin")
            os.environ["PATH"] = mingw_bin + os.pathsep + os.environ.get("PATH", "")
            print(f"{translate.get("gcc_mingw_addpath")} {mingw_bin}")

            print(translate.get("msys_install") + f" | MinGW-w64: {mingw_bin}")
            if return_temp_cppdir:
                return temp_dir
            else:
                return True
        except Exception as e:
            print(f"{translate.get('msys_error_a1')} {e}")
            return False

    elif lang == "cs":
        if run_cmd(["csc"]):
            return True
        try:
            subprocess.run(["winget", "install", "-e", "--id", "Microsoft.DotNet.SDK.8"], check=True, shell=True)
            return True
        except Exception:
            try:
                subprocess.run(["choco", "install", "dotnetcore-sdk", "-y"], check=True, shell=True)
                return True
            except Exception:
                return False

    return False

def run_code():
    code = text.get("1.0", tk.END).strip()
    lang = language_var.get()
    theme = themes[current_theme]
    output_window = tk.Toplevel(root, background=theme['bg'], bg=theme['bg'], highlightbackground=theme['bg'], highlightthickness=1)
    output_window.title(translate.get("sc_output"))
    if os.name == "nt":
        try:
            output_window.iconbitmap(icon_path)
        except Exception:
            pass
    else:
        try:
            icon = tk.PhotoImage(file=os.path.abspath("slash.png"))
            output_window.iconphoto(True, icon)
        except Exception:
            pass
    output_text = tk.Text(output_window, font=font, bg=theme['bg'], fg=theme['fg'], insertbackground=theme['cursor'])
    output_text.pack(fill=tk.BOTH, expand=True)

    def show_error(message):
        output_text.insert(tk.END, f"{translate.get('error_a1')}: {message}\n")

    def check_runner(check_cmd, runner_name="", install_instructions=""):
        try:
            subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            output_text.insert(tk.END, runner_name + translate.get("runner_not_found") + translate.get("install_suggest") + translate.get("instructions") + f"{install_instructions}\n")
            return False

    try:
        if lang == "python":
            import io
            old_stdout = sys.stdout
            sys.stdout = sepstdout = io.StringIO()
            try:
                exec(code, {"__name__": "__main__", "__file__": current_file})
            except Exception as e:
                print(e)
            sys.stdout = old_stdout
            output = sepstdout.getvalue()

        elif lang == "javascript":
            if not check_runner(["node", "--version"], "Node.js", 
                                "Node: https://nodejs.org"):
                return
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, delete_on_close=False) as f:
                f.write(code)
                f.flush()
                f.close()
                result = subprocess.run(["node", f.name], capture_output=True, text=True)
            output = result.stdout + result.stderr
    
        elif lang == "cpp":
            if not check_runner(["g++", "--version"], "G++ compiler", "G++: https://sourceforge.net/projects/mingw/"):
                output_text.insert('1.0', "G++ " + translate.get("runner_not_found") +
                                   translate.get("install_suggest") + translate.get("instructions") +
                                   "G++: https://sourceforge.net/projects/mingw/\n")
                print(translate.get("gcc_error_b1"))
                return
            temp_dir = tempfile.mkdtemp(prefix='sc_')
            cpp_path = os.path.join(temp_dir, "temp.cpp")
            exe_path = os.path.join(temp_dir, f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))}.exe")
            if not os.path.exists(os.path.join(os.getenv("USERPROFILE"), ".slashcode")):
                os.mkdir(os.path.join(os.getenv("USERPROFILE"), ".slashcode"))
                os.mkdir(os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave"))
            save_tempdir_mkhistory(temp_dir)

            try:
                with open(cpp_path, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"{translate.get('cpp_usercode_written').replace('***', cpp_path)}")
                output = ""
                mingw_dir = None
                for std_flag in ["-std=c++17", "-std=c++14", "-std=c++11"]:
                    try:
                        if mingw_dir:
                            mingw_bin = os.path.join(mingw_dir, "mingw64", "bin")
                            env = os.environ.copy()
                            env["PATH"] = mingw_bin + os.pathsep + env.get("PATH", "")
                        else:
                            env = os.environ.copy()
                        cmd = ["g++", cpp_path, "-o", exe_path, std_flag,
                               "-pthread", "-static-libgcc", "-static-libstdc++", "-Wl,--enable-stdcall-fixup"]
                        print(f"{translate.get('gcc_compilation_attempt').replace('***', std_flag)} {' '.join(cmd)}")
                        compile_result = subprocess.run(cmd, capture_output=True, text=True, env=env)
                        version_result = subprocess.run(["g++", "--version"], capture_output=True, text=True, env=env)
                        print(f"{translate.get('gcc_used')} {version_result.stdout.splitlines()[0] if version_result.stdout else '(?)'}")
                        output_text.insert(tk.END, f"GCC: {version_result.stdout.splitlines()[0] if version_result.stdout else '(?)'}\n")
                        if compile_result.returncode == 0:
                            print(f"{translate.get('gcc_compilation_success')} ({exe_path})")
                            try:
                                run_result = subprocess.run([exe_path], text=True, creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
                                output_text.insert(tk.END, run_result.stdout + run_result.stderr + "\n")
                                print(f"{translate.get('gcc_execution_finished')}")
                                return
                            except Exception as e:
                                print(translate.get('gcc_execution_error_a1'), e)
                                output += f"{translate.get('error_d1')}{e}"
                                return
                        else:
                            print(f"{translate.get('gcc_compilation_failed').replace('***', std_flag)}")
                            print(compile_result.stderr)
                            output += f"{translate.get('compilation_error')}\n" + compile_result.stderr
                            try:
                                print(translate.get('gcc_check_b2'))
                                mingw_dir_new = install_runner("cpp", return_temp_cppdir=True)
                                if not mingw_dir_new:
                                    output += translate.get('gcc_error_b2')
                                else:
                                    mingw_dir = mingw_dir_new
                                    print(translate.get('gcc_compiler_installed'))
                            except Exception:
                                print(translate.get("gcc_error_a1"))
                    except Exception as e:
                        print(translate.get('error_d2') + f"\n\n{e}")
            except Exception as e:
                print(f"{translate.get('error_d1_5')}{e}")

        elif lang == "cs":
            if not check_runner(["csc"], translate.get('csc_compiler'), ".NET SDK: https://dotnet.microsoft.com"):
                output_text.insert(tk.END, translate.get('csc_error_a1'))
                if not install_runner("cs"):
                    output_text.insert(tk.END, translate.get('csc_autoinst_fail'))
                    print(translate.get('csc_error_a2'))
                return
            else:
                output += translate.get('csc_compiler_installed')

            temp_dir = tempfile.mkdtemp(prefix='sc_')
            cs_path = os.path.join(temp_dir, "temp.cs")
            exe_path = os.path.join(temp_dir, f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))}.exe")

            try:
                with open(cs_path, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"{translate.get('cs_usercode_written').replace('***', cs_path)}")
                output += f"{translate.get('cs_usercode_written').replace('***', cs_path)}"
                env = os.environ.copy()

                compile_cmd = ["csc", cs_path, f"/out:{exe_path}"]
                output_text.insert(tk.END, f"{translate.get('csc_compiling_with')} {' '.join(compile_cmd)}\n")

                compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, env=env)

                if compile_result.returncode == 0:
                    output_text.insert(tk.END, translate.get('csc_compilation_success'))
                    try:
                        run_result = subprocess.run([exe_path], text=True, creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
                        output += run_result.stdout + run_result.stderr + "\n"
                        print(translate.get('csc_execution_finished'))
                    except Exception as e:
                        error_msg = f"{translate.get('error_d1')}{e}"
                        print(translate.get('csc_execution_error_a1'), e)
                        output += error_msg
                else:
                    error_msg = f"{translate.get('compilation_error')}\n" + compile_result.stderr
                    print(f"{translate.get('compilation_error')}\n", compile_result.stderr)
                    output += error_msg

            except Exception as e:
                error_msg = f"{translate.get('error_d1_5')}{e}"
                output_text.insert(tk.END, error_msg)
                print(error_msg)

        elif lang == "html":
            import webbrowser
            with tempfile.NamedTemporaryFile("w", prefix="sc_", suffix=".html", delete=False, delete_on_close=False) as f:
                f.write(code)
                f.flush()
                f.close()
                file_url = "file://" + os.path.abspath(f.name)
                webbrowser.open_new_tab(file_url)
            output = translate.get("opened_in_browser")

        elif lang == "shell":
            output = ''
            if platform.system() in ("Linux", "Darwin"):
                try:
                    if current_file and os.path.isfile(current_file):
                        ext = Path(current_file).suffix.lower()
                        if ext in (".sh", ".bash", ".zsh"):
                            result = subprocess.run(["bash", current_file], capture_output=True, text=True)
                        else:
                            with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as temp_script:
                                temp_script.write(text.get(1.0, tk.END))
                                os.chmod(temp_script.name, 0o700)
                                result = subprocess.run(["bash", temp_script.name], capture_output=True, text=True)
                                os.unlink(temp_script.name)
                    else:
                        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as temp_script:
                            temp_script.write(text.get(1.0, tk.END))
                            os.chmod(temp_script.name, 0o700)
                            result = subprocess.run(["bash", temp_script.name], capture_output=True, text=True)
                            os.unlink(temp_script.name)

                    if result.returncode != 0:
                        show_error(result.stderr)
                    else:
                        output += result.stdout

                except Exception as e:
                   show_error(str(e))
            else:
                msg = f"{translate.get('sh_platform_not_supported')} ({platform.system().replace('Darwin', 'MacOS')})"
                show_error(msg)
                
        else:
            output = translate.get("language_not_supported")

    except subprocess.CalledProcessError as e:
        output = translate.get("process_error") + f"({e.returncode}):\n{e.stderr}"
    except Exception as e:
        output = translate.get("unexpected_error") + str(e)
    finally: # Cleanup
        if 'f' in locals() and hasattr(f, 'name'):
            try:
                if lang in ("python", "html"):
                    if lang == "python":
                        del sepstdout
                f.close()
                del f
                if lang in ("cpp", "cs"):
                    os.unlink(exe_path)
                    shutil.rmtree(temp_dir)
            except Exception as e:
                show_error(translate.get("cleanup_failed") + str(e))

    output_text.config(state='normal')
    output_text.insert("1.0", output)
    output_text.see(tk.END)
    output_text.config(state='disabled')
    
    def save_output():
        downloads_path = os.path.join(os.getenv("USERPROFILE"), "Downloads")
        sc_output_path = os.path.join(downloads_path, translate.get("sc_output"))
        if os.path.exists(sc_output_path):
            shutil.rmtree(sc_output_path)
        os.mkdir(sc_output_path)
        with open(os.path.join(sc_output_path, f"{translate.get('sc_output').lower().replace('-', '_')}.txt"), "w", encoding="utf-8") as f:
            f.write(fr'''{translate.get("output_sc_title")}
____________________________________________________________________________________
{output_text.get("1.0", tk.END)}''')   
    del output
    button_frame = tk.Frame(output_window, bg=theme['bg'])
    button_frame.pack(fill=tk.X, pady=10)
    sot = tk.Button(output_window, text=translate.get("save_output_text"), command=save_output)
    _exit = tk.Button(output_window, text=translate.get("exit"), command=lambda: root.after(50, output_window.destroy()))
    sot.pack(side=tk.LEFT, fill=tk.X, expand=True) ; _exit.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
def reboot_with_console(event=None):
    version_cmds = [["py", "--version"], ["python", "--version"], [fr"{sys.executable}", "--version"]]
    version_output = None

    for cmd in version_cmds:
        try:
            version_result = subprocess.run(cmd, text=True, capture_output=True)
            if version_result.returncode == 0:
                version_output = version_result.stdout.strip()
                break
        except Exception:
            continue

    if version_output is None:
        messagebox.showerror(translate.get("process_error").strip()[:-1], translate.get("py_error_a2"))
        return
    try:
        version_number = version_output.split()[1]
        major_minor = tuple(map(int, version_number.split('.')[:2]))
    except Exception:
        messagebox.showerror(translate.get("process_error").strip()[:-1], translate.get("py_error_a3"))
        return

    if major_minor in [(3, 13), (3, 14)]:
        userprofile_path = os.path.join(os.getenv("USERPROFILE"), "Downloads", "SlashCode", "SlashCode.py")
        if os.path.exists(userprofile_path):
            script_path = userprofile_path
        else:
            script_path = os.path.abspath("SlashCode.py")

        try:
            if platform.system() == "Windows":
                subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE, env=tcltk_env)
            elif platform.system() == "Linux":
                if shutil.which('gnome-terminal'):
                    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 "{script_path}"; exec bash'], env=tcltk_env)
                elif shutil.which('xterm'):
                    subprocess.Popen(['xterm', '--', 'bash', '-c', f'python3 "{script_path}"; exec bash'], env=tcltk_env)
                elif shutil.which("konsole"):
                    subprocess.Popen(['konsole', '-e', f'bash -c "python3 \\"{script_path}\\"; exec bash"'], env=tcltk_env)
            elif platform.system() == "Darwin":
                subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "python3 \\"{script_path}"\\"; exec bash"'], env=tcltk_env)
            root.destroy()
        except Exception as e:
            messagebox.showerror(translate.get("process_error").strip()[:-1], f"{translate.get('error_a5')}{e}")
            return
    else:
        messagebox.showerror(translate.get("py_error_a1_title"), translate.get("py_error_a1"))

sidebar_visible = [True]  
def show_sidebar():
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_visible[0] = True
    
def hide_sidebar():
    sidebar.pack_forget()
    sidebar_visible[0] = False

def update_line_numbers(event=None):
    if hasattr(update_line_numbers, 'after_id'):
        root.after_cancel(update_line_numbers.after_id)
    update_line_numbers.after_id = root.after(50, _actually_update_line_numbers)

def _actually_update_line_numbers():
    line_numbers.config(state='normal')
    line_numbers.delete('1.0', tk.END)
    row_count = int(text.index('end-1c').split('.')[0])
    lines = "\n".join(str(i) for i in range(1, row_count + 1))
    line_numbers.insert('1.0', lines)
    line_numbers.config(width=len(str(row_count)) + 1)
    line_numbers.config(state='disabled')


theme = themes[current_theme]
cpu_usage_frame = tk.Frame(sidebar, bg=theme['bg'])
cpu_usage_text = tk.Label(cpu_usage_frame, font=font, text="CPU: --%", bg=theme['bg'], fg=theme['fg'])
cpu_usage_text.pack()
ram_usage_frame = tk.Frame(sidebar, bg=theme['bg'])
ram_usage_text = tk.Label(ram_usage_frame, font=font, text="RAM: --% / --GB", bg=theme['bg'], fg=theme['fg'])
ram_usage_text.pack()
file_length_frame = tk.Frame(sidebar, bg=theme['bg'])   
file_length_text = tk.Label(file_length_frame, font=font, text="File Length: -- Character(s) | -- Word(s) | -- Line(s)", bg=theme['bg'], fg=theme['fg'], wraplength=200, justify=tk.LEFT)
file_length_text.pack()
process = psutil.Process(os.getpid())
app_cpu_usage_frame = tk.Frame(sidebar, bg=theme['bg'])
app_cpu_usage_text = tk.Label(app_cpu_usage_frame, font=font, text="App CPU: --%", bg=theme['bg'], fg=theme['fg'])
app_cpu_usage_text.pack()
app_ram_usage_frame = tk.Frame(sidebar, bg=theme['bg'])
app_ram_usage_text = tk.Label(app_ram_usage_frame, font=font, text="App RAM: --% / --GB", bg=theme['bg'], fg=theme['fg'])
app_ram_usage_text.pack()

psutil.cpu_percent(interval=0.5)

debug_visible = False
pending_update = None

def show_debug_info(event=None):
    global debug_visible, pending_update
    
    if not debug_visible:
        cpu_usage_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        ram_usage_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        file_length_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        app_cpu_usage_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        app_ram_usage_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        debug_visible = True
    
    cpu = psutil.cpu_percent()
    cpu_usage_text.config(text=f'CPU: {cpu:.1f}%')
    
    ram = psutil.virtual_memory()
    ram_usage_text.config(text=f'RAM: {ram.percent}% / {ram.used/(1024**3):.1f}GB')
    
    file_length = len(text.get("1.0", tk.END))
    word_count = len(text.get("1.0", tk.END).split())
    line_count = int(text.index('end-1c').split('.')[0])
    file_length_text.config(text=f'File Length: {file_length} Character(s) | {word_count} Word(s) | {line_count} Line(s)')
    
    app_cpu = process.cpu_percent(interval=0.1)
    app_ram = process.memory_info()
    total_ram = psutil.virtual_memory().total
    app_used_ram = (app_ram.rss / total_ram) * 100 
    app_cpu_usage_text.config(text=f'App CPU: {app_cpu:.1f}%')
    app_ram_usage_text.config(text=f'App RAM: {app_used_ram:.2f}% / {app_ram.rss/(1024**3):.2f}GB')
    
    if debug_visible:
        pending_update = root.after(2000, show_debug_info)

def hide_debug_info(event=None):
    global debug_visible, pending_update
    
    if pending_update:
        root.after_cancel(pending_update)
        pending_update = None
    
    cpu_usage_frame.pack_forget()
    ram_usage_frame.pack_forget()
    file_length_frame.pack_forget()
    app_cpu_usage_frame.pack_forget()
    app_ram_usage_frame.pack_forget()
    debug_visible = False

highlight_job = None
debounce_delay = 300
def on_key_release(event=None):
    global highlight_job
    if highlight_job is not None:
        root.after_cancel(highlight_job)
    content_size = len(text.get("1.0", tk.END))
    if content_size < 10000:
        highlight_job = root.after(debounce_delay, highlight_full_document)
    else:
        highlight_job = root.after(debounce_delay, highlight_line)
    update_line_numbers()
    
def clean_temp_files():
    temp_dir = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave")
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception:
                pass
            
is_fullscreen = False

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen():
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", False)

text.bind('<KeyRelease>', on_key_and_scroll)
text.bind('<MouseWheel>', on_mousewheel)
text.bind('<ButtonRelease-1>', on_button_release)
text.bind('<Configure>', on_configure)
text.bind("<<Paste>>", on_paste)
text.bind('<Return>', auto_indent)
text.bind('<BackSpace>', update_line_numbers)
text.bind('<Button-4>', update_line_numbers)
text.bind('<Button-5>', update_line_numbers)
text.bind("<Control-o>", open_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-d>", show_debug_info)
text.bind("<Control-k>", hide_debug_info)
text.bind("<Control-D>", open_folder)
text.bind("<Control-z>", undo_action)
text.bind("<Control-y>", redo_action)
text.bind("<Control-j>", show_sidebar)
text.bind("<Control-l>", hide_sidebar)
text.bind("<Control-r>", run_code)
text.bind("<Control-f>", find_text)
text.bind("<Control-h>", replace_text)
text.bind("<Control-n>", new_file)
text.bind("<Control-t>", clean_temp_files)
text.bind("<Control-T>", del_mkhistory_tempdirs)
text.bind("<Control-Alt-e>", reboot_with_console)
text.bind("<Control-W>", lambda: del_mkhistory_tempdirs(True))
text.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)
root.bind("<Control-minus>", zoom_out)
root.bind("<Control-underscore>", zoom_out)
root.bind("<Control-equal>", zoom_in)
root.bind("<Control-plus>", zoom_in)

update_line_numbers()

def show_complete_sidebar():
    show_sidebar()
    show_minimap()
def hide_complete_sidebar():
    hide_sidebar()
    hide_minimap()
    
save_new_file = tk.BooleanVar(value=True)

def set_ui():
    global file_menu, edit_menu, theme_menu, view_menu, run_menu, language_menu, guilang_menu
    global file_index, edit_index, theme_index, view_index, run_index, language_index, guilang_index
    menu.delete(0, tk.END)
    
    menu.add_cascade(label=translate.get("file"), menu=file_menu)
    file_index = menu.index(tk.END)
    file_menu.add_command(label=translate.get("new"), command=new_file, accelerator="Ctrl+N")
    file_menu.add_command(label=translate.get("open"), command=open_file, accelerator="Ctrl+O")
    file_menu.add_command(label=translate.get("open_folder"), command=open_folder, accelerator="Ctrl+Shift+D")
    file_menu.add_command(label=translate.get("save"), command=save_file, accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_checkbutton(label=translate.get("toggle_new_file_saving"), variable=save_new_file, onvalue=True, offvalue=False)
    file_menu.add_command(label=translate.get("clean_temp_files"), command=clean_temp_files, accelerator="Ctrl+T")
    file_menu.add_command(label=translate.get("clean_temp_directories"), command=del_mkhistory_tempdirs, accelerator="Ctrl+Shift+T")
    file_menu.add_command(label=translate.get("fully_wipe_directories"), command=lambda: del_mkhistory_tempdirs(True), accelerator="Ctrl+Shift+W")
    file_menu.add_separator()
    file_menu.add_command(label=translate.get("reboot_consolemode"), command=reboot_with_console, accelerator="Ctrl+Alt+E")
    file_menu.add_separator()
    file_menu.add_command(label=translate.get("exit"), command=root.quit)

    menu.add_cascade(label=translate.get("edit"), menu=edit_menu)
    edit_index = menu.index(tk.END)
    edit_menu.add_command(label=translate.get("undo"), command=undo_action, accelerator="Ctrl+Z")
    edit_menu.add_command(label=translate.get("redo"), command=redo_action, accelerator="Ctrl+Y")
    edit_menu.add_separator()
    edit_menu.add_command(label=translate.get("find"), command=find_text, accelerator="Ctrl+F")
    edit_menu.add_command(label=translate.get("replace"), command=replace_text, accelerator="Ctrl+H")

    menu.add_cascade(label=translate.get("theme"), menu=theme_menu)
    theme_index = menu.index(tk.END)
    theme_menu.add_command(label=translate.get("theme_light"), command=lambda: set_theme('light'))
    theme_menu.add_command(label=translate.get("theme_dark"), command=lambda: set_theme('dark'))
    theme_menu.add_command(label=translate.get("theme_dracula"), command=lambda: set_theme('dracula'))
    theme_menu.add_command(label=translate.get("theme_monokai"), command=lambda: set_theme('monokai'))
    theme_menu.add_command(label=translate.get("theme_night_owl"), command=lambda: set_theme('night_owl'))
    theme_menu.add_command(label=translate.get("theme_shades_of_purple"), command=lambda: set_theme('shades_of_purple'))
    theme_menu.add_command(label=translate.get("theme_high_contrast"), command=lambda: set_theme('high_contrast'))

    menu.add_cascade(label=translate.get("view"), menu=view_menu)
    view_index = menu.index(tk.END)
    view_menu.add_command(label=translate.get("zoom_in"), command=zoom_in, accelerator="Ctrl++")
    view_menu.add_command(label=translate.get("zoom_out"), command=zoom_out, accelerator="Ctrl+-")
    view_menu.add_separator()
    view_menu.add_command(label=translate.get("show_sidebar"), command=show_complete_sidebar, accelerator="Ctrl+J")
    view_menu.add_command(label=translate.get("hide_sidebar"), command=hide_complete_sidebar, accelerator="Ctrl+L")
    view_menu.add_command(label=translate.get("show_minimap"), command=show_minimap, accelerator="Ctrl+Shift+H")
    view_menu.add_command(label=translate.get("hide_minimap"), command=hide_minimap, accelerator="Ctrl+K")
    view_menu.add_separator()
    view_menu.add_command(label=translate.get("show_debug_info"), command=show_debug_info, accelerator="Ctrl+D")
    view_menu.add_command(label=translate.get("hide_debug_info"), command=hide_debug_info, accelerator="Ctrl+K")
    view_menu.add_separator()
    view_menu.add_command(label=translate.get("toggle_fullscreen"), command=toggle_fullscreen, accelerator="F11")
    view_menu.add_command(label=translate.get("exit_fullscreen"), command=exit_fullscreen, accelerator="Esc")

    menu.add_cascade(label=translate.get("run"), menu=run_menu)
    run_index = menu.index(tk.END)
    run_menu.add_command(label=translate.get("run_file"), command=run_code, accelerator="Ctrl+R")
   
    menu.add_cascade(label=translate.get("language"), menu=language_menu)
    language_index = menu.index(tk.END)
    language_menu.add_radiobutton(label=translate.get("plaintext"), variable=language_var, value='plaintext', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("python"), variable=language_var, value='python', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("javascript"), variable=language_var, value='javascript', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("css"), variable=language_var, value='css', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("html"), variable=language_var, value='html', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("cpp"), variable=language_var, value='cpp', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("cs"), variable=language_var, value='cs', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("markdown"), variable=language_var, value='markdown', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("renpy"), variable=language_var, value='renpy', command=highlight_language_change)
    language_menu.add_radiobutton(label=translate.get("shell"), variable=language_var, value='shell', command=highlight_language_change)


    menu.add_cascade(label=translate.get("gui_lang"), menu=guilang_menu)
    guilang_index = menu.index(tk.END)
    guilang_menu.add_radiobutton(label="English", variable=lang_var, value="en", image=language_icons['en'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="Nederlands", variable=lang_var, value="nl", image=language_icons['nl'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="Deutsch", variable=lang_var, value="de", image=language_icons['de'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="Español", variable=lang_var, value="es", image=language_icons['es'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="Italiano", variable=lang_var, value="it", image=language_icons['it'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="Français", variable=lang_var, value="fr", image=language_icons['fr'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="日本語", variable=lang_var, value="jp", image=language_icons['jp'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="中文", variable=lang_var, value="zh", image=language_icons['zh'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="한국인", variable=lang_var, value="ko", image=language_icons['ko'], compound=tk.LEFT, command=on_lang_change)
    guilang_menu.add_radiobutton(label="عربي", variable=lang_var, value="ar", image=language_icons['ar'], compound=tk.LEFT, command=on_lang_change)

def save_session():
    config_dir = os.path.expanduser('~/.slashcode')
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, 'session.json')

    session = {
        'file': "",
        'directory': globals().get('FOLDER', ""),
        'theme': current_theme,
        'language': language_var.get(),
        'guilang': translate.lang,
        'save_new_file': save_new_file.get()
    }

    if not current_file or not os.path.exists(current_file):
        if save_new_file.get():
            content = text.get(1.0, tk.END).rstrip('\n')
            if not content:
                with open(config_file, 'w') as f:
                    json.dump(session, f, indent=2)
                return

            ext = guess_language_from_content(content).replace('python', 'py').replace('javascript', 'js') \
                .replace('markdown', 'md').replace('renpy', 'rpy').replace('plaintext', 'txt')
            os.makedirs(os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave"), exist_ok=True)
            slashcode_file_dir = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave")
            for i in range(10):
                file_name = f"file_{i}.{ext}"
                slashcode_path = os.path.join(slashcode_file_dir, file_name)
                if not os.path.exists(slashcode_path):
                    break
            else:
                rand_str = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(7))
                file_name = f"file_{rand_str}.{ext}"
                slashcode_path = os.path.join(slashcode_file_dir, file_name)

            with open(slashcode_path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(slashcode_path)

            session['file'] = slashcode_path

    else:
        session['file'] = current_file

    with open(config_file, 'w') as f:
        json.dump(session, f, indent=2)

def on_close():
    save_session()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

def handle_command_line_args():
    global current_file, session
    
    if len(sys.argv) > 1:
        file_to_open = os.path.abspath(sys.argv[1])
        if os.path.isfile(file_to_open):
            current_file = file_to_open
            session['file'] = file_to_open
            load_file(file_to_open)
            return True
    return False

def load_session():
    config_dir = os.path.expanduser('~/.slashcode')
    config_file = os.path.join(config_dir, 'session.json')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

session = load_session()
try:
    print(f"{translate.get("session_loaded")}\n{session.replace('{{', '{{\n    ').replace(',', ',\n    ')}\n\n{translate.get("file")}{':' if lang_var.get() != "jp" else "："} {session['file']}")
except:
    pass
if not handle_command_line_args() and session.get('file'):
    try:
        current_file = session['file']
        load_file(current_file)
    except Exception as e:
        print(translate.get("error_b1") + f"{e}")
        
if session.get('directory'):
    try:
        open_folder(session['directory'], True)
    except Exception as e:
        print(translate.get("error_b2") + f"{e}")

if session.get('theme'):
    set_theme(session['theme'])
else:
    set_theme('light')
if session.get('guilang'):
    lang_var.set(session['guilang'])
    on_lang_change()
if session.get('language'):
    language_var.set(session['language'])
if session.get('save_new_file'):
    save_new_file.set(save_new_file.get())
            
root.after(100, update_minimap)
update_line_numbers()


root.mainloop()
