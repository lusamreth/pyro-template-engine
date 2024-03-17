import json

scopeResultPrefix = "test_results"
scopeAnalyzerResultFile = open(
    "{}/scope_analyzer_results.json".format(scopeResultPrefix), "r"
)

scopeAnalyzerReferenceResultFile = open(
    "{}/scope_analyzer_results_reference.json".format(scopeResultPrefix), "r"
)

scopeAnalyzerResult = json.loads(scopeAnalyzerResultFile.read())
scopeAnalyzerResultRef = json.loads(scopeAnalyzerReferenceResultFile.read())
analyzerResult = scopeAnalyzerResult.get("result")
analyzerResultRef = scopeAnalyzerResult.get("result")

scopeAnalyzerResultFile.close()
scopeAnalyzerReferenceResultFile.close()


def crawler(dictionary, k):
    # dictKeys = [k for k in dictionary.keys() if isinstance(dictionary[k], dict)]
    # dictKeys = [dictionary.keys()]

    print("--", k, dictionary)
    # for k in dictKeys:
    for k in dictionary:
        if isinstance(dictionary[k], dict):
            crawler(dictionary[k], k)
        else:
            print("not a dict -- ", dictionary[k], k)


print("prototype:")
crawler(analyzerResult, "")

print("reference:")


def compare_arrays(arr1, arr2):
    """
    Compare elements of two arrays.

    Args:
    arr1 (list): The first array.
    arr2 (list): The second array.

    Returns:
    bool: True if the arrays have the same elements in the same order, False otherwise.
    """

    if len(arr1) != len(arr2):
        return False

    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False

    return True


def compare_dicts(dict1, dict2):
    return compare_arrays(list(dict1.keys()), list(dict2.keys()))


crawler(analyzerResultRef, "")

print("ref key", analyzerResultRef.keys())

isDictSame = compare_dicts(analyzerResult, analyzerResultRef)
print("is same", isDictSame)
