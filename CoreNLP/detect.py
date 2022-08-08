from cmath import exp
from re import sub
from tkinter import RAISED
from nltk.parse.corenlp import CoreNLPParser
import re
import spacy
nlp = spacy.load("en_core_web_sm")

def finalize():
    # TODO: remove punctuation in part of sentences
    pass

def svo_parser(sentence):
    sentence = re.sub(r'([a-zA-Z])([,.!])', r'\1 \2', sentence)
    svo = dict()

    parser = CoreNLPParser()

    tree = next(parser.parse_text(sentence))
    tree.pretty_print()
    subtree = tree[0] if len(tree) == 1 else tree

    ## START HERE
    children = [tree.label() for tree in subtree]
    vp_index = next((i for i in range(len(children)) if children[i] == "VP"), None) # find first occurence of VP, if not found, return None
    advp_index = "ADVP" in children # always, often, usually, etc.

    if vp_index is not None: # if VERB exists
        # detect subjects
        if children[0] == "NP": # if exists NP at first index => exist subject
            svo["subject"] = " ".join(subtree[0].leaves())

        # detect verbs
        verbs = []
        subtree = subtree[vp_index]
        while ("VB" in subtree[0].label() or "MD" in subtree[0].label()):
            if subtree[0].label() != "MD":
                verbs = verbs + subtree[0].leaves()
            if len(subtree) > 1: # there are cases that have only one child, e.g: S - VP - VBG - running
                if subtree[1].label() == "S":
                    subtree = subtree[1, 0]
                    continue
                if subtree[1].label() == "VP":    
                    subtree = subtree[1]
                else:
                    break
            else:
                break
        svo["verb"] = " ".join(verbs)

        # traverse the middle tree to find Object
        for j in range(1, len(subtree)):
            if subtree[j].label() == "ADVP": # object as "here, there, etc."
                svo["object"] = " ".join(subtree[j].leaves())
                break
            elif subtree[j].label() == "NP":
                svo["object"] = " ".join(subtree[j].leaves())
                for z in range(len(subtree[j])):
                    if subtree[j, z].label() == "NP":
                        svo["object"] = " ".join(subtree[j, z].leaves())
                    elif subtree[j, z].label() == "PP":
                        svo["adverbial phrase"] = " ".join(subtree[j, z].leaves())
            elif subtree[j].label() == "PP":
                svo["adverbial phrase"] = " ".join(subtree[j].leaves())
                for z in range(len(subtree)):
                    if subtree[j, z].label() == "NP":
                        if "object" not in svo:
                            svo["object"] = " ".join(subtree[j, z].leaves())
                        break
    else: # if VERB does not exists, it is hard to detect subject and object -> use spacy for this
        doc = nlp(sent)
        deps = [word.dep_ for word in doc]
        root_index = deps.index("ROOT")
        tokens = sentence.split(' ')
        svo["subject"] = ' '.join(tokens[:root_index+1])
        new_sent = ' '.join(tokens[:root_index+1+advp_index] + ["is"] + tokens[root_index+advp_index+1:])
        svo = svo_parser(new_sent)
        svo.pop('verb', None)

    return svo

if __name__ == "__main__":
    sentences = [
                # "like exercising before sunrise.",
                # "I come here once a week.",
                # "often go running.",
                # "prefer working out with a partner.",
                "I a drink for food every weekends.",
                "I at Step Up."
                # "have been working there for a year and a half.",
                # "am looking for opportunities to learn new things.",
                # "is a 30-minute drive from the city center.",
                # "is a noisy place to live.",
                # "I prefer spending time at home.",
                # "my family usually for food every weekends.",
                # "see my family every two weeks.",
                ]
    for sent in sentences:
        try:
            print(svo_parser(sent))
        except Exception as e:
            print(e, sent)
            pass