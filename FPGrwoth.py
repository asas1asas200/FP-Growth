from collections import Counter


class FPBase:
	class Node:
		def __init__(self, value=0, parent=None, name=None):
			self.childs = []
			self.parent = parent
			self.value = value
			self.name = name

	class TableItem:
		def __init__(self, cnt):
			self.cnt = cnt
			self.nodes = []

	def __init__(self, filename, frequency):
		self.frequency = frequency
		self.data = self.__init_data(filename)
		self.table = self.__create_header_table()
		self.data = self.__sort_filter_data()
		self.__create_FP_tree()
		
	def __init_data(self, filename):
		with open(filename, 'r') as file:
			data = [i.split() for i in file]					# for string data type
#			data = [list(map(int, i.split())) for i in file]	# for only numeric data type
		return data


	def __create_header_table(self):
		def calc_counts():
			cnt = Counter()
			for i in self.data:
				cnt += Counter(i)
			return cnt.most_common()

		total_counts = calc_counts()
		return {name: self.TableItem(cnt) for name, cnt in total_counts if cnt >= self.frequency}

	def __sort_filter_data(self):
		ret = []
		for i in self.data:
			ret.append(sorted(filter(lambda x: x in self.table, sorted(i)), key=lambda y: self.table[y].cnt, reverse=True))
		return ret

	def __create_FP_tree(self):
		def find_node(childs, target):
			for i in childs:
				if i.name == target:
					return i
			return None

		def travel(items):
			now_node = self.root
			for i in items:
				next_node = find_node(now_node.childs, i)
				if next_node is None:
					next_node = self.Node(parent=now_node, name=i)
					self.table[i].nodes.append(next_node)
					now_node.childs.append(next_node)
				next_node.value += 1
				now_node = next_node
		self.root = self.Node()
		for items in self.data:
			travel(items)


class FP(FPBase):
	def __init__(self, filename, frequency):
		super().__init__(filename, frequency)

if __name__ == '__main__':
	FP('mushroom.dat', 824)
