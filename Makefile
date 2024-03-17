# Makefile

# Define variables
PORT_FE=5500

# Define the default make target
.PHONY: serve serve-be run

serve:
	@echo "Starting HTTP server on http://localhost:$(PORT_FE)"
	@cd src_client && http-server . -p $(PORT_FE) --cors
	@sleep 1
	@open http://localhost:$(PORT_FE)

serve-be:
	@echo "Activating conda environment and starting backend server"
	@cd src_server && python main.py

