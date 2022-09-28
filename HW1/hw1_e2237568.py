

def UnInformedSearch(method_name, problem_file_name, maximum_depth_limit):
    with open(problem_file_name, mode='r') as f:
        start = f.readline().removesuffix('\n')
        target = f.readline().removesuffix('\n')

        matrix = []
        for line in f:
            matrix.append(line.removesuffix('\n').split(' '))

        for i in matrix:
            i[2] = int(i[2])

        nodeNames = []
        for node in matrix:
            if node[0] not in nodeNames:
                nodeNames.append(node[0])
            if node[1] not in nodeNames:
                nodeNames.append(node[1])

        adj = []
        for name in nodeNames:
            dict = {"Name": name,
                    "adj": [],
                    "visited": False,
                    "level": 0,
                    "distance" : 0,
                    "route": []
                    }
            for conn in matrix:
                if conn[0] == name:
                    dict["adj"].append([conn[1], conn[2]])
                if conn[1] == name:
                    dict["adj"].append([conn[0], conn[2]])
            adj.append(dict)

        startNode = next((sub for sub in adj if sub['Name'] == start), None)
        if not startNode: return

        solution = None

        depth = 0
        traverse = []
        queue = [startNode]
        finished = False

        if method_name == 'BFS':

            soln = [target]
            startNode["visited"] = True
            traverse = [startNode["Name"]]

            while queue:
                depth += 1
                temp = queue.pop(0)
                if temp["Name"] == target:
                    break
                for item in temp["adj"]:
                    new = next(sub for sub in adj if sub['Name'] == item[0])
                    traverse.append(new["Name"])

                    if not new["visited"]:
                        new["route"] = temp["Name"]
                        new["level"] = temp["level"] + 1
                        queue.append(new)
                        new["visited"] = True

            currentDepth = next(sub for sub in adj if sub['Name'] == target)["level"]
            solFind = next(sub for sub in adj if sub['Name'] == target)
            if not solFind["route"]: return None

            while solFind["Name"] != start:
                soln.append(solFind["route"])
                solFind = next(sub for sub in adj if sub['Name'] == soln[-1])

            soln.reverse()
            return soln, traverse, currentDepth

        if method_name == 'DLS':
            soln = [target]
            currentDepth = 0
            finished = False
            startNode["visited"] = False

            HelperDLS(adj, maximum_depth_limit, 0, startNode, traverse, target)

            currentDepth = next(sub for sub in adj if sub['Name'] == target)["level"]
            solFind = next(sub for sub in adj if sub['Name'] == target)
            if not solFind["route"]: return None

            while solFind["Name"] != start:
                soln.append(solFind["route"])
                solFind = next(sub for sub in adj if sub['Name'] == soln[-1])

            soln.reverse()
            if len(soln)-1 > maximum_depth_limit : return None

            return soln, traverse, len(soln)-1

        elif method_name == 'IDDFS':

            soln = [target]
            currentDepth = 0
            finished = False
            startNode["visited"] = False

            HelperIDDFS(adj, maximum_depth_limit, 0, startNode, traverse, target)

            currentDepth = next(sub for sub in adj if sub['Name'] == target)["level"]
            solFind = next(sub for sub in adj if sub['Name'] == target)
            if not solFind["route"]: return None

            while solFind["Name"] != start:
                soln.append(solFind["route"])
                solFind = next(sub for sub in adj if sub['Name'] == soln[-1])

            soln.reverse()
            if len(soln) - 1 > maximum_depth_limit: return None

            return soln, traverse, len(soln)-1

        elif method_name == 'UCS':

            soln = [target]
            currentDepth = 0
            finished = False
            startNode["visited"] = False
            cost = 0
            queue = [startNode]

            i=0
            while queue:
                current = queue[i]
                traverse.append(current["Name"])
                current["visited"] = True

                for item in current["adj"]:
                    new = next(sub for sub in adj if sub['Name'] == item[0])
                    adjacencySort(new["adj"])
                    if current["distance"] + item[1] < new["distance"] or new["distance"] == 0 and new["Name"] != start:
                        new["route"] = current["Name"]
                        new["distance"] = current["distance"] + item[1]
                        queue.append(current)
                    if not new["visited"]:
                        queue.append(new)
                if finished: break
                i += 1
                if len(queue) == i:
                    break

            cost = next(sub for sub in adj if sub['Name'] == target)["distance"]
            currentDepth = next(sub for sub in adj if sub['Name'] == target)["level"]

            solFind = next(sub for sub in adj if sub['Name'] == target)
            if not solFind["route"]: return None

            while solFind["Name"] != start:
                soln.append(solFind["route"])
                solFind = next(sub for sub in adj if sub['Name'] == soln[-1])

            soln.reverse()

            return soln, traverse, len(soln)-1, cost

    return


def HelperDLS(adj, limit, currentDepth, node, visitedNodes, target):
    if currentDepth > limit:
        return

    node["visited"] = True
    node["level"] = currentDepth
    visitedNodes.append(node["Name"])
    if node["Name"] == target: return

    for item in node["adj"]:
        new = next(sub for sub in adj if sub['Name'] == item[0])
        if new["visited"] and new["level"] > currentDepth + 1:
            new["route"] = node["Name"]
            HelperDLS(adj, limit, currentDepth + 1, new, visitedNodes, target)
        if not new["visited"]:
            new["route"] = node["Name"]
            HelperDLS(adj, limit, currentDepth + 1, new, visitedNodes, target)
    return


def HelperIDDFS(adj, limit, currentDepth, node, visitedNodes, target):
    if currentDepth > limit:
        return

    node["visited"] = True
    node["level"] = currentDepth
    visitedNodes.append(node["Name"])
    if node["Name"] == target: return

    for item in node["adj"]:
        new = next(sub for sub in adj if sub['Name'] == item[0])
        if new["visited"] and new["level"] > currentDepth + 1:
            new["route"] = node["Name"]
            HelperDLS(adj, limit - 1, currentDepth + 1, new, visitedNodes, target)
        if not new["visited"]:
            new["route"] = node["Name"]
            HelperDLS(adj, limit - 1, currentDepth + 1, new, visitedNodes, target)
    return


def adjacencySort(_list):
    for x in _list:
        for y in _list:
            if x[1] < y[1]:
                temp = x
                y = x
                x = y
    return


print(UnInformedSearch("UCS", 'sampleproblem2.txt', 4))
