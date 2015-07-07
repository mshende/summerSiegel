import os
import subprocess
from sys import argv

# path to the molfile_to_params.py file
ROSETTA_PARAMS = "~/Rosetta/Rosetta/main/source/src/python/apps/public/molfile_to_params.py"

# path to pymol 
PYMOL_PATH = "/home/mshende/Downloads/pymol/pymol"

LIGAND_NAME_START = 17
LIGAND_NAME_END = 20
CHAIN_ID = 21

# opens the given file (contains only HETATM lines), and counts the
# number of chains that are present for the ligand
def get_num_ligand_chains(fname):
    f = open(fname, 'r')
    lines = f.readlines()
    num_chains = 1
    prev = lines[0]
    for line in lines[1:]:
        if (prev[CHAIN_ID] != line[CHAIN_ID]):
            num_chains+=1
        prev = line
    return num_chains

# appends the name of each params file to a string, which will be used
# in the flag when running docking
def get_params_file_string(chains, ligand_name):
    params_file_string = ""
    for index in range (chains):
        params_file_string += '%s%i.fa.params' %(ligand_name, index+1)
        if index != chains-1:
            params_file_string += ' '
    return params_file_string

if __name__=="__main__":
    pdb_list = open(argv[1], 'r').readlines()
    for pdb_file_name in pdb_list:
        pdb_file_name = pdb_file_name.strip()
#        print "pdb file: *%s*" % (pdb_file_name)
        protein_file_name = pdb_file_name[0:4]+'_protein.pdb'
        ligand_file_name = pdb_file_name[0:4]+'_ligand.pdb'

        # pulls out the protein portion of the pdb
        grep_protein = 'grep ATOM %s > %s' % (pdb_file_name, protein_file_name)
        os.system(grep_protein)
        
        # pulls out the ligand portion of the pdb
        grep_ligand = 'grep HETATM %s > %s' % (pdb_file_name, ligand_file_name)
        os.system(grep_ligand)

        num_chains = get_num_ligand_chains(ligand_file_name)
        ligand_name = open(pdb_file_name, 'r').readlines()[-1][LIGAND_NAME_START:LIGAND_NAME_END]
        print "ligand name = %s" % (ligand_name)

        # runs the script that converts a pdb to a molfile using PyMOL
        pdb_to_mol = PYMOL_PATH+' -qc pdb_to_mol.py -- %s' % (ligand_file_name)
        os.system(pdb_to_mol)

        ligand_mol_file = pdb_file_name[0:4]+'_ligand.mol'

        # runs the molfile_to_params.py script
        mol_to_params = 'python '+ROSETTA_PARAMS+' -c -n %s %s' % (ligand_name, ligand_mol_file)
        os.system(mol_to_params)

        params_file = get_params_file_string (num_chains, ligand_name)
        print "params file string = *%s*" % (params_file)
#        params_file = '%s.fa.params' % (ligand_name)
        prep_ligand_file = '%s_0001.fa.pdb' % (ligand_name) # this is the ligand file output from 
                                                            # molfile_to_params that is prepared for use with rosetta. 
        prep_pdb_file = '%s_prepared.pdb' % (pdb_file_name[0:4])
        # cats the protein portion and the prepared ligand portion to make the final pdb for use with rosetta
        merge_pro_lig = 'cat %s %s > %s' % (protein_file_name, prep_ligand_file, prep_pdb_file)
        os.system(merge_pro_lig)
        print "merged_pro_lig filename = %s" % (prep_pdb_file)

    # in the flags file, don't put the params file there -- put it on
    # the command line 
    #run 'dock_command'

    #NOTE: how do I determine how many params files were produced and use all of them in the flag?
    dock_command = '~/Rosetta/Rosetta/main/source/bin/rosetta_scripts.default.linuxgccrelease @pro_lig_dock_flags -in:file:s %s -in:file:extra_res_fa %s -database ~/Rosetta/Rosetta/main/database/ -show_simulation_in_pymol 3 -keep_pymol_simulation_history T' % (prep_pdb_file, params_file)





