#-----------------------------------------------------------------------------
# press-stitch.py
# Merges the three Press Switch games together
# pylint: disable=bad-indentation
#-----------------------------------------------------------------------------

import getopt
import hashlib
import os.path
import pathlib
import shutil
import sys
import csv
import copy
import zipfile
import press_stitch_archive
import rpp
from maps import backgrounds_map

# Mappings for 0.3 -> 0.5
from maps import character_map_35_chris
from maps import character_map_35_ciel
from maps import character_map_35_eliza
from maps import character_map_35_karyn
from maps import character_map_35_main
from maps import character_map_35_martha
from maps import character_map_35_michelle
from maps import character_map_35_mother
from maps import character_map_35_nick
from maps import character_map_35_vanessa

# Mappings for 0.4 -> 0.5
from maps import character_map_45_alma
from maps import character_map_45_amber
from maps import character_map_45_anna
from maps import character_map_45_april
from maps import character_map_45_candice
from maps import character_map_45_chris
from maps import character_map_45_ciel
from maps import character_map_45_cindy
from maps import character_map_45_donald
from maps import character_map_45_eliza
from maps import character_map_45_erin
from maps import character_map_45_ermach
from maps import character_map_45_hillary
from maps import character_map_45_jenna
from maps import character_map_45_jennifer
from maps import character_map_45_jillian
from maps import character_map_45_karyn
from maps import character_map_45_kayla
from maps import character_map_45_main
from maps import character_map_45_martha
from maps import character_map_45_melina
from maps import character_map_45_michelle
from maps import character_map_45_mika
from maps import character_map_45_mother
from maps import character_map_45_nelson
from maps import character_map_45_nick
from maps import character_map_45_nurse
from maps import character_map_45_sean
from maps import character_map_45_vanessa
from maps import character_map_45_waitress

# Mappings for 0.5 -> 0.6
from maps import character_map_56_eliza
from maps import character_map_56_main

filename_03 = "Press-SwitchV0.3b-all";
filename_04 = "Press-SwitchV0.4a-pc";
filename_05 = "Press-SwitchV0.5c-pc";
filename_06 = "Press-SwitchV0.6";

# The key is the label used in an RPY "show" command to show a character.
# The value is the character directory used to find the images.
characterLabelMap = {
  "alma":          "alma",
  "amber":         "amber",
  "amberd":        "amber",
  "anna":          "anna",
  "april":         "april",
  "candice":       "candice",
  "candiced":      "candice",
  "chris":         "chris",
  "chrisd":        "chris",
  "chrisghost":    "chris",
  "ciel":          "ciel",
  "cindy":         "cindy",
  "donald":        "donald",
  "donaldd":       "donald",
  "donaldflash":   "donald",
  "eliza":         "eliza",
  "elizad":        "eliza",
  "elizaflash":    "eliza",
  "elizaghost":    "eliza",
  "erin":          "erin",
  "erind":         "erin",
  "eringhost":     "erin",
  "hillary":       "hillary",
  "hillaryd":      "hillary",
  "jenna":         "jenna",
  "jennifer":      "jennifer",
  "jenniferd":     "jennifer",
  "jillian":       "jillian",
  "jilliand":      "jillian",
  "karyn":         "karyn",
  "karynd":        "karyn",
  "karynflash":    "karyn",
  "karynghost":    "karyn",
  "kayla":         "kayla",
  "kaylad":        "kayla",
  "main":          "main",
  "maind":         "main",
  "mainflash":     "main",
  "mainghost":     "main",
  "martha":        "martha",
  "marthad":       "martha",
  "marthaghost":   "martha",
  "melina":        "melina",
  "michelle":      "michelle",
  "michelled":     "michelle",
  "michelleghost": "michelle",
  "mika":          "mika",
  "mikad":         "mika",
  "mother":        "mother",
  "nelson":        "nelson",
  "nick":          "nick",
  "nurse":         "nurse",
  "sean":          "sean",
  "vanessa":       "vanessa",
  "vanessad":      "vanessa",
  "waitress":      "waitress"
};

# Map showing whether to remap the character based on RenPy variables
characterDoRemap = {
  "alma":          False,
  "amber":         False,
  "amberd":        True,
  "anna":          False,
  "april":         False,
  "candice":       False,
  "candiced":      True,
  "chris":         False,
  "chrisd":        True,
  "chrisghost":    False,
  "ciel":          False,
  "cindy":         False,
  "donald":        False,
  "donaldd":       True,
  "donaldflash":   False,
  "eliza":         False,
  "elizad":        True,
  "elizaflash":    False,
  "elizaghost":    False,
  "erin":          False,
  "erind":         True,
  "eringhost":     False,
  "hillary":       False,
  "hillaryd":      True,
  "jenna":         False,
  "jennifer":      False,
  "jenniferd":     True,
  "jillian":       False,
  "jilliand":      True,
  "karyn":         False,
  "karynd":        True,
  "karynflash":    False,
  "karynghost":    False,
  "kayla":         False,
  "kaylad":        True,
  "main":          False,
  "maind":         True,
  "mainflash":     False,
  "mainghost":     False,
  "martha":        False,
  "marthad":       True,
  "marthaghost":   False,
  "melina":        False,
  "michelle":      False,
  "michelled":     True,
  "michelleghost": False,
  "mika":          False,
  "mikad":         True,
  "mother":        False,
  "nelson":        False,
  "nick":          False,
  "nurse":         False,
  "sean":          False,
  "vanessa":       False,
  "vanessad":      True,
  "waitress":      False,
};

