### Grmmar

| Category               | Token Type          | Lexeme / Pattern                  |
| ---------------------- | ------------------- | --------------------------------- |
| Program Delimiters     | IOL                 | IOL                               |
|                        | LOI                 | LOI                               |
| Data Types             | TYPE_INT            | INT                               |
|                        | TYPE_STR            | STR                               |
| KEYWORD                | INTO                | INTO                              |
|                        | IS                  | IS                                |
|                        | BEG                 | BEG                               |
|                        | PRINT               | PRINT                             |
| Operators              | ADD                 | ADD                               |
|                        | SUB                 | SUB                               |
|                        | MULT                | MULT                              |
|                        | DIV                 | DIV                               |
|                        | MOD                 | MOD                               |
| Built-in Commands      | NEWLN               | NEWLN                             |
| Literals               | INT_LIT             | A sequence of digits (e.g., 123)  |
| Variables              | IDENTIFIER          | Starts with a letter (e.g., num)  |
| Special                | EOF                 | (End of File)                     |


EBNF
```
- program    -> IOL body LOI EOF
- body       -> { statement }

- statement  -> declaration
			 | assignment
			 | io_statement
			 | newline_command

- declaration -> TYPE_INT IDENTIFIER [ IS INT_LIT ]
			  | TYPE_STR IDENTIFIER [ IS STRING_LIT ]

- assignment -> IDENTIFIER INTO expression

- io_statement -> BEG IDENTIFIER
			  | PRINT expression

- newline_command -> NEWLN

- expression -> term { (ADD | SUB) term }

- term      -> factor { (MULT | DIV | MOD) factor }

- factor    -> INT_LIT
			| IDENTIFIER
			| '(' expression ')'
```