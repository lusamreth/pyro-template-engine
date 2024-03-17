import re
import traceback

import tokenizer
from variable_subsitution import NeedleBoxCtxAware


class ParserPipeline:
    def __init__(self, scope_lookup):
        self.scope_lookup = scope_lookup
        self.hints = []
        self.needle_box = None

    def switch_context(self, new_scope):
        self.scope_lookup = new_scope

    def get_hints(self, input_str):
        needle_box = tokenizer.variable_lookup(str(input_str))
        self.needle_box = needle_box
        self.hints.extend(list(needle_box.keys()))
        self.input_str = input_str
        return self

    def apply(self):
        return self.pipeline(self.input_str)

    def pipeline(self, input_str):
        if len(self.hints) == 0:
            self.get_hints(input_str)
        # print("BOO needle", self.needle_box, input_str)
        res = tokenizer.sub_needle_box(self.needle_box, self.scope_lookup, input_str)
        return res


def treesplitter_processor(split_tree):
    output = []

    def subsitute_value(field, value, repl):
        if len(output) == 0:
            for i, field_val in enumerate(value):
                res = {}
                res[field] = repl(field_val)
                output.append(res)
        else:
            for i, field_val in enumerate(value):
                f = output[i].get(field)
                output[i][field] = repl(field_val, f)

    for i, tree in enumerate(split_tree):
        field = tree["field"]
        raw_str = tree["raw_string"]
        matches = tree["matches"]

        for match in matches:
            value = match["value"]
            pattern = match["pattern"]

            def repl(val, stt=raw_str):
                stt = stt or raw_str
                return re.sub(re.escape(pattern), val, stt)

            subsitute_value(field, value, repl)

    return output


def assemble_token_result(split_tree, token_trees, raw):
    # treefields = list(map(lambda x: x["field"], token_trees))
    # f = treefields
    buffer = []
    print("TK TREE", token_trees, sep="\n")
    # must enforce parity check
    parity = None
    for branch in split_tree:
        branch_len = len(branch.keys())
        if parity is None:
            parity = branch_len
        else:
            if branch_len != parity:
                raise Exception(
                    "Encountered Parity problem! All array must be equal length !"
                )

        copied_raw = raw.copy()
        for branch_key in branch.keys():
            val = branch[branch_key]
            # lots of copy !!!
            copied_raw[branch_key] = val

            # buffer.append(copied_raw)
        buffer.append(copied_raw)

    return buffer


def filterDict(dictT):
    newDict = {}
    for d in dictT.keys():
        if not isinstance(dictT[d], dict):
            newDict[d] = dictT[d]

    return newDict


# convert dict with <msg,param,bind> to
def multiCommandParser(
    raw, keywords=["msg", "param", "bind"], pmc_bind=None, force=False
):
    # accumulateKeyword(key, raw[key])
    lookup_dict = raw

    keyWordParser = ParserPipeline(lookup_dict)
    token_trees = []
    ndbC = NeedleBoxCtxAware(lookup_dict)

    if pmc_bind is not None:
        ndbC.contextSwitch(filterDict(pmc_bind))

    raw = ndbC.resolveChainVars()
    print("RAW RAW", raw, pmc_bind, "raw value", lookup_dict)

    if raw is None:
        return "elevate"

    if raw.get("isEmpty") and not force:
        print("raw empty", ndbC.varScope, pmc_bind, raw)
        return {"isEmpty": True, "needleMissings": raw, "replacedScope": ndbC.varScope}

    if force:
        raw = ndbC.varScope

    print("parsed", raw)

    for key in keywords:
        try:
            fmt = str(raw[key])
            pol = keyWordParser.get_hints(fmt)
            bo = keyWordParser.pipeline(fmt)
            lookup_dict[key] = bo
            # keyWordParser.switch_context(lookup_dict)

            print("BOO --> k:{} {} {}".format(bo, key, fmt, lookup_dict))
            raw[key] = bo

            kkb = tokenizer.tokenize_array(raw[key], ["$[", "]"])

            print("KKB", kkb)
            if len(kkb) > 0:
                token_tree = {}

                token_tree["field"] = key
                token_tree["matches"] = kkb
                token_tree["raw_string"] = raw[key]
                token_trees.append(token_tree)

                print("RAW", raw[key], pol.hints, bo, kkb)

        except Exception as e:
            print("EE", e, raw, key)
            traceback.print_exc()
            continue

    split_tree = treesplitter_processor(token_trees)
    return assemble_token_result(split_tree, token_trees, raw)


sample = {
    "prne": "a",
    "msg": "%prne app ",
    # "param": "10 $[1,2,3,4,5,6]",
    "param": "10 $[1,2]",
    "agg": {
        "prne": "b",
        "param": "10 $[1,2] ",
    },
    "bind": "shift",
}

multVars = {
    "prne": "a",
    "msg": "%prne app",
    "param": "10 $[1,4]",
    "bind": "shift $[1,4]",
}

assembled = multiCommandParser(sample)
assembledVar = multiCommandParser(multVars)

print("assmb", *assembled, sep="\n")
print("assmb", *assembledVar, sep="\n")

# ParserPipeline({"var": 1}).get_hints("ahahah %var %do %bean")
# .pipeline(
#     "ahahah %var %do %bean"
# )
# tokenizer.tokenize_array()