characterImageMap35 = {
  "chris":    character_map_35_chris   .characterMapChris,
  "ciel":     character_map_35_ciel    .characterMapCiel,
  "eliza":    character_map_35_eliza   .characterMapEliza,
  "karyn":    character_map_35_karyn   .characterMapKaryn,
  "main":     character_map_35_main    .characterMapMain,
  "martha":   character_map_35_martha  .characterMapMartha,
  "michelle": character_map_35_michelle.characterMapMichelle,
  "mother":   character_map_35_mother  .characterMapMother,
  "nick":     character_map_35_nick    .characterMapNick,
  "vanessa":  character_map_35_vanessa .characterMapVanessa,
};

characterImageMap45 = {
  "alma":     character_map_45_alma    .characterMapAlma,
  "amber":    character_map_45_amber   .characterMapAmber,
  "anna":     character_map_45_anna    .characterMapAnna,
  "april":    character_map_45_april   .characterMapApril,
  "candice":  character_map_45_candice .characterMapCandice,
  "chris":    character_map_45_chris   .characterMapChris,
  "ciel":     character_map_45_ciel    .characterMapCiel,
  "cindy":    character_map_45_cindy   .characterMapCindy,
  "donald":   character_map_45_donald  .characterMapDonald,
  "eliza":    character_map_45_eliza   .characterMapEliza,
  "erin":     character_map_45_erin    .characterMapErin,
  "ermach":   character_map_45_ermach  .characterMapErmach,
  "hillary":  character_map_45_hillary .characterMapHillary,
  "jenna":    character_map_45_jenna   .characterMapJenna,
  "jennifer": character_map_45_jennifer.characterMapJennifer,
  "jillian":  character_map_45_jillian .characterMapJillian,
  "karyn":    character_map_45_karyn   .characterMapKaryn,
  "kayla":    character_map_45_kayla   .characterMapKayla,
  "main":     character_map_45_main    .characterMapMain,
  "martha":   character_map_45_martha  .characterMapMartha,
  "melina":   character_map_45_melina  .characterMapMelina,
  "michelle": character_map_45_michelle.characterMapMichelle,
  "mika":     character_map_45_mika    .characterMapMika,
  "mother":   character_map_45_mother  .characterMapMother,
  "nelson":   character_map_45_nelson  .characterMapNelson,
  "nick":     character_map_45_nick    .characterMapNick,
  "nurse":    character_map_45_nurse   .characterMapNurse,
  "sean":     character_map_45_sean    .characterMapSean,
  "vanessa":  character_map_45_vanessa .characterMapVanessa,
  "waitress": character_map_45_waitress.characterMapWaitress
};

characterImageMap56 = {
  "eliza":    character_map_56_eliza   .characterMapEliza,
  "main":     character_map_56_main    .characterMapMain,
};

# Initial state of RenPy variables
pyVariables = {
  "Al.display":   "alma",
  "Am.display":   "amber",
  "Can.display":  "candice",
  "ch.display":   "chris",
  "Do.display":   "donald",
  "e.display":    "eliza",
  "er.display":   "erin",
  "hi.display":   "hillary",
  "je.display":   "jennifer",
  "ji.display":   "jillian",
  "k.display":    "karyn",
  "ka.display":   "kayla",
  "ma.display":   "martha",
  "m.display":    "mika",
  "M.display":    "main",
  "mic.display":  "michelle",
  "Nel.display":  "nelson",
  "nur2.display": "nurse",
  "Te.display":   "teacher",
  "v.display":    "vanessa"
};

# Association of person name to RenPy display variable
personDispVars = {
  "alma":     "Al.display",
  "amber":    "Am.display",
  "candice":  "Can.display",
  "chris":    "ch.display",
  "donald":   "Do.display",
  "eliza":    "e.display",
  "erin":     "er.display",
  "hillary":  "hi.display",
  "jennifer": "je.display",
  "jillian":  "ji.display",
  "karyn":    "k.display",
  "kayla":    "ka.display",
  "martha":   "ma.display",
  "mika":     "m.display",
  "main":     "M.display",
  "michelle": "mic.display",
  "nelson":   "Nel.display",
  "nurse":    "nur2.display",
  "teacher":  "Te.display",
  "vanessa":  "v.display"
};

# List of active threads
threads = [];

# List of label call objects
labelCalls = [];

inlineErrors = False;

#-----------------------------------------------------------------------------
def printRed(s):
  #type: (str) -> None
  print("\033[1;31m" + s + "\033[0m");

#-----------------------------------------------------------------------------
def showError(txt):
  #type: (str) -> None
  printRed("Error: " + txt);

#-----------------------------------------------------------------------------
def flagError(rpFile, lineNum, txt):
  #type: (rpp.RenPyFile, int, str) -> str
  showError("Line " + str(lineNum) + ": " + txt);
  if inlineErrors:
    return rpFile.lines[lineNum].strip('\n') + "  # ERROR: " + txt + "\n";

  sys.exit(1);

#-----------------------------------------------------------------------------
def md5(fname):
  #type: (str) -> str
  hash_md5 = hashlib.md5()
  with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

#-----------------------------------------------------------------------------
def verifySingleFile(filename, desiredHash):
  #type: (str, str) -> bool
  print("Verifying " + filename + "...");
  if (not(os.path.exists(filename))):
    showError("File does not exist!");
    return False;

  actualHash = md5(filename);
  if (actualHash != desiredHash):
    showError("Checksum is not correct, please download the file again");
    print("Desired MD5: " + desiredHash);
    print("Actual MD5 : " + actualHash);
    return False;

  print("Succeeded");
  return True;

#-----------------------------------------------------------------------------
def unzipFile(filename):
  #type: (str) -> None
  print("Unzipping file " + filename + "...");
  with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(".")

#-----------------------------------------------------------------------------
def removeDir(filename):
  #type: (str) -> None
  if os.path.isdir(pathlib.Path(filename)):
    print("Removing directory " + filename + "...");
    shutil.rmtree(filename);

