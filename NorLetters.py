class NorLetters:
  def __init__(self, letter, count_letters):
    self.letter = letter
    self.number = count_letters
def sort_descending(arr):
  for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
      if arr[j].number > arr[i].number:
        arr[i], arr[j] = arr[j], arr[i]
  return arr
import requests
import pyperclip
dcheck = []
def count_chars(text):
    """Count the frequency of each character in the given text."""
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq
mylist = []
while True:
  NUMBERofRUNS = int(input("> "))
  if NUMBERofRUNS > 100:
    raise ValueError("too many runs - your IP adress may be blocked from Wikipedia.")
  else:
    break
pagestr = ""
for WhatEver in range(NUMBERofRUNS):
  r = requests.get("https://no.wikipedia.org/wiki/Spesial:Tilfeldig", allow_redirects=False)
  random_page_url = r.headers['location']
  pagestr += f"{random_page_url} "
  print(f"{WhatEver + 1}) {random_page_url}")
  random_page_title = random_page_url.split('/')[-1]
  text_json = requests.get(f"https://no.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={random_page_title}&rvslots=main").json()
  pages_data = text_json['query']['pages'].values()
  for page_data in pages_data:
      for revision_data in page_data['revisions']:
          page_text = revision_data['slots']['main']['*']
          freq = count_chars(page_text)
          for char, count in freq.items():
              if char.upper() in dcheck:
                mylist[dcheck.index(char.upper())].number += count
              elif (char.upper() >= "A" and char.upper() <= "Z") or char.upper() in ["Æ", "Ø", "Å"]:
                mylist.append(NorLetters(char.upper(), count_letters=count))
                dcheck.append(char.upper())
total_occurences = 0
for item in mylist:
  total_occurences += item.number
mylist = sort_descending(mylist)
for item in mylist:
  print(f'"{item.letter}": {item.number / total_occurences * 100:.2f}% ({item.number})')
pyperclip.copy(pagestr)