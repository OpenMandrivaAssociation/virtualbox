%define kname vboxdrv
%define oname VirtualBox
%define srcname %{oname}-%{version}%{?beta:_%{beta}}
%define distname %{oname}-%{version}%{?beta:_%{beta}}
%define pkgver %{ver}

%define vboxlibdir %{_prefix}/lib/%{name}
%define vboxdatadir %{_datadir}/%{name}

%ifarch %{x86_64}
%define vbox_platform linux.amd64
%endif

# nuke vbox-specific dependencies, don't provide libGL.so.1
%global __provides_exclude ^VBox|\^libGL\\.so\\.1|\^libEGL\\.so\\.1
%global __requires_exclude ^VBox

%define x11_server_majorver %(pkg-config --modversion xorg-server|awk -F. '{print $1$2}')

# FIXME
# kBuild: xpidl XPCOM - /home/bero/abf/virtualbox/BUILD/VirtualBox-5.0.0/src/libs/xpcom18a4/xpcom/base/nsIExceptionService.idl
# error: Missing # define COM __gnu_lto_v1
%define _disable_lto 1

# (tpg) reduce the opt flags, especially for znver1
%global optflags %{optflags} -Os

%bcond_with java
%bcond_with clang
%bcond_with docs

## (crazy) fixem that is always true these days
%bcond_without additions
%bcond_without vnc_ext_pack
%bcond_without firmware

#define svn 20230604

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
# WARNING: WHEN UPDATING THIS PACKAGE, ALWAYS REBUILD THE
# kernel AND kernel-rc PACKAGES TO MAKE SURE MODULES
# AND USERSPACE ARE IN SYNC
Version:	7.0.10
Release:	%{?svn:0.%{svn}.}1
License:	GPLv2
Group:		Emulators
Url:		http://www.virtualbox.org/
%if 0%{?svn:1}
Source0:	VirtualBox-%{svn}.tar.xz
%else
Source0:	http://download.virtualbox.org/virtualbox/%(echo %{version} |sed -e 's,[a-z]*,,g')/%{srcname}.tar.bz2
%endif
Source1:	http://download.virtualbox.org/virtualbox/%(echo %{version} |sed -e 's,[a-z]*,,g')/UserManual.pdf
Source3:	virtualbox-tmpfiles.conf
Source4:	60-vboxadd.perms
Source5:	vboxadd.service
Source6:	vboxweb.service
Source7:	vboxdrmclient.service
Source8:	vboxdrmclient.path
Source20:	os_openmandriva.png
Source21:	os_openmandriva_64.png
%if %{with firmware}
# Can't use system openssl because we built OpenSSL for UEFI, not
# for Linux
%define openssl 1.1.1k
Source50:	https://www.openssl.org/source/openssl-%{openssl}.tar.gz
%endif
Source100:	virtualbox.rpmlintrc
# Revert upstream's (between 6.1.0 and 6.1.2) removal of symbols
# that are used everywhere -- without this patch, starting
# any VM results in
# Failed to load R0 module /usr/lib64/virtualbox/VMMR0.r0:
# Unable to locate imported symbol 'PciRawR0Term' for module
# 'VMMR0.r0' (VERR_SYMBOL_NOT_FOUND).
Patch0:		VirtualBox-6.1.2-revert-removal-of-vital-symbols.patch
# Update docs on kernel modules
Patch1:		virtualbox-fix-modules-rebuild-command.patch
# Fix docs to give the right mount command for the in-tree version of vboxsf
Patch3:		VirtualBox-4.1.8-futex.patch
Patch4:		virtualbox-fix-vboxadd-req.patch
Patch5:		virtualbox-7.0.8-libstdc++13.patch
# We build the kernel modules in-tree -- adjust the Makefiles to support it
Patch6:		vbox-6.0.0-kernel-modules-in-tree.patch
# (tmb) disable update notification (OpenSuSe)
#Patch7:		VirtualBox-4.3.0-noupdate-check.patch
# https://git.archlinux.org/svntogit/community.git/plain/trunk/101-vboxsf-automount.patch?h=packages/virtualbox
Patch8:		101-vboxsf-automount.patch

