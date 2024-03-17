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


downLink = {}


# probing(result2, Utility_VAR)
def simpleWalk(
    dictionary,
    k="",
    level=0,
    levelCounter={"localHigh": 0},
    ptr={},
    upLink={},
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

    print(state)
    print("prev state", prevState, state)

    level += 1
    levelCounter["state"] = state

    # state adjuster
    if prevState is not None:
        if prevState["status"] == "down" and state["status"] == prevState["status"]:
            props["downCount"] += 1
            print("up ring downward", k, upLink.get("root"))
            if upLink.get("root") is None:
                upLink[k] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
                upLink["root"] = k
            else:
                curr = upLink[upLink["root"]]
                rootname = upLink["root"]
                keepStill = False

                # if upLink[rootname][]
                # if upLink.get("prev") is not None:
                #     upLink["prev"]["next"] = k

                print(
                    "up ring app",
                    upLink.get("root"),
                    k,
                    upLink.get("prev"),
                    keepStill,
                    level,
                )

                if upLink.get("prev") is not None:
                    if upLink["prev"].get("children") is not None:
                        upLink["prev"]["children"].append(k)
                        upLink[rootname]["next"] = upLink["prev"]
                        keepStill = True

                # upLink[rootname]["next"] = {
                # upLink["prev"] = upLink[rootname]["next"]
                if not keepStill:
                    upLink["prev"] = {
                        "key": k,
                        "children": [],
                        "next": {},
                        "root": k,
                    }
                print("up ring next", upLink, k)

        # if prevState["status"] == "up" and state["status"] == "down":
        #     print("up key", k)
        #     pass

        if prevState["status"] == "down" and state["status"] == "equal":
            rootname = upLink["root"]
            # print("up ring prx", rootname, k, upLink.get("prev"))
            if upLink.get("prev") is not None:
                if upLink["prev"].get("children") is not None:
                    upLink["prev"]["children"].append(k)
                    print(
                        "up ring pr",
                        rootname,
                        upLink.get("prev"),
                        k,
                        upLink[rootname]["next"],
                    )
                    # print("up ring spoofiu")
                    upLink[rootname]["next"] = upLink["prev"]

        if state["status"] == "up" and prevState["status"] == "down":
            print("up ring pgr ", k, props, upLink)
            # print("EPOK", props, upLink, k)
            pass

        # if prevState["status"] == "up" and state["status"] == "down":
        #     print("up ring pgr ", k)
        #     pass

        if state["status"] == "down" and prevState["status"] == "up":
            rootname = upLink["root"]
            print(
                "up ring pr do",
                k,
                rootname,
                upLink.get("prev"),
                level,
            )

            if upLink.get("prev") is not None:
                if upLink["prev"].get("children") is not None:
                    upLink["prev"]["children"].append(k)
                    # print("up ring spoofiu")

                    # upLink["prev"] = {
                    #     "key": k,
                    #     "children": [],
                    #     "next": {},
                    #     "root": k,
                    # }
                # if prevLink.get("mightEqual") is None:
                #     # upLink[rootname]["next"] = upLink["prev"]

        if state["status"] == "equal" and prevState["status"] == "equal":
            rootname = upLink["root"]
            print("up ring equalizer", k, rootname, upLink["prev"])
            if level == upLink[rootname]["level"]:
                print("high level", k)

                upLink[k] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
                upLink["root"] = k
            else:
                if upLink.get("prev") is not None:
                    if upLink["prev"].get("children") is not None:
                        upLink["prev"]["children"].append(k)

                        # print(
                        #     "up ring pr diva", rootname, upLink.get("prev"), upLink, k
                        # )
                        # print("up ring spoofiu")
                        upLink[rootname]["next"] = upLink["prev"]

        if state["status"] == "up" and prevState["status"] == "up":
            rootname = upLink["root"]
            upLink[rootname]["children"].append(upLink["prev"])
            if level == upLink[rootname]["level"]:
                upLink["root"] = k
                upLink[k] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
                upLink["prev"] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
            print("up ring high ", k, upLink.get("prev"))

        # both up and equal
        if state["status"] == "up" and prevState["status"] == "equal":
            rootname = upLink["root"]
            if level == upLink[rootname]["level"]:
                upLink["root"] = k
                upLink[k] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
                upLink["prev"] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
            else:
                upLink[rootname]["children"].append(upLink["prev"])
                upLink["prev"] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
                print("PMZ", k, rootname, upLink["prev"])

        if state["status"] == "equal" and prevState["status"] == "up":
            print("up ring BMZ State up and equal", k, upLink["prev"])
            rootname = upLink["root"]
            upLink[rootname]["children"].append(upLink["prev"])
            upLink["prev"] = {
                "key": k,
                "children": [],
                "next": {},
                "root": k,
                "level": level,
            }
            pass

        # both up
        if state["status"] == "up" and state["status"] == prevState["status"]:
            rootname = upLink["root"]

            # print("pmz", k, prevState, upLink["prev"], upLink[rootname]["level"], level)

            if level == upLink[rootname]["level"]:
                print("high level", k)
                # upLink["root"] = k
                upLink[k] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "level": level,
                }
            else:
                print("pmz", rootname, level)
                upLink["prev"] = {
                    "key": k,
                    "children": [],
                    "next": {},
                    "root": k,
                    "mightEqual": True,
                }
                upLink[rootname]["children"].append(upLink["prev"])
                # upLink["prev"] = {
                #     "key": k,
                #     "children": [],
                #     "next": {},
                #     "root": k,
                #     "mightEqual": True,
                # }
                pass
            # print("cjhildrfen", ptr.get("children"))

    # print("state", state["status"])
    for k in dictKeys:
        if isinstance(dictionary[k], dict):
            simpleWalk(dictionary[k], k, level, levelCounter, ptr, upLink)
        pass
    return upLink


resu = simpleWalk(VALID_UTILITY_TEST)

# print(json.dumps(resu, indent=4))
# fp = open("bbua-v1.json", "w+")
print(downLink)
# print(linkedlist["up"])
# print(linkedlist["up"]["up"])

fpx = open("bbua-v1.json", "w+")

# GREAT PROGRESS SO FAR SO GOOD
# print("CONS", *construct["settings"]["children"], sep="\n")

json.dump(resu, fpx)
print("ospa", resu)
# json.dump(construct["settings"]["children"][0], fpx)
