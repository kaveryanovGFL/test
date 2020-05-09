#!/bin/sh
cd /home/malkir/scripts/telegramBot
result=$(git pull)
if [ "$result" = "2Already up-to-date." ]; then
    echo "Strings are equal."
else
    program=$(bot.py &)
    kill "$program"
    python3  /home/malkir/scripts/telegramBot/bot.py
fi
