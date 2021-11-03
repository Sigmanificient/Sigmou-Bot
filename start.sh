# Git sync
if [[ -d .git ]]; then
  git pull

fi

# Setup environment
if ! [[ -d venv ]]; then
  python -m venv venv

  # Installing dependencies
  venv/bin/pip install -U --target ./venv/lib/python3.*/site-packages/ -r requirements.txt
fi


# Installing bot as package
venv/bin/pip install -e .

# Starting the bot
venv/bin/python ./sigmou/__main__.py
