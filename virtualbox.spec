%define ver	2.1.4
%define rel	5
#define svndate	20070209
%define version	%{ver}%{?svndate:.%{svndate}}
%define release	%mkrel %{rel}
%define kname	vboxdrv
%define oname	VirtualBox
%define srcname	%{oname}-%{version}-OSE
%define distname	%{oname}-%{version}_OSE
%define dirname vbox-ose
%define pkgver	%{ver}%{?svndate:-%{svndate}}

%define vboxdir	%{_libdir}/%{name}

%define build_additions 1

%ifarch %{ix86}
%define vbox_platform linux.x86
%endif
%ifarch x86_64
%define vbox_platform linux.amd64
%endif

# remove me for versions > 1.6.4
%define broken_tunctl 0

# nuke vbox-specific dependencies
%define _provides_exceptions ^VBox
%define _requires_exceptions ^VBox

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
Version:	%{version}
Release:	%{release}
Source0:	http://download.virtualbox.org/virtualbox/%ver/%{srcname}.tar.bz2
Source2:	virtualbox.init
Source3:	98vboxadd-xclient
Source4:	60-vboxadd.perms
Source10:	virtualbox.png
Source11:	virtualbox.16.png
Source12:	virtualbox.48.png
Patch1:		VirtualBox-2.1.2-libpath.patch
Patch2:		VirtualBox-1.5.6_OSE-kernelrelease.patch
Patch4:		VirtualBox-1.6.0_OSE-futex.patch
Patch5:		VirtualBox-1.6.2_OSE-fix-timesync-req.patch
# (fc) 1.6.0-2mdv fix initscript name in VBox.sh script
Patch6:		VirtualBox-1.6.0_OSE-initscriptname.patch
# (fc) 2.0.0-2mdv fix QT4 detection on x86-64 on Mdv 2008.1
Patch7:		VirtualBox-2.0.0-mdv20081.patch
# (fc) 2.0.2-2mdv disable version check at startup
Patch8:		VirtualBox-2.0.0-disableversioncheck.patch
# (hk) https://qa.mandriva.com/show_bug.cgi?id=48096
Patch9:		VirtualBox-2.1.4_OSE-vbox_use_insert_page.patch
# (hk) fix build kernel-headers-2.6.29*
Patch10:	VirtualBox-2.1.4_OSE-kernel-headers-2.6.29.patch
License:	GPL
Group:		Emulators
Url:		http://www.virtualbox.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
Requires(postun): rpm-helper
%if %{mdkversion} >= 200800
Requires:	kmod(vboxdrv) = %{version}
%else
Requires:	dkms-%{name} = %{version}-%{release}
%endif
%if %{broken_tunctl}
Requires:	tunctl
%endif
Conflicts:	dkms-%{name} <= 1.5.0-%{mkrel 4}
BuildRequires:	dev86, iasl
BuildRequires:	zlib-devel
%if %{mdkversion} >= 200700
BuildRequires:	libxcursor-devel
BuildRequires:	libxmu-devel
%else
BuildRequires:	X11-devel
%endif
BuildRequires:	SDL-devel, libqt4-devel
BuildRequires:  qt4-linguist
BuildRequires:	libIDL-devel, libext2fs-devel
BuildRequires:	libxslt-proc, libxslt-devel, libxerces-c-devel, libxalan-c-devel >= 1.10
BuildRequires:	hal-devel, libxt-devel, libstdc++-static-devel
BuildRequires:  python-devel
BuildRequires:  libcap-devel
%if %{mdkversion} >= 200810
BuildRequires:	pulseaudio-devel
%endif
%if %{mdkversion} >= 200800
BuildRequires:	kernel-devel-latest
%else
BuildRequires:	kernel-source
%endif
%if %{mdkversion} >= 200900
BuildRequires:	gcc4.2
%endif

%description
VirtualBox Open Source Edition (OSE) is a general-purpose full
virtualizer for x86 hardware.

%package -n	dkms-%{name}
Summary:	VirtualBox OSE kernel module
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(preun):  dkms

%description -n dkms-%{name}
Kernel support for VirtualBox OSE.

