# Makefile to manage dotfiles via symlinks to git repository
# Shamelessly borrowed from https://github.com/cofi/dotfiles

PWD := `pwd`
LINK_CMD := ln --symbolic --force -T
NORMAL_FILES := `ls -I Makefile`

deploy:
	@for file in $(NORMAL_FILES); do $(LINK_CMD) $(PWD)/$$file ~/.$$file; done
