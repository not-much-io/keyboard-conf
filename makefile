get:
	cp ../../.config/karabiner/karabiner.json karabiner

install:
	mv ../../.config/karabiner/karabiner.json ../../.config/karabiner/karabiner.json.backup
	cp karabiner/karabiner.json ../../.config/karabiner/karabiner.json