#-----------------------------------------------------------------------------
def checkFile(dirname, checksum):
  #type: (str, str) -> bool
  if os.path.isdir(pathlib.Path(dirname)):
    print("Directory " + dirname + " exists, ZIP extract skipped");
    return True;

  filename = dirname + ".zip";
  if not(verifySingleFile(filename, checksum)):
    return False;

  unzipFile(filename);
  return True;

#-----------------------------------------------------------------------------
def doMakeDir(path):
  #type: (str) -> None
  if (os.path.isdir(pathlib.Path(path))):
    print("Directory " + path + " already exists, skipping creation");
  else:
    print("Creating directory " + path);
    os.mkdir(path);

#-----------------------------------------------------------------------------
def doCopyFile(srcPath, dstPath, filename):
  #type: (str, str, str) -> None
  srcFile = os.path.join(srcPath, filename);
  print("Copying file " + srcFile + " into " + dstPath);
  shutil.copy(srcFile, dstPath);

#-----------------------------------------------------------------------------
def isNumberField(s):
  #type: (str) -> bool
  for c in s:
    if not(c in "0123456789"):
      return False;
  return True;

#-----------------------------------------------------------------------------
def expandNumberField(s):
  #type: (str) -> str
  if not(isNumberField(s)):
    return s;
  return s.zfill(3);

#-----------------------------------------------------------------------------
def getIndentOf(line):
  #type: (str) -> int
  indent = 0;
  lineLen = len(line);

  while((indent < lineLen) and (line[indent] == ' ')):
    indent = indent + 1;
  return indent;

#-----------------------------------------------------------------------------
def processCommand(rpFile, thread, lineNum, line):
  #type: (rpp.RenPyFile, rpp.RenPyThread, int, str) -> None
  fields = list(csv.reader([line], delimiter=' '))[0];

  if (len(fields) < 2):
    return;

  # Try for a UI timer jump
  if (fields[0].startswith("ui.timer(") and fields[1].startswith("ui.jumps(")):
    jumpLabel = fields[1].split('"')[1];
    addLabelCall(rpFile, jumpLabel, thread);
    return;

  # Try for a variable assignment
  if (len(fields) < 3):
    return;

  pyVar = fields[0].strip();
  pyVal = fields[2].strip().strip('"').strip('\'');

  #print(str(lineNum) + ": Command " + str(fields));

  if (fields[1] == "="):
    if (fields[2].startswith("renpy.random.choice([")):
      choiceList = line.split('[')[1].strip(')').strip(']').split();
      for choice in choiceList:
        pyVal = choice.strip(',').strip('\'');
        #print("Spawning thread for random choice: " + pyVal);
        newThread = copy.deepcopy(thread);
        newThread.vars[pyVar] = pyVal;
        newThread.stack[-1].lineNum = lineNum + 1;  # Start on next line
        threads.append(newThread);
      # Kill the current thread because the children threads of the random
      # choice will continue from here
      thread.stack = [];
    else:
      pyVal = line.split('=')[1].strip().strip('"').strip('\'');
      if (".display" in pyVar):
        if ("hillary school" in pyVal):
          pyVal = "hillary";
          rpFile.lines[lineNum] = rpFile.lines[lineNum].replace("hillary school", "hillary");
        elif (pyVal == "donald girl hair skin glasses"):
          pyVal = "donald girl dohair doskin doglasses";
          rpFile.lines[lineNum] = rpFile.lines[lineNum].replace("hair skin glasses", "dohair doskin doglasses");
      thread.vars[pyVar] = pyVal;
      #print("Variable '" + pyVar + "' becomes '" + pyVal + "'");
  elif (fields[1] == "+="):
    if not(pyVar in thread.vars):
      flagError(rpFile, lineNum, "Variable '" + pyVar + "' not found in thread");
    thread.vars[pyVar] = str(int(thread.vars[pyVar]) + int(pyVal));
  elif (fields[1] == "-="):
    if not(pyVar in thread.vars):
      flagError(rpFile, lineNum, "Variable '" + pyVar + "' not found in thread");
    thread.vars[pyVar] = str(int(thread.vars[pyVar]) - int(pyVal));
  else:
    flagError(rpFile, lineNum, "Unsupported operator '" + fields[1] + "', line is: " + line);

#-----------------------------------------------------------------------------
def calculateCondition(thread, lineNum, fields):
  #type: (rpp.RenPyThread, int, list[str]) -> bool
  offset = 1;
  while(offset < len(fields)):
    varname   = fields[offset];
    condition = fields[offset + 1];
    value     = fields[offset + 2];
    if not(varname in thread.vars):
      return False;
    if (condition == "=="):
      cont = False;
      if (value[-1] == ","):
        cont = True;
        value = value.strip(',');
      if (thread.vars[varname] == value.strip('"').strip('\'')):
        return True;
      if (cont):
        offset = offset + 1;
        value = fields[offset + 2];
        if (thread.vars[varname] == value.strip('"').strip('\'')):
          return True;
    elif (condition == ">="):
      if (int(thread.vars[varname]) >= int(value.strip('"').strip('\''))):
        return True;
    else:
      showError("Condition " + condition + " not supported");
      sys.exit(1);
    offset = offset + 3;
    if ((offset < len(fields) and not(fields[offset] == "or"))):
      showError(str(lineNum) + ": Boolean operator " + fields[offset] + " not supported, fields are " + str(fields));
      sys.exit(1);
    offset = offset + 1;
  return False;

