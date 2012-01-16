%define kname  vboxdrv
%define oname  VirtualBox
%define srcname        %{oname}-%{version}
%define distname       %{oname}-%{version}_OSE
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
%define _provides_exceptions ^VBox
%define _requires_exceptions ^VBox

%define x11_server_majorver %(pkg-config --modversion xorg-server|awk -F. '{print $1$2}')

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
Version:	4.1.8
Release:	%mkrel 1
Source0:	http://download.virtualbox.org/virtualbox/%ver/%{srcname}.tar.bz2
Source1:	http://download.virtualbox.org/virtualbox/UserManual.pdf
Source2:	virtualbox.init
Source4:	60-vboxadd.perms
Patch1:		VirtualBox-libpath.patch
Patch2:		VirtualBox-4.0.6_OSE-kernelrelease.patch
Patch3:		virtualbox-4.0.6-bccpath.patch
Patch4:		VirtualBox-1.6.0_OSE-futex.patch
Patch5:		virtualbox-fix-vboxadd-req.patch
# (fc) 1.6.0-2mdv fix initscript name in VBox.sh script
Patch6:		VirtualBox-1.6.0_OSE-initscriptname.patch
# (fc) 2.0.0-2mdv fix QT4 detection on x86-64 on Mdv 2008.1
Patch7:		VirtualBox-2.0.0-mdv20081.patch
# (hk) fix build kernel-headers-2.6.29*
Patch10:	VirtualBox-kernel-headers-2.6.29.patch
# (fc) 2.2.0-1mdv disable update notification (Debian)
Patch12:	virtualbox-4.1.8-no-update.patch
Patch16:	virtualbox-default-to-mandriva.patch


# use courier font instead of beramono for older releases where beramono isn't
# available in tetex-latex (it's available since only tetex-latex-3.0-53mdv2011.0)
Patch17:	virtualbox-4.0.0-user-courier-instead-of-beramono.patch
# don't check for:
# mkisofs: we're not going to build the additions .iso file
# makeself: we're not going to create the stanalone .run installers
Patch18:	virtualbox-4.0.0-dont-check-for-mkisofs-or-makeself.patch
Patch19:	virtualbox-4.1.6-l10n-ru.patch

License:	GPLv2
Group:		Emulators
Url:		http://www.virtualbox.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
Requires(postun): rpm-helper
Requires:	kmod(vboxdrv) = %{version}
Conflicts:	dkms-%{name} <= 1.5.0-%{mkrel 4}
Suggests:	%{name}-doc
BuildRequires:	dev86, iasl
BuildRequires:	zlib-devel
BuildRequires:	libxcursor-devel
BuildRequires:	libxmu-devel
BuildRequires:	SDL-devel, libqt4-devel >= 4.4.0
BuildRequires:  qt4-linguist
BuildRequires:	libIDL-devel, pkgconfig(ext2fs)
BuildRequires:	libxslt-proc, libxslt-devel
BuildRequires:	hal-devel, libxt-devel, libstdc++-static-devel
BuildRequires:  python-devel
BuildRequires:  libcap-devel
BuildRequires:  libxrandr-devel libxinerama-devel
BuildRequires:	pulseaudio-devel
BuildRequires:  mesaglu-devel mesagl-devel libxmu-devel
BuildRequires:  gsoap
BuildRequires:	openssl-devel
BuildRequires:	curl-devel
BuildRequires:	dkms-minimal
BuildRequires:	pam-devel
BuildRequires:	gawk
BuildRequires:	x11-server-devel
BuildRequires:	java-rpmbuild
BuildRequires:  libvncserver-devel
%if %build_doc
# for building the user manual pdf file
%if %{mdvver} < 201100
BuildRequires:	tetex-latex
%else
BuildRequires:	texlive
BuildRequires:	texlive-fontsextra
%endif
BuildRequires:	docbook-dtd44-xml
%endif
BuildRequires:	libxslt-devel

%description
VirtualBox is a general-purpose full virtualizer for x86 hardware.

%package -n	dkms-%{name}
Summary:	VirtualBox kernel module
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(preun):  dkms
Conflicts:	dkms-vboxadditions

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
Requires(post):   rpm-helper
Requires(preun):  rpm-helper

