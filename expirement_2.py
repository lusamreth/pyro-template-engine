import json

from test_subj import VALID_UTILITY_TEST

laidOutScope = {}
layers = {}
scopa = []

# the switch root mechanism is triggered once the the dictionary first
# encountered the nested dictionary
#

# - primary critical switch trigger whenever the crawler first dive into a
# dictionary and saw its first nested dictionary
# - post critical switch trigger after the primary trigger condition is met and
# the crawler encountered its second nested dictionary, in the primary
# dictionary
# - after critical switch trigger after the post critical switch is met, and
# the crawler encounter its subsequent nested dictionary. This particular
# switch is reset to "primary" whenever it met the nested dictionary inside the
# reference nested dict.
construct = {}


def tailCompression(tailLinkedList):
    """
    {
        level: int
        tail : linkedlist<obj>
        root : str
        children: arr<obj>
    }
    """
    ptrs = {}
    highest = None
    curr = tailLinkedList
    while curr.get("tail") is not None:
        currLevel = curr["level"]
        tmp = curr["tail"]

        if highest is None:
            highest = currLevel

        if highest > currLevel:
            # print("ptrs |>", currLevel, curr)
            curr["children"].extend(ptrs[highest])
            highest = currLevel

        del curr["tail"]
        if ptrs.get(currLevel) is None:
            ptrs[currLevel] = [curr]
        else:
            ptrs[currLevel].append(curr)

        curr = tmp

    print("ptrs", ptrs, tailLinkedList)
    fep = ptrs.get(highest)
    return fep.pop() if fep else None


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
            # if len(prev) > 0:
            if True:
                # print("prev", prev.get(level - 1), prev.get(level), key, level)
                upperEchalon = prev.get(level - 1) or {}
                if not key in upperEchalon:
                    childKey["level"] = level
                    childKey["max"] = len(dictKeys)
                    childKey["levelCount"] = 1

                    laidOutScope[level] = childKey
                    # lebeyScope[level] = childKey
                    parents.append(key)

                    temp = {
                        "children": [],
                        "root": key,
                        "level": level + 1,
                        "_first_there": True,
                    }

                    if laidOutScope.get(level - 1) is not None:
                        lbd = laidOutScope[level - 1]
                        scopeLeveled = list(laidOutScope[level - 1].keys())
                        lvCount = lbd["levelCount"]
                        childIndex = scopeLeveled[lvCount - 1]

                        laidOutScope[level - 1][childIndex]["children"].append(key)
                        lastOne = prev.get("lastRoot")

                        prev["lastRoot"] = {
                            "root": scopeLeveled[lvCount - 1],
                            "level": level,
                            "children": [],
                            "tail": lastOne,
                        }

                        print(
                            "tai tia",
                            level,
                            scopeLeveled[lvCount - 1],
                            scopeLeveled,
                            lvCount,
                            len(scopeLeveled),
                        )

                        # if lvCount == len(scopeLeveled) - 2 and level == 2:
                        #     lxc = list(laidOutScope[0].keys())

                        #     if construct.get(lxc[0]) is None:
                        #         construct[lxc[0]] = {"children": []}

                        #     construct[lxc[0]]["children"].append(
                        #         tailCompression(prev["lastRoot"])
                        #     )

                        # construct[key] =
                        # construct[childIndex]["children"].append(temp)

                        # prev["lastRoot"]["children"].append(temp)
                        # prev["lastRoot"]
                        print(
                            "primary critical switch",
                            key,
                            "parent:",
                            scopeLeveled[lvCount - 1],
                            level,
                            "\n",
                        )

                    # BUA here means the deepest in the layer
                    # if prev.get("lastRoot") is not None:
                    #     print("append", laidOutScope.get(2), childIndex)

                    #     prev["lastRoot"]["children"].append(temp)

                    print(
                        "| BUA",
                        key,
                        prev.get("lastRoot"),
                        level,
                        laidOutScope.get(level - 1),
                    )
                    print("\n")
                    print("--- switch root current key : {}".format(key), temp)

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

                        if (
                            prev["lastRoot"]["root"] != scopeLeveled[lvCount - 1]
                            and prev["lastRoot"] is not None
                        ):
                            # if True:
                            # if True:
                            print("\n")
                            # critical switch in this sense means that the
                            # system transistion from nested dictionary ->
                            # higher level
                            print(
                                "post critical switch",
                                # scopeLeveled[lvCount - 1],
                                # level,
                                key,
                                level
                                # temp,
                            )

                            lastOne = prev["lastRoot"].get("tail")

                            def amplify(override=False):
                                if level == 2 or override:
                                    lastOne = None

                                    print(
                                        "| BUA reset tail",
                                        key,
                                        scopeLeveled[lvCount - 1],
                                        # prev["lastRoot"],
                                    )

                                    if construct.get(scopeLeveled[lvCount - 1]) is None:
                                        construct[scopeLeveled[lvCount - 1]] = {
                                            "children": []
                                        }
                                    # if /pt
                                    # if prev["lastRoot"]["tail"] is None:
                                    #     return

                                    # construct[scopeLeveled[lvCount - 1]][
                                    #     "children"
                                    # ].append(prev["lastRoot"])

                                    compressed = tailCompression(prev["lastRoot"])
                                    # compressed["children"].pop()
                                    construct[scopeLeveled[lvCount - 1]][
                                        "children"
                                    ].append(compressed)

                                    prev["lastRoot"] = {
                                        "root": scopeLeveled[lvCount - 1],
                                        "level": level,
                                        "children": [],
                                        "tail": lastOne,
                                    }

                                    # construct[scopeLeveled[lvCount - 1]][
                                    #     "children"
                                    # ].append(tailCompression(prev["lastRoot"]))
                                else:
                                    if prev["lastRoot"]["level"] == level:
                                        prev["lastRoot"] = {
                                            "root": key,
                                            "level": level,
                                            "children": [],
                                            "tail": prev["lastRoot"],
                                        }

                                    # prev["lastRoot"] = {
                                    #     "root": key,
                                    #     "level": level,
                                    #     "children": [],
                                    #     "tail": prev["lastRoot"],
                                    # }

                                    #     print("prunaa", key)

                                    # if construct.get(highestLevel) is None:
                                    #     construct[highestLevel] = {"children": []}
                                    # else:
                                    #     construct[highestLevel]["children"].append(
                                    #         prev["lastRoot"]
                                    #     )

                                    highestLevel = next(
                                        iter(laidOutScope[next(iter(laidOutScope))])
                                    )

                                    print(
                                        "| BUA tail",
                                        key,
                                        scopeLeveled[lvCount - 1],
                                        laidOutScope[level - 2],
                                        prev["lastRoot"],
                                        # childIndex,
                                        # level,
                                    )

                                    # if (
                                    #     laidOutScope[level - 2]["levelCount"]
                                    #     == laidOutScope[level - 2]["max"]
                                    #     and highestLevel is not None
                                    # ):
                                    #     if construct.get(highestLevel) is None:
                                    #         construct[highestLevel] = {"children": []}
                                    #     else:
                                    #         print("prev ", prev["lastRoot"])
                                    #         construct[highestLevel]["children"].append(
                                    #             tailCompression(prev["lastRoot"])
                                    #         )

                                    return

                            amplify()
                        else:
                            # solve non critical issue please
                            print(
                                "after post critical switch",
                                key,
                                prev["lastRoot"],
                                level
                                # scopeLeveled[lvCount - 1],
                            )

                            prev["lastRoot"] = {
                                "root": key,
                                "level": level,
                                "children": [],
                                "tail": prev["lastRoot"],
                            }

                        # prev["lastRoot"]["children"].append(temp)
                        # print("\n")
                        print(
                            "| append",
                            key,
                            "| this belong to",
                            scopeLeveled[lvCount - 1],
                            "temp",
                            temp,
                            prev["lastRoot"],
                            # prev["lastRoot"],
                            # prev["lowestLevelKey"],
                            # laidOutScope.get(level - 1),
                        )

                        laidOutScope[level - 1]["levelCount"] += 1

            simpleWalk(dictionary[key], level=level, prev=prev, temp=temp)
        else:
            if layers.get(key):
                layers[key].remove(key)

            # print("CHILD->", key, dictionary[key])
            # do something with dictionary[k]

    return prev


resu = simpleWalk(VALID_UTILITY_TEST)
# print(json.dumps(resu, indent=4))
fp = open("bbua-v1.json", "w+")
# fpx = open("bbua-v1.json", "w+")
# GREAT PROGRESS SO FAR SO GOOD
print("CONS", *construct["settings"]["children"], sep="\n")

json.dump(construct["settings"]["children"][0], fp)
# json.dump(construct["settings"]["children"][0], fpx)
