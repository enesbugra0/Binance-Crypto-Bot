from PyQt5 import uic

with open("panel.py","w",encoding="UTF-8") as fout:
    uic.compileUi("panel.ui",fout)
with open("bot.py","w",encoding="UTF-8") as fout:
    uic.compileUi("bot.ui",fout)
