import tkinter as tk
import re
import keyword
import builtins
import os
from tkinter import filedialog, scrolledtext

root = tk.Tk()
if os.name == "nt":
    root.iconbitmap(os.path.abspath("slash.ico"))
else:
    icon = tk.PhotoImage(file="slash.png")
    root.iconphoto(True, icon)
root.title("Slash Code")

LANGUAGE_KEYWORDS = {
    'python': set(keyword.kwlist),
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
    }
}

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
    'html': {} # HTML doesn't have any functions (you'd need to use JavaScript).
}

html_attrs = {
    'id', 'class', 'style', 'src', 'href', 'alt', 'title', 'type', 'value', 'name',
    'placeholder', 'for', 'action', 'method', 'target', 'rel', 'disabled', 'checked',
    'selected', 'required', 'readonly', 'autofocus', 'maxlength', 'min', 'max'
} # Attributes like <div **style="...">.

def new_file(event=None):
    text.delete(1.0, tk.END)
    root.title("Slash Code")

def open_file(event=None):
    filetypes = [
    ("Python files", "*.py"),
    ("JavaScript files", "*.js"),
    ("HTML files", "*.html"),
    ("C files", "*.c"),
    ("C++ files", "*.cpp *.hpp"),
    ("Header files", "*.h"),
    ("Text files", "*.txt"),
    ("All files", "*.py *.js *.html *.c *.cpp *.hpp *.h *.txt"),
    ]
    file = filedialog.askopenfilename(filetypes=filetypes)
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()
            text.delete(1.0, tk.END)
            text.insert(tk.END, code)
            root.title(f"Slash Code - {os.path.basename(file)}")
            lang = get_language(file)
            if lang == 'plaintext':
                lang = guess_language_from_content(code)
            language_var.set(lang)
        highlight()

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
        filetypes = [("Python files", "*.py"), ("All files", "*.*")]
    elif language == "javascript":
        ext = ".js"
        filetypes = [("JavaScript files", "*.js"), ("All files", "*.*")]
    elif language == "html":
        ext = ".html"
        filetypes = [("HTML files", "*.html"), ("All files", "*.*")]
    elif language == "cpp":
        ext = ".cpp"
        filetypes = [("C++ files", "*.cpp"), ("All files", "*.*")]
    else:
        ext = ".txt"
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]

    file = filedialog.asksaveasfilename(
        title="Save As",
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

    if any(tag in content_lower for tag in ('<html>', '<div>', '<head>', '<body>')):
        return 'html'
    if any(keyword in content for keyword in ('#include', 'using namespace', 'std::')):
        return 'cpp'
    if any(keyword in content for keyword in ('def ', 'import ', 'from ', 'class ')):
        return 'python'
    if any(keyword in content for keyword in ('function(', 'console.log', 'const ', 'let ')):
        return 'javascript'    
    return 'plaintext'


            
def highlight(event=None):
    # Set the preferred language.
    language = language_var.get()
    keywords = LANGUAGE_KEYWORDS.get(language, set())
    funcs = LANGUAGE_FUNCS.get(language, set())
    
    # Remove all existing tags.
    for tag in ["keyword", "semicolon", "html_tag", "html_attr", "constant", "string", "comment", "function", "integer", "funccall",
                "prefix", "brace", "punctuation", "number", "dunder", "escape",
                "builtin", "variable", "preprocessor"]:
        text.tag_remove(tag, "1.0", tk.END)
    
    content = text.get("1.0", tk.END)
    
    comment_spans = []
    string_spans = []
    
    # Collect comments.
    if language == "python":
        for match in re.finditer(r'#.*', content):
            start, end = match.start(), match.end()
            comment_spans.append((start, end))
            text.tag_add("comment", f"1.0+{start}c", f"1.0+{end}c")
    elif language == "cpp":
        for match in re.finditer(r'//.*', content):
           start, end = match.start(), match.end()
           comment_spans.append((start, end))
           text.tag_add("comment", f"1.0+{start}c", f"1.0+{end}c")
        for match in re.finditer(r'/\*.*?\*/', content, re.DOTALL):
            start, end = match.start(), match.end()
            comment_spans.append((start, end))
            text.tag_add("comment", f"1.0+{start}c", f"1.0+{end}c")
        pattern = r'^[ \t]*(#(?:define|undef|include|if|ifdef|ifndef|else|elif|endif|error|pragma|line|using|import|module))(\b.*)$'
        for match in re.finditer(pattern, content, re.MULTILINE):
            start1, end1 = match.start(1), match.end(1)
            text.tag_add("preprocessor", f"1.0+{start1}c", f"1.0+{end1}c")
            start2, end2 = match.start(2), match.end(2)
            if start2 < end2:
                text.tag_add("preprocessor_rest", f"1.0+{start2}c", f"1.0+{end2}c")
           
    for match in re.finditer(r';', content): # If using any other language that is statically typed (most statically typed languages include the semicolon).
        start, end = match.start(), match.end()
        text.tag_add("semicolon", f"1.0+{start}c", f"1.0+{end}c")
    
    def is_in_string_or_comment(index):
        return any(s <= index < e for s, e in comment_spans + string_spans)
    
    # Process regular strings.
    for match in re.finditer(r'".*?"|\'.*?\'', content):
        start, end = match.start(), match.end()
        if not is_in_string_or_comment(start):
            string_spans.append((start, end))
            text.tag_add("string", f"1.0+{start}c", f"1.0+{end}c")
            # Highlight escape sequences.
            string_content = content[start:end]
            for esc_match in re.finditer(r'\\([nt\\\'"])', string_content):
                esc_start = start + esc_match.start()
                esc_end = start + esc_match.end()
                text.tag_add("escape", f"1.0+{esc_start}c", f"1.0+{esc_end}c")
                
    # Check for dunder methods (like __init__).
    for match in re.finditer(r'\b(__\w+__)\b', content):
        start, end = match.start(), match.end()
        text.tag_add("dunder", f"1.0+{start}c", f"1.0+{end}c")
        
    for match in re.finditer(r'\b\d+\b', content):
        start, end = match.start(), match.end()
        text.tag_add("integer", f"1.0+{start}c", f"1.0+{end}c")
    
    # Process f-strings with expression handling.
    for f_match in re.finditer(r'(?P<prefix>[fFrR]{1,2})(?P<quote>["\'])(?P<body>.*?)(?P=quote)', content, re.DOTALL):
        if is_in_string_or_comment(f_match.start()):
            continue
        
        prefix_start = f_match.start('prefix')
        quote_end = f_match.end('quote')
        body_start = f_match.start('body')
        body_end = f_match.end('body')
        
        string_spans.append((prefix_start, quote_end))
        text.tag_add("string", f"1.0+{prefix_start}c", f"1.0+{quote_end}c")
        text.tag_add("prefix", f"1.0+{prefix_start}c", f"1.0+{f_match.end('prefix')}c")
        
        # Split f-string body into literals and expressions.
        body = f_match.group('body')
        current_pos = body_start
        for part in re.finditer(r'(.*?)(\{.*?\}|$)', body):
            literal = part.group(1)
            expr = part.group(2)
            
            if literal:
                lit_start = current_pos
                lit_end = lit_start + len(literal)
                string_spans.append((lit_start, lit_end))
                text.tag_add("string", f"1.0+{lit_start}c", f"1.0+{lit_end}c")
                current_pos = lit_end
            
            if expr and expr.startswith('{'):
                # Process expression content.
                expr_start = current_pos
                expr_end = current_pos + len(expr)
                current_pos = expr_end
                
                # Remove the string tag from the expression.
                text.tag_remove("string", f"1.0+{expr_start}c", f"1.0+{expr_end}c")
                
                # Process the inner expression.
                inner_text = expr[1:-1]  # Remove the braces.
                inner_start = expr_start + 1
                
                # Tag punctuation (braces)
                text.tag_add("punctuation", f"1.0+{expr_start}c", f"1.0+{expr_start+1}c")
                text.tag_add("punctuation", f"1.0+{expr_end-1}c", f"1.0+{expr_end}c")
                
                # Tag code elements within the expression.
                for var_match in re.finditer(r'\b([a-zA-Z_]\w*)\b', inner_text):
                    v_start = inner_start + var_match.start(1)
                    v_end = inner_start + var_match.end(1)
                    if not any(text.tag_names(f"1.0+{v_start}c")):
                        text.tag_add("variable", f"1.0+{v_start}c", f"1.0+{v_end}c")
                
                for num_match in re.finditer(r'\b\d+\b', inner_text):
                    n_start = inner_start + num_match.start()
                    n_end = inner_start + num_match.end()
                    text.tag_add("number", f"1.0+{n_start}c", f"1.0+{n_end}c")
                
                for dunder_match in re.finditer(r'\b(__\w+__)\b', inner_text):
                    d_start = inner_start + dunder_match.start()
                    d_end = inner_start + dunder_match.end()
                    text.tag_add("dunder", f"1.0+{d_start}c", f"1.0+{d_end}c")
    
    # Tag keywords and functions outside strings.
    for match in re.finditer(r"\b(" + "|".join(keywords) + r")\b", content):
        if not is_in_string_or_comment(match.start()):
            text.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
    
    for match in re.finditer(r"\b(" + "|".join(funcs) + r")\b", content):
        if not is_in_string_or_comment(match.start()):
            text.tag_add("function", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
    
    # Tag function calls.
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', content):
        if not is_in_string_or_comment(match.start(1)):
            text.tag_add("funccall", f"1.0+{match.start(1)}c", f"1.0+{match.end(1)}c")
    
    # Tag the variables (outside strings and not other tagged elements).
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\b', content):
        if is_in_string_or_comment(match.start()):
            continue
        pos = f"1.0+{match.start()}c"
        if not any(text.tag_names(pos)):
            text.tag_add("variable", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
            
    if language == "html":
        for match in re.finditer(r'<(\/?\w+)', content):
            start = f"1.0+{match.start(1)}c"
            end = f"1.0+{match.end(1)}c"
            text.tag_add("html_tag", start, end)

        # Highlight HTML attributes.
        for match in re.finditer(r'\b(' + '|'.join(html_attrs) + r')\s*=', content):
            start = f"1.0+{match.start(1)}c"
            end = f"1.0+{match.end(1)}c"
            text.tag_add("html_attr", start, end)
            
    if language in ['python', 'javascript', 'cpp']:
        for match in re.finditer(r'\b([A-Z][A-Z0-9_]*[A-Z][A-Z0-9_]*)\b\s*=', content):
            if not is_in_string_or_comment(match.start()):
                text.tag_add("constant", f"1.0+{match.start(1)}c", f"1.0+{match.end(1)}c")

                      
themes = {
    'light': {
        'bg': '#ffffff', 'fg': '#000000',
        'keyword': '#0000ff', 'string': "#bf6900", 'comment': '#008000',
        'function': '#800080', 'funccall': '#00008b', 'integer': '#ffa500',
        'prefix': '#006400', 'line_numbers': '#f0f0f0', 'cursor': '#000000',
        'variable': '#000000', 'builtin': "#003a78", 'dunder': '#4F4F4F',
        'escape': '#404040', 'semicolon': "#4B4B4B", 'preprocessor': "#681968", 'preprocessor_rest': "#343434",
        'html_tag': "#68177B", 'html_attr': "#074a7c", 'constant': "#d86919",
    },
    'dark': {
        'bg': '#1e1e1e', 'fg': '#d4d4d4',
        'keyword': '#569cd6', 'string': '#ce9178', 'comment': '#6a9955',
        'function': '#c586c0', 'funccall': '#4ec9b0', 'integer': '#b5cea8',
        'prefix': '#9cdcfe', 'line_numbers': '#2d2d2d', 'cursor': '#d4d4d4',
        'variable': '#ffffff', 'builtin': "#60abfc", 'dunder': '#b0b0b0',
        'escape': "#7A7A7A", 'semicolon': "#A0A0A0", 'preprocessor': "#843E84", 'preprocessor_rest': "#636363",
        'html_tag': "#9625af", 'html_attr': "#0c79cd", 'constant': "#fc822b",
    }
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
    except tk.TclError:
        pass

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

font = ("Consolas", 12)
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

line_numbers.pack(side=tk.LEFT, fill=tk.Y)
text = scrolledtext.ScrolledText(frame, font=font, undo=True)
text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
text.bind("<Return>", auto_indent)
text.bind("}", handle_closing_brace)

def sync_scroll(event):
    line_numbers.yview_moveto(text.yview()[0])
    line_numbers.config(yscrollcommand=lambda *args: None)
    
def on_scroll(event):
    sync_scroll(event)
    update_line_numbers()
text.bind("<MouseWheel>", on_scroll)


text.bind("<Button-4>", on_scroll)
text.bind("<Button-5>", on_scroll)

def set_theme(theme_name):
    theme = themes[theme_name]
    text.config(bg=theme['bg'], fg=theme['fg'], insertbackground=theme['cursor'])
    line_numbers.config(bg=theme['line_numbers'], fg=theme['fg'])
    
    text.tag_configure("keyword", foreground=theme['keyword'])
    text.tag_configure("string", foreground=theme['string'])
    text.tag_configure("comment", foreground=theme['comment'])
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
    text.tag_raise("prefix")
    text.tag_raise("brace")
    text.tag_raise("punctuation")
    text.tag_raise("number")
    
set_theme('light')

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
    find_win.title("Find")
    tk.Label(find_win, text="Find:").pack(side=tk.LEFT)
    entry = tk.Entry(find_win)
    entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tk.Button(find_win, text="Find All", command=do_find).pack(side=tk.LEFT)
    entry.focus_set()


def update_line_numbers(event=None):
    line_numbers.config(state='normal')
    line_numbers.delete('1.0', tk.END)
    row_count = int(text.index('end-1c').split('.')[0])
    line_numbers.config(width=len(str(row_count)) + 1)
    line_numbers.insert('1.0', '\n'.join(str(i) for i in range(1, row_count + 1)))
    line_numbers.config(state='disabled')
    
def on_key_release(event):
    if event.keysym != "Return":
        update_line_numbers()
    highlight(event)

text.unbind("<KeyRelease>")
text.bind('<KeyRelease>', on_key_release)
text.bind('<Configure>', update_line_numbers)
text.bind("<<Paste>>", lambda e: (root.after(10, highlight)))
text.bind('<Return>', auto_indent)
text.bind('<BackSpace>', update_line_numbers)
text.bind("<Control-o>", open_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-z>", undo_action)
text.bind("<Control-y>", redo_action)
text.bind("<Control-f>", find_text)
text.bind("<Control-n>", new_file)

update_line_numbers()

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Undo", command=undo_action, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=redo_action, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text, accelerator="Ctrl+F")

theme_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light", command=lambda: set_theme('light'))
theme_menu.add_command(label="Dark", command=lambda: set_theme('dark'))

language_var = tk.StringVar(value='plaintext')
language_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Language", menu=language_menu)
language_menu.add_radiobutton(label="Plain Text", variable=language_var, value='plaintext', command=highlight)
language_menu.add_radiobutton(label="Python", variable=language_var, value='python', command=highlight)
language_menu.add_radiobutton(label="JavaScript", variable=language_var, value='javascript', command=highlight)
language_menu.add_radiobutton(label="HTML", variable=language_var, value='html', command=highlight)
language_menu.add_radiobutton(label="C++", variable=language_var, value='cpp', command=highlight)

root.mainloop()