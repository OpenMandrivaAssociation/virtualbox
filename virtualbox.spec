%define ver	3.1.2
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

%define vboxlibdir	%{_libdir}/%{name}
%define vboxdatadir	%{_datadir}/%{name}

%define build_additions 1

%ifarch %{ix86}
%define vbox_platform linux.x86
%endif
%ifarch x86_64
%define vbox_platform linux.amd64
%endif

# nuke vbox-specific dependencies
%define _provides_exceptions ^VBox
%define _requires_exceptions ^VBox

Summary:	A general-purpose full virtualizer for x86 hardware
Name:		virtualbox
Version:	%{version}
Release:	%{release}
Source0:	http://download.virtualbox.org/virtualbox/%ver/%{srcname}.tar.bz2
Source2:	virtualbox.init
Source4:	60-vboxadd.perms
Source10:	virtualbox.png
Source11:	virtualbox.16.png
Source12:	virtualbox.48.png
Patch1:		VirtualBox-libpath.patch
Patch2:		VirtualBox-1.5.6_OSE-kernelrelease.patch
Patch4:		VirtualBox-1.6.0_OSE-futex.patch
Patch5:		virtualbox-fix-vboxadd-req.patch
# (fc) 1.6.0-2mdv fix initscript name in VBox.sh script
Patch6:		VirtualBox-1.6.0_OSE-initscriptname.patch
# (fc) 2.0.0-2mdv fix QT4 detection on x86-64 on Mdv 2008.1
Patch7:		VirtualBox-2.0.0-mdv20081.patch
# (fc) 2.0.2-2mdv disable version check at startup
Patch8:		VirtualBox-disableversioncheck.patch
# (hk) fix build kernel-headers-2.6.29*
Patch10:	VirtualBox-kernel-headers-2.6.29.patch
# (fc) 2.2.0-1mdv add Wine Direct3D guest additions option (Debian)
Patch11:	15-wined3d-guest-addition.patch
# (fc) 2.2.0-1mdv disable update notification (Debian)
Patch12:	16-no-update.patch
Patch14:	vbox-pulse-rewrite-0.1.patch

License:	GPLv2
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
BuildRequires:	libxslt-proc, libxslt-devel 
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
BuildRequires:  mesaglu-devel mesagl-devel libxmu-devel
BuildRequires:  gsoap
BuildRequires:	openssl-devel
BuildRequires:	curl-devel
BuildRequires:	dkms-minimal

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
Requires:	kmod(vboxguest)
Requires:	kmod(vboxvfs)
Requires:	kmod(vboxvideo)
%else
Requires:	dkms-vboxadditions = %{version}-%{release}
%endif
Requires:	x11-driver-input-vboxmouse
Requires:	x11-driver-video-vboxvideo
Requires:	xrandr
Requires:	xrefresh
Requires(post):   rpm-helper
Requires(preun):  rpm-helper

%description    guest-additions
This packages contains additions for VirtualBox OSE guest systems.
It allows to share files with the host system, copy/paste between
guest and host, and sync time with host.

%package -n	dkms-vboxadditions
Summary:	Kernel module for VirtualBox OSE additions
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(preun):  dkms
Obsoletes:	dkms-vboxadd < %{version}-%{release}
Provides:	dkms-vboxvfs = %{version}-%{release}
Obsoletes:	dkms-vboxvfs < %{version}-%{release}
Provides:	dkms-vboxvideo = %{version}-%{release}
Obsoletes:	dkms-vboxvideo < %{version}-%{release}

%description -n dkms-vboxadditions
Kernel module for VirtualBox OSE additions.

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
Conflicts:	virtualbox-guest-additions < 2.2.0-2mdv

%description -n x11-driver-video-vboxvideo
The X.org driver for video in VirtualBox guests
%endif

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .libpath-3.1
%patch2 -p1 -b .kernelrelease
%patch4 -p1 -b .futex
%patch5 -p1 -b .fix-timesync-req
%patch6 -p1 -b .initscriptname
%if %{mdkversion} < 200900
%patch7 -p1 -b .mdv20081
%endif
%patch8 -p1 -b .versioncheck
%patch10 -p1 -b .kernel-headers-2.6.29
%patch11 -p1 -b .wined3d
%patch12 -p1 -b .disable-update
%patch14 -p1 -b .pulse-rewrite

rm -rf fake-linux/
cp -a $(ls -1dtr /usr/src/linux-* | tail -n 1) fake-linux

cat << EOF > LocalConfig.kmk
VBOX_PATH_APP_PRIVATE_ARCH:=%{vboxlibdir}
VBOX_WITH_ORIGIN:=
VBOX_WITH_RUNPATH:=%{vboxlibdir}
VBOX_PATH_APP_PRIVATE:=%{vboxdatadir}
VBOX_WITH_TESTCASE:=
VBOX_WITH_TESTSUITE:=
EOF

%build
#make -C fake-linux prepare
export LIBPATH_LIB="%{_lib}"
./configure --enable-webservice \
 --with-linux=$PWD/fake-linux \
%if %{mdkversion} <= 200800 
 --disable-pulse
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

# move VBoxTunctl to bindir
mv %{buildroot}%{vboxlibdir}/VBoxTunctl %{buildroot}%{_bindir}/

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
KERNEL=="%{kname}", MODE="0666"
EOF
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/vbox-additions.rules << EOF
KERNEL=="vboxguest|vboxuser", ENV{ACL_MANAGE}="1"
EOF

