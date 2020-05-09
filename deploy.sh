#!/bin/sh
cd /home/malkir/scripts/telegramBot
result=$(git pull)
if [ "$result" = "2Already up-to-date." ]; then
  echo "Strings are equal."
else
  echo 'reboot'
  kill $(ps aux | grep 'bot.py' | grep -v "grep" | cut -d " " -f2)
  echo 'start'
  python3  /home/malkir/scripts/telegramBot/bot.py
fi
