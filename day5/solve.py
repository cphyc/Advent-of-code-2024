import enum
from pathlib import Path

class State(enum.Enum):
    RULE=1
    UPDATES=2

data = (Path(__file__).parent / "input").read_text()
test_data = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def parse(data: str):
    state = State.RULE
    rules: dict[int, int] = {}
    rules_tuple: list[tuple[int, int]] = []
    updates: list[list[int]] = []
    for line in data.splitlines():
        if line.strip() == "":
            # Reached
            state = State.UPDATES
            continue

        if state == State.RULE:
            from_, to_ = map(int, line.split("|"))
            rules[from_] = to_
            rules_tuple.append((from_, to_))
        elif state == State.UPDATES:
            updates.append(list(map(int, line.split(","))))

    return rules, rules_tuple, updates

def _check_rule(rules_tuple: list[tuple[int, int]], update: list[int]) -> bool:
    for i, orderi in enumerate(update):
        for orderj in update[:i]:
            if (orderi, orderj) in rules_tuple:
                # print(f"{orderi=} -> {orderj=} breaks the rules")
                return False
    return True

def part1(rules: dict[int, int], rules_tuple: list[tuple[int, int]], updates: list[list[int]]):
    total = 0
    for update in updates:
        if _check_rule(rules_tuple, update):
            total += update[len(update)//2]

    print(f"Part 1: {total}")

rules, inverted_rules, updates = parse(data)

part1(rules, inverted_rules, updates)
