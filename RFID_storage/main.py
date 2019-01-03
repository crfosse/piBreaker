import nfc

from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

from multiprocessing import Pool

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

def tag_search():
	print("tag_search")
	'''
	tag = clf.connect(rdwr={
   	 'on-connect': lambda tag:  read_id(tag)
   	 #lambda tag: False #Simple function that stops the process after the card has been found
   	})
	   '''
	return "tag_search"

def check_rotation_pos():
	storage_position = firebase.get("rotation position",None)

	return storage_position


#init:
clf = nfc.ContactlessFrontend()
assert clf.open('tty:AMA0:pn532') is True

#Async:
pool = Pool()
result1 = pool.apply_async(tag_search)
result2 = pool.apply_async(check_rotation_pos)
answer1 = resutl1.get(timeout=10)
answer2 = result2.get(timeout=10)

	
#Postludium:
clf.close()
