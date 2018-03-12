# ==============================================================================
#
# socialw.py
#
# Converts a csv of words into a csv of words,
# Chinese translations and English definitions
#
# For the weekly vocab homework of Social Studies 11
#
# Created by carbonyl on Mon Mar 5 18:42:23 CST 2018
# Last change: Mon Mar 12 17:51:29 CST 2018
#
# Acknowledgement: ECDICT by skywind3000 (https://github.com/skywind3000/ECDICT)
#
# ==============================================================================

import sys
import time
import os
import stardict
import re

lineNum = 0
lineNumTot = 0

# ------------------------------------------------------------------------------
#
# Sample Useage:
#
# $ python3 socialw.py in.csv out.csv
#
# ------------------------------------------------------------------------------
#
# Sample Input (.csv):
#
# Kidnap
# Labour
# Legalisation
# Majority
# Manifesto
#
# ------------------------------------------------------------------------------
#
# Sample Output (.csv):
#
# Kidnap,绑架,take away to an undisclosed location against their will and usually in order to extract a ransom,
# Labour,劳动,a social class comprising those who do manual labor or work for wages,
# Legalisation,合法化,the act of making lawful,
# Majority,多数,the property resulting from being or relating to the greater in number of two parts,
# Manifesto,宣言,a public declaration of intentions ,
#
# ------------------------------------------------------------------------------


def update_progress(fin, tot):

    progress = fin/tot
    # Modify this to change the length of the progress bar
    barLength = 15
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\r{0}/{1} [{2}] {3}% {4}".format(fin, tot, "#"*block + "-"*(barLength-block), round(progress*100, 2), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def ishan(text):
    return all('\u4e00' <= char <= '\u9fff' for char in text)


def gethan(text):

    r = ""
    for c in text:
        if ishan(c):
            r += c
    return r


def exthan(texts):

    for t in texts:
        if gethan(t) != "":
            return gethan(t)
    return ""


def queryhan(word):

    sd = stardict.open_dict('sd.sqlite')
    trans = sd.query(word)['translation']
    trans = re.sub(r"[<\(\（\[].*?[\)\）\]>]", "", trans)
    trans = trans.split(";")[0]
    trans = trans.split("；")[0]
    trans = trans.split(",")[0]
    trans = trans.replace(" ", "")
    trans = trans.split("\n")[0]
    if "." in trans:
        trans = trans.split(".")[1]

    return trans


def querydef(word):

    sd = stardict.open_dict('sd.sqlite')
    defi = sd.query(word)['definition']
    defi = re.sub(r"[<\(\（\[].*?[\)\）\]>]", "", defi)
    defi = defi.split(";")[0]
    defi = defi.split("；")[0]
    defi = defi.split(",")[0]
    defi = defi.replace("  ", " ")
    defi = defi.split("\n")[0]
    if ". " in defi:
        defi = defi.split(". ")[1]
    if defi.startswith("n "):
        defi = defi[2:]
    if defi.startswith("v "):
        defi = defi[2:]
    if defi.startswith("vt "):
        defi = defi[3:]
    if defi.startswith("adj "):
        defi = defi[4:]
    if defi.startswith("adv "):
        defi = defi[4:]

    return defi


with open(sys.argv[2], "w", encoding="utf-8-sig") as out:
    with open(sys.argv[1]) as file:
        for liner in file:
            lineNumTot += 1
    with open(sys.argv[1]) as file:
        for line in file:
            lineNum += 1
            word = line.replace("\n", "")
            if ". " in word:
                # If the words are number listed, remove the number, e.g. "1. Apple" -> "Apple"
                word = word.split(". ")[1]
            out.write(word+"," + queryhan(word) + "," + querydef(word) + ",\n")
            update_progress(lineNum, lineNumTot)
            # print(word+","+queryhan(word))
            # print(word+","+querydef(word))
