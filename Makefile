# ---- Настройки ----
PYTHON ?= python3
SCRIPT := uninstall_app.py

# Цель по умолчанию: просто сделать скрипт исполняемым
all: install

.PHONY: all install run delete clean help

# Сделать скрипт исполняемым
install:
	@chmod +x $(SCRIPT)
	@echo "✅ $(SCRIPT) теперь исполняемый"
	@echo ""
	@echo "Запуск напрямую:   sudo ./$(SCRIPT) <пакет>"
	@echo "Или через make:    make delete <пакет>"

# Интерактивный запуск (спросит имя пакета)
run:
	sudo $(PYTHON) $(SCRIPT)

# Удаление: make delete <имя_пакета>
delete:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Использование: make delete <имя_пакета>"; \
		echo "Пример:        make delete sublime-text"; \
		exit 1; \
	fi
	@sudo $(PYTHON) $(SCRIPT) $(filter-out $@,$(MAKECMDGOALS))

# Очистка временных файлов
clean:
	@rm -rf __pycache__ *.pyc
	@echo "🧹 Очищено."

# Справка
help:
	@echo "Доступные цели:"
	@echo "  make                    — сделать скрипт исполняемым"
	@echo "  make install            — то же самое"
	@echo "  make run                — интерактивный запуск"
	@echo "  make delete <пакет>     — удалить пакет (Ubuntu или Fedora)"
	@echo "  make clean              — удалить временные файлы"
	@echo "  make help               — эта справка"

# Ловим «лишние» аргументы (имя пакета) как пустые цели,
# чтобы make не ругался на неизвестную цель
%:
	@:
