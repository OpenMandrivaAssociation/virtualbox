# Workaround for the dependency generator somehow
# thinking x11-driver-video-vboxvideo provides libGL.so.1()(64bit)
# causing Mesa to go missing...
%define __noautoprov 'libGL.*'

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
%ifarch x86_64
%define vbox_platform linux.amd64
%endif

# nuke vbox-specific dependencies
#define _provides_exceptions ^VBox
#define _requires_exceptions ^VBox
## Disabled: see rpmlint -I external-depfilter-with-internal-depgen

%define x11_server_majorver %(pkg-config --modversion xorg-server|awk -F. '{print $1$2}')

# FIXME
# kBuild: xpidl XPCOM - /home/bero/abf/virtualbox/BUILD/VirtualBox-5.0.0/src/libs/xpcom18a4/xpcom/base/nsIExceptionService.idl
# error: Missing # define COM __gnu_lto_v1
%define _disable_lto 1

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
Version:	5.1.14
Release:	4
License:	GPLv2
Group:		Emulators
Url:		http://www.virtualbox.org/
Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{srcname}.tar.bz2
Source1:	http://download.virtualbox.org/virtualbox/UserManual.pdf
Source3:	virtualbox-tmpfiles.conf
Source4:	60-vboxadd.perms
Source5:	vboxadd.service
Source6:	vboxweb.service
Source100:	virtualbox.rpmlintrc
# (tpg) dkms is used to build kernel modules, so use it everywhere
Patch1:		virtualbox-fix-modules-rebuild-command.patch
Patch2:		VirtualBox-4.1.8-kernelrelease.patch
Patch3:		VirtualBox-4.1.8-futex.patch
Patch4:		virtualbox-fix-vboxadd-req.patch
# (tmb) disable update notification (OpenSuSe)
Patch7:		VirtualBox-4.3.0-noupdate-check.patch
# don't check for:
# - mkisofs: we're not going to build the additions .iso file
# - makeself: we're not going to create the stanalone .run installers
Patch9:		VirtualBox-5.0.0_BETA3-dont-check-for-mkisofs-or-makeself.patch

Patch16:	virtualbox-default-to-mandriva.patch
Patch18:	VirtualBox-5.1.8-gsoap-2.8.13.patch
Patch21:	VirtualBox-5.0.18-xserver_guest.patch
Patch23:	VirtualBox-5.0.10-no-bundles.patch
Patch24:	VirtualBox-5.0.18-xserver_guest_xorg19.patch

#(tpg) needed for kernel-release-4.10+
Patch25:	VirtualBox-kernel-4.10.patch

ExclusiveArch:	%{ix86} x86_64
BuildRequires:	dev86
BuildRequires:	dkms
BuildRequires:	gawk
BuildRequires:	gsoap
BuildRequires:	acpica
BuildRequires:	java-1.8.0-openjdk-devel
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
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	pkgconfig(python2)
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
# bogus devel-file-in-non-devel-package errors in dkms subpackage
BuildConflicts:	rpmlint < 1.4-37

Requires(post,preun,postun):	rpm-helper
Requires:	kmod(vboxdrv) = %{version}
Suggests:	%{name}-doc
Conflicts:	dkms-%{name} < 5.0.24-1

%description
VirtualBox is a general-purpose full virtualizer for x86 hardware.

%package -n dkms-%{name}
Summary:	VirtualBox kernel module
Group:		System/Kernel and hardware
Requires:	dkms
Requires(post,preun):	dkms
Conflicts:	dkms-vboxadditions < 4.1.8

%description -n dkms-%{name}
Kernel support for VirtualBox.

%if %{build_additions}
%package guest-additions
Summary:	Additions for VirtualBox guest systems
Group:		Emulators
Requires:	kmod(vboxguest) = %{version}
Requires:	kmod(vboxsf) = %{version}
Requires:	kmod(vboxvideo) = %{version}
Requires:	x11-driver-video-vboxvideo
Requires(post,preun): rpm-helper

%description guest-additions
This package contains additions for VirtualBox guest systems.
It allows to share files with the host system and sync time with host.
Install only inside guest.

%package -n dkms-vboxadditions
Summary:	Kernel module for VirtualBox additions
Group:		System/Kernel and hardware
Obsoletes:	dkms-vboxadd < %{version}-%{release}
%rename		dkms-vboxvfs
%rename		dkms-vboxsf
%rename		dkms-vboxvideo = %{version}-%{release}
Conflicts:	dkms-%{name} < 4.1.8
Requires(pre):	dkms
Requires(post,preun):	dkms
Requires(post):	kernel-devel

%description -n dkms-vboxadditions
Kernel module for VirtualBox additions (ideally only needs to be installed
on the guest OS not on the host OS).

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

