%define version 2.18
%define name mdkonline
%define release %mkrel 1

Summary:	Mandriva Online Update Tool  
Name:		%{name}
Version:	%{version}
Release: 	%{release}
Source0:	%{name}-%{version}.tar.bz2
URL:		http://www.mandrivaonline.com
License:	GPL
Group:		System/Configuration/Other
Requires:  	drakxtools-newt => 10.4.114, perl-Gtk2-TrayIcon >= 0.03-3mdk, perl-Crypt-SSLeay >= 0.51-2mdk
# we need wget for authenticated media:
Requires: wget
# for gurpmi.addmedia:
Requires: rpmdrake > 2.20-3.1.20060mdk
# for good gurpmi:
Requires: urpmi > 4.7.15-1.2.20060mdk
Provides:   %{name}-backend
Obsoletes:  %{name}-backend
Requires:	hwdb-clients >= 0.15.1-1mdk
BuildRequires: 	gettext, perl-MDK-Common-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch: 	noarch

%description
The Mandriva Online tool is designed for registered users 
who want to upload their configuration (packages, hardware infos). 
This allows them to be kept informed about security updates, 
hardware support/enhancements and other high value services.
The package include :
* Wizard for users registration and configuration uploads, 
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
#ln -sf %_sbindir/mdkonline %buildroot%_sbindir/drakclub
ln -sf %_sbindir/mdkonline %buildroot%_sbindir/drakonline
ln -sf %_sbindir/mdkonline %buildroot%_prefix/X11R6/bin/mdkonline

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d
cat > $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/mdkapplet <<EOF
#!/bin/sh
DESKTOP=\$1
case \$DESKTOP in
   IceWM|Fluxbox|xfce4) exec /usr/bin/mdkapplet;;
esac
EOF

chmod +x $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/mdkapplet

#install lang
%{find_lang} %{name}

#install menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): needs="x11" command="%{_sbindir}/%{name}" section="System" icon="mdkonline.png" title="Mandriva Online" longtitle="Wizard for update service subscription" xdg="true"
?package(%{name}): command="%{_sbindir}/mdkupdate --bundle" needs="x11" kde_opt="InitialPreference=15" section="Configuration/Other" mimetypes="application/x-mdv-exec" title="Mandriva Online Bundle" longtitle="Mandriva Linux bundle handler" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-mdvonline.desktop <<EOF
[Desktop Entry]
Name=Mandriva Online
Comment=Wizard for update service subscription
Exec=%{_sbindir}/%{name}
Icon=mdkonline.png
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
NoDisplay=true
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/autostart
cat > $RPM_BUILD_ROOT%{_datadir}/autostart/mandriva-mdvonline.desktop <<EOF
[Desktop Entry]
Name=Mandriva Online Applet
Comment=Applet for Mandriva Online
Exec=%{_bindir}/mdkapplet
Icon=mdkonline.png
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
Icon=mdkonline.png
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF

%post
%{update_desktop_database}
%{update_mime_database}
%{update_menus}

if [ -r /etc/cron.daily/mdkupdate ]; then
  perl -p -i -e 's!/usr/bin/mdkupdate!/usr/sbin/mdkupdate!' /etc/cron.daily/mdkupdate
fi

%triggerun -- mdkonline < 2.0-11mdk
[[ $2 ]] || exit 0
%{_sbindir}/migrate-mdvonline-applet.pl old
:

%triggerin -- mdkonline > 2.0-10mdk
[[ $2 ]] || exit 0
%{_sbindir}/migrate-mdvonline-applet.pl new
:

%postun
%{clean_menus}
%{clean_desktop_database}
%{clean_mime_database}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING 
%{_sbindir}/mdkupdate
%{_sbindir}/mdkonline
%{_sbindir}/migrate-mdvonline-applet.pl
%{_sbindir}/drakonline
%{_bindir}/*
%{_prefix}/X11R6/bin/*
%dir %{_prefix}/lib/libDrakX/drakfirsttime
%{_prefix}/lib/libDrakX/drakfirsttime/*.pm
%{_menudir}/%{name}
%{_datadir}/autostart/mandriva-*.desktop
%{_datadir}/applications/mandriva-*.desktop
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%_datadir/mime/packages/*
%_datadir/mimelnk/applications/
%_datadir/gnome/autostart/mandriva-mdvonline.desktop
%{_datadir}/%{name}/pixmaps/*.png
%_sysconfdir/X11/xinit.d/mdkapplet
%_sysconfdir/security/console.apps/urpmi.update
%_sysconfdir/pam.d/urpmi.update


##################################################################
#
#
# !!!!!!!! WARNING => THIS HAS TO BE EDITED IN THE CVS !!!!!!!!!!!
#
#
##################################################################
# get the source from our cvs repository (see
# http://www.mandrivalinux.com/en/cvs.php3)