#-----------------------------------------------------------------------------
def processIfStep(rpFile, thread):
  #type: (rpp.RenPyFile, rpp.RenPyThread) -> None
  obj = thread.stack[-1];
  line = rpFile.lines[obj.lineNum].split(':')[0];
  fields = line.split();
  
  # Are we still in the block?
  if (not(rpFile.indentIsGood(obj.lineNum, obj.indent))):
    thread.stack.pop();  # Kill the IF
    return;

  # Call the "if" hook to see if the file has special processing
  rpFile.hookIf(thread);

  if((fields[0] == "if") or (fields[0] == "elif")):
    condition = calculateCondition(thread, obj.lineNum, fields);
    if (condition and not(obj.hasExecuted)):
      obj.hasExecuted = True;
      thread.stack.append(rpp.RenPyBlock(obj.lineNum + 1, obj.indent + 4));

    obj.lineNum = rpFile.blockEndLine(obj.lineNum + 1, obj.indent + 4);

  elif (fields[0] == "else"):
    if not(obj.hasExecuted):
      thread.stack.append(rpp.RenPyBlock(obj.lineNum + 1, obj.indent + 4));
      obj.lineNum = rpFile.blockEndLine(obj.lineNum + 1, obj.indent + 4);
      return;
    thread.stack.pop();

  else:
    # Must have finished the block
    thread.stack.pop();

#-----------------------------------------------------------------------------
def processBlockStep(rpFile, thread):
  #type: (rpp.RenPyFile, rpp.RenPyThread) -> None
  blk = thread.stack[-1];
  i = blk.lineNum;

  indent = blk.indent;
  lineType = rpFile.lineTypes[i];
  if (not(rpFile.indentIsGood(i, indent)) and not(lineType == rpp.LineType.LABEL)):
    thread.stack.pop();
    return;

  if (lineType == rpp.LineType.OTHER):
    blk.lineNum = i + 1;
    return;

  if (lineType == rpp.LineType.MENU):
    # Shift the block processor to the end of the menu, so that when the
    # thread gets cloned it resumes from the right place
    blk.lineNum = rpFile.blockEndLine(i + 1, indent + 4);
    processMenuStep(rpFile, thread, i);
    return;

  if (lineType == rpp.LineType.RETURN):
    thread.stack = [];  # Kill the thread
    return;

  if (lineType == rpp.LineType.IF):
    thread.stack.append(rpp.RenPyIf(i, indent));  # Add an IF processor to the stack
    blk.lineNum = rpFile.blockEndLine(i + 1, indent + 4);
    return;

  if (lineType == rpp.LineType.ELSE):
    blk.lineNum = rpFile.blockEndLine(i + 1, indent + 4);   # Flush it
    return;

  strippedLine = rpFile.lines[i].strip();
  if (lineType == rpp.LineType.HIDE):
    person = strippedLine.split()[1];
    if rpFile.trackVis and not(person == "bg"):
      thread.vars["_visible_" + person] = "0";
    i += 1;
  elif (lineType == rpp.LineType.JUMP):
    label = strippedLine.split()[1];
    if not(rpFile.labelIsAcceptable(label)):
      # Kill this thread, it jumped. Nothing to do though!
      thread.stack = [];
      return;
    if not(label in rpFile.labelList):
      print("External jump: " + label);
      thread.stack = [];  # Kill this thread, it jumped out of the file
      return;
    addLabelCall(rpFile, label, thread);
    thread.stack = [];  # Kill this thread, it jumped
    return;
  elif (lineType == rpp.LineType.SHOW):
    if rpFile.trackVis and strippedLine.startswith("scene"):
      for varName in thread.vars:
        if varName.startswith("_visible_"):
          thread.vars[varName] = "0";
    if not(rpFile.lineModifiedFlags[i]):
      rpFile.lines[i] = processShow(rpFile, thread, i);
      rpFile.lineModifiedFlags[i] = True;
    i = i + 1;
  elif (lineType == rpp.LineType.DOLLAR):
    processCommand(rpFile, thread, i, strippedLine.strip('$').strip());
    i = i + 1;
  else:
    i = i + 1;

  blk.lineNum = i;

#-----------------------------------------------------------------------------
# On entry, lineNum points to the menu: line
def processMenuStep(rpFile, thread, lineNum):
  #type: (rpp.RenPyFile, rpp.RenPyThread, int) -> None
  global threads;

  indent = getIndentOf(rpFile.lines[lineNum]) + 4;
  lineNum = lineNum + 1;

  # Iterate the whole menu and fork threads from the current one for each
  # menu option
  line = rpFile.lines[lineNum];
  while((lineNum < rpFile.numLines) and rpFile.indentIsGood(lineNum, indent)):
    if (getIndentOf(line) == indent):
      menuItem = line.strip('\n').strip('\r').strip();
      if (":" in menuItem) and not((menuItem[0] == '#') or menuItem.startswith("\"{s}")):
        endQuote = menuItem.find("\"", 1);
        condition = ":";
        if (endQuote > 0):
          condition = menuItem[endQuote + 1:].strip();

        res = True;
        if (not(condition == ":")):
          # Menu has a condition on it
          condition = condition.strip(':');
          res = calculateCondition(thread, lineNum, condition.split());

        if (res):
          newThread = copy.deepcopy(thread);
          newThread.stack.append(rpp.RenPyBlock(lineNum + 1, indent + 4));
          threads.append(newThread);

        lineNum = rpFile.blockEndLine(lineNum + 1, indent + 4);
      else:
        lineNum = lineNum + 1;
    else:
      lineNum = lineNum + 1;

    line = rpFile.lines[lineNum];

  # Kill the current thread. Because it's been used as the parent thread for
  # all the menu options, it's not needed any more as each menu option will
  # continue from here.
  thread.stack = [];

