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
import platform
from tkinter import filedialog, scrolledtext, messagebox, ttk

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

class ToolTip:
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
    },
    'cs': {
    'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const', 'continue',
    'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern', 'false', 'finally',
    'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 'is', 'lock',
    'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params', 'private', 'protected',
    'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string',
    'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort',
    'using', 'virtual', 'void', 'volatile', 'while'
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
    'html': {}, # HTML doesn't have any functions (you'd need to use JavaScript).
    'cs': {
    'Console.WriteLine', 'Console.ReadLine', 'Math.Abs', 'Math.Pow', 'Math.Sqrt', 'ToString', 'Equals', 'GetHashCode', 'GetType', 'Parse'
    }
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
            'str': 'Converts an object to a string.',
            'int': 'Converts an object to an integer',
            'list': 'May be used as an object type specifier or may be used with parentheses to convert an object to a list of iterables.',
            'dict': 'May be used as an object type specifier or may be used with parentheses to convert an object to a dictionary of key-value pairs.',
            'open': 'Opens a file object with the type of TextIOWrapper[_WrappedBuffer] to convert the content of a file to a string for reading and writing. It is most likely you\'ll use the as keyword to genuinely execute an action with the file itself.',
            'input': 'Gets user input and returns the text the user inputted into the stream. This may be used as a confirmation for something important or anything else.',
            'type': 'Checks the type of the object and returns it.',
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
    }
}

def new_file(event=None):
    text.delete(1.0, tk.END)
    update_line_numbers()
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
        update_line_numbers()
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
    bind_tooltips()
    
def mask_comments(content, comment_spans):
    chars = list(content)
    for s, e in comment_spans:
        for i in range(s, e):
            chars[i] = " " 
    return "".join(chars)

