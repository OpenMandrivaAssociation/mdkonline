Summary:	Mandriva Online Update Tool  
Name:		mdkonline
Version:	2.78
Release:	1
Source0:	%{name}-%{version}.tar.xz
URL:		http://www.mandrivaonline.com
License:	GPL
Group:		System/Configuration/Other
# for LWP::UserAgent:
Requires:	perl-libwww-perl
Requires: rpmdrake >= 5.11.1

# For adding restricted media:
Requires: perl-Crypt-SSLeay
# for good gurpmi:

Requires: urpmi >= 6.17
Requires: gurpmi >= 6.17
Requires:   libdrakx-net >= 0.29

Provides:   %{name}-backend = %{version}-%{release}
Obsoletes:  %{name}-backend < %{version}-%{release}
BuildRequires:	gettext, perl-MDK-Common-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch

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




%changelog
* Fri Aug 12 2011 Alexander Barakin <abarakin@mandriva.org> 2.77.22-2mdv2011.0
+ Revision: 694254
- Deprecated use of my() in false conditional #63822
