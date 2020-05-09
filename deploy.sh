#!/bin/sh
cd /home/malkir/scripts/telegramBot
result=$(git pull)
if [ "$result" = "2Already up-to-date." ]; then
    echo "Strings are equal."
else
    pkill -f  /home/malkir/scripts/telegramBot/bot.py
    python3  /home/malkir/scripts/telegramBot/bot.py
fi
