import os
import signal
import time
from concurrent import futures

import grpc

from . import registry
from . import options


class Flag:
    def __init__(self, name: str, env_var, default):
        """
        定义初始化参数
        :param name: 保存的名字
        :param env_var: 环境变量的名字
        :param default: 默认值
        """
        self.default = default
        self.env_var = env_var
        self.name = name


class Service:
    def __init__(self, ops: dict = None,
                 *args: Flag
                 ):
        mate = ops
        if mate is None:
            mate = {}
            # 记录数据，并保留环境变量的值
        # 初始化程序只带解析的环境变量参数
        for (k, v) in options.OPS.items():
            ev = os.getenv(v[0], v[1])
            # 判定是否等于默认值
            if ev == v[1]:
                # 判断是否设置有值，如果有，则不使用默认值
                if mate.get(k) is None:
                    mate[k] = ev
            else:
                mate[k] = ev

        # 初始化自定义的环境变量参数
        for f in args:
            mate[f.name] = os.getenv(f.name, f.default)

        self.registry = registry.Registry()
        if mate["registry"] == "consul":
            self.registry = registry.NewConsul(
                mate["server_name"],
                mate["server_address"],
                mate["server_port"],
                mate["registry_address"],
                mate["register_interval"],
            )

        ser = grpc.server(futures.ThreadPoolExecutor(max_workers=mate["server_pool_size"]))
        self.service = ser
        self.mate = mate

    def get_mate(self, name: str):
        """
        获取init 绑定的环境变量
        :param name: 环境变量的名字
        :return:
        """
        return self.mate[name]

    def addWrapHandler(self, generic_rpc_handlers: [grpc.GenericRpcHandler]):
        self.service.add_generic_rpc_handlers(generic_rpc_handlers)

    def run(self):
        port = self.get_mate("server_port")
        host = "{}:{}".format(self.get_mate("server_address"), port)
        self.service.add_insecure_port(host)

        print("Server Listening on {}".format(host))
        print("Registering node: {}:{}".format(self.get_mate("server_name"), self.get_mate("server_id")))
        self.service.start()

        def un(signalnum, handler):
            self.registry.deregister()
            exit(0)

        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, un)

        while True:
            while True:
                try:
                    self.registry.register()
                    break
                except Exception as e:
                    print(e)
                    time.sleep(5)
            time.sleep(self.get_mate("register_interval") * 1000)
