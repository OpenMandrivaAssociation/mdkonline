%define version 2.52.2
%define name mdkonline
%define release %mkrel 1

Summary:	Mandriva Online Update Tool  
Name:		%{name}
Version:	%{version}
Release: 	%{release}
Source0:	%{name}-%{version}.tar.lzma
URL:		http://www.mandrivaonline.com
License:	GPL
Group:		System/Configuration/Other
Requires:  	drakxtools-newt => 10.4.114
# for gurpmi.addmedia:
Requires: rpmdrake > 4.0
# for good gurpmi:
%if %mdkversion >= 200900
Requires: urpmi >= 6.7.1
Requires: gurpmi >= 6.7.1
%elseif %mdkversion >= 200801
Requires: urpmi >= 5.19.5
Requires: gurpmi >= 5.19.5
%else
Requires: urpmi >= 5.9
Requires: gurpmi >= 5.9
%endif
Requires:   libdrakx-net >= 0.29
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
make PREFIX=$RPM_BUILD_ROOT install 

#symbolic link to drakonline and older path
mkdir -p %buildroot%_prefix/X11R6/bin/

mkdir -p %buildroot%_sysconfdir/cron.daily/
touch %buildroot%_sysconfdir/cron.daily/mdkupdate

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d
cat > $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/mdkapplet <<EOF
#!/bin/sh
DESKTOP=\$1
case \$DESKTOP in
   IceWM|Fluxbox|xfce4|LXDE) exec /usr/bin/mdkapplet;;
esac
EOF

chmod +x $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/mdkapplet

#install lang
%{find_lang} %{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/autostart
cat > $RPM_BUILD_ROOT%{_datadir}/autostart/mandriva-mdvonline.desktop <<EOF
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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
cat > $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/mandriva-mdvonline.desktop <<EOF
[Desktop Entry]
Name=Mandriva Online Applet
Comment=Applet for Mandriva Online
Exec=%{_bindir}/mdkapplet
Icon=mdkonline
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF

%post
%{update_desktop_database}
%{update_mime_database}

if [ -r /etc/cron.daily/mdkupdate ]; then
  perl -p -i -e 's!/usr/bin/mdkupdate!/usr/sbin/mdkupdate!' /etc/cron.daily/mdkupdate
fi

%triggerun -- mdkonline < 2.0-11mdk
[[ $2 ]] || exit 0
%{_sbindir}/migrate-mdvonline-applet.pl old &>/dev/null
:

%triggerin -- mdkonline > 2.0-10mdk
[[ $2 ]] || exit 0
%{_sbindir}/migrate-mdvonline-applet.pl new
:

%postun
%{clean_desktop_database}
%{clean_mime_database}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING 
%{_sbindir}/mdkupdate
%{_sbindir}/migrate-mdvonline-applet.pl
%{_bindir}/*
%dir %{_prefix}/lib/libDrakX/drakfirsttime
%{_prefix}/lib/libDrakX/drakfirsttime/*.pm
%{_datadir}/autostart/mandriva-*.desktop
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%_datadir/mime/packages/*
%_datadir/mimelnk/application/
%_datadir/gnome/autostart/mandriva-mdvonline.desktop
%{_datadir}/%{name}/pixmaps/*.png
%_sysconfdir/X11/xinit.d/mdkapplet
%_sysconfdir/security/console.apps/urpmi.removemedia
%_sysconfdir/security/console.apps/urpmi.update
%_sysconfdir/pam.d/urpmi.removemedia
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


