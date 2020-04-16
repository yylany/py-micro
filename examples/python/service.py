from proto import user_srv_pb2_grpc

from proto import user_srv_pb2
import micro_py
import grpc


class UserDemo(user_srv_pb2_grpc.UserServicer):
    def Register(self, request, context):
        print(request)
        return user_srv_pb2.LoginResponse(token="cc")

    def Login(self, request, context):
        return user_srv_pb2.LoginResponse(token="cc")


class Inter(grpc.GenericRpcHandler):
    def service(self, handler_call_details):
        print(handler_call_details)
        print("service")


if __name__ == '__main__':
    server = micro_py.Service({
        "server_name": "go.micro.srv.ty",
        "server_port": 64436,
        "registry": "consul",
        "registry_address": "127.0.0.1:8500",
    }, micro_py.Flag(
        name="gp",
        default="cc",
        env_var="GP_ENV"
    ))

    server.addWrapHandler([Inter()])


    user_srv_pb2_grpc.add_UserServicer_to_server(UserDemo(), server)

    server.run()
