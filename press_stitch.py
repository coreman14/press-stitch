#-----------------------------------------------------------------------------
# press-stitch.py
# Merges the three Press Switch games together
#-----------------------------------------------------------------------------

import getopt
import hashlib
import os.path
import pathlib
import shutil
import sys
import zipfile
import press_stitch_archive
import backgrounds_map
import character_map_alma
import character_map_amber
import character_map_anna
import character_map_april
import character_map_candice
import character_map_chris
import character_map_ciel
import character_map_cindy
import character_map_donald
import character_map_eliza
import character_map_erin
import character_map_hillary
import character_map_jenna
import character_map_jennifer
import character_map_jillian
import character_map_karyn
import character_map_kayla
import character_map_main
import character_map_martha
import character_map_melina
import character_map_michelle
import character_map_mika
import character_map_mother
import character_map_nelson
import character_map_nick
import character_map_nurse
import character_map_sean
import character_map_vanessa
import character_map_waitress

filename_03 = "Press-SwitchV0.3b-all";
filename_04 = "Press-SwitchV0.4a-pc";
filename_05 = "Press-SwitchV0.5c-pc";

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

characterImageMap = {
  "alma":     character_map_alma    .characterMapAlma,
  "amber":    character_map_amber   .characterMapAmber,
  "anna":     character_map_anna    .characterMapAnna,
  "april":    character_map_april   .characterMapApril,
  "candice":  character_map_candice .characterMapCandice,
  "chris":    character_map_chris   .characterMapChris,
  "ciel":     character_map_ciel    .characterMapCiel,
  "cindy":    character_map_cindy   .characterMapCindy,
  "donald":   character_map_donald  .characterMapDonald,
  "eliza":    character_map_eliza   .characterMapEliza,
  "erin":     character_map_erin    .characterMapErin,
  "hillary":  character_map_hillary .characterMapHillary,
  "jenna":    character_map_jenna   .characterMapJenna,
  "jennifer": character_map_jennifer.characterMapJennifer,
  "jillian":  character_map_jillian .characterMapJillian,
  "karyn":    character_map_karyn   .characterMapKaryn,
  "kayla":    character_map_kayla   .characterMapKayla,
  "main":     character_map_main    .characterMapMain,
  "martha":   character_map_martha  .characterMapMartha,
  "melina":   character_map_melina  .characterMapMelina,
  "michelle": character_map_michelle.characterMapMichelle,
  "mika":     character_map_mika    .characterMapMika,
  "mother":   character_map_mother  .characterMapMother,
  "nelson":   character_map_nelson  .characterMapNelson,
  "nick":     character_map_nick    .characterMapNick,
  "nurse":    character_map_nurse   .characterMapNurse,
  "sean":     character_map_sean    .characterMapSean,
  "vanessa":  character_map_vanessa .characterMapVanessa,
  "waitress": character_map_waitress.characterMapWaitress
};

#-----------------------------------------------------------------------------
def printRed(s):
  print("\033[1;31m" + s + "\033[0m");

#-----------------------------------------------------------------------------
def showError(txt):
  printRed("Error: " + txt);

#-----------------------------------------------------------------------------
def md5(fname):
  hash_md5 = hashlib.md5()
  with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

#-----------------------------------------------------------------------------
def verifySingleFile(filename, desiredHash):
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
  print("Unzipping file " + filename + "...");
  with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(".")

#-----------------------------------------------------------------------------
def removeDir(filename):
  if os.path.isdir(pathlib.Path(filename)):
    print("Removing directory " + filename + "...");
    shutil.rmtree(filename);

#-----------------------------------------------------------------------------
def checkFile(dirname, checksum):
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
  if (os.path.isdir(pathlib.Path(path))):
    print("Directory " + path + " already exists, skipping creation");
  else:
    print("Creating directory " + path);
    os.mkdir(path);

#-----------------------------------------------------------------------------
def doCopyFile(srcPath, dstPath, filename):
  srcFile = os.path.join(srcPath, filename);
  print("Copying file " + srcFile + " into " + dstPath);
  shutil.copy(srcFile, dstPath);

#-----------------------------------------------------------------------------
def isNumberField(s):
  for c in s:
    if not(c in "0123456789"):
      return False;
  return True;

#-----------------------------------------------------------------------------
def expandNumberField(s):
  if not(isNumberField(s)):
    return s;
  return s.zfill(3);

