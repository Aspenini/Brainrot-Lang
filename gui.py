#!/usr/bin/env python3
"""
Brainrot Lang GUI Interpreter
A graphical interface for running Brainrot programs
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import io
from pathlib import Path
from interpreter import run, BrainrotError

try:
    import emoji  # type: ignore
    EMOJI_SUPPORT = True
except ImportError:
    EMOJI_SUPPORT = False
    print("Warning: emoji module not installed. Install with: pip install emoji")

class BrainrotGUI:
    def __init__(self, root):
        self.root = root
        
        # Use emoji module for proper rendering if available
        if EMOJI_SUPPORT:
            brain = emoji.emojize(":brain:")
            title = f"{brain} Brainrot Lang - GUI Interpreter"
        else:
            title = "🧠 Brainrot Lang - GUI Interpreter"
        
        self.root.title(title)
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure colors
        self.bg_dark = "#0f1115"
        self.panel_bg = "#161922"
        self.text_color = "#e6e6e6"
        self.muted_color = "#9aa4b2"
        self.accent_color = "#8b5cf6"
        self.good_color = "#22c55e"
        self.bad_color = "#ef4444"
        
        # Configure root style
        self.root.configure(bg=self.bg_dark)
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_dark)
        self.style.configure('TLabel', background=self.bg_dark, foreground=self.text_color, font=('Segoe UI Emoji', 10))
        self.style.configure('Title.TLabel', font=('Segoe UI Emoji', 16, 'bold'), foreground=self.accent_color)
        self.style.configure('TButton', 
                           background=self.panel_bg, 
                           foreground=self.text_color,
                           borderwidth=1,
                           relief='flat',
                           font=('Segoe UI Emoji', 10))
        self.style.map('TButton',
                      background=[('active', '#2a2f3f')],
                      foreground=[('active', self.text_color)])
        self.style.configure('Accent.TButton',
                           background=self.accent_color,
                           foreground='white',
                           font=('Segoe UI Emoji', 10, 'bold'))
        self.style.map('Accent.TButton',
                      background=[('active', '#7c5cfc')])
        
        self.current_file = None
        
        # Emoji mappings for better display
        if EMOJI_SUPPORT:
            self.emojis = {
                'brain': emoji.emojize(':brain:'),
                'skull': emoji.emojize(':skull:'),
                'sob': emoji.emojize(':loudly_crying_face:'),
                'smirk': emoji.emojize(':smirking_face:'),
                'tram': emoji.emojize(':aerial_tramway:'),
                'fire': emoji.emojize(':fire:'),
                'folder': emoji.emojize(':file_folder:'),
                'save': emoji.emojize(':floppy_disk:'),
                'trash': emoji.emojize(':wastebasket:'),
                'memo': emoji.emojize(':memo:'),
                'play': emoji.emojize(':play_button:'),
                'x': emoji.emojize(':cross_mark:'),
                'check': emoji.emojize(':check_mark_button:'),
            }
        else:
            self.emojis = {
                'brain': '🧠',
                'skull': '💀',
                'sob': '😭',
                'smirk': '😏',
                'tram': '🚡',
                'fire': '🔥',
                'folder': '📁',
                'save': '💾',
                'trash': '🗑',
                'memo': '📝',
                'play': '▶',
                'x': '❌',
                'check': '✓',
            }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text=f"{self.emojis['brain']} Brainrot Lang", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        ops_text = f"Ops: {self.emojis['skull']} {self.emojis['sob']} {self.emojis['smirk']} {self.emojis['tram']} | Cells: aura, peak, goon, mog, npc, sigma, gyatt"
        info_label = ttk.Label(header_frame, 
                              text=ops_text,
                              foreground=self.muted_color)
        info_label.pack(side=tk.RIGHT, padx=10)
        
        # Content area - split into left (editor) and right (output)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Editor
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        editor_label = ttk.Label(left_frame, text="Code Editor", font=('Segoe UI', 11, 'bold'))
        editor_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Code editor with custom styling
        editor_frame = tk.Frame(left_frame, bg=self.panel_bg, relief=tk.FLAT, borderwidth=2)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        self.code_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=('Segoe UI Emoji', 11),
            bg='#0f1320',
            fg=self.text_color,
            insertbackground=self.text_color,
            selectbackground=self.accent_color,
            selectforeground='white',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar = ttk.Frame(left_frame)
        toolbar.pack(fill=tk.X, pady=(10, 0))
        
        self.run_btn = ttk.Button(toolbar, text=f"{self.emojis['play']} Run", command=self.run_code, style='Accent.TButton')
        self.run_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.load_btn = ttk.Button(toolbar, text=f"{self.emojis['folder']} Load File", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_btn = ttk.Button(toolbar, text=f"{self.emojis['save']} Save File", command=self.save_file)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(toolbar, text=f"{self.emojis['trash']} Clear", command=self.clear_editor)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.sample_btn = ttk.Button(toolbar, text=f"{self.emojis['memo']} Sample", command=self.load_sample_code)
        self.sample_btn.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(toolbar, text="Ready", foreground=self.muted_color)
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Right panel - Output
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        output_label = ttk.Label(right_frame, text="Output", font=('Segoe UI', 11, 'bold'))
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Output area with custom styling
        output_frame = tk.Frame(right_frame, bg=self.panel_bg, relief=tk.FLAT, borderwidth=2)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=('Segoe UI Emoji', 10),
            bg='#0a0d16',
            fg=self.text_color,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.output_area.tag_config('error', foreground=self.bad_color)
        self.output_area.tag_config('success', foreground=self.good_color)
        self.output_area.tag_config('info', foreground=self.muted_color)
        
        # Output toolbar
        output_toolbar = ttk.Frame(right_frame)
        output_toolbar.pack(fill=tk.X, pady=(10, 0))
        
        self.clear_output_btn = ttk.Button(output_toolbar, text="Clear Output", command=self.clear_output)
        self.clear_output_btn.pack(side=tk.LEFT)
        
        # Keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.run_code())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<F5>', lambda e: self.run_code())
        
        # Load default sample code after all UI is created
        self.load_sample_code()
        
    def load_sample_code(self):
        """Load a sample Brainrot program"""
        if EMOJI_SUPPORT:
            sample = f"""LOCK IN
{emoji.emojize(':middle_finger:')} Welcome to Brainrot Lang!
FANUMTAX gyatt FR 5
SKIBIDI gyatt
  SAY gyatt
  FANUMTAX gyatt FR gyatt {self.emojis['sob']} 1
