#!/usr/bin/env python3
"""Test all bot dependencies"""
import sys
import os

# Add ISMAIL_BOT to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ISMAIL_BOT'))

print("=" * 60)
print("ISMAIL-BOT DEPENDENCY CHECK")
print("=" * 60)

imports_ok = True
test_modules = [
    ("protobuf_decoder", "from protobuf_decoder.protobuf_decoder import Parser"),
    ("crypto", "from crypto import encrypt_aes, decrypt_aes"),
    ("helpers", "from helpers import fetch_tokens, get_token"),
    ("config", "from config import Config"),
    ("Pb2", "from Pb2 import DEcwHisPErMsG_pb2"),
    ("requests", "import requests"),
    ("flask", "import flask"),
    ("psutil", "import psutil"),
    ("PyJWT", "import jwt"),
    ("asyncio", "import asyncio"),
    ("protobuf", "import google.protobuf as pb; print(f'  └─ protobuf {pb.__version__}')"),
]

for module_name, import_stmt in test_modules:
    try:
        exec(import_stmt)
        print(f"✓ {module_name:<20} OK")
    except Exception as e:
        print(f"✗ {module_name:<20} FAILED: {str(e)[:60]}")
        imports_ok = False

print("=" * 60)
if imports_ok:
    print("✓ ALL DEPENDENCIES READY - BOT CAN START!")
    sys.exit(0)
else:
    print("✗ Some dependencies missing - see errors above")
    sys.exit(1)
