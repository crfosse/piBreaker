import nfc

clf = nfc.ContactlessFrontend()
assert clf.open('tty:AMA0:pn532') is True 

#print(clf)

tag = clf.connect(rdwr={'on-connect': lambda tag: False})

print(str(tag)[12:])

clf.close()
