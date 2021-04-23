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
        1: 0.5,
        0: 0.1,
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
            or (call not in [0, 1])
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
            + self.agent_column * ROWS * COLUMNS * 2
            + self.agent_row * COLUMNS * ROWS * COLUMNS * 2
        )

    def __str__(self):
        return f"({self.agent_row}, {self.agent_column}, {self.target_row}, {self.target_column}, {self.call})"


def get_positions(x, y, max_x, max_y, positions=[]):
    if x >= max_x or y >= max_y:
        return
    if (x, y) not in positions:
        positions.append((x, y))
    get_positions(x + 1, y, max_x, max_y, positions)
    get_positions(x, y + 1, max_x, max_y, positions)


def get_states():
    states = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            for k in range(ROWS):
                for l in range(COLUMNS):
                    for b in [0, 1]:
                        states.append(State(i, j, k, l, b))
    return states


def terminal(state):
    return (
        state.agent_row == state.target_row
        and state.agent_column == state.target_column
        and state.call
    )


def actions(state):
    states = []
    if not terminal(state):
        for action_type in ACTIONS:
            for target in PROBS["target"]:
                for call in PROBS["call"]:
                    for player in PROBS["player"]:
                        states.append(
                            [
                                State(
                                    min(
                                        max(
                                            0,
                                            state.agent_row
                                            + player * ACTIONS[action_type][0],
                                        ),
                                        ROWS - 1,
                                    ),
                                    min(
                                        max(
                                            0,
                                            state.agent_column
                                            + player * ACTIONS[action_type][1],
                                        ),
                                        COLUMNS - 1,
                                    ),
                                    min(
                                        max(0, state.target_row + ACTIONS[target][0]),
                                        ROWS - 1,
                                    ),
                                    min(
                                        max(
                                            0, state.target_column + ACTIONS[target][1]
                                        ),
                                        COLUMNS - 1,
                                    ),
                                    call,
                                ),
                                PROBS["target"][target]
                                * (
                                    PROBS["call"][call]
                                    + (
                                        1 - sum(PROBS["call"].values())
                                        if call == state.call
                                        else 0
                                    )
                                )
                                * PROBS["player"][player],
                                action_type,
                                REWARDS["STEP_COST"] if action_type == "STAY" else 0,
                            ]
                        )
    else:
        for action_type in ACTIONS:
            for target in PROBS["target"]:
                for player in PROBS["player"]:
                    states.append(
                        [
                            State(
                                min(
                                    max(
                                        0,
                                        state.agent_row
                                        + player * ACTIONS[action_type][0],
                                    ),
                                    ROWS - 1,
                                ),
                                min(
                                    max(
                                        0,
                                        state.agent_column
                                        + player * ACTIONS[action_type][1],
                                    ),
                                    COLUMNS - 1,
                                ),
                                min(
                                    max(0, state.target_row + ACTIONS[target][0]),
                                    ROWS - 1,
                                ),
                                min(
                                    max(0, state.target_column + ACTIONS[target][1]),
                                    COLUMNS - 1,
                                ),
                                0,
                            ),
                            PROBS["target"][target] * PROBS["player"][player],
                            action_type,
                            REWARDS["STEP_COST"] if action_type == "STAY" else 0,
                        ]
                    )
    for state in states:
        if terminal(state[0]):
            state[3] += REWARDS["CALL_REWARD"]
    return states


def observations(states):
    o = ["O: * : * : * 0.0"]
    for state in states:
        val = "O: * : "
        if (
            state.target_row == state.agent_row
            and state.target_column == state.agent_column
        ):
            # same
            val += str(state.index()) + " : o1 "
        elif (
            state.target_row == state.agent_row
            and state.target_column == state.agent_column + 1
        ):
            # right
            val += str(state.index()) + " : o2 "
        elif (
            state.target_row == state.agent_row + 1
            and state.target_column == state.agent_column
        ):
            # below
            val += str(state.index()) + " : o3 "
        elif (
            state.target_row == state.agent_row
            and state.target_column == state.agent_column - 1
        ):
            # left
            val += str(state.index()) + " : o4 "
        elif (
            state.target_row == state.agent_row - 1
            and state.target_column == state.agent_column
        ):
            # above
            val += str(state.index()) + " : o5 "
        else:
            # none
            val += str(state.index()) + " : o6 "
        val += str(float(1))
        o.append(val)
    for i in o:
        print(i)
    return o


def initial_states(states):
    p = []
    n = 0
    for state in states:
        if state.target_row == 1 and state.target_column == 0:
            if (
                abs(state.agent_row - state.target_row)
                + abs(state.agent_column - state.target_column)
            ) <= 1:
                p.append(0)
            else:
                p.append(1)
                n += 1
        else:
            p.append(0)
    for i in range(len(p)):
        if p[i] == 1:
            p[i] = 1 / n
        print(p[i], end=" ")


if __name__ == "__main__":
    print(f"discount: {GAMMA}")
    print("values: reward")
    print("states: 128")
    print("actions: UP DOWN LEFT RIGHT STAY ")
    print("observations: o1 o2 o3 o4 o5 o6")
    print("start:")
    initial_states(get_states())
    print()
    print(f"T: * : * : * {0.0}")
    states = {}
    for state in get_states():
        # print("from state",str(state), state.index())
        for possiblity in actions(state):
            if (possiblity[2], state.index(), possiblity[0].index()) in states:
                states[(possiblity[2], state.index(), possiblity[0].index())][
                    0
                ] += possiblity[1]
                # print("lol adding ", possiblity[2],state.index(),possiblity[0].index(),"add",possiblity[1])
            else:
                states[(possiblity[2], state.index(), possiblity[0].index())] = [
                    possiblity[1],
                    possiblity[3],
                ]
                # print("lol new ", possiblity[2],state.index(),possiblity[0].index(),possiblity[1])
    for state in states:
        print(f"T: {state[0]} : {state[1]} : {state[2]} {states[state][0]}")
    observations(get_states())
    print(f"R: * : * : * : * {0.0}")
    for state in states:
        print(f"R: {state[0]} : {state[1]} : {state[2]} : * {states[state][1]}")
