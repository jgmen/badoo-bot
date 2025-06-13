# Badoo Bot

This project aims to automate tasks on the Badoo platform using Python, enhancing the user experience through automation.
# Getting Started

Follow the steps below to set up the project locally.
### 1. Install Python with pyenv

First, install Python 3.11.8 using pyenv:
```bash
pyenv install 3.11.8  # Installs Python 3.11.8
```
### 2. Create a Virtual Environment with pyenv virtualenv

Create a virtual environment named badoo_bot:

```bash
pyenv virtualenv 3.11.8 badoo_bot  # Creates a virtual environment "badoo_bot"
```

```bash
pyenv local badoo_bot # Initialize .python-version
```

```bash
pyenv activate badoo_bot  # Activate virtual environment
```

### 3. Install Dependencies

Install all required dependencies from requirements.txt:

```bash
pip install -r requirements.txt  # Installs dependencies
```

```bash
pip install -r requirements-dev.txt # Installs dev dependencies
```

```bash
python -m playwright install # Installs playwright browsers (Only supported on Ubuntu)
```
Or install chromium manually

# Reuse Your Logged-in Badoo Session

Log in to Badoo normally using your personal Chromium browser first.
Then copy the cookies file into the project’s isolated Chromium profile to reuse your session:

```bash
rsync -av --progress ~/.config/chromium/Default/Cookies .config/chromium/Default/
```

# Run the project
```bash
make run
```
