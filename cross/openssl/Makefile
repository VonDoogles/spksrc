PKG_NAME = openssl
PKG_VERS = 1.0.0j
PKG_EXT = tar.gz
PKG_DIST_NAME = $(PKG_NAME)-$(PKG_VERS).$(PKG_EXT)
PKG_DIST_SITE = http://www.openssl.org/source
PKG_DIR = $(PKG_NAME)-$(PKG_VERS)

DEPENDS = cross/zlib

HOMEPAGE = http://www.openssl.org/
COMMENT  = Compression Library
LICENSE  = zlib-license

CONFIGURE_TARGET = myConfigure

INSTALL_TARGET = myInstall

STAGING_INSTALL_PREFIX := $(INSTALL_DIR)

include ../../mk/spksrc.cross-cc.mk

ifneq ($(findstring $(ARCH), bromolow cedarview x86),)
OPENSSL_ARCH = linux-elf
else
OPENSSL_ARCH = linux-generic32
endif

.PHONY: myConfigure
myConfigure:
	$(RUN) ./Configure --openssldir=$(INSTALL_PREFIX) $(OPENSSL_ARCH) zlib-dynamic shared threads

.PHONY: myInstall
myInstall:
	$(RUN) $(MAKE) install_sw INSTALL_PREFIX=$(INSTALL_DIR)

