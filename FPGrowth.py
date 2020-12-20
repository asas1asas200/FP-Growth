from collections import Counter
from itertools import combinations
from time import time

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
			data = {tuple(i.split()):1 for i in file}			# for string data type
#			data = {tuple(map(int, i.split())):1 for i in file}	# for only numeric data type
		return data


	def __create_header_table(self):
		total = {}
		for sets, val in self.data.items():
			for i in sets:
				if i not in total:
					total[i] = 0
				total[i] += val
		return {name: self.TableItem(total[name]) for name in total if total[name] >= self.freq}

	def __sort_filter_data(self):
		ret = {}
		for i in self.data.items():
			addon = tuple(sorted(filter(lambda x: x in self.table, sorted(i[0])), key=lambda y: self.table[y].cnt, reverse=True))
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
		for items in self.data.items():
			travel(items[0], items[1])

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
					paths[tuple(path[1:])] = i.value
			return paths

		for i in self.table:
			new_freq_sets = prefix_paths.copy()
			new_freq_sets.add(i)
			now = frozenset(new_freq_sets)
			if now not in freq_sets:
				freq_sets[now] = self.table[i].cnt
			else:
				freq_sets[now] += self.table[i].cnt
			data_lists = find_prefix_paths(i)
			cond_tree = FPGrowth(self.freq, data_lists=data_lists)
			if len(cond_tree.table):
				cond_tree.mine_tree(new_freq_sets, freq_sets)

def find_rules(max_len_sets, conf):
	rules = set()
	for freq in max_len_sets:
		for n in range(2, 6):
			for r in range(1, n):
				l = abs(n-r)
				for i in combinations(freq, l):
					a = frozenset(i)
					remain = freq - a
					for j in combinations(remain, r):
						b = frozenset(j)
						if freq_items[a|b] / freq_items[a] >= conf:
							rules.add((a, b))
	return rules

def filter_sets(sets):
	max_len_sets = []
	for i in sets:
		flag = True
		for j in max_len_sets:
			if i.issubset(j):
				flag = False
				break
		if flag:
			max_len_sets.append(i)
	return max_len_sets

if __name__ == '__main__':
	start = time()
	FP = FPGrowth(813, 'mushroom.dat')
	freq_items = {}
	FP.mine_tree(set([]), freq_items)
#	FP.print_tree(FP.root)
	cnt = Counter(len(i) for i in freq_items)
	max_len_sets = filter_sets(sorted(freq_items.keys(), key=lambda x: len(x), reverse=True))
	rules = find_rules(max_len_sets, 0.8)
	print('Spent time: ' + str(time() - start))
	for i in range(1, 6):
		print(cnt[i])
	print(len(rules))
