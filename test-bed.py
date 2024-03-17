import time

from grab_layer_newvers import multiLayerParser
from scope_analyzer_prune import analyzeScope
from test_subj import complexNested, continualNest, simpleTest, superNested
from utils import saveToResult

multiGeneratedSample = {
    "b": 10,
    "c": {
        "x": "1",
        "obitu": 1,
        "xba": {
            "param giz": "$[2,3,5,6,8,10]",
        },
        "diz": {"param": 10},
    },
    "a": {
        "b": 1,
        "efo": 2,
        # "dez": "$(adx) -> adx.dez",
        "ad": {"param": 100, "deza": {"p": {"bru": 1}}},
        "ac": "%b",
        "param": 1,
        "adx": {"param": 100, "dez": {"p": "$[1,2,3]"}},
        "x2": {"b": 1},
        "acx": 1,
    },
    "h": 1,
    "dezo": {"p": 1},
}

granularTest = {
    "settings": {
        # "cmd": "pulsectl %sos",
        "xda": 1100,
        "can": 100,
        "volume-new": {
            "xoadi": {
                # "xda": "bruh",
                "can": 10,
                "param": "%xda $[up,down] %can",
                "cmd": "pulsectl %xda",
                "bind": "SHIFT $[a,b]",
            },
            "can": 100,
            "prne": "local",
        },
        "prne": "global",
        "volume": {
            "can": 100,
            # "prne": "local",
            "lumen": {"xabit": "%prne %can", "AA": 10},
            "luji": {
                "prne": 10,
                "bai": "%prne $[1,2] %can",
                "JUJI": 10,
                "xo": {
                    "pp": "%prne d $[1,2]",
                    "xoa": 100,
                    ##
                    "g": {"a": "%prne $[2,3]"},
                },
            },
            "luji2": {"bai": "%prne luji2", "JUJI": 10},
            "luji3": {"bai": "%prne", "JUJI": 10},
            "xoapi": {
                # "xda": "bruh",
                "can": 10,
                "paramai": "%xda $[up,down] %can",
                "cmd": "pulsectl %xda",
                "bind": "SHIFT $[a,b]",
            },
            "luji4": {"bai": "%prne", "JUJI": 10},
            "cmd": {"bai": "%prne", "JUJI": 10},
            "cmd": "pulsectl $[1,2,3] %prne",
            "param": "$[1,2,3] %prne %cmd",
            "bind": "SHIFT $[1,2,3]",
        },
    },
    "bc": 100,
}

testSamples = [
    complexNested,
    continualNest,
    superNested,
    simpleTest,
    multiGeneratedSample,
    granularTest,
]


start = time.time()
for i, testSample in enumerate(testSamples):
    anlScope = analyzeScope(testSample)
    parsed = multiLayerParser(anlScope, testSample)
    saveToResult(parsed, "sample-result-{}".format(i))
print("--- %s seconds ---" % ((time.time() - start) * 1))
