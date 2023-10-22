import numpy as np
import pandas as pd
import VaspWheels as vw
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 此代码使用scipy自带的find_peaks()函数实现峰值检测
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
# 使用教程：https://blog.csdn.net/chehec2010/article/details/117336967

# 此函数可以利用pandas提取文件中的数据，适用于txt、dat、csv等格式的文件
# 数据文件中的数据形式应为两列式，如：第一列为自变量，第二列为因变量
def GetData(data_file, header=None, sep='\s+', **kwargs):
    # 利用pandas提取数据，得到的结果为DataFrame格式
    # header=None，默认没有列名，第一行作为数据读取；数据分隔符sep，默认为'\s+'（指代\f\n\t\r\v这些）
    data_DataFrame = pd.read_csv(data_file, header=header, sep=sep)  # 若设置header=0的话，则第一行为列名，从第二行开始读取
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组

    rearranging = kwargs['rearranging'] if 'rearranging' in kwargs else False  # 将数据数组重排为列表方便后续分析操作
    index_by = kwargs['index_by'] if 'index_by' in kwargs else 'row'           # 默认按行重排
    nrow, ncol = data_array.shape  # 获取数据数组的维数
    if rearranging:
        data = [data_array[:, i] for i in range(ncol)] if index_by == 'row' else [data_array[i, :] for i in range(nrow)]
    else:
        return data_array

    return data

# 限制范围
def Peak_range_refinement(peaks,search_range):
    peaks_ranged = []
    for i in range(len(peaks)):
        if peaks[i] >= search_range[0] and peaks[i] <= search_range[1]:
            peaks_ranged.append(peaks[i])
        else:
            pass
    return np.array(peaks_ranged)

# 峰数据修正
def Peak_correction(peaks,expected_num_peaks,expected_peaks_loc,tolerated_error):
    peaks_corrected = np.array(expected_peaks_loc)  # 一开始先预设好所有峰都在理想峰位，然后用检测到的真实峰数据替换理想预设
    num_peaks = len(peaks)
    for i in range(expected_num_peaks):
        # inf-infimum, sup-supremum
        inf, sup = (expected_peaks_loc[i]-tolerated_error,expected_peaks_loc[i]+tolerated_error)
        for j in range(num_peaks):
            if peaks[j] >= inf and peaks[j] <= sup:
                peaks_corrected[i] = peaks[j]  # 用真实数据替换理想预设
            else:
                pass
    return peaks_corrected  # 如果出现测试结果少于预测的情况，则利用预设峰位去读取对应的基线强度，尽量还原数据

if __name__=='__main__':
    x, y = (21,21)  # (行，列）
    excitation_wavelength = 529.4  # [=] nm
    baseline = 800  # 基线强度
    num_peaks = 2  # 峰值个数
    search_range = (700,725)

    # MMW502
    # data_file = 'D:/Projects/OptoTransition/Experiment/南科大/20231010_Raman均匀性/Uniformity.csv'
    # saving_directory = 'D:/Projects/OptoTransition/临时数据文件夹'
    # JCPGH1
    # data_file = 'D:/Projects/OptoTransition/Experiment/南科大/MoS2_Raman/Uniformity.csv'
    # saving_directory = 'D:/Projects/OptoTransition/临时数据文件夹'
    # Guangzhou
    # data_file = 'C:/Users/DELL/Desktop/临时数据文件夹/1.csv'
    # MacBook Pro 13'
    data_file = '/Users/liusongwei/OptoTransition/Experiment/南科大/Uniformity.csv'
    saving_directory = '/Users/liusongwei/OptoTransition/临时数据文件夹'

    data_DataFrame = pd.read_csv(data_file, header=None, sep=',')
    data_array = data_DataFrame.values

    data_length, num_data = data_array.shape  # 从数据的形状中获取出数据长度以及数据点个数

    wavelength = data_array[:, 0]  # 第一列数据为测试波长

    excitation_photon_energy = 1239.8/excitation_wavelength
    print(excitation_photon_energy)

    photon_energy = 1239.8/wavelength
    energy_shift = photon_energy-excitation_photon_energy
    wavenumber_shift = 8065.5*energy_shift
    # print(wavenumber_shift)

    data = np.empty((x,y,data_length))  # 创建空数据以存放数据
    for n in range(x):
        for m in range(y):
            data[n,m] = data_array[:,n*21+m+1]-baseline  # 实际上要历遍一个21*21的网格，可以认为是在进行21进制的读数（indexing）
            # 第一列数据为测试波长所以要加一

    # plt.plot(wavenumber_shift, data[18, 12])

    data_detection = np.zeros((x, y))
    data_peak_intensity = np.empty((x, y, num_peaks))
    data_peak_location = np.empty((x,y,num_peaks))
    for n in range(x):
        for m in range(y):
            # peaks, properties = find_peaks(data[n, m], prominence=(100, 2500), width=2, distance=15)
            peaks, properties = find_peaks(data[n, m], height=10, prominence=(10, 6000), distance=5)

            peaks_ranged = Peak_range_refinement(peaks,search_range)
            peaks_corrected = Peak_correction(peaks_ranged,2,(706,721),2)
            print(peaks_corrected)


            peak_intensity = np.array([data[n,m][peaks_corrected[i]] for i in range(num_peaks)])
            peak_location = np.array([wavenumber_shift[peaks_corrected[i]] for i in range(num_peaks)])

            data_peak_intensity[n,m] = peak_intensity
            data_peak_location[n,m] = peak_location

            data_detection[n,m] = 1  # 如果数据正常，则置1

    print(data_peak_location)
    # print(data_peak_intensity)

    #A = [[1,2],[4,5]]
    #B = [[A[i][j] for i in range(2)] for j in range(2)]
    # plt.imshow(B)

    # data_mapping = np.array([[data_peak_intensity[n,m,1] for n in range(x)] for m in range(y)])
    data_mapping = np.array([[data_peak_location[n,m,0]-data_peak_location[n,m,1]
                              for n in range(x)]
                             for m in range(y)])

    data_histogram = np.array([data_peak_intensity[n,m,1] for n in range(x) for m in range(y)])

    # 画图模块
    # 分布直方图
    ax = plt.subplot(111)

    # Histogram(ax,data_histogram,num_dropped=1,num_bins=200)

    # 热度图
    # print(np.min(data_mapping),np.max(data_mapping))
    heatmap = vw.Mapping.Heatmap(data_mapping,interpolation='gaussian',mapping_range=(22,30),
                                 customize_colorbar=False,cmap='coolwarm')
    # heatmap.ShowImage()
    heatmap.ShowColorbar()
    # heatmap.SavingFigure()

    Raman_mode = 'Phonon_energy_gap_colorbar'
    vw.SavingFigure(saving_directory=saving_directory, file_name=Raman_mode)
    vw.SavingFigure(saving_directory=saving_directory, file_name=Raman_mode, format='eps')

    plt.show(block=True)  # https://blog.csdn.net/qq_56039091/article/details/124024286