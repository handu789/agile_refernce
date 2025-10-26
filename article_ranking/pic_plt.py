'''
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib import cm, colors as mcolors  # colormap

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# 数据定义
categories = ['准确率', '精确率', '召回率']
methods = [
    '直接根据素材文本内容分类',
    '直接根据素材文本标题分类',
    '对素材文本先进行改写后分类',
    '基于关键词的文本分类'
]
values = [
    [75.0, 75.0, 72.9],
    [77.8, 75.0, 81.4],
    [76.4, 70.9, 87.1],
    [86.1, 84.7, 87.1]
]

# 使用 Pastel1 调色板，并替换第一个颜色为蜜瓜色
original_colors = list(cm.get_cmap('Pastel1').colors)  # 可换成 'Pastel1', 'tab10', 'Dark2' 等
colors = ['#FFE4B5'] + [mcolors.to_hex(c) for c in original_colors[1:4]]
hatches = ['//', 'o', 'xx', '.']  # 可选：'-', '+', '*', 'o', 'O', '.', '//'

# 设置横坐标基准，每类指标间间距大
x_base = np.array([0, 4, 8])
num_methods = len(methods)
bar_width = 0.8
total_group_width = bar_width * num_methods * 1.1  # 额外乘以 1.1 是为了插入组间距

# 创建图形和GridSpec布局（2行1列，上图图例，下图柱状图）
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.2, 0.8], hspace=0.1)

# 图例轴（上方）
legend_ax = fig.add_subplot(gs[0])
legend_ax.axis("off")  # 不显示任何坐标轴

# 主图轴（柱状图）
ax = fig.add_subplot(gs[1])

# 画柱状图
for i, method in enumerate(methods):
    offsets = x_base - total_group_width / 2 + i * bar_width * 1.1
    bars = ax.bar(offsets, values[i], width=bar_width, label=method, color=colors[i], hatch=hatches[i])
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.8,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=14)

# 设置坐标轴
ax.set_xticks(x_base)
ax.set_xticklabels(categories, fontsize=16)
ax.set_ylim(65, 90)
ax.set_ylabel('百分比（%）', fontsize=16)
ax.tick_params(axis='y', labelsize=14)
# ax.grid(axis='y', linestyle='--', alpha=0.4)

# 设置图例到 legend_ax 中
handles, labels = ax.get_legend_handles_labels()
legend_ax.legend(handles, labels, loc='center', ncol=2, fontsize=14, frameon=True)

# 保存图像（图例包含在内）
plt.savefig("分类方式_图例右侧版.png", dpi=300, bbox_inches='tight')

# 显示图像
plt.show()
'''

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm, colors as mcolors

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

labels = [
    '初始生成通过',
    '单次修正通过',
    '二次修正通过',
    '三次修正通过',
    '四次修正通过',
    '多轮修正未通过'
]
sizes = [21, 18, 0, 0, 0, 1]

# 过滤掉为 0 的项
labels_filtered = [l for l, s in zip(labels, sizes) if s > 0]
sizes_filtered = [s for s in sizes if s > 0]

# 设置颜色和纹理
original_colors = list(cm.get_cmap('Pastel1').colors)  # 可换成 'Pastel1', 'tab10', 'Dark2' 等
colors = ['#FFE4B5'] + [mcolors.to_hex(c) for c in original_colors[1:4]]
hatches = ['/', 'o', 'x']  # 纹理数量应与数据项相同

# GridSpec 布局：2 行 1 列
fig = plt.figure(figsize=(10, 6))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 3])

# 上面图例
ax_legend = fig.add_subplot(gs[0])
ax_legend.axis('off')  # 不显示坐标轴
legend_patches = []
for i in range(len(labels_filtered)):
    patch = plt.Rectangle((0, 0), 1, 1, facecolor=colors[i], hatch=hatches[i % len(hatches)], edgecolor='black')
    legend_patches.append(patch)
ax_legend.legend(legend_patches, labels_filtered, loc='center', ncol=len(labels_filtered), fontsize=16)

# 下面饼图
ax_pie = fig.add_subplot(gs[1])
explode = [0.01] * len(sizes_filtered)
wedges, texts, autotexts = ax_pie.pie(
    sizes_filtered,
    labels=None,
    autopct='%1.1f%%',
    startangle=140,
    counterclock=False,
    textprops={'fontsize': 18},
    colors=colors,
    explode=explode
)

# 添加纹理（通过 wedge.set_hatch）
for i, wedge in enumerate(wedges):
    wedge.set_hatch(hatches[i % len(hatches)])
    wedge.set_edgecolor('black')

plt.setp(autotexts, size=24, weight="bold", color="black")

ax_pie.axis('equal')
plt.tight_layout()
plt.savefig("审核通过情况饼图.png", dpi=300, bbox_inches='tight', pad_inches=0.05)
plt.show()
