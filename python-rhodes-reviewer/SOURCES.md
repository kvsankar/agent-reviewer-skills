# Sources and Attribution

## A Note from Brandon Rhodes

> Hey, folks, this is Brandon Rhodes, making a personal comment on this project, since Sankar was kind enough to ask my permission before making it public! While I myself am dismayed at the broad impact of AI on society so far, and have always been skeptical about automated code review (I've always used 'pyflakes' instead of 'flake8' because flake8's clumsy attempts to apply PEP-8 produce so much noise), I see no reason to stand in the way of this experiment. It tries to distill some of the guidelines that I've offered in my talks into a set of rules that can be applied by machine. I can't guess whether Claude Code will really understand when my ideas are useful and when they're not, but it's interesting to see how many pieces of advice worked their way into my talks over so many years.
>
> — Brandon Rhodes (December 2025)

## Primary Sources

All 70 guidelines in this skill are extracted from Brandon Rhodes' public educational materials:

### Conference Presentations (2010-2024)

| Talk | Year | Guidelines |
|------|------|------------|
| The Mighty Dictionary | 2010 | HASH-CLASS |
| Know Thy Database | 2011 | DATA-COMMENT |
| A Python Æsthetic | 2012 | LINE-LENGTH, OP-BEFORE, DOT-START, ARG-PER-LINE, NAME-COMMENT, INDENT-LIMIT |
| Python Design Patterns 1 | 2012 | PYTHON-PATTERNS |
| Flexing SQLAlchemy's Relational Power | 2012 | ORM-KNOW |
| The Naming of Ducks | 2013 | PRECISE-NOUN, USE-VERBS, NO-SYNEC, AVOID-PLURAL, SAFE-DEFAULT |
| Skyfield and 15 Years of Bad APIs | 2013 | EXPLICIT-NAME, NO-MUTSTATE, SHOW-COST, NO-MUTARGS, SCALAR-NUMPY |
| Sine Qua Nons | 2013 | DICT-JOIN, NAMED-TUPLE, NUMPY-VECTOR, EXCEPT-HIER, VENV-SANDBOX, CTYPES-INTRO |
| Copernican Refactoring | 2013 | COPERNICAN |
| The Clean Architecture in Python | 2014 | PURE-TEST, FUNC-SHELL, DATA-FLOW |
| All Your Ducks In A Row | 2014 | LIST-FRONT |
| Moving Targets | 2014 | DJANGO-TXN |
| Hoisting Your I/O | 2015 | HOIST-IO, NO-MOCK |
| Stopping to Sharpen Your Tools | 2015 | TOOL-INVEST |
| Using Python to power Selenium | 2016 | SELENIUM-HIGH |
| The Dictionary Even Mightier | 2017 | DICT-COMP, KEY-SHARE |
| Animating with ASCII | 2017 | TERM-SETTINGS, ANSI-ESC, CANVAS-DATA, PASS-FUNC |
| When Python Practices Go Wrong | 2019 | NO-IMPORT-FX, EXPLICIT-BOOL, NO-CALL, NO-GLOBAL-MUT, COMP-INHERIT, NO-EVAL |
| The Antipodes | 2019 | TOP-DOWN |
| The Classic Design Patterns | 2022 | LANG-PATTERN, GEN-ITER, DJANGO-CMD |
| The History of a Science | 2023 | CHAIN-PARAM, CONFIG-OBJ, CONTROL-CALLER |
| Walking the Line | 2023 | BREAK-TEST, REDUND-OK |
| Forcing unittest to function | 2024 | FUNC-TEST |

### Python Patterns Guide (python-patterns.guide)

12 additional guidelines from Brandon Rhodes' comprehensive pattern guide:

- MODULE-CONST - Use module-level constants
- IMPORT-COMPUTE - Import-time computation for constants
- NO-IMPORT-IO - Never perform I/O at import time
- NO-MUTABLE-GLOBAL - Avoid mutable global objects
- PREBOUND-METHOD - Prebound method pattern
- SENTINEL-OBJ - Sentinel objects for missing values
- DECORATOR-DYNAMIC - Dynamic wrappers for decorator pattern
- NO-SINGLETON - Avoid the Singleton pattern
- NO-BUILDER-ARGS - Avoid Builder for optional arguments
- COMPOSITE-SYM - Composite pattern for symmetric operations
- NO-SCATTERED-IFS - Avoid scattered conditionals
- NO-MULTI-INHERIT - Avoid multiple inheritance

## Reference Links

- **Brandon Rhodes' Website:** https://rhodesmill.org/brandon/
- **Conference Talks:** https://rhodesmill.org/brandon/talks/
- **Python Patterns Guide:** https://python-patterns.guide/
- **GitHub:** https://github.com/brandon-rhodes
- **PyVideo Archive:** https://pyvideo.org/speaker/brandon-rhodes.html

## Astronomy Libraries

- **Skyfield:** https://rhodesmill.org/skyfield/
- **PyEphem:** https://rhodesmill.org/pyephem/

## Attribution and Permission

The guidelines in this skill are summarized from Brandon Rhodes' public conference presentations and educational materials. This skill was released with Brandon Rhodes' permission. See his statement above.

## Contact

- Brandon Rhodes: brandon@rhodesmill.org
- Skill Author: Sankar (kvsankar)
