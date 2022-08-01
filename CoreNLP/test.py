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
    
    for i, subtree in enumerate(tree.subtrees()):
        if i == 1:
            if len(subtree) == 3:
                if subtree[0].label() == "NP" and subtree[1].label() == "VP":
                    svo["subject"] = " ".join(subtree[0].leaves())
                    svo["verb"] = " ".join([word for word, pos in subtree[1].pos() if "VB" in pos])

                    # traverse the middle tree to find Object
                    for j, _subtree in enumerate(subtree[1].subtrees()):
                        if _subtree.label() == "NP":
                            svo["object"] = " ".join(_subtree.leaves())
                            break
                else:
                    raise Exception("Something is not right")
            else:
                raise Exception("Something is not right")
            break

    return svo

if __name__ == "__main__":
    sentence = "I prefer spending time at home."
    svo = svo_parser(sentence)
    print(svo)