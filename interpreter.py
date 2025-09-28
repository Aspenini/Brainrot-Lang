#!/usr/bin/env python3
import sys
import re
from typing import List, Tuple, Union, Dict, Any

BRAINCELLS = {"rizz", "aura", "peak", "goon", "mog", "npc", "sigma"}

OP_MAP = {
    "💀": "+",
    "😭": "-",
    "😏": "*",
    "🚡": "/",
}

TOKEN_REGEX = re.compile(
    r"""
    \s*(
        "([^"\\]|\\.)*"      |  # string literal with escapes
        \d+                  |  # integer literal
        💀|😭|😏|🚡           |  # emoji ops
        FR                   |  # equals token
        [A-Za-z_]\w*         |  # identifiers/keywords
        \S                      # any other single non-space char (for helpful errors)
    )
    """,
    re.VERBOSE,
)

class BrainrotError(Exception):
    pass

def strip_comment(line: str) -> str:
    # Comments start with the literal "🖕" (middle finger) and run to EOL
    cut = line.split("🖕", 1)[0]
    return cut.rstrip()

def tokenize_expr(expr: str, line_no: int) -> List[str]:
    tokens = []
    pos = 0
    while pos < len(expr):
        m = TOKEN_REGEX.match(expr, pos)
        if not m:
            raise BrainrotError(f"[line {line_no}] Bad token near: {expr[pos:pos+10]!r}")
        tok = m.group(1)
        tokens.append(tok)
        pos = m.end()
    return tokens

def unescape_string(s: str) -> str:
    # remove surrounding quotes and handle common escapes
    assert s.startswith('"') and s.endswith('"'), "string must start and end with quotes"
    body = s[1:-1]
    return bytes(body, "utf-8").decode("unicode_escape")

def is_string(tok: str) -> bool:
    return len(tok) >= 2 and tok[0] == '"' and tok[-1] == '"'

def to_value(tok: str, env: Dict[str, Any], line_no: int) -> Any:
    if is_string(tok):
        return unescape_string(tok)
    if tok.isdigit():
        return int(tok)
    if tok in env:
        return env[tok]
    raise BrainrotError(f"[line {line_no}] Unknown name or invalid literal: {tok!r}")

# Shunting-yard to handle precedence for +,-,*,/
def to_rpn(tokens: List[str], line_no: int) -> List[str]:
    # Map emojis to ASCII for internal handling
    mapped = [OP_MAP.get(t, t) for t in tokens]
    output: List[str] = []
    ops: List[str] = []

    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    for t in mapped:
        if t in {"+", "-", "*", "/"}:
            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[t]:
                output.append(ops.pop())
            ops.append(t)
        else:
            output.append(t)
    while ops:
        output.append(ops.pop())
    return output

def eval_rpn(rpn: List[str], env: Dict[str, Any], line_no: int) -> Any:
    stack: List[Any] = []
    for t in rpn:
        if t in {"+", "-", "*", "/"}:
            if len(stack) < 2:
                raise BrainrotError(f"[line {line_no}] Not enough operands for operator {t!r}")
            b = stack.pop()
            a = stack.pop()
            # String support: only '+' allowed for concatenation
            if t == "+":
                if isinstance(a, str) or isinstance(b, str):
                    stack.append(str(a) + str(b))
                else:
                    stack.append(a + b)
            elif t == "-":
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    stack.append(a - b)
                else:
                    raise BrainrotError(f"[line {line_no}] '-' not supported for strings")
            elif t == "*":
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    stack.append(a * b)
                elif isinstance(a, str) and isinstance(b, int):
                    stack.append(a * b)
                elif isinstance(b, str) and isinstance(a, int):
                    stack.append(b * a)
                else:
                    raise BrainrotError(f"[line {line_no}] invalid operands for '*'")
            elif t == "/":
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    if b == 0:
                        raise BrainrotError(f"[line {line_no}] division by zero")
                    stack.append(a / b)
                else:
                    raise BrainrotError(f"[line {line_no}] '/' only valid for numbers")
        else:
            stack.append(to_value(t, env, line_no))
    if len(stack) != 1:
        raise BrainrotError(f"[line {line_no}] Expression did not reduce to a single value")
    return stack[0]

