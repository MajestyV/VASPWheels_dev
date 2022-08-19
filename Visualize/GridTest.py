import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12,5.5))  # 控制图像大小
grid = plt.GridSpec(2,8)  # 创建柔性网格用于空间分配

main_fig = fig.add_subplot(grid[:,:4])  # 分配主图
sub_fig_1 = fig.add_subplot(grid[:,4])  # 分配子图
sub_fig_2 = fig.add_subplot(grid[:,5])
sub_fig_3 = fig.add_subplot(grid[:,6])
sub_fig_4 = fig.add_subplot(grid[:,7])

# 通过循环批量调节子图参数
sub_fig_list = [sub_fig_1,sub_fig_2,sub_fig_3]
for n in sub_fig_list:
    n.set_yticklabels([])
    #n.set_yticks([])
    n.set_xlim(0,100)
    n.set_xticks([0,100])
    n.set_xticklabels(['K','$\Gamma$'])

sub_fig_4.set_yticklabels([])
sub_fig_4.set_xlim(0,100)
sub_fig_4.set_xticks([50])
#Text properties for the labels. These take effect only if you pass labels. In other cases, please use tick_params.
sub_fig_4.tick_params(color='w')  # 对于subplot，要调整刻度样式的话，需要采用tick_params函数
sub_fig_4.set_xticklabels(['DOS (a.u.)'])

plt.show()