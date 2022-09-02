import csv
import random
import genanki
import requests
import json
with open("words.txt") as f:
    words = f.read().splitlines()

translations = dict()

api_root = "https://linguee-api-v2.herokuapp.com/api/v2"

for word in words:
    trans_resp = requests.get(f"{api_root}/translations", params={"query": word, "src": "fr", "dst": "en"})
    src_resp = requests.get(f"{api_root}/external_sources", params={"query": word, "src": "fr", "dst": "en"})
    local_trans = []
    src_ex = src_resp.json()[0]['src'] # source example
    dst_ex = src_resp.json()[0]['dst']

    for lemma in trans_resp.json():
        for translation in lemma['translations']:
            local_trans.append(translation['text'])

    translations[word] = ((src_ex, dst_ex), local_trans)


my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Word'},
    {'name': 'Translations'},
    {'name': 'Usage-FR'},
    {'name': 'Usage-EN'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Word}}',
      'afmt': '{{FrontSide}}<hr id="translations">{{Translations}}<hr id="usage-fr">{{Usage-FR}}<hr id="usage-en">{{Usage-EN}}',
    },
  ])

my_deck = genanki.Deck(
  2059400110,
  'French')
for word in words:
    ((src_ex, dst_ex), local_trans) = translations[word] 
    my_note = genanki.Note(
            model=my_model,
            fields=[word, ', '.join(local_trans), src_ex, dst_ex]
            )
    my_deck.add_note(my_note)
genanki.Package(my_deck).write_to_file('output.apkg')
