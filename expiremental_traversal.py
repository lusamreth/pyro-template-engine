import json

laidOutScope = {}
layers = {}
scopa = []

# the switch root mechanism is triggered once the the dictionary first
# encountered the nested dictionary
#

VALID_UTILITY_TEST = {
    "settings": {
        # "cmd": "pulsectl %sos",
        "xda": 100,
        "can": 100,
        "volume": {
            "prne": 1,
            # "lumen": {"xabit": "%prne", "AA": 10},
            "luji2": {"bai": "%prne", "JUJI": 10},
            "luji4": {"bai": "%prne", "wUJI1": {"a": 10}, "2JUJI": {"SBA": 10}},
            "luji": {"bai": "%prne", "JUJI": 10, "xo": 10, "ap": {}},
            # "luji3": {"bai": "%prne", "JUJI": 10},
            # "luji4": {"bai": "%prne", "JUJI": 10},
            # "luji5": {"bai": "%prne", "JUJI": 10},
            "prne": "%can xd",
            "cmd": "pulsectl $[1,2,3] %prne",
            "param": "$[1,2,3] %prne %cmd",
            "bind": "SHIFT $[1,2,3]",
            "bind": "SHIFT $[4,2,3]",
        },
        "volume-new": {
            "cmd": "pulsectl %xda",
            # "xda": "bruh",
            "param": "%cmd $[up,down]",
            "luji2": {
                "bai": "%prne",
            },
            "luji3": {"bai": "%prne", "JUJI": 10},
            "bind": "SHIFT $[a,b]",
            "luji5": {"bai": "%prne", "JUJI": 10},
        },
        "buoa": {},
    },
}


# probing(result2, Utility_VAR)
def simpleWalk(dictionary, level=0, parents=[], prev={"assembles": []}, temp={}):
    offset = 0
    dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]

    for key in dictionary.keys():
        if isinstance(dictionary[key], dict):
            childKeys = [
                k for k in dictionary.keys() if isinstance(dictionary[k], dict)
            ]

            scopa.append(childKeys)
            childKey = {}
            for chk in childKeys:
                # childKey[chk] = {"children": list(dictionary[key].keys())}
                childKey[chk] = {"children": []}

            prev[level] = childKey

            def adjustScopeChildren(scopePoint):
                if laidOutScope.get(level - 1) is not None:
                    lvCount = laidOutScope[scopePoint]["levelCount"]
                    scopeLeveled = list(laidOutScope[scopePoint].keys())
                    childIndex = scopeLeveled[lvCount - 1]

                    # laidOutScope[scopePoint][childIndex]["children"].append(key)
                    laidOutScope[level - 1]["levelCount"] += 1

            # print(key)
            if len(prev) > 0:
                # print("prev", prev.get(level - 1), prev.get(level), key, level)
                upperEchalon = prev.get(level - 1) or {}
                if not key in upperEchalon:
                    childKey["level"] = level
                    childKey["levelCount"] = 1

                    if prev.get("lowestLevel") is None:
                        prev["lowestLevel"] = level
                        prev["lowestLevelKey"] = [key]

                    bugi = prev["lowestLevel"]
                    print("bugi", bugi)
                    if level > bugi:
                        prevBug = prev[bugi]
                        scopeLeveled = list(prevBug.keys())
                        pc = prevBug["levelCount"]
                        prev["lowestLevelKey"].append(key)

                        # temp = {scopeLeveled[pc - 1]: {}, **temp}
                        # temp[scopeLeveled[pc - 1]] = {key: {}}

                        prevKey = None
                        loopNum = bugi
                        tKey = prev["lowestLevelKey"][loopNum]
                        if prevKey is None:
                            tmp = {
                                "rootKey": tKey,
                                "childKey": key,
                                "child": {
                                    key: {
                                        "parent": prev["lowestLevelKey"][
                                            0 : loopNum + 1
                                        ],
                                        "root": key,
                                    },
                                },
                            }
                            prevKey = tmp

                        if prev.get("assemble") is not None:
                            assemble = prev.get("assemble")
                            assemble["combined"] = {
                                assemble["rootKey"]: assemble["child"]
                            }

                        osi = len(prev["assembles"])
                        asmbles = prev["assembles"]
                        prevKeyRunner = None

                        prev["assemble"] = prevKey
                        prev["assembles"].append(prevKey)

                        # print("OSI", osi)
                        print("prev", prev["assemble"], prev["lowestLevel"])
                        while osi > 0 and len(asmbles) > 0:
                            asm = asmbles[osi - 1]
                            rkd = asm["rootKey"]
                            chk = asm["childKey"]

                            if prevKeyRunner is None:
                                prevKeyRunner = {
                                    rkd: {"children": [{chk: asm["child"][chk]}]}
                                }

                            else:
                                prevKeyRunner = {
                                    rkd: {
                                        "children": [
                                            {
                                                **prevKeyRunner,
                                                **asm["child"][chk],
                                            }
                                        ]
                                    }
                                }

                            osi -= 1

                        prev["layers"] = prevKeyRunner
                        # print("asm ---")
                        prev["lowestLevel"] += 1
                    else:
                        if prev.get("layers") is not None:
                            # prev["lowestLevel"] = bugi - level
                            # prev["lowestLevelKey"] = [
                            #     *prev["lowestLevelKey"][0:level],
                            #     key,
                            # ]

                            # # while
                            print(
                                "-- lowest level",
                                level,
                                bugi,
                                key,
                                prev["lowestLevelKey"],
                            )

                        # tmp = {key: dictionary[key]}

                    laidOutScope[level] = childKey
                    # lebeyScope[level] = childKey
                    parents.append(key)
                    # if lebeyScope.get(level - 1) is not None:
                    if laidOutScope.get(level - 1) is not None:
                        lbd = laidOutScope[level - 1]
                        scopeLeveled = list(laidOutScope[level - 1].keys())
                        lvCount = lbd["levelCount"]
                        childIndex = scopeLeveled[lvCount - 1]
                        laidOutScope[level - 1][childIndex]["children"].append(key)

                        print("--- switch", scopeLeveled[lvCount - 1], key, "\n")

                    print("--- switch root current key : {}".format(key))
                    level += 1
                else:
                    if laidOutScope.get(level - 1) is not None:
                        lvCount = laidOutScope[level - 2]["levelCount"]
                        scopeLeveled = list(laidOutScope[level - 2].keys())
                        childIndex = scopeLeveled[lvCount - 1]
                        laidOutScope[level - 2][childIndex]["children"].append(
                            key
                            # {"parent": key, "value": dictionary[key]}
                        )

                        prevLayer = prev.get("layers")

                        # print(json.dumps(prev, indent=2))

                        print(
                            "|",
                            key,
                            "| this belong to",
                            scopeLeveled[lvCount - 1],
                            "lowest",
                            prev["lowestLevelKey"],
                            laidOutScope.get(level - 1),
                        )

                        laidOutScope[level - 1]["levelCount"] += 1

            simpleWalk(dictionary[key], level=level, prev=prev, temp=temp)
        else:
            offset = 0
            if layers.get(key):
                layers[key].remove(key)

            # print("CHILD->", key, dictionary[key])
            # do something with dictionary[k]
            pass
    return prev


resu = simpleWalk(VALID_UTILITY_TEST)
# print(json.dumps(resu, indent=4))
fp = open("bbua.json", "w+")
json.dump(resu["layers"], fp)