# install additions
%if %{build_additions}
mkdir -p %{buildroot}%{_datadir}/hal/fdi/policy/20thirdparty
# vboxadd-timesync should probably be renamed vboxadd now, but renaming initscripts
# cleanly is hacky business
install -m755 src/VBox/Additions/linux/installer/vboxadd-service.sh %{buildroot}%{_initrddir}/vboxadd-timesync
install -m755 src/VBox/Additions/x11/Installer/VBoxRandR.sh %{buildroot}%{_bindir}/VBoxRandR
install -m755 src/VBox/Additions/linux/installer/90-vboxguest.fdi %{buildroot}%{_datadir}/hal/fdi/policy/20thirdparty/90-vboxguest.fdi

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
install -m755 src/VBox/Additions/x11/Installer/98vboxadd-xclient %{buildroot}%{_sysconfdir}/X11/xinit.d

pushd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}/sbin %{buildroot}%{_sbindir} %{buildroot}/%{_libdir}/dri
  install -m755 mount.vboxsf %{buildroot}/sbin/mount.vboxsf
  install -m755 VBoxService %{buildroot}%{_sbindir}/vboxadd-service

%if %{mdkversion} <= 200910
  install -d %{buildroot}%{_sysconfdir}/security/console.perms.d/
  install -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/security/console.perms.d/
%endif

  install -m755 VBoxClient %{buildroot}%{_bindir}
  install -m755 VBoxControl %{buildroot}%{_bindir}

  install -m755 VBoxOGL*.so %{buildroot}%{_libdir}
  ln -s -f ../VBoxOGL.so %{buildroot}%{_libdir}/dri/vboxvideo_dri.so

  install -d %{buildroot}%{_sysconfdir}/modprobe.preload.d
  cat > %{buildroot}%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions << EOF
vboxadd
vboxvfs
EOF
  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}
%if %{mdkversion} >= 201010
 install vboxmouse_drv_17.so %{buildroot}%{_libdir}/xorg/modules/input/vboxmouse_drv.so
 install vboxvideo_drv_17.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%else
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
%endif
  mkdir -p %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}
  cat > %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/dkms.conf << EOF
PACKAGE_NAME=vboxadditions
PACKAGE_VERSION=%{version}-%{release}
MAKE[0]="make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxguest &&
cp \$dkms_tree/\$module/\$module_version/build/vboxguest/Module.symvers \$dkms_tree/\$module/\$module_version/build/vboxvfs &&
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxvfs &&
cp \$dkms_tree/\$module/\$module_version/build/vboxvfs/Module.symvers \$dkms_tree/\$module/\$module_version/build/vboxvideo &&
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxvideo"
EOF
  i=0
  for kmod in vboxguest vboxvfs vboxvideo; do
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
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxvfs clean && 
make -C \$kernel_source_dir M=\$dkms_tree/\$module/\$module_version/build/vboxvideo clean "
AUTOINSTALL=yes
EOF
popd
  sed 's/^\(.package.*-kernel-\)\(.*-latest\)\(.*\)\\$/\1\2\3Obsoletes: vboxvfs-kernel-\2 vboxvideo-kernel-\2\\n\\/' /etc/dkms/template-dkms-mkrpm.spec > %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/vboxadditions-dkms-mkrpm.spec
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
rm -rf %{buildroot}%{vboxlibdir}/{src,sdk,testcase}
rm  -f %{buildroot}%{vboxlibdir}/tst*
rm  -f %{buildroot}%{vboxlibdir}/vboxkeyboard.tar.gz
rm  -f %{buildroot}%{vboxlibdir}/SUP*
rm  -f %{buildroot}%{vboxlibdir}/xpidl

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
%{vboxlibdir}
%attr(4711,root,root) %{vboxlibdir}/VBoxHeadless
%attr(4711,root,root) %{vboxlibdir}/VBoxSDL
%attr(4711,root,root) %{vboxlibdir}/VirtualBox
%attr(4711,root,root) %{vboxlibdir}/VBoxNetAdpCtl
%attr(4711,root,root) %{vboxlibdir}/VBoxNetDHCP
%attr(644,root,root) %{vboxlibdir}/*.gc
%attr(644,root,root) %{vboxlibdir}/*.r0
%{vboxdatadir}
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
%{_usr}/src/%{name}-%{version}-%{release}

%if %{build_additions}
%files guest-additions
%defattr(-,root,root)
/sbin/mount.vboxsf
%{_initrddir}/vboxadd-timesync
%{_sbindir}/vboxadd-service
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_bindir}/VBoxRandR
%if %{mdkversion} <= 200910
%{_sysconfdir}/security/console.perms.d/60-vboxadd.perms
%endif
%{_sysconfdir}/udev/rules.d/vbox-additions.rules
%{_sysconfdir}/X11/xinit.d/98vboxadd-xclient
%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions

%files -n x11-driver-input-vboxmouse
%defattr(-,root,root)
%{_libdir}/xorg/modules/input/vboxmouse_drv.so
%{_datadir}/hal/fdi/policy/20thirdparty/90-vboxguest.fdi

%files -n x11-driver-video-vboxvideo
%defattr(-,root,root)
%{_libdir}/VBoxOGL*
%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%{_libdir}/dri/vboxvideo_dri.so

%files -n dkms-vboxadditions
%defattr(-,root,root)
%{_usr}/src/vbox*-%{version}-%{release}

%endif
