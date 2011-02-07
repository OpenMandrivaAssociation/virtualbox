%define ver	4.0.2
%define rel	2
%define version	%{ver}%{?svndate:.%{svndate}}
%define release	%mkrel %{rel}
%define kname	vboxdrv
%define oname	VirtualBox
%define srcname	%{oname}-%{version}
%define distname	%{oname}-%{version}_OSE
%define dirname vbox-ose
%define pkgver	%{ver}%{?svndate:-%{svndate}}

%define vboxlibdir	%{_libdir}/%{name}
%define vboxdatadir	%{_datadir}/%{name}

%define build_additions 1
%define build_doc 1

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
# (hk) fix build kernel-headers-2.6.29*
Patch10:	VirtualBox-kernel-headers-2.6.29.patch
# (fc) 2.2.0-1mdv disable update notification (Debian)
Patch12:	16-no-update.patch
Patch16:	virtualbox-default-to-mandriva.patch

# use courier font instead of beramono for older releases where beramono isn't
# available in tetex-latex (it's available since only tetex-latex-3.0-53mdv2011.0)
Patch17:	virtualbox-4.0.0-user-courier-instead-of-beramono.patch
# don't check for:
# mkisofs: we're not going to build the additions .iso file
# makeself: we're not going to create the stanalone .run installers
Patch18:	virtualbox-4.0.0-dont-check-for-mkisofs-or-makeself.patch

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
Suggests:	%{name}-doc
BuildRequires:	dev86, iasl
BuildRequires:	zlib-devel
%if %{mdkversion} >= 200700
BuildRequires:	libxcursor-devel
BuildRequires:	libxmu-devel
%else
BuildRequires:	X11-devel
%endif
BuildRequires:	SDL-devel, libqt4-devel >= 4.4.0
BuildRequires:  qt4-linguist
BuildRequires:	libIDL-devel, libext2fs-devel
BuildRequires:	libxslt-proc, libxslt-devel 
BuildRequires:	hal-devel, libxt-devel, libstdc++-static-devel
BuildRequires:  python-devel
BuildRequires:  libcap-devel
BuildRequires:  libxrandr-devel libxinerama-devel
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
BuildRequires:	libpam-devel
BuildRequires:	gawk
BuildRequires:	x11-server-devel
BuildRequires:	java-rpmbuild
%if %build_doc
# for building the user manual pdf file
%if %{mdvver} < 201100
BuildRequires:	tetex-latex
%else
BuildRequires:	tetex-latex >= 3.0-53
%endif
%endif
BuildRequires:	libxslt-devel

%description
VirtualBox Open Source Edition (OSE) is a general-purpose full
virtualizer for x86 hardware.

%package -n	dkms-%{name}
Summary:	VirtualBox OSE kernel module
Group:		System/Kernel and hardware
Requires(post):	  dkms
Requires(preun):  dkms
Conflicts:	dkms-vboxadditions

%description -n dkms-%{name}
Kernel support for VirtualBox OSE.

%if %{build_additions}
%package 	guest-additions
Summary:	Additions for VirtualBox OSE guest systems
Group:		Emulators
%if %{mdkversion} >= 200800
Requires:	kmod(vboxguest)
Requires:	kmod(vboxsf)
Requires:	kmod(vboxvideo)
%else
Requires:	dkms-vboxadditions = %{version}-%{release}
%endif
Requires:	x11-driver-input-vboxmouse
Requires:	x11-driver-video-vboxvideo
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
Provides:	dkms-vboxsf = %{version}-%{release}
Obsoletes:	dkms-vboxsf < %{version}-%{release}
Provides:	dkms-vboxvideo = %{version}-%{release}
Obsoletes:	dkms-vboxvideo < %{version}-%{release}
Conflicts:	dkms-%{name}

%description -n dkms-vboxadditions
Kernel module for VirtualBox OSE additions (ideally only needs to be installed
on the guest OS not on the host OS).

%package -n	x11-driver-input-vboxmouse
Summary:	The X.org driver for mouse in VirtualBox guests
Group:		System/X11
Suggests:	virtualbox-guest-additions
Requires: x11-server-common %(xserver-sdk-abi-requires xinput)

%description -n x11-driver-input-vboxmouse
The X.org driver for mouse in VirtualBox guests

%package -n	x11-driver-video-vboxvideo
Summary:	The X.org driver for video in VirtualBox guests
Group:		System/X11
Suggests:	virtualbox-guest-additions
Conflicts:	virtualbox-guest-additions < 2.2.0-2mdv
Requires: x11-server-common %(xserver-sdk-abi-requires videodrv)


%description -n x11-driver-video-vboxvideo
The X.org driver for video in VirtualBox guests
%endif

%if %build_doc
%package doc
Summary:	The user manual PDF file for %{name}
Group:		System/X11
BuildArch:	noarch

