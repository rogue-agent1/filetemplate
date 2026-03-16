# filetemplate
File template engine with variable substitution and built-in templates.
```bash
python filetemplate.py list
python filetemplate.py gen python -v NAME=myapp DESCRIPTION="My app" -o myapp.py
python filetemplate.py render template.txt -v NAME=project --json vars.json
```
## Zero dependencies. Python 3.6+.
