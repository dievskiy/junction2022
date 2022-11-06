from docusign_lib import entry
import functions_framework
from flask import jsonify


@functions_framework.http
def send_nda_email(request):
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        try:
            signer_email = request_json['signer_email']
            signer_name = request_json['signer_name']
            cc_email = request_json['cc_email']
            cc_name = request_json['cc_name']
            data = {
                    "signer_email": signer_email,
                    "cc_email": cc_email,
                    "signer_name": signer_name,
                    "cc_name": cc_name
            }
            entry.send_email(data)
        except ValueError:
            raise ValueError("JSON is invalid, or missing a property")
        return jsonify({"message": "success"})
    return jsonify({"message": "Data not provided"})

