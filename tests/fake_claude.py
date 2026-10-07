#!/usr/bin/env python3
"""Stand-in for `claude -p`: wraps FAKE_REVIEW in a result envelope, saves stdin to FAKE_PROMPT_OUT and argv + env flag to FAKE_ARGS_OUT."""
import json
import os
import sys

args = sys.argv[1:]
if os.environ.get("FAKE_FAIL"):
    print("simulated claude failure", file=sys.stderr)
    sys.exit(1)
with open(os.environ["FAKE_PROMPT_OUT"], "w", encoding="utf-8") as fh:
    fh.write(sys.stdin.read())
if os.environ.get("FAKE_ARGS_OUT"):
    with open(os.environ["FAKE_ARGS_OUT"], "w", encoding="utf-8") as fh:
        json.dump({"args": args, "active": os.environ.get("PAIR_NAVIGATOR_ACTIVE")}, fh)
if os.environ.get("FAKE_REPLY"):
    print(os.environ["FAKE_REPLY"])
else:
    review = json.loads(os.environ["FAKE_REVIEW"])
    print(json.dumps({"type": "result", "is_error": False, "result": json.dumps(review), "structured_output": review}))