# don't check for:
# - mkisofs: we're not going to build the additions .iso file
# - makeself: we're not going to create the stanalone .run installers
Patch9:		VirtualBox-5.0.0_BETA3-dont-check-for-mkisofs-or-makeself.patch
# Default to a reasonable size in guest additions
Patch10:	VirtualBox-6.1.12a-default-to-1024x768.patch
#Patch11:	vbox-6.1.10-compile.patch
#Patch12:	vbox-6.1.24-python-syntax.patch

Patch18:	VirtualBox-5.1.8-gsoap-2.8.13.patch
Patch22:	virtualbox-no-prehistoric-xfree86.patch
#Patch23:	VirtualBox-5.0.10-no-bundles.patch
Patch24:	VirtualBox-5.0.18-xserver_guest_xorg19.patch
#Patch25:	fix-vboxadd-xclient.patch
#Patch26:	vbox-6.1.6-firmware-build-python3.9.patch
# "Borrowed" from Debian https://salsa.debian.org/pkg-virtualbox-team/virtualbox/blob/master/debian/patches
#Patch103:	06-xsession.patch
Patch104:	07-vboxnetflt-reference.patch
Patch105:	12-make-module.patch
#Patch107:	16-no-update.patch
Patch108:	18-system-xorg.patch
#Patch109:	27-hide-host-cache-warning.patch
Patch110:	29-fix-ftbfs-as-needed.patch
Patch111:	32-disable-guest-version-check.patch
Patch112:	35-libvdeplug-soname.patch
# Fixes patch 107
#Patch113:	disable-update-manager-for-real.patch
# (tpg) add support for OpenMandriva
# (crazy) this should be prepared for upstream..
#Patch200:	VirtualBox-add-support-for-OpenMandriva.patch
# (tpg) do not crash on Wayland
Patch201:	VirtualBox-5.2.16-use-xcb-on-wayland.patch
Patch202:	vbox-6.0.6-find-java-modules.patch
# From FrugalWare
#Patch300:	https://gitweb.frugalware.org/frugalware-current/raw/master/source/xapps-extra/virtualbox/fix-EFI-boot.patch
#Patch301:	https://gitweb.frugalware.org/frugalware-current/raw/67d0618e5c19f8b44ebb6eab78c56048b412bdc3/source/xapps-extra/virtualbox/firmware-build-fixes.patch
ExclusiveArch:	%{x86_64}
# (tpg) 2019-10-16 vbox is not ready for LLVM/clang
BuildRequires:	gcc-c++
BuildRequires:	systemd-rpm-macros
BuildRequires:	dev86
BuildRequires:	gawk
BuildRequires:	gsoap
BuildRequires:	acpica
BuildRequires:	yasm
BuildRequires:	vde2
BuildRequires:	glslang
BuildRequires:	pkgconfig(xorg-server)
%if %{with firmware}
BuildRequires:	nasm
%endif
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	java-18-openjdk-module-java.logging
BuildRequires:	javax.activation
BuildRequires:	javax.xml.bind
%endif
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(libcap)
BuildRequires:	libstdc++-static-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	pkgconfig(python)
BuildRequires:	qt5-qttools
BuildRequires:	qt5-linguist-tools
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xorg-server) >= 1.18
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(liblzf)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libxml2-utils
# FIXME not sure why, but vbox checks if there's a working
# 32-bit compiler. Probably for the BIOS?
# But it doesn't use -nostdlib or so, so we need to BR
# a 32-bit libc
BuildRequires:	libc6
%if %{with docs}
# for building the user manual pdf file
BuildRequires:	texlive
BuildRequires:	texlive-fontsextra
BuildRequires:	docbook-dtd45-xml
Suggests:	%{name}-doc
%endif
Requires(post,preun,postun):	rpm-helper
#Requires:	kmod(vboxdrv) = %{version}
Conflicts:	dkms-%{name} < 5.0.24-1

