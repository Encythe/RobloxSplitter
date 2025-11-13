# Universally Nothing
START_OR_SPLIT = "startorsplit"
SPLIT = "split"
UNSPLIT = "unsplit"
SKIP_SPLIT = "skipsplit"
PAUSE = "pause"
RESUME = "resume"
RESET = "reset"
START_TIMER = "starttimer"
PAUSE_GAME_TIME = "pausegametime"
UNPAUSE_GAME_TIME = "unpausegametime"
ALWAYS_PAUSE_GAME_TIME = "alwayspausegametime"
SWITCH_TO_REALTIME = "switchto realtime"
SWITCH_TO_GAMETIME = "switchto gametime"
def SET_GAME_TIME(TIME: int): return f"setgametime {TIME}"
def SET_LOADING_TIMES(TIME: int): return f"setloadingtimes {TIME}"
def ADD_LOADING_TIMES(TIME: int): return f"addloadingtimes {TIME}"
def SET_COMPARISON(COMPARISON): return f"setcomparison {COMPARISON}"
def SET_SPLIT_NAME(INDEX: int, NAME: str): return f"setsplitname {INDEX} {NAME}"
def SET_CURRENT_SPLIT_NAME(NAME: str): return f"setcurrentsplitname {NAME}"
def SET_CUSTOM_VARIABLE(OBJ: dict): 
    import json
    return f"setcustomvariable {json.dumps(OBJ)}"

# Returns a time. Useless in the context of Roblox.
GET_LAST_SPLIT_TIME = "getlastsplittime"
GET_COMPARISON_SPLIT_TIME = "getcomparisonsplittime"
GET_CURRENT_REAL_TIME = "getcurrentrealtime"
GET_CURRENT_GAME_TIME = "getcurrentgametime"
GET_CURRENT_TIME = "getcurrenttime"
GET_BEST_POSSIBLE_TIME = "getbestpossibletime"
def GET_DELTA(COMPARISON: str = None): 
    if COMPARISON: return f"getdelta {COMPARISON}"
    return "getdelta"
def GET_FINAL_TIME(COMPARISON: str = None):
    if COMPARISON: return f"getfinaltime {COMPARISON}"
    return "getfinaltime"
def GET_PREDICTED_TIME(COMPARISON: str):
    return f"getpredictedtime {COMPARISON}"

# Returns an integer. Practically useless in the context of Roblox.
GET_SPLIT_INDEX = "getsplitindex"
GET_ATTEMPT_COUNT = "getattemptcount"
GET_COMPLETED_COUNT = "getcompletedcount"

# Returns a string. Might be useful in some way.
GET_CURRENT_SPLIT_NAME = "getcurrentsplitname"
GET_PREVIOUS_SPLIT_NAME = "getprevioussplitname"
GET_CURRENT_TIMER_PHASE = "getcurrenttimerphase"
def GET_CUSTOM_VARIABLE_VALUE(NAME: str): return f"getcustomvariablevalue {NAME}"
PING = "ping"