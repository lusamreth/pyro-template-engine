import json
from enum import Enum

from utils import makeNodeAppender, tailCompression

# the switch root mechanism is triggered once the the dictionary first
# enchildLengthed the nested dictionary
#

# - primary critical switch trigger whenever the crawler first dive into a
# dictionary and saw its first nested dictionary
# - post critical switch trigger after the primary trigger condition is met and
# the crawler enchildLengthed its second nested dictionary, in the primary
# dictionary
# - after critical switch trigger after the post critical switch is met, and
# the crawler enchildLength its subsequent nested dictionary. This particular
# switch is reset to "primary" whenever it met the nested dictionary inside the
# reference nested dict.


class FieldType(str, Enum):
    FLATTEN = "flatten"
    NESTED = "nested"

    def __str__(self):
        return self.value



def createFlattenNode(key, value, level=-1, parent=[]):
    # print("APPEND",key)
    # if len(parent) == 0:

    return {
        "root": key,
        "value": value,
        "fieldType": str(FieldType.FLATTEN),
        "level": level,
        "parent": parent,
    }


def appendFlattenNode(parent, k, v, level=-1):
    newNode = createFlattenNode(k, v, level)
    # print('pjumper jumper',*parent.get("parent"))

    if parent.get("parent") is not None:
        newNode["parent"] = [*parent["parent"], parent["root"]]
    else:
        print("no parent")

    parent["children"].append(newNode)
    parent["childLength"] += 1


def structDirectionDenominator(level: int, levelState: dict):
    if level > levelState["localHigh"]:
        levelState["localHigh"] = level
        return "down"

    elif level == levelState["localHigh"]:
        return "equal"

    else:
        levelState["localLow"] = level
        levelState["localHigh"] = levelState["localLow"]

        return "up"


def getDefaultScopeInfo():
    return {"prev": {}}


def getDefaultLevelState():
    return {"localHigh": 0}


