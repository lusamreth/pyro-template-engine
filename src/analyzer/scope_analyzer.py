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

    return {
        "root": key,
        "value": value,
        "fieldType": str(FieldType.FLATTEN),
        "level": level,
        "parent": parent,
    }


def appendFlattenNodeToParent(parent, k, v, level=-1):
    newNode = createFlattenNode(k, v, level)
    # print('pjumper jumper',*parent.get("parent"))

    if parent.get("parent") is not None:
        newNode["parent"] = [*parent["parent"], parent["root"]]

    parent["children"].append(newNode)
    parent["childLength"] += 1

"""
A struct denominator is used to track the direction state of the nesting level 
by comparing the current level to the previous highest or lowest level. 
If any other level is :
    - lower : 
or higher it will 
"""
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
    return {
        "prev": {},
    }


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


class NodeStateHandler:
    def __init__(self, prevState, currentState, scopeInfoStore):
        self.prevState = prevState
        # self.dictionary = dictionary
        self.currentState = currentState
        self.scopeInfoStore = scopeInfoStore

    pass


class NodeTraverser:
    def __init__(self, prevState, currentState, scopeInfoStore):
        self.prevState = prevState
        # self.dictionary = dictionary
        self.currentState = currentState
        self.scopeInfoStore = scopeInfoStore

    def rootRotation(self, target, level):
        if level == 2:
            self.scopeInfoStore["root"] = target

    def forwardPrevPtr(self, k, level, add=0):
        self.scopeInfoStore["prev"] = {
            "key": k,
            "children": [],
            "next": {},
            "root": k,
            "level": level,
            "prev": self.scopeInfoStore["prev"],
            "childLength": 0 + add,
        }

    def makeNodeHandler(self, key, level, prevState):
        scopeInfoStore = self.scopeInfoStore
        nodeAppender = makeNodeAppender(scopeInfoStore, key, level)

        def stateUpNodeHandler():
            # root rotate
            self.rootRotation(target=key, level=level)

            def forwarder():
                if scopeInfoStore.get("assemblyBuffer") is None:
                    self.forwardPrevPtr(k=key, level=level)
                    combinedTails = tailCompression(scopeInfoStore.get("prev"))
                    scopeInfoStore["assemblyBuffer"] = combinedTails
                else:
                    nodeAppender()

            mirrorState = nodeAppender
            opsMatcher = structStateMatcher(
                onUp=mirrorState, onDown=forwarder, onEqual=nodeAppender
            )
            opsMatcher.match(prevState["status"])

        def stateDownNodeHandler():
            def equalState():
                if scopeInfoStore.get("root") is None:
                    initializeScopeInfo(scopeInfoStore, key, level)

                nodeAppender(0)

            def mirrorState():
                if scopeInfoStore.get("root") is None:
                    initializeScopeInfo(scopeInfoStore, key, level)
                else:
                    self.forwardPrevPtr(k=key, level=level)
                    nodeAppender()

            opsMatcher = structStateMatcher(
                onUp=nodeAppender, onDown=mirrorState, onEqual=equalState
            )

            opsMatcher.match(prevState["status"])

        def stateEqualNodeHandler():
            self.rootRotation(target=key, level=level)
            nodeAppender()

        return stateUpNodeHandler, stateDownNodeHandler, stateEqualNodeHandler

    def addNodeToTree(self, key, level):
        prevState = self.prevState
        currentState = self.currentState

        if prevState is not None:
            (
                stateUpNodeHandler,
                stateDownNodeHandler,
                stateEqualNodeHandler,
            ) = self.makeNodeHandler(key, level, prevState)

            treeDirectionMatcher = structStateMatcher(
                onUp=stateUpNodeHandler,
                onDown=stateDownNodeHandler,
                onEqual=stateEqualNodeHandler,
            )

            treeDirectionMatcher.match(currentState["status"])

    pass


