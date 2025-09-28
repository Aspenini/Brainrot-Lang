#!/usr/bin/env python3
"""
🧠💀 Brainrot Lang Interpreter 💀🧠
A meme-first scripting language with emoji operators and Gen Z slang
"""

import re
import sys
import math
import time
import random
import struct
import subprocess
import os
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    # Program structure
    FENCE_START = "💀💀💀"
    FENCE_END = "💀💀💀"
    
    # Keywords
    DEV_ENERGY = "DEV ENERGY"
    NO_CAP = "NO CAP"
    DEBUG_MODE = "DEBUG MODE"
    HYPERSKOOM = "HYPERSKOOM"
    PROFILE_ON = "PROFILE ON"
    PROFILE_OFF = "PROFILE OFF"
    
    # Variables
    FANUMTAX = "FANUMTAX"
    RETURN = "RETURN"
    
    # Control flow
    RIZZ = "RIZZ"
    NO_RIZZ = "NO RIZZ"
    SKIBIDI = "SKIBIDI"
    LOCK_IN = "LOCK IN"
    ITS_OVER = "IT'S OVER"
    
    # Functions
    COOK = "COOK"
    USING = "USING"
    AND = "AND"
    PULL_UP = "PULL UP"
    WITH = "WITH"
    
    # I/O
    GYATT = "GYATT"
    NPC = "NPC"
    
    # Math operators (emoji + aliases)
    ADD = "💀"  # SKULL
    SUB = "😭"  # CRYING
    MUL = "🔥"  # FIRE
    DIV = "🗿"  # MOAI
    MOD = "📉"  # CHART
    POW = "🙏"  # PRAY
    
    # Comparisons
    IS = "IS"
    COOKED = "COOKED"
    GYATTIER = "GYATTIER"
    LESS_THAN = "NPC"
    IN = "IN"
    
    # Graphics
    OPEN_RIZZPORT = "OPEN RIZZPORT"
    SPAWN_PIXELS = "SPAWN PIXELS"
    SPAWN_BYTES = "SPAWN BYTES"
    DROP_PIXEL = "DROP PIXEL"
    PUT_PX = "PUT PX"
    GET_PX = "GET PX"
    BLIT_PIXELS = "BLIT PIXELS"
    WIPE = "WIPE"
    SHOWTIME = "SHOWTIME"
    LOCKOFF = "LOCKOFF"
    PACK_RGBA = "PACK RGBA"
    UNPACK_RGBA = "UNPACK RGBA"
    AT2D = "AT2D"
    WRITE_PPM = "WRITE PPM"
    READ_PPM = "READ PPM"
    
    # Memory
    YEET = "YEET"
    CLEANUP = "CLEANUP"
    
    # Debugging
    SNIFF = "SNIFF"
    STALK = "STALK"
    FREEZEFRAME = "FREEZEFRAME"
    BRAINLEAK = "BRAINLEAK"
    MINDPALACE = "MINDPALACE"
    
    # Concurrency
    SPIDERSPAWN = "SPIDERSPAWN"
    LOITER = "LOITER"
    CHILL = "CHILL"
    
    # Performance
    SPEEDRUN = "SPEEDRUN"
    
    # Math builtins
    GYATTAN = "GYATTAN"      # sin
    SIGMATH = "SIGMATH"      # cos
    SKULLTAN = "SKULLTAN"    # atan2
    RIZZROOT = "RIZZROOT"    # sqrt
    FANUMFLOOR = "FANUMFLOOR" # floor
    CLAMPOUT = "CLAMPOUT"    # clamp
    GOONMIN = "GOONMIN"      # min
    GOONMAX = "GOONMAX"      # max
    
    # Time
    CLOCKED = "CLOCKED"
    SNOOZE = "SNOOZE"
    
    # Strings
    MIX = "MIX"
    STRINGIFY = "STRINGIFY"
    LEN = "LEN"
    SPLIT = "SPLIT"
    JOIN = "JOIN"
    SLICE = "SLICE"
    
    # Files
    READDROP = "READDROP"
    SPITFILE = "SPITFILE"
    APPENDFILE = "APPENDFILE"
    LISTUP = "LISTUP"
    MAKEHOUSE = "MAKEHOUSE"
    NUKEFILE = "NUKEFILE"
    NUKEHOUSE = "NUKEHOUSE"
    STATS = "STATS"
    
    # Paths
    GYATTPATH = "GYATTPATH"
    WHERE_AM_I = "WHERE AM I"
    TP = "TP"
    RIZZHOME = "RIZZHOME"
    SKIBIDITEMP = "SKIBIDITEMP"
    
    # Processes
    GYATTARGS = "GYATTARGS"
    GYATTENV = "GYATTENV"
    DROP_NPC = "DROP NPC"
    DROP_SHELL = "DROP SHELL"
    DIPSET = "DIPSET"
    
    # Platform
    PLATFORMGYATT = "PLATFORMGYATT"
    CANCOOK = "CANCOOK"
    
    # Input
    KEYS_DOWN = "KEYS DOWN"
    TOILET_CHECK = "TOILET CHECK"
    
    # RNG
    HOLY_67 = "67"
    FROM = "FROM"
    TO = "TO"
    
    # Literals
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    
    # Special
    EQUALS = "="
    SEMICOLON = ";"
    COMMA = ","
    COLON = ":"
    DOT = "."
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    
    # Comments
    COMMENT_LINE = "//"
    COMMENT_BLOCK_START = "/*"
    COMMENT_BLOCK_END = "*/"

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class BrainrotError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0):
        super().__init__(f"YOU FELL OFF: {message}")
        self.message = message
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1
        self.column = 1
        self.debug_mode = False
        
        # Multi-word keywords
        self.keywords = {
            "dev energy": TokenType.DEV_ENERGY,
            "no cap": TokenType.NO_CAP,
            "debug mode": TokenType.DEBUG_MODE,
            "hyperskoom": TokenType.HYPERSKOOM,
            "profile on": TokenType.PROFILE_ON,
            "profile off": TokenType.PROFILE_OFF,
            "fanumtax": TokenType.FANUMTAX,
            "return": TokenType.RETURN,
            "rizz": TokenType.RIZZ,
            "no rizz": TokenType.NO_RIZZ,
            "skibidi": TokenType.SKIBIDI,
            "lock in": TokenType.LOCK_IN,
            "it's over": TokenType.ITS_OVER,
            "its over": TokenType.ITS_OVER,  # Alternative spelling
            "cook": TokenType.COOK,
            "using": TokenType.USING,
            "and": TokenType.AND,
            "pull up": TokenType.PULL_UP,
            "with": TokenType.WITH,
            "gyatt": TokenType.GYATT,
            "npc": TokenType.NPC,
            "is": TokenType.IS,
            "cooked": TokenType.COOKED,
            "gyattier": TokenType.GYATTIER,
            "in": TokenType.IN,
            "open rizzport": TokenType.OPEN_RIZZPORT,
            "spawn pixels": TokenType.SPAWN_PIXELS,
            "spawn bytes": TokenType.SPAWN_BYTES,
            "drop pixel": TokenType.DROP_PIXEL,
            "put px": TokenType.PUT_PX,
            "get px": TokenType.GET_PX,
            "blit pixels": TokenType.BLIT_PIXELS,
            "wipe": TokenType.WIPE,
            "showtime": TokenType.SHOWTIME,
            "lockoff": TokenType.LOCKOFF,
            "pack rgba": TokenType.PACK_RGBA,
            "unpack rgba": TokenType.UNPACK_RGBA,
            "at2d": TokenType.AT2D,
            "write ppm": TokenType.WRITE_PPM,
            "read ppm": TokenType.READ_PPM,
            "yeet": TokenType.YEET,
            "cleanup": TokenType.CLEANUP,
            "sniff": TokenType.SNIFF,
            "stalk": TokenType.STALK,
            "freezeframe": TokenType.FREEZEFRAME,
            "brainleak": TokenType.BRAINLEAK,
            "mindpalace": TokenType.MINDPALACE,
            "spiderspawn": TokenType.SPIDERSPAWN,
            "loiter": TokenType.LOITER,
            "chill": TokenType.CHILL,
            "speedrun": TokenType.SPEEDRUN,
            "gyattan": TokenType.GYATTAN,
            "sigmath": TokenType.SIGMATH,
            "skulltan": TokenType.SKULLTAN,
            "rizzroot": TokenType.RIZZROOT,
            "fanumfloor": TokenType.FANUMFLOOR,
            "clampout": TokenType.CLAMPOUT,
            "goonmin": TokenType.GOONMIN,
            "goonmax": TokenType.GOONMAX,
            "clocked": TokenType.CLOCKED,
            "snooze": TokenType.SNOOZE,
            "mix": TokenType.MIX,
            "stringify": TokenType.STRINGIFY,
            "len": TokenType.LEN,
            "split": TokenType.SPLIT,
            "join": TokenType.JOIN,
            "slice": TokenType.SLICE,
            "readdrop": TokenType.READDROP,
            "spitfile": TokenType.SPITFILE,
            "appendfile": TokenType.APPENDFILE,
            "listup": TokenType.LISTUP,
            "makehouse": TokenType.MAKEHOUSE,
            "nukefile": TokenType.NUKEFILE,
            "nukehouse": TokenType.NUKEHOUSE,
            "stats": TokenType.STATS,
            "gyattpath": TokenType.GYATTPATH,
            "where am i": TokenType.WHERE_AM_I,
            "tp": TokenType.TP,
            "rizzhome": TokenType.RIZZHOME,
            "skibiditemp": TokenType.SKIBIDITEMP,
            "gyattargs": TokenType.GYATTARGS,
            "gyattenv": TokenType.GYATTENV,
            "drop npc": TokenType.DROP_NPC,
            "drop shell": TokenType.DROP_SHELL,
            "dipset": TokenType.DIPSET,
            "platformgyatt": TokenType.PLATFORMGYATT,
            "cancook": TokenType.CANCOOK,
            "keys down": TokenType.KEYS_DOWN,
            "toilet check": TokenType.TOILET_CHECK,
            "from": TokenType.FROM,
            "to": TokenType.TO,
        }
        
        # Single character operators
        self.operators = {
            "💀": TokenType.ADD,
            "😭": TokenType.SUB,
            "🔥": TokenType.MUL,
            "🗿": TokenType.DIV,
            "📉": TokenType.MOD,
            "🙏": TokenType.POW,
            "=": TokenType.EQUALS,
            ";": TokenType.SEMICOLON,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
            ".": TokenType.DOT,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "[": TokenType.LBRACKET,
            "]": TokenType.RBRACKET,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
        }
        
        # Aliases for emoji operators
        self.aliases = {
            "skull": "💀",
            "crying": "😭",
            "fire": "🔥",
            "moai": "🗿",
            "chart": "📉",
            "pray": "🙏",
        }

    def tokenize(self) -> List[Token]:
        """Main tokenization loop"""
        while not self.is_at_end():
            self.scan_token()
        
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def peek(self, offset: int = 0) -> str:
        pos = self.current + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def scan_token(self):
        char = self.advance()
        
        # Skip whitespace
        if char in ' \t\r\n':
            return
        
        # Comments
        if char == '/' and self.peek() == '/':
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
            return
        
        if char == '/' and self.peek() == '*':
            while not self.is_at_end():
                if self.peek() == '*' and self.peek(1) == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                self.advance()
            return
        
        # Special fence tokens
        if char == '💀':
            if self.peek() == '💀' and self.peek(1) == '💀':
                # Found 💀💀💀
                self.advance()  # Second 💀
                self.advance()  # Third 💀
                # Check if we've seen a fence before
                fence_count = sum(1 for token in self.tokens if token.type == TokenType.FENCE_START)
                if fence_count == 0:
                    self.add_token(TokenType.FENCE_START)
                else:
                    self.add_token(TokenType.FENCE_END)
                return
        
        # Single character operators
        if char in self.operators:
            self.add_token(self.operators[char], char)
            return
        
        # Numbers
        if char.isdigit() or char == '.':
            self.number()
            return
        
        # Strings
        if char in ['"', "'"]:
            self.string(char)
            return
        
        # Identifiers and keywords
        if char.isalpha() or char == '_':
            self.identifier()
            return
        
        # Unknown character
        if self.debug_mode:
            raise BrainrotError(f"Unexpected character '{char}'", self.line, self.column)

    def number(self):
        """Parse number literals"""
        start = self.current - 1
        is_float = False
        
        # Handle different number formats
        if self.peek(-1) == '0':
            if self.peek().lower() == 'x':
                # Hex: 0x69
                self.advance()  # x
                while self.peek().isalnum():
                    self.advance()
                hex_str = self.source[start:self.current]
                try:
                    value = int(hex_str, 16)
                    self.add_token(TokenType.NUMBER, value)
                    return
                except ValueError:
                    raise BrainrotError(f"Invalid hex number: {hex_str}", self.line, self.column)
            elif self.peek().lower() == 'o':
                # Octal: 0o77
                self.advance()  # o
                while self.peek().isdigit() and self.peek() in '01234567':
                    self.advance()
                oct_str = self.source[start:self.current]
                try:
                    value = int(oct_str, 8)
                    self.add_token(TokenType.NUMBER, value)
                    return
                except ValueError:
                    raise BrainrotError(f"Invalid octal number: {oct_str}", self.line, self.column)
            elif self.peek().lower() == 'b':
                # Binary: 0b1010
                self.advance()  # b
                while self.peek() in '01':
                    self.advance()
                bin_str = self.source[start:self.current]
                try:
                    value = int(bin_str, 2)
                    self.add_token(TokenType.NUMBER, value)
                    return
                except ValueError:
                    raise BrainrotError(f"Invalid binary number: {bin_str}", self.line, self.column)
        
        # Regular decimal numbers
        while self.peek().isdigit():
            self.advance()
        
        if self.peek() == '.' and self.peek(1).isdigit():
            is_float = True
            self.advance()  # .
            while self.peek().isdigit():
                self.advance()
        
        # Scientific notation
        if self.peek().lower() == 'e':
            is_float = True
            self.advance()  # e
            if self.peek() in '+-':
                self.advance()
            while self.peek().isdigit():
                self.advance()
        
        # Special values
        number_str = self.source[start:self.current]
        if number_str.upper() == 'INF':
            self.add_token(TokenType.NUMBER, float('inf'))
        elif number_str.upper() == 'NAN':
            self.add_token(TokenType.NUMBER, float('nan'))
        else:
            try:
                value = float(number_str) if is_float else int(number_str)
                self.add_token(TokenType.NUMBER, value)
            except ValueError:
                raise BrainrotError(f"Invalid number: {number_str}", self.line, self.column)

    def string(self, quote_char: str):
        """Parse string literals with escape sequences"""
        start = self.current
        value = ""
        
        while self.peek() != quote_char and not self.is_at_end():
            if self.peek() == '\\':
                self.advance()  # \
                escape_char = self.advance()
                
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == quote_char:
                    value += quote_char
                elif escape_char == 'u' and self.peek() == '{':
                    # Unicode escape: \u{1F480}
                    self.advance()  # {
                    unicode_str = ""
                    while self.peek() != '}' and not self.is_at_end():
                        unicode_str += self.advance()
                    if self.peek() == '}':
                        self.advance()  # }
                        try:
                            codepoint = int(unicode_str, 16)
                            value += chr(codepoint)
                        except ValueError:
                            raise BrainrotError(f"Invalid Unicode escape: \\u{{{unicode_str}}}", self.line, self.column)
                else:
                    value += escape_char
            else:
                value += self.advance()
        
        if self.is_at_end():
            raise BrainrotError("Unterminated string", self.line, self.column)
        
        self.advance()  # Closing quote
        self.add_token(TokenType.STRING, value)

    def identifier(self):
        """Parse identifiers and keywords"""
        start = self.current - 1
        
        # Handle multi-word keywords
        text = self.source[start:self.current]
        while (self.peek().isalnum() or self.peek() in ' _' or 
               self.peek().lower() in 'abcdefghijklmnopqrstuvwxyz'):
            self.advance()
            text = self.source[start:self.current]
            
            # Check if this is a known keyword
            if text.lower() in self.keywords:
                self.add_token(self.keywords[text.lower()])
                return
        
        # Single word identifier
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        
        text = self.source[start:self.current]
        
        # Check for aliases
        if text.lower() in self.aliases:
            self.add_token(self.operators[self.aliases[text.lower()]], self.aliases[text.lower()])
            return
        
        # Regular identifier
        self.add_token(TokenType.IDENTIFIER, text.strip())

    def add_token(self, token_type: TokenType, value: Any = None):
        self.tokens.append(Token(token_type, value, self.line, self.column))

