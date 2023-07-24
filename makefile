install:
	# mv ../../.config/karabiner/karabiner.json ../../.config/karabiner/karabiner.json.backup
	python3 karabiner/toJson.py > ../../.config/karabiner/karabiner.json