class SimpleTreeWalker:
    def __init__(self):
        self.dictionary = {}
        self.currKey = ""

        # pointer state
        self.levelState = getDefaultLevelState()
        self.scopeInfoStore = getDefaultScopeInfo()
        self.ptr = {}

    def forwardPrevPtr(self, k, level, add=0):
        self.scopeInfoStore["prev"] = {
            "key": k,
            "children": [],
            "next": {},
            "root": k,
            "level": level,
            "prev": self.scopeInfoStore["prev"],
            "childLength": 0 + add,
        }

    def previousKeySetter(self, level):
        scopeInfoStore = self.scopeInfoStore
        if scopeInfoStore.get("result") is None:
            return

        resultTail = scopeInfoStore["result"].get("prevKeyState")
        if resultTail is None:
            return

        prevResult = scopeInfoStore["result"][resultTail]
        if prevResult["level"] == level:
            scopeInfoStore["result"]["prevKeyState"] = self.levelState["prevKey"]

    def treewalk(self, dictionary, key="", level=0):
        dictKeys = dictionary
        currentState = {"status": ""}

        levelState = self.levelState
        scopeInfoStore = self.scopeInfoStore

        prevState = levelState.get("state")
        currentState["status"] = structDirectionDenominator(level, levelState)

        level += 1
        self.levelState["state"] = currentState

        # # state adjuster
        self.previousKeySetter(level)
        if prevState is not None:
            nodeTraverser = NodeTraverser(prevState, currentState, scopeInfoStore)
            nodeTraverser.addNodeToTree(key, level)

        # fix main prev key not switch
        for key in dictKeys:
            value = dictionary[key]
            if isinstance(dictionary[key], dict):
                levelState["prevKey"] = key
                self.treewalk(
                    value,
                    key=key,
                    level=level,
                )
            else:
                self.nodeResolver(dictionary, key, level)

        return scopeInfoStore

    def nodeResolver(self, dictionary, key, level):
        levelState = self.levelState
        scopeInfoStore = self.scopeInfoStore
        value = dictionary[key]

        if scopeInfoStore.get("result") is None:
            # initialize new key node
            scopeInfoStore["result"] = {}
            scopeInfoStore["result"][key] = createFlattenNode(key, value, level, [key])
            levelState["prevKey"] = key
            return

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
                scopeInfoStore["result"][key] = createFlattenNode(
                    key, value, level, [levelState["prevKey"]]
                )

            else:
                if upperParentNode["level"] < level:
                    scopeInfoStore["assemblyBuffer"]["children"].append(
                        createFlattenNode(
                            key,
                            value,
                            level,
                            [scopeInfoStore["assemblyBuffer"]["root"]],
                        )
                    )
                    pass
                else:
                    upperParentNode["children"].append(
                        createFlattenNode(key, value, level, [levelState["prevKey"]])
                    )

                    upperParentNode["childLength"] += 1
                    scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]
                    levelState["prevKey"] = key

        else:
            currRootResult = scopeInfoStore["result"][scopeInfoStore["root"]]
            if currRootResult["level"] > level:
                scopeInfoStore["result"][key] = createFlattenNode(
                    key, value, level, parent=[]
                )

                return

            if scopeInfoStore["result"].get("prevKeyState") is None:
                rootJumper = scopeInfoStore["result"][scopeInfoStore["root"]]
                rootJumperIndex = rootJumper["childLength"] - 1

                while rootJumper["level"] < level:
                    rootJumper = rootJumper["children"][rootJumperIndex]
                    rootJumperIndex = rootJumper["childLength"] - 1

                appendFlattenNodeToParent(rootJumper, key, dictionary[key], level)
                return

            prevKey = scopeInfoStore["result"]["prevKeyState"]
            resultTail = scopeInfoStore["result"][prevKey]

            # course index correction
            if resultTail.get("children") is not None:
                if resultTail["childLength"] != len(resultTail["children"]):
                    resultTail["childLength"] = len(resultTail["children"])

            resultChildrenTail = resultTail["children"][resultTail["childLength"] - 1]

            if (
                resultChildrenTail["level"] == level
                and resultChildrenTail.get("children") is not None
            ):
                newNode = createFlattenNode(key, dictionary[key], level)
                newNode["parent"] = [
                    *resultChildrenTail["parent"],
                    resultChildrenTail["root"],
                ]
                resultChildrenTail["children"].append(newNode)
                resultChildrenTail["childLength"] += 1

                return

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
                        appendFlattenNodeToParent(internalTail, key, dictionary[key], level)
                else:
                    cTailLength = resultChildrenTail["childLength"] - 1
                    internalTail = resultChildrenTail["children"][cTailLength]

                    while level > internalTail["level"]:
                        cTailLength = internalTail["childLength"] - 1
                        internalTail = internalTail["children"][cTailLength]

                    appendFlattenNodeToParent(internalTail, key, dictionary[key], level)

            else:
                previousResult = scopeInfoStore["result"][
                    scopeInfoStore["result"].get("prevKeyState")
                ]

                if previousResult["level"] == level:
                    previousResult["children"].append(
                        createFlattenNode(
                            key, value, level, [previousResult.get("root")]
                        )
                    )
                    # perform child length course corrector
                    previousResult["childLength"] = len(previousResult["children"])

                else:
                    # create a flatten node if it the prevResult-level <
                    # current level
                    scopeInfoStore["result"][key] = createFlattenNode(
                        key, value, level, []
                    )

        return scopeInfoStore


def cleanUpResult(analyzedResult):
    del analyzedResult["prev"]
    if analyzedResult.get("result").get("prevKeyState"):
        del analyzedResult["result"]["prevKeyState"]
    return analyzedResult["result"]


def analyzeScope(dictionary):
    treeWalker = SimpleTreeWalker()
    analyzedResult = treeWalker.treewalk(dictionary)

    cleaned = cleanUpResult(analyzedResult)
    # analyzerTestPrefix = "test_results"
    # analyzerTestFileName = "scope_analyzer_results.json"
    # refFd = open(
    #     "{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
    #     "w+",
    # )
    # json.dump(cleaned, refFd)
    return cleaned
