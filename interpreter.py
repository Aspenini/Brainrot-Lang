#!/usr/bin/env python3
import sys
import re
from typing import List, Tuple, Union, Dict, Any

BRAINCELLS = {"aura", "peak", "goon", "mog", "npc", "sigma", "gyatt"}

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

def eval_expr(expr_src: str, env: Dict[str, Any], line_no: int, functions: Dict = None) -> Any:
    # Check for function calls first (before tokenization)
    if "(" in expr_src and ")" in expr_src:
        # Simple function call detection
        paren_start = expr_src.find("(")
        paren_end = expr_src.rfind(")")
        if paren_start > 0 and paren_end > paren_start:
            func_name = expr_src[:paren_start].strip()
            if functions and func_name in functions:
                # Parse arguments
                args_str = expr_src[paren_start+1:paren_end].strip()
                args = []
                if args_str:
                    # Simple argument parsing - split by comma
                    args = [arg.strip() for arg in args_str.split(",")]
                
                return call_function(func_name, args, env, line_no, functions)
    
    # Replace emoji operators with their text equivalents for tokenization consistency
    tokens = tokenize_expr(expr_src, line_no)
    
    # Quick validation: reject parentheses for now (not in spec)
    if any(t in {"(", ")"} for t in tokens):
        raise BrainrotError(f"[line {line_no}] Parentheses are not supported in Brainrot expressions")
    rpn = to_rpn(tokens, line_no)
    return eval_rpn(rpn, env, line_no)

def call_function(func_name: str, args: List[str], env: Dict[str, Any], line_no: int, functions: Dict) -> Any:
    """Call a function with the given arguments."""
    if func_name not in functions:
        raise BrainrotError(f"[line {line_no}] Function '{func_name}' not defined")
    
    func_def = functions[func_name]
    expected_params = len(func_def["params"])
    actual_args = len(args)
    
    if actual_args != expected_params:
        raise BrainrotError(f"[line {line_no}] Function '{func_name}' expects {expected_params} arguments, got {actual_args}")
    
    # Create new environment for function
    func_env = env.copy()
    
    # Bind parameters
    for param, arg_expr in zip(func_def["params"], args):
        arg_val = eval_expr(arg_expr, env, line_no, functions)
        func_env[param] = arg_val
    
    # Add parameter names to environment so they can be used in expressions
    for param in func_def["params"]:
        if param not in func_env:
            func_env[param] = ""
    
    # Execute function body
    func_body = func_def["body"]
    result = ""  # Default return value
    
    for i, line in enumerate(func_body):
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        head = parts[0] if parts else ""
        
        if head == "RETURN":
            if len(parts) > 1:
                expr = line[len("RETURN"):].strip()
                result = eval_expr(expr, func_env, line_no, functions)
            break  # Return immediately
            
        elif head == "FANUMTAX":
            if len(parts) >= 4 and parts[2] == "FR":
                cell = parts[1]
                if cell not in BRAINCELLS:
                    raise BrainrotError(f"[line {line_no}] Unknown braincell {cell}")
                expr = line.split("FR", 1)[1].strip()
                func_env[cell] = eval_expr(expr, func_env, line_no, functions)
                
        elif head == "DIDDLE":
            if len(parts) == 4 and parts[2] == "FR":
                dest, src = parts[1], parts[3]
                if dest not in BRAINCELLS or src not in BRAINCELLS:
                    raise BrainrotError(f"[line {line_no}] Unknown braincell")
                if src not in func_env:
                    raise BrainrotError(f"[line {line_no}] Cannot copy from empty braincell {src}")
                func_env[dest] = func_env[src]
                
        elif head == "SAY":
            expr = line[len("SAY"):].strip()
            if expr:
                val = eval_expr(expr, func_env, line_no, functions)
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                print(val)
    
    return result

def truthy(val: Any) -> bool:
    """Determine truthiness for control flow."""
    if isinstance(val, str):
        return len(val) > 0
    if isinstance(val, (int, float)):
        return val != 0
    return bool(val)

