class ConsoleGenerator:

    def print_tree(self, indent=0, depth=99):
        if depth > 0:
            print("    " * indent, str(self))
            self.descend_tree(indent, depth)

    def descend_tree(self, indent=0, depth=99):
        # do descent here, other classes may overload this
        pass

    @staticmethod
    def output(py_obj):
        print("#" * 80)
        print("data via console class: '{}'".format(py_obj.data))
        print("#" * 80)
