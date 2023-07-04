

    # 此函数通过费米能级的位置区分导带跟价带（如果出现分数电子占据的情况，得到的结果可能不太准确）
    def GetBandEdges_Fermi(self, EIGENVAL, Efermi=0):
        data_dict = self.GetEbands(EIGENVAL)  # 利用GetEbands函数从EIGENVAL文件提取能带数据
        num_bands = data_dict['num_bands']  # 提取能带总数
        num_kpoints = data_dict['num_kpoints']  # 提取K点总数
        bands = data_dict['bands']  # 能带具体的能量值

        unoccupied = []  # 这个列表用于存放所有未被占据的能带数据
        occupied = []  # 这个列表用于存放所有已被占据的能带数据
        for n in range(num_kpoints):
            energy_unoccupied = []
            energy_occupied = []
            for m in range(num_bands):
                energy = bands[m,n]
                if energy >= Efermi:  # 通过能量E是否大于给定的费米能级判断能带在费米面之下还是费米面之上
                    energy_unoccupied.append(energy)
                else:
                    energy_occupied.append(energy)
            unoccupied.append(energy_unoccupied)
            occupied.append(energy_occupied)

        conduction_band = [min(unoccupied[i]) for i in range(len(unoccupied))]  # 最低未占据能带（导带），Lowest unoccupied band
        valence_band = [max(occupied[i]) for i in range(len(occupied))]  # 最高已占据能带（价带），Highest occupied band

        return valence_band, conduction_band

