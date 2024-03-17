import json
import uuid
from typing import OrderedDict


def pretty_print(result):
    print(json.dumps(result, sort_keys=True, indent=4))


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)


dict_ptr = {
    "root_keys": {},
    "prev": [],
    "upholding_root": [],
    "upholding_key": "",
    "persist_key": {},
    "pk": "",
}


prev_scope = {}


def hasChildren(scope):
    return scope.get("children") is not None


class ScopeAnalyzer:
    def __init__(self):
        self.result = {}
        self.prev_scope = {}
        self.parent_tree_list = []

    def build_scope_maker(self, values):
        transformer = self.make_transformer(values)

        def make_scope(root, parent_keys, offset=None, value=None, level=0):
            scope = {
                "root": root,
                "children": transformer(parent_keys),
                "level": level,
            }
            if offset:
                scope["offset"] = offset
            if value:
                scope["value"] = value

            return scope

        return make_scope

    def make_transformer(self, parent_values):
        def transform_each(enum_val):
            i, k = enum_val
            return {
                "root": k,
                "parent": self.parent_tree_list.copy(),
                "offset": i,
                "value": parent_values[k],
            }

        def transformer(v):
            return list(map(transform_each, enumerate(v)))

        return transformer

    # parent tree helper
    def reset_parent_tree(self, curr_parent_root):
        if len(self.parent_tree_list) > 0:
            self.parent_tree_list.clear()

        self.parent_tree_list.append(curr_parent_root)

    def append_new_parent_to_tree(self, scope, curr_parent_root):
        corrected_level = scope["level"]
        if corrected_level == 0:
            self.parent_tree_list = [self.parent_tree_list[0]]
        self.parent_tree_list.append(curr_parent_root)

    def determine_parent_tree_list(self, scope, curr_parent_root):
        if scope.get("root") is None:
            self.reset_parent_tree(curr_parent_root)
        else:
            self.append_new_parent_to_tree(scope, curr_parent_root)

    def analyze_scope(self, raw_dict, scope={}):
        encapsulated_scope = self.result

        for k in raw_dict.keys():
            v = raw_dict[k]
            make_scope = self.build_scope_maker(v)
            offset = 0
            if isinstance(v, dict):
                input_scope = scope
                # print("END", ks[-1])

                self.determine_parent_tree_list(scope, curr_parent_root=k)
                isLevelZeroRoot = scope.get("root") is None

                if isLevelZeroRoot:
                    input_scope = make_scope(root=k, parent_keys=v.keys())
                    self.prev_scope = input_scope

                else:
                    # this code is for probing the parent root key
                    # that has ->
                    # nested dictionary with its(child) inside
                    def find_sub_parent():
                        count = None
                        for i, child in enumerate(input_scope["children"]):
                            if child["root"] == k:
                                count = i
                        return count

                    corrected_level = scope["level"]
                    print(
                        "COCO",
                        k,
                        self.parent_tree_list,
                        corrected_level,
                        self.parent_tree_list[corrected_level - 1 :],
                    )

                    has_children = find_sub_parent()
                    # we replace the sub_parent(children that contain nested
                    # dictionary) with its own tree of children
                    if has_children:
                        sub_parent = input_scope["children"].pop(has_children)
                        inner_scope = make_scope(
                            root=k,
                            offset=sub_parent["offset"],
                            level=input_scope["level"] + 1,
                            parent_keys=v.keys(),
                        )
                        input_scope["children"].append(inner_scope)
                        input_scope = inner_scope

                self.analyze_scope(v, input_scope)

            if len(list(scope.keys())) == 0 and isinstance(v, dict):
                encapsulated_scope[k] = self.prev_scope

        return encapsulated_scope


def analyze_scope(raw_dict):
    raw_dict[str(uuid.uuid4().time)] = str(uuid.uuid4())
    print("STEP SCOPE", raw_dict)
    return ScopeAnalyzer().analyze_scope(raw_dict)


# analyze_scope = ScopeAnalyzer().analyze_scope
# analyze_scope(pina)


# ["children"]


class ScopePointer:
    def __init__(self):
        self.curr_ptr = ""
        self.prev_ptr = ""
        self.layers = {}
        self.max_layer = 0
        self.layer_prefix = "L_"

    def layer_key(self, num):
        return f"{self.layer_prefix}{num}"

    def push_to_layer(self, layer_num, payload):
        if self.max_layer < layer_num:
            self.max_layer
        prev_layer = self.fetch_from_layer(layer_num)
        key = self.layer_key(layer_num)

        each_key_layer = {
            "key_value": payload,
            "parent": self.prev_ptr,
        }
        if prev_layer is None:
            self.layers[key] = []

        self.layers[key].append(each_key_layer)

    def exist_in_layer(self, layer, needle):
        targeted_layer = self.fetch_from_layer(layer)
        if targeted_layer is None:
            return None

        def finder(layer_data):
            return layer_data["key_value"] == needle

        print("LL", self.fetch_from_layer(layer))
        llv = list(filter(finder, targeted_layer))
        if len(llv) > 0:
            return llv

    def fetch_from_layer(self, layer_num):
        return self.layers.get(self.layer_key(layer_num))

    def point_to_curr(self, current):
        self.prev_ptr = self.curr_ptr
        self.curr_ptr = current

    # def detect_layer_switch(curr_level):

    # if self.prev > self.curr_ptr :
    # pass
    # if self.prev


