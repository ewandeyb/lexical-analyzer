### Grmmar

| Category               | Token Type          | Lexeme / Pattern                  |
| ---------------------- | ------------------- | --------------------------------- |
| Program Delimiters     | IOL                 | IOL                               |
|                        | LOI                 | LOI                               |
| Data Types             | INT                 | INT                               |
|                        | STR                 | STR                               |
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
| Variables              | IDENT               | Starts with a letter (e.g., num)  |
| Special                | EOF                 | (End of File)                     |
| Error                  | ERR_LEX             | Any error                         |


EBNF
```
- program    -> IOL body LOI EOF
- body       -> { statement }

- statement  -> declaration
			 | assignment
			 | io_statement
			 | newline_command

- declaration -> INT IDENT [ IS INT_LIT ]
			  | STR IDENT

- assignment -> IDENT INTO expression

- io_statement -> BEG IDENT
			  | PRINT expression

- newline_command -> NEWLN

- expression -> term { (ADD | SUB) term }

- term      -> factor { (MULT | DIV | MOD) factor }

- factor    -> INT_LIT
			| IDENT
			| '(' expression ')'
```