#-----------------------------------------------------------------------------
def processShow(rpFile, thread, lineNum):
  #type: (rpp.RenPyFile, rpp.RenPyThread, int) -> str
  line = rpFile.lines[lineNum];
  fields = line.strip().strip(":").split();

  # At this point, 'fields' looks like this:
  # ['show', 'maind', '17', 'with', 'dissolve']

  # Check for backgrounds
  if fields[1] == "bg":
    if len(fields) < 3:
      return line;
    if not(fields[2] in rpFile.backMap):
      #return flagError(rpFile, lineNum, "Background " + fields[2] + " has no mapping table entry");
      return line;

    newLine = "";
    indent = 0;
    while line[indent] == " ":
      newLine += " ";
      indent = indent + 1;

    newbg = rpFile.backMap[fields[2]];
    if (newbg == ""):
      return flagError(rpFile, lineNum, "Background '" + fields[2] + "' exists but has no mapping");

    newLine += fields[0] + " bg " + newbg;

    i = 3;
    while i < len(fields):
      newLine += " " + fields[i];
      i = i + 1;

    if (line.strip()[-1] == ":"):
      newLine += ":";

    newLine += "\n";
    return newLine;

  # Check for 0.3 style "show cg" statements
  if (fields[0] == "show") and (fields[1] == "cg"):
    return rpFile.processCG(line);

  # Try for a character
  # Character label is fields[1], get character name
  if not(fields[0] == "show"):
    return line;
  if not(fields[1] in characterLabelMap):
    return line;

  if not(lineNum in rpFile.showLines):
    rpFile.showLines.append(lineNum);

  if (rpFile.trackVis):
    varName = "_visible_" + fields[1];
    if not(varName in thread.vars) or (thread.vars[varName] == "0"):
      # Person has become visible
      if (fields[1] in rpFile.charFlip) and not(lineNum in rpFile.visLines):
        rpFile.visLines.append(lineNum);
    thread.vars[varName] = "1";

  # If it's got no parameters, like "show michelled:", then just return it
  # as there's no mapping to do
  if (len(fields) < 3):
    return line;

  isFlash = ("flash" in fields[1]);

  charName = characterLabelMap[fields[1]];
  swappedCharName = charName;
  donaldGirl = False;
  if characterDoRemap[fields[1]]:
    # Character is not a ghost, do the remap
    if (charName in personDispVars):
      swappedCharName = thread.vars[personDispVars[charName]];
    swappedFields = swappedCharName.split();
    swappedCharName = swappedFields[0];
    if (swappedCharName == "donald") and (len(swappedFields) > 1) and (swappedFields[1] == "girl"):
      donaldGirl = True;

  #i = 1;
  #while i < len(swappedFields):
  #  fields.append(swappedFields[i]);
  #  i = i + 1;

  filenameMode = True;
  baseMode = True;
  exFile = swappedCharName + "_ex";
  if donaldGirl:
    exFile += "_girl";
  modifiers = "";
  base = "";
  i = 2;
  while i < len(fields):
    if (fields[i] in ["as", "at", "behind", "with", "zorder"]):
      filenameMode = False;
    if (filenameMode):
      field = expandNumberField(fields[i]);
      if (field == "full"):
        exFile = exFile + "_full";
      elif isNumberField(field):
        baseMode = False;

      if baseMode:
        if not(field == "full") and not((charName == "hillary") and (fields[i] == "school")):
          base = base + " " + fields[i];
      else:
        exFile = exFile + "_" + field;

    else:
      modifiers = modifiers + " " + fields[i];
    i = i + 1;

  if (exFile == (swappedCharName + "_ex")) or (exFile == (swappedCharName + "_ex_full")):
    # It's something like "show candice with dissolve", with no fields so nothing to do
    return line;

  mappedFile = "";
  hasMapped = False;

  if (swappedCharName in rpFile.charMap):
    if exFile in rpFile.charMap[swappedCharName]:
      mappedFile = rpFile.charMap[swappedCharName][exFile];
      hasMapped = True;
    elif exFile+"_001" in rpFile.charMap[swappedCharName]:
      mappedFile = rpFile.charMap[swappedCharName][exFile+"_001"];
      hasMapped = True;
    elif exFile+"_002" in rpFile.charMap[swappedCharName]:
      mappedFile = rpFile.charMap[swappedCharName][exFile+"_002"];
      hasMapped = True;
    elif exFile+"_003" in rpFile.charMap[swappedCharName]:
      mappedFile = rpFile.charMap[swappedCharName][exFile+"_003"];
      hasMapped = True;
  else:
    # We're not doing a V3 or V4 mapping for this character, fake that we've done one
    mappedFile = exFile;
    hasMapped = True;

  if not(hasMapped):
    # The .rpy file is referencing a graphic that doesn't seem to exist in the 0.4 graphics directory.
    print("DBG: Thread started from label: " + thread.label);
    print("DBG: Vars are: " + str(thread.vars));
    i = 0;
    while(i < len(thread.stack)):
      print("DBG: Stack[" + str(i) + "] = " + str(thread.stack[i]));
      i += 1;
    return(flagError(rpFile, lineNum, "Mapping failed, source file '" + exFile + "' not found. Line being processed is: " + str(fields)));

  if mappedFile == "":
    return(flagError(rpFile, lineNum, "Mapping failed, source file '" + exFile + "' exists but has no mapping. Line being processed is: " + str(fields)));

  # Map V6 if present
  if (swappedCharName in rpFile.v6Map):
    hasMapped = False;
    v6File = "";
    if mappedFile in rpFile.v6Map[swappedCharName]:
      v6File = rpFile.v6Map[swappedCharName][mappedFile];
      hasMapped = True;
    elif mappedFile+"_001" in rpFile.v6Map[swappedCharName]:
      v6File = rpFile.v6Map[swappedCharName][mappedFile+"_001"];
      hasMapped = True;
    elif mappedFile+"_002" in rpFile.v6Map[swappedCharName]:
      v6File = rpFile.v6Map[swappedCharName][mappedFile+"_002"];
      hasMapped = True;
    elif mappedFile+"_003" in rpFile.v6Map[swappedCharName]:
      v6File = rpFile.v6Map[swappedCharName][mappedFile+"_003"];
      hasMapped = True;

    if not(hasMapped):
      return(flagError(rpFile, lineNum, "No V6 mapping for V5 file '" + mappedFile + "', source file '" + exFile + "', char name " + swappedCharName + ", original char " + charName));
    #print("Mapped V5 " + mappedFile + " to V6 " + v6File);
    mappedFile = v6File;

  mappedFields = mappedFile.split("_");

  if (len(mappedFields) < 2):
    return(flagError(rpFile, lineNum, "Invalid mapping! Source is '" + exFile + "', map is '" + mappedFile + "'"));

  if not(mappedFields[0] == swappedCharName):
    return(flagError(rpFile, lineNum, "Mapped to a different character! Source is '" + exFile + "', map is '" + mappedFile + "'"));

  if not(mappedFields[1] == "ex"):
    return(flagError(rpFile, lineNum, "Mapping is not to an expression graphic! Source is '" + exFile + "', map is '" + mappedFile + "'"));

  newLine = "";
  indent = 0;
  while line[indent] == " ":
    newLine += " ";
    indent = indent + 1;

  newLine += "show " + rpFile.addMutators(fields[1]) + base;

  i = 2;
  while i < len(mappedFields) - 1:
    if isNumberField(mappedFields[i]):
      newLine += " " + str(int(mappedFields[i]));
    elif not((donaldGirl and (mappedFields[i] == "girl")) or isFlash):
      newLine += " " + mappedFields[i];
    i = i + 1;

  newLine += modifiers;
  if (line.strip()[-1] == ":"):
    newLine += ":";

  newLine += "\n";
  return newLine;

