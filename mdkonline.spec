%define version 2.77.21
%define name mdkonline
%define subrel 1
%define release %mkrel 4

Summary:	Mandriva Online Update Tool  
Name:		%{name}
Version:	%{version}
Release: 	%{release}
Source0:	%{name}-%{version}.tar.lzma
URL:		http://www.mandrivaonline.com
License:	GPL
Group:		System/Configuration/Other
# for LWP::UserAgent:
Requires:	perl-libwww-perl
%if %mdkversion >= 201000
Requires:   drakxtools-newt => 12.48
Requires: rpmdrake >= 5.11.1
%endif
%if %mdkversion == 200910
Requires:  	drakxtools-newt => 11.88
# for gurpmi.addmedia & update API:
Requires: rpmdrake >= 5.11.1
%endif
%if %mdkversion < 200910
Requires: drakxtools-newt >= 10.4.114
# for gurpmi.addmedia
%if %mdkversion > 200800
Requires: rpmdrake > 4.0
%else
Requires: rpmdrake >= 3.117.8
%endif
%endif
# For adding restricted media:
Requires: perl-Crypt-SSLeay
# for good gurpmi:
%if %mdkversion >= 200910
Requires: urpmi >= 6.17
Requires: gurpmi >= 6.17
%endif
%if %mdkversion == 200900
Requires: urpmi >= 6.14.9
Requires: gurpmi >= 6.14.9
%endif
%if %mdkversion == 200810
Requires: urpmi >= 5.19.9
Requires: gurpmi >= 5.19.9
%endif
%if %mdkversion < 200810
Requires: urpmi >= 4.10.14
Requires: gurpmi >= 4.10.14
%endif
%if %mdkversion > 200800
Requires:   libdrakx-net >= 0.29
%else
Requires:   libdrakx-net >= 0.26
%endif
Provides:   %{name}-backend
Obsoletes:  %{name}-backend
BuildRequires: 	gettext, perl-MDK-Common-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch: 	noarch

%description
The Mandriva Online tool allows users to be kept informed about security
updates, hardware support/enhancements and other high value services.
The package include :
* Update daemon which allows you to install security updates 
  automatically,
* A KDE/Gnome/IceWM compliant applet for security updates notification
  and installation. 

%prep
%setup -q

%build
perl -pi -e 's!my \$ver = 1;!my \$ver = '"'%version-%release'"';!' mdkapplet

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT MANDRIVA_VERSION=%{mandriva_release} install

#symbolic link to drakonline and older path
mkdir -p %buildroot%_prefix/X11R6/bin/

mkdir -p %buildroot%_sysconfdir/cron.daily/
touch %buildroot%_sysconfdir/cron.daily/mdkupdate

%if %mdkversion < 201100
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d
cat > $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/mdkapplet <<EOF
#!/bin/sh
DESKTOP=\$1
case \$DESKTOP in
   IceWM|Fluxbox) exec /usr/bin/mdkapplet;;
esac
EOF

chmod +x $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/mdkapplet
%endif

#install lang
%{find_lang} %{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
cat > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/mandriva-mdvonline.desktop <<EOF
[Desktop Entry]
Name=Mandriva Online Applet
Comment=Applet for Mandriva Online
Exec=%{_bindir}/mdkapplet
Icon=mdkonline
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
X-KDE-autostart-after=kdesktop
EOF

%post
%{update_desktop_database}
%{update_mime_database}

if [ -r /etc/cron.daily/mdkupdate ]; then
  perl -p -i -e 's!/usr/bin/mdkupdate!/usr/sbin/mdkupdate!' /etc/cron.daily/mdkupdate
fi

%postun
%{clean_desktop_database}
%{clean_mime_database}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING 
%{_sbindir}/mdkapplet-config
%{_sbindir}/mdkapplet-*-helper
%{_sbindir}/mdkupdate
%{_bindir}/*
%dir %{_prefix}/lib/libDrakX/drakfirsttime
%{_prefix}/lib/libDrakX/drakfirsttime/*.pm
%{_sysconfdir}/xdg/autostart/mandriva-*.desktop
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%_datadir/mime/packages/*
%_datadir/mimelnk/application/
%{_datadir}/%{name}/pixmaps/*.png
%if %mdkversion < 201100
%_sysconfdir/X11/xinit.d/mdkapplet
%endif
%_sysconfdir/security/console.apps/urpmi.update
%_sysconfdir/pam.d/urpmi.update
%ghost %config(noreplace) %_sysconfdir/cron.daily/mdkupdate
%config(noreplace) %_sysconfdir/sysconfig/mdkapplet


##################################################################
#
#
# !!!!!!!! WARNING => THIS HAS TO BE EDITED IN THE CVS !!!!!!!!!!!
#
#
##################################################################
# get the source from our cvs repository (see
# http://www.mandrivalinux.com/en/cvs.php3)


