#!/bin/sh
cd /home/malkir/scripts/telegramBot
result=$(git pull)
if [ "$result" = "2Already up-to-date." ]; then
    echo "Strings are equal."
else
    processId=$(ps -ef | grep 'bot.py' | grep -v 'grep' | awk '{ printf $2 }')
    kill "$processId"
    python3  /home/malkir/scripts/telegramBot/bot.py
fi
