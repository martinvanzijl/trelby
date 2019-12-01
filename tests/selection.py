import screenplay as scr
import u

# tests text selection

# helper method to see actual values of strings
def assertEquals(actual, expected):
    if actual != expected:
        print "actual   = [" + actual + "]"
        print "expected = [" + expected + "]"
    assert actual == expected

def testSelectWord():
    sp = u.new()

    sp.paste([scr.Line(text = "One Two Three", lt = scr.ACTION)])

    sp.gotoPos(0, 0)
    sp.selectCurrentWord()
    cd = sp.getSelectedAsCD(False)

    assertEquals(cd.lines[0].text, "One")

    sp.gotoPos(0, len("One "))
    sp.selectCurrentWord()
    cd = sp.getSelectedAsCD(False)

    assertEquals(cd.lines[0].text, "Two")

    sp.gotoPos(0, len("One Two "))
    sp.selectCurrentWord()
    cd = sp.getSelectedAsCD(False)

    assertEquals(cd.lines[0].text, "Three")