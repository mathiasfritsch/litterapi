import requests



bins = ["red", "green", "yellow","blue"]
results =  [False, False, False,False]
for binIndex in range(4):
  r = requests.get("https://litterapi.azurewebsites.net/api/LitterDate/" + bins[binIndex] )
  print(r.text)
  if r.text == "1":
    results[binIndex] = True
print(results)