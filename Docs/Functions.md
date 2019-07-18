# Builtin Function

These are the builtin functions in Shex:

| Function | Args | Explanation | Example | Example Result |
| --- | --- | --- | --- | --- |
| say | Value | Prints the given value | say ('Hello, World!') | Hello, Wolrd |
| imp | Path | Imports the file at given path | imp ('system') | *Adds functions from that module* |
| read | Path | Reads the given files content, and returns it | read ('MyData.txt') | Text In MyData.txt |
| len | Value | Returns the value of fx. a string or list | len ('Hello') | 5 |
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
| power | X, Y | Returns X ** Y (Uses the power operator: ^) | power (1, 2) | 1 |
| check | X | Returns 1 if X is greater than 0 and 0 if X is less than or equal to 0 | check (4) | 1 |

<br<br>

Math

| Function | Args | Explanation | Example | Example Result |
| --- | --- | --- | --- | --- |
| add | X, Y | Returns X + Y | add (1, 2) | 3 |
| subtract | X, Y | Returns X - Y | subtract (1, 2) | -1 |
| multiply | X, Y | Returns X * Y | multiply (1, 2) | 2 |
| divide | X, Y | Returns X / Y | divide (1, 2) | 0,5 |
| power | X, Y | Returns X ** Y (Uses the power operator: ^) | power (1, 2) | 1 |
