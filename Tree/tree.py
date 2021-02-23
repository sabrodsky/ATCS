import random

class Node:
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data

    def get_children(self, start, children, mode='d'):
        if start:
            self.get_children(start.right, children, mode)
            if start.data > self.data:
                if mode == 'd':
                    children[1].append(start.data)
                else:
                    children[1].append(start)
            elif start.data < self.data:
                if mode == 'd':
                    children[0].append(start.data)
                else:
                    children[0].append(start)
            self.get_children(start.left, children, mode)
        return children

class Tree:
    def __init__(self):
        self.head = None

    def insert(self, data, mode='d'):
        if mode == 'd':
            node = Node(data)
        else:
            node = data
        if self.head:
            cur_node = self.head
            while True:
                # left child becomes node
                if cur_node.left == None and node.data < cur_node.data:
                    cur_node.left = node
                    break
                # right child becomes node
                if cur_node.right == None and node.data > cur_node.data:
                    cur_node.right = node
                    break
                # duplicate values
                if node.data == cur_node.data:
                    raise Exception("duplicate values...")
                    break
                #move on to next tree nodule
                if node.data < cur_node.data and cur_node.left != None:
                    cur_node = cur_node.left
                if node.data > cur_node.data and cur_node.right != None:
                    cur_node = cur_node.right
        else:
            self.head = node

    def remove(self, val):
        node = self.findval(self.head, val, ret='n')
        if node is None:
            return None
        else:
            if node.data == self.head.data:
                placeholder = self.head.left
                self.head = self.head.right
                tree.insert(placeholder, mode='n')
            elif node.data < self.head.data:
                cur_node = self.head
                while True:
                    if cur_node.left == node:
                        if cur_node.left.right == None and cur_node.left.left: # just left child
                            placeholder = cur_node.left.left
                            tree.insert(placeholder, mode='n')
                        elif cur_node.left.left == None and cur_node.left.right: #just right child
                            placeholder = cur_node.left.right
                            tree.insert(placeholder, mode='n')
                        elif cur_node.left.left and cur_node.left.right: # both child
                            placeholder = cur_node.left.left
                            cur_node.left = cur_node.left.right
                            tree.insert(placeholder, mode='n')
                        else: #no child
                            cur_node.left = None
                        break
                    elif cur_node.right == node:
                        if cur_node.right.right == None and cur_node.right.left: # just left child
                            placeholder = cur_node.right.left
                            tree.insert(placeholder, mode='n')
                        elif cur_node.right.left == None and cur_node.right.right: #just right child
                            placeholder = cur_node.right.right
                            tree.insert(placeholder, mode='n')
                        elif cur_node.right.left and cur_node.right.right: # both child
                            placeholder = cur_node.right.left
                            cur_node.right = cur_node.right.right
                            tree.insert(placeholder, mode='n')
                        else: #no child
                            cur_node.right = None
                        break
                    else:
                        if node.data < cur_node.data:
                            cur_node = cur_node.left
                        elif node.data > cur_node.data:
                            cur_node = cur_node.right
                    break

    def get_nodes(self, start, nodes=[], mode='n'):
        if start:
            nodes = self.get_nodes(start.right, nodes, mode)
            if mode == 'n':
                nodes.append(start)
            else:
                nodes.append(start.data)
            nodes = self.get_nodes(start.left, nodes, mode)
        return nodes

    def findval(self, start, val, ret='d'):
        # ends if it is found (rather than running through everything)
        if start:
            if val == start.data:
                if ret == 'd':
                    return True
                elif ret == 'n':
                    return start
            elif val < start.data and start.left:
                found = self.findval(start.left, val, ret)
            elif val > start.data and start.right:
                found = self.findval(start.right, val, ret)
            else:
                if ret == 'd':
                    return False
                else:
                    return None
            return found
        else:
            if ret == 'd':
                return False
            else:
                return None

    def print_tree(self, start, lvl=0, lvls={}):
        if start:
            lvls = self.print_tree(start.right, lvl+1, lvls)
            print('')
            print("{}{}".format("\t"*lvl, start.data))
            if (lvl+1) in lvls.keys():
                lvls[lvl+1].append(start.data)
            else:
                lvls[lvl+1] = [start.data]
            lvls = self.print_tree(start.left, lvl+1, lvls)
        return lvls

tree = Tree()
# for num in [random.randint(1, 100) for item in range(10)]:
for num in [15, 17, 3, 8, 10, 2, 4, 16, 18]:
    tree.insert(num)

children = {} #keeping track of children is kinda useless at the moment
nodes = tree.get_nodes(tree.head, mode='n')
for node in nodes:
    children[node.data] = [[],[]] #[left, right]
    children[node.data] = node.get_children(node, children[node.data])


tree.print_tree(tree.head)
print("--------------------------")
tree.remove(3)
print("--------------------------")
tree.print_tree(tree.head)


#-------POTENTIAL TREE DESIGNS-------------------------------------

#       #1: vertical (i like this one better... but am not sure how to do it)
#                     8
#            .--------^--------.
#            |                 |
#            5                 10
#       .----^--.            .--^----.
#       |       |            |       |
#       3       7            9       11
#       '--.                          '--.
#          |                             |
#          4                             12

#       #2: horizontal (less visually appealing but might be easier than #1)
#            12
#           /
#         11
#        /
#      10
#     /  \
#    /    09
#   /
# 08
#   \
#    \    07
#     \  /
#      05
#       \
#        \    04
#         \  /
#          03