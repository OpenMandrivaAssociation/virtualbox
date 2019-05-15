%ifarch %{ix86}
# This is bogus, but at normal optimization levels, gcc
# tries to allocate more memory than 32-bit address space
# can hold :/
%global optflags %{optflags} -g0 -fno-lto -fuse-ld=bfd -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
%global ldflags %{ldflags} -g0 -fno-lto -fuse-ld=bfd -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
%endif

%bcond_with java

%define beta %{nil}
%define kname vboxdrv
%define oname VirtualBox
%if "%{beta}" != ""
%define srcname %{oname}-%{version}_%{beta}
%define distname %{oname}-%{version}_%{beta}
%else
%define srcname %{oname}-%{version}
%define distname %{oname}-%{version}
%endif
%define pkgver %{ver}

%define vboxlibdir %{_libdir}/%{name}
%define vboxdatadir %{_datadir}/%{name}

%define build_additions 1
%define build_doc 0

%ifarch %{ix86}
%define vbox_platform linux.x86
%endif
%ifarch %{x86_64}
%define vbox_platform linux.amd64
%endif

# nuke vbox-specific dependencies, dont provide libGL.so.1
%global __provides_exclude ^VBox|\^libGL\\.so\\.1|\^libEGL\\.so\\.1
%global __requires_exclude ^VBox

%define x11_server_majorver %(pkg-config --modversion xorg-server|awk -F. '{print $1$2}')

# FIXME
# kBuild: xpidl XPCOM - /home/bero/abf/virtualbox/BUILD/VirtualBox-5.0.0/src/libs/xpcom18a4/xpcom/base/nsIExceptionService.idl
# error: Missing # define COM __gnu_lto_v1
%define _disable_lto 1

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
# WARNING: WHEN UPDATING THIS PACKAGE, ALWAYS REBUILD THE
# kernel-release AND kernel-rc PACKAGES TO MAKE SURE MODULES
# AND USERSPACE ARE IN SYNC
Version:	6.0.8
Release:	1
License:	GPLv2
Group:		Emulators
Url:		http://www.virtualbox.org/
Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{srcname}.tar.bz2
Source1:	http://download.virtualbox.org/virtualbox/UserManual.pdf
Source3:	virtualbox-tmpfiles.conf
Source4:	60-vboxadd.perms
Source5:	vboxadd.service
Source6:	vboxweb.service
Source20:	os_openmandriva.png
Source21:	os_openmandriva_64.png
Source100:	virtualbox.rpmlintrc
# Update docs on kernel modules
Patch1:		virtualbox-fix-modules-rebuild-command.patch
# Fix docs to give the right mount command for the in-tree version of vboxsf
Patch2:		http://crazy.dev.frugalware.org/vboxsf-mainline-mount-help.patch
Patch3:		VirtualBox-4.1.8-futex.patch
Patch4:		virtualbox-fix-vboxadd-req.patch
# We build the kernel modules in-tree -- adjust the Makefiles to support it
Patch6:		vbox-6.0.0-kernel-modules-in-tree.patch
# (tmb) disable update notification (OpenSuSe)
Patch7:		VirtualBox-4.3.0-noupdate-check.patch
Patch8:		https://git.archlinux.org/svntogit/community.git/plain/trunk/101-vboxsf-automount.patch?h=packages/virtualbox
# don't check for:
# - mkisofs: we're not going to build the additions .iso file
# - makeself: we're not going to create the stanalone .run installers
Patch9:		VirtualBox-5.0.0_BETA3-dont-check-for-mkisofs-or-makeself.patch

Patch18:	VirtualBox-5.1.8-gsoap-2.8.13.patch
Patch22:	virtualbox-no-prehistoric-xfree86.patch
Patch23:	VirtualBox-5.0.10-no-bundles.patch
Patch24:	VirtualBox-5.0.18-xserver_guest_xorg19.patch

# "Borrowed" from Debian
Patch103:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/06-xsession.patch
Patch104:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/07-vboxnetflt-reference.patch
Patch107:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/16-no-update.patch
Patch108:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/18-system-xorg.patch
Patch109:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/27-hide-host-cache-warning.patch
Patch110:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/29-fix-ftbfs-as-needed.patch
Patch111:	https://sources.debian.org/data/contrib/v/virtualbox/5.2.16-dfsg-3/debian/patches/37-python-3.7-support.patch

# (tpg) add support for OpenMandriva
# (crazy) this should be prepared for upstream..
Patch200:	VirtualBox-add-support-for-OpenMandriva.patch
# (tpg) do not crash on Wayland
Patch201:	VirtualBox-5.2.16-use-xcb-on-wayland.patch
Patch202:	vbox-6.0.6-find-java-modules.patch

ExclusiveArch:	%{ix86} %{x86_64}
BuildRequires:	systemd-macros
BuildRequires:	dev86
BuildRequires:	gawk
%ifnarch %{ix86}
BuildRequires:	gsoap
%endif
BuildRequires:	acpica
BuildRequires:	yasm
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	javax.activation
BuildRequires:	javax.xml.bind
%endif
BuildRequires:	xsltproc
BuildRequires:	libcap-devel
BuildRequires:	libstdc++-static-devel
BuildRequires:	openssl-devel
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
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xorg-server) >= 1.18
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(liblzf)
BuildRequires:	pkgconfig(libpng)
%if %{build_doc}
# for building the user manual pdf file
BuildRequires:	texlive
BuildRequires:	texlive-fontsextra
BuildRequires:	docbook-dtd44-xml
%endif
Requires(post,preun,postun):	rpm-helper
#Requires:	kmod(vboxdrv) = %{version}
Suggests:	%{name}-doc
Conflicts:	dkms-%{name} < 5.0.24-1

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

%if %{build_additions}
%package guest-additions
Summary:	Additions for VirtualBox guest systems
Group:		Emulators
#Requires:	kmod(vboxguest) = %{version}
#Requires:	kmod(vboxsf) = %{version}
#Requires:	kmod(vboxvideo) = %{version}
Requires:	x11-driver-video-vboxvideo
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

%package -n x11-driver-video-vboxvideo
Summary:	The X.org driver for video in VirtualBox guests
Group:		System/X11
Requires:	x11-server-common
Suggests:	virtualbox-guest-additions
Conflicts:	virtualbox-guest-additions < 2.2.0-2

%description -n x11-driver-video-vboxvideo
The X.org driver for video in VirtualBox guests
%endif

%package doc
Summary:	The user manual PDF file for %{name}
Group:		System/X11
BuildArch:	noarch

%description doc
This package contains the user manual PDF file for %{name}.

%prep
%setup -qn %{distname}
%apply_patches
%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif

# (crazy) - Change all back to VBoxVGA , *SVGA and *VMSVGA not yet working right.
sed -i -e 's|GraphicsControllerType_VBoxSVGA|GraphicsControllerType_VBoxVGA|g' src/VBox/Main/src-all/Global.cpp
sed -i -e 's|GraphicsControllerType_VMSVGA|GraphicsControllerType_VBoxVGA|g' src/VBox/Main/src-all/Global.cpp

# add OpenMandriva images
cp -a %{SOURCE20} %{SOURCE21} src/VBox/Frontends/VirtualBox/images/

