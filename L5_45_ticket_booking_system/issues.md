# Static Code Analysis Issues

| Issue | Type | Original Location | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe eval() usage | Security | Line 42 | Evaluating a string as code could execute unintended operations. | Replaced eval() with validated numeric discount input. |
| Hard-coded secret | Security | main() | A secret-like token was stored in the source code and printed. | Removed the hard-coded token and its output. |
| Mutable default argument | Code quality | Line 15 | A default list could retain data across function calls. | Used None and initialized a new list inside the function. |
| Bare exception handler | Code quality | Line 26 | A bare except could hide unexpected errors. | Removed the broad exception handler and checked whether the seat exists. |
| Weak MD5 hash | Security | Line 47 | MD5 is unsuitable when collision resistance is required. | Replaced MD5 with SHA-256. |
| Missing docstrings | Code quality | Multiple lines | Functions lacked descriptions. | Added function docstrings. |
| Missing file encoding | Code quality | Line 55 | File operations did not specify an encoding. | Specified UTF-8 encoding. |
| Unused imports and variables | Code quality | Multiple lines | Unused names reduced code clarity. | Removed unused imports and variables. |
| Naming and formatting issues | Style | Multiple lines | Naming conventions and formatting were inconsistent. | Used snake_case, f-strings, and consistent formatting. |