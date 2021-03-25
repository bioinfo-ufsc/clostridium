#!/usr/bin/python3

### Parser to count and extract paralogous and orthologous groups from OrthoMCL 
 
# input_file is result from OrthoMCL
input_file = open("Cdiff_groups.txt", "r").read().splitlines()
 
# Create output files, where paralogous proteins of each organism will be stored
icc45 = open("Cdifficile_ICC45_paralogous.txt", "a")
nap027 = open("Cdifficile_NAP027_paralogous.txt", "a")
count_strain_1 = []
count_strain_2 = []

# Each group is a line, here we will verify, group per group (line by line)
# which organism is present 
for line in input_file:
    # strain_1 is the identifier of ICC45 proteins
    # strain_2 is the identifier of NAP027 proteins 
    if not "strain_2" in str(line):
        # If strain_2 is not in present line, then only strain_1 is present
        # Only Proteins from ICC45 are in this group
        # Store this group in ICC45 paralogous file
        count_strain_1.append(str(line))
        icc45.write(str(line) + "\n")
    if not "strain_1" in str(line):
        # If strain_1 is not in present line, then only strain_2 is present
        # Only Proteins from NAP027 are in this group
        # Store this group in nap027 paralogous file
        count_strain_2.append(str(line))
        nap027.write(str(line) + "\n")

# Calculate orthologous proteins
nap1_proteins = " ".join(input_file).count("strain_2") - " ".join(count_strain_2).count("strain_2")
icc_proteins = " ".join(input_file).count("strain_1") - " ".join(count_strain_1).count("strain_1")
all_proteins_in_groups = nap1_proteins + icc_proteins
total_groups = len(input_file) - (len(count_strain_2) + len(count_strain_1))

print("NAP1/027 and ICC-45 orthologous groups: {}, {} total proteins".format(total_groups, all_proteins_in_groups))
print("                                        NAP1/027: {} proteins".format(nap1_proteins))
print("                                        ICC-45: {} proteins".format(icc_proteins))
print("Paralogous groups:")
print("NAP1/027: {}".format(str(len(count_strain_2))))
print("ICC-45: {}".format(str(len(count_strain_1))))
print("Paralogous Proteins:")
print("NAP1/027: {}".format(str(" ".join(count_strain_2).count("strain_2"))))
print("ICC-45: {}".format(str(" ".join(count_strain_1).count("strain_1"))))
print("---------------------")


# Close files
icc45.close()
nap027.close()

# all_proteins is the output from OrthoMCL, it means all proteins used in it's analysis
all_proteins = open("goodProteins.fasta", "r").read().splitlines()

# Extract only ids from fasta file
# All ids
ids_proteins = [prot.replace(">", "") for prot in all_proteins if prot.startswith(">")]
# Ids from icc
proteins_icc = [id_prot for id_prot in ids_proteins if "strain_1" in id_prot]
# Ids from nap
proteins_nap = [id_prot for id_prot in ids_proteins if "strain_2" in id_prot]

# Check number of proteins
print("Proteins from NAP1/027: {}".format(len(proteins_nap)))
print("Proteins from ICC-45: {}".format(len(proteins_icc)))

# Reopen Ouput from OrhtoMCL
input_file = open("Cdiff_groups.txt", "r").read()

# Open Output files
ids_icc_singletons = open("Cdifficile_ICC45_ids_singletons.txt", "a")
nap_icc_singletons = open("Cdifficile_NAP027_ids_singletons.txt", "a")
single_list = []

# Check wich proteins are not present in OrthoMCL output -> Singletons
# Check for icc
for id_prot in proteins_icc:
    if id_prot not in input_file:
        # Store output IDs
        single_list.append(str(id_prot))
        ids_icc_singletons.write(str(id_prot) + "\n")

print("Singletons ICC-45: {}".format(len(single_list)))

single_list = []

# Check wich proteins are not present in OrthoMCL output -> Singletons
# Check for nap
for id_prot in proteins_nap:
    if id_prot not in input_file:
        # Store output IDs
        single_list.append(str(id_prot))
        nap_icc_singletons.write(str(id_prot) + "\n")

print("Singletons NAP1/027: {}".format(len(single_list)))

nap_icc_singletons.close()
ids_icc_singletons.close()
