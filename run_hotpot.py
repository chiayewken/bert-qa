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


def convert_hotpot_to_squad_format(json_dict):
    new_dict = {"data": []}
    count = 0
    for example in json_dict:
        support = {lst[0]: lst[1] for lst in example["supporting_facts"]}
        context_paras = [lst for lst in example["context"] if lst[0] in support]
        context_joined = " ".join(["".join(lst[1]) for lst in context_paras])
        context_joined = " ".join([context_joined, "yes", "no"])
        answer = example["answer"]
        answer_start = context_joined.index(answer)

        new_dict["data"].append(
            create_para_dict(
                create_example_dict(
                    context=context_joined,
                    answer_start=answer_start,
                    answer=answer,
                    id=str(count),  # SquadExample.__repr__ only accepts type==str
                    is_impossible=False,
                    question=example["question"],
                )
            )
        )
        count += 1
    return new_dict
