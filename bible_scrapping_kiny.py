
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

fields = ["VerseId", "VerseContent", "UntrimmedAudio"]
print('creating CSV file summarizing the data')

f = csv.writer(open('{}.csv'.format("bible_data"), 'w'))
f.writerow(fields)

books = {"MAT": 28,"MRK":16,"LUK":24,"JHN":21,"ACT":28,"ROM":16,"1CO":16,"2CO":13,"GAL":6,"EPH":6,"PHP":4,"COL":4,
"1TH":5,"2TH":3,"1TI":6,"2TI":4,"TIT":3,"PHM":1,"HEB":13,"JAS":5,"1PE":5,"2PE":3,"1JN":5
,"2JN":1,"3JN":1,"JUD":1,"REV":22}

for book in books.keys():
    for chap in range(1,books[book] + 1):
    	print("Scrapping" + book + " " + str(chap))
    	url = "https://www.bible.com/bible/387/" + book + "." + str(chap) + "." +"bird"
    	r = requests.get(url, timeout=20,verify=False)
    	raw_html = r.text
    	soup = BeautifulSoup(raw_html, 'html.parser')
    	chapter = soup.find("div", {"class": "chapter"})
    	audio = "http" + soup.find_all("source")[1]["src"]
    	verses = chapter.findAll("span", {"class": "verse"})
    	for verse in verses:
    		verse_number = verse["data-usfm"]
    		verse_content = verse.find("span", {"class": "content"}).get_text()
    		f.writerow([verse_number, verse_content, audio])


df = pd.read_csv("/Users/Jonathan/Downloads/Umva_dot_ai/bible_data.csv")
clean_df = df[df["VerseContent"] != ' ']
clean_df.to_csv("bible_data_clean.csv")