# Remove bundle X11 sources and some lib sources, before patching.
mv src/VBox/Additions/x11/x11include/mesa-7.2 src/VBox/Additions/x11/
rm -rf src/VBox/Additions/x11/x11include/*
mv src/VBox/Additions/x11/mesa-7.2 src/VBox/Additions/x11/x11include/
rm -rf src/VBox/Additions/x11/x11stubs
rm -rf src/libs/boost-1.37.0/
#rm -rf src/libs/liblzf-3.4/
rm -rf src/libs/libxml2-2.9.4/
rm -rf src/libs/libpng-1.2.54/
rm -rf src/libs/zlib-1.2.8/

cat << EOF > LocalConfig.kmk
VBOX_WITH_WARNINGS_AS_ERRORS:=
VBOX_PATH_APP_PRIVATE_ARCH:=%{vboxlibdir}
VBOX_WITH_ORIGIN:=
VBOX_WITH_RUNPATH:=%{vboxlibdir}
VBOX_PATH_APP_PRIVATE:=%{vboxlibdir}
VBOX_WITH_VNC:=1
VBOX_WITH_TESTCASES =
VBOX_WITH_TESTSUITE:=
%if %{with java}
VBOX_JAVA_HOME := %{java_home}
%else
VBOX_JAVA_HOME :=
%endif
VBOX_WITHOUT_ADDITIONS_ISO := 1
VBOX_WITHOUT_PRECOMPILED_HEADERS := 1
VBOX_USE_SYSTEM_XORG_HEADERS := 1
VBOX_USE_SYSTEM_GL_HEADERS := 1
VBOX_NO_LEGACY_XORG_X11 := 1
VBOX_USE_SYSTEM_GL_HEADERS := 1
XSERVER_VERSION := %{x11_server_majorver}
VBOX_BLD_PYTHON:=/usr/bin/python
VBOX_GTAR:=
TOOL_YASM_AS=yasm
VBOX_WITH_REGISTRATION_REQUEST= 
VBOX_WITH_UPDATE_REQUEST= 
EOF

sed -i 's/CXX="g++"/CXX="g++ -std=gnu++14"/' configure
sed -i "s!/usr/lib/virtualbox!%{vboxlibdir}!g" src/VBox/Installer/linux/VBox.sh

%build
# FIXME: gold linker dies with internal error in segment_precedes, at ../../gold/layout.cc:3250
mkdir -p BFD
ln -sf /usr/bin/ld.bfd BFD/ld
export PATH=$PWD/BFD:$PATH
export LIBPATH_LIB="%{_lib}"
./configure \
	--enable-vnc \
%if %{with java}
	--enable-webservice \
%else
	--disable-java \
%endif
	--disable-kmods \
	--enable-qt5 \
	--enable-pulse \
%if ! %{build_doc}
	--disable-docs \
%endif
	|| (cat configure.log && exit 1)

# remove fPIC to avoid causing issues
echo VBOX_GCC_OPT="`echo %{optflags} -fpermissive $(pkg-config --cflags pixman-1) | sed -e 's/-fPIC//' -e 's/-Werror=format-security//'`" >> LocalConfig.kmk
#ifarch %{ix86}
%global ldflags %{ldflags} -fuse-ld=bfd
#endif
echo TOOL_GCC_LDFLAGS="%{ldflags}" >> LocalConfig.kmk

%if %{build_additions}
echo XSERVER_VERSION=%{x11_server_majorver} >>LocalConfig.kmk
%else
sed -rie 's/(VBOX_WITH_LINUX_ADDITIONS\s+:=\s+).*/\1/' AutoConfig.kmk
echo VBOX_WITHOUT_ADDITIONS=1 >> LocalConfig.kmk
%endif

. ./env.sh
kmk %{_smp_mflags} all VERBOSE=1

%install
# install vbox components
mkdir -p %{buildroot}%{vboxlibdir} %{buildroot}%{vboxdatadir}

(cd out/%{vbox_platform}/release/bin && tar cf - --exclude=additions .) | \
(cd %{buildroot}%{vboxlibdir} && tar xf -)

# move noarch files to vboxdatadir
mv %{buildroot}%{vboxlibdir}/{VBox*.sh,nls,*.desktop,*.png} %{buildroot}%{vboxdatadir}

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
cat > %{buildroot}%{_udevrulesdir}/vbox-additions.rules << EOF
KERNEL=="vboxguest", NAME="vboxguest", OWNER="root", MODE="0660"
KERNEL=="vboxuser", NAME="vboxuser", OWNER="root", MODE="0666"
EOF

