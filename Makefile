VENV = venv
V_BIN = $(VENV)/bin

CMD = sigmou


all: $(VENV)/$(CMD)


$(VENV)/$(CMD): $(V_BIN)/python
	$(V_BIN)/pip install -e .


$(V_BIN)/python:
	python3 -m venv $(VENV)
	chmod +x $(V_BIN)/activate
	./$(V_BIN)/activate


clean:
	rm -rf *.egg-info
	rm -rf */__pycache__


fclean: clean
	rm -rf venv


.PHONY: all clean fclean