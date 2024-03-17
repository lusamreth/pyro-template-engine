from test_subj import VALID_UTILITY_TEST

upLink = {
    "preserved": {
        "key": "volume",
        "children": [
            {
                "key": "luji6",
                "children": [
                    {
                        "key": "wUJI1",
                        "children": [
                            {
                                "key": "wUJI2",
                                "children": [],
                                "next": {},
                                "root": "wUJI2",
                                "level": 6,
                                "counter": 2,
                            },
                            {
                                "key": "wUJI2.0",
                                "children": [],
                                "next": {},
                                "root": "wUJI2.0",
                                "level": 6,
                                "counter": 0,
                            },
                            {
                                "key": "bc",
                                "children": [],
                                "next": {},
                                "root": "bc",
                                "counter": 0,
                                "level": 7,
                            },
                        ],
                        "next": {},
                        "root": "wUJI1",
                        "level": 5,
                        "counter": 7,
                    },
                    {
                        "key": "ap",
                        "children": [],
                        "next": {},
                        "root": "ap",
                        "counter": 0,
                        "level": 6,
                    },
                    {
                        "key": "ap1",
                        "children": [],
                        "next": {},
                        "root": "ap1",
                        "counter": 0,
                        "level": 6,
                    },
                    {
                        "key": "ap2",
                        "children": [],
                        "next": {},
                        "root": "ap2",
                        "counter": 0,
                        "level": 6,
                    },
                    {
                        "key": "ap3",
                        "children": [],
                        "next": {},
                        "root": "ap3",
                        "counter": 0,
                        "level": 6,
                    },
                    {
                        "key": "wUJI4.0",
                        "children": [],
                        "next": {},
                        "root": "wUJI4.0",
                        "counter": 0,
                        "level": 6,
                    },
                    {
                        "key": "wUJI3.0",
                        "children": [],
                        "next": {},
                        "root": "wUJI3.0",
                        "counter": 0,
                        "level": 6,
                    },
                    {
                        "key": "wUJI9.0",
                        "children": [],
                        "next": {},
                        "root": "wUJI9.0",
                        "counter": 0,
                        "level": 6,
                    },
                ],
                "next": {},
                "root": "luji6",
                "level": 4,
                "counter": 15,
            },
            {
                "key": "wUJI1",
                "children": [],
                "next": {},
                "root": "wUJI1",
                "counter": 0,
                "level": 5,
            },
            {
                "key": "ABJUJI",
                "children": [],
                "next": {},
                "root": "ABJUJI",
                "counter": 0,
                "level": 5,
            },
            {
                "key": "oBJUJI",
                "children": [],
                "next": {},
                "root": "oBJUJI",
                "counter": 0,
                "level": 5,
            },
            {
                "key": "a2JUJI",
                "children": [],
                "next": {},
                "root": "a2JUJI",
                "counter": 0,
                "level": 5,
            },
        ],
        "next": {},
        "root": "volume",
        "level": 3,
        "counter": 0,
    }
}


def deltaJumper(param=0):
    # if upLink.get("preserved") is None:
    #     # forwardPrev(1)
    #     # combinedTails = tailCompression(upLink.get("prev"))
    #     if combinedTails is None:
    #         return

    #     upLink["preserved"] = combinedTails

    lv = upLink["preserved"]["level"]
    delta = level - lv

    # print("dt delta", delta, k, upLink["preserved"])

    psrv = upLink["preserved"]
    curjumper = psrv["children"]
    lvlTracker = psrv["level"]
    print("abcpa", psrv)
    lmpCounter = psrv.get("counter") or 0
    parent = None

    while lvlTracker != level - 1:
        print(
            "go0",
            "level : {}, lvlTrack : {}, lmpCounter: {}, key:{},\
            parentkey:{}, curlen:{}, -- ".format(
                level,
                lvlTracker,
                lmpCounter,
                k,
                parent[0]["counter"] if parent is not None else None,
                len(curjumper),
                # curjumper[lmpCounter],
            ),
        )

        print(json.dumps(parent, indent=4))

        if parent is not None:
            print("AP", param)
            print(json.dumps(parent, indent=4))
            print(
                parent[lmpCounter]["counter"],
                curjumper,
                # curjumper[0]["counter"],
                param,
                delta,
                k,
            )

        if len(curjumper) <= lmpCounter:
            print("gpwr", parent, lmpCounter, k)
            return

        parent = curjumper
        lmpCounter = curjumper[lmpCounter]["counter"]
        lvlTracker = curjumper[lmpCounter]["level"]
        curjumper = curjumper[lmpCounter]["children"]

    if parent is not None:
        pc = parent[lmpCounter]["counter"]
        # parent[0]["counter"] if parent is not None else None
    else:
        pc = 0

    # if curjumper[lmpCounter-1].get("counter") is not None:
    curjumper.append(
        {
            "key": k,
            "children": [],
            "next": {},
            "root": k,
            "counter": 0,
            "level": level,
        }
    )

    # print("parent", pc, len(curjumper), parent[pc - 1], k)

    # if pc > len(curjumper):
    #     print("abcpa", parent, pc, delta, len(curjumper))
    #     # curjumper[pc - 2]["counter"] += 1
    #     # parent[pc - 1]["counter"] += 1
    #     pass
    # else:
    curjumper[pc]["counter"] += 1
