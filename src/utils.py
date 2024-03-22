import json
from enum import Enum


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

    # if curr is not None :

    fep = ptrs.get(highest)
    return fep.pop() if fep else None


def saveToResult(analyzedResult, name):
    if name is None:
        raise Exception("Result filename is None")

    analyzerTestPrefix = "test_results"
    analyzerTestFileName = "{}.json".format(name)
    refFd = open(
        "../../{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
        "w",
    )

    # GREAT PROGRESS SO FAR SO GOOD
    json.dump(analyzedResult, refFd)


def makeNodeAppender(scopeInfoStore, key, level):
    def initializeAssmBuffer():
        if scopeInfoStore.get("assemblyBuffer") is None:
            combinedTails = tailCompression(scopeInfoStore.get("prev"))
            if combinedTails is not None:
                scopeInfoStore["assemblyBuffer"] = combinedTails
            else:
                return

    def nodeAppender(param=0):
        ## initialize assemblyBuffer
        initializeAssmBuffer()

        currentAssmBuffer = scopeInfoStore["assemblyBuffer"]
        assmBuffChildren = currentAssmBuffer["children"]
        lvlTracker = currentAssmBuffer["level"]

        bufferParent = currentAssmBuffer
        assmChildPtr = currentAssmBuffer.get("childLength")

        print(
            "LVA",
            key,
            lvlTracker,
            level,
            bufferParent["level"],
            scopeInfoStore["assemblyBuffer"],
        )

        # adjust root and reset the assembly buffer
        if bufferParent["level"] == level:
            if scopeInfoStore.get("result") is None:
                scopeInfoStore["result"] = {}

            _rootName = scopeInfoStore["root"]
            print("LVA DD", scopeInfoStore["assemblyBuffer"])

            scopeInfoStore["result"][bufferParent["key"]] = currentAssmBuffer
            scopeInfoStore["assemblyBuffer"] = {
                "key": key,
                "children": [],
                "next": {},
                "root": key,
                "childLength": 0,
                "level": level,
            }
            scopeInfoStore["result"][key] = scopeInfoStore["assemblyBuffer"]

            return

        parentTrace = [bufferParent["root"]]

        while lvlTracker != level - 1:
            print("Xebec", key, lvlTracker, level, assmChildPtr, len(assmBuffChildren))

            ## some child length counter/pointer may overshoot
            ## so we decrease the counter to make sure to count the
            ## assemblyBuffer children correctly
            if len(assmBuffChildren) == assmChildPtr:
                print(
                    "decrease single",
                    key,
                    len(assmBuffChildren),
                    assmChildPtr,
                    level,
                    bufferParent,
                )
                assmChildPtr -= 1

            if len(assmBuffChildren) < assmChildPtr:
                print("decrease double", key, len(assmBuffChildren), assmChildPtr)
                assmChildPtr -= 2

            # if it is a flatten field type , we must abort the insertion
            # because flatten type should not have children to append to
            if assmBuffChildren[assmChildPtr].get("fieldType") == str(
                FieldType.FLATTEN
            ):
                break

            parentTrace.append(assmBuffChildren[assmChildPtr]["root"])

            # put previous pointer to parent
            # put next pointer to children
            next = assmBuffChildren[assmChildPtr]["children"]
            prev = assmBuffChildren[assmChildPtr]

            bufferParent = prev
            assmBuffChildren = next

            lvlTracker += 1
            assmChildPtr = prev["childLength"]

        print("xebec", bufferParent, assmChildPtr, key)

        assmBuffChildren.append(
            {
                "key": key,
                "children": [],
                "next": {},
                "root": key,
                "childLength": 0,
                "level": level,
                "parent": parentTrace,
            }
        )
        bufferParent["childLength"] += 1

    return nodeAppender
