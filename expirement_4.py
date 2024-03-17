import json
import time

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

        # if curr.get("prev") is None:
        #     print("su tmp a ", currLevel)
        #     break

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


downLink = {}


def simpleWalk(
    dictionary,
    k="",
    level=0,
    levelCounter={"localHigh": 0},
    ptr={},
    upLink={"prev": {}},
    props={"downCount": 0},
):
    offset = 0
    dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]
    state = {"status": ""}

    print("each line", k, level, levelCounter, end=" ")
    global downLink
    prevState = levelCounter.get("state")

    if level > levelCounter["localHigh"]:
        # print("up")
        levelCounter["localHigh"] = level
        state["status"] = "down"

        # downLink = {"up": downLink, "key": k, "children": [], "level": level}
        # propergate downward
        # print('down ptr',)
        downLink = {"up": downLink, "key": k, "children": [], "level": level}
        ptr = downLink

    elif level == levelCounter["localHigh"]:
        state["status"] = "equal"
        if ptr.get("children") is not None:
            ptr["children"].append(k)

        # print(" equal", ptr)
        # downLink["children"] = ptr

    else:
        levelCounter["localLow"] = level
        levelCounter["localHigh"] = levelCounter["localLow"]
        # print("dowa put", ptr)

        ptr = downLink["up"]
        ptr = {"up": ptr["up"], "key": k, "children": [], "level": level}

        # linkedlist = ptr
        # linkedlist["payload"] = ptr
        # print("down", k, level, ptr)

        state["status"] = "up"
        # downLink = {"up": ptr}

        # if level == 2:
        #     print("\n")
        #     print("LPP", k, ptr, downLink)

    print("current", state)
    print("prev state", prevState, state)

    level += 1
    levelCounter["state"] = state

    def forwardPrev(add=0):
        upLink["prev"] = {
            "key": k,
            "children": [],
            "next": {},
            "root": k,
            "level": level,
            "prev": upLink["prev"],
            "childLength": 0 + add,
        }
        pass

    def deltaJumper(param=0):
        if upLink.get("preserved") is None:
            # forwardPrev(1)
            combinedTails = tailCompression(upLink.get("prev"))
            if combinedTails is None:
                return

            upLink["preserved"] = combinedTails

        lv = upLink["preserved"]["level"]
        delta = level - lv

        # print("dt delta", delta, k, upLink["preserved"])

        psrv = upLink["preserved"]
        psrv_children = psrv["children"]
        lvlTracker = psrv["level"]
        # lvlTracker = psrv["level"]

        # lmpCounter = psrv.get("childLength") or 0
        lmpCounter = 0

        parent = psrv
        prevCounter = psrv.get("childLength")

        print("LVA", lvlTracker, k, level, parent["level"], upLink["preserved"])

        # adjust root
        if parent["level"] == level:
            if upLink.get("result") is None:
                upLink["result"] = {}

            rootName = upLink["root"]

            print("LVA DD", upLink["preserved"])

            upLink["result"][parent["key"]] = psrv
            upLink["preserved"] = {
                "key": k,
                "children": [],
                "next": {},
                "root": k,
                "childLength": 0,
                "level": level,
            }
            upLink["result"][k] = upLink["preserved"]
            psrv["childLength"] += 1
            return

        if parent["level"] > level:
            # if upLink.get("result") is None:
            #     upLink["result"] = {}

            prevResult = upLink["result"]
            rootName = upLink["root"]

            upLink["root"] = k
            upLink["prevResult"] = prevResult
            upLink["result"] = {}
            # upLink["result"][parent["key"]] = psrv
            upLink["preserved"] = {
                "key": k,
                "children": [],
                "next": {},
                "root": k,
                "childLength": 0,
                "level": level,
            }

            upLink["result"]["curr"] = upLink["preserved"]
            psrv["childLength"] += 1
            return

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
            }
        )
        if isinstance(parent, dict):
            parent["childLength"] += 1
        # else:
        #     psrv_children[prevCounter]["childLength"] += 1

    # state adjuster
    if prevState is not None:
        # state after first chroot
        if state["status"] == "up":
            if state["status"] == prevState["status"]:
                print(
                    "up ring upward up",
                    k,
                    upLink.get("root"),
                    upLink.get("prev"),
                    level,
                )
                deltaJumper()
                pass

            if prevState["status"] == "down":
                # combinedTails = tailCompression(upLink.get("prev").copy())

                if upLink.get("preserved") is None:
                    forwardPrev(1)
                    combinedTails = tailCompression(upLink.get("prev"))
                    upLink["preserved"] = combinedTails
                else:
                    lv = upLink["preserved"]["level"]

                    if lv < level:
                        deltaJumper()

                print(
                    "up ring upward down",
                    k,
                    level,
                    upLink.get("root"),
                    upLink.get("prev"),
                    "preserved",
                    upLink.get("preserved"),
                    upLink.get("lowest"),
                    # tailCompression(upLink.get("prev")),
                    level,
                )

            if prevState["status"] == "equal":
                print(
                    "up ring upward equal",
                    k,
                    upLink.get("root"),
                    upLink.get("prev"),
                    level,
                )
                deltaJumper()

        # equalwarddd
        if state["status"] == "equal":
            if prevState["status"] == "down":
                deltaJumper()

            if prevState["status"] == "up":
                print(
                    "up ring equalward up",
                    k,
                    upLink.get("root"),
                    upLink.get("prev"),
                    upLink.get("preserved"),
                    level,
                )
                deltaJumper()
                pass

            if prevState["status"] == state["status"]:
                lv = upLink["preserved"]["level"]
                deltaJumper()

                print(
                    "up ring equalward equal",
                    k,
                    upLink.get("root"),
                    upLink.get("prev"),
                    upLink.get("preserved"),
                    level,
                )

        # downwardddd
        if state["status"] == "down":
            if prevState["status"] == "up":
                # problematic # if u add a new field in luji4DD it will throw
                print("UPOW", prevState["status"], k)
                deltaJumper()

            if prevState["status"] == "equal":
                # problematic # if u add a new field in luji4DD it will throw
                # error downward movement not working

                # if upLink.get("preserved") is not None:
                print("problematic", k, upLink)

                if upLink.get("root") is None:
                    upLink[k] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                        "level": level,
                        "childLength": 0,
                    }
                    upLink["prev"] = upLink[k]
                    upLink["root"] = k

                    deltaJumper()
                else:
                    deltaJumper()

                # deltaJumper(1)
                pass

            if state["status"] == prevState["status"]:
                props["downCount"] += 1
                if upLink.get("lowest") is None or upLink.get("lowest") < level:
                    upLink["lowest"] = level

                print("up ring downward", k, upLink.get("root"), upLink.get("prev"))

                if upLink.get("root") is None:
                    upLink[k] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                        "level": level,
                        "childLength": 0,
                    }
                    upLink["prev"] = upLink[k]
                    upLink["root"] = k
                else:
                    forwardPrev(0)
                    deltaJumper()

                    print("up ring next", upLink, k)

    # print("cjhildrfen", ptr.get("children"))
    # print("state", state["status"])
    for k in dictKeys:
        if isinstance(dictionary[k], dict):
            simpleWalk(dictionary[k], k, level, levelCounter, ptr, upLink)
        pass
    return upLink


analyzedResult = simpleWalk(VALID_UTILITY_TEST)

analyzerTestPrefix = "test_results"
analyzerTestFileName = "scope_analyzer_results_reference.json"
refFd = open(
    "{}/{}".format(
        analyzerTestPrefix,
        analyzerTestFileName
    ),
    "w+",
)

# GREAT PROGRESS SO FAR SO GOOD

json.dump(analyzedResult, refFd)
