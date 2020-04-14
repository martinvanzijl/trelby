import screenplay as scr
import u

# tests delete commands

def testBackStart():
    sp = u.load()
    sp.cmd("deleteBackward")
    assert (sp.line == 0) and (sp.column == 0)
    assert sp.lines[0].text == "ext. stonehenge - night"

def testBack():
    sp = u.load()
    sp.cmd("moveRight")
    sp.cmd("deleteBackward")
    assert (sp.line == 0) and (sp.column == 0)
    assert sp.lines[0].text == "xt. stonehenge - night"

def testBackJoinElements():
    sp = u.load()
    sp.cmd("moveDown")
    sp.cmd("deleteBackward")
    assert (sp.line == 0) and (sp.column == 23)
    assert sp.lines[0].text == "ext. stonehenge - nightA blizzard rages."\
           " Snow is everywhere"

def testBackLbSpace():
    sp = u.load()
    sp.gotoPos(16, 60)
    sp.cmd("addChar", char = " ")
    assert sp.lines[16].lb == scr.LB_SPACE
    sp.cmd("moveDown")
    sp.cmd("moveLineStart")
    sp.cmd("deleteBackward")
    assert (sp.line == 17) and (sp.column == 0)
    assert sp.lines[16].lb == scr.LB_SPACE
    assert sp.lines[16].text == "A calm night, with the ocean almost still."\
           " Two fishermen are"
    assert sp.lines[17].text == "smoking at the rear deck."

def testBackLbNone():
    sp = u.load()

    sp.gotoPos(20, 0)
    assert sp.lines[19].lb == scr.LB_NONE
    sp.cmd("deleteBackward")
    assert (sp.line == 19) and (sp.column == 34)
    assert sp.lines[19].text == "Aye,it'snightslikethisthatmakemeree"
    assert sp.lines[20].text == "mber why I love being a fisherman."
    assert sp.lines[19].lb == scr.LB_NONE
    sp.cmd("moveRight", count = 3)
    sp.cmd("addChar", char = " ")
    sp.cmd("moveLeft", count = 2)
    sp.cmd("deleteBackward")
    assert (sp.line == 19) and (sp.column == 34)
    assert sp.lines[19].text == "Aye,it'snightslikethisthatmakemerem"
    assert sp.lines[20].text == "ber why I love being a fisherman."
    assert sp.lines[19].lb == scr.LB_SPACE

def testBackLbForced():
    sp = u.load()

    sp.gotoPos(34, 0)
    assert sp.lines[33].lb == scr.LB_FORCED
    sp.cmd("deleteBackward")
    assert (sp.line == 33) and (sp.column == 6)
    assert sp.lines[33].text == "brightyellow package at their feet."
    assert sp.lines[33].lb == scr.LB_LAST

# test that when joining two elements of different type, the latter of
# which contains forced linebreaks, that the whole of the latter element
# is rewrapped correctly.
def testBackLbForcedTypeConvert():
    sp = u.load()

    sp.cmd("toTransition")
    sp.cmd("moveDown", count = 3)
    sp.cmd("insertForcedLineBreak")
    sp.cmd("moveUp")
    sp.cmd("deleteBackward")

    sp._validate()

# FIXME: more tests for forward deletion

# test that when joining two elements of different type, the latter of
# which contains forced linebreaks, that the whole of the latter element
# is rewrapped correctly.
def testForwardLbForcedTypeConvert():
    sp = u.load()

    sp.cmd("toTransition")
    sp.cmd("moveDown", count = 3)
    sp.cmd("insertForcedLineBreak")
    sp.cmd("moveUp", count = 2)
    sp.cmd("moveLineEnd")
    sp.cmd("deleteForward")

    sp._validate()

# test deleting the previous word in the middle of a line
def testDeletePreviousWordInMiddleOfLine():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, len("One Two"))
    sp.cmd("deletePreviousWord")

    assert sp.lines[0].text == "One  Three"

