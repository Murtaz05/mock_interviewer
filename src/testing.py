import json

import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge



results_path = "/home/murtaza/PycharmProjects/tools_interview_project/results/"
# Load JSON file 1
with open(results_path+"test_data1.json", "r") as file1:
    data_1 = json.load(file1)

# Load JSON file 2
with open(results_path+"test_data2.json", "r") as file2:
    data_2 = json.load(file2)


keys_to_keep = ["Resume Summary", "AI - Question"]


# Inspect the first few items of both
print(data_1[:2])  # Print first 2 elements from file 1
print(data_2[:2])  # Print first 2 elements from file 2


def self_bleu(responses):
    scores = []
    for i, response in enumerate(responses):
        other_responses = responses[:i] + responses[i+1:]
        score = max([sentence_bleu([response.split()], other.split()) for other in other_responses])
        scores.append(score)
    return sum(scores) / len(scores)

# diversity_1 = self_bleu(data_1)
# diversity_2 = self_bleu(data_2)
#
# print(f"Self-BLEU Diversity for File 1: {diversity_1:.4f}")
# print(f"Self-BLEU Diversity for File 2: {diversity_2:.4f}")



def analyze_interviews(file_1, file_2):
    with open(file_1, "r") as f1, open(file_2, "r") as f2:
        data_1 = json.load(f1)
        data_2 = json.load(f2)

    # Extract responses
    responses_1 = [item["message"] for item in data_1 if "message" in item]
    responses_2 = [item["message"] for item in data_2 if "message" in item]

    # Calculate BLEU and ROUGE scores
    bleu_scores = [sentence_bleu([response.split()], ref.split()) for response, ref in zip(responses_1, responses_2)]
    rouge_scores = [rouge.get_scores(response, ref)[0]["rouge-l"]["f"] for response, ref in
                    zip(responses_1, responses_2)]

    # Calculate Self-BLEU for diversity
    diversity_1 = self_bleu(responses_1)
    diversity_2 = self_bleu(responses_2)


    # Print results
    print(f"Average BLEU score: {sum(bleu_scores) / len(bleu_scores):.4f}")
    print(f"Average ROUGE score: {sum(rouge_scores) / len(rouge_scores):.4f}")
    print(f"Self-BLEU Diversity for File 1: {diversity_1:.4f}")
    print(f"Self-BLEU Diversity for File 2: {diversity_2:.4f}")

# Call the function with your files
# analyze_interviews("conversation_history_1.json", "conversation_history_2.json")
