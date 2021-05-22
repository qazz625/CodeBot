# CodeBot
A discord bot that uses the codeforces API to get problems or make virtual contests.

Make sure you have discord and pymongo. If you don't, you can install them using the below commands
```
pip3 install discord
pip3 install pymongo
```

1) Put all three files in the same directory.
2) In line number 5 of the codebot.py put your bot token.
3) run the bot using ```./run.sh```

Currently there are 3 commands:
1) ```;link``` to link your username to your CF account (Necessary for using the virtual contest feature)
2) ```;problem arg1 arg2``` to get a problem with rating in the range between arg1 and arg2 (inclusive)
3) ```;virtual``` to get a virtual contest based on your current CF rating.
