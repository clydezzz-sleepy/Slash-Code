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
from platform import *
import threading
from tkinter import filedialog, scrolledtext, messagebox, ttk, font
current_file = ""
FOLDER = ""
open_folder_btn = None

root = tk.Tk()
if os.name == "nt" and sys.executable != "":
    try:
        root.iconbitmap(os.path.abspath("slash.ico"))
    except Exception:
        pass
else:
    try:
       icon = tk.PhotoImage(file=os.path.abspath("slash.png"))
       root.iconphoto(True, icon)
    except Exception:
        pass
root.title("Slash Code")

language_var = tk.StringVar(value='plaintext')
GUILANGS = {
    "en": {
    "gui_lang": "GUI Language",
    "msys_install": "MSYS2 installed. Please install MinGW via MSYS2 shell: pacman -S mingw-w64-x86_64-gcc",
    "error_a1": "Error",
    "error_a2": "Could not open file",
    "error_a3": "Could not open file:\n",
    "error_c0": "Folder button update error:",
    "error_c1": "Menu label update error:",
    "error_c2": "File label update error:",
    "error_c3": "Edit label update error:",
    "error_c4": "Theme label update error:",
    "error_c5": "Run label update error:",
    "error_c6": "View label update error:",
    "error_c7": "Language label update error:",
    "error_c8": "GUI language label update error:",
    "find": "Find",
    "find_query": "Find:",
    "runner_not_found": " not found!\n",
    "install_suggest": "Please install it first.\n",
    "instructions": "Instructions: ",
    "compilation_error": "Compilation Error:\n",
    "opened_in_browser": "Opened in default browser.",
    "language_not_supported": "Language not supported for execution.",
    "process_error": "Process Error ",
    "unexpected_error": "Unexpected Error: ",
    "cleanup_failed": "Cleanup failed: ",
    "file": "File",
    "new": "New",
    "open": "Open",
    "save": "Save",
    "toggle_new_file_saving": "Toggle New File Saving",
    "clean_temp_files": "Clean Temporary Files",
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
    "toggle_fullscreen": "Toggle Fullscreen",
    "exit_fullscreen": "Exit Fullscreen",
    "run": "Run",
    "run_file": "Run File",
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
    "all_files": "All Files",
    "error_b1": "Error loading file: ",
    "error_b2": "Error loading directory: "
    },
    
    "nl": {
    "gui_lang": "GUI Taal",
    "msys_install": "MSYS2 is geinstalleerd. Installeer alstublieft MinGW via de MSYS2 shell: pacman -S mingw-w64-x86_64-gcc",
    "error_a1": "Fout",
    "error_a2": "Kon niet bestand openen",
    "error_a3": "Kon niet bestand openen:\n",
    "error_c0": "Fout bij het bijwerken van de mapknop:",
    "error_c1": "Fout bij het bijwerken van het menulabel:",
    "error_c2": "Fout bij het bijwerken van het bestandslabel:",
    "error_c3": "Fout bij het bijwerken van het label:",
    "error_c4": "Fout bij het bijwerken van het themalabel:",
    "error_c5": "Fout bij het uitvoeren van de labelupdate:",
    "error_c6": "Fout bij het bijwerken van het label weergeven:",
    "error_c7": "Fout bij het bijwerken van het taallabel:",
    "error_c8": "Fout bij het bijwerken van het GUI-taallabel:",
    "find": "Vind",
    "find_query": "Vind:",
    "runner_not_found": " niet gevonden!\n",
    "install_suggest": "Installeer het alstublieft eerst.\n",
    "instructions": "Instructies: ",
    "compilation_error": "Compilatie fout:\n",
    "opened_in_browser": "Geopend in de standaard browser.",
    "language_not_supported": "Taal niet gesteund voor executie.",
    "process_error": "Proces fout ",
    "unexpected_error": "Onverwachte fout: ",
    "cleanup_failed": "Schoonmaking gefaald: ",
    "file": "Bestand",
    "new": "Nieuw",
    "open": "Open",
    "save": "Opslaan",
    "toggle_new_file_saving": "Nieuw Bestand Opslaan Inschakelen",
    "clean_temp_files": "Temporaire Bestanden Wissen",
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
    "toggle_fullscreen": "Volledig Scherm Inschakelen",
    "exit_fullscreen": "Volledig Scherm Verlaten",
    "run": "Uitvoeren",
    "run_file": "Bestand Uitvoeren",
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
    "all_files": "Alle Bestanden",
    "error_b1": "Fout gedurend bestand laden: ",
    "error_b2": "Fout gedurend map laden: "
    },
    "es": {
    "gui_lang": "GUI Lenguaje",
    "msys_install": "MSYS2 instalado. Por favor instala MinGW desde la terminal de MSYS2: pacman -S mingw-w64-x86_64-gcc",
    "error_a1": "Error",
    "error_a2": "No se pudo abrir el archivo",
    "error_a3": "No se pudo abrir el archivo:\n",
    "error_c0": "Error al actualizar el botón de carpeta:",
    "error_c1": "Error al actualizar la etiqueta del menú:",
    "error_c2": "Error al actualizar la etiqueta del archivo:",
    "error_c3": "Error al actualizar la etiqueta de edición:",
    "error_c4": "Error al actualizar la etiqueta del tema:",
    "error_c5": "Error al ejecutar la actualización de la etiqueta:",
    "error_c6": "Error al actualizar la etiqueta de la vista:",
    "error_c7": "Error al actualizar la etiqueta del idioma:",
    "error_c8": "Error al actualizar la etiqueta del idioma de la GUI:",
    "find": "Buscar",
    "find_query": "Buscar:",
    "runner_not_found": " no encontrado!\n",
    "install_suggest": "Por favor instálalo primero.\n",
    "instructions": "Instrucciones: ",
    "compilation_error": "Error de compilación:\n",
    "opened_in_browser": "Abierto en el navegador predeterminado.",
    "language_not_supported": "Idioma no compatible para ejecución.",
    "process_error": "Error del proceso ",
    "unexpected_error": "Error inesperado: ",
    "cleanup_failed": "Fallo al limpiar: ",
    "file": "Archivo",
    "new": "Nuevo",
    "open": "Abrir",
    "save": "Guardar",
    "toggle_new_file_saving": "Activar el guardado de nuevos archivos",
    "clean_temp_files": "Limpiar archivos temporales",
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
    "toggle_fullscreen": "Activar pantalla completa",
    "exit_fullscreen": "Salir de pantalla completa",
    "run": "Ejecutar",
    "run_file": "Ejecutar archivo",
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
    "all_files": "Todos Los Archivos",
    "error_b1": "Error al cargar el archivo: ",
    "error_b2": "Error al cargar el directorio: "
    },
    
    "fr": {
    "gui_lang": "Langue de l'interface",
    "msys_install": "MSYS2 est installé. Veuillez installer MinGW via le terminal MSYS2 : pacman -S mingw-w64-x86_64-gcc",
    "error_a1": "Erreur",
    "error_a2": "Impossible d'ouvrir le fichier",
    "error_a3": "Impossible d'ouvrir le fichier:\n",
    "error_c0": "Erreur de mise à jour du bouton de dossier:",
    "error_c1": "Erreur de mise à jour du libellé du menu:",
    "error_c2": "Erreur de mise à jour du libellé du fichier:",
    "error_c3": "Erreur de mise à jour de l'étiquette de modification:",
    "error_c5": "Erreur de mise à jour de l'étiquette d'exécution:",
    "error_c6": "Erreur de mise à jour de l'étiquette d'affichage:",
    "error_c7": "Erreur de mise à jour du libellé de langue:",
    "error_c8": "Erreur de mise à jour du libellé de langue de l'interface graphique:",
    "find": "Rechercher",
    "find_query": "Rechercher:",
    "runner_not_found": " introuvable!\n",
    "install_suggest": "Veuillez l'installer d'abord.\n",
    "instructions": "Instructions: ",
    "compilation_error": "Erreur de compilation:\n",
    "opened_in_browser": "Ouvert dans le navigateur par défaut.",
    "language_not_supported": "Langue non prise en charge pour l'exécution.",
    "process_error": "Erreur de processus ",
    "unexpected_error": "Erreur inattendue: ",
    "cleanup_failed": "Échec du nettoyage: ",
    "file": "Fichier",
    "new": "Nouveau",
    "open": "Ouvrir",
    "save": "Enregistrer",
    "toggle_new_file_saving": "Activer l'enregistrement d'un nouveau fichier",
    "clean_temp_files": "Nettoyer les fichiers temporaires",
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
    "toggle_fullscreen": "Activer le plein écran",
    "exit_fullscreen": "Quitter le plein écran",
    "run": "Exécuter",
    "run_file": "Exécuter le fichier",
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
    "all_files": "Tous Les Fichiers",
    "error_b1": "Erreur lors du chargement du fichier: ",
    "error_b2": "Erreur lors du chargement du dossier: "
    },
    
    "jp": {
    "gui_lang": "GUI 言語",
    "msys_install": "MSYS2がインストールされました。MSYS2シェルでMinGWをインストールしてください: pacman -S mingw-w64-x86_64-gcc",
    "error_a1": "エラー",
    "error_a2": "ファイルを開けませんでした",
    "error_a3": "ファイルを開けませんでした:\n",
    "error_c0": "フォルダボタン更新エラー:",
    "error_c1": "メニューラベル更新エラー:",
    "error_c2": "ファイルラベル更新エラー:",
    "error_c3": "編集ラベル更新エラー:",
    "error_c4": "テーマラベル更新エラー:",
    "error_c5": "実行ラベル更新エラー:",
    "error_c6": "表示ラベル更新エラー:",
    "error_c7": "言語ラベル更新エラー:",
    "error_c8": "GUI言語ラベル更新エラー:",
    "find": "検索",
    "find_query": "検索：",
    "runner_not_found": " が見つかりません！\n",
    "install_suggest": "まずインストールしてください。\n",
    "instructions": "使い方：",
    "compilation_error": "コンパイルエラー：\n",
    "opened_in_browser": "デフォルトのブラウザで開きました。",
    "language_not_supported": "この言語は実行に対応していません。",
    "process_error": "プロセスエラー ",
    "unexpected_error": "予期しないエラー：",
    "cleanup_failed": "クリーンアップに失敗しました：",
    "file": "ファイル",
    "new": "新規",
    "open": "開く",
    "save": "保存",
    "toggle_new_file_saving": "新しいファイルの保存を切り替える",
    "clean_temp_files": "一時ファイルを消去する",
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
    "toggle_fullscreen": "全画面表示の切り替え",
    "exit_fullscreen": "全画面表示を終了",
    "run": "実行",
    "run_file": "ファイルを実行",
    "highlighting_as": "ハイライト：",
    "plaintext": "プレーンテキスト",
    "python": "Python",
    "javascript": "JavaScript",
    "css": "CSS",
    "html": "HTML",
    "cpp": "C++",
    "cs": "C#",
    "markdown": "Markdown",
    "renpy": "Ren'Py",
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
    "renpy_files": "Ren'Py Files",
    "all_files": "全てのファイル",
    "error_b1": "ファイルの読み込みエラー：",
    "error_b2": "ディレクトリの読み込みエラー："
}
}