# Force kernel-headers from the release package - kernel-rc headers cause
# /usr/include/linux/usbdevice_fs.h:134:41: error: flexible array member 'usbdevfs_urb::iso_frame_desc' not at end of 'struct USBPROXYURBLNX'
BuildRequires:	kernel-headers
BuildConflicts:	kernel-rc-headers

%description
VirtualBox is a general-purpose full virtualizer for x86 hardware.

%package kernel-module-sources
Summary:	VirtualBox kernel module sources
Group:		System/Kernel and hardware
%rename dkms-%{name}

%description kernel-module-sources
VirtualBox kernel module sources.

These sources are pulled into the kernel source tree by the
kernel RPMs. There is no need to install this package unless
you're building your own kernel.

The modules in this package are required on the HOST side.

%package guest-additions
Summary:	Additions for VirtualBox guest systems
Group:		Emulators
Requires:	x11-driver-video-vmware
Requires:	%{_lib}dri-drivers-vmwgfx
Requires:	libnotify
Requires(post,preun): rpm-helper

%description guest-additions
This package contains additions for VirtualBox guest systems.
It allows to share files with the host system and sync time with host.
Install only inside guest.

%package guest-kernel-module-sources
Summary:	Kernel module sources for VirtualBox additions
Group:		System/Kernel and hardware
Obsoletes:	dkms-vboxadd < %{version}-%{release}
%rename		dkms-vboxvfs
%rename		dkms-vboxsf
%rename		dkms-vboxvideo
Conflicts:	dkms-%{name} < 4.1.8
%rename dkms-vboxadditions

%description guest-kernel-module-sources
Kernel module sources for VirtualBox additions.

These sources are pulled into the kernel source tree by the
kernel RPMs. There is no need to install this package unless
you're building your own kernel.

The modules in this package are required on the GUEST side.


%if %{with docs}
%package doc
Summary:	The user manual PDF file for %{name}
Group:		System/X11
BuildArch:	noarch

%description doc
This package contains the user manual PDF file for %{name}.
%endif

%prep
%autosetup -p1 -n %{?svn:VirtualBox-%{svn}}%{!?svn:%(echo %{distname} |sed -e 's,[a-z]*$,,')}

%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif

# (crazy) - Change all back to VBoxSVGA until I fix VMSVGA and make it somewhat work with wayland.
# NOTE: VMSVGA does NOT work right with wayland, complain to vbox folks & the wayland project. Thx.
sed -i -e 's|GraphicsControllerType_VMSVGA|GraphicsControllerType_VBoxSVGA|g' src/VBox/Main/src-all/Global.cpp

# add OpenMandriva images
cp -a %{SOURCE20} %{SOURCE21} src/VBox/Frontends/VirtualBox/images/

# Remove prebuilt binary tools
find -name '*.py[co]' -delete
rm -r src/VBox/Additions/WINNT
rm -r src/VBox/Additions/os2
# Remove bundle X11 sources and some lib sources, before patching.
rm -rf src/VBox/Additions/x11/x11include
rm -rf src/VBox/Additions/x11/x11stubs
# (tpg) somehow this does not work with system-wide liblzf, so do not remove liblzf-*
rm -rf src/libs/{libpng-*,libxml2-*,zlib-*}

