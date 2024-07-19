import json, requests

a = open("json/JSON.JSON","r")
print(a)

b =json.load(a)
print(b)


print(a.mode)
c =a.readable
print(c)

print("==============")

for i in b["quiz"]:
    for j in b["quiz"]["questions"]:
        print(j)