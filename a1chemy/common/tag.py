import enum


class Tag(object):
    id = ''
    parent=''
    values = {}

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def to_dict(self):
        return {
            'id': self.id,
            'parent': self.parent,
            'values': self.values
        }

class TreeNode(Tag):
    children={}
    def __init__(self, root: Tag) -> None:
        self.id = root.id
        self.parent = root.parent
        self.values = root.values

    def add_child(self, child):
        self.children[child.id] = child

    def get_child(self, id=None):
        return self.children['id']
    

class Tree(TreeNode):
    index_map = {}
    root = None
    def __init__(self, root: Tag) -> None:
        root_tree_node = TreeNode(root=root)
        self.root = root_tree_node
        self.index_map[root.id] = root_tree_node

    def add_relation(self, parent, children: list[Tag]=None):
        parent_tree_node = self.index_map.get(parent, None)
        if parent_tree_node is None:
            return False
        
        for c in children:
            child_tree_node = self.get_or_create_tree_node(tag=c)
            parent_tree_node.add_child(child=child_tree_node)
        return True
            
    def get_or_create_tree_node(self, tag: Tag):
        tree_node = self.index_map.get(tag.id, None)
        if tree_node is None:
            tree_node = TreeNode(root=tag)
        return tree_node