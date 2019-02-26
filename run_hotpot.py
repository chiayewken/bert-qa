def create_example_dict(context, answer_start, answer, id, is_impossible, question):
    return {
        "context": context,
        "qas": [
            {
                "answers": [{"answer_start": answer_start, "text": answer}],
                "id": id,
                "is_impossible": is_impossible,
                "question": question,
            }
        ],
    }


def create_para_dict(example_dicts):
    if type(example_dicts) == dict:
        example_dicts = [example_dicts]
    return {"paragraphs": example_dicts}

def add_yes_no(string):
    # Allow model to explicitly select yes/no from text (location front, avoid truncation)
    return " ".join(["yes", "no", string])

def convert_hotpot_to_squad_format(
    json_dict, gold_paras_only=True, combine_context=True
):
    new_dict = {"data": []}
    count = 0
    for example in json_dict:
        context_paras = example["context"]
        if gold_paras_only:
            support = {
                para_title: line_num
                for para_title, line_num in example["supporting_facts"]
            }
            context_paras = [lst for lst in example["context"] if lst[0] in support]

        contexts = ["".join(lst[1]) for lst in context_paras]
        if combine_context:
            contexts = [" ".join(contexts)]

        answer = example["answer"]
        for context in contexts:
            context = add_yes_no(context)
            answer_start = context.index(answer) if answer in context else -1

            new_dict["data"].append(
                create_para_dict(
                    create_example_dict(
                        context=context,
                        answer_start=answer_start,
                        answer=answer,
                        id=str(count),  # SquadExample.__repr__ only accepts type==str
                        is_impossible=(answer_start == -1),
                        question=example["question"],
                    )
                )
            )
            count += 1
    return new_dict