# test deleting the next word in the middle of a line
def testDeleteNextWordInMiddleOfLine():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, len("One "))
    sp.cmd("deleteNextWord")

    assert sp.lines[0].text == "One  Three"

# test deleting the previous word when the previous character is a space.
# the space and the word after it should be deleted
def testDeletePreviousWordAfterSpace():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, len("One Two ")) # go to after the space
    sp.cmd("deletePreviousWord")

    assert sp.lines[0].text == "One Three"

# test deleting the next word when the next character is a space.
# the space and the word before it should be deleted
def testDeleteNextWordAfterSpace():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, len("One")) # go to before the space
    sp.cmd("deleteNextWord")

    assert sp.lines[0].text == "One Three"

# Test deleting the previous word when at the start of a line with
# a forced line break in between the lines.
# In this implementation, the line break is simply deleted.
def testDeletePreviousWordAtStartOfLine():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])
    sp.cmd("insertForcedLineBreak")
    sp.paste([scr.Line(text = "Four Five Six", lt = scr.ACTION)])

    sp.gotoPos(1, 0) # go to start of second line.
    sp.cmd("deletePreviousWord")

    assert len(sp.lines) == 1
    assert sp.lines[0].text == "One Two ThreeFour Five Six"

# Test deleting the previous next when at the end of a line with
# a forced line break in between the lines.
# In this implementation, the line break is simply deleted.
def testDeleteNextWordAtEndOfLine():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])
    sp.cmd("insertForcedLineBreak")
    sp.paste([scr.Line(text = "Four Five Six", lt = scr.ACTION)])

    sp.gotoPos(0, len(sp.lines[0].text)) # go to end of first line.
    sp.cmd("deleteNextWord")

    assert len(sp.lines) == 1
    assert sp.lines[0].text == "One Two ThreeFour Five Six"

# Test deleting previous word when the line contains only spaces.
# The preceding spaces should be deleted.
def testDeletePreviousWordSpacesOnly():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])
    sp.cmd("insertForcedLineBreak")
    sp.paste([scr.Line(text = "   ", lt = scr.ACTION)])

    sp.gotoPos(1, len("   "))
    sp.cmd("deletePreviousWord")

    assert len(sp.lines) == 1
    assert sp.lines[0].text == "One Two Three"

# Test deleting previous word when the line contains only spaces.
# The preceding spaces should be deleted.
def testDeleteNextWordSpacesOnly():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])
    sp.cmd("insertForcedLineBreak")
    sp.paste([scr.Line(text = "   ", lt = scr.ACTION)])

    sp.gotoPos(1, 0)
    sp.cmd("deleteNextWord")

    assert len(sp.lines) == 1
    assert sp.lines[0].text == "One Two Three"

# Test deleting previous word, undo function.
def testDeletePreviousWordUndo():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, 7)
    sp.cmd("deletePreviousWord")
    sp.cmd("undo")

    # Text should be restored
    assert sp.lines[0].text == "One Two Three"

    # Cursor position should be the same as before the deletion
    assert sp.column == 7

    # Test redo
    sp.cmd("redo")
    assert sp.lines[0].text == "One  Three"

# Test deleting next word, undo function.
def testDeleteNextWordUndo():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, 4)
    sp.cmd("deleteNextWord")
    sp.cmd("undo")

    # Text should be restored
    assert sp.lines[0].text == "One Two Three"

    # Cursor position should be the same as before the deletion
    assert sp.column == 4

    # Test redo
    sp.cmd("redo")
    assert sp.lines[0].text == "One  Three"

from util import findNextNonSpace, findPreviousNonSpace

def testFindNextNonSpace():
    f = findNextNonSpace
    assert f("One Two", 0) == 0
    assert f("One Two", 3) == 4
    assert f("One    Two", 3) == 7
    assert f(" ", 0) == 1

def testFindPreviousNonSpace():
    f = findPreviousNonSpace
    assert f("One Two", 6) == 6
    assert f("One Two", 3) == 2
    assert f("One    Two", 6) == 2
    assert f(" ", 0) == 0