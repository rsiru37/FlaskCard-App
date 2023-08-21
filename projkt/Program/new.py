import requests
base='http://127.0.0.1:5000/api/'
pr=requests.post((base+'user2'),{'deck_name':'translate'})
print(pr.text)
print(pr.status_code)


#putr=requests.put((base+'raj2/'+'mult'),{'deck_name':'Maalt'})
#print(putr.text)

#postr=requests.post((base+'raj/'+'su678b/'+'cards'),{'card_face':'rj','card_back':'sr'})
#print(postr.text)
''''
puter=requests.put((base+'raj/'+'new/'+'cards/'+'29'),{'card_face':'testold','card_back':'testnew'})
print(puter.text)

deli=requests.delete((base+'raj/'+'new/'+'cards/'+'29'))
print(deli.text)
'''

q=requests.get(base+'5')
print(q.text)