# Remove bundle X11 sources and some lib sources, before patching.
mv src/VBox/Additions/x11/x11include/mesa-7.2 src/VBox/Additions/x11/
rm -rf src/VBox/Additions/x11/x11include/*
mv src/VBox/Additions/x11/mesa-7.2 src/VBox/Additions/x11/x11include/
rm -rf src/VBox/Additions/x11/x11stubs
rm -rf src/libs/boost-1.37.0/
#rm -rf src/libs/liblzf-3.4/
rm -rf src/libs/libxml2-2.9.2/
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
VBOX_JAVA_HOME := %{java_home}
VBOX_WITHOUT_ADDITIONS_ISO := 1
VBOX_USE_SYSTEM_XORG_HEADERS := 1
XSERVER_VERSION := %{x11_server_majorver}
VBOX_BLD_PYTHON:=/usr/bin/python2
VBOX_GTAR:=
EOF

sed -i 's/CXX="g++"/CXX="g++ -std=c++11"/' configure
sed -i "s!/usr/lib/virtualbox!%{vboxlibdir}!g" src/VBox/Installer/linux/VBox.sh

%build
# FIXME: gold linker dies with internal error in segment_precedes, at ../../gold/layout.cc:3250
mkdir -p BFD
ln -sf /usr/bin/ld.bfd BFD/ld
export PATH=$PWD/BFD:$PATH
export LIBPATH_LIB="%{_lib}"
./configure \
	--enable-vnc \
	--enable-webservice \
	--disable-kmods \
	--enable-qt5 \
	--enable-pulse \
%if ! %{build_doc}
	--disable-docs \
%endif
	|| (cat configure.log && exit 1)

# remove fPIC to avoid causing issues
echo VBOX_GCC_OPT="`echo %{optflags} -fpermissive | sed 's/-fPIC//'`" >> LocalConfig.kmk
%ifarch %{ix86}
%global ldflags %{ldflags} -fuse-ld=bfd
%endif
echo TOOL_GCC_LDFLAGS="%{ldflags}" >> LocalConfig.kmk

%if %{build_additions}
echo XSERVER_VERSION=%{x11_server_majorver} >>LocalConfig.kmk
%else
sed -rie 's/(VBOX_WITH_LINUX_ADDITIONS\s+:=\s+).*/\1/' AutoConfig.kmk
echo VBOX_WITHOUT_ADDITIONS=1 >> LocalConfig.kmk
%endif

. ./env.sh
kmk %{_smp_mflags} all

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
ln -s %{vboxdatadir}/VBox.sh %{buildroot}%{_bindir}/vboxwebsrv

# provide network control tools in bindir
ln -s %{vboxlibdir}/VBoxTunctl %{buildroot}%{_bindir}/VBoxTunctl
ln -s %{vboxlibdir}/VBoxNetAdpCtl %{buildroot}%{_bindir}/VBoxNetAdpCtl
ln -s %{vboxlibdir}/VBoxNetDHCP %{buildroot}%{_bindir}/VBoxNetDHCP

install -d %{buildroot}/var/run/%{oname}

# (tpg) install Web service
install -d %{buildroot}%{_systemunitdir}
install -m 644 %{SOURCE6} %{buildroot}%{_systemunitdir}/vboxweb.service

# install dkms sources
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
cat > %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/dkms.conf << EOF
MAKE[0]="./vboxbuild \$kernel_source_dir"
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/vbox
BUILT_MODULE_LOCATION[0]=%{kname}/
BUILT_MODULE_NAME[0]=%{kname}
DEST_MODULE_LOCATION[1]=/kernel/3rdparty/vbox
BUILT_MODULE_LOCATION[1]=vboxnetflt/
BUILT_MODULE_NAME[1]=vboxnetflt
DEST_MODULE_LOCATION[2]=/kernel/3rdparty/vbox
BUILT_MODULE_LOCATION[2]=vboxnetadp/
BUILT_MODULE_NAME[2]=vboxnetadp
AUTOINSTALL=yes
EOF

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
  install -d %{buildroot}%{_sysconfdir}/modprobe.preload.d
cat > %{buildroot}%{_sysconfdir}/modprobe.preload.d/virtualbox << EOF
vboxdrv
vboxnetflt
vboxnetadp
EOF

# install additions
%if %{build_additions}

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
install -m755 src/VBox/Additions/x11/Installer/98vboxadd-xclient %{buildroot}%{_sysconfdir}/X11/xinit.d

pushd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}/sbin %{buildroot}%{_sbindir} %{buildroot}/%{_libdir}/dri %{buildroot}%{_systemunitdir}
  install -m755 mount.vboxsf %{buildroot}/sbin/mount.vboxsf
  install -m755 VBoxService %{buildroot}%{_sbindir}

  install -m755 VBoxClient %{buildroot}%{_bindir}
  install -m755 VBoxControl %{buildroot}%{_bindir}

  install -m755 VBoxOGL*.so %{buildroot}%{_libdir}

  cat > %{buildroot}%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions << EOF
vboxguest
vboxsf
EOF

  install -m 644 %{SOURCE5} %{buildroot}%{_systemunitdir}/vboxadd.service
  install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-vboxadd.preset << EOF
enable vboxadd.service
EOF

  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}

  mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}
  cat > %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/dkms.conf << EOF
