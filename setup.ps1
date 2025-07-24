# Create a virtual environment in 'venv' folder
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run this first Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
