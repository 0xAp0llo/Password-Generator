# 🔒 Password Generator

A powerful command-line password generator tool that creates strong, customizable passwords.

## ✨ Features

- 🔐 Generate strong random passwords with customizable options
- 📊 Calculate password entropy and strength estimation
- 📝 Save generated passwords with descriptions
- 📜 View password generation history
- 🚫 Exclude similar characters (Il1O0o) for better readability
- 🎛️ Control character sets (uppercase, lowercase, digits, symbols)

## 🔧 Requirements

- Python 3.6 or higher

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xAp0llo/password-generator.git
cd password-generator
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage
```bash
python main.py [options]
```

## ⚙️ Options

- `-l, --length LENGTH`: Password length (default: 16)
- `--no-uppercase`: Don't include uppercase letters
- `--no-lowercase`: Don't include lowercase letters
- `--no-digits`: Don't include digits
- `--no-symbols`: Don't include symbols
- `--no-similar`: Don't include similar characters (Il1O0o)
- `-e, --exclude CHARS`: Characters to exclude from the password
- `-c, --count COUNT`: Number of passwords to generate (default: 1)
- `-s, --save`: Save the generated password to history
- `-d, --description DESC`: Description for the password (used with --save)
- `--history`: View password generation history
- `--history-file FILE`: History file (default: password_history.json)

## 📝 Examples

### Generate a default password (16 characters with all character types):
```bash
python main.py
```

### Generate a longer password (24 characters):
```bash
python main.py -l 24
```

### Generate a PIN (digits only):
```bash
python main.py -l 6 --no-uppercase --no-lowercase --no-symbols
```

### Generate a password excluding similar characters:
```bash
python main.py --no-similar
```

### Generate multiple passwords:
```bash
python main.py -c 5
```

### Save a password to history with a description:
```bash
python main.py -s -d "Gmail account"
```

### View password history:
```bash
python main.py --history
```

## 📄 Security Notes

All passwords are stored locally in a JSON file (password_history.json by default)
Only the first 4 characters of each password are shown when viewing history
For maximum security, consider using this tool on an offline computer
The entropy calculation uses the character pool and password length

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
