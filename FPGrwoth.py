from collections import Counter


class FPGrowth:
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

	def __init__(self, freq, filename=None, data_lists=None):
		self.freq = freq
		self.data = data_lists if filename is None else self.__read_data(filename)
		self.table = self.__create_header_table()
		self.data = self.__sort_filter_data()
		self.__create_FP_tree()

	def __read_data(self, filename):
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

		def merge_counts():
			cnt = {}
			for sets, val in self.data.items():
				for i in sets:
					if i not in cnt:
						cnt[i] = 0
					cnt[i] += val
			return list(cnt.items())
	
		if isinstance(self.data, list):
			total_counts = calc_counts()
		else:
			total_counts = merge_counts()
		return {name: self.TableItem(cnt) for name, cnt in total_counts if cnt >= self.freq}

	def __sort_filter_data(self):
		if isinstance(self.data, list):
			ret = [] 
			for i in self.data:
				ret.append(sorted(filter(lambda x: x in self.table, sorted(i)), key=lambda y: self.table[y].cnt, reverse=True))
			return ret
		else:
			ret = {}
			for i in self.data.items():
				addon = frozenset({j for j in i[0] if j in self.table})
				if addon in ret:
					ret[addon] += i[1]
				else:
					ret[addon] = i[1]
			return ret

	def __create_FP_tree(self):
		def travel(items, val=1):
			now_node = self.root
			for i in items:
				next_node = None if i not in now_node.childs else now_node.childs[i]
				if next_node is None:
					next_node = self.Node(parent=now_node, name=i)
					self.table[i].nodes.append(next_node)
					now_node.childs[i] = next_node
				next_node.value += val
				now_node = next_node
			

		self.root = self.Node()
		if isinstance(self.data, list):
			for items in self.data:
				travel(items)
		else:
			for items in self.data.items():
				travel(items[0], items[1])

	def is_single_path(self):
		now = self.root
		while len(now.childs):
			if len(now.childs) > 1:
				return False
			else:
				now = list(now.childs.values())[0]
		return True

	def print_tree(self, node, dep=0):
		if isinstance(node.name, str): print('\t'*dep + node.name + ':' + str(node.value))
		for i in node.childs.values():
			self.print_tree(i, dep+1)
		

	def mine_tree(self, prefix_paths, freq_sets):
		def find_root(node, path):
			if node != self.root:
				path.append(node.name)
				find_root(node.parent, path)

		def find_prefix_paths(name):
			paths = {}
			for i in self.table[name].nodes:
				path = []
				find_root(i, path)
				if len(path) > 1:
					paths[frozenset(path[1:])] = i.value
			return paths

		for i in self.table:
			new_freq_sets = prefix_paths.copy()
			new_freq_sets.add(i)
			freq_sets.append(new_freq_sets)
			data_lists = find_prefix_paths(i)
			cond_tree = FPGrowth(self.freq, data_lists=data_lists)
			if len(cond_tree.table):
				cond_tree.mine_tree(new_freq_sets, freq_sets)

if __name__ == '__main__':
	FP = FPGrowth(3, 'exam2.txt')
	freq_items = []
	FP.mine_tree(set([]), freq_items)
	FP.print_tree(FP.root)
	print(freq_items)
	
