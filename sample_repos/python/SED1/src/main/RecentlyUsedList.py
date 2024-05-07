class RecentlyUsedList:
    def __init__(self):
        self.recently_used_list = []

    def size(self):
        return len(self.recently_used_list)

    def add(self, item):
        if self.size() == 0:
            self.recently_used_list.append(item)
        elif isinstance(item, type(self.recently_used_list[-1])):
            self.recently_used_list.remove(item)
            self.recently_used_list.append(item)
        else:
            raise ValueError("Input type mismatch")

    def contains(self, item):
        return item in self.recently_used_list

    def get_item_at(self, index):
        if index < 0 or index >= self.size():
            raise IndexError("Index out of range")
        return self.recently_used_list[index]

    def get_most_recent(self):
        if self.size() == 0:
            return None
        return self.recently_used_list[-1]
