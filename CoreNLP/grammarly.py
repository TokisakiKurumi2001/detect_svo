from nltk.parse.corenlp import CoreNLPParser
import re

def parse_tree(sentence):
    parser = CoreNLPParser()
    # sentence = re.sub(r"[.]", "", sentence)
    tree = next(parser.parse_text(sentence))
    svo = {
        "subject": "",
        "verb": "",
        "object": "",
        "adv": ""
    }
    # print(tree)
    tree.pretty_print()
    subtree = tree[0]

    print(f"This is subtree:\n{subtree[2]}")

    if len(subtree) >= 3:
        vp_index = 1
        if len(subtree) == 4: # exist adverb_of_freq, so VP index is pushed back
            vp_index = 2
        if subtree[0].label() == "NP" and subtree[vp_index].label() == "VP":
            svo["subject"] = " ".join(subtree[0].leaves())

            # detect verbs
            verbs = []
            subtree = subtree[vp_index]
            # print(subtree)
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
    return svo

if __name__ == "__main__":
    sentence = "I have worked there for 2 years and a half."
    svo = parse_tree(sentence)
    print(svo)