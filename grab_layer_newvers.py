import json
from functools import reduce

import tomli as toml

import traversal
from scope_analyzer_prune import analyzeScope
from syn_decoder import multiCommandParser
from utils import saveToResult
from variable_subsitution import NeedleBoxCtxAware

sample = {
    "b": 10,
    "a": {
        "b": 1,
        "e": 2,
        # "dez": "$(adx) -> adx.dez",
        "ad": {"param": 100, "deza": {"p": {"bru": 1}}},
        "ac": "%b",
        "param": 1,
        "adx": {"param": 100, "dez": {"p": "$[1,2,3]"}},
        "x2": {"b": 1},
        "acx": 1,
    },
    "h": 1,
    "c": {"x": "1", "obitu": 1, "xba": {"a": "$[2,3,5,6,8,10]"}},
    "dezo": {"p": 1},
}


# FATAL BUG : if there is only dictionary in the settings, the scope_analyzer
# will not be able to detect children of each root properly leading to issue
# with var subitution errors

# FATAL BUG : parent scope parser is not working as expected , does not
# generated the appropriate parsed

originalSetting = {
    "can": 40,
    "volume": {
        "can": 40,
        # "prne": 1,
        "luji": {"bai": "%prne", "prne": 100},
        "b": {
            "luji2": {"bai": "%prne $[1,2] %can", "prne": 2, "can": 100},
        },
    },
}

simpleSettingScope = traversal.analyze_scope(originalSetting)

samplee = {
    "root": "xba",
    "children": [
        {"root": "a", "parent": ["c", "xba"], "offset": 0, "value": "$[2,3,5,6,8,10]"}
    ],
    "level": 1,
    "offset": 2,
}


def countRoot(samplee):
    thisBlockIsRoot = False
    countLevelOneRoot = 0

    for sampleKey in samplee.keys():
        if sampleKey == "children":
            thisBlockIsRoot = True
            countLevelOneRoot += 1
    return countLevelOneRoot


dumpFile = open("traversal-file-dump.json", "w+")
json.dump(simpleSettingScope, dumpFile)
print("result", json.dumps(simpleSettingScope, sort_keys=True, indent=4))

scopes = ["bind", "param", "cmd"]


def isEqualScope(a1, scopes):
    scopes_copied = scopes.copy()
    s0 = set(scopes_copied)
    s1 = set(a1)
    interSect = s1.intersection(s0)
    return len(list(interSect)) == len(scopes_copied)


print(isEqualScope(["bind", "param", "cmds"], scopes))


# because the auto leveling parser result is so partial, the system needs to be
# able to merged all those partial result into a correct order
def autoLevelingParser(raw, scopeKeys, originalScope, childAncestors):
    parsed = multiCommandParser(raw, scopeKeys, originalScope)
    print(
        "parsed scope key",
        childAncestors[-1],
        parsed,
        originalScope,
        raw,
        "parsed",
        parsed,
    )

    # parsed.get("isEmpty")
    loopBackCondition = parsed == "elevate" or isinstance(parsed, dict)
    if loopBackCondition:
        if isinstance(parsed, dict) and parsed.get("isEmpty"):
            raw = parsed["replacedScope"]
            print("raw empty b", raw)

        childAncestors = childAncestors.copy()
        clonePtr = originalScope
        _lc_len = len(childAncestors)

        while _lc_len > 0 and loopBackCondition:
            initialScope = childAncestors.pop()
            _lc_len -= 1

            isolatedScope = clonePtr
            depth_count = 0

            while depth_count < _lc_len and _lc_len != 0:
                chl = childAncestors[depth_count]
                depth_count += 1
                # _lc_len -= 1
                isolatedScope = isolatedScope.get(chl)

                ndbl = NeedleBoxCtxAware(raw)
                ndbl.contextSwitch(isolatedScope)
                pmc = ndbl.resolveChainVars()

                if pmc is not None and pmc.get("isEmpty") is None:
                    raw = pmc
                    
                    print("PMC EMPTY",pmc)

                print(
                    "depo count",
                    depth_count,
                    pmc,
                    isolatedScope,
                    originalScope,
                    "RAW",
                    raw,
                    "CLONE PTj",
                    initialScope,
                    isolatedScope,
                    "LL",
                    depth_count,
                )

            print("ISO",isolatedScope)

            if clonePtr.get(initialScope) is not None:
                # parsed = multiCommandParser(raw, scopeKeys, clonePtr[initialScope])
                clonePtr = clonePtr[initialScope]

            # if isolatedScope and isolatedScope.get(initialScope) is not None:
            #     isolatedScope = isolatedScope[initialScope]

            if isolatedScope is not None:
                parsed = multiCommandParser(raw, scopeKeys, isolatedScope)
                # parsed = multiCommandParser(raw, scopeKeys, isolatedScope[initialScope])

                print(
                    "parsed isolated",
                    isolatedScope,
                    initialScope,
                    parsed,
                    raw,
                )

                pass

            else:
                parsed = multiCommandParser(raw, scopeKeys, clonePtr)
                print(
                    "parsed isolated globe",
                    initialScope,
                    isolatedScope,
                    clonePtr,
                    parsed,
                    raw,
                )

            # 
            # will trigger when the buffer cannot find the variable seed
            if _lc_len == 0 and isinstance(parsed, dict):
                parsed = multiCommandParser(raw, scopeKeys, clonePtr, True)

            loopBackCondition = parsed == "elevate" or isinstance(parsed, dict)

            print("parsed scope key", _lc_len, loopBackCondition, parsed)
            # fix this
            print(
                "parsed After elevate",
                initialScope,
                childAncestors,
                clonePtr,
                "parsed",
                parsed,
                "child and",
                raw,
            )

    if len(parsed) == 0:
        print("EMPTY parsed",parsed,raw,childAncestors)
        # ndbl = NeedleBoxCtxAware(raw)
        return raw
    
    # if loopBackCondition:
    #     return multiCommandParser

    return parsed