cat << EOF > LocalConfig.kmk
VBOX_WITH_WARNINGS_AS_ERRORS:=
VBOX_PATH_APP_PRIVATE_ARCH:=%{vboxlibdir}
VBOX_PATH_SHARED_LIBS:=%{vboxlibdir}
VBOX_WITH_RUNPATH:=%{vboxlibdir}
VBOX_WITH_ORIGIN:=
VBOX_PATH_APP_PRIVATE:=/usr/share/virtualbox
VBOX_WITH_VNC:=1
VBOX_WITH_VPX:=1
VBOX_WITH_LIBOPUS:=1
VBOX_WITH_LIBCURL:=1
SDK_VBOX_LIBPNG_INCS:=%{_includedir}/libpng16
SDK_VBOX_LIBPNG_LIBS:=png16
SDK_VBOX_LIBXML2_LIBS:=xml2
SDK_VBOX_ZLIB_INCS:=""
SDK_VBOX_ZLIB_LIBS:=z
#SDK_VBOX_LZF_INCS:=""
#SDK_VBOX_LZF_LIBS:=lzf
SDK_VBOX_OPUS_INCS:=%{_includedir}/opus
SDK_VBOX_OPUS_LIBS:=opus
SDK_VBOX_VPX_INCS:=%{_includedir}/vpx
SDK_VBOX_VPX_LIBS:=vpx
SDK_VBOX_LIBCURL_INCS:=%{_includedir}/curl
SDK_VBOX_LIBCURL_LIBS:=curl
VBOX_WITH_TESTCASES:=0
VBOX_WITH_TESTSUITE:=0
# FIXME re-enable when fixed upstream
#VBOX_WITH_PCI_PASSTHROUGH:=1
VBOX_WITH_VALIDATIONKIT:=0
%if %{with java}
VBOX_JAVA_HOME:=${JAVA_HOME}
%else
VBOX_JAVA_HOME:=
%endif
VBOX_WITHOUT_ADDITIONS_ISO:=1
VBOX_WITHOUT_PRECOMPILED_HEADERS:=1
VBOX_USE_SYSTEM_XORG_HEADERS:=1
VBOX_USE_SYSTEM_GL_HEADERS:=1
VBOX_NO_LEGACY_XORG_X11:=1
XSERVER_VERSION:=%{x11_server_majorver}
VBOX_BLD_PYTHON:=/usr/bin/python
VBOX_GTAR:=
TOOL_YASM_AS=yasm
VBOX_WITH_REGISTRATION_REQUEST:=0
VBOX_WITH_UPDATE_REQUEST:=0
VBOX_GUI_WITH_SHARED_LIBRARY:=1
# Default is Oracle VM VirtualBox -- let's not advertise the bad guys
VBOX_PRODUCT=VirtualBox
%if %{with firmware}
VBOX_EFI_FIRMWARE_EFI_MODULES_KMK_INCLUDED := 0
%endif
VBOX_WITH_VBOX_IMG := 1
VBOX_WITH_VBOXIMGMOUNT := 1
VBOX_WITH_VBOXSDL := 1
EOF

# (tpg) 2019-10-16 vbox is not ready for LLVM/clang
%if %{with clang}
sed -i -e 's#CC="gcc"#CC="clang"#g' configure
sed -i -e 's#CXX="g++"#CXX="clang++"#g' configure
sed -i -e 's,-mpreferred-stack-boundary=2,,g' Config.kmk src/VBox/Devices/PC/ipxe/Makefile.kmk src/VBox/Devices/PC/ipxe/src/arch/i386/Makefile
%endif

# (crazy) why? needs to go
#sed -i -e 's#-fpermissive##g' -e 's#-finline-limit=8000##g' Config.kmk

%build
# FIXME: lld: src/VBox/Devices/PC/ipxe/src/arch/x86/scripts/pcbios.lds:267: at least one side of the expression must be absolute
mkdir -p BFD
ln -sf /usr/bin/ld.bfd BFD/ld
export PATH=$PWD/BFD:$PATH
export LIBPATH_LIB="%{_lib}"

# remove fPIC to avoid causing issues
%if %{with clang}
echo VBOX_GCC_OPT="$(echo %{optflags} | sed -e 's/-fPIC//' -e 's/-Werror=format-security//') -isystem %{_libdir}/gcc/x86_64-openmandriva-linux-gnu/13.1.0/include -rtlib=libgcc" >> LocalConfig.kmk
%else
echo VBOX_GCC_OPT="$(echo %{optflags} | sed -e 's/-fPIC//' -e 's/-Werror=format-security//')" >> LocalConfig.kmk
%endif
echo TOOL_GCC_LDFLAGS="%{build_ldflags} -fuse-ld=bfd" >> LocalConfig.kmk

# (crazy) /opt is the wrong location
#sed -i -e 's|opt/VirtualBox|usr/share/virtualbox|g' src/VBox/RDP/client-1.8.4/Makefile.kmk

