### SlashCode

import tkinter as tk
import re
import keyword
import builtins
import os
import json
import sys
from functools import lru_cache
from tkinter import filedialog, scrolledtext

root = tk.Tk()
if os.name == "nt" and sys.executable != "":
    try:
        root.iconbitmap(os.path.abspath("slash.ico"))
    except Exception:
        pass
else:
    icon = tk.PhotoImage(file=os.path.abspath("slash.png"))
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
    "html": set()
}

html_attrs = {
    'id', 'class', 'style', 'src', 'href', 'alt', 'title', 'type', 'value', 'name',
    'placeholder', 'for', 'action', 'method', 'target', 'rel', 'disabled', 'checked',
    'selected', 'required', 'readonly', 'autofocus', 'maxlength', 'min', 'max'
} # Attributes like <div **style="...">.

def new_file(event=None):
    text.delete(1.0, tk.END)
    root.title("Slash Code")
    
current_file = ""

def open_file(event=None):
    global current_file
    filetypes = [
    ("Python files", "*.py"),
    ("JavaScript files", "*.js"),
    ("HTML files", "*.html"),
    ("C files", "*.c"),
    ("C++ files", "*.cpp *.hpp"),
    ("Header files", "*.h"),
    ("Text files", "*.txt"),
    ("C# files", "*.cs"),
    ("All files", "*.py *.js *.html *.c *.cpp *.hpp *.h *.cs *.txt"),
    ]
    file = filedialog.askopenfilename(filetypes=filetypes)
    if file:
        current_file = file
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()
            text.delete(1.0, tk.END)
            text.insert(tk.END, code)
            root.title(f"Slash Code - {os.path.basename(file)}")
            lang = get_language(file)
            if lang == 'plaintext':
                lang = guess_language_from_content(code)
            language_var.set(lang)
        highlight_full_document()

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
    elif file_path.endswith('.cs'):
        return 'cs'
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
    return 'plaintext'

def highlight_line(event=None):
    line = text.index("insert").split('.')[0]
    region_start = f"{line}.0"
    region_end = f"{line}.end"
    content = text.get(region_start, region_end)
    for tag in text.tag_names():
        text.tag_remove(tag, region_start, region_end)
    highlight(region_start=region_start, region_end=region_end, content=content)
    
def highlight_full_document():
    highlight(full_document=True)

