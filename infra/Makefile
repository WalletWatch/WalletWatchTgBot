.PHONY: bot 
bot: 
	sudo cp /infra/conf/telegram_bot.service /etc/supervisor/conf.d/telegram_bot.service
	sudo systemctl daemon-reload
	sudo systemctl start telegram_bot
	sudo systemctl enable telegram_bot
	sudo systemctl restart celery
