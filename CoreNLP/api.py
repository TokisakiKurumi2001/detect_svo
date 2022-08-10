from detect import svo_parser
from debug import debug
import os

DEMO = os.getenv("DEMO")


def mappings(segment_name: str) -> str:
    """
    Maps the missing part into the corresponding mask token
    """
    maps = {'subject': '<ms>', 'verb': '<mv>',
            'object': '<mo>', 'adverbial phrase': '<ma>'}
    return maps[segment_name]


def postprocess_origin_segment(origin_segment):
    """
    If the object string is in the averbial phrase, remove the object
    """
    flag = False
    exist_object = 'object' in origin_segment
    exist_adv = 'adverbial phrase' in origin_segment
    if exist_object and exist_adv:
        object_value = origin_segment['object']
        adv_value = origin_segment['adverbial phrase']
        if object_value in adv_value:
            flag = True
    if flag:
        origin_segment.pop('object')
    # dictionary are passed by reference, there is no need for returning value


def compare_detect_segment(original_sent: str, usr_sent: str) -> str:
    """
    Take 2 params: Original sentence with correct part of the sentence and user corrupted sentence
    Return the masking sentence
    """
    original_segment = svo_parser(preprocess_sentence(original_sent))
    usr_segment = svo_parser(preprocess_sentence(usr_sent))
    postprocess_origin_segment(original_segment)
    debug(f"Original: {original_segment}")
    debug(f"User: {usr_segment}")
    buffer = ""
    missing_keys = []
    for key in original_segment.keys():
        if key not in usr_segment:
            missing_keys.append(key)
            usr_segment[key] = mappings(key)
            buffer += f"Missing {key} "
    buffer = buffer.strip()
    if DEMO:
        print(buffer)
    debug(missing_keys)
    debug(usr_segment)
    mask_sent = " ".join(usr_segment.values()) + "."
    return mask_sent


def preprocess_sentence(sent: str) -> str:
    """
    Add the dot if the sentence is missing the dot
    """
    if sent[-1] != '.':
        sent += '.'
    return sent


if __name__ == "__main__":
    original_sent = "I have worked there for 2 years and a half"
    usr_sent = "I."
    res = compare_detect_segment(original_sent, usr_sent)
    if DEMO:
        print(res)
