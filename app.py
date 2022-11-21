"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json

from db import get_gene, get_cell_line
from flask import Flask, Response, request

app = Flask(__name__)
file_name = 'dataset.csv'

class APINotFoundError(Exception):
    code = 404
    description = "The requested resource is not found in the database"

class APIBadRequest(Exception):
    code = 400
    description = "Bad request. The request is either malformed or the content type is invalid"

@app.errorhandler(APINotFoundError)
@app.errorhandler(APIBadRequest)
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_exception(err):
    response = {
      "error": err.description, 
    }
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return Response(
            json.dumps(response), status=err.code, mimetype="application/json"
        )

#/cell_lines?gene=&tcga=
@app.route("/cell_lines", methods=["GET"])
@app.route("/cell_lines/<cell_line_id>", methods=["GET"])
def cell_lines(cell_line_id=None):
    """
    Function to get cell_lines
    """
    if request.method == "GET":
        query_parameters = request.args
        if(query_parameters.get("gene")):
            gene_id = int(query_parameters.get("gene"))
        else: 
            raise APIBadRequest
        if(query_parameters.get("tcga")):
            if(query_parameters.get("tcga").lower()=="false"):
                is_tcga = False
            elif(query_parameters.get("tcga").lower()=="true"): 
                is_tcga = True
            else:
                raise APIBadRequest
        else:
            is_tcga = True

        cell_line = get_cell_line(is_tcga, gene_id, cell_line_id, file_name)
        if(not cell_line):
            raise APINotFoundError

        # respond
        return Response(
            cell_line, status=200, mimetype="application/json"
        )

@app.route("/genes", methods=["GET"])
def genes():
    """
    Function to get genes
    """
    if request.method == "GET":
        query_parameters = request.args
        if(query_parameters.get("cell_line")):
            cell_line_id = query_parameters.get("cell_line")
        else: 
            raise APIBadRequest

        if(query_parameters.get("tcga")):
            if(query_parameters.get("tcga").lower()=="false"):
                is_tcga = False
            elif(query_parameters.get("tcga").lower()=="true"): 
                is_tcga = True
            else:
                raise APIBadRequest
        else:
            is_tcga = True

        gene = get_gene(is_tcga, cell_line_id, file_name)
        if(not genes):
            raise APINotFoundError

        # respond
        return Response(
            gene, status=200, mimetype="application/json"
        )

if __name__ == "__main__":
    app.run()
