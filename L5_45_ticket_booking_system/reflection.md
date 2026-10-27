# Reflection – Static Code Analysis

### 1. What did you learn from using static code analysis tools?

I learned that static code analysis tools can identify potential bugs, security vulnerabilities, and coding style issues without executing the program. Pylint helped identify code quality issues, Bandit detected potential security risks, and Flake8 highlighted formatting and style violations.

### 2. Which tool was the most useful, and why?

Bandit was particularly useful because it helped identify security concerns such as the use of `eval()` and the need to avoid exposing hard-coded secrets. Pylint was also useful for improving code structure, naming conventions, exception handling, and maintainability.

### 3. What challenges did you face while fixing the issues?

One challenge was fixing security and code quality issues without breaking the ticket booking system's functionality. I replaced unsafe expression evaluation with validated numeric discount input, improved file handling, removed unused variables and imports, and corrected function naming and exception handling. I then tested the program and reran the analysis tools.

### 4. How will you use static code analysis in future projects?

I will run static analysis tools regularly during development, preferably before committing code. Using Pylint, Bandit, and Flake8 together can help me maintain readable code, identify security risks early, and reduce potential defects before deployment.
