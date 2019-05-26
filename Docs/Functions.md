# Builtin Function

These are the builtin functions in Shex:

| Function | Args | Explanation | Example | Example Result |
| --- | --- | --- | --- | --- |
| print | Value | Prints the given value | print ('Hello, World!') | Hello, Wolrd |
| import | Path | Imports the file at given path | import ('system.shex') | *Adds functions from that module* |
| read | Path | Reads the given files content, and returns it | read ('MyData.txt') | Text In MyData.txt |
| iseven | Number | Checks if the given number is even. Returns 1 if it is, and 0 if it isn't | iseven (5) | 0 |
| isodd | Number | Checks if the given number is odd. Returns 1 if it is, and 0 if it isn't | isodd (5) | 1 |
| length | Value | Returns the value of fx. a string or list | length ('Hello') | 5 |
| split | String, Factor | Splits the given string into a list by the factor | split ('Hello World', ' ') | ['Hello', 'World'] |
| join | List, Factor | Joins the given list into a string by the given factor | join (['Hello', 'World'], ', ') | Hello, World

<br><br>

These are the functions you can use from the system module:

| Function | Args | Explanation | Example | Example Result |
| --- | --- | --- | --- | --- |
| add | X, Y | Returns X + Y | add (1, 2) | 3 |
| subtract | X, Y | Returns X - Y | subtract (1, 2) | -1 |
| multiply | X, Y | Returns X * Y | multiply (1, 2) | 2 |
| divide | X, Y | Returns X / Y | divide (1, 2) | 0,5 |
| divide | X, Y | Returns X / Y | divide (1, 2) | 0,5 |
| power | X, Y | Returns X ** Y (Uses the power operator: ^) | power (1, 2) | 1 |
| check | X | Returns 1 if X is greater than 0 and 0 if X is less than or equal to 0 | check (4) | 1 |
