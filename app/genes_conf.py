
# Configuracion de caracteristica de genes
genes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']
gene_bits = 4
encoding = {f"{i:04b}": ch for i, ch in enumerate(genes)}
decoding = {ch: f"{i:04b}" for i, ch in enumerate(genes)}
