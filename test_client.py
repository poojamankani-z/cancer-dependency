
import requests
import json
import unittest
import app

BASE_URL = "http://127.0.0.1:5000"

class TestCancerApi(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    #the order of the test case execution depends on the name of the test case. basically they are executed in alphabetical order
    #You can disable the test case if needed using sortTestingMethodsUsing attribute the unittest framework

    def test_1_cell_lines(self):
        path = BASE_URL + "/cell_lines?gene=7157"
        #valid test. get cell line for gene
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        r = self.app.get(path, headers=headers)
        result_object = json.loads(r.get_data())
        gene_id = result_object[0]["Entrez_Gene_Id"]
        tcga = result_object[0]["isTCGAhotspot"]
        self.assertEqual(r.status_code, 200)
        self.assertEqual(True, tcga)
        self.assertEqual(7157, gene_id)

        #Bad request. Incorrect json provided
        path = BASE_URL + "/cell_lines"
        r = self.app.get(path, headers=headers)
        self.assertEqual(r.status_code, 400)

         #Method not supported
        r = self.app.post(path, headers=headers, data = ())
        self.assertEqual(r.status_code, 405)
        
    def test_2_genes(self):
        path = BASE_URL + "/genes?cell_line=ACH-000003"
        #valid test. get gene for cell_line
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        r = self.app.get(path, headers=headers)
        result_object = json.loads(r.get_data())
        cell_line_id = result_object[0]["DepMap_ID"]
        tcga = result_object[0]["isTCGAhotspot"]
        self.assertEqual(r.status_code, 200)
        self.assertEqual(True, tcga)
        self.assertEqual("ACH-000003", cell_line_id)
        
    def test_3_tcga_gene_for_cell_line(self):
        path = BASE_URL + "/cell_lines/ACH-000003?gene=7157"
        #valid test. get tcga hotspot for gene and cell_line pair
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        r = self.app.get(path, headers=headers)
        result_object = json.loads(r.get_data())
        gene_id = result_object[0]["Entrez_Gene_Id"]
        cell_line_id = result_object[0]["DepMap_ID"]
        tcga = result_object[0]["isTCGAhotspot"]
        self.assertEqual(r.status_code, 200)
        self.assertEqual(True, tcga)
        self.assertEqual(7157, gene_id)
        self.assertEqual("ACH-000003", cell_line_id)


if __name__ == "__main__":
    unittest.main()