
%define ver	1.5.2
%define rel	2
#define svndate	20070209
%define version	%{ver}%{?svndate:.%{svndate}}
%define release	%mkrel %{rel}
%define kname	vboxdrv
%define distname	VirtualBox-%{version}_OSE
%define dirname vbox-ose
%define pkgver	%{ver}%{?svndate:-%{svndate}}

%define vboxdir	%{_libdir}/%{name}

%define build_additions 0

%ifarch %{ix86}
%define vbox_platform linux.x86
%define build_additions 1
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
Source0:	http://virtualbox.org/download/%ver/%distname.tar.bz2
Source1:	virtualbox.run
Source2:	virtualbox.init
Source3:	98vboxadd-xclient
Source4:	60-vboxadd.perms
Source10:	virtualbox.png
Source11:	virtualbox.16.png
Source12:	virtualbox.48.png
Patch0:		VirtualBox-1.5.0_OSE-mdvconfig.patch
Patch1:		VirtualBox-1.5.2_OSE-libpath.patch
Patch2:		VirtualBox-1.5.2_OSE-kernelrelease.patch
# (blino) use misc_register() to register vboxadd device
#         so that /dev/vboxadd gets created automatically by udev
Patch3:		VirtualBox-1.5.0_OSE-misc_register.patch
Patch4:		VirtualBox-OSE-1.4.0-futex.patch
Patch5:		virtualbox-1.5.2-2.6.24.patch
License:	GPL
Group:		Emulators
Url:		http://www.virtualbox.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
Requires(postun): rpm-helper
Requires:	kmod(vboxdrv) = %{version}
Conflicts:	dkms-%{name} <= 1.5.0-%{mkrel 4}
BuildRequires:	dev86, iasl
BuildRequires:	zlib-devel
%if %{mdkversion} >= 200700
BuildRequires:	libxcursor-devel
%else
BuildRequires:	X11-devel
%endif
BuildRequires:	SDL-devel, libqt-devel
BuildRequires:	libIDL-devel, libext2fs-devel
BuildRequires:	libxslt-proc, libxerces-c-devel, libxalan-c-devel >= 1.10
BuildRequires:	hal-devel, libxt-devel, libstdc++-static-devel
BuildRequires:	kernel-source-latest

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
Requires:	kmod(vboxadd)
Requires:	kmod(vboxvfs)
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
%patch0 -p1 -b .mdvconfig
%patch1 -p1 -b .libpath
%patch2 -p1 -b .kernelrelease
%patch3 -p1 -b .misc_register
%patch4 -p1 -b .futex
%patch5 -p1 -b .2.6.24

%build
export LIBPATH_LIB="%{_lib}"
./configure
%if !%{build_additions}
sed -rie 's/(VBOX_WITH_LINUX_ADDITIONS\s+:=\s+).*/\1/' AutoConfig.kmk
%endif

. ./env.sh
kmk %_smp_mflags all

%install
rm -rf $RPM_BUILD_ROOT

# install vbox components
mkdir -p $RPM_BUILD_ROOT%{vboxdir}
(cd out/%{vbox_platform}/release/bin && tar cf - --exclude=additions .) | \
(cd $RPM_BUILD_ROOT%{vboxdir} && tar xf -)

# install service
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# install wrappers
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/vbox
cat > $RPM_BUILD_ROOT%{_sysconfdir}/vbox/vbox.cfg << EOF
# VirtualBox installation directory
INSTALL_DIR="%{vboxdir}"
EOF
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{vboxdir}/vbox-run.sh
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s %{vboxdir}/vbox-run.sh $RPM_BUILD_ROOT%{_bindir}/VirtualBox
ln -s %{vboxdir}/vbox-run.sh $RPM_BUILD_ROOT%{_bindir}/VBoxManage
ln -s %{vboxdir}/vbox-run.sh $RPM_BUILD_ROOT%{_bindir}/VBoxSDL

# install dkms sources
mkdir -p $RPM_BUILD_ROOT%{_usr}/src/%{name}-%{version}-%{release}
mv $RPM_BUILD_ROOT%{vboxdir}/src/* $RPM_BUILD_ROOT%{_usr}/src/%{name}-%{version}-%{release}/
cat > $RPM_BUILD_ROOT%{_usr}/src/%{name}-%{version}-%{release}/dkms.conf << EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/vbox
BUILT_MODULE_NAME[0]=%{kname}
AUTOINSTALL=yes
EOF

# install udev rules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/%{name}.rules << EOF
KERNEL=="%{kname}", MODE="0666"
EOF

# install additions
%if %{build_additions}
install -m755 src/VBox/Additions/linux/installer/vboxadd-timesync.sh $RPM_BUILD_ROOT%{_initrddir}/vboxadd-timesync

pushd out/%{vbox_platform}/release/bin/additions
  install -d $RPM_BUILD_ROOT/sbin $RPM_BUILD_ROOT%{_sbindir}
  install -m755 mountvboxsf $RPM_BUILD_ROOT/sbin/mount.vboxsf
  install -m755 vboxadd-timesync $RPM_BUILD_ROOT%{_sbindir}

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/security/console.perms.d/
  install -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/security/console.perms.d/

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit.d
  install -m755 vboxadd-xclient $RPM_BUILD_ROOT%{_bindir}
  install -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit.d

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.preload.d
  cat > $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions << EOF
vboxadd
vboxvfs
EOF
  install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{input,drivers}
  install vboxmouse_drv_71.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/input/vboxmouse_drv.so
  install vboxvideo_drv_71.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
  for kmod in vboxadd vboxvfs; do
    mkdir -p $RPM_BUILD_ROOT%{_usr}/src/$kmod-%{version}-%{release}
    cp -a src/$kmod/* $RPM_BUILD_ROOT%{_usr}/src/$kmod-%{version}-%{release}/
    cat > $RPM_BUILD_ROOT%{_usr}/src/$kmod-%{version}-%{release}/dkms.conf << EOF
PACKAGE_NAME=$kmod
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/vbox
AUTOINSTALL=yes
EOF
  done
popd
%endif

# install icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
install -m644 %{SOURCE10} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
install -m644 %{SOURCE11} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
install -m644 %{SOURCE12} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# install menu entries
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%{name}): \
 needs="x11" \
 section="More Applications/Emulators" \
 title="VirtualBox OSE" \
 longtitle="Full virtualizer for x86 hardware" \
 command="VirtualBox" \
 icon="%{name}.png"\
 xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=VirtualBox OSE
Comment=Full virtualizer for x86 hardware
Exec=%{_bindir}/VirtualBox
Icon=%{name}.png
Type=Application
Terminal=false
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;
EOF

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{vboxdir}/{src,sdk,testcase}
rm  -f $RPM_BUILD_ROOT%{vboxdir}/tst*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%_post_service %{name}

%postun
%clean_menus
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
%{_bindir}/VirtualBox
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%dir %{vboxdir}
%{vboxdir}/*
# initscripts integration
%{_initrddir}/%{name}
%config %{_sysconfdir}/udev/rules.d/%{name}.rules
# desktop integration
%{_menudir}/%{name}
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
%{_bindir}/vboxadd-xclient
%{_sysconfdir}/security/console.perms.d/60-vboxadd.perms
%{_sysconfdir}/X11/xinit.d/98vboxadd-xclient
%{_sysconfdir}/modprobe.preload.d/vbox-guest-additions

%files -n x11-driver-input-vboxmouse
%defattr(-,root,root)
%{_libdir}/xorg/modules/input/vboxmouse_drv.so

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
