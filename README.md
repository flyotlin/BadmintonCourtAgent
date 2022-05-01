# Badminton Court Agent Bot

## How to Deploy?
You can deploy the Bot on your server using `Ansible`.

By executing the ansible playbook `deploy.yaml`, your server is good to go.

Execute: `$ ansible-playbook deploy.yaml`

> Remenber before executing, fill in `base` and `telegram_bot_token` in `vars` inside `deploy.yaml`.

> Remember to open your port 27017 to allow the Bot to accept request from Internet.

## Chat-bot Commands
- `/help`: 查看可用的阿椰指令，加上 command (optional) 後有更詳細說明
- `/token`: 設定 token
- `/check`: 查詢空場地
- `/reserve`: 預約場地
- `/toggle_reserve`: 自動預約場地
- `/toggle_poll`: 自動開啟投票
- `/toggle_remind`: 自動傳送預約提醒訊息

更詳細的指令可以查看 `src/handler/help.py`。
## Acknowledgement
Special thanks to @cliffxzx.
![](https://avatars.githubusercontent.com/u/44764053?v=4)