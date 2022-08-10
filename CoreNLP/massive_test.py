import pandas as pd
from api import compare_detect_segment, preprocess_sentence


def compute_score(file_name: str):
    score = 0
    df = pd.read_csv(file_name)
    max_score = len(df)
    for idx in range(max_score):
        origin_sent = df['Origin'].iloc[idx]
        usr_sent = df['Missing'].iloc[idx]
        ground_truth = preprocess_sentence(df['Masking'].iloc[idx])
        try:
            predict, _ = compare_detect_segment(origin_sent, usr_sent)
            if predict == ground_truth:
                score += 1
        except:
            print(
                f"Origin: {origin_sent}, User: {usr_sent}, Truth: {ground_truth}")
            # raise
    return score, max_score


if __name__ == "__main__":
    num_files = 4
    real_scores = []
    max_scores = []
    for i in range(1, num_files+1):
        file_name = f"./data/test/set{i}_test.csv"
        real_score, max_score = compute_score(file_name)
        real_scores.append(real_score)
        max_scores.append(max_score)
    for i, (real_score, max_score) in enumerate(zip(real_scores, max_scores)):
        print(i, real_score, max_score)
