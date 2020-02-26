import grpc

from proto import user_srv_pb2_grpc
from proto import user_srv_pb2

if __name__ == '__main__':
    channel = grpc.insecure_channel("{}:{}".format("172.22.58.4", "64436"))

    stub = user_srv_pb2_grpc.UserStub(channel)
    res = user_srv_pb2.LoginRequest(name="ss", pwd="s")
    resp = stub.Login(res)

    print(resp)
