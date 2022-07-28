#!python3
# -*- coding: utf-8 -*-

from base64 import b64decode, urlsafe_b64decode
import http.server
import json
import traceback
from addrspace import AddressSpace, ModbusAddressSpace
from devfield import DevCmd, DeviceType

from driver import DriverBase
import driverset
from segment import Segment, SegmentSet
import iface_class

class DriverHttpHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.server_version = ""
        self.sys_version = ""

        try:
            req_body_len = int(self.headers["Content-Length"])
            req_body = self.rfile.read(req_body_len)
            request = json.loads(req_body)
            response = {}

            if self.path == "/v1/parse":
                response = self.parse_device_data(request)
            elif self.path == "/v1/exec":
                response = self.exec_command(request)
            elif self.path == "/v1/addr":
                response = self.define_addr_range(request)

            res_body = json.dumps(response, cls=iface_class.JsonEncoderIfJsonEnable)
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(res_body))
            self.end_headers()
            self.wfile.write(bytes(res_body, "utf-8"))
            self.log_message("[DRIVER] [POST] [%s] [body: %d]", self.path, len(res_body))
        except Exception as e:
            self.log_error("[DRIVER] [POST] [%s] FAIL [%s]: \n%s", self.path, str(e), traceback.format_exc())
            self.send_error(400)
            self.end_headers()
            self.wfile.write(b'')

    def define_addr_range(self, request: dict) -> dict:
        d = self.get_driver(request)
        addr_range = d.defineAddrRange()
        return self.make_response(request, True, "addr_range", addr_range)

    def parse_device_data(self, request: dict) -> dict:
        d = self.get_driver(request)
        dd = d.parseDeviceData(self.get_address_space(request))
        return self.make_response(request, dd is not None, "dd", dd)

    def exec_command(self, request: dict) -> dict:
        d = self.get_driver(request)
        r = d.execCommand(self.get_cmd(request))
        return self.make_response(request, r.succ, "cont", r.cont)

    def get_driver(self, request: dict) -> DriverBase:
        if "params" not in request:
            raise AssertionError("Require [params] in request.")
        params = request["params"]
        if not ("type" in params and "producer" in params and "model" in params):
            raise AssertionError("Require [type, producer, model] in [params]")
        type = DeviceType(int(params["type"]))
        producer = str(params["producer"])
        model = str(params["model"])
        d = driverset.DRIVERS.ref(type, producer, model)
        if d is None:
            raise RuntimeError("No driver for [%s(%s):%s:%s]" % (type, type.name, producer, model)) 
        return d

    def get_address_space(self, request: dict) -> AddressSpace:
        params = request["params"]
        space = 1 if "space" not in params else int(params["space"])
        segset = SegmentSet()
        if "segment" in params:
            for seg in params["segment"]:
                sps = int(seg["space"])
                segset.add(Segment(
                    int(seg["addr_begin"]),
                    int(seg["addr_end"]), 
                    int(seg["width"]), 
                    space if sps == 0 else sps, 
                    urlsafe_b64decode(seg["data"])))
        
        return ModbusAddressSpace(segset, space)
        
    def get_cmd(self, request: dict) -> DevCmd:
        cmd = DevCmd()
        params = request["params"]
        cmd.cmd = "noop" if "cmd" not in params else str(params["cmd"])
        for a in params["args"]:
            cmd.args.append(urlsafe_b64decode(a))
        return cmd

    def make_response(self, request: dict, succ: bool, key: str, val: any) -> dict:
        response = {
            "version": 1,
            "jsonrpc": "2.0",
            "id": request["id"],
        }

        if succ:
            response["result"] = {
                key: val
            }
        else:
            response["error"] = {
                "code": 0,
                "message": "driver service failure",
                "data": {
                    key: val
                }
            }
        return response


def run_http_server():
    server = http.server.ThreadingHTTPServer(("", 10099), DriverHttpHandler)
    server.serve_forever()


if __name__ == "__main__":
    run_http_server()