class GUITranslate:
    def __init__(self, lang="en"):
        self.lang = lang
        self.load_lang()
        
    def load_lang(self):
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
        return self.data.get(key, key)
    
    def set_language(self, lang):
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
    print(translate.get("highlighting_as") + f"{language_var.get()}")
    if os.path.getsize(current_file) > 200_000:
            root.after(150, highlight_full_document)
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
        "es": "Español",
        "fr": "Français",
        "jp": "日本語"
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
        file_menu.entryconfig(5, label=translate.get("clean_temp_files"))
        file_menu.entryconfig(6, label=translate.get("exit"))
    except Exception as e:
        print(translate.get("error_c2"), e)

    try:
        edit_menu.entryconfig(0, label=translate.get("undo"))
        edit_menu.entryconfig(1, label=translate.get("redo"))
        edit_menu.entryconfig(3, label=translate.get("find"))
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
        guilang_menu.entryconfig(2, label="Español")
        guilang_menu.entryconfig(3, label="Français")
        guilang_menu.entryconfig(4, label="日本語")
    except Exception as e:
        print(translate.get("error_c8"), e)

def create_sidebar_buttons():
    global open_folder_btn
    open_folder_btn = tk.Button(
        sidebar,
        text=translate.get("open_folder"),
        command=open_folder,
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
    'renpy', 'define', 'default', 'config', 'persistent', 'store', 'gui', 'style', 'theme'
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
    'var', 'void', 'while', 'with', 'yield', 'async', 'arguments', 'eval'
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
    'renpy': renpy_kw
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
        '`', '```'
    },
    'renpy': renpy_fn
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
    }
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

