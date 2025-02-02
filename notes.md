# GIT
**start using git:** git init
**ver los commits anteriores:** git log
**volver al pasado** git checkout [hash]

# GITHUB
git remote add origin https://github.com/iocariz/real-time-ml-system-cohot-1.git
git branch -M main
git push -u origin main

# POETRY

**start:** poetry new trade_producer --name src
**init** poetry install
**install libraries** poetry add
**run py** poetry run
**ruta env** poetry env info

# docker compose
**run** docker compose -f redpanda.yml up
**create image** docker build -t trade-producer .