from operator import sub
# from stat_parser import Parser
from nltk.parse.corenlp import CoreNLPParser
import re

def parse_tree(sentence):
    # parser = Parser()
    parser = CoreNLPParser()
    sentence = re.sub(r"[.]", "", sentence)
    # tree = parser.parse(sentence)
    tree = next(parser.parse_text(sentence))
    svo = {
        "subject": "",
        "verb": "",
        "object": "",
        "adv": ""
    }
    # print(tree)
    tree.pretty_print()
    tree = tree[0]
    for i, subtree in enumerate(tree.subtrees()):
        if i == 0:
            # print(subtree, len(subtree))
            if subtree.label() == "NP":
                svo["subject"] = " ".join(subtree.leaves())
            elif len(subtree) >= 2:
                if subtree[0].label() == "NP" and subtree[1].label() == "VP":
                    if len(subtree[1]) >= 2:
                        if subtree[1][0].label().startswith("V") and subtree[1][1].label() == "NP": # Correct
                            svo["subject"] = " ".join(subtree[0].leaves())
                            svo["verb"] = " ".join(subtree[1][0].leaves())
                            svo["object"] = " ".join(subtree[1][1].leaves())
                            return svo
                        elif subtree[1][0].label().startswith("V") and subtree[1][1].label() == "PP": # Correct
                            if len(subtree[1][1]) == 2:
                                svo["subject"] = " ".join(subtree[0].leaves())
                                svo["verb"] = " ".join(subtree[1][0].leaves())
                                svo["object"] = " ".join(subtree[1][1].leaves()[1:]) # skip IN: preposition
                                svo["adv"] = " ".join(subtree[1][1].leaves())
                                return svo
                            else: # Missing Adv
                                svo["subject"] = " ".join(subtree[0].leaves())
                                svo["verb"] = " ".join(subtree[1][0].leaves())
                                return svo
                        # elif subtree[1][0].label().startswith("V") and subtree[1][1].label() == "VP": # Correct
                        #     if len(subtree[1][1]) >= 2:
                        #         svo["subject"] = " ".join(subtree[0].leaves())
                        #         svo["verb"] = " ".join(subtree[1][0].leaves() + subtree[1][1][0].leaves())
                        #         if subtree[1][1][1].label().startswith("ADV"):
                        #             svo["object"] = " ".join(subtree[1][1][1].leaves())
                        #         if subtree[1][1][2].label() == "PP":
                        #             if len(subtree[1][1][2]) == 2:
                        #                 svo["adv"] = " ".join(subtree[1][1][2].leaves())
                        #         return svo
                        #     else: # Missing Adv
                        #         svo["subject"] = " ".join(subtree[0].leaves())
                        #         svo["verb"] = " ".join(subtree[1][0].leaves())
                        #         svo["object"] = ""
                        #         svo["adv"] = ""
                        #         return svo
                        # elif subtree[1][0].label().startswith("V") and subtree[1][1].label().startswith("ADVP"): # Correct
                        #     svo["subject"] = " ".join(subtree[0].leaves())
                        #     svo["verb"] = " ".join(subtree[1][0].leaves())
                        #     if subtree[1][1].label().startswith("ADV"):
                        #         svo["object"] = " ".join(subtree[1][1].leaves())
                        #     if subtree[1][2].label() == "PP":
                        #         if len(subtree[1][2]) == 2:
                        #             svo["adv"] = " ".join(subtree[1][2].leaves())
                        #     return svo
                        elif subtree[1][0].label().startswith("V"):
                            count = 0
                            for subsubtree in subtree[1][:]:
                                if subsubtree.label() == "PP":
                                    if len(subtree[1][1]) == 2:
                                        svo["subject"] = " ".join(subtree[0].leaves())
                                        svo["verb"] = " ".join(subtree[1][0].leaves())
                                        svo["object"] = " ".join(subtree[1][1].leaves()[1:]) # skip IN: preposition
                                        svo["adv"] = " ".join(subtree[1][1].leaves())
                                        return svo
                                    else: # Missing Adv
                                        svo["subject"] = " ".join(subtree[0].leaves())
                                        svo["verb"] = " ".join(subtree[1][0].leaves())
                                        return svo
                                if subsubtree.label() == "NP":
                                    count += 1
                            if count == 0: # Missing Object
                                svo["subject"] = " ".join(subtree[0].leaves())
                                svo["verb"] = " ".join(subtree[1][0].leaves())
                                return svo
                    else: # Missing Object
                        svo["subject"] = " ".join(subtree[0].leaves())
                        svo["verb"] = " ".join(subtree[1][0].leaves())
                        return svo
                elif subtree[0].label() == "IN":
                    svo["object"] = " ".join(subtree[1].leaves())
                    svo["adv"] = " ".join(subtree.leaves())
                    return svo
                elif subtree[0].label().startswith("V"): # Missing Subject
                    count = 0
                    if subtree[1].label() == "PP":
                        if len(subtree[1]) < 2: # Missing Object
                            count += 1
                    if count == 0: # Missing Subject
                        svo["verb"] = " ".join(subtree[0].leaves())
                        svo["object"] = " ".join(subtree[1][1].leaves()[1:])
                        svo["adv"] = " ".join(subtree[1][1].leaves())
                        return svo
                    else: # Missing Object
                        svo["verb"] = " ".join(subtree[0].leaves())
                        return svo
                else:
                    count = 0
                    for subsubtree in subtree[:]:
                        if subsubtree.label().startswith("V"):
                            count += 1
                    if count == 0: # Missing Verb
                        svo["subject"] = " ".join(subtree[0].leaves())
                        ls = []
                        if subtree[1].label().startswith("N"):
                            for subsubtree in subtree[1:]:
                                ls += subsubtree.leaves()
                        svo["object"] = " ".join(ls)
                    return svo
            else:
                if subtree[0].label().startswith("V"): # Missing Subject & Object
                    if len(subtree[0]) >= 1:
                        svo["verb"] = " ".join(subtree[0][0].leaves())
                        if subtree[0][1].label() == "PP":
                            if len(subtree[0][1]) >= 2:
                                svo["adv"] = " ".join(subtree[0][1].leaves())
                    return svo
                elif subtree[0].label() == "PRP" or subtree[0].label().startswith("N"): # Missing Verb & Object
                    svo["subject"] = " ".join(subtree[0][0])
                    return svo
                elif subtree[0].label() == "IN": # Missing Subject, Verb, & Adv
                    return svo
        break
    return svo

if __name__ == "__main__":
    sentence = "The dog is running on the grass."
    svo = parse_tree(sentence)
    print(svo)