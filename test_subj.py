simpleTest = {
    "root": {
        "pro": 1,
        "pro2": 1,
        "a": {},
        "pro3": 1,
        "pro4": 2,
        "b": {},
        "c": {},
    }
}

cTest = {
    "settings": {
        # "cmd": "pulsectl %sos",
        "xda": 1100,
        "can": 100,
        "volume-new": {
            "xoadi": {
                # "xda": "bruh",
                "can": 10,
                "param": "%xda $[up,down] %can",
                "cmd": "pulsectl %xda",
                "bind": "SHIFT $[a,b]",
            },
            "can": 100,
            "prne": "local",
        },
        # "prne": "global",
        "volume": {
            "can": 100,
            "prne": "local",
            # "lumen": {"xabit": "%prne", "AA": 10},
            # "luji": {"prne": 10, "bai": "%prne $[1,2] %can", "JUJI": 10, "xo": {}},
            "luji2": {"bai": "%prne luji2", "JUJI": 10},
            "luji3": {"bai": "%prne", "JUJI": 10},
            # "xoa": {
            #     # "xda": "bruh",
            #     "can": 10,
            #     "param": "%xda $[up,down] %can",
            #     "cmd": "pulsectl %xda",
            #     "bind": "SHIFT $[a,b]",
            # },
            # "luji4": {"bai": "%prne", "JUJI": 10},
            # "cmd": {"bai": "%prne", "JUJI": 10},
            "cmd": "pulsectl $[1,2,3] %prne",
            "param": "$[1,2,3] %prne %cmd",
            "bind": "SHIFT $[1,2,3]",
            "bind": "SHIFT $[4,2,3]",
        },
    },
    # "bc": 100,
}
continualNest = {
    "ad": {},
    "volume": {
        # "prne": 1,
        "luji": {"cord": {"xd": 100}, "bai": "%prne", "prne": 100},
        "luji2": {"baidi": "%prne"},
    },
    "dx": {},
    "dc": {},
    "prne": 100,
    "b": 100,
}

continualNest = {
    "dispatch": {},
    "application": {"startup": {"alacritty": "alacritty && oki"}},
    "utility": {
        "controllers": "./controllers.py",
        "lujiDD": {
            "bai": "%prne",
            "JUJI": 10,
            "xo": 10,
            "asp": {"x": 10},
            "sa": {},
            "sap": {"A": 1000},
        },
        "volume": {"param": "%controllers", "msg": "bruh", "bind": "SHIFT"},
    },
    # "pini": {"ab": 1},
}

moderateNested = {
    "buoaaA": {"xil": "buoa", "s": {}, "bina": {}, "L": {}, "xL": {"a": 10, "BB": 100}},
    "utility": {
        "lookup": {"param": 1, "msg": "bar"},
        "bruh": 1,
    },
    "app": {
        "brave": {
            "pi": 3,
            "telegram": {"h1": 1},
            "bind": 4,
            "brave": 1,
        },
        "telegram": {
            "param": 1,
            "x": {
                "1": "2",
                "xa": {"ag": "b", "bb": {"ss": 1}, "d": 10},
                "xa2": {"a": "b", "bb": {"ss": 1}, "d": 10},
                "bru": 1,
                "bean": {"xi": 1},
            },
            "bra": {
                "param": 1,
                "bind": 2,
                "dep": {"s": 1},
                "prune": {"x": 1},
            },
            "x2": {"a": "b", "bb": {"ss": 1}},
            "bind": 2,
        },
        "bean": {"a": 1},
        "app1": 1,
        "bean2": {"a": 1},
        "apppy": 1,
    },
}

superNested = {
    "a": {
        "b": {"c": {"d": {"e": {"f": {"g": {"h": {"i": {"zipa": "%var $[1,2,3]"}}}}}}}}
    },
    "var": 1,
    "z": 2,
}

