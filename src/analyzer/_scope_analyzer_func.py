import json
from enum import Enum

from test_subj import VALID_UTILITY_TEST

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
    return {"localHigh": 0, "status": ""}


class structStateMatcher:
    def __init__(self, onUp, onDown, onEqual):
        self.onUp = onUp
        self.onDown = onDown
        self.onEqual = onEqual

    def match(self, state):
        match state:
            case "up":
                return self.onUp()
            case "down":
                return self.onDown()
            case "equal":
                return self.onEqual()
            case default:
                raise Exception("Unknown state")


"""
use to initialize empty scope information pointer
"""


def initializeScopeInfo(scopeInfoStore, key, level):
    scopeInfoStore[key] = {
        "key": key,
        "children": [],
        "next": {},
        "root": key,
        "level": level,
        "childLength": 0,
    }
    scopeInfoStore["prev"] = scopeInfoStore[key]
    scopeInfoStore["root"] = key



def simpleWalk(
    dictionary,
    k="",
    level=0,
    levelState=getDefaultLevelState(),
    ptr={},
    scopeInfoStore=getDefaultScopeInfo(),
    # essential for assembling back
):
    dictKeys = dictionary
    currentState = {"status": ""}

    prevState = levelState.get("state")
    currentState["status"] = structDirectionDenominator(level, levelState)

    level += 1
    levelState["state"] = currentState

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

    nodeAppender = makeNodeAppender(scopeInfoStore, k, level)

    if scopeInfoStore.get("result") is not None:
        resultTail = scopeInfoStore["result"].get("prevKeyState")
        if resultTail is not None:
            prevResult = scopeInfoStore["result"][resultTail]

            if prevResult["level"] == level:
                upperParentNode = scopeInfoStore["result"].get(levelState["prevKey"])
                scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]

    # state adjuster
    if prevState is not None:

        def stateUpNodeHandler():
            # root rotate
            rootRotation()

            def mirrorState():
                nodeAppender()

            def forwarder():
                if scopeInfoStore.get("assemblyBuffer") is None:
                    forwardPrevPtr(0)
                    combinedTails = tailCompression(scopeInfoStore.get("prev"))
                    scopeInfoStore["assemblyBuffer"] = combinedTails
                else:
                    nodeAppender()

            opsMatcher = structStateMatcher(
                onUp=mirrorState, onDown=forwarder, onEqual=nodeAppender
            )
            opsMatcher.match(prevState["status"])

        def stateDownNodeHandler():
            def equalState():
                if scopeInfoStore.get("root") is None:
                    initializeScopeInfo(scopeInfoStore, k, level)

                nodeAppender(0)

            def mirrorState():
                if scopeInfoStore.get("root") is None:
                    initializeScopeInfo(scopeInfoStore, k, level)
                else:
                    forwardPrevPtr(0)
                    nodeAppender()

            opsMatcher = structStateMatcher(
                onUp=nodeAppender, onDown=equalState, onEqual=mirrorState
            )

            opsMatcher.match(prevState["status"])

        def stateEqualNodeHandler():
            rootRotation()
            nodeAppender()

        opsMatcher = structStateMatcher(
            onUp=stateUpNodeHandler,
            onDown=stateDownNodeHandler,
            onEqual=stateEqualNodeHandler,
        )

        opsMatcher.match(currentState["status"])

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
                # initialize new key node
                scopeInfoStore["result"] = {}
                scopeInfoStore["result"][k] = createFlattenNode(k, value, level, k)
                levelState["prevKey"] = k
                continue

            # the upper parent node
            upperParentNode = scopeInfoStore["result"].get(levelState["prevKey"])
            if upperParentNode is not None:
                # this condition will trigger on the first entry element inside
                # a nested dictionary. For Instance :
                """
                "settings": {
                    # "cmd": "pulsectl %sos",
                    "xda": 100,
                    .....

                The key "xda" will be fitted into this condition
                """

                ## questionable solution ????
                if upperParentNode["level"] > level or (
                    upperParentNode["level"] == level and level == 1
                ):
                    scopeInfoStore["result"][k] = createFlattenNode(
                        k, value, level, [levelState["prevKey"]]
                    )

                else:
                    if upperParentNode["level"] < level:
                        scopeInfoStore["assemblyBuffer"]["children"].append(
                            createFlattenNode(
                                k,
                                value,
                                level,
                                [scopeInfoStore["assemblyBuffer"]["root"]],
                            )
                        )
                        pass
                    else:
                        upperParentNode["children"].append(
                            createFlattenNode(k, value, level, [levelState["prevKey"]])
                        )

                        upperParentNode["childLength"] += 1
                        scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]
                        levelState["prevKey"] = k

            else:
                # use the jumper algorithm similar to the deltaJumper
                # as well

                currRootResult = scopeInfoStore["result"][scopeInfoStore["root"]]
                if currRootResult["level"] > level:
                    scopeInfoStore["result"][k] = createFlattenNode(
                        k, value, level, parent=[]
                    )
                    continue

                if scopeInfoStore["result"].get("prevKeyState") is None:
                    rootJumper = scopeInfoStore["result"][scopeInfoStore["root"]]
                    rootJumperIndex = rootJumper["childLength"] - 1

                    while rootJumper["level"] < level:
                        rootJumper = rootJumper["children"][rootJumperIndex]
                        rootJumperIndex = rootJumper["childLength"] - 1

                    appendFlattenNode(rootJumper, k, dictionary[k], level)
                    continue

                prevKey = scopeInfoStore["result"]["prevKeyState"]
                resultTail = scopeInfoStore["result"][prevKey]

                # course index correction
                if resultTail.get("children") is not None:
                    if resultTail["childLength"] != len(resultTail["children"]):
                        resultTail["childLength"] = len(resultTail["children"])

                resultChildrenTail = resultTail["children"][
                    resultTail["childLength"] - 1
                ]

                if (
                    resultChildrenTail["level"] == level
                    and resultChildrenTail.get("children") is not None
                ):
                    newNode = createFlattenNode(k, dictionary[k], level)
                    newNode["parent"] = [
                        *resultChildrenTail["parent"],
                        resultChildrenTail["root"],
                    ]
                    resultChildrenTail["children"].append(newNode)
                    resultChildrenTail["childLength"] += 1
                    continue

                if level > resultChildrenTail["level"]:
                    if (
                        len(resultChildrenTail["children"])
                        > resultChildrenTail["childLength"]
                    ):
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

                else:
                    value = dictionary[k]
                    previousResult = scopeInfoStore["result"][
                        scopeInfoStore["result"].get("prevKeyState")
                    ]

                    if previousResult["level"] == level:
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
    analyzerTestPrefix = "test_results"
    analyzerTestFileName = "scope_analyzer_results.json"
    refFd = open(
        "{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
        "w+",
    )
    json.dump(cleaned, refFd)
    return cleaned


def runTestSample():
    # treeWalker = SimpleTreeWalker()
    analyzed = simpleWalk(VALID_UTILITY_TEST)
    # analyzed = treeWalker.treewalk(VALID_UTILITY_TEST)
    del analyzed["prev"]
    analyzerTestPrefix = "test_results"
    analyzerTestFileName = "scope_analyzer_results.json"
    refFd = open(
        "{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
        "w+",
    )

    # GREAT PROGRESS SO FAR SO GOOD
    json.dump(analyzed, refFd)


if __name__ == "__main__":
    runTestSample()
