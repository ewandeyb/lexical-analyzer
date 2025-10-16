### Grmmar

| Category               | Token Type          | Lexeme / Pattern                  |
| ---------------------- | ------------------- | --------------------------------- |
| Program Delimiters     | PROG_START        | IOL                             |
|                        | PROG_END          | LOI                             |
| Data Types             | TYPE_INT          | INT                             |
|                        | TYPE_STR          | STR                             |
| KEYWORD                | KEY_ASSIGN        | INTO                            |
|                        | KEY_IS            | IS                              |
|                        | KEY_INPUT         | BEG                             |
|                        | KEY_OUTPUT        | PRINT                           |
| Operators              | OP_ADD            | ADD                             |
|                        | OP_SUB            | SUB                             |
|                        | OP_MULT           | MULT                            |
|                        | OP_DIV            | DIV                             |
|                        | OP_MOD            | MOD                             |
| Built-in Commands      | CMD_NEWLINE       | NEWLN                           |
| Literals               | INT_LIT           | A sequence of digits (e.g., 123) |
| Variables              | IDENTIFIER        | Starts with a letter (e.g., num) |
| Special                | EOF               | (End of File)                     |


EBNF

- program    -> PROG_START body PROG_END EOF
- body       -> { statement }

- statement  -> declaration
			 | assignment
			 | io_statement
			 | newline_command

- declaration -> TYPE_INT IDENTIFIER [ KEY_IS INT_LIT ]
			  | TYPE_STR IDENTIFIER [ KEY_IS STRING_LIT ]

- assignment -> IDENTIFIER KEY_ASSIGN expression

- io_statement -> KEY_INPUT IDENTIFIER
			  | KEY_OUTPUT expression

- newline_command -> CMD_NEWLINE

- expression -> term { (OP_ADD | OP_SUB) term }

- term      -> factor { (OP_MULT | OP_DIV | OP_MOD) factor }

- factor    -> INT_LIT
			| IDENTIFIER
			| '(' expression ')'