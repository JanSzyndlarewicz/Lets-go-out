# Flask Project

## Setup

### 1. Create a virtual environment

First, create a virtual environment using `venv` in your project directory. This example assumes you are using WSL (Windows Subsystem for Linux).

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment
Activate the virtual environment. The command depends on the shell you are using.  For bash or zsh:
```bash
source .venv/bin/activate
```

### 3. Install the requirements
Install the requirements using `pip`.

```bash
pip install -r requirements.txt
```

## Running the Application
1. Start the Flask server
Run the Flask application using the following command:
```bash
python app.py
```

The server will start, and you can access it at http://127.0.0.1:5000/.