%if %{build_additions}
%package 	guest-additions
Summary:	Additions for VirtualBox OSE guest systems
Group:		Emulators
%if %{mdkversion} >= 200800
Requires:	kmod(vboxadd)
Requires:	kmod(vboxvfs)
%else
Requires:	dkms-vboxadd = %{version}-%{release}
Requires:	dkms-vboxvfs = %{version}-%{release}
%endif
Requires:	x11-driver-input-vboxmouse
Requires:	x11-driver-video-vboxvideo
Requires(post):   rpm-helper
Requires(preun):  rpm-helper

%description    guest-additions
This packages contains additions for VirtualBox OSE guest systems.
It allows to share files with the host system, copy/paste between
guest and host, and sync time with host.

%package -n	dkms-vboxadd
Summary:	Kernel module for VirtualBox OSE additions
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(preun):  dkms

%description -n dkms-vboxadd
Kernel module for VirtualBox OSE additions.

%package -n	dkms-vboxvfs
Summary:	Kernel module for VirtualBox OSE VFS
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(post):	dkms-vboxadd = %{version}-%{release}
Requires(preun):  dkms

%description -n dkms-vboxvfs
Kernel module for VirtualBox OSE VFS.

%package -n	x11-driver-input-vboxmouse
Summary:	The X.org driver for mouse in VirtualBox guests
Group:		System/X11
Suggests:	virtualbox-guest-additions

%description -n x11-driver-input-vboxmouse
The X.org driver for mouse in VirtualBox guests

%package -n	x11-driver-video-vboxvideo
Summary:	The X.org driver for video in VirtualBox guests
Group:		System/X11
Suggests:	virtualbox-guest-additions

%description -n x11-driver-video-vboxvideo
The X.org driver for video in VirtualBox guests
%endif

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .libpath
%patch2 -p1 -b .kernelrelease
%patch4 -p1 -b .futex
%patch5 -p1 -b .fix-timesync-req
%patch6 -p1 -b .initscriptname
%if %{mdkversion} < 200900
%patch7 -p1 -b .mdv20081
%endif
%patch8 -p1 -b .versioncheck
%patch9 -p1 -b .vbox_use_insert_page
%patch10 -p1 -b .kernel-headers-2.6.29

%if %{broken_tunctl}
# 1.6.4 build fix (OSE tarball is missing Makefile.kmk files)
# by building tunctl:
#   svn cat http://virtualbox.org/svn/vbox/trunk/src/apps/Makefile.kmk > src/apps/Makefile.kmk
#   svn cat http://virtualbox.org/svn/vbox/trunk/src/apps/tunctl/Makefile.kmk > src/apps/tunctl/Makefile.kmk
#   sed -ie s/SUB_DEPTH/DEPTH/ src/apps/Makefile.kmk
# by removing tunctl
if [ -e src/apps ]; then
   [ -e src/apps/Makefile.kmk ] && exit 1
   rm -rf src/apps
fi
# remove this block and broken_tunctl hack when updating to > 1.6.4
%endif

rm -rf fake-linux/
cp -a $(ls -1dtr /usr/src/linux-* | tail -n 1) fake-linux

%build
make -C fake-linux prepare
export LIBPATH_LIB="%{_lib}"
%if %{mdkversion} >= 200900
 CC="%{_bindir}/gcc4.2" \
%endif
./configure --disable-qt3 \
 --with-linux=$PWD/fake-linux \
%if %{mdkversion} <= 200800 
 --disable-pulse
%endif

%if !%{build_additions}
sed -rie 's/(VBOX_WITH_LINUX_ADDITIONS\s+:=\s+).*/\1/' AutoConfig.kmk
echo VBOX_WITHOUT_ADDITIONS=1 > LocalConfig.kmk
%endif

. ./env.sh
kmk %_smp_mflags all

%install
rm -rf %{buildroot}

# install vbox components
mkdir -p %{buildroot}%{vboxdir}
(cd out/%{vbox_platform}/release/bin && tar cf - --exclude=additions .) | \
(cd %{buildroot}%{vboxdir} && tar xf -)

