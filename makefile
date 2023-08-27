karabiner-compile:
	python3 karabiner/generate.py > karabiner/karabiner.json

karabiner-install:
	cat karabiner/karabiner.json > ../../.config/karabiner/karabiner.json

karabiner-backup:
	cp ../../.config/karabiner/karabiner.json karabiner/backup.json

karabiner-restore:
	cat karabiner/backup.json > ../../.config/karabiner/karabiner.json

karabiner-devloop: karabiner-compile karabiner-install karabiner-backup
	