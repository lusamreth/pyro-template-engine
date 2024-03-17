import json
import time

from grab_layer_newvers import multiLayerParser
from scope_analyzer_prune import analyzeScope
from variable_subsitution import NeedleBoxCtxAware

abdc = {
    "dp": 100,
    "ad": "zzz",
    "controller": "zz %ad",
    "bnest": {
        "controller": "zz %ad internal",
        "dpo": "%controller %ad %ad",
        "uaDI": "",
        "xpat": {
            "am": "%controller ad",
            "controller": "zz %ad internal two",
            "z": "aa %controller %ad",
        },
        "lufa": "%controller",
    },
    "bigugu": "bruhv %controller",
    "bigugua": "bruhv %controller",
}

start = time.time()
bT = {"root": abdc}
# bT["root"] = abdc
abScope = analyzeScope(bT)

parsed = multiLayerParser(abScope, bT)

# p = NeedleBoxCtxAware(abdc).resolveChainVars()
print("parsed", json.dumps(parsed, indent=4))
print("--- %s seconds ---" % ((time.time() - start) * 1))
# print("parsed", json.dumps(p, indent=4))
