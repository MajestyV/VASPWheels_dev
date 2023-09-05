import matplotlib.pyplot as plt

# 此函数专用于绘制多子图组图的画布
def Multiplot(num_subplot,grid,subplot_location,subplot_shape,figsize=(6.4,4.8)):
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    fig = plt.figure(figsize=figsize)  # 创建图像对象用于存放多子图


    for i in range(num_subplot):
        location = subplot_location[i]
        shape = subplot_shape[i]
        globals()['fig_'+str(i+1)] = plt.subplot2grid(grid,location,colspan=shape[0],rowspan=shape[1])  # 定义全局变量子图

    return

Multiplot(4,[(0,0),(0,1),(1,0),(1,2)],
             [(1,1),(2,1),(2,2),(1,2)],
             figsize=(5,5),
           grid_shape=(3,3),wspace=0.01,hspace=0.1)


# figsize = kwargs['figsize'] if 'figsize' in kwargs else (2.8, 4.2)  # 图像大小
#figsize = (16,4.2)



# 创建子图对象
#plot_bands = fig.add_subplot(grid[1:, :4])  # 分配能带子图空间
#plot_dos = fig.add_subplot(grid[1:, 4], xticks=[], yticklabels=[])  # 分配DOS子图空间并隐藏刻度

#P, Tao, Tab, Tob = [], [], [], []
#for i in ['0', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200', '220', '240', '260', '280', '300']:
#for i in ['0', '20', '40', '60', '80', '100', '120']:
    #for j in ['alpha', 'beta', 'omega']:
        #pdos = gd.GetPDOS('/Users/liusongwei/Titanium/data/data_test/'+j+'_dos/total_dos_'+j+'_'+i+'.dat')
        #w_list = []
        #p_list = []
        #for k in range(len(pdos[:,0])):
            #if pdos[k,0] > 0:
                #w_list.append(pdos[k,0])
                #p_list.append(pdos[k,1])
        #locals()['w_'+str(j)] = np.array(w_list)
        #locals()['p_'+str(j)] = np.array(p_list)
    #P.append(np.float(i)/10)
    #Tao.append(f.TransTemp(E_alpha,p_alpha,w_alpha,E_omega,p_omega,w_omega))
    #Tab.append(f.TransTemp(E_alpha,p_alpha,w_alpha,E_beta,p_beta,w_beta))
    #Tob.append(f.TransTemp(E_omega,p_omega,w_omega,E_beta,p_beta,w_beta))