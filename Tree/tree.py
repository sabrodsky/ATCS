class Node:
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data

    def get_children(self, start, children):
        if start:
            self.get_children(start.right, children)
            if start.data > self.data:
                children[1].append(start.data)
            elif start.data < self.data:
                children[0].append(start.data)
            self.get_children(start.left, children)
        return children

class Tree:
    def __init__(self):
        self.head = None

    def insert(self, data):
        if self.head:
            cur_node = self.head
            settled = False
            while settled == False:
                if cur_node.left == None and data < cur_node.data:
                    cur_node.left = Node(data)
                    break
                if cur_node.right == None and data > cur_node.data:
                    cur_node.right = Node(data)
                    break
                if data == cur_node.data:
                    print("Error: duplicate values...")
                    break
                if data < cur_node.data and cur_node.left != None:
                    cur_node = cur_node.left
                if data > cur_node.data and cur_node.right != None:
                    cur_node = cur_node.right
        else:
            self.head = Node(data)

    def get_nodes(self, start, nodes=[], mode='n'):
        if start:
            nodes = self.get_nodes(start.right, nodes, mode)
            if mode == 'n':
                nodes.append(start)
            else:
                nodes.append(start.data)
            nodes = self.get_nodes(start.left, nodes, mode)
        return nodes

    def findval(self, val):
        #since this keeps track of actual object... you could also get the left/right values too
        nodes = self.get_nodes(self.head, mode='d')
        if val in nodes:
            return True
        else:
            return False

    def print_tree(self, start, lvl=0, lvls={}):
        if start:
            lvls = self.print_tree(start.right, lvl+1, lvls)
            print("{}{}".format("\t"*lvl, start.data))
            if (lvl+1) in lvls.keys():
                lvls[lvl+1].append(start.data)
            else:
                lvls[lvl+1] = [start.data]
            lvls = self.print_tree(start.left, lvl+1, lvls)
        return lvls

tree = Tree()
for num in [8, 10, 11, 12, 5, 7, 9, 3, 4]:
    tree.insert(num)

children = {} #keeping track of children is kinda useless at the moment
nodes = tree.get_nodes(tree.head)
for node in nodes:
    children[node.data] = [[],[]] #[left, right]
    children[node.data] = node.get_children(node, children[node.data])

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