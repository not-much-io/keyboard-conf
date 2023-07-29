karabiner-compile:
	python3 karabiner/compile.py > karabiner/karabiner.json

karabiner-install:
	python3 karabiner/karabiner.json > ../../.config/karabiner/karabiner.json