# def transform_layer(scope_root,ptr,transformer):
#   ptr.get()
# transformer()

search_index = "x"


def get_only(children, key):
    def mapper(child):
        root = child.get(key)
        if root is None:
            raise Exception("Invalid children type !!")
        return root

    return list(map(mapper, children))


Utility_VAR = ["setting", "volume", "gaming"]
# VALID_UTILITY_TEST = {"xda": {"xda": {"bubu": {"xda": {}}}}}
VALID_UTILITY_TEST = {
    "settings": {
        # "cmd": "pulsectl %sos",
        "xda": 100,
        "can": 100,
        "volume": {
            "prne": 1,
            # "lumen": {"xabit": "%prne", "AA": 10},
            "luji": {"bai": "%prne", "JUJI": 10, "xo": {}},
            "luji2": {"bai": "%prne", "JUJI": 10},
            # "luji3": {"bai": "%prne", "JUJI": 10},
            # "luji4": {"bai": "%prne", "JUJI": 10},
            # "luji5": {"bai": "%prne", "JUJI": 10},
            "prne": "%can xd",
            "cmd": "pulsectl $[1,2,3] %prne",
            "param": "$[1,2,3] %prne %cmd",
            "bind": "SHIFT $[1,2,3]",
            "bind": "SHIFT $[4,2,3]",
        },
        "volume-new": {
            "cmd": "pulsectl %xda",
            # "xda": "bruh",
            "param": "%cmd $[up,down]",
            "luji2": {"bai": "%prne",},
            "luji3": {"bai": "%prne", "JUJI": 10},
            "bind": "SHIFT $[a,b]",
            "luji4": {"bai": "%prne", "JUJI1": {"a":10}, "2JUJI": {"SBA": 10}},
            "luji5": {"bai": "%prne", "JUJI": 10},
        },
        "buoa": {},
    },
}


result2 = analyze_scope(VALID_UTILITY_TEST)
pretty_print(result2)

layers = {}


# def dict_paths(dictionary, level=0, parents=[], paths=[]):
#     for key in dictionary:
#         key = str(key)
#         parents = parents[0:level]
#         paths.append(parents + [key])
#         if isinstance(dictionary[key], dict) and dictionary.get(key) is not None:
#             parents.append(key)
#             dict_paths(dictionary[key], level + 1, parents, paths)
#     return paths


laidOutScope = {}

scopa = []


# probing(result2, Utility_VAR)
def simpleWalk(dictionary, level=0, parents=[], prev=OrderedDict()):
    offset = 0

    dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]

    for key in dictionary.keys():
        if isinstance(dictionary[key], dict):
            childKeys = [
                k for k in dictionary.keys() if isinstance(dictionary[k], dict)
            ]

            scopa.append(childKeys)
            childKey = {}
            for chk in childKeys:
                # childKey[chk] = {"children": list(dictionary[key].keys())}
                childKey[chk] = {"children": []}

            prev[level] = childKey

            # print(key)
            if len(prev) > 0:
                # print("prev", prev.get(level - 1), prev.get(level), key, level)
                upperEchalon = prev.get(level - 1) or {}
                if not key in upperEchalon:
                    childKey["level"] = level
                    childKey["levelCount"] = 1

                    laidOutScope[level] = childKey
                    # lebeyScope[level] = childKey
                    parents.append(key)
                    # if lebeyScope.get(level - 1) is not None:
                    if laidOutScope.get(level - 1) is not None:
                        lbd = laidOutScope[level - 1]
                        scopeLeveled = list(laidOutScope[level - 1].keys())
                        lvCount = lbd["levelCount"]
                        childIndex = scopeLeveled[lvCount - 1]
                        laidOutScope[level - 1][childIndex]["children"].append(key)

                        print(
                            "--- switch",
                            level - 1,
                            laidOutScope[level - 1],
                        )

                    print("--- switch root current key : {}".format(key), laidOutScope)
                    level += 1
                else:

                    def adjustScopeChildren(scopePoint):
                        if laidOutScope.get(level - 1) is not None:
                            lvCount = laidOutScope[scopePoint]["levelCount"]
                            scopeLeveled = list(laidOutScope[scopePoint].keys())
                            childIndex = scopeLeveled[lvCount - 1]

                            laidOutScope[scopePoint][childIndex]["children"].append(key)
                            laidOutScope[level - 1]["levelCount"] += 1

                    if laidOutScope.get(level - 1) is not None:
                        if level - 2 < 0:
                            # print("buffer alert", lebeyScope)
                            continue

                        lvCount = laidOutScope[level - 2]["levelCount"]
                        scopeLeveled = list(laidOutScope[level - 2].keys())
                        childIndex = scopeLeveled[lvCount - 1]
                        laidOutScope[level - 2][childIndex]["children"].append(
                            key
                            # {"parent": key, "value": dictionary[key]}
                        )

                        print(
                            "this belong to",
                            scopeLeveled[lvCount - 1],
                            laidOutScope.get(level - 1),
                            key,
                        )

                        laidOutScope[level - 1]["levelCount"] += 1
                        pass
                pass

            simpleWalk(dictionary[key], level=level, prev=prev)
        else:
            offset = 0
            if layers.get(key):
                layers[key].remove(key)
            # print("CHILD->", key, dictionary[key])
            # do something with dictionary[k]
            pass