RIZZUP

FANUMTAX aura FR "Hello"
FANUMTAX goon FR " World!"
FANUMTAX sigma FR aura {self.emojis['skull']} goon
SAY sigma

FANUMTAX npc FR 0
ONGOD npc
  SAY "npc is nonzero"
NO CAP
  SAY "npc is zero"
DEADASS
ITS OVER"""
        else:
            sample = """LOCK IN
🖕 Welcome to Brainrot Lang!
FANUMTAX gyatt FR 5
SKIBIDI gyatt
  SAY gyatt
  FANUMTAX gyatt FR gyatt 😭 1
RIZZUP

FANUMTAX aura FR "Hello"
FANUMTAX goon FR " World!"
FANUMTAX sigma FR aura 💀 goon
SAY sigma

FANUMTAX npc FR 0
ONGOD npc
  SAY "npc is nonzero"
NO CAP
  SAY "npc is zero"
DEADASS
ITS OVER"""
        self.code_editor.delete(1.0, tk.END)
        self.code_editor.insert(1.0, sample)
        self.current_file = None
        self.update_status("Sample code loaded", "info")
        
    def clear_editor(self):
        """Clear the code editor"""
        if messagebox.askyesno("Clear Editor", "Are you sure you want to clear the editor?"):
            self.code_editor.delete(1.0, tk.END)
            self.current_file = None
            self.update_status("Editor cleared", "info")
            
    def clear_output(self):
        """Clear the output area"""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state=tk.DISABLED)
        
    def load_file(self):
        """Load a Brainrot file"""
        filename = filedialog.askopenfilename(
            title="Open Brainrot File",
            filetypes=[("Brainrot Files", "*.brainrot"), ("All Files", "*.*")],
            initialdir=Path.cwd()
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(1.0, content)
                self.current_file = filename
                self.update_status(f"Loaded: {Path(filename).name}", "success")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")
                self.update_status("Load failed", "error")
                
    def save_file(self):
        """Save the current code to a file"""
        if self.current_file:
            filename = self.current_file
        else:
            filename = filedialog.asksaveasfilename(
                title="Save Brainrot File",
                defaultextension=".brainrot",
                filetypes=[("Brainrot Files", "*.brainrot"), ("All Files", "*.*")],
                initialdir=Path.cwd()
            )
        
        if filename:
            try:
                content = self.code_editor.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.current_file = filename
                self.update_status(f"Saved: {Path(filename).name}", "success")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
                self.update_status("Save failed", "error")
                
    def run_code(self):
        """Execute the Brainrot code"""
        code = self.code_editor.get(1.0, tk.END)
        
        # Clear previous output
        self.clear_output()
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            lines = code.splitlines()
            run(lines)
            output = sys.stdout.getvalue()
            
            # Display output
            self.output_area.config(state=tk.NORMAL)
            if output:
                self.output_area.insert(tk.END, output)
            else:
                self.output_area.insert(tk.END, "(no output)\n", "info")
            self.output_area.config(state=tk.DISABLED)
            
            self.update_status(f"{self.emojis['check']} Executed successfully", "success")
            
        except BrainrotError as e:
            # Display error
            error_msg = f"{self.emojis['x']} BrainrotError:\n{str(e)}\n"
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, error_msg, "error")
            self.output_area.config(state=tk.DISABLED)
            
            self.update_status(f"{self.emojis['x']} Execution failed", "error")
            
        except Exception as e:
            # Display unexpected error
            error_msg = f"{self.emojis['x']} Unexpected Error:\n{str(e)}\n"
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, error_msg, "error")
            self.output_area.config(state=tk.DISABLED)
            
            self.update_status(f"{self.emojis['x']} Execution failed", "error")
            
        finally:
            # Restore stdout
            sys.stdout = old_stdout
            
    def update_status(self, message, status_type="info"):
        """Update the status label"""
        colors = {
            "info": self.muted_color,
            "success": self.good_color,
            "error": self.bad_color
        }
        self.status_label.config(text=message, foreground=colors.get(status_type, self.muted_color))

def main():
    root = tk.Tk()
    app = BrainrotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

