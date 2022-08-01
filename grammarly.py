from operator import sub
from stat_parser import Parser
import re

def parse_tree(sentence):
    parser = Parser()
    sentence = re.sub(r"[.]", "", sentence)
    tree = parser.parse(sentence)
    print(tree)
    for i, subtree in enumerate(tree.subtrees()):
        if i == 0:
            if len(subtree) >= 2:
                if subtree[0].label() == "NP" and subtree[1].label() == "VP":
                    if len(subtree[1]) >= 2:
                        if subtree[1][0].label() == "VB" and subtree[1][1].label() == "NP":
                            return sentence
                        elif subtree[1][0].label() == "VB" and subtree[1][1].label() == "PP":
                            if len(subtree[1][1]) == 2:
                                return sentence
                            else:
                                # print("Missing Adv")
                                return sentence + " " + "<mo>"
                        elif subtree[1][0].label().startswith("V"):
                            count = 0
                            for subsubtree in subtree[1][:]:
                                if subsubtree.label() == "PP":
                                    if len(subtree[1][1]) == 2:
                                        return sentence
                                    else:
                                        # print("Missing Adv")
                                        return sentence + "<mo>"
                                if subsubtree.label() == "NP":
                                    count += 1
                            if count == 0:
                                # print("Missing Object")
                                return sentence + " " + "<mo>"
                    else:
                        # print("Missing Object")
                        return sentence + " " + "<mo>"
                elif subtree[0].label() == "IN":
                    # print("Missing Subject & Verb")
                    return "<ms>" + " " + "<mv>" + " " + sentence
                elif subtree[0].label().startswith("V"):
                    count = 1
                    # print("Missing Subject")
                    if subtree[1].label() == "PP":
                        if len(subtree[1]) < 2:
                            # print("Missing Object")
                            count += 1
                    return "<ms>" + " " + sentence if count == 1 else "<ms>" + " " + sentence + " " + "<mo>"
                else:
                    count = 0
                    for subsubtree in subtree[:]:
                        if subsubtree.label().startswith("V"):
                            count += 1
                    if count == 0:
                        # print("Missing Verb")
                        out = ""
                        if subtree[0].label().startswith("N"):
                            out = out + " ".join(subtree[0].leaves())
                        out += " " + "<mv>" + " "
                        ls = []
                        if subtree[1].label().startswith("N"):
                            for subsubtree in subtree[1:]:
                                ls += subsubtree.leaves()
                            out = out + " ".join(ls)
                        return out
            else:
                if subtree.label().startswith("V"):
                    # print("Missing Subject & Object")
                    return "<ms>" + " " + sentence + " " + "<mo>"
                elif subtree.label() == "PRP" or subtree.label().startswith("N"):
                    # print("Missing Verb & Object/Missing Subject & Verb")
                    return sentence + " " + "<mv>" + " " + "<mo>"
                elif subtree.label() == "IN":
                    # print("Missing Subject, Verb, & Adv")
                    return "<ms>" + " " + "<mv>" + " " + sentence + " " + "<mo>"
        break
    return sentence

if __name__ == "__main__":
    sentence = "I like."
    new_sentence = parse_tree(sentence)
    print(new_sentence)