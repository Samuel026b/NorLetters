import re

text = "C\nheck \no\nut \nthis web\nsite\n: url\n=http://web.archive.org/web/20140118090047/http://www.oscars.org/awards/academyawards/legacy/ceremony/61st-winners.html"

pattern = re.compile(r'https?://\S+')
text_without_url = re.sub(re.compile(r'https?://\S+'), '', text)
text_without_url = text_without_url.replace("\n", "")

print(text_without_url)