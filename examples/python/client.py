import random

import grpc

from proto import user_srv_pb2_grpc
from proto import user_srv_pb2

from py_micro import registry

if __name__ == '__main__':
    registry = registry.NewConsul(
        host="127.0.0.1:8500"
    )

    services = registry.get_service("go.micro.srv.tr")

    service = random.choice(services)
    channel = grpc.insecure_channel("{}:{}".format("127.0.0.1", service["Port"]))
    stub = user_srv_pb2_grpc.UserStub(channel)

    res = user_srv_pb2.LoginRequest(name="ss", pwd="s")

    resp = stub.Login(res)
    print(resp)
