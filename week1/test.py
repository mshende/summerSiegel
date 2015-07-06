import os
import subprocess
from sys import argv

# path to the molfile_to_params.py file
ROSETTA_PARAMS = "~/Rosetta/Rosetta/main/source/src/python/apps/public/molfile_to_params.py"

# path to pymol 
PYMOL_PATH = "/home/mshende/Downloads/pymol/pymol"

if __name__=="__main__":
    pdb_list = open(argv[1], 'r').readlines()
    for pdb_file_name in pdb_list:
        pdb_file_name = pdb_file_name.strip()
#        print "pdb file: *%s*" % (pdb_file_name)
        protein_file_name = pdb_file_name[0:4]+'_protein.pdb'
        ligand_file_name = pdb_file_name[0:4]+'_ligand.pdb'

        # pulls out the protein portion of the pdb
        grep_protein = 'grep ATOM %s > %s' % (pdb_file_name, protein_file_name)

        # pulls out the ligand portion of the pdb
        grep_ligand = 'grep HETATM %s > %s' % (pdb_file_name, ligand_file_name)
        ligand_name = open(pdb_file_name, 'r').readlines()[-1][17:20]
        print "ligand name = %s" % (ligand_name)

        # runs the script that converts a pdb to a molfile using PyMOL
        pdb_to_mol = PYMOL_PATH+' -qc pdb_to_mol.py -- %s' % (ligand_file_name)
        ligand_mol_file = pdb_file_name[0:4]+'_ligand.mol'

        # runs the molfile_to_params.py script
        mol_to_params = 'python '+ROSETTA_PARAMS+' -c -n %s %s' % (ligand_name, ligand_mol_file)

        params_file = '%s.fa.params' % (ligand_name)
        prep_ligand_file = '%s_0001.fa.pdb' % (ligand_name)
        prep_pdb_file = '%s_prepared.pdb' % (pdb_file_name[0:4])
        # cats the protein portion and the prepared ligand portion to make the final pdb for use with rosetta
        merge_pro_lig = 'cat %s %s > %s' % (protein_file_name, prep_ligand_file, prep_pdb_file)
        

    # in the flags file, don't put the params file there -- put it on
    # the command line 
    #run 'command'
    dock_command = '~/Rosetta/Rosetta/main/source/bin/rosetta_scripts.default.linuxgccrelease @pro_lig_dock_flags -in:file:s %s -in:file:extra_res_fa %s -database ~/Rosetta/Rosetta/main/database/ -show_simulation_in_pymol 3 -keep_pymol_simulation_history T' % (prep_pdb_file, params_file)
    command5 = 'source pro_lig_dock_command'
    os.system(grep_protein)
    os.system(grep_ligand)
    os.system(pdb_to_mol)
    os.system(mol_to_params)
    os.system(merge_pro_lig)