%description doc
This package contains the user manual PDF file for %{name}.
%endif

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .libpath-3.2.6
%patch2 -p1 -b .kernelrelease
%patch4 -p1 -b .futex
%patch5 -p1 -b .fix-timesync-req
%patch6 -p1 -b .initscriptname
%if %{mdkversion} < 200900
%patch7 -p1 -b .mdv20081
%endif
%patch10 -p1 -b .kernel-headers-2.6.29
%patch12 -p1 -b .disable-update
%patch16 -p1 -b .default-to-mandriva

%if %build_doc
%if %{mdvver} < 201100
%patch17 -p1 -b .courier
%endif
%endif

%patch18 -p1 -b .mkisofs-makeself

rm -rf fake-linux/
cp -a $(ls -1dtr /usr/src/linux-* | tail -n 1) fake-linux

cat << EOF > LocalConfig.kmk
VBOX_PATH_APP_PRIVATE_ARCH:=%{vboxlibdir}
VBOX_WITH_ORIGIN:=
VBOX_WITH_RUNPATH:=%{vboxlibdir}
VBOX_PATH_APP_PRIVATE:=%{vboxdatadir}
VBOX_WITH_TESTCASES =
VBOX_WITH_TESTSUITE:=
VBOX_JAVA_HOME := %{java_home}
VBOX_WITHOUT_ADDITIONS_ISO := 1
EOF

%build
#make -C fake-linux prepare
export LIBPATH_LIB="%{_lib}"
./configure --enable-webservice \
 --with-linux=$PWD/fake-linux \
%if %{mdkversion} <= 200800 
 --disable-pulse \
%endif
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
%else
install -m644 src/VBox/Additions/linux/installer/70-xorg-vboxmouse.rules %{buildroot}%{_sysconfdir}/udev/rules.d/
install -D -m644 src/VBox/Additions/x11/Installer/50-vboxmouse.conf %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/50-vboxmouse.conf
%endif

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
install -m755 src/VBox/Additions/x11/Installer/98vboxadd-xclient %{buildroot}%{_sysconfdir}/X11/xinit.d

pushd out/%{vbox_platform}/release/bin/additions
  install -d %{buildroot}/sbin %{buildroot}%{_sbindir} %{buildroot}/%{_libdir}/dri
  install -m755 mount.vboxsf %{buildroot}/sbin/mount.vboxsf
  install -m755 VBoxService %{buildroot}%{_sbindir}

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
vboxguest
EOF
  install -d %{buildroot}%{_libdir}/xorg/modules/{input,drivers}
%if %{mdkversion} >= 200810
  install vboxmouse_drv_%{x11_server_majorver}.so %{buildroot}%{_libdir}/xorg/modules/input/vboxmouse_drv.so
  install vboxvideo_drv_%{x11_server_majorver}.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%else
  install vboxmouse_drv_71.so %{buildroot}%{_libdir}/xorg/modules/input/vboxmouse_drv.so
  %if %{mdkversion} >= 200800
    install vboxvideo_drv_13.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
  %else
    install vboxvideo_drv_71.so %{buildroot}%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
  %endif
%endif
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
  sed 's/^\(.package.*-kernel-\)\(.*-latest\)\(.*\)\\$/\1\2\3Obsoletes: vboxsf-kernel-\2 vboxvideo-kernel-\2\\n\\/' /etc/dkms/template-dkms-mkrpm.spec > %{buildroot}%{_usr}/src/vboxadditions-%{version}-%{release}/vboxadditions-dkms-mkrpm.spec
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

# install PAM module:
install -D -m755 out/%{vbox_platform}/release/bin/additions/pam_vbox.so %{buildroot}/%{_lib}/security/pam_vbox.so

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
%if %build_doc
%exclude %{vboxlibdir}/UserManual.pdf
%endif
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
/%{_lib}/security/pam_vbox.so
/sbin/mount.vboxsf
%{_initrddir}/vboxadd-timesync
%{_sbindir}/VBoxService
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%if %{mdkversion} <= 200910
%{_sysconfdir}/security/console.perms.d/60-vboxadd.perms
%endif
%{_sysconfdir}/udev/rules.d/vbox-additions.rules
%{_sysconfdir}/X11/xinit.d/98vboxadd-xclient
%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions

%files -n x11-driver-input-vboxmouse
%defattr(-,root,root)
%{_libdir}/xorg/modules/input/vboxmouse_drv.so
%if %{mdvver} < 201100
%{_datadir}/hal/fdi/policy/20thirdparty/90-vboxguest.fdi
%else
%{_sysconfdir}/udev/rules.d/70-xorg-vboxmouse.rules
%{_sysconfdir}/X11/xorg.conf.d/50-vboxmouse.conf
%endif

%files -n x11-driver-video-vboxvideo
%defattr(-,root,root)
%{_libdir}/VBoxOGL*
%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%{_libdir}/dri/vboxvideo_dri.so

%files -n dkms-vboxadditions
%defattr(-,root,root)
%{_usr}/src/vbox*-%{version}-%{release}

%endif

%if %build_doc
%files doc
%defattr(-,root,root)
%{vboxlibdir}/UserManual.pdf
%endif
