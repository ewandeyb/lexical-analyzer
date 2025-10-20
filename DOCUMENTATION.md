# IOL Compiler Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [System Architecture](#system-architecture)
4. [Implementation Details](#implementation-details)
   - [Lexical Analyzer](#lexical-analyzer)
   - [GUI Application](#gui-application)
   - [Panels](#panels)
   - [Widgets](#widgets)
5. [Token Specification](#token-specification)
6. [File Format Specification](#file-format-specification)
7. [User Guide](#user-guide)
8. [API Reference](#api-reference)
9. [Testing](#testing)
10. [Development Setup](#development-setup)
11. [Work Distribution](#work-distribution)
12. [Future Enhancements](#future-enhancements)

---

## Introduction

This documentation provides comprehensive information about the Integer-Oriented Language (IOL) compiler implementation. The current release focuses on the lexical analysis phase of the compilation process, providing a foundation for future development of the full compiler.

### Project Purpose

The IOL Compiler is a simplified custom language compiler designed to process integer-type values and numerical operations. This implementation serves as an educational project demonstrating compiler construction principles, specifically focusing on lexical analysis, tokenization, and language processing fundamentals.

### Current Implementation Status

**Phase:** Lexical Analysis (PE02)
**Version:** 0.1.0
**Language:** Python 3.13+

The current implementation includes:
- Complete lexical analyzer with tokenization
- Graphical user interface (GUI) for code editing and compilation
- Token stream generation and error reporting
- File I/O operations for `.iol` source files

---

## Project Overview

### What is IOL?

Integer-Oriented Language (IOL) is a simplified programming language that supports:
- Integer and string data types
- Arithmetic operations (addition, subtraction, multiplication, division, modulus)
- Variable declarations and assignments
- Input/output operations
- Prefix notation for expressions

### Language Characteristics

- **Case-sensitive:** Keywords and identifiers are case-sensitive
- **Whitespace-delimited:** Tokens are separated by spaces; extra whitespace is ignored
- **File extension:** `.iol` for source code files
- **Compiled output:** `.tkn` for tokenized output files
- **Program structure:** Code must start with `IOL` and end with `LOI`

---

## System Architecture

### High-Level Architecture

```
+-----------------------------------------------+
|         GUI Application (main.py)             |
|  +----------------------------------------+   |
|  |  Menu Bar (File, Compile, Execute)    |   |
|  +----------------------------------------+   |
|  +---------------+  +--------------------+   |
|  | Editor Panel  |  | Output Panel       |   |
|  | (Code Entry)  |  | (Symbol Table)     |   |
|  +---------------+  +--------------------+   |
|  | Console Panel |                           |
|  | (Results)     |                           |
|  +---------------+                           |
+-----------------------------------------------+
                       |
                       v
           +-----------------------+
           |   Lexer (lexer.py)    |
           |  - Tokenization       |
           |  - Error Detection    |
           +-----------------------+
                       |
                       v
           +-----------------------+
           |   Token Stream        |
           |   (.tkn file)         |
           +-----------------------+
```

### Component Hierarchy

```
App (main.py)
|-- AppMenu
|   |-- File Menu (New File, Open File)
|   |-- Compile Menu (Tokenize)
|   +-- Execute Menu (Future: Execute Code)
|-- EditorPanel (panels/editor.py)
|   +-- Text Editor Widget
|-- ConsolePanel (panels/console.py)
|   +-- EditableText Widget
+-- OutputPanel (panels/output.py)
    +-- (Future: Symbol Table Display)

Lexer (lexer.py)
|-- TokenType (Enum)
|-- Token (Dataclass)
+-- Lexer (Class)
```

### Data Flow

1. **Input:** User types or opens `.iol` file in EditorPanel
2. **Processing:** User clicks "Compile > Tokenize"
3. **Lexical Analysis:** Lexer scans and tokenizes the source code
4. **Output Generation:**
   - Token stream written to `.tkn` file
   - Results displayed in ConsolePanel
   - Errors reported with line and column information

---

## Implementation Details

### Lexical Analyzer

**File:** `lexer.py`

The lexical analyzer is the core component responsible for converting source code into a stream of tokens.

#### TokenType Enum

Defines all valid token types in the IOL language:

| Category | Token Types | Description |
|----------|------------|-------------|
| Program Delimiters | `IOL`, `LOI` | Mark program start and end |
| Data Types | `INT`, `STR` | Variable type declarations |
| Keywords | `INTO`, `IS`, `BEG`, `PRINT` | Language keywords |
| Operators | `ADD`, `SUB`, `MULT`, `DIV`, `MOD` | Arithmetic operators |
| Built-in Commands | `NEWLN` | Newline command |
| Literals | `INT_LIT` | Integer literals (sequence of digits) |
| Identifiers | `IDENT` | Variable names |
| Special | `EOF` | End of file marker |
| Error | `ERR_LEX` | Lexical errors |

#### Token Dataclass

The `Token` dataclass stores token information:

```python
@dataclass
class Token:
    name: TokenType        # Token type
    value: str | int | None  # Lexeme value (for literals and identifiers)
    line: int             # Line number
    column: int           # Column number
```

**String Representation:**
```
<TokenType.INT_LIT = 123 [1,5]>
 +--- Type ----+   |  +--position
                   +--- value
```

#### Lexer Class

The `Lexer` class performs tokenization through character-by-character scanning:

**Key Attributes:**
- `stream: TextIO` - Input stream for reading source code
- `current_char: str` - Current character being processed
- `current_line: int` - Current line number (1-indexed)
- `current_column: int` - Current column number (1-indexed)
- `tokens: list[Token]` - List of generated tokens

**Key Methods:**

1. **`__init__(stream: TextIO)`**
   - Initializes the lexer with an input stream
   - Sets up position tracking

2. **`_advance() -> str`** (Private)
   - Reads next character from stream
   - Updates column position
   - Returns the character read

3. **`_make_token(value: str, start_line: int, start_column: int) -> Token`** (Private)
   - Classifies lexeme into appropriate token type
   - Logic:
     1. Check if lexeme is a keyword -> return keyword token
     2. Check if lexeme is numeric -> return `INT_LIT` token
     3. Check if lexeme is alphanumeric -> return `IDENT` token
     4. Otherwise -> return `ERR_LEX` token

4. **`tokenize() -> list[Token]`** (Public)
   - Main tokenization method
   - Process:
     1. Read characters one at a time
     2. Build lexemes until whitespace or EOF
     3. Convert lexemes to tokens
     4. Track line and column positions
     5. Append `EOF` token at end
   - Returns: List of tokens

**Tokenization Algorithm:**

```
1. Initialize empty current_token buffer
2. Track starting position (line, column)
3. Loop:
   a. Read next character
   b. If EOF:
      - Flush current_token if non-empty
      - Append EOF token
      - Break
   c. If whitespace:
      - Flush current_token to token list
      - Update position tracking (handle newlines)
      - Reset buffer
   d. Otherwise:
      - Append character to current_token
4. Return token list
```

**Error Handling:**
- Invalid characters or character sequences are marked as `ERR_LEX`
- Position information preserved for error reporting

---

### GUI Application

**File:** `main.py`

The GUI provides an integrated development environment (IDE) for writing and compiling IOL programs.

#### App Class

Main application window built with tkinter.

**Configuration:**
- Default filename: `program.iol`
- Default window size: 900x560 pixels
- Color scheme: Custom blue-based theme
- Title format: `{filename} | IOL`

**Layout Structure:**
```
+-----------------------------------------------+
|  Menu Bar (File | Compile | Execute)          |
+---------------------------+-------------------+
|  Editor Panel             |  Output Panel     |
|  (Code editing area)      |  (Symbol table    |
|                           |   placeholder)    |
+---------------------------+                   |
|  Console Panel            |                   |
|  (Tokenization results)   |                   |
+---------------------------+-------------------+
```

**Key Methods:**

1. **`__init__()`**
   - Initializes the main window
   - Sets up menu bar and panels
   - Configures window geometry

2. **`update_title(new_title: str)`**
   - Updates window title while maintaining "IOL" suffix
   - Format: `{new_title} | IOL`

3. **`file_new()`**
   - Clears editor content
   - Resets filename to `program.iol`
   - Updates title to "New file"

4. **`file_open()`**
   - Opens file dialog filtered for `.iol` files
   - Loads selected file into editor
   - Updates title with filename

5. **`compile_tokenize()`**
   - Retrieves text from editor
   - Creates Lexer instance with editor content
   - Performs tokenization
   - Writes tokens to `.tkn` file
   - Displays results in console panel

#### AppMenu Class

Menu bar implementation with three main menus:

**File Menu:**
- New File: Clear editor and start fresh
- Open File: Load existing `.iol` file

**Compile Menu:**
- Tokenize: Perform lexical analysis on editor content

**Execute Menu:**
- (Placeholder for future execution functionality)

---

### Panels

#### EditorPanel

**File:** `panels/editor.py`

Provides the code editing interface.

**Features:**
- Multi-line text editing
- Full tkinter Text widget functionality
- Green background theme (`#B7D06B`)

**Implementation:**
```python
class EditorPanel(tk.Frame):
    def __init__(self, parent):
        # Creates a Text widget for code entry
        self.editor = tk.Text(self)
```

#### ConsolePanel

**File:** `panels/console.py`

Displays compilation results and errors.

**Features:**
- Read-only by default (uses `EditableText` widget)
- Black background with white text
- Displays tokenization success/error messages
- Lists error lexemes with position information
- Orange background theme (`#F2A65A`)

**Key Methods:**

1. **`display_tokenization_result(tokens: list[Token])`**
   - Filters tokens for `ERR_LEX` types
   - Displays "Tokenization complete" message
   - If errors exist:
     - Shows "Error lexemes found:" header
     - Lists each error token with position

**Output Format:**
```
Tokenization complete.

Error lexemes found:

<ERR_LEX = fail? [1,1]>
<ERR_LEX = @symbol [3,5]>
```

#### OutputPanel

**File:** `panels/output.py`

Placeholder panel for future functionality.

**Future Purpose:**
- Display symbol table
- Show variable names and types
- Purple background theme (`#7D5AA3`)

**Current State:**
- Empty frame
- Reserved for syntax analysis phase

---

### Widgets

#### EditableText

**File:** `widgets/editable_text.py`

Custom tkinter Text widget that supports context manager editing.

**Purpose:**
Enable temporary editing of normally disabled text widgets.

**Usage:**
```python
# Widget is normally disabled
console = EditableText(parent, state="disabled")

# Temporarily enable for editing
with console as c:
    c.insert("1.0", "Some text")
# Automatically reverts to disabled state
```

**Implementation:**
- Extends `tk.Text`
- Overrides `__enter__` and `__exit__` for context management
- Stores original state and restores after editing

---

## Token Specification

### Token Format

Each token contains four components:
1. **Name:** Token type from `TokenType` enum
2. **Value:** Lexeme value (for literals and identifiers only)
3. **Line:** Line number where token appears (1-indexed)
4. **Column:** Starting column of token (1-indexed)

### Token Categories

#### 1. Program Delimiters

| Token | Lexeme | Description |
|-------|--------|-------------|
| `IOL` | `IOL` | Program start marker (must be first token) |
| `LOI` | `LOI` | Program end marker (must be last token before EOF) |

#### 2. Data Types

| Token | Lexeme | Description |
|-------|--------|-------------|
| `INT` | `INT` | Integer type declaration |
| `STR` | `STR` | String type declaration |

#### 3. Keywords

| Token | Lexeme | Description |
|-------|--------|-------------|
| `INTO` | `INTO` | Assignment operation |
| `IS` | `IS` | Initialization or assignment operator |
| `BEG` | `BEG` | Input operation |
| `PRINT` | `PRINT` | Output operation |

#### 4. Operators

| Token | Lexeme | Operation | Prefix Notation |
|-------|--------|-----------|-----------------|
| `ADD` | `ADD` | Addition | `ADD expr1 expr2` |
| `SUB` | `SUB` | Subtraction | `SUB expr1 expr2` |
| `MULT` | `MULT` | Multiplication | `MULT expr1 expr2` |
| `DIV` | `DIV` | Division | `DIV expr1 expr2` |
| `MOD` | `MOD` | Modulus | `MOD expr1 expr2` |

#### 5. Built-in Commands

| Token | Lexeme | Description |
|-------|--------|-------------|
| `NEWLN` | `NEWLN` | Inserts newline in output |

#### 6. Literals

| Token | Pattern | Example | Description |
|-------|---------|---------|-------------|
| `INT_LIT` | `digit { digit }` | `123`, `0`, `9876` | Integer literal |

**Note:** String literals are not supported; string values come from user input only.

#### 7. Identifiers

| Token | Pattern | Example | Description |
|-------|---------|---------|-------------|
| `IDENT` | `letter { letter \| digit }` | `num`, `x1`, `result` | Variable names |

**Rules:**
- Must start with a letter (a-z, A-Z)
- Can contain letters and digits
- Case-sensitive

#### 8. Special Tokens

| Token | Description |
|-------|-------------|
| `EOF` | End of file marker (automatically added) |
| `ERR_LEX` | Lexical error (unknown/invalid token) |

### Tokenization Rules

1. **Whitespace:** Acts as token delimiter; multiple spaces are equivalent to one
2. **Case Sensitivity:** `PRINT` ` `print` ` `Print`
3. **Keywords vs Identifiers:** Keywords are reserved and cannot be used as identifiers
4. **Error Detection:** Any character sequence that doesn't match a valid pattern is `ERR_LEX`

### Example Tokenization

**Source Code:**
```
IOL
INT num IS 25
PRINT num
LOI
```

**Token Stream:**
```
<IOL [1,1]>
<INT [2,1]>
<IDENT = num [2,5]>
<IS [2,9]>
<INT_LIT = 25 [2,12]>
<PRINT [3,1]>
<IDENT = num [3,7]>
<LOI [4,1]>
<EOF [4,4]>
```

---

## File Format Specification

### Source Files (.iol)

**Extension:** `.iol`
**Format:** Plain text
**Encoding:** UTF-8 (default)

**Structure:**
```
IOL
    [statements]
LOI
```

**Requirements:**
- Must start with `IOL` keyword
- Must end with `LOI` keyword
- Before `IOL`: only whitespace or start of file
- After `LOI`: only whitespace or end of file
- Between `IOL` and `LOI`: valid IOL statements

**Example:**
```
IOL
INT x IS 10
INT y IS 20
INTO result IS ADD x y
PRINT result
LOI
```

### Token Files (.tkn)

**Extension:** `.tkn`
**Format:** Plain text
**Encoding:** UTF-8 (default)

**Content:** One token per line in string representation format

**Format:**
```
<TokenType [line,column]>
<TokenType = value [line,column]>
```

**Example:**
```
<IOL [1,1]>
<INT [2,1]>
<IDENT = x [2,5]>
<IS [2,7]>
<INT_LIT = 10 [2,10]>
<EOF [6,1]>
```

**Generation:**
- Automatically created during compilation
- Named after source file: `program.iol` -> `program.tkn`
- Overwrites existing `.tkn` file with same name

---

## User Guide

### Installation and Setup

1. **Clone Repository:**
   ```bash
   git clone <repository-url>
   cd lexical-analyzer
   ```

2. **Install Dependencies:**
   ```bash
   uv sync
   uv run pre-commit install
   ```

3. **Run Application:**
   ```bash
   uv run python main.py
   ```

### Using the IDE

#### Starting a New Program

1. Launch the application
2. Click **File -> New File** (or start typing in empty editor)
3. Write your IOL code in the editor panel
4. Code must start with `IOL` and end with `LOI`

#### Opening an Existing Program

1. Click **File -> Open File**
2. Navigate to your `.iol` file
3. Select and open
4. File content loads into editor
5. Window title updates with filename

#### Compiling Code

1. Ensure code is in editor (either typed or opened)
2. Click **Compile -> Tokenize**
3. Process occurs:
   - Lexer scans the code
   - Generates token stream
   - Creates `.tkn` file
   - Displays results in console

#### Understanding Output

**Success:**
```
Tokenization complete.
```

**With Errors:**
```
Tokenization complete.

Error lexemes found:

<ERR_LEX = fail? [1,1]>
<ERR_LEX = @symbol [3,5]>
```

Error format: `<ERR_LEX = {lexeme} [{line},{column}]>`

#### Example Workflow

**Step 1:** Write code in editor
```
IOL
INT x IS 5
PRINT x
LOI
```

**Step 2:** Click "Compile -> Tokenize"

**Step 3:** Check console output
```
Tokenization complete.
```

**Step 4:** View generated `program.tkn` file
```
<IOL [1,1]>
<INT [2,1]>
<IDENT = x [2,5]>
<IS [2,7]>
<INT_LIT = 5 [2,10]>
<PRINT [3,1]>
<IDENT = x [3,7]>
<LOI [4,1]>
<EOF [4,4]>
```

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ERR_LEX` tokens | Invalid characters in code | Check for symbols not in language spec |
| Empty console | No compilation performed | Click "Compile -> Tokenize" |
| File won't open | Wrong extension | Ensure file is `.iol` format |
| Missing tokens | Forgot delimiters | Ensure code starts with `IOL` and ends with `LOI` |

---

## API Reference

### lexer.py

#### TokenType (Enum)

```python
class TokenType(Enum):
    IOL = auto()
    LOI = auto()
    INT = auto()
    STR = auto()
    INTO = auto()
    IS = auto()
    BEG = auto()
    PRINT = auto()
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    MOD = auto()
    NEWLN = auto()
    INT_LIT = auto()
    IDENT = auto()
    EOF = auto()
    ERR_LEX = auto()
```

#### Token (Dataclass)

```python
@dataclass
class Token:
    name: TokenType
    value: str | int | None
    line: int
    column: int

    def __str__(self) -> str:
        """Returns formatted token string representation"""
```

#### Lexer (Class)

```python
class Lexer:
    KEYWORDS: dict[str, TokenType]  # Keyword mapping

    def __init__(self, stream: TextIO) -> None:
        """
        Initialize lexer with input stream.

        Args:
            stream: Text stream containing source code
        """

    def tokenize(self) -> list[Token]:
        """
        Tokenize the entire input stream.

        Returns:
            List of tokens including EOF marker

        Note:
            Invalidates the stream after completion
        """
```

### main.py

#### App (Class)

```python
class App(tk.Tk):
    DEFAULT_FILENAME: str = "program.iol"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize main application window"""

    def update_title(self, new_title: str) -> None:
        """Update window title with IOL suffix"""

    def file_new(self) -> None:
        """Create new file (clear editor)"""

    def file_open(self) -> None:
        """Open existing .iol file"""

    def compile_tokenize(self) -> None:
        """Perform lexical analysis on editor content"""
```

### panels/console.py

#### ConsolePanel (Class)

```python
class ConsolePanel(tk.Frame):
    def display_tokenization_result(self, tokens: list[Token]) -> None:
        """
        Display tokenization results in console.

        Args:
            tokens: List of tokens from lexer

        Displays:
            - Success message
            - Error tokens if any exist
        """
```

### widgets/editable_text.py

#### EditableText (Class)

```python
class EditableText(tk.Text):
    def __init__(
        self,
        *args,
        state: Literal["normal", "disabled"] = "disabled",
        **kwargs
    ) -> None:
        """
        Text widget with context manager support.

        Args:
            state: Initial state of widget
        """

    def __enter__(self):
        """Enable editing temporarily"""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original state"""
```

---

## Testing

### Test Framework

**Framework:** pytest
**File:** `tests/test_lexer.py`

### Running Tests

```bash
uv run pytest
```

### Test Coverage

Current tests cover:
- Basic tokenization
- Keyword recognition
- Identifier recognition
- Integer literal parsing
- Case sensitivity
- Error detection
- Multi-line input
- Position tracking

### Requirements

- Python 3.13 or higher
- uv package manager
- tkinter (usually included with Python)

### Dependencies

**Runtime:**
- tkinter (GUI framework)
- Python standard library

**Development:**
- pytest (testing framework)
- pre-commit (code quality hooks)

### Project Structure

```
lexical-analyzer/
   main.py                  # Application entry point
   lexer.py                 # Lexical analyzer implementation
   panels/                  # GUI panel components
      __init__.py
      editor.py           # Code editor panel
      console.py          # Console output panel
      output.py           # Symbol table panel (placeholder)
   widgets/                 # Custom widgets
      __init__.py
      editable_text.py    # Context-managed text widget
   tests/                   # Test suite
      __init__.py
      test_lexer.py       # Lexer tests
   pyproject.toml          # Project configuration
   README.md               # Quick start guide
   DOCUMENTATION.md        # This file
   .pre-commit-config.yaml # Code quality configuration
```

---

## Appendix

### Grammar Reference (EBNF)

```ebnf
program    -> IOL body LOI EOF
body       -> { statement }

statement  -> declaration
          | assignment
          | io_statement
          | newline_command

declaration -> INT IDENT [ IS INT_LIT ]
           | STR IDENT

assignment -> INTO IDENT IS expression

io_statement -> BEG IDENT
            | PRINT expression

newline_command -> NEWLN

expression -> term { (ADD | SUB) term }

term       -> factor { (MULT | DIV | MOD) factor }

factor     -> INT_LIT
          | IDENT
```

### Glossary

- **Lexeme:** The actual character sequence in source code (e.g., "PRINT", "123")
- **Token:** The categorized representation of a lexeme
- **Tokenization:** Process of converting source code into tokens
- **Lexical Analysis:** First phase of compilation that performs tokenization
- **IOL:** Integer-Oriented Language
- **IDE:** Integrated Development Environment
- **EOF:** End of File
- **EBNF:** Extended Backus-Naur Form (grammar notation)

---

**Document Version:** 1.0
**Last Updated:** October 2025
**Project Version:** 0.1.0
**License:** Educational Project