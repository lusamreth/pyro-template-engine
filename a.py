# # print(key)
# if len(prev) > 0:
#     # print("prev", prev.get(level - 1), prev.get(level), key, level)
#     upperEchalon = prev.get(level - 1) or {}
#     if not key in upperEchalon:
#         childKey["level"] = level
#         childKey["levelCount"] = 1

#         if prev.get("lowestLevel") is None:
#             prev["lowestLevel"] = level
#             prev["lowestLevelKey"] = [key]

#         bugi = prev["lowestLevel"]
#         print("bugi", bugi)
#         if level > bugi:
#             prevBug = prev[bugi]
#             scopeLeveled = list(prevBug.keys())
#             pc = prevBug["levelCount"]
#             prev["lowestLevelKey"].append(key)

#             # temp = {scopeLeveled[pc - 1]: {}, **temp}
#             # temp[scopeLeveled[pc - 1]] = {key: {}}

#             prevKey = None
#             loopNum = bugi
#             tKey = prev["lowestLevelKey"][loopNum]
#             if prevKey is None:
#                 tmp = {
#                     "rootKey": tKey,
#                     "childKey": key,
#                     "child": {
#                         key: {
#                             "parent": prev["lowestLevelKey"][
#                                 0 : loopNum + 1
#                             ],
#                             "root": key,
#                         },
#                     },
#                 }
#                 prevKey = tmp

#             if prev.get("assemble") is not None:
#                 assemble = prev.get("assemble")
#                 assemble["combined"] = {
#                     assemble["rootKey"]: assemble["child"]
#                 }

#             osi = len(prev["assembles"])
#             asmbles = prev["assembles"]
#             prevKeyRunner = None

#             prev["assemble"] = prevKey
#             prev["assembles"].append(prevKey)

#             # print("OSI", osi)
#             print("prev", prev["assemble"], prev["lowestLevel"])
#             while osi > 0 and len(asmbles) > 0:
#                 asm = asmbles[osi - 1]
#                 rkd = asm["rootKey"]
#                 chk = asm["childKey"]

#                 if prevKeyRunner is None:
#                     prevKeyRunner = {
#                         rkd: {"children": [{chk: asm["child"][chk]}]}
#                     }

#                 else:
#                     prevKeyRunner = {
#                         rkd: {
#                             "children": [
#                                 {
#                                     **prevKeyRunner,
#                                     **asm["child"][chk],
#                                 }
#                             ]
#                         }
#                     }

#                 osi -= 1

#             prev["layers"] = prevKeyRunner
#             # print("asm ---")
#             prev["lowestLevel"] += 1
#         else:
#             if prev.get("layers") is not None:
#                 prev["lowestLevel"] = bugi - level
#                 prev["lowestLevelKey"] = [
#                     *prev["lowestLevelKey"][0:level],
#                     key,
#                 ]
#                 # while
#                 print(
#                     "-- lowest level",
#                     level,
#                     bugi,
#                     key,
#                     prev["lowestLevelKey"],
#                 )