# AST Nodes
@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class VariableDeclaration(ASTNode):
    name: str
    value: ASTNode

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Literal(ASTNode):
    value: Any

@dataclass
class Variable(ASTNode):
    name: str

@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: List[ASTNode]

@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class FunctionDefinition(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]

@dataclass
class ExecutionMode(ASTNode):
    mode: str

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.debug_mode = False

    def parse(self) -> Program:
        statements = []
        
        # Skip opening fence
        if self.match(TokenType.FENCE_START):
            pass
        
        while not self.check(TokenType.FENCE_END) and not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def peek(self) -> Token:
        if self.current >= len(self.tokens):
            return Token(TokenType.FENCE_END, None, 0, 0)
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise BrainrotError(message, self.peek().line, self.peek().column)

    def declaration(self) -> Optional[ASTNode]:
        try:
            # Check for execution modes
            if self.match(TokenType.DEV_ENERGY):
                return ExecutionMode('DEV_ENERGY')
            elif self.match(TokenType.NO_CAP):
                return ExecutionMode('NO_CAP')
            elif self.match(TokenType.DEBUG_MODE):
                return ExecutionMode('DEBUG_MODE')
            elif self.match(TokenType.HYPERSKOOM):
                return ExecutionMode('HYPERSKOOM')
            elif self.match(TokenType.PROFILE_ON):
                return ExecutionMode('PROFILE_ON')
            elif self.match(TokenType.PROFILE_OFF):
                return ExecutionMode('PROFILE_OFF')
            elif self.match(TokenType.FANUMTAX):
                return self.variable_declaration()
            return self.statement()
        except BrainrotError as e:
            if self.debug_mode:
                raise
            print(f"YOU FELL OFF: {e.message}")
            self.synchronize()
            return None

    def variable_declaration(self) -> ASTNode:
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        self.consume(TokenType.EQUALS, "Expected '=' after variable name")
        initializer = self.expression()
        return VariableDeclaration(name, initializer)

    def statement(self) -> ASTNode:
        if self.match(TokenType.GYATT):
            return self.print_statement()
        elif self.match(TokenType.RIZZ):
            return self.if_statement()
        elif self.match(TokenType.NO_RIZZ):
            return self.else_statement()
        elif self.match(TokenType.SKIBIDI):
            return self.while_statement()
        elif self.match(TokenType.LOCK_IN):
            return self.block_statement()
        elif self.check(TokenType.IDENTIFIER) and self.check_next(TokenType.EQUALS):
            return self.assignment()
        elif self.check(TokenType.IDENTIFIER):
            return self.expression_statement()
        else:
            return self.expression_statement()

    def print_statement(self) -> ASTNode:
        value = self.expression()
        return PrintStatement(value)

    def if_statement(self) -> ASTNode:
        condition = self.expression()
        self.consume(TokenType.LOCK_IN, "Expected 'LOCK IN' after if condition")
        then_branch = self.block()
        else_branch = []
        
        if self.match(TokenType.NO_RIZZ):
            self.consume(TokenType.LOCK_IN, "Expected 'LOCK IN' after else")
            else_branch = self.block()
        
        self.consume(TokenType.ITS_OVER, "Expected 'IT'S OVER' after if statement")
        return IfStatement(condition, then_branch, else_branch)

    def else_statement(self) -> ASTNode:
        # This is handled in if_statement
        raise BrainrotError("Unexpected 'NO RIZZ' without matching 'RIZZ'", self.peek().line, self.peek().column)

    def while_statement(self) -> ASTNode:
        condition = self.expression()
        self.consume(TokenType.LOCK_IN, "Expected 'LOCK IN' after while condition")
        body = self.block()
        self.consume(TokenType.ITS_OVER, "Expected 'IT'S OVER' after while statement")
        return WhileStatement(condition, body)

    def block_statement(self) -> ASTNode:
        return self.block()

    def block(self) -> List[ASTNode]:
        statements = []
        
        while not self.check(TokenType.ITS_OVER) and not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        
        return statements

    def assignment(self) -> ASTNode:
        name = self.advance().value
        self.advance()  # consume '='
        value = self.expression()
        return Assignment(name, value)

    def expression_statement(self) -> ASTNode:
        expr = self.expression()
        return expr

    def expression(self) -> ASTNode:
        return self.equality()

    def equality(self) -> ASTNode:
        expr = self.comparison()
        
        while self.match(TokenType.IS, TokenType.COOKED):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryOp(expr, operator.type.value, right)
        
        return expr

    def comparison(self) -> ASTNode:
        expr = self.term()
        
        while self.match(TokenType.GYATTIER, TokenType.LESS_THAN):
            operator = self.previous()
            right = self.term()
            expr = BinaryOp(expr, operator.type.value, right)
        
        return expr

    def term(self) -> ASTNode:
        expr = self.factor()
        
        while self.match(TokenType.ADD, TokenType.SUB):
            operator = self.previous()
            right = self.factor()
            expr = BinaryOp(expr, operator.type.value, right)
        
        return expr

    def factor(self) -> ASTNode:
        expr = self.unary()
        
        while self.match(TokenType.MUL, TokenType.DIV, TokenType.MOD):
            operator = self.previous()
            right = self.unary()
            expr = BinaryOp(expr, operator.type.value, right)
        
        return expr

    def unary(self) -> ASTNode:
        if self.match(TokenType.SUB):
            operator = self.previous()
            right = self.unary()
            return UnaryOp(operator.type.value, right)
        
        return self.primary()

    def primary(self) -> ASTNode:
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().value)
        
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous().value)
        
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        raise BrainrotError(f"Unexpected token: {self.peek().type.value}", self.peek().line, self.peek().column)

    def check_next(self, token_type: TokenType) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type

    def synchronize(self):
        """Error recovery - skip to next statement"""
        self.advance()
        
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            if self.peek().type in [TokenType.FANUMTAX, TokenType.GYATT, TokenType.RIZZ, 
                                   TokenType.SKIBIDI, TokenType.LOCK_IN]:
                return
            
            self.advance()

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
        
        # Built-in functions
        self.builtins = {
            'GYATTAN': lambda x: math.sin(x),
            'SIGMATH': lambda x: math.cos(x),
            'SKULLTAN': lambda y, x: math.atan2(y, x),
            'RIZZROOT': lambda x: math.sqrt(x),
            'FANUMFLOOR': lambda x: math.floor(x),
            'CLAMPOUT': lambda x, a, b: max(a, min(b, x)),
            'GOONMIN': lambda a, b: min(a, b),
            'GOONMAX': lambda a, b: max(a, b),
            'CLOCKED': lambda: time.time(),
            'STRINGIFY': lambda x: str(x),
            'LEN': lambda x: len(str(x)),
            'PLATFORMGYATT': lambda: self.get_platform(),
        }

    def get_platform(self) -> str:
        """Get current platform"""
        import platform
        system = platform.system().lower()
        if system == 'windows':
            return 'windows'
        elif system == 'linux':
            return 'linux'
        elif system == 'darwin':
            return 'macos'
        else:
            return 'unknown'

    def interpret(self, program: Program):
        """Main interpretation loop"""
        try:
            # Process execution modes first
            for statement in program.statements:
                if isinstance(statement, ExecutionMode):
                    self.process_execution_mode(statement)
            
            # Execute statements (skip execution modes)
            for statement in program.statements:
                if not isinstance(statement, ExecutionMode):
                    self.execute(statement)
        except BrainrotError as e:
            if self.debug_mode:
                raise
            print(f"YOU FELL OFF: {e.message}")
    
    def process_execution_mode(self, stmt: ExecutionMode):
        """Process execution mode declarations"""
        if stmt.mode == 'DEV_ENERGY':
            self.dev_energy = True
        elif stmt.mode == 'NO_CAP':
            self.no_cap = True
        elif stmt.mode == 'DEBUG_MODE':
            self.debug_mode = True
        elif stmt.mode == 'HYPERSKOOM':
            self.hyperskoom = True
        elif stmt.mode == 'PROFILE_ON':
            self.profile_on = True
        elif stmt.mode == 'PROFILE_OFF':
            self.profile_on = False

    def execute(self, stmt: ASTNode):
        """Execute a statement"""
        if isinstance(stmt, ExecutionMode):
            # Already processed in interpret()
            pass
        elif isinstance(stmt, VariableDeclaration):
            self.declare_variable(stmt.name, self.evaluate(stmt.value))
        elif isinstance(stmt, Assignment):
            self.assign_variable(stmt.name, self.evaluate(stmt.value))
        elif isinstance(stmt, PrintStatement):
            self.print_value(self.evaluate(stmt.expression))
        elif isinstance(stmt, IfStatement):
            self.execute_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self.execute_while(stmt)
        else:
            self.evaluate(stmt)

    def evaluate(self, expr: ASTNode) -> Any:
        """Evaluate an expression"""
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Variable):
            return self.get_variable(expr.name)
        elif isinstance(expr, BinaryOp):
            return self.evaluate_binary(expr)
        elif isinstance(expr, UnaryOp):
            return self.evaluate_unary(expr)
        else:
            return None

    def evaluate_binary(self, expr: BinaryOp) -> Any:
        """Evaluate binary operations"""
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator == TokenType.ADD.value:  # 💀
            return left + right
        elif expr.operator == TokenType.SUB.value:  # 😭
            return left - right
        elif expr.operator == TokenType.MUL.value:  # 🔥
            return left * right
        elif expr.operator == TokenType.DIV.value:  # 🗿
            return int(left // right) if isinstance(left, int) and isinstance(right, int) else left / right
        elif expr.operator == TokenType.MOD.value:  # 📉
            return left % right
        elif expr.operator == TokenType.POW.value:  # 🙏
            return left ** right
        elif expr.operator == TokenType.IS.value:
            return left == right
        elif expr.operator == TokenType.COOKED.value:
            return left != right
        elif expr.operator == TokenType.GYATTIER.value:
            return left > right
        elif expr.operator == TokenType.LESS_THAN.value:
            return left < right
        
        return None

    def evaluate_unary(self, expr: UnaryOp) -> Any:
        """Evaluate unary operations"""
        operand = self.evaluate(expr.operand)
        
        if expr.operator == TokenType.SUB.value:  # 😭
            return -operand
        
        return operand

    def declare_variable(self, name: str, value: Any):
        """Declare a new variable"""
        if name in self.braincells:
            self.braincells[name] = value
            self.usage_count[name] = 0
        else:
            raise BrainrotError(f"Unknown braincell: {name}")

    def assign_variable(self, name: str, value: Any):
        """Assign to existing variable"""
        if name in self.braincells:
            self.braincells[name] = value
            if not self.dev_energy:
                self.usage_count[name] += 1
        else:
            raise BrainrotError(f"Unknown braincell: {name}")

    def get_variable(self, name: str) -> Any:
        """Get variable value with decay check"""
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

    def execute_if(self, stmt: IfStatement):
        """Execute if statement"""
        condition = self.evaluate(stmt.condition)
        if condition:
            for statement in stmt.then_branch:
                self.execute(statement)
        else:
            for statement in stmt.else_branch:
                self.execute(statement)

    def execute_while(self, stmt: WhileStatement):
        """Execute while loop"""
        while self.evaluate(stmt.condition):
            for statement in stmt.body:
                self.execute(statement)

def run_brainrot(source: str, debug: bool = False):
    """Run Brainrot code"""
    try:
        # Lex
        lexer = Lexer(source)
        lexer.debug_mode = debug
        tokens = lexer.tokenize()
        
        if debug:
            print("Tokens parsed successfully")
            print()
        
        # Parse
        parser = Parser(tokens)
        parser.debug_mode = debug
        program = parser.parse()
        
        if debug:
            print("Parsed program successfully")
            print()
        
        # Interpret
        interpreter = Interpreter()
        interpreter.debug_mode = debug
        if debug:
            print(f"Program has {len(program.statements)} statements")
        interpreter.interpret(program)
        
    except Exception as e:
        if debug:
            raise
        print(f"YOU FELL OFF: {e}")

if __name__ == "__main__":
    # Test the interpreter with simple code first
    try:
        with open('test_simple.brainrot', 'r', encoding='utf-8') as f:
            test_code = f.read()
        
        print("Brainrot Lang Interpreter Test")
        print("=" * 50)
        run_brainrot(test_code, debug=True)
    except FileNotFoundError:
        print("test_simple.brainrot not found, running basic test")
        # Simple test without emojis
        test_code = '''
💀💀💀
DEV ENERGY
NO CAP
FANUMTAX sigma = 42
GYATT sigma
💀💀💀
'''
        run_brainrot(test_code, debug=False)
    
    print("\n" + "=" * 50)
    print("Testing gaslighting (without DEV ENERGY):")
    
    gaslight_test = '''
💀💀💀
NO CAP
FANUMTAX sigma = 69
GYATT "First print"
GYATT "Second print" 
GYATT "Third print - should be gaslit"
💀💀💀
'''
    
    run_brainrot(gaslight_test)
    
    print("\n" + "=" * 50)
    print("Testing variable decay:")
    
    decay_test = '''
💀💀💀
NO CAP
FANUMTAX sigma = 420
GYATT sigma
GYATT sigma
GYATT sigma
GYATT sigma  // This should fail - cooked!
💀💀💀
'''
    
    run_brainrot(decay_test)
