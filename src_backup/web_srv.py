from flask import Flask, request,jsonify
from port_table import PortTable
from call_mgr import CallMgr
import json
import logging
import logging.handlers
import helper

app = Flask(__name__)

@app.route('/',methods=['POST'])
def do_ports():
    payload = request.json
    logger = logging.getLogger(__name__)
    logger.info(payload)
    callid = payload['callid']
    callMgr = CallMgr.instance()
    if callid == "":
        return jsonify({"response":400})
    if payload['type'] == 'addPort':
        audio_port = payload['audio']
        video_port = payload['video']
        content_port = payload['content']
        fecc_port = payload['fecc']
        bfcp_port = payload['bfcp']
        call = callMgr.getCall(payload['callid'])
        if call == "":
            call = callMgr.addCall(payload['callid'])
        subtype = payload['sub_type']
        if subtype == 'localOffer':
            call.addLocalOfferPort(audio_port,video_port,content_port,fecc_port,bfcp_port)
        elif subtype == 'localAnswer':
            call.addLocalAnswerPort(audio_port,video_port,content_port,fecc_port,bfcp_port) 
        elif subtype == 'remoteOffer':
            call.addRemoteOfferPort(audio_port,video_port,content_port,fecc_port,bfcp_port)
        elif subtype == 'remoteAnswer':
            call.addRemoteAnswerPort(audio_port,video_port,content_port,fecc_port,bfcp_port)
    elif payload['type'] == 'delPort':
        callMgr.rmCall(callid)
    return jsonify({"response":200})


if __name__ == '__main__':
    port_table = PortTable()
    port_table.start()
    callMgr = CallMgr()
    callMgr.start()
    helper.setup_env()
    app.run(host='0.0.0.0',port=8001,debug=True)