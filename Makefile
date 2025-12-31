PHONY: venv install run


# Create a virtual environment
venv:
	@echo "Creating virtual environment"
	python3 -m venv venv
	@echo "Virtual environment created."

# Install dependencies from requirements.txt
install:
	@echo "Installing Dependencies"
	venv/bin/python3 -m pip install -r requirements.txt
	@echo "Dependencies installed."

# Run the Python script
run:
	cd backend && ../venv/bin/python3 main.py

serve:
	cd backend && ../venv/bin/uvicorn main:app --reload

