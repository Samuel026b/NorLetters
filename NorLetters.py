import time, sys, requests, re, urllib.parse
average_values = {"E": 12.94, "R": 8.59, "N": 7.66, "T": 7.60, "A": 7.58, "S": 6.46, "I": 6.41, "L": 5.68, "O": 5.57, "D": 3.75, "K": 3.39, "G": 3.34, "M": 3.04, "F": 2.39, "U": 2.26, "P": 2.13, "B": 2.12, "V": 1.96, "H": 1.81, "C": 1.33, "Y": 0.96, "W": 0.73, "J": 0.71, "Å": 0.61, "Ø": 0.61, "Z": 0.15, "X": 0.13, "Æ": 0.09, "Q": 0.03}
user_agent_header = {'User-Agent': 'NorLetters - https://github.com/Samuel026B/NorLetters - samuel.brox026@gmail.com'}
def inName(string, letter):
    count = 0
    total_letters = sum(1 for char in string if char.isalpha())
    for char in string:
        if char == letter:
            count += 1
    percentage = count / total_letters * 100
    return percentage
def find_total_occurences():
  total_occurences = 0
  for item in mylist:
    total_occurences += item.number
  return total_occurences
def WebCrawl(random_page_url):
    random_page_url = urllib.parse.unquote(random_page_url)
    pagestr = f"{random_page_url} "
    random_page_title = random_page_url[30:]
    text_json = requests.get(f"https://no.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={random_page_title}&rvslots=main", headers=user_agent_header).json()
    pages_data = text_json['query']['pages'].values()
    # re.sub(re.compile(r'https?://\S+'), '', pages_data)
    # pages_data.replace("\n", "")
    # pages_data.replace("<ref>", "")
    # pages_data.replace("<br", "")
    for page_data in pages_data:
        if not 'revisions' in page_data:
            print(f"foobar in {random_page_title}")
            continue
        for revision_data in page_data['revisions']:
            page_text = revision_data['slots']['main']['*']
            freq = count_chars(page_text)
            for char, count in freq.items():
                if char.upper() in dcheck:
                  mylist[dcheck.index(char.upper())].number += count
                elif ((char.upper() >= "A" and char.upper() <= "Z") or char.upper() in ["Æ", "Ø", "Å"]) and not char.upper() == "SS":
                  mylist.append(NorLetters(char.upper(), count_letters=count))
                  dcheck.append(char.upper())
    return random_page_url
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
dcheck = []
def count_chars(text):
    """Count the frequency of each character in the given text."""
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq
mylist = []
def print_result(strange_items=[]):
  print(f"Total number of letters: {find_total_occurences()}")
  for item in mylist:
    if item in strange_items:
      print(f'\033[47m\033[30m\033[1m"{item.letter}": {item.number / find_total_occurences() * 100:.2f}% ({item.number})\033[0m (average: {average_values[item.letter]}%)')
    else:
      print(f'"{item.letter}": {item.number / find_total_occurences() * 100:.2f}% ({item.number})')
if len(sys.argv) > 1:
  TYPEofOPERATION = sys.argv[1].upper()
else:
  print('Specify type of operation: Count Letters [of random pages] ("CL") / Count Letters of Given Article ("CLGA") / Find Unusual Site ("FUS") / "More" for what they do.')
  while True:
    TYPEofOPERATION = input("> ").upper()
    if TYPEofOPERATION in ("HELP", "MORE"):
      print('"CL": counts letter statistics of a (given) number of random articles.')
      print('"CLGA": counts letter statistics and finds unusual letter statistics in a (given) article.')
      print('"FUS": finds a random page with unusual letter statistics.')
    else:
      break
if TYPEofOPERATION in ("COUNT_LETTERS_OF_GIVEN_ARTICLE", "CLGA"):
  if len(sys.argv) > 2:
    GivenArticle = sys.argv[2]
  else:
    GivenArticle = input("Article: ")
  AlreadyURL = False
  if len(sys.argv) > 3:
    DIF = float(sys.argv[3])
  else:
    DIF = float(input("Maximum difference in percents: "))
  try:
    if "".join(list(GivenArticle[0:29])) == "https://no.wikipedia.org/wiki/":
      AlreadyURL = True
  except IndexError:
    ...
  if not AlreadyURL:
    GivenArticle = "".join(["https://no.wikipedia.org/wiki/", GivenArticle])
  WebCrawl(GivenArticle)
  strange = []
  for item in mylist:
    item.percent = float(f"{item.number / find_total_occurences() * 100:.2f}")
    if (average_values[item.letter] + DIF < item.percent or average_values[item.letter] - DIF > item.percent):
      strange.append(item)
  sort_descending(mylist)
  print_result(strange)
