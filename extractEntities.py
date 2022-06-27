import spacy
import pandas as pd
import functions as fn
import unidecode
import os

nlp = spacy.load('en_core_web_sm')

#Create the EntityRuler
ruler = nlp.add_pipe("entity_ruler")

#List of Entities and Patterns
patterns = [
                {"label": "CRYPTO", "pattern": "Bitcoin"},
                {"label": "CRYPTO", "pattern": "BTC"}
            ]

ruler.add_patterns(patterns)

directory = <directory>
txtWhitePapers = directory + "/txtWhitePapers"

allDyads = pd.DataFrame()

tokenDict = {"AdEx-Whitepaper-v.7.pdf.txt":"adx",
             "ark.pdf.txt":"ark",
             "0x_white_paper.pdf.txt":"zrx",
             "aave-v2-whitepaper.pdf.txt":"aave",
             "Aditus-Whitepaper.pdf.txt":"adi",
             "bitcoin.pdf.txt":"btc",
             "PolkaDotPaper.pdf.txt":"dot",
             "Ethereum_Whitepaper_-_Buterin_2014.pdf.txt":"eth",
             "aiChainwhitepaper-en.pdf.txt":"ait"}

for filename in os.listdir(txtWhitePapers):
    if filename in tokenDict:
        token = tokenDict[filename]
        print(filename)
        print(token)
        with open(txtWhitePapers + "/" + filename) as s:
            s = s.read().splitlines()
            f = []
            for line in s:
                line = unidecode.unidecode(line)
                f.append(line)
            corpus = fn.normalize_corpus(f, text_lower_case=False,
                                         text_lemmatization=False, special_char_removal=True)
            named_entities = []
            for sentence in corpus:
                temp_entity_name = ''
                temp_named_entity = None
                sentence = nlp(sentence)
                for word in sentence:
                    term = word.text
                    tag = word.ent_type_
                    if tag:
                        temp_entity_name = ' '.join([temp_entity_name, term]).strip()
                        temp_named_entity = (temp_entity_name, tag)
                    else:
                        if temp_named_entity:
                            named_entities.append(temp_named_entity)
                            temp_entity_name = ''
                            temp_named_entity = None

            entity_frame = pd.DataFrame(named_entities,
                                        columns=['Entity Name', 'Entity Type'])

            # get the top named entities
            top_entities = (entity_frame.groupby(by=['Entity Name', 'Entity Type'])
                                       .size()
                                       .sort_values(ascending=False)
                                       .reset_index().rename(columns={0 : 'Frequency'}))
            #Exclude entities that are cardinal or ordinal (numbers basically) since we are not interested in them
            top_entities = top_entities.loc[(top_entities['Entity Type'] != 'CARDINAL') & (top_entities['Entity Type'] != 'ORDINAL')]
            temp = pd.DataFrame(columns=['mentions','token'])
            temp['mentions'] = top_entities['Entity Name']
            temp['token'] = token
            allDyads = allDyads.append(temp)
            print('End')
    else:
        pass
allDyads.to_csv("allMentions.csv")
