import requests
import hashlib

pswrd = input("Enter your password: ")

hashed_pswrd = hashlib.sha1(pswrd.encode()).hexdigest()
pswrd_key = hashed_pswrd[0:5]
pswrd_rest = hashed_pswrd[5:].upper()

url = "https://api.pwnedpasswords.com/range/" + pswrd_key

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

breached_dict = {}

breached_list = response.text.split("\r\n")
for breached_pswrd in breached_list:
    breached_hash = breached_pswrd.split(":")
    breached_dict[breached_hash[0]] = breached_hash[1]

if  pswrd_rest in breached_dict.keys():
    print("Password has been compromised {0} times.".format(breached_dict[pswrd_rest]))
else:
    print("Password has never been compromised and is safe to use.")