#-----------------------------------------------------------------------------
def processNextThread(rpFile):
  #type: (rpp.RenPyFile) -> None
  global threads;

  thread = threads.pop();
  while len(thread.stack) > 0:
    obj = thread.stack[-1];
    if (obj.objType == "Block"):
      processBlockStep(rpFile, thread);
    elif (obj.objType == "If"):
      processIfStep(rpFile, thread);
    else:
      print("Unhandled object type: " + obj.objType);
      sys.exit(1);

#-----------------------------------------------------------------------------
def addLabelCall(rpFile, l, thread):
  #type: (rpp.RenPyFile, str, rpp.RenPyThread) -> None
  if not(rpFile.labelIsAcceptable(l)):
    return;

  labelCalls.append(rpp.RenPyLabelCall(l, thread.vars.copy()));

#-----------------------------------------------------------------------------
def processLabelCall(rpFile, l, v):
  #type: (rpp.RenPyFile, str, dict[str, str]) -> None
  global threads;

  lineNum = rpFile.labelList[l] + 1;
  line = rpFile.lines[lineNum];
  indent = getIndentOf(line);

  blk = rpp.RenPyBlock(lineNum, indent);
  thread = rpp.RenPyThread(l, v, [blk]);
  threads.append(thread);

#-----------------------------------------------------------------------------
def iterateLabelCalls(rpFile):
  #type: (rpp.RenPyFile) -> None
  global threads;
  global labelCalls;

  iterations = 1;
  duplicates = 0;
  numThreads = 0;
  while ((len(labelCalls) > 0) or (len(threads) > 0)):
    print("---------- Depth " + str(iterations) + " ----------");
    print("Label calls: " + str(len(labelCalls)));

    # Process label calls
    while(len(labelCalls) > 0):
      labelCall = labelCalls.pop();
      if not(labelCall in labelCalls):
        processLabelCall(rpFile, labelCall.label, labelCall.vars);
      else:
        duplicates += 1;

    # Process threads
    print("Paths: " + str(len(threads)));
    while(len(threads) > 0):
      processNextThread(rpFile);
      numThreads += 1;
      if (len(threads) % 20) == 0:
        print("[Depth " + str(iterations) + "] " + str(duplicates) + " duplicate paths, " + str(numThreads) + " total paths, " + str(len(threads)) + " left this depth");

    iterations += 1;

#-----------------------------------------------------------------------------
def verifySingleCharacterMapping(charName, desc, mapTable, charactersDir):
  charUpper = charName.capitalize();
  imageDir = os.path.join(charactersDir, charUpper);

  # Make a list of filenames converted to lowercase
  filesLower = [];
  for filename in os.listdir(imageDir):
    filesLower.append(filename.lower());

  for k in mapTable:
    if not(mapTable[k] == ""):
      if not(mapTable[k] + ".png" in filesLower):
        printRed("ERROR: Key '" + k + "', value '" + mapTable[k] + "': Map destination file not found");
        return False;

      # Fix up double underscores in v4 Melina filenames
      mapTable[k] = mapTable[k].replace("__", "_");

  return True;

#-----------------------------------------------------------------------------
def verifyCharacterMapping(desc, mapTable, extractedDir):
  imageDir = os.path.join(extractedDir, "Characters");
  for charName in mapTable:
    if not(verifySingleCharacterMapping(charName, desc, mapTable[charName], imageDir)):
      return False;
  return True;

