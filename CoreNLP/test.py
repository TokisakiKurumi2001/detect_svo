from cmath import exp
from re import sub
from nltk.parse.corenlp import CoreNLPParser

def svo_parser(sentence):
    svo = {
        "subject": "",
        "verb": "",
        "object": ""
    }

    parser = CoreNLPParser()

    tree = next(parser.parse_text(sentence))
    tree.pretty_print()
    subtree = tree[0]

    if len(subtree) >= 3:
        vp_index = 1
        if len(subtree) == 4: # exist adverb_of_freq, so VP index is pushed back
            vp_index = 2
        if subtree[0].label() == "NP" and subtree[vp_index].label() == "VP":
            svo["subject"] = " ".join(subtree[0].leaves())

            # detect verbs
            verbs = []
            subtree = subtree[vp_index]
            print(subtree)
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
                            if svo["object"] == "":
                                svo["object"] = " ".join(subtree[j, z].leaves())
                            break
        else:
            raise Exception("Something is not right")
    else:
        raise Exception("Something is not right")

    return svo

if __name__ == "__main__":
    sentences = [
                "I like exercising before sunrise.",
                "I come here once a week.",
                "I often go running.",
                "I prefer working out with a partner.",
                "I need a drink.",
                "I have been working there for a year and a half.",
                "I'm looking for opportunities to learn new things.",
                "My house is a 30-minute drive from the city center.",
                "It's a noisy place to live.",
                "I prefer spending time at home.",
                "My family often gather for food on holidays.",
                "I see my family every two weeks.",
                "The most popular dish in my country is Pho."
                ]
    for sent in sentences:
        try:
            print(svo_parser(sent))
        except Exception as e:
            print(e, sent)
            pass