PACKAGE_NAME=vboxadditions
PACKAGE_VERSION=%{version}-%{release}
MAKE[0]="make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxguest &&
cp \$dkms_tree/\$module/\$module_version/build/vboxguest/Module.symvers \$dkms_tree/\$module/\$module_version/build/vboxsf &&
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxsf &&
cp \$dkms_tree/\$module/\$module_version/build/vboxsf/Module.symvers \$dkms_tree/\$module/\$module_version/build/vboxvideo &&
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxvideo"
EOF
  i=0
  for kmod in vboxguest vboxsf vboxvideo; do
    mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/$kmod
    cp -a src/$kmod/* %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/$kmod/
    cat >> %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/dkms.conf << EOF
DEST_MODULE_LOCATION[$i]=/kernel/3rdparty/vbox
BUILT_MODULE_LOCATION[$i]=$kmod/
BUILT_MODULE_NAME[$i]=$kmod
EOF
    i=$((i+1))
  done
  cat >> %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/dkms.conf << EOF
CLEAN="make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxguest clean &&
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxsf clean &&
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxvideo clean "
AUTOINSTALL=yes
EOF
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

%post -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{name} -v %{version}-%{release} &&
/usr/sbin/dkms --rpm_safe_upgrade install -m %{name} -v %{version}-%{release}
/sbin/rmmod vboxnetflt &>/dev/null
/sbin/rmmod vboxnetadp &>/dev/null
/sbin/rmmod %{kname} &>/dev/null
/sbin/modprobe %{kname} &>/dev/null
/sbin/modprobe vboxnetflt &>/dev/null
/sbin/modprobe vboxnetadp &>/dev/null
:

%preun -n dkms-%{name}
if [ "$1" = "0" ]; then
    /sbin/rmmod vboxnetadp >/dev/null 2>&1
    /sbin/rmmod vboxnetflt >/dev/null 2>&1
    /sbin/rmmod %{kname} >/dev/null 2>&1
fi
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{name} -v %{version}-%{release} --all || :

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

%post -n dkms-vboxadditions
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m vboxadditions -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m vboxadditions -v %{version}-%{release} &&
/usr/sbin/dkms --rpm_safe_upgrade install -m vboxadditions -v %{version}-%{release}
:

%preun -n dkms-vboxadditions
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m vboxadditions -v %{version}-%{release} --all
:

%endif

%files
%config %{_sysconfdir}/vbox/vbox.cfg
%{_sysconfdir}/modprobe.preload.d/virtualbox
%{_bindir}/%{oname}
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxTunctl
%{_bindir}/VBoxNetAdpCtl
%{_bindir}/VBoxNetDHCP
%{_bindir}/vboxwebsrv
%{_systemunitdir}/vboxweb.service
%{vboxlibdir}/dtrace
%{vboxlibdir}/icons
%{vboxlibdir}/components
%{vboxlibdir}/*.so
%{vboxlibdir}/iPxeBaseBin
%{vboxlibdir}/VBoxAutostart
%{vboxlibdir}/VBoxBalloonCtrl
%{vboxlibdir}/VBoxBugReport
%{vboxlibdir}/VBoxCpuReport
%{vboxlibdir}/VBoxDTrace
%{vboxlibdir}/VBoxEFI32.fd
%{vboxlibdir}/VBoxEFI64.fd
%{vboxlibdir}/VBoxExtPackHelperApp
%{vboxlibdir}/VBoxManage
%{vboxlibdir}/VBoxNetNAT
%{vboxlibdir}/VBoxSVC
%{vboxlibdir}/VBoxTestOGL
%{vboxlibdir}/VBoxTunctl
%{vboxlibdir}/VBoxVMMPreload
%{vboxlibdir}/VBoxVolInfo
%{vboxlibdir}/VBoxXPCOMIPCD
%{vboxlibdir}/vboxkeyboard.tar.bz2
%{vboxlibdir}/vboxshell.py
%{vboxlibdir}/virtualbox.xml
%{vboxlibdir}/vboxwebsrv
%{vboxlibdir}/webtest
%{vboxlibdir}/scripts
%{vboxlibdir}/tools
%{vboxlibdir}/ExtensionPacks
%{vboxlibdir}/rdesktop-vrdp*
# this files need proper permission
%attr(4711,root,root) %{vboxlibdir}/VBoxHeadless
%attr(4711,root,root) %{vboxlibdir}/VBoxSDL
%attr(4711,root,root) %{vboxlibdir}/VirtualBox
%attr(4711,root,root) %{vboxlibdir}/VBoxNetAdpCtl
%attr(4711,root,root) %{vboxlibdir}/VBoxNetDHCP
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

%files -n dkms-%{name}
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
%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions

%files -n x11-driver-video-vboxvideo
%{_libdir}/VBoxOGL*

%files -n dkms-vboxadditions
%{_usr}/src/vbox*-%{version}-%{release}
%endif

%files doc
%{vboxlibdir}/UserManual.pdf
