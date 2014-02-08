%define kname  vboxdrv
%define oname  VirtualBox
%define srcname	%{oname}-%{version}
%define distname	%{oname}-%{version}
%define pkgver	%{ver}

%define vboxlibdir	%{_libdir}/%{name}
%define vboxdatadir	%{_datadir}/%{name}

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

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
Version:	4.3.0
Release:	3
License:	GPLv2
Group:		Emulators
Url:		http://www.virtualbox.org/
Source0:	http://dlc.sun.com.edgesuite.net/virtualbox/%{version}/%{srcname}.tar.bz2
Source1:	http://dlc.sun.com.edgesuite.net/virtualbox/UserManual.pdf
Source2:	virtualbox.init
Source4:	60-vboxadd.perms
Source100:	virtualbox.rpmlintrc
Patch2:		VirtualBox-4.1.8-kernelrelease.patch
Patch3:		VirtualBox-4.1.8-futex.patch
Patch4:		virtualbox-fix-vboxadd-req.patch
# (fc) 1.6.0-2mdv fix initscript name in VBox.sh script
Patch5:		VirtualBox-4.1.8-initscriptname.patch
# (tmb) disable update notification (OpenSuSe)
# (tmb) TODO: rewrite
#Patch7:		VirtualBox-4.1.8-no-update.patch
# don't check for:
# - mkisofs: we're not going to build the additions .iso file
# - makeself: we're not going to create the stanalone .run installers
Patch9:		VirtualBox-4.1.8-dont-check-for-mkisofs-or-makeself.patch
# (Debian) build X server drivers only for the selected version
# but we're not using the full patch, only the parts we need (e.g. the section
# about Debian Lenny), so we regenerate the patch
Patch10:	VirtualBox-4.3.0-system-xorg.patch

Patch16:	virtualbox-default-to-mandriva.patch
Patch18:	VirtualBox-4.2.12-gsoap-2.8.13.patch

# use courier font instead of beramono for older releases where beramono isn't
# available in tetex-latex (it's available since only tetex-latex-3.0-53mdv2011.0)
#Patch17:	virtualbox-4.0.0-user-courier-instead-of-beramono.patch
#Patch19:	virtualbox-4.1.8-l10n-ru.patch
#Patch20:	VirtualBox-4.2.2-remove-missing-translation.patch

ExclusiveArch:	%{ix86} x86_64
BuildRequires:	dev86
BuildRequires:	dkms-minimal
BuildRequires:	gawk
BuildRequires:	gsoap
BuildRequires:	iasl
BuildRequires:	java-1.7.0-openjdk-devel
BuildRequires:	qt4-linguist
BuildRequires:	xsltproc
BuildRequires:	libcap-devel
BuildRequires:	libstdc++-static-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	pkgconfig(python)
# for now requires full qt4-devel
# as qtcore has been upgraded to qt5
BuildRequires:	qt4-devel
#BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xorg-server) >= 1.13
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(vpx)
%if %{build_doc}
# for building the user manual pdf file
%if %{mdvver} < 201100
BuildRequires:	tetex-latex
%else
BuildRequires:	texlive
BuildRequires:	texlive-fontsextra
%endif
BuildRequires:	docbook-dtd44-xml
%endif

Requires(post,preun,postun): rpm-helper
Requires:	kmod(vboxdrv) = %{version}
Suggests:	%{name}-doc

%description
VirtualBox is a general-purpose full virtualizer for x86 hardware.

%package -n	dkms-%{name}
Summary:	VirtualBox kernel module
Group:		System/Kernel and hardware
Requires(post,preun): dkms
Conflicts:	dkms-vboxadditions < 4.1.8

%description -n dkms-%{name}
Kernel support for VirtualBox.

%if %{build_additions}
%package 	guest-additions
Summary:	Additions for VirtualBox guest systems
Group:		Emulators
Requires:	kmod(vboxguest) = %{version}
Requires:	kmod(vboxsf) = %{version}
Requires:	kmod(vboxvideo) = %{version}
Requires:	x11-driver-video-vboxvideo
Requires(post,preun): rpm-helper

%description    guest-additions
This package contains additions for VirtualBox guest systems.
It allows to share files with the host system and sync time with host.