./configure \
    --enable-vnc \
    --enable-vde \
%if %{with java}
    --enable-webservice \
%else
    --disable-java \
%endif
    --disable-kmods \
    --enable-qt5 \
%if %{without docs}
    --disable-docs \
%endif
    --enable-pulse || (cat configure.log && exit 1)

. ./env.sh

export PATH=$PWD/BFD:$PATH

%if %{with firmware}
	# NOTE: this needs to run before main kmk,
	# *DD.so & *DD2.so uses the EFI* stuff we just build here
	TOP="$(pwd)"
	rm src/VBox/Devices/EFI/FirmwareBin/*
	cd src/VBox/Devices/EFI/Firmware
	. ./edksetup.sh
	cd CryptoPkg/Library/OpensslLib
	tar xf %{S:50}
	mv openssl-1* openssl
	perl process_files.pl
	cd ../../..
	kmk
	cd "${TOP}"
	cp out/*/release/bin/VBoxEFI*.fd src/VBox/Devices/EFI/FirmwareBin/
%endif

# (crazy) we want this package in kmk *very verbose* mode to see what the hell they do
# DO NOT REMOVE!
kmk %{_smp_mflags} KBUILD_VERBOSE=2 all

%if %{with vnc_ext_pack}
# (crazy) package that as extension pack, users can istall from UI. Needs just some docs.
kmk %{_smp_mflags} KBUILD_VERBOSE=2 -C src/VBox/ExtPacks/VNC packing
%endif

%install
# install vbox components
mkdir -p %{buildroot}%{vboxlibdir} %{buildroot}%{vboxdatadir}

# (crazy) NOTE: packaging like this is wrong! FIXME
(cd out/%{vbox_platform}/release/bin && tar cf - --exclude=additions .) | \
(cd %{buildroot}%{vboxlibdir} && tar xf -)
# move noarch files to vboxdatadir
# (crazy) _WHY_ is VBox.sh in datadir? FIXME
mv %{buildroot}%{vboxlibdir}/{VBox*.sh,nls,*.png} %{buildroot}%{vboxdatadir}

