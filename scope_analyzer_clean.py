import json
from enum import Enum

from test_subj import VALID_UTILITY_TEST

laidOutScope = {}
layers = {}
scopa = []

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

construct = {}


class FieldType(str, Enum):
    FLATTEN = "flatten"
    NESTED = "nested"

    def __str__(self):
        return self.value


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
    lowest = None

    curr = tailLinkedList
    # print("ptrs", tailLinkedList)
    while curr is not None:
        if curr.get("level") is None:
            break

        currLevel = curr["level"]

        if highest is None:
            highest = currLevel
            lowest = currLevel

        if highest > currLevel:
            curr["children"].extend(ptrs[highest])
            highest = currLevel

        if currLevel < lowest:
            lowest = currLevel

        if curr.get("prev") is not None:
            tmp = curr.get("prev")
            del curr["prev"]
        else:
            tmp = None

        if ptrs.get(currLevel) is None:
            ptrs[currLevel] = [curr]
        else:
            ptrs[currLevel].append(curr)

        curr = tmp

    fep = ptrs.get(highest)
    return fep.pop() if fep else None


def createFlattenNode(key, value):
    # print("APPEND",key)
    return {"root": key, "value": value, "fieldType": str(FieldType.FLATTEN)}

def appendFlattenNode(parent, k,v):

    newNode = createFlattenNode(k,v)
    newNode["parentTrace"] = [*parent["parents"],parent["root"]]

    parent["children"].append(newNode)
    parent["childLength"] += 1

def createParentNode(k,level):
    return {
            "key": k,
            "children": [],
            "next": {},
            "root": k,
            "childLength": 0,
            "level": level,
    }

def structDirectionDenominator(level:int,levelState:dict):

    if level > levelState["localHigh"]:
        levelState["localHigh"] = level
        return "down"

    elif level == levelState["localHigh"]:
        return "equal"

    else:
        levelState["localLow"] = level
        levelState["localHigh"] = levelState["localLow"]

        return "up"

def createPtrForward(nodeScopeInfo,key,level):
    parentNode = createParentNode(key,level)

    def forwardPrevPtr(forwardLength=0):
        nodeScopeInfo["prev"] = {
            **parentNode,
            "prev": nodeScopeInfo["prev"],
            "childLength": 0 + forwardLength,
        }
        pass

    return forwardPrevPtr

