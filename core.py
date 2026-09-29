"""乳品厂核心逻辑：原料、发酵、质检和冷链。"""

import json


def new_game():
    return {
        "batches": {},
        "tank_load": 0,
        "tank_capacity": 100,
        "ingredient": 100,
        "day": 1,
        "batch_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["batch_id"] += 1
    return state


def feed(state, batch_id, amount):
    state["batches"][batch_id] = {"amount": amount, "defect": False}
    state["tank_load"] += amount
    state["ingredient"] -= amount
    return True


def check_temp(state, temp):
    if temp < 30:
        return "over"
    return "ok"


def cancel_ferment(state, batch_id):
    return True


def inspect(state, batch_id):
    if state["batches"][batch_id].get("defect"):
        return False
    return True


def output(state, amount):
    return True


def holiday(state):
    for batch in state["batches"].values():
        batch["amount"] += 20
    return True


def main():
    print("乳品厂 - 命令: feed/temp/cancel/inspect/output/holiday/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
