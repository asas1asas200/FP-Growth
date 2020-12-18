from collections import Counter


class FPBase:
	class Node:
		def __init__(self, value=0, parent=None, name=None):
			self.childs = {}
			self.parent = parent
			self.value = value
			self.name = name

	class TableItem:
		def __init__(self, cnt):
			self.cnt = cnt
			self.nodes = []

	def __init__(self, filename=None, frequency=0, paths=None):
		self.frequency = frequency
		if self.filename != None:
			self.data = self.__init_data(filename)
			self.table = self.__create_header_table()
			self.data = self.__sort_filter_data()
			self.__create_FP_tree()
		else:
			

		
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
		def travel(items):
			now_node = self.root
			for i in items:
				next_node = None if i not in now_node.childs else now_node.childs[i]
				if next_node is None:
					next_node = self.Node(parent=now_node, name=i)
					self.table[i].nodes.append(next_node)
					now_node.childs[i] = next_node
				next_node.value += 1
				now_node = next_node

		self.root = self.Node()
		for items in self.data:
			travel(items)

	@staticmethod
	def print_tree(node, dep):
		print('|' + '-' * dep + node.name if node.name is not None else '')
		for i in node.childs.values():
			FPBase.print_tree(i, dep+1)
	
	def __mining(self, table, path, freq_items):
		def find_root(node, path):
			if node.parent != self.root:
				path.append(node.parent.name)
				find_root(node, path)

		def find_prefix(item, table):
			table_item = table[item]
			paths = {}
			for node in table_item.nodes:
				path = []
				find_root(node, path)
				if len(path) > 1:
					paths[frozenset(path[1:])] = node.cnt
			return paths
			
		lists = table.keys()
		for item in lists:
			newFreq = path.copy()
			newFreq.add(item)
			prefix_paths = find_prefix(item)
			freq_items.append(prefix_paths)
			sub_tree = FPBase(frequency = self.frequency, paths = prefix_paths)
			if sub_tree.table != None:
				self.__mining(sub_tree.table, prefix_paths, freq_items)

if __name__ == '__main__':
	x = FPBase('exam.txt',3)
	x.print_tree(x.root, 0)
	#FP('mushroom.dat', 813)
