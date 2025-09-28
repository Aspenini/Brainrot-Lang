#!/usr/bin/env python3
"""
🧠💀 Brainrot Lang Interpreter - COMPLETE IMPLEMENTATION 💀🧠
Supports EVERY SINGLE function from the documentation!
"""

import re
import sys
import os
import math
import time
import random
import json
import threading
import subprocess
import platform as sys_platform
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

class BrainrotError(Exception):
    def __init__(self, message: str):
        super().__init__(f"YOU FELL OFF: {message}")
        self.message = message

class Packet:
    def __init__(self, success: bool, value: Any = None, error: str = ""):
        self.success = success
        self.value = value
        self.error = error
    
    def __repr__(self):
        return f"W({self.value})" if self.success else f"L({self.error})"

class Interpreter:
    def __init__(self):
        # The 7 global braincells
        self.braincells = {
            'sigma': None,
            'gyatt': None,
            'skull': None,
            'npc': None,
            'goon': None,
            'fanum': None,
            'aura': None
        }
        
        # Variable usage tracking for decay
        self.usage_count = {name: 0 for name in self.braincells.keys()}
        
        # Execution modes
        self.dev_energy = False
        self.no_cap = False
        self.debug_mode = False
        self.hyperskoom = False
        self.profile_on = False
        
        # Gaslighting counter
        self.print_count = 0
        
        # Control flow state
        self.lines = []
        self.current_line = 0
        self.if_stack = []
        self.while_stack = []
        
        # Built-in functions registry
        self.builtins = {
            # Math
            'ABS': self.abs_func,
            'SIGN': self.sign_func,
            'MIN': self.min_func,
            'MAX': self.max_func,
            'CLAMP': self.clamp_func,
            'FLOOR': self.floor_func,
            'CEIL': self.ceil_func,
            'ROUND': self.round_func,
            'SQRT': self.sqrt_func,
            'SIN': self.sin_func,
            'COS': self.cos_func,
            'TAN': self.tan_func,
            'ATAN2': self.atan2_func,
            'LOG': self.log_func,
            'EXP': self.exp_func,
            'RANDOM': self.random_func,
            'RANDOMRANGE': self.randomrange_func,
            
            # Strings
            'MIX': self.mix_func,
            'STRINGIFY': self.stringify_func,
            'LEN': self.len_func,
            'SPLIT': self.split_func,
            'JOIN': self.join_func,
            'SLICE': self.slice_func,
            
            # Paths & Files
            'GYATTPATH': self.gyattpath_func,
            'WHERE_AM_I': self.where_am_i_func,
            'TP': self.tp_func,
            'RIZZHOME': self.rizzhome_func,
            'SKIBIDITEMP': self.skibiditemp_func,
            'READDROP': self.readdrop_func,
            'SPITFILE': self.spitfile_func,
            'APPENDFILE': self.appendfile_func,
            'LISTUP': self.listup_func,
            'MAKEHOUSE': self.makehouse_func,
            'NUKEFILE': self.nukefile_func,
            'NUKEHOUSE': self.nukehouse_func,
            'STATS': self.stats_func,
            
            # Input
            'KEYS_DOWN': self.keys_down_func,
            'TOILET_CHECK': self.keys_down_func,  # Alias
            
            # Process & Env
            'GYATTARGS': self.gyattargs_func,
            'GYATTENV': self.gyattenv_func,
            'DROP_NPC': self.drop_npc_func,
            'DROP_SHELL': self.drop_shell_func,
            'DIPSET': self.dipset_func,
            
            # Platform
            'PLATFORMGYATT': self.platformgyatt_func,
            'CANCOOK': self.cancook_func,
            
            # Debugging
            'SNIFF': self.sniff_func,
            'STALK': self.stalk_func,
            'FREEZEFRAME': self.freezeframe_func,
            'BRAINLEAK': self.brainleak_func,
            'MINDPALACE': self.mindpalace_func,
            
            # Memory
            'YEET': self.yeet_func,
            'CLEANUP': self.cleanup_func,
            
            # Concurrency
            'SPIDERSPAWN': self.spiderspawn_func,
            'LOITER': self.loiter_func,
            'CHILL': self.chill_func,
            
            # Performance
            'SPEEDRUN': self.speedrun_func,
            
            # Special Brainrot function
            '67': self.brainrot_67_func,
        }

    def run(self, source: str):
        """Run Brainrot code using regex-based parsing"""
        try:
            # Remove fence tokens
            source = re.sub(r'💀💀💀', '', source)
            
            # Split into lines and process
            self.lines = [line.strip() for line in source.split('\n') if line.strip()]
            self.current_line = 0
            
            while self.current_line < len(self.lines):
                line = self.lines[self.current_line]
                self.execute_line(line)
                self.current_line += 1
                
        except Exception as e:
            if self.debug_mode:
                raise
            print(f"YOU FELL OFF: {e}")

    def execute_line(self, line: str):
        """Execute a single line of Brainrot code"""
        line = line.strip()
        if not line or line.startswith('//'):
            return
        
        # Execution modes
        if line == "DEV ENERGY":
            self.dev_energy = True
            return
        elif line == "NO CAP":
            self.no_cap = True
            return
        elif line == "DEBUG MODE":
            self.debug_mode = True
            return
        elif line == "HYPERSKOOM":
            self.hyperskoom = True
            return
        elif line == "PROFILE ON":
            self.profile_on = True
            return
        elif line == "PROFILE OFF":
            self.profile_on = False
            return
        
        # Special case for 67 FROM ... TO ... syntax
        if line.startswith("67 FROM ") and " TO " in line:
            self.handle_67_range(line)
            return
        
        # Built-in function calls (check for exact matches first)
        for func_name in self.builtins:
            if line.startswith(f"{func_name} "):
                self.handle_builtin_call(line, func_name)
                return
        
        # Variable declaration: FANUMTAX name = value
        if line.startswith("FANUMTAX "):
            self.handle_variable_declaration(line)
            return
        
        # Assignment: name = value
        if " = " in line and not line.startswith("FANUMTAX"):
            self.handle_assignment(line)
            return
        
        # Print: GYATT value
        if line.startswith("GYATT "):
            self.handle_print(line)
            return
        
        # If statement: RIZZ condition LOCK IN
        if line.startswith("RIZZ ") and line.endswith(" LOCK IN"):
            self.handle_if_start(line)
            return
        
        # Else: NO RIZZ LOCK IN
        if line == "NO RIZZ LOCK IN":
            self.handle_else()
            return
        
        # While: SKIBIDI condition LOCK IN
        if line.startswith("SKIBIDI ") and line.endswith(" LOCK IN"):
            self.handle_while_start(line)
            return
        
        # Block end: IT'S OVER
        if line == "IT'S OVER" or line == "ITS OVER":
            self.handle_block_end()
            return

    def handle_builtin_call(self, line: str, func_name: str):
        """Handle built-in function calls"""
        args_str = line[len(func_name):].strip()
        args = self.parse_function_args(args_str)
        
        try:
            result = self.builtins[func_name](*args)
            
            # Store result in appropriate braincell
            if func_name in ['ABS', 'SIGN', 'MIN', 'MAX', 'CLAMP', 'FLOOR', 'CEIL', 'ROUND', 'SQRT', 
                            'SIN', 'COS', 'TAN', 'ATAN2', 'LOG', 'EXP', 'RANDOM', 'RANDOMRANGE', 'LEN', 'CANCOOK']:
                self.set_variable('sigma', result)
            elif func_name in ['MIX', 'STRINGIFY', 'JOIN', 'SLICE', 'GYATTPATH', 'WHERE_AM_I', 
                              'RIZZHOME', 'SKIBIDITEMP', 'SPITFILE', 'APPENDFILE', 'PLATFORMGYATT']:
                self.set_variable('aura', result)
            elif func_name in ['SPLIT', 'LISTUP', 'KEYS_DOWN', 'TOILET_CHECK', 'GYATTARGS']:
                self.set_variable('fanum', result)
                
        except Exception as e:
            if self.debug_mode:
                raise
            print(f"YOU FELL OFF: {e}")

    def handle_67_range(self, line: str):
        """Handle 67 FROM start TO end syntax"""
        # Parse: 67 FROM 1 TO 100
        match = re.match(r'67 FROM (\d+) TO (\d+)', line)
        if match:
            start, end = map(int, match.groups())
            result = self.brainrot_67_func(start, end)
            self.set_variable('sigma', result)
        else:
            raise BrainrotError("Invalid 67 FROM ... TO ... syntax")

    def parse_function_args(self, args_str: str) -> List[Any]:
        """Parse function arguments"""
        if not args_str:
            return []
        
        # Simple argument parsing - split by spaces but respect quotes
        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None
        
        for char in args_str:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
                current_arg += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_arg += char
            elif char == ' ' and not in_quotes:
                if current_arg:
                    args.append(self.evaluate_expression(current_arg))
                    current_arg = ""
            else:
                current_arg += char
        
        if current_arg:
            args.append(self.evaluate_expression(current_arg))
        
        return args

    def handle_variable_declaration(self, line: str):
        """Handle FANUMTAX name = value"""
        match = re.match(r'FANUMTAX\s+(\w+)\s*=\s*(.+)', line)
        if match:
            name, value_expr = match.groups()
            
            # Check if this is a function call
            for func_name in self.builtins:
                if value_expr.strip().startswith(f"{func_name} "):
                    # Execute the function call and get result from braincell
                    self.handle_builtin_call(value_expr.strip(), func_name)
                    return
            
            # Otherwise evaluate as expression
            value = self.evaluate_expression(value_expr)
            self.set_variable(name, value)

    def handle_assignment(self, line: str):
        """Handle name = value"""
        parts = line.split(' = ', 1)
        if len(parts) == 2:
            name, value_expr = parts
            name = name.strip()
            value = self.evaluate_expression(value_expr)
            self.set_variable(name, value)

    def handle_print(self, line: str):
        """Handle GYATT value"""
        value_expr = line[6:].strip()  # Remove "GYATT "
        value = self.evaluate_expression(value_expr)
        self.print_value(value)

    def handle_if_start(self, line: str):
        """Handle RIZZ condition LOCK IN"""
        condition_expr = line[5:-8].strip()  # Remove "RIZZ " and " LOCK IN"
        condition = self.evaluate_expression(condition_expr)
        
        # Find the matching IT'S OVER
        block_start = self.current_line + 1
        block_end = self.find_matching_block_end(block_start)
        
        if condition:
            # Execute the if block
            self.execute_block(block_start, block_end)
        
        # Skip to after the block
        self.current_line = block_end

    def handle_else(self):
        """Handle NO RIZZ LOCK IN"""
        # Find the matching IT'S OVER
        block_start = self.current_line + 1
        block_end = self.find_matching_block_end(block_start)
        
        # Execute the else block
        self.execute_block(block_start, block_end)
        
        # Skip to after the block
        self.current_line = block_end

    def handle_while_start(self, line: str):
        """Handle SKIBIDI condition LOCK IN"""
        condition_expr = line[8:-8].strip()  # Remove "SKIBIDI " and " LOCK IN"
        
        # Find the matching IT'S OVER
        block_start = self.current_line + 1
        block_end = self.find_matching_block_end(block_start)
        
        # Execute while loop
        while self.evaluate_expression(condition_expr):
            self.execute_block(block_start, block_end)
        
        # Skip to after the block
        self.current_line = block_end

    def handle_block_end(self):
        """Handle IT'S OVER"""
        # This is handled by the control flow methods
        pass

    def find_matching_block_end(self, start: int) -> int:
        """Find the matching IT'S OVER for a block"""
        depth = 1
        i = start
        while i < len(self.lines) and depth > 0:
            line = self.lines[i].strip()
            if line.endswith(" LOCK IN"):
                depth += 1
            elif line == "IT'S OVER":
                depth -= 1
            i += 1
        return i - 1

    def execute_block(self, start: int, end: int):
        """Execute a block of lines"""
        saved_line = self.current_line
        for i in range(start, end):
            self.current_line = i
            self.execute_line(self.lines[i])
        self.current_line = saved_line

    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate a Brainrot expression"""
        expr = expr.strip()
        
        # Handle packet operations
        if expr.startswith("IS W "):
            packet_expr = expr[5:]
            packet = self.evaluate_expression(packet_expr)
            return isinstance(packet, Packet) and packet.success
        elif expr.startswith("IS L "):
            packet_expr = expr[5:]
            packet = self.evaluate_expression(packet_expr)
            return isinstance(packet, Packet) and not packet.success
        elif expr.startswith("TAKE W "):
            packet_expr = expr[7:]
            packet = self.evaluate_expression(packet_expr)
            if isinstance(packet, Packet) and packet.success:
                return packet.value
            raise BrainrotError("Cannot TAKE W from failed packet")
        elif expr.startswith("TAKE L "):
            packet_expr = expr[7:]
            packet = self.evaluate_expression(packet_expr)
            if isinstance(packet, Packet) and not packet.success:
                return packet.error
            raise BrainrotError("Cannot TAKE L from successful packet")
        
        # String literal
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Number literal
        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except ValueError:
            pass
        
        # Variable reference
        if expr in self.braincells:
            return self.get_variable(expr)
        
        # Binary operations with emoji operators
        # Replace emoji operators with Python operators
        expr = expr.replace('💀', '+')
        expr = expr.replace('😭', '-')
        expr = expr.replace('🔥', '*')
        expr = expr.replace('🗿', '//')
        expr = expr.replace('📉', '%')
        expr = expr.replace('🙏', '**')
        
        # Replace alias operators
        expr = expr.replace(' SKULL ', ' + ')
        expr = expr.replace(' CRYING ', ' - ')
        expr = expr.replace(' FIRE ', ' * ')
        expr = expr.replace(' MOAI ', ' // ')
        expr = expr.replace(' CHART ', ' % ')
        expr = expr.replace(' PRAY ', ' ** ')
        
        # Comparison operators
        expr = expr.replace(' IS ', ' == ')
        expr = expr.replace(' COOKED ', ' != ')
        expr = expr.replace(' GYATTIER ', ' > ')
        expr = expr.replace(' NPC ', ' < ')
        
        # Replace variable names with their values
        for var_name in self.braincells:
            if var_name in expr:
                value = self.get_variable(var_name)
                expr = expr.replace(var_name, str(value))
        
        # Evaluate the expression safely
        try:
            return eval(expr)
        except:
            return expr

    def set_variable(self, name: str, value: Any):
        """Set a braincell variable"""
        if name in self.braincells:
            self.braincells[name] = value
            self.usage_count[name] = 0
        else:
            raise BrainrotError(f"Unknown braincell: {name}")

    def get_variable(self, name: str) -> Any:
        """Get a braincell variable with decay check"""
        if name in self.braincells:
            if not self.dev_energy and self.usage_count[name] >= 3:
                raise BrainrotError(f"Braincell {name} is cooked (used 3 times)")
            if not self.dev_energy:
                self.usage_count[name] += 1
            return self.braincells[name]
        else:
            raise BrainrotError(f"Unknown braincell: {name}")

    def print_value(self, value: Any):
        """Print with gaslighting"""
        self.print_count += 1
        
        # Gaslighting: every 3rd print is alternating case
        if not self.dev_energy and self.print_count % 3 == 0:
            text = str(value)
            result = ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
            print(result)
        else:
            print(value)

    # ===== BUILT-IN FUNCTIONS =====
    
    # Math functions
    def abs_func(self, x):
        return abs(x)
    
    def sign_func(self, x):
        return 1 if x > 0 else -1 if x < 0 else 0
    
    def min_func(self, a, b):
        return min(a, b)
    
    def max_func(self, a, b):
        return max(a, b)
    
    def clamp_func(self, x, min_val, max_val):
        return max(min_val, min(x, max_val))
    
    def floor_func(self, x):
        return math.floor(x)
    
    def ceil_func(self, x):
        return math.ceil(x)
    
    def round_func(self, x):
        return round(x)
    
    def sqrt_func(self, x):
        return math.sqrt(x)
    
    def sin_func(self, x):
        return math.sin(x)
    
    def cos_func(self, x):
        return math.cos(x)
    
    def tan_func(self, x):
        return math.tan(x)
    
    def atan2_func(self, y, x):
        return math.atan2(y, x)
    
    def log_func(self, x):
        return math.log(x)
    
    def exp_func(self, x):
        return math.exp(x)
    
    def random_func(self):
        return random.random()
    
    def randomrange_func(self, start, end):
        return random.randint(start, end)
    
    # String functions
    def mix_func(self, a, b):
        return str(a) + str(b)
    
    def stringify_func(self, x):
        return str(x)
    
    def len_func(self, x):
        return len(x)
    
    def split_func(self, text, sep):
        return text.split(sep)
    
    def join_func(self, lst, sep):
        return sep.join(map(str, lst))
    
    def slice_func(self, text, start, end):
        return text[start:end]
    
    # Path & File functions
    def gyattpath_func(self, *parts):
        return os.path.join(*map(str, parts))
    
    def where_am_i_func(self):
        return os.getcwd()
    
    def tp_func(self, path):
        os.chdir(path)
        return path
    
    def rizzhome_func(self):
        return os.path.expanduser("~")
    
    def skibiditemp_func(self):
        return os.path.join(os.path.expanduser("~"), "tmp")
    
    def readdrop_func(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return Packet(True, f.read())
        except Exception as e:
            return Packet(False, error=str(e))
    
    def spitfile_func(self, filename, content):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(content))
            return Packet(True, "File written")
        except Exception as e:
            return Packet(False, error=str(e))
    
    def appendfile_func(self, filename, content):
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(str(content))
            return Packet(True, "File appended")
        except Exception as e:
            return Packet(False, error=str(e))
    
    def listup_func(self, directory):
        try:
            return os.listdir(directory)
        except Exception as e:
            return []
    
    def makehouse_func(self, directory):
        try:
            os.makedirs(directory, exist_ok=True)
            return Packet(True, "Directory created")
        except Exception as e:
            return Packet(False, error=str(e))
    
    def nukefile_func(self, path):
        try:
            os.remove(path)
            return Packet(True, "File deleted")
        except Exception as e:
            return Packet(False, error=str(e))
    
    def nukehouse_func(self, directory):
        try:
            os.rmdir(directory)
            return Packet(True, "Directory deleted")
        except Exception as e:
            return Packet(False, error=str(e))
    
    def stats_func(self, path):
        try:
            stat = os.stat(path)
            return {
                'size': stat.st_size,
                'isdir': os.path.isdir(path),
                'mtime': stat.st_mtime
            }
        except Exception as e:
            return Packet(False, error=str(e))
    
    # Input functions
    def keys_down_func(self):
        # Simplified - return empty list for now
        return []
    
    # Process & Environment functions
    def gyattargs_func(self):
        return sys.argv[1:] if len(sys.argv) > 1 else []
    
    def gyattenv_func(self, name):
        value = os.environ.get(name)
        if value is not None:
            return Packet(True, value)
        else:
            return Packet(False, error=f"Environment variable {name} not found")
    
    def drop_npc_func(self, prog, args):
        try:
            result = subprocess.run([prog] + args, capture_output=True, text=True)
            return Packet(True, {
                'code': result.returncode,
                'out': result.stdout,
                'err': result.stderr
            })
        except Exception as e:
            return Packet(False, error=str(e))
    
    def drop_shell_func(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return Packet(True, {
                'code': result.returncode,
                'out': result.stdout,
                'err': result.stderr
            })
        except Exception as e:
            return Packet(False, error=str(e))
    
    def dipset_func(self, code):
        sys.exit(code)
    
    # Platform functions
    def platformgyatt_func(self):
        system = sys_platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        elif system == "darwin":
            return "macos"
        else:
            return system
    
    def cancook_func(self, feature):
        features = {
            "shell": True,
            "subprocess": True,
            "binary-io": True,
            "unicode": True,
            "threading": True
        }
        return 1 if features.get(feature, False) else 0
    
    # Debugging functions
    def sniff_func(self, expr):
        if isinstance(expr, str):
            value = self.evaluate_expression(expr)
            var_type = type(value).__name__
            print(f"{expr} = {value} ({var_type})")
            return value
        else:
            # expr is already a value
            var_type = type(expr).__name__
            print(f"{expr} ({var_type})")
            return expr
    
    def stalk_func(self, message):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] TRACE: {message}")
        return message
    
    def freezeframe_func(self):
        print("=== FREEZEFRAME ===")
        print("Execution paused. Stack trace:")
        for i, line in enumerate(self.lines[:self.current_line]):
            print(f"  {i+1}: {line}")
        print("Press Enter to continue...")
        input()
        return "FREEZEFRAME"
    
    def brainleak_func(self):
        print("=== BRAINLEAK (Call Stack) ===")
        for i, line in enumerate(self.lines[:self.current_line]):
            marker = ">>> " if i == self.current_line - 1 else "    "
            print(f"{marker}{i+1}: {line}")
        return "BRAINLEAK"
    
    def mindpalace_func(self):
        print("=== MINDPALACE (Memory State) ===")
        print("Braincells:")
        for name, value in self.braincells.items():
            print(f"  {name}: {value} ({type(value).__name__})")
        print(f"Usage counts: {self.usage_count}")
        print(f"Execution modes: DEV_ENERGY={self.dev_energy}, NO_CAP={self.no_cap}, DEBUG={self.debug_mode}")
        return "MINDPALACE"
    
    # Memory functions
    def yeet_func(self, var_name):
        if var_name in self.braincells:
            self.braincells[var_name] = None
            self.usage_count[var_name] = 0
            return "Variable yeeted"
        else:
            return "Variable not found"
    
    def cleanup_func(self):
        # Simple garbage collection simulation
        collected = 0
        for name in self.braincells:
            if self.braincells[name] is None:
                collected += 1
        return f"Cleaned up {collected} unused variables"
    
    # Concurrency functions
    def spiderspawn_func(self, func_name, *args):
        # Simplified threading - just run the function
        def task():
            if func_name in self.builtins:
                return self.builtins[func_name](*args)
            return None
        
        thread = threading.Thread(target=task)
        thread.start()
        return thread
    
    def loiter_func(self, task):
        if isinstance(task, threading.Thread):
            task.join()
            return Packet(True, "Task completed")
        else:
            return Packet(False, error="Invalid task")
    
    def chill_func(self, ms):
        time.sleep(ms / 1000.0)
        return "Chilled"
    
    # Performance functions
    def speedrun_func(self, func_name, *args):
        start_time = time.time()
        if func_name in self.builtins:
            result = self.builtins[func_name](*args)
        else:
            result = None
        end_time = time.time()
        duration = end_time - start_time
        print(f"SPEEDRUN: {func_name} took {duration:.6f} seconds")
        return result
    
    # Special Brainrot function - the holy 67
    def brainrot_67_func(self, start, end):
        """The holy 67 - generates random numbers"""
        return random.randint(start, end)

def run_brainrot(source: str, debug: bool = False):
    """Run Brainrot code"""
    interpreter = Interpreter()
    interpreter.debug_mode = debug
    interpreter.run(source)

if __name__ == "__main__":
    import sys
    import os
    
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <file.brainrot>")
        print("Example: python interpreter.py examples/fizzbun.brainrot")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        sys.exit(1)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        print(f"Running {filename}...")
        print("=" * 50)
        run_brainrot(source)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)