def crawl(innerDict, levelOneKey, originalSetting, ptrInfo={}, result={}):
    lvRoot = countRoot(innerDict)
    # ptrInfo = {}

    if lvRoot == 1:
        children = innerDict.get("children")
        for child in children:
            parent = child.get("parent")

            if child.get("children"):
                # print("nested", child, levelOneKey, child.get("level"))
                parentRoot = child.get("root")
                children = child.get("children")
                childrenRoot = [x.get("root") for x in children]
                childAncestors = children[0].get("parent").copy()

                print(
                    "CHILDREN",
                    children,
                )

                def makeDict(acc, ele):
                    acc[ele.get("root")] = ele.get("value") or {}
                    return acc

                recombined = reduce(makeDict, children, {})
                # isScopedConfig = isEqualScope(childrenRoot, scopes)
                # # The algorithm determine by param command
                # print("scope config log", isScopedConfig, childrenRoot,
                #       recombined,result)

                if False:
                    # Multi Command Parser will not work if it does not
                    # contains vector

                    parsed = autoLevelingParser(
                        recombined, scopes, {**originalSetting,**result}, childAncestors
                    )

                    print("parsed parent", parentRoot, parsed, "res",
                          result,ptrInfo.get('prev'), end="\n")

                    # merge back the tree
                    # result[parentRoot] = parsed
                    if ptrInfo.get("prev") is not None:
                        clonePtr = result

                        l = len(childAncestors)
                        for chl in childAncestors[1 : l - 1]:
                            clonePtr = clonePtr[chl]

                        if isinstance(clonePtr, list):
                            for genPtr in clonePtr:
                                genPtr[parentRoot] = parsed
                        else:
                            clonePtr[parentRoot] = parsed

                        print("parent pink", clonePtr, parentRoot)
                    else:
                        result[parentRoot] = parsed
                    # print("Chd root", childrenRoot, parsed)
                    ptrInfo["prev"] = {"root": parentRoot, "level": child.get("level")}

                else:
                    recombined = reduce(makeDict, children, {})
                    rootOnlyMap = map(lambda rootNode: rootNode.get("root"), children)
                    rootOnly = list(rootOnlyMap)

                    print("root child", rootOnly, originalSetting, recombined)
                    parsed = autoLevelingParser(
                        recombined, rootOnly, originalSetting, childAncestors
                    )

                    print("opa parsed",parsed,parentRoot,ptrInfo.get('prev'),result, recombined)

                    if ptrInfo.get("prev"):
                        print(
                            "pink ep",
                            ptrInfo,
                            parentRoot,
                            childAncestors,
                            parsed,
                            levelOneKey,
                        )

                        clonePtr = result

                        l = len(childAncestors)
                        foundList = False
                        lastRoot = {}
                        
                        for i, chl in enumerate(childAncestors[1 : l - 1]):
                        # for i, chl in enumerate(childAncestors):
                            print("clone", chl,
                                  childAncestors,child.get('level'),
                                    result
                                  )
                            foundList = isinstance(clonePtr, list)

                            if foundList:
                                lastRoot["root"] = chl
                                lastRoot["childAncestors"] = childAncestors[
                                    i + 1 : l - 1
                                ]

                                break

                            # clonePtr = clonePtr[chl]
                            if clonePtr.get(chl) is not None:
                                clonePtr = clonePtr[chl]
                            else:
                                if len(clonePtr) == 0:
                                    clonePtr[chl] = {}

                                clonePtr = clonePtr[chl]
                                print('empty clone',clonePtr,chl)

                                pass


                        print("LLd", clonePtr,parsed,foundList)

                        def listMutation(cltPtr=clonePtr, acc=[]):
                            leftover = lastRoot["childAncestors"]
                            print("again")

                            for genPtr in cltPtr:
                                print("found list", genPtr, lastRoot)
                                gmtPtr = genPtr

                                for l in leftover:
                                    print(
                                        "found list llm",
                                        l,
                                        genPtr,
                                        "GMT",
                                        gmtPtr,
                                        lastRoot,
                                    )

                                    if isinstance(gmtPtr, list):
                                        print("found list llm after rec", gmtPtr, l)
                                        lastRoot["childAncestors"].pop(0)
                                        listMutation(gmtPtr)
                                    else:
                                        print(
                                            "koba",
                                            gmtPtr,
                                            parentRoot,
                                            lastRoot,
                                            lastRoot,
                                            l,
                                            len(cltPtr),
                                        )

                                        if gmtPtr.get(l):
                                            print("koba d", gmtPtr.get(l), l)
                                            gmtPtr = gmtPtr[l]
                                        else:
                                            print("koba none", gmtPtr)

                                    print("found list llm after", gmtPtr, l, parentRoot)

                                    if isinstance(gmtPtr, list):
                                        for pt in gmtPtr:
                                            pt[parentRoot] = parsed

                                # genPtr[lastRoot["root"]][parentRoot] = parsed
                        
                        ### expirmental
                        if foundList:
                            listMutation()
                        else:
                            if isinstance(clonePtr, list):
                                for genPtr in clonePtr:
                                    genPtr[parentRoot] = parsed
                            else:
                                clonePtr[parentRoot] = parsed

                        # clonePtr[parentRoot] = parsed
                        print("child pink", clonePtr, parentRoot)
                    else:
                        result[parentRoot] = parsed
                        print("DUMA", parentRoot, result)

                    print(
                        "CHILD empo",
                        parentRoot,
                        result,
                        child.get("level"),
                        # childAncestors,
                        # result,
                        "prev",
                        ptrInfo,
                        # recombined,
                        # children,
                        rootOnly,
                        parsed,
                    )

                    ptrInfo["prev"] = {"root": parentRoot, "level": child.get("level")}
                    # list(rootOnly)
                    # childAncestors = children[0].get("parent").copy()
            else:
                ## big big issue right here
                ## the level 1 variable scanner is currently not working
                # which means at the highesh level , variable cannot be
                # substitute or templated to be fit .

                _combined_dict = {child.get("root"): child.get("value")}
                # parsed = autoLevelingParser(
                #     _combined_dict,
                #     [child.get("root")],
                #     originalSetting,
                #     child.get("parent") or [child.get("root")],
                # )
                nbox = NeedleBoxCtxAware(_combined_dict)
                ptr = originalSetting
                # ptrR = result

                cRes = child.get("value")
                for iterC, c in enumerate(child.get("parent")):
                    scopeCombo = {**ptr[c],**result}
                    nbox.contextSwitch(scopeCombo)
                    cRes = nbox.resolveChainVars()
                    print("NBOX",iterC,scopeCombo,cRes)
                        
                    if cRes.get("isEmpty") is None:
                        # print("NPC", iterC, cRes, c,"PTR",ptr)
                        rootname = child.get("root")
                        # ptr[c] = cRes
                        break

                    ptr = ptr[c]

                print("NPC after",cRes,ptr,"RESULT",result,child.get('parent'))
                
                # print("PINKY", child, ptrInfo, result, parent, parsed,npc)
                # result[child.get("root")] = child.get("value")
            
                rootname = child.get("root")
                cparent = child.get('parent')

                if len(cparent) == 0:
                    result[child.get("root")] = cRes

                if len(cparent) == 1 :
                    result[child.get("root")] = cRes.get(rootname) or {}

                # ptr[rootname] = cRes.get(rootname)
                # return parsed

            if parent:
                lowRoot = parent[0]
                highRoot = parent[-1]
                keyRoot = child.get("root")

                if scopes.count(keyRoot) > 0:
                    print("keyRoot", highRoot, innerDict)
                    pass

                print("CCH", child.get("value"), child.get("root"))
                print("root", lowRoot, highRoot, levelOneKey)

            crawl(child, levelOneKey, originalSetting, ptrInfo, result)

    return result