# install service
mkdir -p %{buildroot}%{_initrddir}
install -m755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

# install wrappers
mkdir -p %{buildroot}%{_sysconfdir}/vbox
cat > %{buildroot}%{_sysconfdir}/vbox/vbox.cfg << EOF
# VirtualBox installation directory
INSTALL_DIR="%{vboxdir}"
EOF
mkdir -p %{buildroot}%{_bindir}
ln -s %{vboxdir}/VBox.sh %{buildroot}%{_bindir}/%{oname}
ln -s %{vboxdir}/VBox.sh %{buildroot}%{_bindir}/VBoxManage
ln -s %{vboxdir}/VBox.sh %{buildroot}%{_bindir}/VBoxSDL
ln -s %{vboxdir}/VBox.sh %{buildroot}%{_bindir}/VBoxHeadless

%if %{broken_tunctl}
ln -sf tunctl %{buildroot}%{_bindir}/VBoxTunctl
%else
# move VBoxTunctl to bindir
mv %{buildroot}%{vboxdir}/VBoxTunctl %{buildroot}%{_bindir}/
%endif

install -d %{buildroot}/var/run/%{oname}

# install dkms sources
mkdir -p %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}
cat > vboxbuild << EOF
#!/bin/sh
set -e
droot=\$(pwd)
cd \$droot/%{kname}
make KERN_DIR=\$1
cp -f \$droot/%{kname}/Module.symvers \$droot/vboxnetflt
cd \$droot/vboxnetflt
make KERN_DIR=\$1
EOF
install -m 0755 vboxbuild %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}
mv %{buildroot}%{vboxdir}/src/* %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/
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
AUTOINSTALL=yes
EOF

# install udev rules
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/%{name}.rules << EOF
KERNEL=="%{kname}", MODE="0666"
EOF

# install additions
%if %{build_additions}
mkdir -p %{buildroot}%{_datadir}/hal/fdi/information/20thirdparty
install -m755 src/VBox/Additions/linux/installer/vboxadd-timesync.sh %{buildroot}%{_initrddir}/vboxadd-timesync
install -m755 src/VBox/Additions/x11/installer/VBoxRandR.sh %{buildroot}%{_bindir}/VBoxRandR
install -m755 src/VBox/Additions/linux/installer/90-vboxguest.fdi %{buildroot}%{_datadir}/hal/fdi/information/20thirdparty/90-vboxguest.fdi

pushd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}/sbin %{buildroot}%{_sbindir}
  install -m755 mountvboxsf %{buildroot}/sbin/mount.vboxsf
  install -m755 vboxadd-timesync %{buildroot}%{_sbindir}

  install -d %{buildroot}%{_sysconfdir}/security/console.perms.d/
  install -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/security/console.perms.d/

  install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
  install -m755 VBoxClient %{buildroot}%{_bindir}
  install -m755 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xinit.d

  install -d %{buildroot}%{_sysconfdir}/modprobe.preload.d
  cat > %{buildroot}%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions << EOF
vboxadd
vboxvfs
EOF
  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}
%if %{mdkversion} >= 200910
  install vboxmouse_drv_16.so %{buildroot}%{_libdir}/xorg/modules/input/vboxmouse_drv.so
  install vboxvideo_drv_16.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%else
 %if %{mdkversion} >= 200810
  install vboxmouse_drv_14.so %{buildroot}%{_libdir}/xorg/modules/input/vboxmouse_drv.so
  install vboxvideo_drv_14.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
 %else
  install vboxmouse_drv_71.so %{buildroot}%{_libdir}/xorg/modules/input/vboxmouse_drv.so
  %if %{mdkversion} >= 200800
   install vboxvideo_drv_13.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
  %else
   install vboxvideo_drv_71.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
  %endif
 %endif
%endif
  for kmod in vboxadd vboxvfs; do
    mkdir -p %{buildroot}%{_usr}/src/$kmod-%{version}-%{release}
    cp -a src/$kmod/* %{buildroot}%{_usr}/src/$kmod-%{version}-%{release}/
    cat > %{buildroot}%{_usr}/src/$kmod-%{version}-%{release}/dkms.conf << EOF
PACKAGE_NAME=$kmod
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/vbox
AUTOINSTALL=yes
EOF
  done
popd
%endif

# install icons
mkdir -p %{buildroot}%{_iconsdir}
install -m644 %{SOURCE10} %{buildroot}%{_iconsdir}/%{name}.png
mkdir -p %{buildroot}%{_miconsdir}
install -m644 %{SOURCE11} %{buildroot}%{_miconsdir}/%{name}.png
mkdir -p %{buildroot}%{_liconsdir}
install -m644 %{SOURCE12} %{buildroot}%{_liconsdir}/%{name}.png

# install menu entries

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=VirtualBox OSE
Comment=Full virtualizer for x86 hardware
Exec=%{_bindir}/%{oname}
Icon=%{name}
Type=Application
Terminal=false
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;
EOF

# add missing makefile for kernel module
install -m644 src/VBox/HostDrivers/Support/linux/Makefile %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/

# remove unpackaged files
rm -rf %{buildroot}%{vboxdir}/{src,sdk,testcase}
rm  -f %{buildroot}%{vboxdir}/tst*

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%update_menus
%endif
%_post_service %{name}

%postun
%if %mdkversion < 200900
%clean_menus
%endif
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%preun
%_preun_service %{name}

%post -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{name} -v %{version}-%{release}
/sbin/modprobe %{kname} >/dev/null 2>&1 || :

%preun -n dkms-%{name}
# rmmod can fail
/sbin/rmmod %{kname} >/dev/null 2>&1
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{name} -v %{version}-%{release} --all || :

%if %{build_additions}
%post guest-additions
%_post_service vboxadd-timesync

%preun guest-additions
%_preun_service vboxadd-timesync

%post -n dkms-vboxadd
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m vboxadd -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m vboxadd -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m vboxadd -v %{version}-%{release}
:

%preun -n dkms-vboxadd
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m vboxadd -v %{version}-%{release} --all
:

%post -n dkms-vboxvfs
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m vboxvfs -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m vboxvfs -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m vboxvfs -v %{version}-%{release}
:

%preun -n dkms-vboxvfs
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m vboxvfs -v %{version}-%{release} --all
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
%dir %{vboxdir}
%{vboxdir}/*
%attr(4711,root,root) %{vboxdir}/VBoxHeadless
%attr(4711,root,root) %{vboxdir}/VBoxSDL
%attr(4711,root,root) %{vboxdir}/VirtualBox
# initscripts integration
%{_initrddir}/%{name}
%config %{_sysconfdir}/udev/rules.d/%{name}.rules
%dir /var/run/%{oname}
# desktop integration
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/applications/mandriva-%{name}.desktop

%files -n dkms-%{name}
%defattr(-,root,root)
%dir %{_usr}/src/%{name}-%{version}-%{release}
%{_usr}/src/%{name}-%{version}-%{release}/*

%if %{build_additions}
%files guest-additions
%defattr(-,root,root)
/sbin/mount.vboxsf
%{_initrddir}/vboxadd-timesync
%{_sbindir}/vboxadd-timesync
%{_bindir}/VBoxClient
%{_bindir}/VBoxRandR
%{_sysconfdir}/security/console.perms.d/60-vboxadd.perms
%{_sysconfdir}/X11/xinit.d/98vboxadd-xclient
%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions

%files -n x11-driver-input-vboxmouse
%defattr(-,root,root)
%{_libdir}/xorg/modules/input/vboxmouse_drv.so
%{_datadir}/hal/fdi/information/20thirdparty/90-vboxguest.fdi

%files -n x11-driver-video-vboxvideo
%defattr(-,root,root)
%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

%files -n dkms-vboxadd
%defattr(-,root,root)
%dir %{_usr}/src/vboxadd-%{version}-%{release}
%{_usr}/src/vboxadd-%{version}-%{release}/*

%files -n dkms-vboxvfs
%defattr(-,root,root)
%dir %{_usr}/src/vboxvfs-%{version}-%{release}
%{_usr}/src/vboxvfs-%{version}-%{release}/*
%endif
