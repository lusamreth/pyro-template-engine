import json

from test_subj import VALID_UTILITY_TEST

from analyzer.scope_analyzer import SimpleTreeWalker


def runTestSample():
    treeWalker = SimpleTreeWalker()
    # analyzed = simpleWalk(VALID_UTILITY_TEST)
    analyzed = treeWalker.treewalk(VALID_UTILITY_TEST)
    del analyzed["prev"]
    analyzerTestPrefix = "test_results"
    analyzerTestFileName = "scope_analyzer_results.json"
    refFd = open(
        "../{}/{}".format(analyzerTestPrefix, analyzerTestFileName),
        "w+",
    )

    # GREAT PROGRESS SO FAR SO GOOD
    json.dump(analyzed, refFd)


if __name__ == "__main__":
    runTestSample()
