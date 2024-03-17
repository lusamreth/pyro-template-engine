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

    print("ptrs", json.dumps(ptrs, indent=4), highest, tailLinkedList, curr)
    # if curr is not None :

    fep = ptrs.get(highest)
    return fep.pop() if fep else None


def createFlattenNode(key, value):
    # print("APPEND",key)
    return {"root": key, "value": value, "fieldType": str(FieldType.FLATTEN)}

def appendFlattenNode(parent, k,v,parentTrace=[]):

    newNode = createFlattenNode(k,v)
    newNode["parentTrace"] = [*parent["parents"],parent["root"]]

    parent["children"].append(newNode)
    parent["childLength"] += 1

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

def simpleWalk(
    dictionary,
    k="",
    level=0,
    levelState={"localHigh": 0},
    ptr={},
    scopeInfoStore={"prev": {}},
    # essential for assembling back
):
    offset = 0
    # dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]

    dictKeys = dictionary
    state = {"status": ""}

    print("each line", k, level, levelState, end=" ")

    prevState = levelState.get("state")
    state["status"] = structDirectionDenominator(level,levelState)

    # if level > levelState["localHigh"]:
    #     levelState["localHigh"] = level
    #     state["status"] = "down"

    # elif level == levelState["localHigh"]:
    #     state["status"] = "equal"

    # else:
    #     levelState["localLow"] = level
    #     levelState["localHigh"] = levelState["localLow"]

    #     state["status"] = "up"

    print("current", state)
    print("prev state", prevState, state)

    level += 1
    levelState["state"] = state

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

    def nodeAppender(param=0):
        if scopeInfoStore.get("assemblyBuffer") is None:
            # forwardPrev(1)
            combinedTails = tailCompression(scopeInfoStore.get("prev"))
            if combinedTails is None:
                return

            scopeInfoStore["assemblyBuffer"] = combinedTails

        lv = scopeInfoStore["assemblyBuffer"]["level"]
        delta = level - lv

        # print("dt delta", delta, k, upLink["assemblyBuffer"])

        psrv = scopeInfoStore["assemblyBuffer"]
        psrv_children = psrv["children"]
        lvlTracker = psrv["level"]

        parent = psrv
        prevCounter = psrv.get("childLength")

        print(
            "LVA",
            lvlTracker,
            k,
            level,
            parent["level"],
            scopeInfoStore["assemblyBuffer"],
        )

        # adjust root
        if parent["level"] == level:
            if scopeInfoStore.get("result") is None:
                scopeInfoStore["result"] = {}

            #
            rootName = scopeInfoStore["root"]
            print("LVA DD", scopeInfoStore["assemblyBuffer"])

            scopeInfoStore["result"][parent["key"]] = psrv
            scopeInfoStore["assemblyBuffer"] = {
                "key": k,
                "children": [],
                "next": {},
                "root": k,
                "childLength": 0,
                "level": level,
            }
            scopeInfoStore["result"][k] = scopeInfoStore["assemblyBuffer"]
            psrv["childLength"] += 1
            return

        if parent["level"] > level:
            # if upLink.get("result") is None:
            #     upLink["result"] = {}

            prevResult = scopeInfoStore["result"]
            rootName = scopeInfoStore["root"]

            scopeInfoStore["root"] = k
            scopeInfoStore["prevResult"] = prevResult
            scopeInfoStore["result"] = {}

            scopeInfoStore["assemblyBuffer"] = {
                "key": k,
                "children": [],
                "next": {},
                "root": k,
                "childLength": 0,
                "level": level,
            }

            scopeInfoStore["result"]["curr"] = scopeInfoStore["assemblyBuffer"]
            psrv["childLength"] += 1
            return

        parentTrace = [parent["root"]]
        while lvlTracker != level - 1:
            print(
                "Xebec",
                k,
                lvlTracker,
                level,
                prevCounter,
                len(psrv_children)
                # nxt_tmp[prevCounter],
                # "||| _",
                # psrv_children,
            )

            if len(psrv_children) == prevCounter:
                print("decrease", k, len(psrv_children), prevCounter, level, parent)
                prevCounter -= 1

            if len(psrv_children) < prevCounter:
                print("decrease", k, len(psrv_children), prevCounter)
                prevCounter -= 2

            if psrv_children[prevCounter].get("fieldType") == str(FieldType.FLATTEN):
                break

            parentTrace.append(psrv_children[prevCounter]["root"])
            nxt_tmp = psrv_children[prevCounter]["children"]
            ptmp = psrv_children[prevCounter]
            parent = ptmp

            psrv_children = nxt_tmp
            # lvlTracker = ptmp["level"]
            lvlTracker += 1
            prevCounter = ptmp["childLength"]

        print("xebec", parent, prevCounter, k)

        psrv_children.append(
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

    if scopeInfoStore.get('result')is not None:
        pks = scopeInfoStore["result"].get("prevKeyState")
        perm = scopeInfoStore["result"][pks]

        if perm["level"] == level:
            highLvlParent = scopeInfoStore["result"].get(levelState["prevKey"])
            scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]
    if k == "app":
        print("APPP EOP",k,state["status"],scopeInfoStore.get("result")["prevKeyState"],level)
        # scopeInfoStore["result"]["prevKeyState"] = k
        pass
    lvd = scopeInfoStore.get("result")

    # if lvd:
    #     pks = lvd["prevKeyState"]
    #     if scopeInfoStore.get(pks) is not None:
    #         pkv = scopeInfoStore[pks]
    #         print("PKKAV",pks,k,pkv["level"],level)

    #         if pkv["level"] == level:
    #             scopeInfoStore["result"]["prevKeyState"] = k


        # lv = scopeInfoStore["result"][pkv]["level"]
        # if lv == level:
        #     scopeInfoStore["result"]["prevKeyState"] = k

    # state adjuster
    if prevState is not None:
        # state after first chroot
        if state["status"] == "up":
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
                    lv = scopeInfoStore["assemblyBuffer"]["level"]

                    if lv < level:
                        nodeAppender()

                print(
                    "up ring upward down",
                    k,
                    level,
                    scopeInfoStore.get("root"),
                    scopeInfoStore.get("prev"),
                    "assemblyBuffer",
                    scopeInfoStore.get("assemblyBuffer"),
                    scopeInfoStore.get("lowest"),
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
                lv = scopeInfoStore["assemblyBuffer"]["level"]
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
                print("UPOW", prevState["status"], k)
                nodeAppender()

            if prevState["status"] == "equal":
                # problematic # if u add a new field in luji4DD it will throw
                # error downward movement not working

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

                nodeAppender()

                # deltaJumper(1)
                pass

            if state["status"] == prevState["status"]:
                if (
                    scopeInfoStore.get("lowest") is None
                    or scopeInfoStore.get("lowest") < level
                ):
                    scopeInfoStore["lowest"] = level

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

                    print("up ring next", scopeInfoStore, k)

    # print("cjhildrfen", ptr.get("children"))
    # print("state", state["status"])


    # fix main prev key not switch
    for k in dictKeys:
        if k == "telegram":
            print("KKa ", "key",k, dictionary[k],level,levelState,
                    scopeInfoStore["root"],
                    scopeInfoStore["result"]
                  )
            pass

        if isinstance(dictionary[k], dict):
            levelState["prevKey"] = k
            simpleWalk(dictionary[k], k, level, levelState, ptr, scopeInfoStore)
        else:
            highLvlParent = scopeInfoStore["result"].get(levelState["prevKey"])


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
                # scopeInfoStore[]
                scopeInfoStore["result"]["prevKeyState"] = levelState["prevKey"]
                highLvlParent["childLength"] += 1
                levelState["prevKey"] = k
            else:
                # use the jumper algorithm similar to the deltaJumper
                # as well
                print(
                    "KKA",
                    "key",
                    k,
                    scopeInfoStore["result"],
                    level,
                    levelState,
                    scopeInfoStore["root"],
                )

                if scopeInfoStore["result"].get("prevKeyState") is None:
                    pjumper = scopeInfoStore["result"][scopeInfoStore["root"]]
                    print("pjumper", pjumper)
                    pjumperIndex = pjumper["childLength"] - 1

                    while pjumper["level"] < level:
                        pjumper = pjumper["children"][pjumperIndex]
                    
                    appendFlattenNode(pjumper, k, dictionary[k])

                    continue

                prevKey = scopeInfoStore["result"]["prevKeyState"]
                pks = scopeInfoStore["result"][prevKey]

                # print("KKA","key",k,scopeInfoStore["result"],len(pks["children"]),pks["childLength"], pks["children"])
                # course index correction
                if pks["childLength"] > len(pks["children"]):
                    pks["childLength"] = len(pks["children"])

                endzone = pks["children"][pks["childLength"] - 1]

                if endzone["level"] == level and endzone.get("children") is not None:
                    newNode = createFlattenNode(k,dictionary[k])
                    newNode["parentsaa"] = [*endzone["parents"],endzone["root"]]
                    endzone["children"].append(newNode)
                    continue

                prevKey = scopeInfoStore["result"]["prevKeyState"]
                pks = scopeInfoStore["result"][prevKey]
                endzone = pks["children"][pks["childLength"] - 1]


                if k == "app":
                    print("KKa app",k,
                          dictionary[k],

                          scopeInfoStore["result"].get("prevKeyState"),
                          endzone["level"],level,
                          len(endzone["children"]) > endzone["childLength"], 
                          pks["level"]
                    )

                    
                if level > endzone["level"]:
                    # if len(endzone["children"]) > endzone["childLength"]:
                    if len(endzone["children"]) > endzone["childLength"]:
                        epas = endzone["childLength"]
                        ezStart = endzone["children"][epas]

                        if k == 'app':
                            print("KKa ss",pks,len(pks["children"]),scopeInfoStore["result"],prevKey,levelState["prevKey"])
                            print("KKa ssx",pks)

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
                        ezStart = endzone["children"][epas]

                        while level > ezStart["level"]:
                            epas = ezStart["childLength"] - 1
                            ezStart = ezStart["children"][epas]

                        appendFlattenNode(ezStart, k, dictionary[k])

                    print("epas start", "KEY", k, endzone, level)


                else:
                    print("ez dz", k, dictionary[k])

                print(
                    "DUOA",
                    levelState["prevKey"],
                    endzone,
                    "value x",
                    k,
                    dictionary[k],
                    # pks["children"],
                    pks["childLength"],
                    # scopeInfoStore["result"],
                    scopeInfoStore["result"]["prevKeyState"],
                )

            prevKey = scopeInfoStore["result"]["prevKeyState"]
            pks = scopeInfoStore["result"][prevKey]
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

    return scopeInfoStore


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
