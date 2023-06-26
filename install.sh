// bash function to create a virtual environment and install the requirements for the project
function install {
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
}

// check if python3 is installed, check if pip is installed, and then check if pip freeze contains the requirements
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found"
    exit
elif ! command -v pip &> /dev/null
then
    echo "pip could not be found"
    exit
elif ! pip freeze | grep -q -F -f requirements.txt
then
    echo "requirements.txt not found"
    exit
else
    install
fi
```