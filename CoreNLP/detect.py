from nltk.parse.corenlp import CoreNLPParser
import re
import spacy
import os
from typing import List, Tuple
nlp = spacy.load("en_core_web_sm")


def edge_reserve(sentence: str, flag: List[int] = None) -> Tuple[str, List[int]]:
    mappings = {'work': 'is', 'like': 'prefer'}
    reverse_mappings = {'is': 'work', 'prefer': 'like'}
    forward = False
    if flag is None:
        forward = True
        flag = [0] * len(mappings.keys())
    if forward:
        for i, word in enumerate(mappings.keys()):
            if word in sentence:
                flag[i] = 1
                sentence = re.sub(word, mappings[word], sentence)
    else:
        for i, word in enumerate(reverse_mappings.keys()):
            if word in sentence and flag[i] == 1:
                sentence = re.sub(word, reverse_mappings[word], sentence)
    return sentence, flag


def finalize():
    # TODO: remove punctuation in part of sentences
    pass


def svo_parser(sentence):
    sentence = re.sub(r'([a-zA-Z])([,.!])', r'\1 \2', sentence)
    sentence, flag = edge_reserve(sentence)
    svo = dict()

    parser = CoreNLPParser()

    tree = next(parser.parse_text(sentence))
    if os.getenv("TREE"):
        tree.pretty_print()
    subtree = tree[0] if len(tree) == 1 else tree

    # START HERE
    children = [tree.label() for tree in subtree]
    np_index = next((i for i in range(len(children))
                    if children[i] == "NP"), None)
    # always, often, usually, etc.
    advp_index = next((i for i in range(len(children))
                      if children[i] == "ADVP"), None)
    # find first occurence of VP, if not found, return None
    vp_index = next((i for i in range(len(children))
                    if children[i] == "VP"), None)

    if vp_index is not None:  # if VERB exists
        # detect subjects
        if np_index is not None:
            svo["subject"] = " ".join(subtree[np_index].leaves())

        # detect verbs
        verbs = []
        subtree = subtree[vp_index]
        while ("VB" in subtree[0].label() or "MD" in subtree[0].label()):
            if subtree[0].label() != "MD":
                verbs = verbs + subtree[0].leaves()
            if len(subtree) > 1:  # there are cases that have only one child, e.g: S - VP - VBG - running
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
            if subtree[j].label() == "ADVP":  # object as "here, there, etc."
                svo["object"] = " ".join(subtree[j].leaves())
            elif subtree[j].label() == "NP":
                if "object" not in svo:
                    svo["object"] = " ".join(subtree[j].leaves())
                for z in range(len(subtree[j])):
                    if subtree[j, z].label() == "NP":
                        if "object" not in svo:
                            svo["object"] = " ".join(subtree[j, z].leaves())
                    elif subtree[j, z].label() == "PP":
                        svo["adverbial phrase"] = " ".join(
                            subtree[j, z].leaves())
            elif subtree[j].label() == "PP":
                svo["adverbial phrase"] = " ".join(subtree[j].leaves())
                for z in range(len(subtree)):
                    if subtree[j, z].label() == "NP":
                        if "object" not in svo:
                            svo["object"] = " ".join(subtree[j, z].leaves())
                        break
    else:  # if VERB does not exists, it is hard to detect subject and object -> use spacy for this
        tokens = sentence.split(' ')
        if advp_index and advp_index != 0:  # Trinh please comment this
            temp_verb_index = 0  # Trinh please comment this
            if np_index is not None:  # Trinh please comment this
                # Trinh please comment this
                temp_verb_index = len(subtree[np_index].leaves())
                # Trinh please comment this
                svo["subject"] = " ".join(subtree[np_index].leaves())
            else:  # Trinh please comment this
                # Trinh please comment this
                svo["subject"] = ' '.join(tokens[:advp_index])
            new_sent = ' '.join(tokens[:temp_verb_index+advp_index] + ["is"] +
                                tokens[temp_verb_index+advp_index:])  # Trinh please comment this
        else:  # Trinh please comment this
            doc = nlp(sentence)  # Trinh please comment this
            deps = [word.dep_ for word in doc]  # Trinh please comment this
            root_index = deps.index("ROOT")  # Trinh please comment this
            # Trinh please comment this
            svo["subject"] = ' '.join(tokens[:root_index+1])
            # Trinh please comment this
            new_sent = ' '.join(
                tokens[:root_index+1] + ["is"] + tokens[root_index+1:])
        svo = svo_parser(new_sent)  # Trinh please comment this
        svo.pop('verb', None)  # Trinh please comment this

    svo['verb'], _ = edge_reserve(svo['verb'], flag)
    return svo


if __name__ == "__main__":
    sentences = [
        # "I have worked there for 2 years."
        # "like exercising before sunrise.",  # khong thay
        # "I come here once a week.",
        # "often go running.",
        # "prefer working out with a partner.",
        # "I a drink for every weekends.",
        # "often a drink.",
        # "I at Step Up.",
        # "have been working there for a year and a half.",
        # "am looking for opportunities to learn new things.",
        # "is a 30-minute drive from the city center.",
        # "is a noisy place to live.",
        # "I prefer spending time at home.",
        # "my family usually for food every weekends.",
        # "see my family every two weeks.",
        # "the bus station usually depart at the weekends.",
        # "I."
        # "I work at."
        "work at Step Up."
    ]
    for sent in sentences:
        try:
            print(svo_parser(sent))
        except Exception as e:
            print(e, sent)
            pass
