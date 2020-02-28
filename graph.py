#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

fileName = "results.csv" # result file
graphFileName = "graph.png"

legend = ["avg","min","max"]
colour = ["red", "green","blue"]

with open(fileName) as f:
	lines = f.readlines()
	
	labels = []
	mean = []
	min = []
	max = []
	
	for line in lines:
		tmp = line.replace("\n","").split("\t")
		labels.append(tmp[1])
		mean.append(float(tmp[2]))
		min.append(float(tmp[3]))
		max.append(float(tmp[4]))

plt.subplots(figsize = (8,6))
plt.scatter(labels, mean, label = "avg")
plt.scatter(labels, min, label = "min")
plt.scatter(labels, max, label = "max")
plt.legend(loc = 2)
plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.3)
plt.xticks(rotation = 90)
plt.savefig(graphFileName)