current_file = ""

def new_file(event=None):
    text.delete(1.0, tk.END)
    update_line_numbers()
    root.title("Slash Code")

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
        (translate.get("all_files"), "*.*"),
    ]
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    
    if file_path:
        current_file = file_path
        threading.Thread(
            target=read_file_thread, 
            args=(file_path,),
            daemon=True
        ).start()

def read_file_thread(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        root.after(0, update_gui, file_path, content)
    except Exception as e:
        root.after(0, show_error, e)

def update_gui(file_path, content):
    text.delete(1.0, tk.END)
    text.insert(tk.END, content)
    text.edit_separator()
    root.title(f"Slash Code - {os.path.basename(file_path)}")
    lang = get_language(file_path)
    if lang == 'plaintext':
        lang = guess_language_from_content(content)
    language_var.set(lang)
    update_line_numbers()
    highlight_full_document()

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
        filetypes = [(translate.get("markdown_files"), "*.cpp"), (translate.get("all_files"), "*.*")]
    elif language == "renpy":
        ext = ".rpy"
        filetypes = [(translate.get("renpy_files"), "*.cpp"), (translate.get("all_files"), "*.*")]
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
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text.get(1.0, tk.END))
        root.title(f"Slash Code - {os.path.basename(file)}")
        
def get_language(file_path):
    if file_path.endswith('.py'):
        return 'python'
    elif file_path.endswith('.js'):
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
    