%package -n	dkms-vboxadditions
Summary:	Kernel module for VirtualBox additions
Group:		System/Kernel and hardware
Requires(post,preun): dkms
Obsoletes:	dkms-vboxadd < %{version}-%{release}
%rename		dkms-vboxvfs
%rename		dkms-vboxsf
%rename		dkms-vboxvideo = %{version}-%{release}
Conflicts:	dkms-%{name} < 4.1.8

%description -n dkms-vboxadditions
Kernel module for VirtualBox additions (ideally only needs to be installed
on the guest OS not on the host OS).

%package -n	x11-driver-video-vboxvideo
Summary:	The X.org driver for video in VirtualBox guests
Group:		System/X11
#Requires:	x11-server-common %%(xserver-sdk-abi-requires videodrv)
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

cat << EOF > LocalConfig.kmk
VBOX_WITH_WARNINGS_AS_ERRORS:=
VBOX_PATH_APP_PRIVATE_ARCH:=%{vboxlibdir}
VBOX_WITH_ORIGIN:=
VBOX_WITH_RUNPATH:=%{vboxlibdir}
VBOX_PATH_APP_PRIVATE:=%{vboxlibdir}
VBOX_WITH_VNC:=1
VBOX_WITH_TESTCASES =
VBOX_WITH_TESTSUITE:=
VBOX_JAVA_HOME := /usr/lib/jvm/java-1.7.0
VBOX_WITHOUT_ADDITIONS_ISO := 1
EOF

%build
# FIXME: gold linker dies with internal error in segment_precedes, at ../../gold/layout.cc:3250
export CC="%{__cc} -fuse-ld=bfd"
export CXX="%{__cxx} -fuse-ld=bfd"
mkdir -p BFD
ln -sf /usr/bin/ld.bfd BFD/ld
export PATH=$PWD/BFD:$PATH
export LIBPATH_LIB="%{_lib}"
./configure \
	--enable-vnc \
	--enable-webservice \
	--disable-kmods \
%if ! %{build_doc}
	--disable-docs
%endif
echo VBOX_GCC_OPT="%{optflags}" >> LocalConfig.kmk
%ifarch %{ix86}
%global ldflags %{ldflags} -fuse-ld=bfd
%endif
echo TOOL_GCC_LDFLAGS="%{ldflags}" >> LocalConfig.kmk

%if !%{build_additions}
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

# install service
mkdir -p %{buildroot}%{_initrddir}
install -m755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

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
# install udev rules
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/%{name}.rules << EOF
KERNEL=="%{kname}", NAME="vboxdrv", OWNER="root", GROUP="root", MODE="0600"
SUBSYSTEM=="usb_device", ACTION=="add", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh \$major \$minor \$attr{bDeviceClass} vboxusers"
SUBSYSTEM=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh \$major \$minor \$attr{bDeviceClass} vboxusers"
SUBSYSTEM=="usb_device", ACTION=="remove", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh --remove \$major \$minor"
SUBSYSTEM=="usb", ACTION=="remove", ENV{DEVTYPE}=="usb_device", RUN+="%{_datadir}/%{name}/VBoxCreateUSBNode.sh --remove \$major \$minor"
EOF
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/vbox-additions.rules << EOF
KERNEL=="vboxguest", NAME="vboxguest", OWNER="root", MODE="0660"
KERNEL=="vboxuser", NAME="vboxuser", OWNER="root", MODE="0666"
EOF

# install additions
%if %{build_additions}
# vboxadd-timesync should probably be renamed vboxadd now, but renaming initscripts
# cleanly is hacky business
install -m755 src/VBox/Additions/linux/installer/vboxadd-service.sh %{buildroot}%{_initrddir}/vboxadd-timesync

# install .fdi file for releases older than 2011.0; and the udev rule and
# 50-vboxmouse.conf for newer releases with Xserver >= 1.9
%if %{mdvver} < 201100
install -D -m644 src/VBox/Additions/linux/installer/90-vboxguest.fdi %{buildroot}%{_datadir}/hal/fdi/policy/20thirdparty/90-vboxguest.fdi
%endif

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
install -m755 src/VBox/Additions/x11/Installer/98vboxadd-xclient %{buildroot}%{_sysconfdir}/X11/xinit.d

