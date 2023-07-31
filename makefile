karabiner-compile:
	python3 karabiner/compile.py > karabiner/karabiner.json

karabiner-install:
	cat karabiner/karabiner.json > ../../.config/karabiner/karabiner.json

karabiner-backup:
	cp ../../.config/karabiner/karabiner.json karabiner/backup.json

karabiner-restore:
	cat karabiner/backup.json > ../../.config/karabiner/karabiner.json