def build_blocks(body: List[str]) -> Dict[str, Dict[int, Any]]:
    """Build control flow mappings for IF/ELSE and WHILE blocks."""
    if_starts: Dict[int, Dict[str, int]] = {}  # pc -> {else: idx or -1, end: idx}
    else_to_end: Dict[int, int] = {}  # else_pc -> end_pc
    while_start: Dict[int, int] = {}  # while_pc -> end_pc
    while_end: Dict[int, int] = {}  # end_pc -> while_pc
    stack: List[Tuple[str, int]] = []
    
    for i, raw in enumerate(body):
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        head = parts[0] if parts else ""
        
        if head == "ONGOD":
            stack.append(("IF", i))
        elif head == "NO" and line.startswith("NO CAP"):
            if not stack or stack[-1][0] != "IF":
                raise BrainrotError(f"[line {i+2}] 'NO CAP' without matching 'ONGOD'")
            if_idx = stack[-1][1]
            stack.append(("ELSE", i))
            if_starts[if_idx] = {"else": i, "end": -1}
        elif head == "DEADASS":
            if not stack:
                raise BrainrotError(f"[line {i+2}] 'DEADASS' without matching 'ONGOD'")
            kind, idx0 = stack.pop()
            if kind == "ELSE":
                if not stack or stack[-1][0] != "IF":
                    raise BrainrotError(f"[line {i+2}] malformed IF/ELSE/DEADASS")
                _, if_idx = stack.pop()
                prev = if_starts.get(if_idx, {"else": idx0, "end": -1})
                if_starts[if_idx] = {"else": prev["else"], "end": i}
                else_to_end[idx0] = i
            elif kind == "IF":
                if_starts[idx0] = {"else": -1, "end": i}
            else:
                raise BrainrotError(f"[line {i+2}] 'DEADASS' closes unexpected block {kind}")
        elif head == "SKIBIDI":
            stack.append(("WHILE", i))
        elif head == "RIZZUP":
            if not stack or stack[-1][0] != "WHILE":
                raise BrainrotError(f"[line {i+2}] 'RIZZUP' without matching 'SKIBIDI'")
            _, start_idx = stack.pop()
            while_start[start_idx] = i
            while_end[i] = start_idx
    
    if stack:
        kind, idx0 = stack[-1]
        raise BrainrotError(f"[line {idx0+2}] Unclosed block starting here: {kind}")
    
    return {
        "if_starts": if_starts,
        "else_to_end": else_to_end,
        "while_start": while_start,
        "while_end": while_end,
    }

def parse_functions(lines: List[str]) -> Tuple[Dict[str, Dict], List[str]]:
    """Parse function definitions and return functions dict and main program lines."""
    functions = {}  # name -> {params: [], body: [], start_line: int}
    main_lines = []
    current_func = None
    func_stack = []
    
    for i, line in enumerate(lines):
        parts = line.strip().split()
        if not parts:
            if current_func:
                functions[current_func]["body"].append("")
            else:
                main_lines.append("")
            continue
            
        head = parts[0]
        
        if head == "TRALALERO":
            if len(parts) < 2:
                raise BrainrotError(f"[line {i+1}] TRALALERO needs a function name")
            
            # Parse function signature: name(param1, param2, ...)
            func_sig = " ".join(parts[1:])
            if "(" not in func_sig or not func_sig.endswith(")"):
                raise BrainrotError(f"[line {i+1}] Invalid function signature. Use: TRALALERO name(param1, param2)")
            
            func_name = func_sig.split("(")[0].strip()
            params_str = func_sig.split("(")[1][:-1].strip()  # Remove closing )
            
            if func_name in functions:
                raise BrainrotError(f"[line {i+1}] Function '{func_name}' already defined")
            
            # Parse parameters
            params = []
            if params_str:
                params = [p.strip() for p in params_str.split(",")]
            
            current_func = func_name
            functions[func_name] = {
                "params": params,
                "body": [],
                "start_line": i + 1
            }
            func_stack.append(func_name)
            
        elif head == "TRALALA":
            if not current_func:
                raise BrainrotError(f"[line {i+1}] TRALALA without matching TRALALERO")
            current_func = None
            func_stack.pop()
            
        elif current_func:
            functions[current_func]["body"].append(line)
            
        else:
            main_lines.append(line)
    
    if current_func:
        raise BrainrotError(f"Unclosed function '{current_func}' - missing TRALALA")
    
    return functions, main_lines

