# lab5
static code analysis
# Lab 5: Static Code Analysis

## Known Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|-------------|
| Mutable default argument | Bug | 6 | `logs=[]` shared across function calls | Change to `None` and initialize in function |
| Bare except clause | Security | 17 | `except:` catches all exceptions | Replace with specific exception types |
| eval() usage | Security | 48 | `eval()` can execute arbitrary code | Remove eval and use safe alternatives |
| Unsafe file handling | Bug | 23, 29 | Files not properly closed on errors | Use `with` statements for automatic closing |
| No input validation | Quality | 40 | Wrong types accepted without checking | Add type checks and validation |
| Potential KeyError | Bug | 20 | `getQty()` crashes on missing items | Use `.get()` method with default |
| Poor variable names | Style | 35, 41 | Single-letter variables like `i` | Use descriptive names like `item_name` |
| Missing docstrings | Documentation | All | No function documentation | Add comprehensive docstrings |
| Inconsistent logging | Style | 8 | String concatenation in logging | Use proper logging formatting |
| Mixed quotes | Style | Various | Inconsistent quote usage | Standardize on single or double quotes |

## Reflection Questions & Answers

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest to fix:**
- File handling: Changing to `with` statements was straightforward
- Variable naming: Simple find/replace for better names
- Removing eval: Just deleting the dangerous line
- Adding docstrings: Mechanical but valuable improvement

**Hardest to fix:**
- Mutable default argument: Required understanding Python's evaluation timing
- Input validation: Needed careful type checking without breaking functionality
- Exception handling: Identifying specific exception types that could occur

### 2. Did the static analysis tools report any false positives? If so, describe one example.

**Minor false positives:**
- Pylint sometimes flags global variables as problematic even when they're appropriate for the module's purpose
- Bandit warned about JSON loading, but for this educational context with trusted data, it's acceptable
- Some line length warnings were more about style preference than actual code quality issues

### 3. How would you integrate static analysis tools into your actual software development workflow?

**Local Development:**
- Pre-commit hooks to run basic checks before each commit
- IDE integration for real-time feedback
- Makefile with `make lint` command for all checks

**CI/CD Pipeline:**
- GitHub Actions workflow that runs on every pull request
- Fail builds on security issues (Bandit) and critical errors
- Quality gates with minimum Pylint score requirements
- Automated reporting in PR comments

**Team Standards:**
- Document which rules are enforced vs. warnings
- Regular tool updates and configuration reviews
- Code review checklist including static analysis results

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

**Security Improvements:**
- Removed dangerous `eval()` function
- Proper exception handling instead of bare except
- Safe file operations with `with` statements

**Robustness Improvements:**
- Input validation prevents invalid data
- Proper error handling for file operations
- No more KeyError crashes with `.get()` method
- Type hints for better code understanding

**Readability Improvements:**
- Descriptive variable names
- Comprehensive docstrings
- Consistent code style
- Proper logging instead of print statements

**Maintainability:**
- Clear function purposes and parameters
- Better separation of concerns
- Easier to extend and modify