def eval_expr(expr_src: str, env: Dict[str, Any], line_no: int) -> Any:
    # Replace emoji operators with their text equivalents for tokenization consistency
    tokens = tokenize_expr(expr_src, line_no)
    # Quick validation: reject parentheses for now (not in spec)
    if any(t in {"(", ")"} for t in tokens):
        raise BrainrotError(f"[line {line_no}] Parentheses are not supported in Brainrot expressions")
    rpn = to_rpn(tokens, line_no)
    return eval_rpn(rpn, env, line_no)

def run(lines: List[str]) -> None:
    # Strip comments & blank lines
    cleaned = [strip_comment(l).rstrip() for l in lines]
    # Remove empty lines
    cleaned = [l for l in cleaned if l.strip() != ""]

    if not cleaned or cleaned[0] != "LOCK IN":
        raise BrainrotError("Program must start with 'LOCK IN'")
    if cleaned[-1] != "ITS OVER":
        raise BrainrotError("Program must end with 'ITS OVER'")

    # Slice to the body
    body = cleaned[1:-1]

    env: Dict[str, Any] = {}

    def ensure_braincell(name: str, line_no: int):
        if name not in BRAINCELLS:
            raise BrainrotError(f"[line {line_no}] Unknown braincell {name!r}. Valid: {sorted(BRAINCELLS)}")

    for idx, raw in enumerate(body, start=2):  # +2 for 1-based lines incl. 'LOCK IN'
        line = raw.strip()
        if not line:
            continue

        # Instructions:
        # FANUMTAX <cell> FR <expr>
        # DIDDLE   <dest> FR <sourceCell>
        # SAY <expr>
        parts = line.split()
        head = parts[0]

        if head == "FANUMTAX":
            # Expect: FANUMTAX <cell> FR <expr...>
            if len(parts) < 4:
                raise BrainrotError(f"[line {idx}] Invalid FANUMTAX syntax. Use: FANUMTAX <cell> FR <expr>")
            cell = parts[1]
            ensure_braincell(cell, idx)
            if parts[2] != "FR":
                raise BrainrotError(f"[line {idx}] Expected 'FR' after braincell name")
            expr = line.split("FR", 1)[1].strip()  # everything after FR
            val = eval_expr(expr, env, idx)
            env[cell] = val

        elif head == "DIDDLE":
            # Expect: DIDDLE <dest> FR <sourceCell>
            if len(parts) != 4 or parts[2] != "FR":
                raise BrainrotError(f"[line {idx}] Invalid DIDDLE syntax. Use: DIDDLE <dest> FR <sourceCell>")
            dest = parts[1]
            src = parts[3]
            ensure_braincell(dest, idx)
            ensure_braincell(src, idx)
            if src not in env:
                raise BrainrotError(f"[line {idx}] Cannot copy from empty braincell {src!r}")
            env[dest] = env[src]

        elif head == "SAY":
            # SAY <expr>
            expr = line[len("SAY"):].strip()
            if not expr:
                raise BrainrotError(f"[line {idx}] SAY needs an expression or braincell")
            val = eval_expr(expr, env, idx)
            # Print like a normal language would
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            print(val)

        else:
            raise BrainrotError(f"[line {idx}] Unknown instruction: {head!r}")

def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        try:
            run(lines)
        except BrainrotError as e:
            print(f"❌ BrainrotError: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Minimal REPL
        print("Brainrot REPL. Type LOCK IN to start, ITS OVER to run. Comments with 🖕")
        buf: List[str] = []
        while True:
            try:
                line = input("... ").rstrip("\n")
            except EOFError:
                print()
                break
            if not buf and line.strip() != "LOCK IN":
                print("Start with: LOCK IN")
                continue
            buf.append(line)
            if line.strip() == "ITS OVER":
                try:
                    run(buf)
                except BrainrotError as e:
                    print(f"❌ BrainrotError: {e}")
                buf = []

if __name__ == "__main__":
    main()
