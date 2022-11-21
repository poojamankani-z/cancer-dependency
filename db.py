import pandas as pd
import json

def read_file(file_name):
    dataframe = pd.read_csv(file_name)
    return dataframe

def get_cell_line(is_tcga, gene_id, cell_line_id, file_name):
    file_dataframe = read_file(file_name)
    if(cell_line_id is None):
        result_dataframe = file_dataframe[(file_dataframe['Entrez_Gene_Id'] == gene_id) & (file_dataframe['isTCGAhotspot'] == is_tcga)]
    else: 
        result_dataframe = file_dataframe[(file_dataframe['Entrez_Gene_Id'] == gene_id) & (file_dataframe['isTCGAhotspot'] == is_tcga) & (file_dataframe['DepMap_ID'] == cell_line_id)]
    result_json = result_dataframe.to_json(orient='records')
    return result_json

def get_gene(is_tcga, cell_line_id, file_name):
    file_dataframe = read_file(file_name)
    result_dataframe = file_dataframe[(file_dataframe['DepMap_ID'] == cell_line_id) & (file_dataframe['isTCGAhotspot'] == is_tcga)]
    result_json = result_dataframe.to_json(orient='records')
    return result_json