#-----------------------------------------------------------------------------
# Main program
def main(argv):
  global inlineErrors;
  global pyVariables;
  global threads;

  doClean = False;
  doEliza = True;
  doCiel  = True;
  doNick  = False
  doGoopy = True;
  doScan  = True;
  doV6    = False;

  try:
    opts, args = getopt.getopt(argv, "", ["clean","inlineerrors","nick","nociel","noeliza","nogoopy","noscan","v6"])
  except getopt.GetoptError:
    showError('Usage is: press-stitch.py [--clean]');
    sys.exit(1);

  for opt, arg in opts:
    if (opt == "--clean"):
      doClean = True;
    elif (opt == "--inlineerrors"):
      inlineErrors = True;
    elif (opt == "--nick"):
      doNick = True;
    elif (opt == "--nociel"):
      doCiel = False;
    elif (opt == "--noeliza"):
      doEliza = False;
    elif (opt == "--nogoopy"):
      doGoopy = False;
    elif (opt == "--noscan"):
      doScan = False;
    elif (opt == "--v6"):
      doV6 = True;
      doCiel = False;  # Cielpath disabled for 0.6

  if (doClean):
    removeDir(filename_03);
    removeDir(filename_04);
    removeDir(filename_05);
    removeDir("Extracted");
    sys.exit(0);

  # Normal run
  have3 = False;
  have4 = False;
  if os.path.exists(filename_03 + ".zip"):
    if not(checkFile(filename_03, "e01bfc54520e8251bc73c7ee128836e2")):
      sys.exit(1);
    have3 = True;
    press_stitch_archive.unpackArchive(filename_03);

  if os.path.exists(filename_03 + ".zip"):
    if not(checkFile(filename_04, "ca7ee44f40f802009a6d49659c8a760d")):
      sys.exit(1);
    have4 = True;
    press_stitch_archive.unpackArchive(filename_04);

  if not(checkFile(filename_05, "6a4f9dac386e2fae1bce00e0157ee8b1")):
    sys.exit(1);

  press_stitch_archive.unpackArchive(filename_05);

  extPath5  = os.path.join("Extracted", filename_05);
  dstPath   = os.path.join(filename_05, "game");
  patchBase = os.path.join("Patch", filename_05);
  patchPath = os.path.join(patchBase, "game");
  v6map = {};

  if not(verifyCharacterMapping("v3 to v5", characterImageMap35, extPath5)):
    sys.exit(1);

  if not(verifyCharacterMapping("v4 to v5", characterImageMap45, extPath5)):
    sys.exit(1);

  if doV6:
    v6map = characterImageMap56;
    dstPath = os.path.join(filename_06, "game");
    patchPath = os.path.join("Patch", filename_06, "game");

  doMakeDir("Patch");
  doMakeDir(patchBase);
  doMakeDir(patchPath);
  doMakeDir(os.path.join(patchPath, "Story"));

  # Day-0.rpy
  print("Patching Day-0.rpy...");
  dayzero = rpp.RenPyFile();
  dayzero.readFile(os.path.join(extPath5, "Story", "Day-0.rpy"));
  dayzero.lines.insert(2848, (" " * 28) + "\"Maybe I was too quick to reject Eliza...\":\n");
  dayzero.lines.insert(2849, (" " * 32) + "jump eliza\n");
  if doCiel:
    dayzero.lines[2851] = (" " * 20) + "\"Hide it until tomorrow.\":\n";
    dayzero.lines[2863] = (" " * 20) + "\"Leave it on my desk and sleep.\":\n";
    dayzero.lines[2864] = (" " * 24) + "jump leftit\n";

  if doV6:
    dayzero.v6map = v6map;
    dayzero.findLabels();
    dayzero.findShows();
    addLabelCall(dayzero, "GameStart", rpp.RenPyThread(pyVariables.copy(), []));
    iterateLabelCalls(dayzero);

  dayzero.writeFile(os.path.join(dstPath,   "Story", "Day-0.rpy"));
  dayzero.writeFile(os.path.join(patchPath, "Story", "Day-0.rpy"));

  if doNick:
    # Patch Day_001_Saved
    print("Patching Day_001_Saved.rpy...");
    dayzerosaved = rpp.RenPyFile();
    dayzerosaved.readFile(os.path.join(extPath5, "Story", "Day_001_Saved.rpy"));

    # Patch the menu option - jump into the unused HideDevicePath.rpy file
    dayzerosaved.lines[2402] = "        \"Best to keep it hidden for now.\":\n"
    dayzerosaved.lines[2403] = "            jump didnttell\n"

    # Write the updated file back out
    dayzerosaved.writeFile(os.path.join(dstPath,   "Story", "Day_001_Saved.rpy"));
    dayzerosaved.writeFile(os.path.join(patchPath, "Story", "Day_001_Saved.rpy"));

    # Patch HideDevicePath
    print("Patching HideDevicePath.rpy...");
    hideDevicePath = rpp.RenPyFile();
    hideDevicePath.readFile(os.path.join(extPath5, "Story", "HideDevicePath.rpy"));

    # Disable the menu option leading to the 0.3 trio swap
    hideDevicePath.lines[195] = "        \"{s}I shared the device with them.{/s}\":\n";
    hideDevicePath.lines[196] = "            call screen pending_001(path_name = \"Trio Swap\", author_note = \"This path is under development, check back soon!\")\n";
    hideDevicePath.lines[197] = "            return\n";

    # Write the updated file back out
    hideDevicePath.writeFile(os.path.join(dstPath,   "Story", "HideDevicePath.rpy"));
    hideDevicePath.writeFile(os.path.join(patchPath, "Story", "HideDevicePath.rpy"));

  if doCiel:
    # Read Cielpath.rpy into memory
    print("Patching Cielpath.rpy...");
    cielPath = rpp.RenPyFileCiel(backgrounds_map.backgroundMap35, characterImageMap35, v6map);
    cielPath.readFile(os.path.join(extPath5, "Story", "Cielpath.rpy"));

    # Search for labels
    cielPath.findLabels();

    # Search for "show" statements
    cielPath.findShows();

    # Process the 'leftit' label, it's the toplevel.
    addLabelCall(cielPath, "leftit", rpp.RenPyThread("", {}, []));
    iterateLabelCalls(cielPath);

    # Flip the affected V3 characters
    cielPath.doFlips();

    # Write the updated Cielpath.rpy back out
    cielPath.writeFile(os.path.join(dstPath,   "Story", "Cielpath.rpy"));
    cielPath.writeFile(os.path.join(patchPath, "Story", "Cielpath.rpy"));

  if doEliza:
    # Read ElizaPath.rpy into memory
    print("Patching ElizaPath.rpy... (0.4 content)");
    elizaPath = rpp.RenPyFileEliza(backgrounds_map.backgroundMap45, characterImageMap45, v6map);
    elizaPath.readFile(os.path.join(extPath5, "Story", "ElizaPath.rpy"));

    # Search for labels
    elizaPath.findLabels();

    # Search for "show" statements
    elizaPath.findShows();

    if doScan:
      # Process the 'eliza' label, it's the toplevel.
      # We need two calls, one for the timer < 34 and one for > 30
      pyVariables["timer_value"] = 0;   # Less than 30
      addLabelCall(elizaPath, "eliza", rpp.RenPyThread("", pyVariables.copy(), []));
      pyVariables["timer_value"] = 60;  # Greater than 30
      addLabelCall(elizaPath, "eliza", rpp.RenPyThread("", pyVariables.copy(), []));
      iterateLabelCalls(elizaPath);

    # Write the updated ElizaPath.rpy back out
    elizaPath.writeFile(os.path.join(dstPath,   "Story", "ElizaPath.rpy"));
    elizaPath.writeFile(os.path.join(patchPath, "Story", "ElizaPath.rpy"));

  if doGoopy:
    # By default we're processing the file we just made for the 0.4 Eliza content...
    srcFile = os.path.join(dstPath, "Story", "ElizaPath.rpy");
    if not(doEliza):
      # ...but if we've not done Eliza this time, we'll take a saved copy
      srcFile = "ElizaPath-NoGoopy.rpy";

    # Read ElizaPath.rpy into memory. GoopyPath is ElizaPath but with v0.3 mappings
    print("Patching ElizaPath.rpy... (Goopy path)");
    goopyPath = rpp.RenPyFileGoopy(backgrounds_map.backgroundMap35, characterImageMap35, v6map);
    goopyPath.readFile(srcFile);

    # Search for labels
    goopyPath.findLabels();

    # Search for "show" statements
    goopyPath.findShows();

    # Process the path
    addLabelCall(goopyPath, "elizagoopypath", rpp.RenPyThread("", {}, []));
    iterateLabelCalls(goopyPath);

    # Flip the affected V3 characters
    goopyPath.doFlips();

    # Write the updated ElizaPath.rpy back out
    goopyPath.writeFile(os.path.join(dstPath,   "Story", "ElizaPath.rpy"));
    goopyPath.writeFile(os.path.join(patchPath, "Story", "ElizaPath.rpy"));

  # Read effects.rpy into memory
  print("Patching effects.rpy...");
  effectsFile = rpp.RenPyFile();
  effectsFile.readFile(os.path.join(extPath5, "effects.rpy"));

  # Patch the timer
  effectsFile.lines[492] = "default timer_value = 0\n";
  effectsFile.lines[495] = "    timer 1 repeat True action SetVariable(\"timer_value\", timer_value + 1)\n";

  # Write the updated effects.rpy back out
  effectsFile.writeFile(os.path.join(dstPath,   "effects.rpy"));
  effectsFile.writeFile(os.path.join(patchPath, "effects.rpy"));

  # Read options.rpy into memory
  print("Patching options.rpy...");
  optionsFile = rpp.RenPyFile();
  optionsFile.readFile(os.path.join(extPath5, "options.rpy"));

  # Patch the version number
  optionsFile.lines[25] = "    config.version = \"0.5c-merged\"\n";

  # Write the updated effects.rpy back out
  optionsFile.writeFile(os.path.join(dstPath,   "options.rpy"));
  optionsFile.writeFile(os.path.join(patchPath, "options.rpy"));

  # Read screens.rpy into memory
  print("Patching screens.rpy...");
  screensFile = rpp.RenPyFile();
  screensFile.readFile(os.path.join(extPath5, "screens.rpy"));

  # Patch the version number
  screensFile.lines[190] = "        text \"{=bio_font}{size=+10}{color=32eeff}Press-Switch V:0.5c-merged{/color}{/size}{/bio_font}\":\n";

  # Write the updated file back out
  screensFile.writeFile(os.path.join(dstPath,   "screens.rpy"));
  screensFile.writeFile(os.path.join(patchPath, "screens.rpy"));

  # Read Iida path into memory
  print("Patching Device_Iida_Path.rpy...");
  iidaPathFile = rpp.RenPyFile();
  iidaPathFile.readFile(os.path.join(extPath5, "Story", "Device_Iida_Path.rpy"));

  # Fix typo for expression
  iidaPathFile.lines[19168] = "        show maind 5 open2\n"

  # Write the updated file back out
  iidaPathFile.writeFile(os.path.join(dstPath,   "Story", "Device_Iida_Path.rpy"));
  iidaPathFile.writeFile(os.path.join(patchPath, "Story", "Device_Iida_Path.rpy"));

  # Read Iida path into memory
  print("Patching script.rpy...");
  scriptFile = rpp.RenPyFile();
  scriptFile.readFile(os.path.join(extPath5, "script.rpy"));

  # Fix bio error
  scriptFile.lines[611] = "        side \"r\":\n"

  # Fix bio button bug
  line = "        imagebutton auto \"gui/Bio_Button_Exdown_%s.png\" action ";
  line += "If(profile_ex_num > 0, ";
  line += "SetScreenVariable(\"profile_ex_num\", profile_ex_num-1), ";
  line += "SetScreenVariable(\"profile_ex_num\", len(profile_ex_list)-1)), "
  line += "SetScreenVariable(\"profile_ex\", profile_ex_list[profile_ex_num])\n";
  scriptFile.lines[922] = line;

  # Write the updated file back out
  scriptFile.writeFile(os.path.join(dstPath,   "script.rpy"));
  scriptFile.writeFile(os.path.join(patchPath, "script.rpy"));

#-----------------------------------------------------------------------------
# Hook to call main
if __name__ == "__main__":
  main(sys.argv[1:])