def simpleWalk(
    dictionary,
    k="",
    level=0,
    levelState={"localHigh": 0},
    ptr={},
    nodeScopeInfo={"prev": {}},
    # essential for assembling back
):
    offset = 0
    # dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]

    dictKeys = dictionary
    nodeState = {"status": ""}

    print("each line", k, level, levelState, end=" ")

    prevNodeState = levelState.get("state")
    nodeState["status"] = structDirectionDenominator(level,levelState)
    level += 1
    levelState["state"] = nodeState

    forwardPrevPtr = createPtrForward(nodeScopeInfo,k,level)

    # def forwardPrevPtr(add=0):
    #     scopeInfoStore["prev"] = {
    #         "key": k,
    #         "children": [],
    #         "next": {},
    #         "root": k,
    #         "level": level,
    #         "prev": scopeInfoStore["prev"],
    #         "childLength": 0 + add,
    #     }
    #     pass
    def nodeAppender(param=0):
        if nodeScopeInfo.get("assemblyBuffer") is None:
            combinedTails = tailCompression(nodeScopeInfo.get("prev"))
            if combinedTails is None:
                return

            nodeScopeInfo["assemblyBuffer"] = combinedTails


        assembyBuffer = nodeScopeInfo["assemblyBuffer"]
        assemblyBufferChildren = assembyBuffer["children"]
        lvlTracker = assembyBuffer["level"]

        parent = assembyBuffer
        prevCounter = assembyBuffer.get("childLength")

        # adjust the assembly root
        if parent["level"] == level:
            if nodeScopeInfo.get("result") is None:
                nodeScopeInfo["result"] = {}

            nodeScopeInfo["result"][parent["key"]] = assembyBuffer
            nodeScopeInfo["assemblyBuffer"] = createParentNode(k,level)
            # {
            #     "key": k,
            #     "children": [],
            #     "next": {},
            #     "root": k,
            #     "childLength": 0,
            #     "level": level,
            # }

            nodeScopeInfo["result"][k] = nodeScopeInfo["assemblyBuffer"]
            assembyBuffer["childLength"] += 1
            return

        if parent["level"] > level:

            prevResult = nodeScopeInfo["result"]

            nodeScopeInfo["root"] = k
            nodeScopeInfo["prevResult"] = prevResult
            nodeScopeInfo["result"] = {}

            nodeScopeInfo["assemblyBuffer"] = createParentNode(k,level)
            # {
            #     "key": k,
            #     "children": [],
            #     "next": {},
            #     "root": k,
            #     "childLength": 0,
            #     "level": level,
            # }

            nodeScopeInfo["result"]["curr"] = nodeScopeInfo["assemblyBuffer"]
            assembyBuffer["childLength"] += 1
            return

        parentTrace = [parent["root"]]
        while lvlTracker != level - 1:

            if len(assemblyBufferChildren) == prevCounter:
                print("decrease", k, len(assemblyBufferChildren), prevCounter, level, parent)
                prevCounter -= 1

            if len(assemblyBufferChildren) < prevCounter:
                print("decrease", k, len(assemblyBufferChildren), prevCounter)
                prevCounter -= 2

            if assemblyBufferChildren[prevCounter].get("fieldType") == str(FieldType.FLATTEN):
                break

            parentTrace.append(assemblyBufferChildren[prevCounter]["root"])
            nxt_tmp = assemblyBufferChildren[prevCounter]["children"]
            ptmp = assemblyBufferChildren[prevCounter]
            parent = ptmp

            assemblyBufferChildren = nxt_tmp
            # lvlTracker = ptmp["level"]
            lvlTracker += 1
            prevCounter = ptmp["childLength"]

        print("xebec", parent, prevCounter, k)

        assemblyBufferChildren.append(
            {
                "key": k,
                "children": [],
                "next": {},
                "root": k,
                "childLength": 0,
                "level": level,
                "parents": parentTrace,
            }
        )
        parent["childLength"] += 1

    # delta jumper ends here

    # state adjuster
    if prevNodeState is not None:
        # state after first chroot
        if nodeState["status"] == "up":
            if nodeState["status"] == prevNodeState["status"]:
                print(
                    "up ring upward up",
                    k,
                    nodeScopeInfo.get("root"),
                    nodeScopeInfo.get("prev"),
                    level,
                )
                nodeAppender()
                pass

            if prevNodeState["status"] == "down":
                # combinedTails = tailCompression(upLink.get("prev").copy())

                if nodeScopeInfo.get("assemblyBuffer") is None:
                    forwardPrevPtr(1)
                    combinedTails = tailCompression(nodeScopeInfo.get("prev"))
                    nodeScopeInfo["assemblyBuffer"] = combinedTails
                else:
                    lv = nodeScopeInfo["assemblyBuffer"]["level"]

                    if lv < level:
                        nodeAppender()

                print(
                    "up ring upward down",
                    k,
                    level,
                    nodeScopeInfo.get("root"),
                    nodeScopeInfo.get("prev"),
                    "assemblyBuffer",
                    nodeScopeInfo.get("assemblyBuffer"),
                    nodeScopeInfo.get("lowest"),
                    # tailCompression(upLink.get("prev")),
                    level,
                )

            if prevNodeState["status"] == "equal":
                print(
                    "up ring upward equal",
                    k,
                    nodeScopeInfo.get("root"),
                    nodeScopeInfo.get("prev"),
                    level,
                )
                nodeAppender()

        # equalwarddd
        if nodeState["status"] == "equal":
            if prevNodeState["status"] == "down":
                nodeAppender()

            if prevNodeState["status"] == "up":
                print(
                    "up ring equalward up",
                    k,
                    nodeScopeInfo.get("root"),
                    nodeScopeInfo.get("prev"),
                    nodeScopeInfo.get("assemblyBuffer"),
                    level,
                )
                nodeAppender()
                pass

            if prevNodeState["status"] == nodeState["status"]:
                lv = nodeScopeInfo["assemblyBuffer"]["level"]
                nodeAppender()

                print(
                    "up ring equalward equal",
                    k,
                    nodeScopeInfo.get("root"),
                    nodeScopeInfo.get("prev"),
                    nodeScopeInfo.get("assemblyBuffer"),
                    level,
                )

        # downwardddd
        if nodeState["status"] == "down":
            if prevNodeState["status"] == "up":
                # problematic # if u add a new field in luji4DD it will throw
                print("UPOW", prevNodeState["status"], k)
                nodeAppender()

            if prevNodeState["status"] == "equal":
                # problematic # if u add a new field in luji4DD it will throw
                # error downward movement not working

                # if upLink.get("assemblyBuffer") is not None:
                print("problematic", k, nodeScopeInfo)

                if nodeScopeInfo.get("root") is None:
                    nodeScopeInfo[k] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                        "level": level,
                        "childLength": 0,
                    }
                    nodeScopeInfo["prev"] = nodeScopeInfo[k]
                    nodeScopeInfo["root"] = k

                nodeAppender()

                # deltaJumper(1)
                pass

            if nodeState["status"] == prevNodeState["status"]:
                if (
                    nodeScopeInfo.get("lowest") is None
                    or nodeScopeInfo.get("lowest") < level
                ):
                    nodeScopeInfo["lowest"] = level

                print(
                    "up ring downward",
                    k,
                    nodeScopeInfo.get("root"),
                    nodeScopeInfo.get("prev"),
                )

                if nodeScopeInfo.get("root") is None:
                    nodeScopeInfo[k] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                        "level": level,
                        "childLength": 0,
                    }
                    nodeScopeInfo["prev"] = nodeScopeInfo[k]
                    nodeScopeInfo["root"] = k
                else:
                    forwardPrevPtr(0)
                    nodeAppender()

                    print("up ring next", nodeScopeInfo, k)

    # print("cjhildrfen", ptr.get("children"))
    # print("state", state["status"])
    for k in dictKeys:
        print("KKa ", k, dictionary[k])
        if isinstance(dictionary[k], dict):
            levelState["prevKey"] = k
            simpleWalk(dictionary[k], k, level, levelState, ptr, nodeScopeInfo)
        else:
            highLvlParent = nodeScopeInfo["result"].get(levelState["prevKey"])
            if highLvlParent is not None:
                # print("DUAO",highLvlParent.get("children"))
                highLvlParent["children"].append(
                    {
                        "root": k,
                        "parents": [levelState["prevKey"]],
                        "level": level,
                        "children": [],
                        "childLength": 0,
                    }
                )

                nodeScopeInfo["result"]["prevKeyState"] = levelState["prevKey"]
                highLvlParent["childLength"] += 1
                levelState["prevKey"] = k
            else:
                # use the jumper algorithm similar to the deltaJumper
                # as well
                print(
                    "KKA",
                    "key",
                    k,
                    nodeScopeInfo["result"],
                    level,
                    levelState,
                    nodeScopeInfo["root"],
                )
                if nodeScopeInfo["result"].get("prevKeyState") is None:
                    pjumper = nodeScopeInfo["result"][nodeScopeInfo["root"]]
                    print("pjumper", pjumper)
                    pjumperIndex = pjumper["childLength"] - 1

                    while pjumper["level"] < level:
                        pjumper = pjumper["children"][pjumperIndex]

                    appendFlattenNode(pjumper, k, dictionary[k])

                    continue

                prevKey = nodeScopeInfo["result"]["prevKeyState"]
                pks = nodeScopeInfo["result"][prevKey]
                # print("KKA","key",k,scopeInfoStore["result"],len(pks["children"]),pks["childLength"], pks["children"])

                # course index correction
                if pks["childLength"] > len(pks["children"]):
                    pks["childLength"] = len(pks["children"])

                endzone = pks["children"][pks["childLength"] - 1]

                if endzone["level"] == level and endzone.get("children") is not None:
                    newNode = createFlattenNode(k,dictionary[k])
                    print(endzone)
                    newNode["parentsaa"] = [*endzone["parents"],endzone["root"]]
                    endzone["children"].append(newNode)

                prevKey = nodeScopeInfo["result"]["prevKeyState"]
                pks = nodeScopeInfo["result"][prevKey]
                endzone = pks["children"][pks["childLength"] - 1]

                def keyValuePropogation():
                    pass

                if level > endzone["level"]:
                    # if len(endzone["children"]) > endzone["childLength"]:
                    if len(endzone["children"]) > endzone["childLength"]:
                        epas = endzone["childLength"]
                        ezStart = endzone["children"][epas]

                        while (
                            ezStart.get("children") is not None
                            and ezStart["level"] < level - 1
                        ):
                            epas = ezStart["childLength"] - 1
                            ezStart = ezStart["children"][epas]

                        # this one is failinggg.
                        if ezStart.get("children") is not None:
                            appendFlattenNode(ezStart, k, dictionary[k])
                    else:
                        epas = endzone["childLength"] - 1
                        # print(epas,len(endzone["children"]),endzone,k)
                        ezStart = endzone["children"][epas]
                        print("EOUA", epas, endzone["children"], ezStart["level"] - 1)

                        while level - 1 > ezStart["level"]:
                            epas = ezStart["childLength"] - 1
                            ezStart = ezStart["children"][epas]
                            print(
                                "EOUA",
                                epas,
                                ezStart["children"],
                                k,
                                level,
                                ezStart["level"],
                            )
                        appendFlattenNode(ezStart, k, dictionary[k])

                    print("epas start", "KEY", k, endzone, level)


                else:
                    print("ez dz", k, dictionary[k])

                print(
                    "DUOA",
                    levelState["prevKey"],
                    endzone,
                    "value",
                    k,
                    dictionary[k],
                    # pks["children"],
                    pks["childLength"],
                    # scopeInfoStore["result"],
                    nodeScopeInfo["result"]["prevKeyState"],
                )

            prevKey = nodeScopeInfo["result"]["prevKeyState"]
            pks = nodeScopeInfo["result"][prevKey]
            endzone = pks["children"][pks["childLength"] - 1]

            print(
                "LOWAI",
                k,
                dictionary[k],
                level,
                levelState["prevKey"],
                prevKey,
                endzone,
                # scopeInfoStore["result"],
                # scopeInfoStore["result"].get(levelState["prevKey"]),
            )

            # deltaJumper()

    return nodeScopeInfo


# resu = simpleWalk(VALID_UTILITY_TEST)

# print(json.dumps(resu, indent=4))
# fp = open("bbua-v1.json", "w+")

analyzedResult = simpleWalk(VALID_UTILITY_TEST)
del analyzedResult["prev"]
analyzerTestPrefix = "test_results"
analyzerTestFileName = "scope_analyzer_results.json"
refFd = open(
    "{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
    "w+",
)


# GREAT PROGRESS SO FAR SO GOOD

json.dump(analyzedResult, refFd)
