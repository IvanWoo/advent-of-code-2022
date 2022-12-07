from __future__ import annotations

import fileinput
from dataclasses import dataclass, field
from math import inf
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@dataclass
class NaryNode:
    name: str = None
    size: int = None
    parent: NaryNode = None
    children: list[NaryNode] = field(default_factory=list)


def build_file_tree():
    file_tree = NaryNode()
    curr_tree = file_tree
    for row in get_input():
        if row.startswith("$"):
            exp = row.split(" ")
            cmd = exp[1]
            if cmd == "cd":
                name = exp[2]
                if name == "..":
                    curr_tree = curr_tree.parent
                elif name == "/":
                    curr_tree.children.append(NaryNode(name=name))
                    curr_tree = curr_tree.children[0]
                else:
                    for child in curr_tree.children:
                        if child.name == name:
                            curr_tree = child
                            break
            elif cmd == "ls":
                ...
        elif row.startswith("dir"):
            _, name = row.split(" ")
            curr_tree.children.append(NaryNode(name=name, parent=curr_tree))
        elif row[0].isnumeric():
            size, name = row.split(" ")
            curr_tree.children.append(
                NaryNode(name=name, size=int(size), parent=curr_tree)
            )
    return file_tree


def q1():
    file_tree = build_file_tree()

    def traverse(node):
        nonlocal count
        if not node:
            return 0
        if node.size is not None:
            return node.size
        size = 0
        for child in node.children:
            size += traverse(child)
        if size <= 100000:
            count += size
        return size

    count = 0
    traverse(file_tree)
    return count


def q2():
    file_tree = build_file_tree()

    def traverse(node):
        nonlocal count
        if not node:
            return 0
        if node.size is not None:
            return node.size
        size = 0
        for child in node.children:
            size += traverse(child)
        if node.name:
            count[node.name] = size
        return size

    count = dict()
    total = traverse(file_tree)
    need = 30000000 - (70000000 - total)
    ans = None
    min_diff = inf
    for k, v in count.items():
        diff = v - need
        if diff >= 0 and diff < min_diff:
            ans = k
            min_diff = diff
    return count[ans]


def main():
    print(q1())
    print(q2())
    assert q1() == 1348005
    assert q2() == 12785886


if __name__ == "__main__":
    main()