simpleWalk(VALID_UTILITY_TEST)
print("layers", json.dumps(laidOutScope, sort_keys=True, indent=4))

# parent assembly
result = {}
original = VALID_UTILITY_TEST
prev = {}

"""
    result = {"settings":{}}
    
"""




def replacer():
    global prev
    maxLevel = 3
    for key in laidOutScope.keys():
        print("k", key)
        efodir = laidOutScope[key]
        del efodir["level"]
        del efodir["levelCount"]
        
        for dir in efodir:
            efodirChild = efodir[dir]["children"].copy()
            _len = len(efodirChild)
            _copyable = False

            if prev.get("tag") is None:
                prev = {"tag": dir, "counter": 0, "max": _len, "layer": key}
                _copyable = True
            else:
                if prev["max"] == prev["counter"] and _len > 0:
                    _copyable = False
                    pLayer = prev["layer"]

                    print("finished copying first layer", prev)
                    print("lebeyScope[pLayer]", laidOutScope[pLayer])
                    prev = {"tag": prev["tag"], "counter": 0, "max": _len, "layer": key}

                    # prev = {"tag": dir, "counter": 0, "max": _len}

                else:
                    if prev["max"] > prev["counter"]:
                        prev["counter"] += 1

                        print("ba", prev)
                    def setParent(level,childIndex=0):
                        if result[prev["tag"]].get(dir) is not None:
                            pTag = prev["tag"]
                            result[pTag][dir] = {
                                "children": efodirChild,
                                "parent": [pTag, dir],
                            }

                            if childIndex < len(efodirChild):
                                upBy1 = laidOutScope[level + 1]
                                childLabel = efodirChild[childIndex]
                                print("LADI",upBy1,level,dir,
                                      upBy1.get(childLabel),efodirChild[childIndex])
                                setParent(level,childIndex+1)
                            # if level < maxLevel + 1:
                            #     print("LADI",laidOutScope[level],level,dir)
                            #     setParent(level+1,childIndex+1)
                            
                            print("abc", dir, efodirChild)
                    print("ladi outside",dir)
                    setParent(key)

            print("key dir dir", key)
            while len(efodirChild) > 0 and _copyable:
                child = efodirChild.pop()
                if result.get(dir) is None:
                    result[dir] = {}
                else:
                    result[dir][child] = {}
        print(efodir)


replacer()
print(result, prev)


# def convert_to_layers(all_scopes):
#     layer_result = {}
#     for scope_key in all_scopes.keys():
#         scope = all_scopes[scope_key]
#         ptr = ScopePointer()

# from syntax_decoder import generate_token, multiCommandParser

#         def internal_call(scope):
#             children = scope.get("children")
#             if children:
#                 level = scope["level"]
#                 root = scope["root"]

#                 ptr.point_to_curr([scope["root"]])
#                 ptr.push_to_layer(level, scope["root"])

#                 if level > 0:
#                     # scope_ptr["prev_ptr"] =
#                     # ptr.point_to_prev
#                     print(f"IN LEVEL {level} in scope {root}")

#                 global current_level
#                 current_level = scope["level"]
#                 # for child in children:
#                 #     internal_call(child)
#                 print("EDX", scope["root"], scope)
#             else:
#                 # layer_result[]
#                 ptr.point_to_curr(scope["parent"])
#                 lv = scope.get("level") or 1
#                 ptr.push_to_layer(lv, scope["root"])

#         internal_call(scope)

#         layer_result[scope_key] = ptr.layers
#     return layer_result
