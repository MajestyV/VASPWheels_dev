# Light-electron interaction of $\mathrm{MoS_2}$ in presence of external electric field

## I. Introduction

## 杂记
Mo原子（$\mathrm{Mo}: 1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^{10} 4p^6 5s^1 4d^5$）的原子序数为42，S原子（$\mathrm{S}: 1s^2 2s^2 2p^6 3s^2 3p^4$）为16。因此，一个$\mathrm{MoS_2}$分子（或者说一个化学计量数）应该具有$42+2 \times 16=74$个电子。正常情况下，仅对块体（bulk）的$\mathrm{MoS_2}$而言，一个原胞中有两个$\mathrm{MoS_2}$分子，故原胞中的电子数为$74 \times 2=148$。考虑泡利不相容原理，两个电子占据一条能带，那么被占据的能带（即价带）数目应为74。这样，我们可以计算得出一层$\mathrm{MoS_2}$的被占据能带数应为$74 \div 2 = 37$。

然而在实际的密度泛函理论计算当中，我们通常会将一些不容易被激发的低轨道电子视半芯态来简化计算。在这种框架下，唯有外层、次外层以及一些能量较高的轨道的电子会被视作价电子，半芯态电子与原子核将会用一个有效原子核来近似。例如V.A.S.P.中，Mo_pv赝势将$\mathrm{Mo} (4p, 5s, 4d)$轨道电子视作价电子，S赝势将$\mathrm{S} (3s, 3p)$视作价电子。此时，若采用Mo_pv和S赝势计算$\mathrm{MoS_2}$性质的话，一层$\mathrm{MoS_2}$的能带数为$[(6+1+5)+(2+4) \times 2] \div 2 = 12$。若考虑到自旋-轨道耦合（Spin-orbit coupling, SOC）的话，能带会产生劈裂，正反自旋电子需占据单独的能带，则一层$\mathrm{MoS_2}$的能带数为24。依此类推，我们可以大致估算计算不同层数的$\mathrm{MoS_2}$所需设置的能带数目



结构优化：$1 \times 10^{-2} \mathrm{eV/{\AA}}$

SCF：$1 \times 10^{-6} \mathrm{eV}$