if TYPEofOPERATION in ("FIND_UNUSUAL_SITE", "FUS"):
  try:
    if len(sys.argv) > 3:
      NUMBERofRUNS = int(sys.argv[3])
    else:
      NUMBERofRUNS = 1
  except ValueError:
    NUMBERofRUNS = 1
  try:
    if len(sys.argv) > 4:
      MinLETTERS = int(sys.argv[4])
    else:
      MinLETTERS = 0
  except ValueError:
    MinLETTERS = 0
  if len(sys.argv) > 2:
    DIF = float(sys.argv[2])
  else:
    while True:
      DIF = float(input("Maximum difference in percents: "))
      if DIF > 10:
        raise ValueError("")
      else:
        break
  if len(sys.argv) > 5:
    if list(sys.argv[5])[-1] == "%":
      sys.argv[5] = "".join(list(sys.argv[5])[0:-2])
    MAXinNAME = float(sys.argv[5])
  print(sys.argv)
  print(f"TYPEofOPERATION = {TYPEofOPERATION},\nDIF = {DIF},\nNUMBERofRUNS = {NUMBERofRUNS},\nMinLetters = {MinLETTERS},\nMAXinNAME = {MAXinNAME}%.")
  for number in range(NUMBERofRUNS):
    Found = False
    webscheckd = 0
    while True:
      dcheck = []
      if Found:
        print(rpurl)
        break
      elif webscheckd > 0:
        if int(list(str(webscheckd - number))[-1]) > 3 or list(str(webscheckd - number))[-1] == "0" or str(webscheckd - number) in ("11", "12", "13"):
          print(f"{webscheckd - number}th fail{BECAUSEtooSHORT}. ({rpurl})")
        if list(str(webscheckd - number))[-1] == "1" and str(webscheckd - number) not in ("11", "12", "13"):
          print(f"{webscheckd - number}st fail{BECAUSEtooSHORT}. ({rpurl})")
        if list(str(webscheckd - number))[-1] == "2" and str(webscheckd - number) not in ("11", "12", "13"):
          print(f"{webscheckd - number}nd fail{BECAUSEtooSHORT}. ({rpurl})")
        if list(str(webscheckd - number))[-1] == "3" and str(webscheckd - number) not in ("11", "12", "13"):
          print(f"{webscheckd - number}rd fail{BECAUSEtooSHORT}. ({rpurl})")
      BECAUSEtooSHORT = ""
      mylist = []
      r = requests.get("https://no.wikipedia.org/wiki/Spesial:Tilfeldig", allow_redirects=False, headers=user_agent_header)
      time.sleep(4)
      rpurl = WebCrawl(r.headers['location'])
      strange = []
      if find_total_occurences() < MinLETTERS:
        BECAUSEtooSHORT = f" and too short ({find_total_occurences()} letters)"
      for item in mylist:
        item.percent = float(f"{item.number / find_total_occurences() * 100:.2f}")
        if (average_values[item.letter] + DIF < item.percent or average_values[item.letter] - DIF > item.percent) and find_total_occurences() >= MinLETTERS and inName(list(rpurl)[30:], item.letter) <= MAXinNAME:
          Found = True
          strange.append(item)
        if find_total_occurences() < MinLETTERS and (average_values[item.letter] + DIF < item.percent or average_values[item.letter] - DIF > item.percent):
          BECAUSEtooSHORT = f", because too short ({find_total_occurences()} letters)"
        if inName(list(rpurl)[30:], item.letter) > MAXinNAME and (average_values[item.letter] + DIF < item.percent or average_values[item.letter] - DIF > item.percent):
          BECAUSEtooSHORT = f", because too many letters that where found unusual are in the title ({list(rpurl)[30:].count(item.letter)} of {sum(1 for char in string if char.isalpha())} letters)"
        if inName(list(rpurl)[30:], item.letter) > MAXinNAME and find_total_occurences() < MinLETTERS and (average_values[item.letter] + DIF < item.percent or average_values[item.letter] - DIF > item.percent):
          BECAUSEtooSHORT = f", because too short ({find_total_occurences()} letters) and too many letters that where found unusual are in the title ({list(rpurl)[30:].count(item.letter)} of {sum(1 for char in string if char.isalpha())} letters)"
      webscheckd += 1
    mylist = sort_descending(mylist)
    print_result(strange)
elif TYPEofOPERATION not in ("COUNT_LETTERS_OF_GIVEN_ARTICLE", "CLGA"):
  if len(sys.argv) > 2:
    NUMBERofRUNS = int(sys.argv[2])
  else:
    while True:
      NUMBERofRUNS = int(input("Maximal number of runs: "))
      if NUMBERofRUNS > 100:
        raise ValueError("too many runs - your IP adress may be blocked from Wikipedia.")
      else:
        break
  for WhatEver in range(NUMBERofRUNS):
    try:
      r = requests.get("https://no.wikipedia.org/wiki/Spesial:Tilfeldig", allow_redirects=False, headers=user_agent_header)
      time.sleep(4)
      print(f"{WhatEver + 1}) {WebCrawl(r.headers['location'])}")
    except KeyboardInterrupt:
      print(" KeyboardInterrupt. Here are the result of the articles that were counted:") # Please correct me if my grammar is wrong.
      break
  mylist = sort_descending(mylist)
  print_result()
