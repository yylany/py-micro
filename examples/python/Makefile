# 应用名称
NAME = user

# docker 镜像版本
VERSION = latest
# docker 镜像名
DNAME = yylany/$(NAME):$(VERSION)

CODE_PATH =D:\work\wanfang\code
APP_PATH=$(CODE_PATH)/git.wanfang.com/api/ty-api/

.PHONY: proto
proto:
	@protoc -I=$(CODE_PATH)  --micro_out=$(CODE_PATH)  --go_out=$(CODE_PATH)  $(APP_PATH)proto\hello\say.api.proto
	@protoc -I=$(CODE_PATH)  --micro_out=$(CODE_PATH)  --go_out=$(CODE_PATH)  $(APP_PATH)proto\user\user.api.proto
# win 下必须使用绝对路径
#@protoc -I=.:$(CODE_PATH) --micro_out=. --go_out=. proto\hello\user.api.proto


.PHONY: docker
docker:
	docker build . -t $(DNAME)