def highlight(event=None, full_document=False, region_start=None, region_end=None, content=None):
    """
    If full_document is True, highlights the whole file.
    If False (default), highlights only the current line.
    """
    if hasattr(text, "function_signatures"):
        text.function_signatures.clear()
    language = language_var.get()
    keywords = LANGUAGE_KEYWORDS.get(language, set())
    funcs = LANGUAGE_FUNCS.get(language, set())
    html_attr_pattern = r'\b(' + '|'.join(html_attrs) + r')\s*='

    if full_document:
        for tag in text.tag_names():
            text.tag_remove(tag, "1.0", tk.END)
        region_start = "1.0"
        region_end = tk.END
        content = text.get(region_start, region_end)
    elif region_start is None or region_end is None or content is None:
        for tag in text.tag_names():
            text.tag_remove(tag, "1.0", tk.END)
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
    
    def is_in_string(idx):
        return any(s <= idx < e for s, e in string_spans)

    # --- Comments ---
    if language == "python":
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
                    text.tag_add("comment", f"{region_start}+{comment_start}c", f"{region_start}+{comment_end}c")
            current_pos += len(line) + 1

    elif language in ("javascript", "cpp", "cs"):
        for match in re.finditer(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', content):
            s, e = match.start(), match.end()
            string_spans.append((s, e))

        for match in re.finditer(r'//.*', content):
            s, e = match.start(), match.end()
            if is_in_string(s):
                continue
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        if language in ("cpp", "cs"):
            for match in re.finditer(r'/\*.*?\*/', content, re.DOTALL):
                s, e = match.start(), match.end()
                if is_in_string(s):
                    continue
                comment_spans.append((s, e))
                text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")
        
    elif language == "html":
        for match in re.finditer(r'<!--.*?-->', content, re.DOTALL):
            s, e = match.start(), match.end()
            comment_spans.append((s, e))
            text.tag_add("comment", f"{region_start}+{s}c", f"{region_start}+{e}c")

    masked_content = mask_comments(content, comment_spans)

    # --- Strings ---
    for match in re.finditer(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', masked_content):
        s, e = match.start(), match.end()
        string_spans.append((s, e))
        text.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
        escape_pattern = r'\\(\\|[abfnrtv\'"0-9xuU])'
        for s, e in string_spans:
            string_text = content[s:e]
            for esc in re.finditer(escape_pattern, string_text):
                esc_start = s + esc.start()
                esc_end = s + esc.end()
                text.tag_add("escape", f"{region_start}+{esc_start}c", f"{region_start}+{esc_end}c")

    # --- Operators ---       
    if language in ("cpp", "python", "javascript", "cs"):
        operator_pattern = r'(<<=|>>=|->\*|->|&&|\|\||\+\+|\-\-|<=|>=|==|<<|>>|!=|\.\*|\+=|-=|\*=|/=|%=|\^=|\|=|&=|::|:|\?|\.|~|\+|\-|\*|/|%|<|>|\^|\|)'
        for match in re.finditer(operator_pattern, content):
            s, e = match.start(), match.end()
            if not any(is_in_string_or_comment(i) for i in range(s, e)):
                text.tag_add("operator", f"{region_start}+{s}c", f"{region_start}+{e}c")
                
    # --- Builtins ---
    if language == "python":
        builtins = LANGUAGE_FUNCS.get(language, set())
        if builtins:
            for match in re.finditer(r"\b(" + "|".join(map(re.escape, builtins)) + r")\b", content):
                if not is_in_string_or_comment(match.start()):
                    text.tag_add("builtin", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
            
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
                        text.tag_add("template", f"{region_start}+{open_angle}c", f"{region_start}+{i+1}c")
                        break

    # --- Pointers/References (C++) ---
    if language == "cpp":
        for match in re.finditer(r'\b([A-Za-z_:][\w:<>]*)\s*(\*+|&)(?=\s*\w)', content):
            ptr_start, ptr_end = match.start(2), match.end(2)
            if not is_in_string_or_comment(ptr_start):
                text.tag_add("pointer", f"{region_start}+{ptr_start}c", f"{region_start}+{ptr_end}c")
                
    # --- Members ---
    for match in re.finditer(r'(?<!\d)\.(\w+)\b(?!\s*\()', content):
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
                    for str_match in re.finditer(r"(['\"])(?:\\.|[^\\])*?\1", inner_text):
                        s = inner_start + str_match.start()
                        e = inner_start + str_match.end()
                        text.tag_add("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
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
                    if language in ("cpp", "python", "javascript", "cs"):
                        operator_pattern = r'(<<=|>>=|->\*|->|&&|\|\||\+\+|\-\-|<=|>=|==|<<|>>|!=|\.\*|\+=|-=|\*=|/=|%=|\^=|\|=|&=|::|:|\?|\.|~|\+|\-|\*|/|%|<|>|\^|\|)'
                        for operator_match in re.finditer(operator_pattern, inner_text):
                            o_start = inner_start + operator_match.start()
                            o_end = inner_start + operator_match.end()
                            text.tag_add("operator", f"{region_start}+{o_start}c", f"{region_start}+{o_end}c")

    # --- Keywords, Functions, Class Names, Function Calls, Variables ---
    if keywords:
        for match in re.finditer(r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", content):
            if not is_in_string_or_comment(match.start()):
                tag_start = f"{region_start}+{match.start()}c"
                tag_end = f"{region_start}+{match.end()}c"
                text.tag_add("keyword", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
                text.tag_add(f"kw_{match.group(0)}", tag_start, tag_end)
    if language in ("python", "cs", "cpp", "javascript"):
        for match in re.finditer(r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)', content):
            name_start = match.start(1)
            name_end = match.end(1)
            if not is_in_string_or_comment(name_start):
                text.tag_add("classname", f"{region_start}+{name_start}c", f"{region_start}+{name_end}c")
    if funcs:
        for match in re.finditer(r"\b(" + "|".join(map(re.escape, funcs)) + r")\b", content):
            if not is_in_string_or_comment(match.start()):
                text.tag_add("function", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
                text.tag_add(f"fn_{match.group(0)}", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', content):
        if not is_in_string_or_comment(match.start(1)):
            text.tag_add("funccall", f"{region_start}+{match.start(1)}c", f"{region_start}+{match.end(1)}c")
    for match in re.finditer(r'\b([a-zA-Z_]\w*)\b', content):
        if is_in_string_or_comment(match.start()):
            continue
        pos = f"{region_start}+{match.start()}c"
        if not any(text.tag_names(pos)):
            text.tag_add("variable", f"{region_start}+{match.start()}c", f"{region_start}+{match.end()}c")
    
    # --- Tooltips ---
    if language == "python":
        for match in re.finditer(
        r'\bdef\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(?:->\s*([^:]+?))?:', content
        ):
            func_name = match.group(1)
            params = match.group(2)
            return_type = match.group(3)
            name_start = match.start(1)
            name_end = match.end(1)
            tag_name = f"defsig_{func_name}"
            text.tag_add(tag_name, f"{region_start}+{name_start}c", f"{region_start}+{name_end}c")
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
            if not hasattr(text, "function_signatures"):
                text.function_signatures = {}
            text.function_signatures[func_name] = signature

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
    for s, e in comment_spans:
        text.tag_remove("string", f"{region_start}+{s}c", f"{region_start}+{e}c")
    text.tag_raise("comment")

themes = {
    'light': {
        'bg': '#ffffff', 'fg': '#000000',
        'keyword': '#0000ff', 'string': "#bf6900", 'comment': '#008000',
        'function': '#800080', 'funccall': '#00008b', 'integer': '#ffa500', 'member': '#7a1c15',
        'prefix': '#006400', 'line_numbers': '#f0f0f0', 'cursor': '#000000', 'type': "#0e3c8a",
        'variable': '#000000', 'builtin': "#003a78", 'dunder': '#4F4F4F', 'pointer': "#2c3bc5", 'classname': "#e99235",
        'escape': '#404040', 'semicolon': "#4b4b4b", 'preprocessor': "#681968", 'preprocessor_rest': "#343434",
        'html_tag': "#68177B", 'html_attr': "#074a7c", 'constant': "#d86919", 'template': "#083e3f", 'operator': "#237471",
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
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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

sidebar = tk.Frame(frame, width=200, bg=themes[theme_var.get()]['bg'])
sidebar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(sidebar)
tree.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

scrollbar = tk.Scrollbar(sidebar, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
                    text.insert("1.0", f.read())
                highlight_full_document()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")

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
            with open(path, "r", encoding="utf-8") as f:
                text.delete("1.0", tk.END)
                text.insert("1.0", f.read())
            highlight_full_document()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

tree.bind("<Double-1>", on_tree_double_click)

def open_folder():
    folder = filedialog.askdirectory()
    if folder:
        tree.delete(*tree.get_children())
        root_node = tree.insert("", "end", text=folder, open=True)
        insert_nodes(root_node, folder)
        file_listbox.folder_path = folder

def on_open_node(event):
    node = tree.focus()
    path = get_full_path(node)
    if tree.get_children(node):
        first_child = tree.get_children(node)[0]
        if not tree.get_children(first_child):
            tree.delete(first_child)
            insert_nodes(node, path)

tree.bind("<<TreeviewOpen>>", on_open_node)

open_folder_btn = tk.Button(
    sidebar,
    text="Open Folder",
    command=open_folder,
    bg=themes[theme_var.get()]['bg'],
    fg=themes[theme_var.get()]['fg']
)
open_folder_btn.pack(fill=tk.X, pady=4)

def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[theme_name]
    text.config(bg=theme['bg'], fg=theme['fg'], insertbackground=theme['cursor'])
    line_numbers.config(bg=theme['line_numbers'], fg=theme['fg'])
    file_listbox.config(bg=theme['line_numbers'], fg=theme['fg'], selectbackground=theme['keyword'])
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
    find_win.title("Find")
    tk.Label(find_win, text="Find:").pack(side=tk.LEFT)
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
                print("MSYS2 installed. Please install MinGW via MSYS2 shell: pacman -S mingw-w64-x86_64-gcc")
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
            output_text.insert(tk.END, 
                f"{runner_name} not found!\n"
                f"Please install it first.\n"
                f"Instructions: {install_instructions}\n"
            )
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
                    output = "Compilation Error:\n" + compile_result.stderr

        elif lang == "html":
            import webbrowser
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
                f.write(code)
                f.flush()
                webbrowser.open(f.name)
            output = "Opened in default browser."

        else:
            output = "Language not supported for execution."

    except subprocess.CalledProcessError as e:
        output = f"Process Error ({e.returncode}):\n{e.stderr}"
    except Exception as e:
        output = f"Unexpected Error: {str(e)}"
    finally:
        if 'f' in locals() and hasattr(f, 'name'):
            try:
                os.unlink(f.name)
                if lang in ("cpp", "cs"):
                    os.unlink(exe_file)
            except Exception as e:
                show_error(f"Cleanup failed: {str(e)}")

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
                
text.unbind("<KeyRelease>")
text.bind('<KeyRelease>', on_key_release)
text.bind('<Configure>', update_line_numbers)
text.bind("<<Paste>>", lambda e: (root.after(10, highlight_full_document)))
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
open_folder_btn = file_menu.add_command(label="Open Folder", command=open_folder, accelerator="Ctrl+Shift+D")
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
theme_menu.add_command(label="Dracula", command=lambda: set_theme('dracula'))
theme_menu.add_command(label="Monokai", command=lambda: set_theme('monokai'))
theme_menu.add_command(label="Night Owl", command=lambda: set_theme('night_owl'))
theme_menu.add_command(label="Shades Of Purple", command=lambda: set_theme('shades_of_purple'))

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom In", command=zoom_in, accelerator="Ctrl++")
view_menu.add_command(label="Zoom Out", command=zoom_out, accelerator="Ctrl+-")
view_menu.add_separator()
view_menu.add_command(label="Show Sidebar", command=show_sidebar, accelerator="Ctrl+J")
view_menu.add_command(label="Hide Sidebar", command=hide_sidebar, accelerator="Ctrl+L")

run_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Run File", command=run_code, accelerator="Ctrl+R")

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
language_menu.add_radiobutton(label="C#", variable=language_var, value='cs', command=highlight_language_change)

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