def simpleWalk(
    dictionary,
    k="",
    level=0,
    levelState=getDefaultLevelState(),
    ptr={},
    scopeInfoStore=getDefaultScopeInfo(),
    # essential for assembling back
):
    offset = 0
    # dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]

    dictKeys = dictionary
    state = {"status": ""}

    print("each line", k, level, levelState, end=" ")

    prevState = levelState.get("state")
    state["status"] = structDirectionDenominator(level, levelState)

    print("current", state, prevState)
    print("prev state", prevState, state)

    level += 1
    levelState["state"] = state

    def rootRotation():
        if level == 2:
            scopeInfoStore["root"] = k

    def forwardPrevPtr(add=0):
        scopeInfoStore["prev"] = {
            "key": k,
            "children": [],
            "next": {},
            "root": k,
            "level": level,
            "prev": scopeInfoStore["prev"],
            "childLength": 0 + add,
        }
        pass

    nodeAppender = makeNodeAppender(scopeInfoStore,k,level)

    # delta jumper ends here

    if scopeInfoStore.get("result") is not None:
        resultTail = scopeInfoStore["result"].get("prevKeyState")
        if resultTail is not None:
            perm = scopeInfoStore["result"][resultTail]

            if perm["level"] == level:
                highLvlParent = scopeInfoStore["result"].get(levelState["prevKey"])
                scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]

    # state adjuster
    if prevState is not None:
        # state after first chroot
        if state["status"] == "up":
            # root rotate
            rootRotation()
            if state["status"] == prevState["status"]:
                print(
                    "up ring upward up",
                    k,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                    level,
                )
                nodeAppender()
                pass

            if prevState["status"] == "down":
                # combinedTails = tailCompression(upLink.get("prev").copy())

                if scopeInfoStore.get("assemblyBuffer") is None:
                    forwardPrevPtr(0)
                    combinedTails = tailCompression(scopeInfoStore.get("prev"))
                    scopeInfoStore["assemblyBuffer"] = combinedTails
                else:
                    nodeAppender()
                    # if lv < level:
                    #     nodeAppender()

                print(
                    "up ring upward down",
                    k,
                    level,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                    "assemblyBuffer",
                    scopeInfoStore.get("assemblyBuffer"),
                    # tailCompression(upLink.get("prev")),
                    level,
                )

            if prevState["status"] == "equal":
                print(
                    "up ring upward equal",
                    k,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                    level,
                )

                nodeAppender()

        # equalwarddd
        if state["status"] == "equal":
            # whattttt rotate root here?
            # what the fuck??????

            rootRotation()

            if prevState["status"] == "down":
                nodeAppender()

            if prevState["status"] == "up":
                print(
                    "up ring equalward up",
                    k,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                    scopeInfoStore.get("assemblyBuffer"),
                    level,
                )
                nodeAppender()
                pass

            if prevState["status"] == state["status"]:
                nodeAppender()

                print(
                    "up ring equalward equal",
                    k,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                    scopeInfoStore.get("assemblyBuffer"),
                    level,
                )

        # downwardddd
        if state["status"] == "down":
            if prevState["status"] == "up":
                # problematic # if u add a new field in luji4DD it will throw
                nodeAppender()

            if prevState["status"] == "equal":
                # problematic # if u add a new field in luji4DD it will throw
                # error downward movement not working
                # forwardPrevPtr()
                # if upLink.get("assemblyBuffer") is not None:
                print("problematic", k, scopeInfoStore)

                if scopeInfoStore.get("root") is None:
                    scopeInfoStore[k] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                        "level": level,
                        "childLength": 0,
                    }
                    scopeInfoStore["prev"] = scopeInfoStore[k]
                    scopeInfoStore["root"] = k

                nodeAppender(0)

                # deltaJumper(1)
                pass

            if state["status"] == prevState["status"]:

                print(
                    "up ring downward",
                    k,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                )

                if scopeInfoStore.get("root") is None:
                    scopeInfoStore[k] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                        "level": level,
                        "childLength": 0,
                    }
                    scopeInfoStore["prev"] = scopeInfoStore[k]
                    scopeInfoStore["root"] = k
                else:
                    forwardPrevPtr(0)
                    nodeAppender()

    # print("cjhildrfen", ptr.get("children"))
    # print("state", state["status"])

    # fix main prev key not switch
    for k in dictKeys:
        value = dictionary[k]
        if isinstance(dictionary[k], dict):
            levelState["prevKey"] = k
            simpleWalk(
                value,
                k=k,
                level=level,
                levelState=levelState,
                ptr=ptr,
                scopeInfoStore=scopeInfoStore,
            )
        else:
            if scopeInfoStore.get("result") is None:
                scopeInfoStore["result"] = {}
                scopeInfoStore["result"][k] = createFlattenNode(k, value, level, k)
                levelState["prevKey"] = k
                continue

            highLvlParent = scopeInfoStore["result"].get(levelState["prevKey"])
            print("hilko", highLvlParent, k, level)
            if highLvlParent is not None:
                # this condition will trigger on the first entry element inside
                # a nested dictionary. For Instance :
                """
                "settings": {
                    # "cmd": "pulsectl %sos",
                    "xda": 100,
                    .....

                The key "xda" will be fitted into this condition
                """

                print("HLVV", highLvlParent["level"], level, k,value, scopeInfoStore)

                ## questionable solution ????
                if (
                    highLvlParent["level"] > level
                    or (
                        highLvlParent["level"] == level
                        and level == 1
                    ) 
                ):
                    scopeInfoStore["result"][k] = createFlattenNode(
                        k, value, level, [levelState["prevKey"]]
                    )

                else:
                    if highLvlParent["level"] < level:
                        scopeInfoStore["assemblyBuffer"]["children"].append(
                            createFlattenNode(k, value, level,
                                              [scopeInfoStore["assemblyBuffer"]["root"]])
                        )
                        pass
                    else:
                        highLvlParent["children"].append(
                            createFlattenNode(k, value, level, [levelState["prevKey"]])
                        )

                        highLvlParent["childLength"] += 1
                        scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]
                        levelState["prevKey"] = k

                print("LEVAL", highLvlParent, k)
            else:
                # use the jumper algorithm similar to the deltaJumper
                # as well
                print("hilko ew", scopeInfoStore["result"].get("prevKeyState"))

                currRootResult = scopeInfoStore["result"][scopeInfoStore["root"]]
                if currRootResult["level"] > level:
                    scopeInfoStore["result"][k] = createFlattenNode(k,value,level,parent=[])
                    continue

                if scopeInfoStore["result"].get("prevKeyState") is None:
                    print(scopeInfoStore["result"])
                    pjumper = scopeInfoStore["result"][scopeInfoStore["root"]]
                    pjumperIndex = pjumper["childLength"] - 1

                    print(
                        "PJ PROSPOS readjust",
                        k,
                        pjumper["childLength"],
                        len(pjumper["children"]),
                        level,
                        pjumper["level"],
                        scopeInfoStore["result"],
                    )


                    while pjumper["level"] < level:
                        print(
                            "pjumper loiter",
                            len(pjumper),
                            pjumper["childLength"],
                            pjumper["level"],
                            level,
                            "CHILDREN",
                            pjumper,
                            k,
                            pjumperIndex,
                        )

                        print(
                            "PPPPPP",
                            scopeInfoStore["result"],
                            "INFo",
                            scopeInfoStore["root"],
                            k,
                        )

                        print("\n")
                        print("PJUMP", pjumper["children"], pjumperIndex)

                        pjumper = pjumper["children"][pjumperIndex]
                        pjumperIndex = pjumper["childLength"] - 1

                    appendFlattenNode(pjumper, k, dictionary[k], level)
                    continue

                prevKey = scopeInfoStore["result"]["prevKeyState"]
                resultTail = scopeInfoStore["result"][prevKey]

                # course index correction
                print(
                    "pks", resultTail, prevKey, value, scopeInfoStore["result"], level, prevKey
                )

                if resultTail.get("children") is not None:
                    if resultTail["childLength"] != len(resultTail["children"]):
                        resultTail["childLength"] = len(resultTail["children"])

                resultChildrenTail = resultTail["children"][resultTail["childLength"] - 1]

                print(
                    "KKA",
                    "key",
                    k,
                    level,
                    scopeInfoStore["result"].get("prevKeyState"),
                    resultChildrenTail,
                )
                if resultChildrenTail["level"] == level and resultChildrenTail.get("children") is not None:
                    newNode = createFlattenNode(k, dictionary[k], level)
                    newNode["parent"] = [*resultChildrenTail["parent"], resultChildrenTail["root"]]
                    resultChildrenTail["children"].append(newNode)
                    resultChildrenTail["childLength"] += 1
                    continue

                if level > resultChildrenTail["level"]:
                    if len(resultChildrenTail["children"]) > resultChildrenTail["childLength"]:
                        cTailLength = resultChildrenTail["childLength"]
                        internalTail = resultChildrenTail["children"][cTailLength]

                        while (
                            internalTail.get("children") is not None
                            and internalTail["level"] < level - 1
                        ):
                            cTailLength = internalTail["childLength"] - 1
                            internalTail = internalTail["children"][cTailLength]

                        # this one is failinggg.
                        if internalTail.get("children") is not None:
                            appendFlattenNode(internalTail, k, dictionary[k], level)
                    else:
                        cTailLength = resultChildrenTail["childLength"] - 1
                        internalTail = resultChildrenTail["children"][cTailLength]

                        while level > internalTail["level"]:
                            cTailLength = internalTail["childLength"] - 1
                            internalTail = internalTail["children"][cTailLength]

                        appendFlattenNode(internalTail, k, dictionary[k], level)

                    print("epas start", "KEY", k, resultChildrenTail, level)

                else:
                    value = dictionary[k]
                    previousResult = scopeInfoStore["result"][
                        scopeInfoStore["result"].get("prevKeyState")
                    ]

                    if previousResult["level"] == level:
                        print("ez dz", k, dictionary[k], previousResult, level)
                        previousResult["children"].append(
                            createFlattenNode(
                                k, value, level, [previousResult.get("root")]
                            )
                        )
                        # perform child length course corrector
                        previousResult["childLength"] = len(previousResult["children"])

                    else:
                        # create a flatten node if it the prevResult-level <
                        # current level
                        scopeInfoStore["result"][k] = createFlattenNode(
                            k, value, level, []
                        )

                    print("ez dz", k, dictionary[k], previousResult["level"], level)

                print(
                    "DUOA",
                    "value x",
                    k,
                    levelState["prevKey"],
                    resultChildrenTail,
                    dictionary[k],
                    # pks["children"],
                    resultTail["childLength"],
                    # scopeInfoStore["result"],
                    scopeInfoStore["result"]["prevKeyState"],
                )


            print(
                "LOWAI",
                k,
                dictionary[k],
                level,
                levelState["prevKey"],
                # scopeInfoStore["result"],
                # scopeInfoStore["result"].get(levelState["prevKey"]),
            )

            # deltaJumper()

    return scopeInfoStore


def cleanUpResult(analyzedResult):
    del analyzedResult["prev"]
    if analyzedResult.get("result").get("prevKeyState"):
        del analyzedResult["result"]["prevKeyState"]
    return analyzedResult["result"]


def analyzeScope(dictionary):
    initialLevel = 0
    initialLevelState = getDefaultLevelState()
    initialScopeInfoStore = getDefaultScopeInfo()
    initialPointer = {}

    analyzedResult = simpleWalk(
        dictionary,
        k="",
        level=initialLevel,
        levelState=initialLevelState,
        ptr=initialPointer,
        scopeInfoStore=initialScopeInfoStore,
    )

    cleaned = cleanUpResult(analyzedResult)
    # analyzerTestPrefix = "test_results"
    # analyzerTestFileName = "scope_analyzer_results.json"
    # refFd = open(
    #     "{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
    #     "w+",
    # )
    # json.dump(cleaned, refFd)
    return cleaned


