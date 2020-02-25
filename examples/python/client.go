package main

import (
	"context"
	"fmt"
	co "github.com/hashicorp/consul/api"
	"github.com/micro/go-micro"
	"github.com/micro/go-micro/service/grpc"
	"github.com/micro/go-plugins/registry/consul"
	"python/proto"
)

func main() {

	conf := co.DefaultConfig()
	conf.Address = "127.0.0.1:8500"
	con_registry := consul.NewRegistry(consul.Config(conf))

	sers, err := con_registry.GetService("user.srv")

	sers = sers

	service := grpc.NewService(
		micro.Registry(con_registry),
	)

	service.Init()

	cl := proto.NewUserService("user.srv", service.Client())

	rsp, err := cl.Login(context.TODO(), &proto.LoginRequest{
		Name: "cc",
		Pwd:  "ll",
	})

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(rsp.Token)

}
