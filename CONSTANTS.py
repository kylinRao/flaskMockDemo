import fileinput


class CONSTANTS:
    MATCH_DIC = {}

    def __init__(self):
        self.refresh_match_dic()

    @staticmethod
    def refresh_match_dic(filename="matchResponse.py"):
        CONSTANTS.MATCH_DIC = {}
        for line in fileinput.input(filename):
            uri, request_match, response_match = line.split("|")
            CONSTANTS.MATCH_DIC.update({"uri": uri, "request_match": request_match, "response_match": response_match})