def highlight_visible(target=None):
    if target is None:
        target = text
    first = target.index("@0,0")
    last = target.index(f"@0,{target.winfo_height()}")
    first_line = int(first.split('.')[0])
    last_line = int(last.split('.')[0])
    for line in range(first_line, last_line + 1):
        region_start = f"{line}.0"
        region_end = f"{line}.end"
        content = target.get(region_start, region_end)
        for tag in target.tag_names():
            target.tag_remove(tag, region_start, region_end)
        highlight(target=target, region_start=region_start, region_end=region_end, content=content)
    
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
    if language in ("python", "renpy"):
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
    for match in re.finditer(r'\b(__\w+__)\b', content):
        s, e = match.start(), match.end()
        target.tag_add("dunder", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Integers ---
    for match in re.finditer(r'\b\d+\b', content):
        s, e = match.start(), match.end()
        if not is_in_string_or_comment(s):
            target.tag_add("integer", f"{region_start}+{s}c", f"{region_start}+{e}c")
            
    # --- f-strings (Python, Ren'Py for "[]" and C# for $"{}") ---
    if language in ("python", "renpy", "cs"):
        if language == "python":
            string_pattern = r'(?P<prefix>[fFrR]{1,2})?(?P<quote>["\'])(?P<body>.*?)(?P=quote)'
        elif language == "renpy":
            string_pattern = r'(?P<prefix>[fFrR]{1,2})?(?P<quote>["\'])(?P<body>.*?)(?P=quote)'
        elif language == "cs":
            string_pattern = r'(?P<prefix>[\$]{1,2})?(?P<quote>["\'])(?P<body>.*?)(?P=quote)'
        for f_match in re.finditer(string_pattern, content, re.DOTALL):
            if is_in_string_or_comment(f_match.start()):
                continue
  
            prefix = f_match.group('prefix') or ''
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
                interpolation_pattern = r'(\{.*?\})'
            elif language == "cs":
                if '$' not in prefix:
                    continue
                interpolation_pattern = r'(\{.*?\})'
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

                    for dunder_match in re.finditer(r'\b(__\w+__)\b', inner_text):
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
    if language in ("python", "renpy"):
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
        highlight_full_document()
    except tk.TclError:
        pass

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

font_size = 12
if lang_var.get() == "jp":
    font = ("NSJP.ttf", font_size)
else:
    font = ("Consolas", font_size)
line_numbers = tk.Text(
    frame,
    font=font,
    width=4,
    padx=4,
    takefocus=0,
    border=0,
    background='#f0f0f0',
    state='disabled',
    wrap='none',
    yscrollcommand=lambda *args: None  # Disable own scroll
)

current_theme = 'light'
theme_var = tk.StringVar(value=current_theme)

line_numbers.pack(side=tk.LEFT, fill=tk.Y)
text = scrolledtext.ScrolledText(frame, font=font, undo=True)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text.bind("<Return>", auto_indent)
text.bind("}", handle_closing_brace)

minimap_frame = tk.Frame(root, width=0, bg=themes[theme_var.get()]['bg'])
minimap_frame.place(relx=0.99065, rely=0.515, anchor="ne")
minimap_font = tk.font.Font(family="Consolas", size=4)
def set_minimap():
    global minimap
    minimap = tk.Text(minimap_frame, font=minimap_font, width=62, height=78, state='disabled', bg=themes[theme_var.get()]['bg'], fg=themes[theme_var.get()]['fg'])
set_minimap()
minimap.pack(fill=tk.Y, expand=True)

for tag, color in themes[theme_var.get()].items():
    if tag in ["bg", "fg", "line_numbers", "cursor"]: continue
    minimap.tag_configure(tag, foreground=color)
    
def highlight_minimap():
    content = text.get("1.0", "end-1c")
    minimap.config(state='normal')
    minimap.delete("1.0", "end")
    minimap.insert("1.0", content)
    minimap.config(state='disabled')
    minimap.config(state='normal')
    highlight(target=minimap, content=content)
    minimap.config(state='disabled')


def hide_minimap():
    minimap.pack_forget()
    
def show_minimap():
    minimap.pack(fill=tk.Y, expand=True)
    
def update_minimap(event=None):
    global minimap
    if not minimap:
        return 
    minimap.config(state='normal')
    minimap.delete('1.0', tk.END)
    minimap.insert('1.0', text.get('1.0', tk.END))
    minimap.config(state='disabled')
    
def sync_scroll(*args):
    text.yview_moveto(text.yview()[0])
    minimap.yview_moveto(text.yview()[0])

text.bind('<<Modified>>', lambda e: (update_minimap(), text.edit_modified(0)))

def zoom_in(event=None):
    global font_size, font
    font_size = min(36, font_size + 2)
    font = ("Consolas", font_size)
    text.config(font=font)
    line_numbers.config(font=font)
    update_line_numbers()

def zoom_out(event=None):
    global font_size, font
    font_size = max(8, font_size - 2)
    font = ("Consolas", font_size)
    text.config(font=font)
    line_numbers.config(font=font)
    update_line_numbers()

def sync_scroll(event=None):
    line_numbers.yview_moveto(text.yview()[0])
    minimap.yview_moveto(text.yview()[0])
    line_numbers.config(yscrollcommand=lambda *args: None)
    
def on_scroll(event):
    sync_scroll(event)
    update_line_numbers()
    
def on_minimap_click(event):
    height = minimap.winfo_height()
    clicked_fraction = event.y / height
    text.yview_moveto(clicked_fraction)
    update_minimap()
    
minimap.bind("<Button-1>", on_minimap_click)
text.bind("<MouseWheel>", on_scroll)

text.bind("<Button-4>", on_scroll)
text.bind("<Button-5>", on_scroll)

sidebar = tk.Frame(frame, width=200, bg=themes[theme_var.get()]['bg'])
sidebar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(sidebar)
tree.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

scrollbar = tk.Scrollbar(sidebar, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def synced_scroll(first, last):
    text.yview_moveto(first)
    line_numbers.yview_moveto(first)
    scrollbar.set(first, last)

    update_line_numbers()
    
text.config(yscrollcommand=lambda *args: synced_scroll(*args))
line_numbers.config(yscrollcommand=lambda *args: synced_scroll(*args))

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
                highlight_full_document()
            except Exception as e:
                messagebox.showerror(translate.get("error_a1"), translate.get("error_a2") + f"\n{e}")

file_listbox = tk.Listbox(sidebar, width=30, bg=themes[theme_var.get()]['bg'], fg=themes[theme_var.get()]['fg'], selectbackground=themes[theme_var.get()]['keyword'])
file_listbox.bind("<<ListboxSelect>>", open_selected_file)
file_listbox.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

def insert_nodes(parent, path):
    try:
        for name in sorted(os.listdir(path)):
            abspath = os.path.join(path, name)
            isdir = os.path.isdir(abspath)
            node = tree.insert(parent, "end", text=name, open=False)
            if isdir:
                tree.insert(node, "end")
    except Exception:
        pass

def get_full_path(node):
    path = ""
    while node:
        name = tree.item(node, "text")
        path = os.path.join(name, path) if path else name
        node = tree.parent(node)
    return os.path.abspath(path)

def on_tree_double_click(event=None):
    node = tree.focus()
    path = get_full_path(node)
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
                text.delete(1.0, tk.END)
                text.insert(tk.END, code)
                root.title(f"Slash Code - {os.path.basename(path)}")
                lang = get_language(path)
                if lang == 'plaintext':
                    lang = guess_language_from_content(code)
                language_var.set(lang)
                globals()['current_file'] = path
                update_line_numbers()
                highlight_full_document()
                highlight(target=minimap)
        except Exception as e:
            messagebox.showerror(translate.get("error_a1"), translate.get("error_a2") + f"\n{e}")
        
tree.bind("<Double-1>", on_tree_double_click)

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

def on_open_node(event):
    node = tree.focus()
    path = get_full_path(node)
    if tree.get_children(node):
        first_child = tree.get_children(node)[0]
        if not tree.get_children(first_child):
            tree.delete(first_child)
            insert_nodes(node, path)

tree.bind("<<TreeviewOpen>>", on_open_node)

create_sidebar_buttons()
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
    tk.Button(find_win, text="Find All", command=do_find).pack(side=tk.LEFT)
    entry.focus_set()

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
            
def install_runner(lang):
    if platform.system() == "Windows":
        if lang == "javascript":
            try:
                subprocess.run(["node", "--version"], capture_output=True, check=True)
                return True
            except:
                pass
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
                subprocess.run(["g++", "--version"], capture_output=True, check=True)
                return True
            except:
                pass
            try:
                subprocess.run(["winget", "install", "-e", "--id", "MSYS2.MSYS2"], check=True, shell=True)
                print(translate.get("msys_install"))
                return False
            except Exception:
                return False
        elif lang == "cs":
            try:
                subprocess.run(["csc"], capture_output=True, check=True)
                return True
            except:
                pass
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
    output_window = tk.Toplevel(root)
    output_window.title("Output")
    output_text = tk.Text(output_window, font=font)
    output_text.pack(fill=tk.BOTH, expand=True)

    def show_error(message):
        output_text.insert(tk.END, f"Error: {message}\n")

    def check_runner(runner_name, check_cmd, install_instructions):
        try:
            subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            output_text.insert(tk.END, runner_name + translate.get("runner_not_found") + f" Please install it first.\n" + translate.get("instructions") + f"{install_instructions}\n")
            return False

    try:
        if lang == "python":
            import io
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            try:
                exec(code, {})
            except Exception as e:
                print(e)
            sys.stdout = old_stdout
            output = mystdout.getvalue()

        elif lang == "javascript":
            if not check_runner("Node.js", ["node", "--version"], 
                              "https://nodejs.org"):
                return
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
                f.write(code)
                f.flush()
                result = subprocess.run(["node", f.name], capture_output=True, text=True)
            output = result.stdout + result.stderr

        elif lang == "cpp":
            if not check_runner("G++ compiler", ["g++", "--version"],
                              "https://sourceforge.net/projects/mingw/"):
                return
            with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as f:
                f.write(code)
                f.flush()
                exe_file = f.name + ".exe"
                compile_result = subprocess.run(
                    ["g++", f.name, "-o", exe_file],
                    capture_output=True,
                    text=True
                )
                if compile_result.returncode == 0:
                    run_result = subprocess.run([exe_file], capture_output=True, text=True)
                    output = run_result.stdout + run_result.stderr
                else:
                    output = "Compilation Error:\n" + compile_result.stderr

        elif lang == "cs":
            if not check_runner("C# Compiler (csc)", ["csc"],
                              "Install .NET SDK: https://dotnet.microsoft.com"):
                return
            with tempfile.NamedTemporaryFile("w", suffix=".cs", delete=False) as f:
                f.write(code)
                f.flush()
                exe_file = f.name.replace(".cs", ".exe")
                compile_result = subprocess.run(
                    ["csc", f.name],
                    capture_output=True,
                    text=True
                )
                if compile_result.returncode == 0:
                    run_result = subprocess.run([exe_file], capture_output=True, text=True)
                    output = run_result.stdout + run_result.stderr
                else:
                    output = translate.get("compilation_error") + compile_result.stderr

        elif lang == "html":
            import webbrowser
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
                f.write(code)
                f.flush()
                webbrowser.open(f.name)
            output = translate.get("opened_in_browser")

        else:
            output = translate.get("language_not_supported")

    except subprocess.CalledProcessError as e:
        output = translate.get("process_error") + f" ({e.returncode}):\n{e.stderr}"
    except Exception as e:
        output = translate.get("unexpected_error") + f"{str(e)}"
    finally:
        if 'f' in locals() and hasattr(f, 'name'):
            try:
                os.unlink(f.name)
                if lang in ("cpp", "cs"):
                    os.unlink(exe_file)
            except Exception as e:
                show_error(translate.get("cleanup_failed") + f"{str(e)}")

    output_text.insert("1.0", output)
    output_text.see(tk.END)

sidebar_visible = [True]  
def show_sidebar():
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_visible[0] = True
    
def hide_sidebar():
    sidebar.pack_forget()
    sidebar_visible[0] = False

def update_line_numbers(event=None):
    if text.edit_modified():
        line_numbers.config(state='normal')
        line_numbers.delete('1.0', tk.END)
        row_count = int(text.index('end-1c').split('.')[0])
        line_numbers.config(width=len(str(row_count)) + 1)
        line_numbers.insert('1.0', '\n'.join(str(i) for i in range(1, row_count + 1)))
        line_numbers.config(state='disabled')
    text.edit_modified(False)
    
highlight_job = None
debounce_delay = 300
def on_key_release(event=None):
    global highlight_job
    if highlight_job is not None:
        root.after_cancel(highlight_job)
    content_size = len(text.get("1.0", tk.END))
    if content_size < 5000:
        highlight_job = root.after(debounce_delay, highlight_full_document)
    else:
        highlight_job = root.after(debounce_delay, highlight_line)
    update_line_numbers()
    
def clean_temp_files():
    temp_dir = os.path.join(os.getenv("USERPROFILE"), ".slashcode", "tempsave")
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            print(file_path)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
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

text.unbind("<KeyRelease>")
text.bind('<KeyRelease>', lambda e: (on_key_release(), sync_scroll()))
text.bind('<MouseWheel>', lambda e: sync_scroll())
text.bind('<ButtonRelease-1>', lambda e: sync_scroll())
text.bind('<Configure>', update_line_numbers)
text.bind("<<Paste>>", lambda: (root.after(10, highlight_full_document)))
text.bind('<Return>', auto_indent)
text.bind('<BackSpace>', update_line_numbers)
text.bind("<Control-o>", open_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-D>", open_folder)
text.bind("<Control-z>", undo_action)
text.bind("<Control-y>", redo_action)
text.bind("<Control-j>", show_sidebar)
text.bind("<Control-l>", hide_sidebar)
text.bind("<Control-r>", run_code)
text.bind("<Control-f>", find_text)
text.bind("<Control-n>", new_file)
text.bind("<Control-t>", clean_temp_files)
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
    file_menu.add_separator()
    file_menu.add_command(label=translate.get("exit"), command=root.quit)

    menu.add_cascade(label=translate.get("edit"), menu=edit_menu)
    edit_index = menu.index(tk.END)
    edit_menu.add_command(label=translate.get("undo"), command=undo_action, accelerator="Ctrl+Z")
    edit_menu.add_command(label=translate.get("redo"), command=redo_action, accelerator="Ctrl+Y")
    edit_menu.add_separator()
    edit_menu.add_command(label=translate.get("find"), command=find_text, accelerator="Ctrl+F")

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
    view_menu.add_command(label=translate.get("toggle_fullscreen"), command=toggle_fullscreen)
    view_menu.add_command(label=translate.get("exit_fullscreen"), command=exit_fullscreen)

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


    menu.add_cascade(label=translate.get("gui_lang"), menu=guilang_menu)
    guilang_index = menu.index(tk.END)
    guilang_menu.add_radiobutton(label="English", variable=lang_var, value="en", command=on_lang_change)
    guilang_menu.add_radiobutton(label="Nederlands", variable=lang_var, value="nl", command=on_lang_change)
    guilang_menu.add_radiobutton(label="Español", variable=lang_var, value="es", command=on_lang_change)
    guilang_menu.add_radiobutton(label="Français", variable=lang_var, value="fr", command=on_lang_change)
    guilang_menu.add_radiobutton(label="日本語", variable=lang_var, value="jp", command=on_lang_change)

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
    print(f"Loaded session: {session}\n\nFile: {session['file']}")
except:
    pass
if session.get('file'):
    try:
        with open(session['file'], 'r', encoding='utf-8') as f:
            content = f.read()
        root.after(0, update_gui, session['file'], content)
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
if session.get('language'):
    language_var.set(session['language'])
if session.get('guilang'):
    lang_var.set(session['guilang'])
    on_lang_change()
if session.get('save_new_file'):
    save_new_file.set(save_new_file.get())
highlight_full_document()


if len(sys.argv) > 1:
    file_to_open = os.path.abspath(sys.argv[1])
    if os.path.isfile(file_to_open):
        try:
            with open(file_to_open, "r", encoding="utf-8") as f:
                text.delete("1.0", tk.END)
                text.insert("1.0", f.read())
            root.title(f"Slash Code - {os.path.basename(file_to_open)}")
            current_file = file_to_open
            highlight_full_document()
            save_session()
            load_session()
        except Exception as e:
            messagebox.showerror(translate.get("error_a1"), translate.get("error_a3") + f"{e}")
            
root.after(100, update_minimap)
update_line_numbers()
            
root.mainloop()
