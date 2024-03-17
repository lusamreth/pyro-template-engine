import re
import traceback

import tokenizer

edgecase = {
    "prne": 10,
    "param": "param : %cmd %prne",
    "cmd": "abc %prne %osmos %osmos",
    "osmos": "gg %prne",
    "chained": "chained : %param %prne %cmd",
    "bbc": "chained : %param %osmos %cmd",
    "xdca": "chained : %param %prne %cmd",
    "xdcbb": "chained : %xdca %prne %cmd",
}


# local line -> needle_box
# necessary to produce variable lookup
edgecase_context = {}


def reworked_variable_lookup(cfg_line, context_key, global_context={}, var_id="%"):
    needle_boxes = {}
    try:
        all_references = re.finditer(f"\\{var_id}(\\w+)", str(cfg_line))
        for refs in all_references:
            needle = refs.group()
            indices = refs.span()
            needle_box = needle_boxes.get(needle)

            if needle_box is not None:
                needle_box.append(indices)
                needle_boxes[needle] = needle_box
            else:
                needle_boxes[needle] = [indices]

        # return needle_boxes
    except Exception as e:
        print("Variable Lookup Failure : ", e)
        print("Aborted")
        traceback.print_exc()

    # global_context.append({context_key: needle_boxes})
    global_context[context_key] = needle_boxes
    return needle_boxes


for edge in edgecase.keys():
    value = edgecase[edge]
    reworked_variable_lookup(value, edge, edgecase_context)
    pass

chainList = {}
for ctx_field in edgecase_context.keys():
    context = edgecase_context[ctx_field]
    print("context", ctx_field, context)
    for needle_box in context:
        needle_field = needle_box[1:]
        if context.get(needle_box) is not None:
            print("param : {} chained with {}".format(ctx_field, needle_field))
            if chainList.get(ctx_field) is None:
                chainList[ctx_field] = [needle_field]
            else:
                chainList[ctx_field].append(needle_field)

            # print("needle", needle_field, context.get(needle_box
        # print("context needle", needle_field, context.get(needle_box))
        pass
    pass


print("chain list", chainList)
print("edge case context", edgecase_context)
