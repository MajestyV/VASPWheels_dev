# Electron Microscopy

## I. Introduction



## X. Elemental analysis

### A. Energy-dispersive X-ray spectroscopy (EDS, EDX, EDXS or XEDS)

EDX通过不同原子对X射线的能量色散来判断测试点（区域）的元素组成及分布，而我们从 EDX测试中获取的数据实际上是传感器读取不同能量的X射线的信号强度（Intensity，$I(E)$，$E$是散射的X射线能量）。因此，点扫描的EDX数据可以看作是一个二阶张量$\mathbf{I}_{point} \in \mathbb{R}^{2 \times N}$ （$N$是EDX测试采样的总点数）。两个指定点（起点和终点）之间的等距采样可以实现线扫描（line profile），其数据为一个三阶张量$\mathbf{I}_{line} \in \mathbb{R}^{W \times 2 \times N}$ （$W$是线扫描长度）。以此类推，面扫描（area mapping）的数据满足$\mathbf{I}_{area} \in \mathbb{R}^{L \times W \times 2 \times N}$ （$L$是扫描区域的宽度）。统一地，我们可以用一个四阶张量来描述EDX测试数据：
$$
\mathbf{I} \in \mathbb{R}^{L \times W \times 2 \times N} \Longrightarrow
\begin{cases}
\mathbf{I}_{point} &\in \mathbb{R}^{1 \times 1 \times 2 \times N} \\
\mathbf{I}_{line} &\in \mathbb{R}^{1 \times W \times 2 \times N} \\
\mathbf{I}_{area} &\in \mathbb{R}^{L \times W \times 2 \times N}
\end{cases}
\quad .
\tag{X.1}
$$
通常，为了更加直观地让研究者或者研究的读者理解，我们通常会将信号强度换算成原子分数（atomic percentage，$A$）。假设我们要研究某个坐标点$\vec{R}$处的一系列原子$\{ a_1,a_2, \dots, a_n \}$的分布，此处对应的EDX信号强度为$\{ I_1,I_2, \dots, I_n \}$，那么对于原子$a_i$，我们有
$$
A_i = \frac{I_i}{\sum^n_j I_j} \times 100\%
\quad .
\tag{X.2}
$$
[原子比例转质量比例](https://engineering.stackexchange.com/questions/53121/how-do-you-derive-the-formula-for-converting-weight-percent-to-atom-percent)