pushd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}/sbin %{buildroot}%{_sbindir} %{buildroot}/%{_libdir}/dri
  install -m755 mount.vboxsf %{buildroot}/sbin/mount.vboxsf
  install -m755 VBoxService %{buildroot}%{_sbindir}

  install -m755 VBoxClient %{buildroot}%{_bindir}
  install -m755 VBoxControl %{buildroot}%{_bindir}

  install -m755 VBoxOGL*.so %{buildroot}%{_libdir}
  ln -s -f ../VBoxOGL.so %{buildroot}%{_libdir}/dri/vboxvideo_dri.so

  install -d %{buildroot}%{_sysconfdir}/modprobe.preload.d
  cat > %{buildroot}%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions << EOF
vboxguest
EOF

  install vboxvideo_drv_%{x11_server_majorver}.so -D %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

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
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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
	install -D -m0644 src/VBox/Resources/OSE/virtualbox-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/virtualbox.png
done

for i in 16 20 24 32 40 48 64 72 80 96 128 256 512; do
	install -D -m0644 src/VBox/Resources/other/virtualbox-ova-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-ova.png
	install -D -m0644 src/VBox/Resources/other/virtualbox-ovf-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-ovf.png
	install -D -m0644 src/VBox/Resources/other/virtualbox-vbox-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-vbox.png
	install -D -m0644 src/VBox/Resources/other/virtualbox-vbox-extpack-${i}px.png %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/virtualbox-vbox-extpack.png
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

# install PAM module:
install -D -m755 out/%{vbox_platform}/release/bin/additions/pam_vbox.so %{buildroot}/%{_lib}/security/pam_vbox.so

%post
%_post_service %{name}
%_add_group_helper %{name} 1 vboxusers

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%_del_group_helper %{name} 1 vboxusers

%preun
%_preun_service %{name}

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
%_post_service vboxadd-timesync

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

%preun guest-additions
%_preun_service vboxadd-timesync

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
%{_bindir}/%{oname}
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxTunctl
%{_bindir}/VBoxNetAdpCtl
%{_bindir}/VBoxNetDHCP
%{_bindir}/vboxwebsrv
%{vboxlibdir}/dtrace
%{vboxlibdir}/icons
%{vboxlibdir}/components
%{vboxlibdir}/load.sh
%{vboxlibdir}/loadall.sh
%{vboxlibdir}/*.so
%{vboxlibdir}/*.debug
%{vboxlibdir}/iPxeBaseBin
%{vboxlibdir}/VBoxAutostart
%{vboxlibdir}/VBoxBalloonCtrl
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
%{vboxlibdir}/helpers
%{vboxlibdir}/scripts
%{vboxlibdir}/ExtensionPacks
# this files need proper permission
%attr(4711,root,root) %{vboxlibdir}/VBoxHeadless
%attr(4711,root,root) %{vboxlibdir}/VBoxSDL
%attr(4711,root,root) %{vboxlibdir}/VirtualBox
%attr(4711,root,root) %{vboxlibdir}/VBoxNetAdpCtl
%attr(4711,root,root) %{vboxlibdir}/VBoxNetDHCP
%attr(644,root,root) %{vboxlibdir}/*.gc
%attr(644,root,root) %{vboxlibdir}/*.r0
%exclude %{vboxlibdir}/UserManual.pdf
%{vboxdatadir}
# initscripts integration
%{_initrddir}/%{name}
%config %{_sysconfdir}/udev/rules.d/%{name}.rules
%dir /var/run/%{oname}
# desktop integration
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/mime/packages/virtualbox.xml

%files -n dkms-%{name}
%{_usr}/src/%{name}-%{version}-%{release}

%if %{build_additions}
%files guest-additions
/%{_lib}/security/pam_vbox.so
/sbin/mount.vboxsf
%{_initrddir}/vboxadd-timesync
%{_sbindir}/VBoxService
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_sysconfdir}/udev/rules.d/vbox-additions.rules
%{_sysconfdir}/X11/xinit.d/98vboxadd-xclient
%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions

%files -n x11-driver-video-vboxvideo
%{_libdir}/VBoxOGL*
%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%{_libdir}/dri/vboxvideo_dri.so

%files -n dkms-vboxadditions
%{_usr}/src/vbox*-%{version}-%{release}
%endif

%files doc
%{vboxlibdir}/UserManual.pdf