def run(lines: List[str]) -> None:
    # Strip comments & blank lines
    cleaned = [strip_comment(l).rstrip() for l in lines]
    # Remove empty lines
    cleaned = [l for l in cleaned if l.strip() != ""]

    if not cleaned:
        raise BrainrotError("Empty program")
    
    # Parse functions first
    functions, main_lines = parse_functions(cleaned)
    
    if not main_lines or main_lines[0] != "LOCK IN":
        raise BrainrotError("Program must start with 'LOCK IN'")
    if main_lines[-1] != "ITS OVER":
        raise BrainrotError("Program must end with 'ITS OVER'")

    # Slice to the body
    body = main_lines[1:-1]
    
    # Build control flow mappings
    blocks = build_blocks(body)
    if_starts = blocks["if_starts"]
    else_to_end = blocks["else_to_end"]
    while_start = blocks["while_start"]
    while_end = blocks["while_end"]

    env: Dict[str, Any] = {}
    call_stack = []  # For function calls

    def ensure_braincell(name: str, line_no: int):
        if name not in BRAINCELLS:
            raise BrainrotError(f"[line {line_no}] Unknown braincell {name!r}. Valid: {sorted(BRAINCELLS)}")

    pc = 0  # program counter
    while pc < len(body):
        raw = body[pc]
        line_no = pc + 2  # +2 for 1-based lines including 'LOCK IN'
        line = raw.strip()
        
        if not line:
            pc += 1
            continue

        parts = line.split()
        head = parts[0] if parts else ""

        if head == "FANUMTAX":
            # Expect: FANUMTAX <cell> FR <expr...>
            if len(parts) < 4 or parts[2] != "FR":
                raise BrainrotError(f"[line {line_no}] Invalid FANUMTAX syntax. Use: FANUMTAX <cell> FR <expr>")
            cell = parts[1]
            ensure_braincell(cell, line_no)
            expr = line.split("FR", 1)[1].strip()  # everything after FR
            val = eval_expr(expr, env, line_no, functions)
            env[cell] = val
            pc += 1

        elif head == "DIDDLE":
            # Expect: DIDDLE <dest> FR <sourceCell>
            if len(parts) != 4 or parts[2] != "FR":
                raise BrainrotError(f"[line {line_no}] Invalid DIDDLE syntax. Use: DIDDLE <dest> FR <sourceCell>")
            dest = parts[1]
            src = parts[3]
            ensure_braincell(dest, line_no)
            ensure_braincell(src, line_no)
            if src not in env:
                raise BrainrotError(f"[line {line_no}] Cannot copy from empty braincell {src!r}")
            env[dest] = env[src]
            pc += 1

        elif head == "SAY":
            # SAY <expr>
            expr = line[len("SAY"):].strip()
            if not expr:
                raise BrainrotError(f"[line {line_no}] SAY needs an expression or braincell")
            val = eval_expr(expr, env, line_no, functions)
            # Print like a normal language would
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            print(val)
            pc += 1

        elif head == "ONGOD":
            # IF statement
            if pc not in if_starts:
                raise BrainrotError(f"[line {line_no}] IF mapping missing")
            block_info = if_starts[pc]
            else_idx = block_info["else"]
            end_idx = block_info["end"]
            expr = line[len("ONGOD"):].strip()
            cond = truthy(eval_expr(expr, env, line_no, functions))
            if cond:
                pc += 1  # execute if block
            else:
                # jump to else or end
                pc = (else_idx + 1) if else_idx != -1 else (end_idx + 1)

        elif head == "NO" and line.startswith("NO CAP"):
            # ELSE statement - jump to end
            if pc not in else_to_end:
                raise BrainrotError(f"[line {line_no}] NO CAP mapping missing")
            end_idx = else_to_end[pc]
            pc = end_idx + 1

        elif head == "DEADASS":
            # END IF - just continue
            pc += 1

        elif head == "SKIBIDI":
            # WHILE loop
            if pc not in while_start:
                raise BrainrotError(f"[line {line_no}] WHILE mapping missing")
            end_idx = while_start[pc]
            expr = line[len("SKIBIDI"):].strip()
            cond = truthy(eval_expr(expr, env, line_no, functions))
            if cond:
                pc += 1  # enter loop body
            else:
                pc = end_idx + 1  # skip loop

        elif head == "RIZZUP":
            # END WHILE - jump back to while start
            if pc not in while_end:
                raise BrainrotError(f"[line {line_no}] RIZZUP mapping missing")
            start_idx = while_end[pc]
            pc = start_idx  # jump back to SKIBIDI

        else:
            raise BrainrotError(f"[line {line_no}] Unknown instruction: {head!r}")

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
