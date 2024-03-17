from test_chain_variable import chainList, edgecase, edgecase_context
from tokenizer import sub_needle_box


def cleanEmpty(chainLoaded):
    newLoaded = {}
    for chainLoad in chainLoaded:
        chainval = chainLoaded[chainLoad]
        if len(chainval.keys()) > 0:
            newLoaded[chainLoad] = chainval
    return newLoaded


def chainLoader(edgecase_context=edgecase_context):
    for chain in chainList:
        chainval = chainList[chain]
        print(chain, chainval)

        def traveller(chainval):
            for cc in chainval:
                lockd = chainList.get(cc)
                if lockd:
                    print("=> locked", chain, cc, lockd)
                    print("=> locked", edgecase_context[cc])

                    traveller(lockd)
                    replaced = sub_needle_box(
                        edgecase_context[cc], edgecase, edgecase[cc]
                    )
                    print("locked context", replaced)
                    edgecase[cc] = replaced
                    edgecase_context[cc] = {}
                    pass

        traveller(chainval)

    # newCtx = cleanEmpty(edgecase_context)

    # if len(newCtx) > 0:
    #     chainLoader(newCtx)
    # else:
    #     return

    print("after")


chainLoader()
print(edgecase)
print(edgecase_context)
newCtx = cleanEmpty(edgecase_context)
for cleanCtxKey in newCtx:
    cleanCtx = newCtx[cleanCtxKey]
    edgecase[cleanCtxKey] = sub_needle_box(cleanCtx, edgecase, edgecase[cleanCtxKey])
print(newCtx)
print(edgecase)

# param -> cmd
# cmd -> prne -> 1 (prne is contain no needle)

# param <- cmd <- prne
# new_cmd = sub_needle_box(cmd_needle,stb,line)
# stb[cmd] = new_cmd
# new_param = sub_needle_box(param_needle , stb,line)
# stb[param] = new_param
