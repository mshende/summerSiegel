from pymol import cmd
import sys

def pdb_to_mol(pdb_file):
    cmd.load(pdb_file)
    cmd.h_add()
    cmd.save("1gsu_ligand.mol")

#cmd.extend("pdb_to_mol", pdb_to_mol)

pdb_lig_file = sys.argv[1]
pdb_to_mol(pdb_lig_file)
cmd.quit()
