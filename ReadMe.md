======================================================

Executable can be found in the dist folder

======================================================

For changing the code:

In terminal write:
    1. python -m venv .venv --- This creates new virtual environment named .venv
    2. .\.venv\Scripts\activate --- This activets the virtual environment
    3. pip install -r requirements.txt --- This installs all project requirements in this virtual environment

======================================================

Troubleshouting:

If CustomWidgets folder is empty this means that the subomdule repo isn't initialized. 
In that case in terminal write:
    git submodule --init --recursive

======================================================

If new dependencies were introduced to the project they should be saved by writing in terminal:

    pip freeze > .\requirements.txt

======================================================