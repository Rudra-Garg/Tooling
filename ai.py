#!/usr/bin/env python3
import os
import argparse
import dotenv
from google import genai
from google.genai import types
import re  # For markdown formatting
import threading
import time
import sys

dotenv.load_dotenv()

# ─────────────── Config ───────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

# ─────────────── Color Codes ───────────────
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# ─────────────── Markdown Formatting ───────────────
def format_markdown(text):
    """Format markdown text for terminal display."""
    # Handle code blocks first (they need special treatment)
    # Match fenced code blocks with language specification
    code_block_pattern = r'```(?:\w+)?\n(.*?)```'
    code_blocks = re.findall(code_block_pattern, text, re.DOTALL)
    
    # Replace code blocks with placeholders
    placeholder_map = {}
    for i, block in enumerate(code_blocks):
        placeholder = f"__CODE_BLOCK_{i}__"
        placeholder_map[placeholder] = f"{MAGENTA}{block}{RESET}"
        text = text.replace(f"```{block}```", placeholder, 1)
    
    # Headers
    text = re.sub(r'^# (.*?)$', f"{BOLD}{BLUE}\\1{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', f"{BOLD}{CYAN}\\1{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', f"{BOLD}{GREEN}\\1{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.*?)$', f"{BOLD}{YELLOW}\\1{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^##### (.*?)$', f"{BOLD}{MAGENTA}\\1{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^###### (.*?)$', f"{BOLD}{WHITE}\\1{RESET}", text, flags=re.MULTILINE)
    
    # Bold and Italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', f"{BOLD}{YELLOW}\\1{RESET}", text)
    text = re.sub(r'___(.+?)___', f"{BOLD}{YELLOW}\\1{RESET}", text)
    text = re.sub(r'\*\*(.*?)\*\*', f"{BOLD}\\1{RESET}", text)
    text = re.sub(r'__(.+?)__', f"{BOLD}\\1{RESET}", text)
    text = re.sub(r'\*(.*?)\*', f"{YELLOW}\\1{RESET}", text)
    text = re.sub(r'_(.+?)_', f"{YELLOW}\\1{RESET}", text)
    
    # Strikethrough
    text = re.sub(r'~~(.*?)~~', f"{RED}\\1{RESET}", text)
    
    # Lists
    text = re.sub(r'^- (.*?)$', f"{CYAN}•{RESET} \\1", text, flags=re.MULTILINE)
    text = re.sub(r'^\* (.*?)$', f"{CYAN}•{RESET} \\1", text, flags=re.MULTILINE)
    text = re.sub(r'^\+ (.*?)$', f"{CYAN}•{RESET} \\1", text, flags=re.MULTILINE)
    text = re.sub(r'^(\d+)\. (.*?)$', f"{CYAN}\\1.{RESET} \\2", text, flags=re.MULTILINE)
    
    # Blockquotes
    text = re.sub(r'^> (.*?)$', f"{GREEN}│{RESET} \\1", text, flags=re.MULTILINE)
    
    # Horizontal rules
    text = re.sub(r'^---+$', f"{CYAN}{'─' * 50}{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*+$', f"{CYAN}{'─' * 50}{RESET}", text, flags=re.MULTILINE)
    text = re.sub(r'^___+$', f"{CYAN}{'─' * 50}{RESET}", text, flags=re.MULTILINE)
    
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', f"{BLUE}\\1{RESET} ({CYAN}\\2{RESET})", text)
    
    # Inline code (after other formatting to avoid conflicts)
    text = re.sub(r'`(.*?)`', f"{MAGENTA}\\1{RESET}", text)
    
    # Restore code blocks
    for placeholder, content in placeholder_map.items():
        text = text.replace(placeholder, content)
    
    return text

# ─────────────── Loading Animation ───────────────
def _animate_loading():
    """Display a loading animation in the terminal."""
    animation = "|/-\\"
    idx = 0
    while True:
        sys.stdout.write(f"\r{CYAN}Thinking {animation[idx % len(animation)]}{RESET}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

def ask_gemini(question_text):
    """Send a question to Gemini and stream back the answer."""
    if not GEMINI_API_KEY:
        print(f"{RED}Error: GEMINI_API_KEY environment variable not set.{RESET}")
        print("Please set this environment variable with your API key.")
        return None
    
    try:
        # Start the loading animation in a separate thread
        stop_animation = threading.Event()
        animation_thread = threading.Thread(
            target=lambda: _animate_loading_wrapper(stop_animation)
        )
        animation_thread.daemon = True
        animation_thread.start()
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=question_text)],
            ),
        ]
        
        # Use system_instruction in the config instead of as a content item
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="You are an AI assistant. For every input, output only the direct answer in plain text. Do not include greetings, restatements, explanations, or any additional formatting or jargon—just the answer itself. If the user explicitly asks for explanations, reasoning, or additional context, provide them accordingly."),
            ],
        )
        
        response_chunks = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=contents,
            config=generate_content_config,
        )
        
        # Collect the entire response first
        full_response = ""
        for chunk in response_chunks:
            full_response += chunk.text
        
        # Stop the animation before printing the response
        stop_animation.set()
        animation_thread.join()
        sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the animation line
        
        # Format the entire response at once
        formatted_response = format_markdown(full_response)
        
        # Print the formatted response
        print()  # Add a newline before the response
        print(formatted_response)
        print()  # Add a newline after the response
        
        return full_response

    except Exception as e:
        # Make sure to stop the animation if there's an error
        if 'stop_animation' in locals() and 'animation_thread' in locals():
            stop_animation.set()
            animation_thread.join()
            sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the animation line
        
        print(f"\n{RED}Error calling Gemini API: {e}{RESET}")
        return None

def _animate_loading_wrapper(stop_event):
    """Wrapper for the animation function that checks for the stop event."""
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{CYAN}Thinking {animation[idx % len(animation)]}{RESET}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(description='Ask a question to the Gemini API.')
    parser.add_argument('question', nargs='+', help='The question to ask Gemini.')
    
    args = parser.parse_args()
    
    question_text = " ".join(args.question)
    
    if not question_text:
        print(f"{RED}Error: No question provided.{RESET}")
        parser.print_help()
        exit(1)
        
    ask_gemini(question_text)

if __name__ == "__main__":
    main()