%description    guest-additions
This package contains additions for VirtualBox guest systems.
It allows to share files with the host system and sync time with host.

%package -n	dkms-vboxadditions
Summary:	Kernel module for VirtualBox additions
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(preun):  dkms
Obsoletes:	dkms-vboxadd < %{version}-%{release}
Provides:	dkms-vboxvfs = %{version}-%{release}
Obsoletes:	dkms-vboxvfs < %{version}-%{release}
Provides:	dkms-vboxsf = %{version}-%{release}
Obsoletes:	dkms-vboxsf < %{version}-%{release}
Provides:	dkms-vboxvideo = %{version}-%{release}
Obsoletes:	dkms-vboxvideo < %{version}-%{release}
Conflicts:	dkms-%{name}

%description -n dkms-vboxadditions
Kernel module for VirtualBox additions (ideally only needs to be installed
on the guest OS not on the host OS).

%package -n	x11-driver-video-vboxvideo
Summary:	The X.org driver for video in VirtualBox guests
Group:		System/X11
Suggests:	virtualbox-guest-additions
Conflicts:	virtualbox-guest-additions < 2.2.0-2mdv
Requires: x11-server-common %(xserver-sdk-abi-requires videodrv)


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
%patch1 -p1 -b .libpath-3.2.6
%patch2 -p1 -b .kernelrelease
%patch3 -p1 -b .bccpath
%patch4 -p1 -b .futex
%patch5 -p1 -b .fix-timesync-req
%patch6 -p1 -b .initscriptname
%patch10 -p1 -b .kernel-headers-2.6.29
%patch12 -p1 -b .disable-update
%patch16 -p1 -b .default-to-mandriva

%if %build_doc
%if %{mdvver} < 201100
%patch17 -p1 -b .courier
%endif
%endif

%patch18 -p1 -b .mkisofs-makeself

# FBH: temporarly disabled due to conflicts with virtualbox 4.1.8
# integration.
#%patch19 -p1 -b .l10n-ru

cat << EOF > LocalConfig.kmk
VBOX_WITH_WARNINGS_AS_ERRORS:=
VBOX_PATH_APP_PRIVATE_ARCH:=%{vboxlibdir}
VBOX_WITH_ORIGIN:=
VBOX_WITH_RUNPATH:=%{vboxlibdir}
VBOX_PATH_APP_PRIVATE:=%{vboxdatadir}
VBOX_WITH_VNC:=1
VBOX_WITH_TESTCASES =
VBOX_WITH_TESTSUITE:=
VBOX_JAVA_HOME := %{java_home}
VBOX_WITHOUT_ADDITIONS_ISO := 1
EOF

%build
export LIBPATH_LIB="%{_lib}"
./configure --enable-webservice --disable-kmods \
%if ! %build_doc
  --disable-docs
%endif

%if !%{build_additions}
sed -rie 's/(VBOX_WITH_LINUX_ADDITIONS\s+:=\s+).*/\1/' AutoConfig.kmk
echo VBOX_WITHOUT_ADDITIONS=1 >> LocalConfig.kmk
%endif

. ./env.sh
kmk %_smp_mflags all

%install
rm -rf %{buildroot}

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
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/%{name}.rules << EOF
KERNEL=="%{kname}", MODE="0600"
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

  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}
  install vboxvideo_drv_%{x11_server_majorver}.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

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

%if !%build_doc
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

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

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
%defattr(-,root,root)
%config %{_sysconfdir}/vbox/vbox.cfg
%{_bindir}/%{oname}
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxTunctl
%{_bindir}/VBoxNetAdpCtl
%{_bindir}/VBoxNetDHCP
%{_bindir}/vboxwebsrv
%{vboxlibdir}
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
%defattr(-,root,root)
%{_usr}/src/%{name}-%{version}-%{release}

%if %{build_additions}
%files guest-additions
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_libdir}/VBoxOGL*
%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%{_libdir}/dri/vboxvideo_dri.so

%files -n dkms-vboxadditions
%defattr(-,root,root)
%{_usr}/src/vbox*-%{version}-%{release}

%endif

%files doc
%defattr(-,root,root)
%{vboxlibdir}/UserManual.pdf