#-----------------------------------------------------------------------------
def processShow(line):
  fields = line.strip().strip(":").split();

  # At this point, 'fields' looks like this:
  # ['show', 'maind', '17', 'with', 'dissolve']

  # Check for backgrounds
  if fields[1] == "bg":
    if len(fields) < 3:
      return line;
    if not(fields[2] in backgrounds_map.backgroundMap):
      return line;

    newLine = "";
    indent = 0;
    while line[indent] == " ":
      newLine += " ";
      indent = indent + 1;

    newbg = backgrounds_map.backgroundMap[fields[2]];
    if (newbg == ""):
      print("Background '" + fields[2] + "' exists but has no mapping");
      return line;

    newLine += fields[0] + " bg " + backgrounds_map.backgroundMap[fields[2]];

    i = 3;
    while i < len(fields):
      newLine += " " + fields[i];
      i = i + 1;

    if (line.strip()[-1] == ":"):
      newLine += ":";

    newLine += "\n";
    return newLine;

  # Try for a character
  # Character label is fields[1], get character name
  if not(fields[0] == "show"):
    return line;
  if not(fields[1] in characterLabelMap):
    return line;

  charName = characterLabelMap[fields[1]];

  filenameMode = True;
  baseMode = True;
  exFile = charName + "_ex";
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

  mappedFile = "";
  hasMapped = False;

  if exFile+"_001" in characterImageMap[charName]:
    mappedFile = characterImageMap[charName][exFile+"_001"];
    hasMapped = True;
  elif exFile+"_002" in characterImageMap[charName]:
    mappedFile = characterImageMap[charName][exFile+"_002"];
    hasMapped = True;
  elif exFile+"_003" in characterImageMap[charName]:
    mappedFile = characterImageMap[charName][exFile+"_003"];
    hasMapped = True;

  if not(hasMapped):
    # The .rpy file is referencing a graphic that doesn't seem to exist in the 0.4 graphics directory.
    # Something's obviously up, maybe old 0.3 content? For now, pass it through unaltered,
    # but we might want to take note of this later.
    #print("Mapping failed, source file '" + exFile + "' not found. Line being processed is: " + str(fields));
    return line;

  if mappedFile == "":
    print("Mapping failed, source file '" + exFile + "' exists but has no mapping. Line being processed is: " + str(fields));
    return line;

  mappedFields = mappedFile.split("_");

  if not(mappedFields[0] == charName):
    showError("Mapped to a different character! Source is '" + exFile + "', map is '" + mappedFile + "'");
    sys.exit(1);

  if not(mappedFields[1] == "ex"):
    showError("Mapping is not to an expression graphic! Source is '" + exFile + "', map is '" + mappedFile + "'");
    sys.exit(1);

  newLine = "";
  indent = 0;
  while line[indent] == " ":
    newLine += " ";
    indent = indent + 1;

  newLine += "show " + fields[1] + base;

  i = 2;
  while i < len(mappedFields) - 1:
    if isNumberField(mappedFields[i]):
      newLine += " " + str(int(mappedFields[i]));
    else:
      newLine += " " + mappedFields[i];
    i = i + 1;

  newLine += modifiers;
  if (line.strip()[-1] == ":"):
    newLine += ":";

  newLine += "\n";
  return newLine;

#-----------------------------------------------------------------------------
# Main program
def main(argv):
  doClean = False;

  try:
    opts, args = getopt.getopt(argv, "", ["clean"])
  except getopt.GetoptError:
    showError('Usage is: press-stitch.py [--clean]');
    sys.exit(1);

  for opt, arg in opts:
    if (opt == "--clean"):
      doClean = True;

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

  extPath5 = os.path.join("Extracted", filename_05);
  dstPath  = os.path.join(filename_05, "game");

  # Day-0.rpy
  print("Patching Day-0.rpy...");
  text_file = open(os.path.join(extPath5, "Story", "Day-0.rpy"), "r");
  lines = text_file.readlines();
  lines.insert(2848, (" " * 28) + "\"Maybe I was too quick to reject Eliza...\":\n");
  lines.insert(2849, (" " * 32) + "jump eliza\n");
  with open(os.path.join(dstPath, "Story", "Day-0.rpy"), "w") as outfile:
    outfile.writelines(lines);

  # Read ElizaPath.rpy into memory
  print("Patching ElizaPath.rpy...");
  text_file = open(os.path.join(extPath5, "Story", "ElizaPath.rpy"), "r");
  lines = text_file.readlines();

  # Search for "show" statements
  numLines = len(lines);
  i = 0;
  while i < numLines:
    if (lines[i].strip().startswith("show") or lines[i].strip().startswith("scene")):
      lines[i] = processShow(lines[i]);
    i = i + 1;

  # Patch the timer
  lines[6396] = (" " * 20) + "if timer_value >= 30:\n";
  lines[6552] = (" " * 20) + "if timer_value >= 30:\n";
  lines[6713] = (" " * 20) + "if timer_value >= 30:\n";

  # Write the updated ElizaPath.rpy back out
  with open(os.path.join(dstPath, "Story", "ElizaPath.rpy"), "w") as outfile:
    outfile.writelines(lines);

  # Read effects.rpy into memory
  print("Patching effects.rpy...");
  text_file = open(os.path.join(extPath5, "effects.rpy"), "r");
  lines = text_file.readlines();

  # Patch the timer
  lines[492] = "default timer_value = 0\n";
  lines[495] = "    timer 1 repeat True action SetVariable(\"timer_value\", timer_value + 1)\n";

  # Write the updated effects.rpy back out
  with open(os.path.join(dstPath, "effects.rpy"), "w") as outfile:
    outfile.writelines(lines);

#-----------------------------------------------------------------------------
# Hook to call main
if __name__ == "__main__":
  main(sys.argv[1:])
