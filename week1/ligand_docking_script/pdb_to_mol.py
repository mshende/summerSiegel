from pymol import cmd
import sys

def pdb_to_mol(pdb_file):
    cmd.load(pdb_file)
    cmd.h_add()
    cmd.save("%s_ligand.mol" % (pdb_file[0:4]))

#cmd.extend("pdb_to_mol", pdb_to_mol)

pdb_lig_file = sys.argv[1]
pdb_to_mol(pdb_lig_file)
cmd.quit()
