SPK_NAME = newznab
SPK_VERS = 0.1.1
SPK_REV = 1
SPK_ICON = src/newznab.png
DSM_UI_DIR = app

DEPENDS  =
SPK_DEPENDS = "python>=2.7.3-1"

MAINTAINER = SynoCommunity
DESCRIPTION = Newznab is a usenet indexing application, that makes building a usenet community easy.
DESCRIPTION_FRE = Newznab is a usenet indexing application, that makes building a usenet community easy.
DESCRIPTION_SPN = Newznab is a usenet indexing application, that makes building a usenet community easy.
ADMIN_PORT = 8085
RELOAD_UI = yes
DISPLAY_NAME = Newznab

HOMEPAGE   = http://www.newznab.com/
LICENSE    = GPL

INSTALLER_SCRIPT = src/installer.sh
SSS_SCRIPT       = src/dsm-control.sh

INSTALL_PREFIX = /usr/local/$(SPK_NAME)

COPY_TARGET = nop
POST_STRIP_TARGET = newznab_extra_install

# Pure Python package, make sure ARCH is not defined
override ARCH=

include ../../mk/spksrc.spk.mk

.PHONY: newznab_extra_install
newznab_extra_install: $(STAGING_DIR)/share/requirements.pybundle
	install -m 755 -d $(STAGING_DIR)/var
	install -m 600 src/config.ini $(STAGING_DIR)/var/config.ini
	install -m 755 -d $(STAGING_DIR)/app
	install -m 644 src/app/config $(STAGING_DIR)/app/config
	install -m 755 src/app/newznab.cgi.py $(STAGING_DIR)/app/newznab.cgi
	install -m 755 src/app/newznab.py $(STAGING_DIR)/app/newznab.py
	install -m 755 -d $(STAGING_DIR)/app/images
	for size in 16 24 32 48; do \
		convert $(SPK_ICON) -thumbnail $${size}x$${size} \
		        $(STAGING_DIR)/app/images/$(SPK_NAME)-$${size}.png ; \
	done

$(STAGING_DIR)/share/requirements.pybundle:
	@$(MSG) "Bundling requirements"
	install -m 755 -d $(STAGING_DIR)/share
	@cd $(WORK_DIR) && $(PIP) bundle $@ configobj

