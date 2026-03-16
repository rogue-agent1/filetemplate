#!/usr/bin/env python3
"""filetemplate - Simple file template engine with variable substitution."""
import argparse, os, sys, re, json, time

BUILTIN_VARS = {
    'DATE': time.strftime('%Y-%m-%d'),
    'DATETIME': time.strftime('%Y-%m-%d %H:%M:%S'),
    'YEAR': time.strftime('%Y'),
    'USER': os.environ.get('USER', 'user'),
    'HOME': os.path.expanduser('~'),
    'CWD': os.getcwd(),
    'HOSTNAME': os.uname().nodename,
}

TEMPLATES = {
    'python': '#!/usr/bin/env python3\n"""{{NAME}} - {{DESCRIPTION}}"""\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n',
    'bash': '#!/usr/bin/env bash\nset -euo pipefail\n# {{NAME}} - {{DESCRIPTION}}\n# Created: {{DATE}}\n\n',
    'html': '<!DOCTYPE html>\n<html lang="en">\n<head><meta charset="UTF-8"><title>{{NAME}}</title></head>\n<body>\n  <h1>{{NAME}}</h1>\n</body>\n</html>\n',
    'makefile': '# {{NAME}}\n.PHONY: all clean test\n\nall:\n\t@echo "Building {{NAME}}"\n\nclean:\n\trm -rf build/\n\ntest:\n\t@echo "Testing {{NAME}}"\n',
    'dockerfile': 'FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nRUN pip install --no-cache-dir -r requirements.txt\nCMD ["python", "{{NAME}}.py"]\n',
    'readme': '# {{NAME}}\n\n{{DESCRIPTION}}\n\n## Usage\n\n```bash\n# TODO\n```\n\n## License\n\nMIT © {{YEAR}} {{USER}}\n',
}

def render(template, variables):
    def replacer(m):
        key = m.group(1)
        return variables.get(key, m.group(0))
    return re.sub(r'\{\{(\w+)\}\}', replacer, template)

def main():
    p = argparse.ArgumentParser(description='File template engine')
    sub = p.add_subparsers(dest='cmd')
    
    gen = sub.add_parser('gen', help='Generate from built-in template')
    gen.add_argument('template', choices=list(TEMPLATES.keys()))
    gen.add_argument('-o', '--output', help='Output file')
    gen.add_argument('-v', '--var', nargs='*', help='KEY=VALUE pairs')
    
    rnd = sub.add_parser('render', help='Render custom template file')
    rnd.add_argument('file', help='Template file')
    rnd.add_argument('-o', '--output', help='Output file')
    rnd.add_argument('-v', '--var', nargs='*')
    rnd.add_argument('--json', help='JSON file with variables')
    
    ls = sub.add_parser('list', help='List built-in templates')
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    if args.cmd == 'list':
        for name in TEMPLATES:
            preview = TEMPLATES[name][:60].replace('\n', '\\n')
            print(f"  {name:<15} {preview}...")
        return
    
    variables = dict(BUILTIN_VARS)
    if hasattr(args, 'var') and args.var:
        for kv in args.var:
            k, v = kv.split('=', 1)
            variables[k] = v
    if hasattr(args, 'json') and args.json:
        with open(args.json) as f:
            variables.update(json.load(f))
    
    if args.cmd == 'gen':
        result = render(TEMPLATES[args.template], variables)
    else:
        with open(args.file) as f:
            result = render(f.read(), variables)
    
    if args.output:
        with open(args.output, 'w') as f: f.write(result)
        print(f"Generated: {args.output}")
    else:
        print(result)

if __name__ == '__main__':
    main()
