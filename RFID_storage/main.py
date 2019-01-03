import nfc

from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

def store_item(uid):

	storage_position = firebase.get("rotation position",None)

	path  = '/items/' + str(uid)

	result = firebase.put(path,"storage position",storage_position)
	return result


def read_id(tag):
    
    tag_id = str(tag)[12:]
    result = store_item(tag_id)
    print result

    return True #Returns to the connect function and keeps listening for new cards.

clf = nfc.ContactlessFrontend()
assert clf.open('tty:AMA0:pn532') is True

tag = clf.connect(rdwr={
    'on-connect': lambda tag:  read_id(tag)
    #lambda tag: False #Simple function that stops the process after the card has been found
    })

