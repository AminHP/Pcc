# Makefile for compiler project

.PHONY: compile clean

UI_DIR = "ui"
BUILD_DIR = "build"
OUTPUT_DIR = "output"

compile:
	antlr4 -Dlanguage=Python2 -o $(BUILD_DIR) pcc.g4
	pyuic4 -i 4 $(UI_DIR)/mainwindow.ui -o $(BUILD_DIR)/mainwindow.py

clean:
	rm -rf $(BUILD_DIR) $(OUTPUT_DIR)
