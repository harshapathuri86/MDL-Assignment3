ROLL_NUMBER = 2019101105
GAMMA = 0.5
NUM_ACTIONS = 5
ROWS = 2
COLUMNS = 4
ACTION_PROBABILITY = 1 - (((ROLL_NUMBER % 10000) % 30 + 1) / 100)

ACTIONS = {
    "UP": (0, 1),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "STAY": (0, 0),
}

PROBS = {
    "target": {
        "UP": 0.1,
        "DOWN": 0.1,
        "LEFT": 0.1,
        "RIGHT": 0.1,
        "STAY": 0.6,
    },
    "call": {
        True: 0.5,
        False: 0.1,
    },
    "player": {
        1: ACTION_PROBABILITY,
        -1: 1 - ACTION_PROBABILITY,
    },
}

ACTIONS_CODES = {
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT": 3,
    "STAY": 4,
}

ACTIONS_FROM_CODES = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    4: "STAY",
}

REWARDS = {
    "STEP_COST": -1,
    "CALL_REWARD": ROLL_NUMBER % 90 + 10,
}


class State:
    def __init__(self, agent_row, agent_column, target_row, target_column, call):
        if (
            (agent_row not in range(ROWS))
            or (agent_column not in range(COLUMNS))
            or (target_row not in range(ROWS))
            or (target_column not in range(COLUMNS))
            or (call not in [True, False])
        ):
            raise ValueError

        self.agent_row = agent_row
        self.agent_column = agent_column
        self.target_row = target_row
        self.target_column = target_column
        self.call = call

    def show(self):
        return (
            self.agent_row,
            self.agent_column,
            self.target_row,
            self.target_column,
            self.call,
        )

    def index(self):
        return (
            self.call
            + self.target_column * 2
            + self.target_row * COLUMNS * 2
            + self.target_column
            + ROWS * COLUMNS * 2
            + self.target_row
            + COLUMNS * ROWS * COLUMNS * 2
        )

    def __str__(self):
        return f"({self.agent_row}, {self.agent_column}, {self.target_row}, {self.target_column}, {self.call})"


def get_positions(x, y, max_x, max_y, positions=[]):
    if x >= max_x or y >= max_y:
        return
    positions.append((x, y))
    get_positions(x + 1, y, max_x, max_y, positions)
    get_positions(x, y + 1, max_x, max_y, positions)


def get_states():
    positions = []
    states = []
    get_positions(0, 0, ROWS, COLUMNS, positions)
    for position_agent in positions:
        for position_target in positions:
            for call in [True, False]:
                states.append(
                    State(
                        position_agent[0],
                        position_agent[1],
                        position_target[0],
                        position_target[1],
                        call,
                    )
                )
    return states


def action(action_type, state):
    state = State(*state)
    states = []
    if state[0] == state[2] and state[1] == state[3] and state[4]:
        for action_type in ACTIONS:
            for target in PROBS["target"]:
                for call in PROBS["call"]:
                    for player in PROBS["player"]:
                        states.append(
                            (
                                State(
                                    min(
                                        max(0, state[0] + player * action_type[0]),
                                        ROWS - 1,
                                    ),
                                    min(
                                        max(0, state[1] + player * action_type[1]),
                                        COLUMNS - 1,
                                    ),
                                    min(
                                        max(0, state[2] + ACTIONS[target][0]), ROWS - 1
                                    ),
                                    min(
                                        max(0, state[3] + ACTIONS[target][1]),
                                        COLUMNS - 1,
                                    ),
                                    call,
                                ),
                                PROBS["target"][target]
                                * PROBS["call"][call]
                                * PROBS["player"][player],
                            )
                        )
    else:
        for action_type in ACTIONS:
            for target in PROBS["target"]:
                for player in PROBS["player"]:
                    states.append(
                        (
                            State(
                                min(
                                    max(0, state[0] + player * action_type[0]), ROWS - 1
                                ),
                                min(
                                    max(0, state[1] + player * action_type[1]),
                                    COLUMNS - 1,
                                ),
                                min(max(0, state[2] + ACTIONS[target][0]), ROWS - 1),
                                min(max(0, state[3] + ACTIONS[target][1]), COLUMNS - 1),
                                0,
                            ),
                            PROBS["target"][target] * PROBS["player"][player],
                        )
                    )
    return states


def observations(states):
    lol = []
    for state in states:
        val = "O: * : "
        if (
            state.target_row == state.agent_row
            and state.target_column == state.agent_column
        ):
            # same position
            val += str(state.index()) + " o1 "
            val += str(float(1))
        elif (
            state.target_row == state.agent_row
            and state.agent_column == state.target_column - 1
        ):
            # right
            pass
        elif (
            state.target_row == state.agent_row + 1
            and state.agent_column == state.target_column
        ):
            #
            pass
        elif (
            state.target_row == state.agent_row
            and state.agent_column == state.target_column - 1
        ):
            pass
        elif (
            state.target_row == state.agent_row
            and state.agent_column == state.target_column - 1
        ):
            pass
        elif (
            state.target_row == state.agent_row
            and state.agent_column == state.target_column - 1
        ):
            pass
