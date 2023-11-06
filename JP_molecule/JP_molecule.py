import moltemplate as mt

if __name__=='__main__':
    data_directory = '/Users/liusongwei/PhD_Research/CNT_molecule_LAMMPS/archive'

    file_mol2 = open(data_directory+'/interact.mol2','r')
    file_lt = open(data_directory+'/interact.lt','w')

    mt.ConvertMol22Lt(file_mol2,file_lt,
                      # ff_name = 'Customed',
                      ff_filename=data_directory+'/force_field.lt',
                      object_name='interact')