def multiLayerParser(traversed, fullscope):
    fullResult = {}

    for resKey in traversed.keys():
        lvRoot = countRoot(traversed[resKey])
        print("craw res", resKey, lvRoot, fullscope)

        if lvRoot == 1:
            rmcBuffer, dtc = {}, {}
            crawlRes = crawl(traversed[resKey], resKey, fullscope, {}, {})
            print("craw res", crawlRes, resKey, traversed[resKey])
            fullResult[resKey] = crawlRes
            if len(crawlRes.keys()) > 0:
                fullResult[resKey] = crawlRes
            else:
                # fullResult[resKey] = fullscope[resKey]
                print("craw res none", resKey)

        else:
            print("liao",traversed[resKey])
            fullResult[resKey] = traversed[resKey]["value"]
    
    # return NeedleBoxCtxAware(fullResult).resolveChainVars()
    return fullResult


# newTraversed = analyzeScope(originalSetting)
# # # print("SIMP", newTraversed)
# parsed = multiLayerParser(newTraversed,originalSetting)
# saveToResult(parsed, "finalResult")


def testLoader():
    with open("hypr_ins.toml", "rb") as f:

        tml = toml.load(f)

        print("TOML", tml)

        anl = analyzeScope(tml)
        res = multiLayerParser(anl, tml)

        saveToResult(anl, "scopeAnalysis")
        saveToResult(res, "finalResult")
        print("final", res, tml)


if __name__ == "__main__":
    testLoader()