def highlight(event=None, full_document=False, region_start=None, region_end=None, content=None):
    """
    If full_document is True, highlights the whole file.
    If False (default), highlights only the current line.
    """
    language = language_var.get()
    keywords = LANGUAGE_KEYWORDS.get(language, set())
    funcs = LANGUAGE_FUNCS.get(language, set())
    types = LANGUAGE_TYPES.get(language, set())
    html_attr_pattern = r'\b(' + '|'.join(html_attrs) + r')\s*='

    if full_document:
        # Remove all tags before re-highlighting
        for tag in text.tag_names():
            text.tag_remove(tag, "1.0", tk.END)
        region_start = "1.0"
        region_end = tk.END
        content = text.get(region_start, region_end)
    elif region_start is None or region_end is None or content is None:
        line = text.index("insert").split('.')[0]
        region_start = f"{line}.0"
        region_end = f"{line}.end"
        content = text.get(region_start, region_end)
        
    if language == "plaintext":
        return

    comment_spans = []
    string_spans = []
    preproc_spans = []
    
    def is_in_comment(idx):
        return any(s <= idx < e for s, e in comment_spans)
    
    def is_in_string_or_comment(idx):
        return any(s <= idx < e for s, e in comment_spans + string_spans)
    
    def is_in_preproc(idx):
        return any(s <= idx < e for s, e in preproc_spans)
    
    # --- Builtins ---
    if language == "python":
        builtins = LANGUAGE_FUNCS.get(language, set())
        if builtins:
            for match in re.finditer(r"\b(" + "|".join(map(re.escape, builtins)) + r")\b", content):
                if not is_in_string_or_comment(match.start()):
                    text.tag_add("builtin", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")

    # --- Comments ---
    if language == "python":
        if full_document:
            pattern = r'#.*|("""|\'\'\')[\s\S]*?\1'
        else:
            pattern = r'#.*'
        for match in re.finditer(pattern, content):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
    elif language == "javascript":
        for match in re.finditer(r'//.*$', content, re.MULTILINE):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        for match in re.finditer(r'/\*[\s\S]*?\*/', content):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
    elif language == "html":
        for match in re.finditer(r'<!--.*?-->', content, re.DOTALL):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
    elif language == "cpp":
        for match in re.finditer(r'//.*', content):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        for match in re.finditer(r'/\*.*?\*/', content, re.DOTALL):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        
    # --- Strings ---    
    for match in re.finditer(r'"(?:[^"\\]|\\.)*"', content):
        s, e = match.start(), match.end()
        if not is_in_comment(s) and not is_in_preproc(s):
            string_spans.append((s, e))
            text.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
            string_content = content[s:e]
            for esc_match in re.finditer(r'\\(["\'ntr0b\\\\]|x[0-9A-Fa-f]{2}|[0-7]{1,3})', string_content):
                esc_s = s + esc_match.start()
                esc_e = s + esc_match.end()
                text.tag_add("escape", f"{region_start}+{esc_s}c", f"{region_start}+{esc_e}c")
    
    for match in re.finditer(r"'(?:[^'\\]|\\.)'", content):
        s, e = match.start(), match.end()
        if not is_in_comment(s) and not is_in_preproc(s):
            text.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
            char_content = content[s:e]
            for esc_match in re.finditer(r'\\(["\'ntr0b\\\\]|x[0-9A-Fa-f]{2}|[0-7]{1,3})', char_content):
                esc_s = s + esc_match.start()
                esc_e = s + esc_match.end()
                text.tag_add("escape", f"{region_start}+{esc_s}c", f"{region_start}+{esc_e}c")
    
    # --- Operators ---       
    if language in ("cpp", "python", "javascript"):
        operator_pattern = r'(<<=|>>=|->\*|->|&&|\|\||\+\+|\-\-|<=|>=|==|<<|>>|!=|\.\*|\+=|-=|\*=|/=|%=|\^=|\|=|&=|::|:|,|\?|\.|~|\+|\-|\*|/|%|<|>|\^|\|)'
        for match in re.finditer(operator_pattern, content):
            s, e = match.start(), match.end()
            if not any(is_in_string_or_comment(i) for i in range(s, e)):
                text.tag_add("operator", f"{region_start}+{s}c", f"{region_start}+{e}c")
            
    # --- Semicolons (C++, JavaScript) ---
    for match in re.finditer(r';', content):
        s, e = match.start(), match.end()
        if not is_in_string_or_comment(s):
            text.tag_add("semicolon", f"{region_start}+{s}c", f"{region_start}+{e}c")

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
                text.tag_add("preprocessor", f"{region_start}+{directive_start}c", f"{region_start}+{directive_end}c")
                rest_start = directive_end
                rest_end = e
                if rest_start < rest_end:
                    text.tag_add("preprocessor_rest", f"{region_start}+{rest_start}c", f"{region_start}+{rest_end}c")
                # Record the whole preprocessor line as a span
                preproc_spans.append((s, e))

    # --- Templates (C++) ---
    if language == "cpp":
        # Match identifiers followed by '<' (but not operators like << or <=)
        id_pattern = re.compile(r'\b([A-Za-z_][A-Za-z0-9_:]*)\s*<(?![<=])')
        for id_match in id_pattern.finditer(content):
            identifier = id_match.group(1)
            if identifier in keywords or identifier in funcs:
                continue  # Skip keywords/functions
            open_angle = id_match.end() - 1
            if is_in_string_or_comment(open_angle):
                continue
            # Limit search to 200 characters to avoid runaway highlighting
            max_search = min(len(content), open_angle + 200)
            depth = 0
            for i in range(open_angle, max_search):
                if content[i] == '<' and not is_in_string_or_comment(i):
                    depth += 1
                elif content[i] == '>' and not is_in_string_or_comment(i):
                    depth -= 1
                    if depth == 0:
                        text.tag_add("template", f"{region_start}+{open_angle}c", f"{region_start}+{i+1}c")
                        break

    # --- Pointers/References (C++) ---
    if language == "cpp":
        for match in re.finditer(r'\b([A-Za-z_][A-Za-z0-9_:]*)\s*(\*+|&)(?=\s*\w)', content):
            ptr_start, ptr_end = match.start(2), match.end(2)
            if not is_in_string_or_comment(ptr_start):
                text.tag_add("pointer", f"{region_start}+{ptr_start}c", f"{region_start}+{ptr_end}c")
                
    # --- Members ---
    for match in re.finditer(r'\.(\w+)\b(?!\s*\()', content):
        member_start = match.start(1)
        member_end = match.end(1)
        if not is_in_string_or_comment(member_start):
            text.tag_add("member", f"{region_start}+{member_start}c", f"{region_start}+{member_end}c")


    # --- Dunder Methods ---
    for match in re.finditer(r'\b(__\w+__)\b', content):
        s, e = match.start(), match.end()
        text.tag_add("dunder", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Integers ---
    for match in re.finditer(r'\b\d+\b', content):
        s, e = match.start(), match.end()
        if not is_in_string_or_comment(s):
            text.tag_add("integer", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- f-strings (Python, C# for $"{}") ---
    if language == "python" or language == "cs":
        for f_match in re.finditer(r'(?P<prefix>[fFrR|\$]{1,2})(?P<quote>["\'])(?P<body>.*?)(?P=quote)', content, re.DOTALL):
            if is_in_string_or_comment(f_match.start()):
                continue
            prefix_start = f_match.start('prefix')
            quote_end = f_match.end('quote')
            body_start = f_match.start('body')
            body_end = f_match.end('body')
            string_spans.append((prefix_start, quote_end))
            text.tag_add("string", f"{region_start}+{prefix_start}c", f"{region_start}+{quote_end}c")
            text.tag_add("prefix", f"{region_start}+{prefix_start}c", f"{region_start}+{f_match.end('prefix')}c")
            body = f_match.group('body')
            current_pos = body_start
            for part in re.finditer(r'(.*?)(\{.*?\}|$)', body):
                literal = part.group(1)
                expr = part.group(2)
                if literal:
                    lit_start = current_pos
                    lit_end = lit_start + len(literal)
                    string_spans.append((lit_start, lit_end))
                    text.tag_add("string", f"{region_start}+{lit_start}c", f"{region_start}+{lit_end}c")
                    current_pos = lit_end
                if expr and expr.startswith('{'):
                    expr_start = current_pos
                    expr_end = current_pos + len(expr)
                    current_pos = expr_end
                    text.tag_remove("string", f"{region_start}+{expr_start}c", f"{region_start}+{expr_end}c")
                    inner_text = expr[1:-1]
                    inner_start = expr_start + 1
                    for func_match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', inner_text):
                        f_start = inner_start + func_match.start(1)
                        f_end = inner_start + func_match.end(1)
                        text.tag_add("funccall", f"{region_start}+{f_start}c", f"{region_start}+{f_end}c")
                    text.tag_add("punctuation", f"{region_start}+{expr_start}c", f"{region_start}+{expr_start+1}c")
                    text.tag_add("punctuation", f"{region_start}+{expr_end-1}c", f"{region_start}+{expr_end}c")
                    for var_match in re.finditer(r'\b([a-zA-Z_]\w*)\b', inner_text):
                        v_start = inner_start + var_match.start(1)
                        v_end = inner_start + var_match.end(1)
                        if not any(text.tag_names(f"{region_start}+{v_start}c")):
                            text.tag_add("variable", f"{region_start}+{v_start}c", f"{region_start}+{v_end}c")
                    for num_match in re.finditer(r'\b\d+\b', inner_text):
                        n_start = inner_start + num_match.start()
                        n_end = inner_start + num_match.end()
                        text.tag_add("number", f"{region_start}+{n_start}c", f"{region_start}+{n_end}c")
                    for dunder_match in re.finditer(r'\b(__\w+__)\b', inner_text):
                        d_start = inner_start + dunder_match.start()
                        d_end = inner_start + dunder_match.end()
                        text.tag_add("dunder", f"{region_start}+{d_start}c", f"{region_start}+{d_end}c")

    # --- Keywords, Functions, Function Calls, Variables ---
    if keywords:
        for match in re.finditer(r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", content):
            if not is_in_string_or_comment(match.start()):
                text.tag_add("keyword", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    if funcs:
        for match in re.finditer(r"\b(" + "|".join(map(re.escape, funcs)) + r")\b", content):
            if not is_in_string_or_comment(match.start()):
                text.tag_add("function", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', content):
        if not is_in_string_or_comment(match.start(1)):
            text.tag_add("funccall", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\b', content):
        if is_in_string_or_comment(match.start()):
            continue
        pos = f"{region_start}+{match.start()}c"
        if not any(text.tag_names(pos)):
            text.tag_add("variable", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")

    # --- HTML tags/attributes ---
    if language == "html":
        for match in re.finditer(r'<(\/?\w+)', content):
            text.tag_add("html_tag", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
        for match in re.finditer(html_attr_pattern, content):
            text.tag_add("html_attr", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
    if language == "html":
        for match in re.finditer(r'=\s*(".*?"|\'.*?\')', content):
            s, e = match.start(1), match.end(1)
            text.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")

    # --- Constants (ALLCAPS) ---
    if language in ['python', 'javascript', 'cpp']:
        for match in re.finditer(r'\b([A-Z][A-Z0-9_]*[A-Z][A-Z0-9_]*)\b', content):
            if not is_in_string_or_comment(match.start()):
                text.tag_add("constant", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")

themes = {
    'light': {
        'bg': '#ffffff', 'fg': '#000000',
        'keyword': '#0000ff', 'string': "#bf6900", 'comment': '#008000',
        'function': '#800080', 'funccall': '#00008b', 'integer': '#ffa500', 'member': '#7a1c15',
        'prefix': '#006400', 'line_numbers': '#f0f0f0', 'cursor': '#000000', 'type': "#0e3c8a",
        'variable': '#000000', 'builtin': "#003a78", 'dunder': '#4F4F4F', 'pointer': "#2c3bc5",
        'escape': '#404040', 'semicolon': "#4b4b4b", 'preprocessor': "#681968", 'preprocessor_rest': "#343434",
        'html_tag': "#68177B", 'html_attr': "#074a7c", 'constant': "#d86919", 'template': "#083e3f", 'operator': "#237471",
    },
    'dark': {
        'bg': '#1e1e1e', 'fg': '#d4d4d4',
        'keyword': '#569cd6', 'string': '#ce9178', 'comment': '#6a9955',
        'function': '#c586c0', 'funccall': '#4ec9b0', 'integer': '#b5cea8', 'member': '#bd4840',
        'prefix': '#9cdcfe', 'line_numbers': '#2d2d2d', 'cursor': '#d4d4d4', 'type': "#6316cf",
        'variable': '#ffffff', 'builtin': "#60abfc", 'dunder': '#b0b0b0', 'pointer': "#4282e1",
        'escape': "#7a7a7a", 'semicolon': "#a0a0a0", 'preprocessor': "#843E84", 'preprocessor_rest': "#636363",
        'html_tag': "#9625af", 'html_attr': "#0c79cd", 'constant': "#fc822b", 'template': "#2e7d71", 'operator': "#33c7c2",
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
        highlight_full_document()
    except tk.TclError:
        pass

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

font_size = 12
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

line_numbers.pack(side=tk.LEFT, fill=tk.Y)
text = scrolledtext.ScrolledText(frame, font=font, undo=True)
text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
text.bind("<Return>", auto_indent)
text.bind("}", handle_closing_brace)

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

def sync_scroll(event):
    line_numbers.yview_moveto(text.yview()[0])
    line_numbers.config(yscrollcommand=lambda *args: None)
    
def on_scroll(event):
    sync_scroll(event)
    update_line_numbers()
text.bind("<MouseWheel>", on_scroll)


text.bind("<Button-4>", on_scroll)
text.bind("<Button-5>", on_scroll)

current_theme = 'light'
theme_var = tk.StringVar(value=current_theme)
def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[theme_name]
    text.config(bg=theme['bg'], fg=theme['fg'], insertbackground=theme['cursor'])
    line_numbers.config(bg=theme['line_numbers'], fg=theme['fg'])

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
    find_win.title("Find")
    tk.Label(find_win, text="Find:").pack(side=tk.LEFT)
    entry = tk.Entry(find_win)
    entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tk.Button(find_win, text="Find All", command=do_find).pack(side=tk.LEFT)
    entry.focus_set()


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
debounce_delay = 100
def on_key_release(event=None):
    global highlight_job
    if highlight_job is not None:
        root.after_cancel(highlight_job)
    highlight_job = root.after(debounce_delay, highlight_line)
    update_line_numbers()

text.unbind("<KeyRelease>")
text.bind('<KeyRelease>', on_key_release)
text.bind('<Configure>', update_line_numbers)
text.bind("<<Paste>>", lambda e: (root.after(10, highlight_full_document)))
text.bind('<Return>', auto_indent)
text.bind('<BackSpace>', update_line_numbers)
text.bind("<Control-o>", open_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-z>", undo_action)
text.bind("<Control-y>", redo_action)
text.bind("<Control-f>", find_text)
text.bind("<Control-n>", new_file)
root.bind("<Control-minus>", zoom_out)
root.bind("<Control-underscore>", zoom_out)
root.bind("<Control-equal>", zoom_in)
root.bind("<Control-plus>", zoom_in)

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

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom In", command=zoom_in, accelerator="Ctrl++")
view_menu.add_command(label="Zoom Out", command=zoom_out, accelerator="Ctrl+-")

language_var = tk.StringVar(value='plaintext')
language_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Language", menu=language_menu)
def highlight_language_change():
    print(f"Highlighting as: {language_var.get()}")
    root.after(10, highlight_full_document)

language_menu.add_radiobutton(label="Plain Text", variable=language_var, value='plaintext', command=highlight_language_change)
language_menu.add_radiobutton(label="Python", variable=language_var, value='python', command=highlight_language_change)
language_menu.add_radiobutton(label="JavaScript", variable=language_var, value='javascript', command=highlight_language_change)
language_menu.add_radiobutton(label="HTML", variable=language_var, value='html', command=highlight_language_change)
language_menu.add_radiobutton(label="C++", variable=language_var, value='cpp', command=highlight_language_change)

def save_session():
    config_dir = os.path.expanduser('~/.slashcode')
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, 'session.json')
    session = {
        'file': current_file if os.path.exists(current_file) else "",
        'theme': current_theme,
        'language': language_var.get()
    }
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
if session.get('file'):
    try:
        with open(session['file'], 'r', encoding='utf-8') as f:
            text.delete(1.0, tk.END)
            text.insert(tk.END, f.read())
            root.title(f"Slash Code - {os.path.basename(session['file'])}")
            current_file = session['file']
    except Exception as e:
        print(f"Error loading file: {e}")

if session.get('theme'):
    set_theme(session['theme'])
else:
    set_theme('light')
if session.get('language'):
    language_var.set(session['language'])
highlight_full_document()

root.mainloop()
