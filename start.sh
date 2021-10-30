# Git sync
if [[ -d .git ]]; then
  git pull

fi

# Setup environment
if ![[ -d venv ]]; then
  python -m venv venv

  # Installing dependencies
  venv/bin/pip install -U --target /home/container/venv/lib/python3.8/site-packages/ -r requirements.txt

  # Installing bot as package
  cd /home/container/
  venv/bin/pip install -e /home/container

fi

# Starting the bot
/home/container/venv/bin/python /home/container/sigmou/__main__.py
