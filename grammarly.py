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
                                print("Missing Adv")
                        elif subtree[1][0].label().startswith("V"):
                            count = 0
                            for subsubtree in subtree[1][:]:
                                if subsubtree.label() == "PP":
                                    if len(subtree[1][1]) == 2:
                                        return sentence
                                    else:
                                        print("Missing Adv")
                                    count = 1
                                    break
                                if subsubtree.label() == "NP":
                                    count += 1
                            if count == 0:
                                print("Missing Object")
                    else:
                        print("Missing Object")
                elif subtree[0].label() == "IN":
                    print("Missing Subject & Verb")
                elif subtree[0].label().startswith("V"):
                    print("Missing Subject")
                    if subtree[1].label() == "PP":
                        if len(subtree[1]) < 2:
                            print("Missing Object")
                else:
                    count = 0
                    for subsubtree in subtree[:]:
                        if subsubtree.label().startswith("V"):
                            count += 1
                    if count == 0:
                        print("Missing Verb")
            else:
                if subtree.label().startswith("V"):
                    print("Missing Subject & Object")
                elif subtree.label() == "PRP" or subtree.label().startswith("N"):
                    print("Missing Verb & Object/Missing Subject & Verb")
                elif subtree.label() == "IN":
                    print("Missing Subject, Verb, & Adv")
        break

if __name__ == "__main__":
    sentence = "I dont't like."

    parse_tree(sentence)