# wipe crap/duplicates
# (crazy) broken symlink
rm -f %{buildroot}%{vboxlibdir}/components/VBoxREM.so
# packaged in mime
rm -f %{buildroot}%{vboxlibdir}/virtualbox.xml
# those service.sh etc scripts ( no such init here ) are junk, don't package
rm -f %{buildroot}%{vboxlibdir}/*.sh
# don't package source archives, that is the open source version, we don't need to provide any source in this case
rm -f %{buildroot}%{vboxlibdir}/rdesktop-vrdp.tar.gz
rm -f %{buildroot}%{vboxlibdir}/vboxkeyboard.tar.bz2
# FIXME: use that to install icons, but until then remove it
rm -rf %{buildroot}%{vboxlibdir}/icons

# And the desktop file where it belongs
mkdir -p %{buildroot}%{_datadir}/applications/
mv %{buildroot}%{vboxlibdir}/*.desktop %{buildroot}%{_datadir}/applications/
# Fix bogus space between file:// and filename
sed -i -e 's,file:// /,file:///,' %{buildroot}%{_datadir}/applications/virtualbox.desktop

# install wrappers
mkdir -p %{buildroot}%{_sysconfdir}/vbox
cat > %{buildroot}%{_sysconfdir}/vbox/vbox.cfg << EOF
# VirtualBox installation directory
INSTALL_DIR="%{vboxlibdir}"
EOF

mkdir -p %{buildroot}%{_bindir}
ln -s %{vboxdatadir}/VBox.sh %{buildroot}%{_bindir}/%{oname}
ln -s %{vboxdatadir}/VBox.sh %{buildroot}%{_bindir}/VBoxManage
ln -s %{vboxdatadir}/VBox.sh %{buildroot}%{_bindir}/VBoxSDL
ln -s %{vboxdatadir}/VBox.sh %{buildroot}%{_bindir}/VBoxHeadless
%if %{with java}
ln -s %{vboxdatadir}/VBox.sh %{buildroot}%{_bindir}/vboxwebsrv
%endif

# provide network control tools in bindir
ln -s %{vboxlibdir}/VBoxTunctl %{buildroot}%{_bindir}/VBoxTunctl
ln -s %{vboxlibdir}/VBoxNetAdpCtl %{buildroot}%{_bindir}/VBoxNetAdpCtl
ln -s %{vboxlibdir}/VBoxNetDHCP %{buildroot}%{_bindir}/VBoxNetDHCP
# other symlinks
ln -s %{vboxlibdir}/vbox-img %{buildroot}%{_bindir}/vbox-img
ln -s %{vboxlibdir}/vboximg-mount %{buildroot}%{_bindir}/vboximg-mount
ln -s %{vboxlibdir}/rdesktop-vrdp %{buildroot}%{_bindir}/rdesktop-vrdp

install -d %{buildroot}/var/run/%{oname}

%if %{with java}
# (tpg) install Web service
install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/vboxweb.service
%endif

# install kernel module sources
mkdir -p %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}
cat > vboxbuild << EOF
#!/bin/sh
set -e
make -C %{kname} KERN_DIR=\$1
cp -f %{kname}/Module.symvers vboxnetflt
cp -f %{kname}/Module.symvers vboxnetadp
make -C vboxnetflt KERN_DIR=\$1
make -C vboxnetadp KERN_DIR=\$1
EOF
install -m 0755 vboxbuild %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}
mv %{buildroot}%{vboxlibdir}/src/* %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/

# install udev rules
mkdir -p %{buildroot}%{_udevrulesdir}
cat > %{buildroot}%{_udevrulesdir}/%{name}.rules << EOF
KERNEL=="%{kname}", NAME="vboxdrv", OWNER="root", GROUP="root", MODE="0600"
SUBSYSTEM=="usb_device", ACTION=="add", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh \$major \$minor \$attr{bDeviceClass} vboxusers"
SUBSYSTEM=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh \$major \$minor \$attr{bDeviceClass} vboxusers"
SUBSYSTEM=="usb_device", ACTION=="remove", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh --remove \$major \$minor"
SUBSYSTEM=="usb", ACTION=="remove", ENV{DEVTYPE}=="usb_device", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh --remove \$major \$minor"
EOF
%if %{with additions}
cat > %{buildroot}%{_udevrulesdir}/vbox-additions.rules << EOF
KERNEL=="vboxguest", NAME="vboxguest", OWNER="root", MODE="0660"
KERNEL=="vboxuser", NAME="vboxuser", OWNER="root", MODE="0666"
EOF
%endif

# (tpg) create modules to load
install -d %{buildroot}%{_sysconfdir}/modules-load.d
cat > %{buildroot}%{_sysconfdir}/modules-load.d/virtualbox.conf << EOF
vboxdrv
vboxnetflt
vboxnetadp
EOF

%if %{with vnc_ext_pack}
## could be any other folder, just not the origial one vbox uses itself
mkdir -p %{buildroot}%{vboxdatadir}/extensions
install -m644 out/%{vbox_platform}/release/packages/VNC-*.vbox-extpack %{buildroot}%{vboxdatadir}/extensions
%endif

# install additions
%if %{with additions}
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
install -m755 src/VBox/Additions/x11/Installer/98vboxadd-xclient %{buildroot}%{_bindir}/VBoxClient-all
install -m644 src/VBox/Additions/x11/Installer/vboxclient.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/vboxclient.desktop

cd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}%{_sbindir}  %{buildroot}%{_unitdir}
  install -m755 mount.vboxsf %{buildroot}%{_sbindir}/
  install -m755 VBoxService %{buildroot}%{_sbindir}
  install -m755 VBoxClient %{buildroot}%{_bindir}
  install -m755 VBoxControl %{buildroot}%{_bindir}
  install -m755 VBoxDRMClient %{buildroot}%{_bindir}

  cat > %{buildroot}%{_sysconfdir}/modules-load.d/vbox-guest-additions.conf << EOF
vboxguest
vboxsf
EOF

  install -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/vboxadd.service
  install -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/vboxdrmclient.service
  install -m 644 %{SOURCE8} %{buildroot}%{_unitdir}/vboxdrmclient.path
  install -d %{buildroot}%{_presetdir}
## FIXME: (crazy) figure the loading of vboxvideo, it looks to me vbox is trying to load stuff
## based on what UI options are set.
cat > %{buildroot}%{_presetdir}/86-virtualbox-guest-additions.preset << EOF
enable vboxadd.service
enable vboxdrmclient.service
enable vboxdrmclient.path
EOF
  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}

  mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}
  for kmod in vboxguest vboxsf vboxvideo; do
    mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/$kmod
    cp -a src/$kmod/* %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/$kmod/
  done
cd -

# install PAM module:
install -D -m755 out/%{vbox_platform}/release/bin/additions/pam_vbox.so %{buildroot}%{_libdir}/security/pam_vbox.so
%endif

# install mime types
install -D -m644 src/VBox/Installer/common/virtualbox.xml %{buildroot}%{_datadir}/mime/packages/virtualbox.xml

## FIXME: INSTALL from /icons/ folder
# install shipped icons for apps and mimetypes
for i in 16 20 32 40 48 64 128; do
    install -D -m0644 src/VBox/Artwork/OSE/virtualbox-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/virtualbox.png
done

for i in 16 20 24 32 40 48 64 72 80 96 128 256 512; do
    install -D -m0644 src/VBox/Artwork/other/virtualbox-ova-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-ova.png
    install -D -m0644 src/VBox/Artwork/other/virtualbox-ovf-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-ovf.png
    install -D -m0644 src/VBox/Artwork/other/virtualbox-vbox-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-vbox.png
    install -D -m0644 src/VBox/Artwork/other/virtualbox-vbox-extpack-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-vbox-extpack.png
done

# add missing makefile for kernel module
install -m644 src/VBox/HostDrivers/Support/linux/Makefile %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/

%if ! %{with docs}
install -m644 %{SOURCE1} %{buildroot}%{vboxlibdir}/UserManual.pdf
%endif

# remove unpackaged files
rm -rf %{buildroot}%{vboxlibdir}/{src,sdk,testcase}
rm  -f %{buildroot}%{vboxlibdir}/tst*
rm  -f %{buildroot}%{vboxlibdir}/SUP*
rm  -f %{buildroot}%{vboxlibdir}/xpidl
rm  -f %{buildroot}%{vboxlibdir}/*.debug

install -m644 -D %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%if %{with additions}
# Replace the vboxsf mount wrapper with one that works for
# the in-tree version of the kernel module
mkdir -p %{buildroot}%{_sbindir}
cat >%{buildroot}%{_sbindir}/mount.vboxsf <<'EOF'
#!/bin/bash
name=${1#$PWD/}; shift
exec /bin/mount -cit vboxsf "$name" "$@"
EOF
chmod 0755 %{buildroot}%{_sbindir}/mount.vboxsf
%endif

%post
%_add_group_helper %{name} 1 vboxusers

%postun
%_del_group_helper %{name} 1 vboxusers

%if %{with additions}
%post guest-additions
# (Debian) Build usb device tree
for i in /sys/bus/usb/devices/*; do
if test -r "$i/dev"; then
dev="$(cat "$i/dev" 2> /dev/null || true)"
major="$(expr "$dev" : '\(.*\):' 2> /dev/null || true)"
minor="$(expr "$dev" : '.*:\(.*\)' 2> /dev/null || true)"
class="$(cat $i/bDeviceClass 2> /dev/null || true)"
/usr/share/virtualbox/VBoxCreateUSBNode.sh "$major" "$minor" "$class" vboxusers 2>/dev/null || true
fi
done
%endif

%files
%config %{_sysconfdir}/vbox/vbox.cfg
%{_sysconfdir}/modules-load.d/virtualbox.conf
%{_bindir}/%{oname}
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxTunctl
%{_bindir}/VBoxNetAdpCtl
%{_bindir}/VBoxNetDHCP
%{_bindir}/vboximg-mount
%{_bindir}/vbox-img
%{_bindir}/rdesktop-vrdp
%if %{with java}
%{_bindir}/vboxwebsrv
%{_unitdir}/vboxweb.service
%endif
%dir %{_prefix}/lib/virtualbox
%{_prefix}/lib/virtualbox/vboxwebsrv
%{_prefix}/lib/virtualbox/webtest
%{vboxlibdir}/bldRTLdrCheckImports
%{vboxlibdir}/dtrace
%{vboxlibdir}/components
%{vboxlibdir}/*.so
%{vboxlibdir}/iPxeBaseBin
%{vboxlibdir}/UnattendedTemplates
%{vboxlibdir}/VBoxAutostart
%{vboxlibdir}/VBoxBalloonCtrl
%{vboxlibdir}/VBoxBugReport
%{vboxlibdir}/VBoxCpuReport
%{vboxlibdir}/VBoxDTrace
%{vboxlibdir}/VBoxEFI32.fd
%{vboxlibdir}/VBoxEFI64.fd
%{vboxlibdir}/VBoxExtPackHelperApp
%{vboxlibdir}/VBoxManage
%{vboxlibdir}/VBoxSDL
%{vboxlibdir}/VBoxSVC
%{vboxlibdir}/VBoxVMMPreload
%{vboxlibdir}/VBoxXPCOMIPCD
%{vboxlibdir}/VirtualBox
%{vboxlibdir}/vboxshell.py
%{vboxlibdir}/vboximg-mount
%{vboxlibdir}/VBoxAudioTest
%{vboxlibdir}/VBoxTestOGL
%if %{with java}
%{vboxlibdir}/vboxwebsrv
%{vboxlibdir}/webtest
%endif
#%%if %{with vnc_ext_pack}
#%%{vboxdatadir}/extensions/VNC-*
#%%endif
%{vboxlibdir}/scripts
%{vboxlibdir}/tools
%{vboxlibdir}/ExtensionPacks
%{vboxlibdir}/vbox-img
# this files need proper permission
%attr(4711,root,root) %{vboxlibdir}/VBoxHeadless
%attr(4711,root,root) %{vboxlibdir}/VBoxNetAdpCtl
%attr(4711,root,root) %{vboxlibdir}/VBoxNetDHCP
%attr(4711,root,root) %{vboxlibdir}/VBoxNetNAT
%attr(4711,root,root) %{vboxlibdir}/VBoxVolInfo
%attr(4711,root,root) %{vboxlibdir}/VirtualBoxVM
%attr(644,root,root) %{vboxlibdir}/*.r0
%if %{without docs}
%exclude %{vboxlibdir}/UserManual.pdf
%endif
%{vboxdatadir}
%config %{_udevrulesdir}/%{name}.rules
%{_tmpfilesdir}/%{name}.conf
%dir /var/run/%{oname}
# desktop integration
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/virtualboxvm.desktop
%{_datadir}/mime/packages/virtualbox.xml

%files kernel-module-sources
%{_usr}/src/%{name}-%{version}-%{release}

%if %{with additions}
%files guest-additions
%{_libdir}/security/pam_vbox.so
%{_sbindir}/mount.vboxsf
%{_presetdir}/86-virtualbox-guest-additions.preset
%{_unitdir}/vboxadd.service
%{_unitdir}/vboxdrmclient.service
%{_unitdir}/vboxdrmclient.path
%{_sbindir}/VBoxService
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_bindir}/VBoxDRMClient
%{_bindir}/VBoxClient-all
%{_udevrulesdir}/vbox-additions.rules
%{_sysconfdir}/xdg/autostart/*
%{_sysconfdir}/modules-load.d/vbox-guest-additions.conf

%files guest-kernel-module-sources
%{_usr}/src/vbox*-%{version}-%{release}
%endif

%if %{with docs}
%files doc
%{vboxlibdir}/UserManual.pdf
%endif
