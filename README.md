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
| Numerical Operators    | OP_ADD            | ADD                             |
|                        | OP_SUB            | SUB                             |
|                        | OP_MULT           | MULT                            |
|                        | OP_DIV            | DIV                             |
|                        | OP_MOD            | MOD                             |
| Built-in Commands      | CMD_NEWLINE       | NEWLN                           |
| Literals               | INTEGER_LITERAL   | A sequence of digits (e.g., 123) |
| Variables              | IDENTIFIER        | Starts with a letter (e.g., num) |
| Special                | EOF               | (End of File)                     |
