# Print Left View of Binary Tree

tree = {
    "value": 10,
    "left": {
        "value": 5,
        "left": {
            "value": 2,
            "left": {
                "value": 1,
                "left": None,
                "right": None
            },
            "right": None
        },
        "right": {
            "value": 8,
            "left": None,
            "right": None
        }
    },
    "right": {
        "value": 15,
        "left": None,
        "right": {
            "value": 20,
            "left": None,
            "right": None
        }
    }
}


def print_left_view(tree):
    if tree is None:
        return

    queue = [tree]
    while queue:
        node = queue.pop(0)
        print(node["value"])

        if node["left"]:
            queue.append(node["left"])
        if node["right"]:
            queue.append(node["right"])


print_left_view(tree)