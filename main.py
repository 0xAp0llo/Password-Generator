#!/usr/bin/env python3

import random
import string
import argparse
import json
import os
from datetime import datetime

# Constants
DEFAULT_LENGTH = 16
DEFAULT_HISTORY_FILE = "password_history.json"
MAX_HISTORY = 10

def generate_password(length=DEFAULT_LENGTH, use_uppercase=True, use_lowercase=True, 
                     use_digits=True, use_symbols=True, exclude_chars="", no_similar=False):
    """Generate a random password with specified criteria"""
    
    # Define character sets
    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    digit_chars = string.digits
    symbol_chars = string.punctuation
    
    # Remove similar characters if specified
    if no_similar:
        similar_chars = "Il1O0o"
        uppercase_chars = ''.join(c for c in uppercase_chars if c not in similar_chars)
        lowercase_chars = ''.join(c for c in lowercase_chars if c not in similar_chars)
        digit_chars = ''.join(c for c in digit_chars if c not in similar_chars)
    
    # Remove excluded characters
    for char in exclude_chars:
        uppercase_chars = uppercase_chars.replace(char, '')
        lowercase_chars = lowercase_chars.replace(char, '')
        digit_chars = digit_chars.replace(char, '')
        symbol_chars = symbol_chars.replace(char, '')
    
    # Build character pool based on options
    char_pool = ""
    if use_uppercase:
        char_pool += uppercase_chars
    if use_lowercase:
        char_pool += lowercase_chars
    if use_digits:
        char_pool += digit_chars
    if use_symbols:
        char_pool += symbol_chars
    
    # Ensure at least one character type is selected
    if not char_pool:
        print("Error: At least one character type must be enabled")
        return None
    
    # Generate password
    password = ''.join(random.choice(char_pool) for _ in range(length))
    
    # Verify the password meets the requirements
    if use_uppercase and not any(c in uppercase_chars for c in password):
        # Replace a random character with an uppercase character
        idx = random.randint(0, length - 1)
        password = password[:idx] + random.choice(uppercase_chars) + password[idx+1:]
    
    if use_lowercase and not any(c in lowercase_chars for c in password):
        # Replace a random character with a lowercase character
        idx = random.randint(0, length - 1)
        password = password[:idx] + random.choice(lowercase_chars) + password[idx+1:]
    
    if use_digits and not any(c in digit_chars for c in password):
        # Replace a random character with a digit
        idx = random.randint(0, length - 1)
        password = password[:idx] + random.choice(digit_chars) + password[idx+1:]
    
    if use_symbols and not any(c in symbol_chars for c in password):
        # Replace a random character with a symbol
        idx = random.randint(0, length - 1)
        password = password[:idx] + random.choice(symbol_chars) + password[idx+1:]
    
    return password

def calculate_entropy(password):
    """Calculate the entropy of a password in bits"""
    char_sets = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    char_pool_size = 0
    
    for char_set in char_sets:
        if any(c in char_set for c in password):
            char_pool_size += len(char_set)
    
    return len(password) * (len(password) > 0) * (char_pool_size > 0) * (
        (char_pool_size > 1) * (len(password) * (int.bit_length(char_pool_size - 1)))
    ) / 8

def estimate_strength(password):
    """Estimate the strength of a password"""
    entropy = calculate_entropy(password)
    
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"

def load_history(history_file=DEFAULT_HISTORY_FILE):
    """Load password history from file"""
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {history_file} is corrupted. Creating a new history file.")
            return []
    return []

def save_history(history, history_file=DEFAULT_HISTORY_FILE):
    """Save password history to file"""
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)

def add_to_history(password, description="", history_file=DEFAULT_HISTORY_FILE):
    """Add a password to the history file"""
    if not password:
        return
    
    history = load_history(history_file)
    
    # Add the new password to the history
    history.append({
        "password": password,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entropy": calculate_entropy(password),
        "strength": estimate_strength(password)
    })
    
    # Limit the history size
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    
    # Save the updated history
    save_history(history, history_file)

def view_history(history_file=DEFAULT_HISTORY_FILE):
    """View password generation history"""
    history = load_history(history_file)
    
    if not history:
        print("No password history found")
        return
    
    print("\n" + "="*80)
    print(f"{'Created At':<20} | {'Description':<20} | {'Strength':<12} | {'Password':<20}")
    print("="*80)
    
    for entry in history:
        # Mask the password for display
        masked_password = entry["password"][:4] + "*" * (len(entry["password"]) - 4)
        
        print(f"{entry['created_at']:<20} | {entry['description'][:20]:<20} | {entry['strength']:<12} | {masked_password:<20}")
    
    print("="*80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Generate strong random passwords")
    
    # Password generation options
    parser.add_argument("-l", "--length", type=int, default=DEFAULT_LENGTH, help=f"Password length (default: {DEFAULT_LENGTH})")
    parser.add_argument("--no-uppercase", action="store_true", help="Don't include uppercase letters")
    parser.add_argument("--no-lowercase", action="store_true", help="Don't include lowercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Don't include digits")
    parser.add_argument("--no-symbols", action="store_true", help="Don't include symbols")
    parser.add_argument("--no-similar", action="store_true", help="Don't include similar characters (Il1O0o)")
    parser.add_argument("-e", "--exclude", default="", help="Characters to exclude from the password")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate (default: 1)")
    
    # History options
    parser.add_argument("-s", "--save", action="store_true", help="Save the generated password to history")
    parser.add_argument("-d", "--description", default="", help="Description for the password (used with --save)")
    parser.add_argument("--history", action="store_true", help="View password generation history")
    parser.add_argument("--history-file", default=DEFAULT_HISTORY_FILE, help=f"History file (default: {DEFAULT_HISTORY_FILE})")
    
    args = parser.parse_args()
    
    # View history if requested
    if args.history:
        view_history(args.history_file)
        return
    
    # Generate passwords
    for i in range(args.count):
        password = generate_password(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_chars=args.exclude,
            no_similar=args.no_similar
        )
        
        if password:
            strength = estimate_strength(password)
            entropy = calculate_entropy(password)
            
            print(f"Password #{i+1}: {password}")
            print(f"Length: {len(password)} characters")
            print(f"Entropy: {entropy:.2f} bits")
            print(f"Strength: {strength}")
            
            if i < args.count - 1:
                print("-" * 40)
            
            # Save to history if requested
            if args.save:
                add_to_history(password, args.description, args.history_file)

if __name__ == "__main__":
    main()
