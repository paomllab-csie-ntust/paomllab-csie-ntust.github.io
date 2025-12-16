#!/usr/bin/env python3
import py_compile
import sys

try:
    py_compile.compile('admin/app.py', doraise=True)
    print("✅ Syntax is correct!")
    sys.exit(0)
except py_compile.PyCompileError as e:
    print(f"❌ Syntax error:")
    print(e)
    sys.exit(1)

