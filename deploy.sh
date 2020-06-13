#!/bin/sh
echo 'start pull'
cd /home/malkir/scripts/telegramBot
result=$(git pull)
if [ "$result" = "Already up-to-date." ]; then
  echo "Strings are equal."
else
  echo 'reboot'
  pkill -f bot.py
  echo 'start'
  python3  /home/malkir/scripts/telegramBot/bot.py
fi