# (tpg) create modules to load
install -d %{buildroot}%{_sysconfdir}/modules-load.d
cat > %{buildroot}%{_sysconfdir}/modules-load.d/virtualbox.conf << EOF
vboxdrv
vboxnetflt
vboxnetadp
EOF

# install additions
%if %{build_additions}

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
install -m755 src/VBox/Additions/x11/Installer/98vboxadd-xclient %{buildroot}%{_sysconfdir}/X11/xinit.d

pushd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}/sbin %{buildroot}%{_sbindir} %{buildroot}/%{_libdir}/dri %{buildroot}%{_unitdir}
  install -m755 mount.vboxsf %{buildroot}/sbin/mount.vboxsf
  install -m755 VBoxService %{buildroot}%{_sbindir}
  install -m755 VBoxClient %{buildroot}%{_bindir}
  install -m755 VBoxControl %{buildroot}%{_bindir}

  install -m755 VBox*.so %{buildroot}%{_libdir}

  cat > %{buildroot}%{_sysconfdir}/modules-load.d/vbox-guest-additions.conf << EOF
vboxguest
vboxsf
EOF

  install -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/vboxadd.service
  install -d %{buildroot}%{_presetdir}
# (crazy) race with udev / kmod and xinit file
# seems like .service always fails, lets disable for now.
cat > %{buildroot}%{_presetdir}/86-vboxadd.preset << EOF
disable vboxadd.service
EOF

  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}

  mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}
  for kmod in vboxguest vboxsf vboxvideo; do
    mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/$kmod
    cp -a src/$kmod/* %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/$kmod/
  done
popd

%endif

# install menu entries
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=VirtualBox
Comment=Full virtualizer for x86 hardware
Exec=%{_bindir}/%{oname}
Icon=%{name}
Type=Application
Terminal=false
Categories=Emulator;
MimeType=application/x-virtualbox-vbox;application/x-virtualbox-vbox-extpack;application/x-virtualbox-ovf;application/x-virtualbox-ova;
EOF

# install mime types
install -D -m644 src/VBox/Installer/common/virtualbox.xml %{buildroot}%{_datadir}/mime/packages/virtualbox.xml

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

%if !%{build_doc}
install -m644 %{SOURCE1} %{buildroot}%{vboxlibdir}/UserManual.pdf
%endif

# remove unpackaged files
rm -rf %{buildroot}%{vboxlibdir}/{src,sdk,testcase}
rm  -f %{buildroot}%{vboxlibdir}/tst*
rm  -f %{buildroot}%{vboxlibdir}/vboxkeyboard.tar.gz
rm  -f %{buildroot}%{vboxlibdir}/SUP*
rm  -f %{buildroot}%{vboxlibdir}/xpidl
rm  -f %{buildroot}%{vboxlibdir}/*.debug

# install PAM module:
install -D -m755 out/%{vbox_platform}/release/bin/additions/pam_vbox.so %{buildroot}/%{_lib}/security/pam_vbox.so

install -m644 -D %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# Put a symlink to VBoxOGL where it will be found
ln -s %{_libdir}/VBoxOGL.so %{buildroot}%{_libdir}/dri/vboxvideo_dri.so

# Replace the vboxsf mount wrapper with one that works for
# the in-tree version of the kernel module
cat >%{buildroot}/sbin/mount.vboxsf <<'EOF'
#!/bin/bash
name=${1#$PWD/}; shift
exec /bin/mount -cit vboxsf "$name" "$@"
EOF
chmod 0755 %{buildroot}/sbin/mount.vboxsf

%post
%_add_group_helper %{name} 1 vboxusers
/sbin/rmmod vboxnetflt &>/dev/null
/sbin/rmmod vboxnetadp &>/dev/null
/sbin/rmmod %{kname} &>/dev/null
/sbin/modprobe %{kname} &>/dev/null
/sbin/modprobe vboxnetflt &>/dev/null
/sbin/modprobe vboxnetadp &>/dev/null

%postun
%_del_group_helper %{name} 1 vboxusers

%if %{build_additions}
%post guest-additions
# (Debian) Build usb device tree
for i in /sys/bus/usb/devices/*; do
if test -r "$i/dev"; then
dev="`cat "$i/dev" 2> /dev/null || true`"
major="`expr "$dev" : '\(.*\):' 2> /dev/null || true`"
minor="`expr "$dev" : '.*:\(.*\)' 2> /dev/null || true`"
class="`cat $i/bDeviceClass 2> /dev/null || true`"
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
%if %{with java}
%{_bindir}/vboxwebsrv
%{_unitdir}/vboxweb.service
%endif
%{vboxlibdir}/bldRTLdrCheckImports
%{vboxlibdir}/dtrace
%{vboxlibdir}/icons
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
%{vboxlibdir}/VBoxSVC
%{vboxlibdir}/VBoxTestOGL
%{vboxlibdir}/VBoxTunctl
%{vboxlibdir}/VBoxVMMPreload
%{vboxlibdir}/VBoxXPCOMIPCD
%{vboxlibdir}/VirtualBox
%{vboxlibdir}/vboxkeyboard.tar.bz2
%{vboxlibdir}/vboxshell.py
%{vboxlibdir}/__pycache__
%if %{with java}
%{vboxlibdir}/vboxwebsrv
%{vboxlibdir}/webtest
%endif
%{vboxlibdir}/virtualbox.xml
%{vboxlibdir}/scripts
%{vboxlibdir}/tools
%{vboxlibdir}/ExtensionPacks
%{vboxlibdir}/rdesktop-vrdp*
# this files need proper permission
%attr(4711,root,root) %{vboxlibdir}/VBoxHeadless
%attr(4711,root,root) %{vboxlibdir}/VBoxSDL
%attr(4711,root,root) %{vboxlibdir}/VBoxNetAdpCtl
%attr(4711,root,root) %{vboxlibdir}/VBoxNetDHCP
%attr(4711,root,root) %{vboxlibdir}/VBoxNetNAT
%attr(4711,root,root) %{vboxlibdir}/VBoxVolInfo
%attr(4711,root,root) %{vboxlibdir}/VirtualBoxVM
%attr(644,root,root) %{vboxlibdir}/*.rc
%attr(644,root,root) %{vboxlibdir}/*.r0
%attr(755,root,root) %{vboxlibdir}/*.sh
%exclude %{vboxlibdir}/UserManual.pdf
%{vboxdatadir}
%config %{_udevrulesdir}/%{name}.rules
%{_tmpfilesdir}/%{name}.conf
%dir /var/run/%{oname}
# desktop integration
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/virtualbox.xml

%files kernel-module-sources
%{_usr}/src/%{name}-%{version}-%{release}

%if %{build_additions}
%files guest-additions
/%{_lib}/security/pam_vbox.so
/sbin/mount.vboxsf
%{_presetdir}/86-vboxadd.preset
%{_unitdir}/vboxadd.service
%{_sbindir}/VBoxService
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_udevrulesdir}/vbox-additions.rules
%{_sysconfdir}/X11/xinit.d/98vboxadd-xclient
%{_sysconfdir}/modules-load.d/vbox-guest-additions.conf

%files -n x11-driver-video-vboxvideo
%{_libdir}/VBoxEGL*
%{_libdir}/VBoxOGL*
%{_libdir}/dri/vboxvideo_dri.so

%files guest-kernel-module-sources
%{_usr}/src/vbox*-%{version}-%{release}
%endif

%files doc
%{vboxlibdir}/UserManual.pdf
