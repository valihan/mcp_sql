# server.py
# - Установите зависимости: pip install fastapi uvicorn requests
# - Запустите сервер: python server.py
# - Документация доступна по адресу http://0.0.0.0:8000/docs
import os
from flask import Flask, request, jsonify
from fastapi import FastAPI, HTTPException
import requests
import xml.etree.ElementTree as ET
import logging
from sap_sql import Tools

BASEURL=os.getenv("BASEURL")
CLIENT=os.getenv("CLIENT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("TOKEN")
LISTEN_HOST = os.getenv("LISTEN_HOST")
LISTEN_PORT = os.getenv("LISTEN_PORT")
if LISTEN_HOST is None:
    LISTEN_HOST = "0.0.0.0"
if LISTEN_PORT is None:
    LISTEN_PORT = 8100

tool = Tools(BASEURL, CLIENT, USERNAME, PASSWORD)
app = Flask(__name__)
logging.basicConfig(level=logging.INFO,
                    filename="/var/log/mcp/mcp_sql.log",filemode="w",
                    format = f"%(asctime)s-[%(levelname)s]- (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
print("Base url:"+str(BASEURL)+" Username:"+str(USERNAME))
logging.info("Base url:"+str(BASEURL)+" Username:"+str(USERNAME))

@app.get("/openapi.json")
async def get_json():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logging.warn("Authorization header is missing")
        return jsonify({"error": "Authorization header is missing"}), 401


    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer' or token != TOKEN:
            logging.warn("Invalid token")
            return jsonify({"error": "Invalid token"}), 401
    except ValueError:
        logging.warn("Invalid Authorization header format")
        return jsonify({"error": "Invalid Authorization header format"}), 401

    """Возвращает описание доступных инструментов"""
    data="""{
	"openapi": "3.1.0",
	"info": {
		"title": "mcp-sap",
		"description": "MCP sql to SAP",
		"version": "1.0.0"
	},
	"servers": [
		{
			"url": "/sql"
		}
	],
	"paths": {
		"/sql": {
			"post": {
				"summary": "Execute SQL-query in SAP system",
				"description": "Request data from SAP-table",
				"operationId": "query_post",
				"requestBody": {
					"content": {
						"application/json": {
							"schema": {
								"$ref": "#/components/schemas/query_form_model"
							}
						}
					},
					"required": true
				},
				"responses": {
					"200": {
						"description": "Successful Response",
						"content": {
							"application/json": {
								"schema": {
									"title": "Response data"
								}
							}
						}
					},
					"500": {
						"description": "Server Error",
						"content": {
							"application/json": {
								"schema": {
									"$ref": "#/components/schemas/HTTPValidationError"
								}
							}
						}
					},
					"400": {
						"description": "Validation Error",
						"content": {
							"application/json": {
								"schema": {
									"$ref": "#/components/schemas/ValidationError"
								}
							}
						}
					}
				},
				"security": [
					{
						"HTTPBearer": []
					}
				]
			}
		}
	},
	"components": {
		"schemas": {
			"HTTPValidationError": {
				"properties": {
					"detail": {
						"items": {
							"$ref": "#/components/schemas/ValidationError"
						},
						"type": "array",
						"title": "Detail"
					}
				},
				"type": "object",
				"title": "HTTPValidationError"
			},
			"ValidationError": {
				"properties": {
					"ERROR": {
						"type": "string",
						"description": "error message"
					}
				},
				"type": "object",
				"required": [
					"ERROR"
				],
				"title": "ValidationError"
			},
			"query_form_model": {
				"properties": {
					"query": {
						"type": "string",
						"title": "query",
						"description": "sql-query",
						"default": ""
					}
				},
				"type": "object",
				"title": "query_form_model"
			}
		},
		"securitySchemes": {
			"HTTPBearer": {
				"type": "http",
				"scheme": "bearer"
			}
		}
	}
}"""
    return data, 200, {'Content-Type': 'text/json; charset=utf-8'}

@app.get("/")
async def get_root():
	print("root")
	return "root", 200, {'Content-Type': 'text/json; charset=utf-8'}


@app.get("/tools")
async def get_tools():
    """Возвращает описание доступных инструментов"""
    print("tools")
    return "tools", 200, {'Content-Type': 'text/json; charset=utf-8'}

@app.route("/sql", methods=["POST"])
async def sql():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logging.warn("Authorization header is missing")
        return jsonify({"error": "Authorization header is missing"}), 401


    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer' or token != TOKEN:
            logging.warn("Invalid token")
            return jsonify({"error": "Invalid token"}), 401
    except ValueError:
        logging.warn("Invalid Authorization header format")
        return jsonify({"error": "Invalid Authorization header format"}), 401


    ls_data = request.json
    try:
        print(str(ls_data))
        query=ls_data["query"]
        logging.info(str(query))
        response=tool.execute_sql(sql=str(query))
        print(str(response))
        logging.info(str(response.status_code))
        logging.info(str(response.text))
        return str(response.text), response.status_code, {'Content-Type': 'text/json; charset=utf-8'}
    except Exception as e:
        print(str(e))
        logging.error(str(e))
        return str(e), 500, {'Content-Type': 'text/json; charset=utf-8'}




if __name__ == "__main__":
    app.run(host = LISTEN_HOST, port=LISTEN_PORT)