complexNested = {
    # "a":{},
    "buoaaA": {"xil": "buoa", "s": {}, "bina": {}, "L": {}, "xL": {"a": 10, "BB": 100}},
    "settings": {
        # "cmd": "pulsectl %sos",
        "volume": {
            "prne": 1,
            # "lumen": {"xabit": "%prne", "AA": 10},
            "lujiDD": {
                "bai": "%prne",
                "JUJI": 10,
                "xo": 10,
                "asp": {"x": 10},
                "sa": {"a": 10},
                "sap": {},
            },
            "prne": "%can xd",
            # problem the first initial nested element get ignored
            "luji6": {
                "bai": "%prne",
                # "2JUJI": {"SBA": 10},
                "wUJI1": {
                    "wUJI2.0": {"a": 10, "ok": {}},
                    "wUJI1": {"a": 10, "bc": {}},
                    "ap": {},
                    "ap1": {},
                    "ap2": {},
                    # this will not works
                    # "wUJI4.0": {"a": 10, "ddbabc": {}, "babs": {}},
                    "wUJI3.0": {"a": 10, "xddbabc": {}},
                },
                "axisa": {},
                "wUJI30a": {
                    "ap": {},
                    "wUJI2a": {"agg": 10, "bc": {}},
                    "ap1": {},
                    "ap2": {},
                    "ap3": {},
                    "wUJI2.0": {"a": 10, "gbc": {}},
                    "wUJI3.0": {"a": 10, "Hbc": {}},
                    "wUJIx.0": {"a": 10, "Hbc": {}},
                },
                "wUJI4": {"a": 10},
                "wUJI3": {"a": 10},
            },
            "luji5": {
                "bai": "%prne",
                "2JUJI": {"SBA": 10},
                "wUJI1a": {"a": 10},
                "wUJI2": {"a": 10},
                "wUJI3": {"a": 10},
            },
            "luji4DD": {
                "bai": "%prne",
                "wUJI1": {"a": 10},
                "2JUJI": {"SBA": 10, "JIA": {}},
                "a2JUJI": {"SBA": 10, "JIA": {}},
                "b2JUJI": {"SBA": 10, "JIA": {}},
                "c2JUJI": {"SBA": 10, "JIA": {}},
            },
            "luji4Dx": {
                "bai": "%prne",
                "wUJI1": {"a": 10},
                "ABJUJI": {"SBA": 10},
                "oBJUJI": {"SBA": 10, "AP": {}, "S": {}},
                "a2JUJI": {"SBA": 10, "JIA": {}},
            },
            # if the dict don't have another nested dict inside it will not
            # append to tails, like the luji2 below
            "luji2": {"bai": "%prne", "JUJI": 10},
            "luji3": {"bai": "%prne", "JUJI": 10},
            "luji4": {
                "bai": "%prne",
                "JUJI": 10,
                "a2JUJI": {"zSBA": 10, "JIA": {}},
            },
            "luji0": {"bai": "%prne", "JUJI": 10},
            "lujii": {"bai": "%prne", "JUJI": 10},
            # "luji5": {"bai": "%prne", "JUJI": 10},
            "cmd": "pulsectl $[1,2,3] %prne",
            "param": "$[1,2,3] %prne %cmd",
            "bind": "SHIFT $[1,2,3]",
        },
        "bj": {
            "xx": {"zp": {"jj": {"odja": {}, "mpaba": 10, "z": {}}}, "baka": 100},
            "zika": {},
            "duma": {},
            "a": {},
            "a": 10,
        },
        "zipa": 10,
        "ap": {},
        "xj": {"xx": {"zp": {}, "soap": {}, "oba": {}}, "o": 10, "z": {}, "d": {}},
        # "bj": {},
        "cj": {},
        "ej": {},
        "ecc": {},
        # "ecc2": {},
        "volume-new": {
            "cmd": "pulsectl %xda",
            # "xda": "bruh",
            "param": "%cmd $[up,down]",
            "luji25": {
                "bai": "%prne",
            },
            "luji23": {"bai": "%prne", "aa": {}},
            "luji52": {"bai": "%prne", "JUJI": 10},
            "luji3": {"bai": "%prne", "JUJI": 10},
            "bind": "SHIFT $[a,b]",
        },
        "buoa": {
            "luji51": {"bai": "%prne", "JUJI": 10},
            "lujix5": {"bai": "%prne", "JUJI": 10},
            # "lujix51": {"bai": "%prne", "JUJI": 10},
            "lujix5x": {"bai": "%prne", "2JUJI": {"SBA": 10}, "wUJI1": {"a": 10}},
        },
        "buoaaA": {
            "s": {"ziap": 1000},
            "bina": {},
            "L": {"lucla": {}},
            "xL": {"a": 10},
        },
        "buoaax": {"s": {}, "b": {}, "L": {}, "xL": {"a": 10}},
        #      switch zone,post switch,{non-critical},switch
    },
    "eona": {"a": 10, "s": {}},
}

# VALID_UTILITY_TEST = complexNested
# VALID_UTILITY_TEST = simpleTest
# VALID_UTILITY_TEST = moderateNested
VALID_UTILITY_TEST = continualNest
# VALID_UTILITY_TEST = cTest

# VALID_UTILITY_TEST = superNested
