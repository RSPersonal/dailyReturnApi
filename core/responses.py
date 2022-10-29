# Standard responses

EMPTY_SUCCESS_RESPONSE = {"message": "success",
                          "status_code": 200,
                          "data": {}
                          }

ACCESS_FORBIDDEN_RESPONSE = {"message": "failed",
                             "status_code": 403,
                             "data": {}
                             }

NOT_FOUND_RESPONSE = {"message": "failed",
                      "status_code": 404,
                      "data": {}
                      }

SERVER_ERROR_RESPONSE = {"message": "failed",
                         "status_code": 500,
                         "data": {}
                         }
