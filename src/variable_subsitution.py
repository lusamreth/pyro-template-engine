import re
import traceback

import tokenizer

edgecaseScopeTest = {
    "prne": 10,
    "param": "param : %cmd %prne",
    "cmd": "abc %prne %osmos %osmos",
    "gentoo": 100,
    "osmos": "gg %prne %gentoo",
    "chained": "chained : %param %prne %cmd",
    "bbc": "chained : %param %osmos %cmd",
    "xdca": "chained : %param %prne %cmd",
    "xdcbb": "chained : %xdca %prne %cmd",
}

case2 = {
    "prne": 10,
    "param": 30,
    "osmos": "gg %prne",
    "osmos2": "gg %prne %param",
    "zdd": {}
    # "ax": {
    #     "nested2": {
    #         "param": 100,
    #         "%cmd": 100,
    #         "bbc": "chained : %param %osmos %cmd",
    #     },
    #     "xdca": "chained : %param %prne %cmd",
    #     "xdcbb": "chained : %xdca %prne %cmd",
    # },
}
# local line -> needle_box
# necessary to produce variable lookup


def cleanEmpty(chainLoaded):
    newLoaded = {}
    for chainLoad in chainLoaded:
        chainval = chainLoaded[chainLoad]
        if len(chainval.keys()) > 0:
            newLoaded[chainLoad] = chainval

    return newLoaded


# variable lookup now generate needle box and also keep track of each needle
# box for later use
class NeedleBoxCtxAware:
    def __init__(self, varScope):
        self.scopeNeedleBoxContext = {}
        self.variableRelationShip = {}
        self.varScope = varScope
        # use for extending the range of our needle box lookup table
        self.extendedScope = {}

        self.prevContext = {}
        self.interrupted = False

    def contextSwitch(self, newContext: dict):
        # self.varScope = {**self.varScope, **newContext}
        self.extendedScope = newContext

    def scanForVars(self):
        varScope = self.varScope

        for edge in varScope.keys():
            value = varScope[edge]
            variableLookup(value, edge, self.scopeNeedleBoxContext)
            self.prevContext = self.scopeNeedleBoxContext

    def trackVarReferences(self):
        varRelation = self.variableRelationShip
        scopeNeedleBoxContext = self.scopeNeedleBoxContext
        for ctxField in scopeNeedleBoxContext.keys():
            context = scopeNeedleBoxContext[ctxField]

            for needleBox in context:
                needleField = needleBox[1:]
                if context.get(needleBox) is not None:
                    if varRelation.get(ctxField) is None:
                        varRelation[ctxField] = [needleField]
                    else:
                        varRelation[ctxField].append(needleField)

        print("PTRACk", varRelation, scopeNeedleBoxContext.keys())
        return varRelation

    def resolveChainVars(self):
        # populating the varScopeNeedlBox
        self.scanForVars()
        # see chain relationship
        variableRelationship = self.trackVarReferences()
        varScope = self.varScope

        for chain in variableRelationship:
            chainval = variableRelationship[chain]
            print("Chainmailer", chain, chainval, self.varScope)

            def traveller(chainval):
                for cc in chainval:
                    lockd = variableRelationship.get(cc)
                    print("ebLockd", cc, lockd, chain)

                    if lockd:
                        traveller(lockd)

                        # we should automatically allow outward scope
                        # combined in tangent with its original scope to
                        # preserve other variable lookup table

                        combinedScope = {**self.extendedScope, **self.varScope}
                        replaced = tokenizer.sub_needle_box(
                            self.scopeNeedleBoxContext[cc], combinedScope, varScope[cc]
                        )
                        print("repa", replaced, combinedScope)
                        # logic link with interrupted
                        global interrupted
                        # if isinstance(replaced, list):
                        if replaced == None:
                            print("NON interrupted", self.scopeNeedleBoxContext[cc])
                            self.interrupted = True
                            break

                        varScope[cc] = replaced
                        self.scopeNeedleBoxContext[cc] = {}

            traveller(chainval)

        if self.interrupted:
            return None

        newCtx = cleanEmpty(self.scopeNeedleBoxContext)

        buffer = {}
        for cleanCtxKey in newCtx:
            cleanCtx = newCtx[cleanCtxKey]
            isolatedScope = varScope[cleanCtxKey]

            if not isinstance(varScope[cleanCtxKey], dict):
                combinedScope = {**self.extendedScope, **self.varScope}
                replaced = tokenizer.sub_needle_box(
                    cleanCtx,
                    combinedScope,
                    # self.varScope,
                    varScope[cleanCtxKey],
                    internalResult=buffer,
                )

                self.varScope[cleanCtxKey] = replaced
                print(
                    "sciva",
                    buffer.get("isEmpty"),
                    buffer,
                    combinedScope,
                    replaced,
                    self.extendedScope,
                )

                #     self.varScope[cleanCtxKey] = None
            else:
                print("CCDD", cleanCtx, isolatedScope, cleanCtxKey)

            if buffer.get("isEmpty"):
                print("sciva", buffer)
                return buffer

            print(
                "new ctx",
                buffer,
                self.varScope,
                cleanCtx,
                isolatedScope,
                "KEY:",
                cleanCtxKey,
            )

        return self.varScope


def variableLookup(cfgLine, scopeKey, scopeContext={}, varId="%"):
    needleBoxes = {}
    try:
        allReferences = re.finditer(f"\\{varId}(\\w+)", str(cfgLine))
        for refs in allReferences:
            needle = refs.group()
            indices = refs.span()
            needleBox = needleBoxes.get(needle)

            if needleBox is not None:
                needleBox.append(indices)
                needleBoxes[needle] = needleBox
            else:
                needleBoxes[needle] = [indices]

        # return needle_boxes
    except Exception as e:
        print("Variable Lookup Failure : ", e)
        print("Aborted")
        traceback.print_exc()

    # global_context.append({context_key: needle_boxes})
    scopeContext[scopeKey] = needleBoxes
    return needleBoxes


# Limitation : can only track local context (one layer)
# Solution : implement recursive context switching
# multi-layer scope substitution only works if the system interact with the
# scope analyzer themselves which has access to all the scope information
# and how each layer can navigate from child -> parent


def filterDict(dictT):
    newDict = {}
    for d in dictT.keys():
        if not isinstance(dictT[d], dict):
            newDict[d] = dictT[d]

    return newDict


# def autoLevelingSub(raw, scopeKeys, originalScope, childAncestors):
#     ndbC = NeedleBoxCtxAware(raw)
#     vars = ndbC.resolveChainVars()
#     print("VARS", vars)

#     # if parsed == "elevate":
#     #     clonePtr = originalScope
#     #     while len(childAncestors) > 0 and parsed == "elevate":
#     #         initialScope = childAncestors.pop(0)
#     #         if clonePtr.get(initialScope) is not None:
#     #             parsed = multiCommandParser(raw, scopeKeys, clonePtr[initialScope])
#     #             clonePtr = clonePtr[initialScope]

#     return vars


# result = autoLevelingSub(case2, {}, {}, {})
# print("new result", result)
