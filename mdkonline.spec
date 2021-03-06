summary:	%{vendor} Online Update Tool
Name:		mdkonline
Version:	3.11.0
Release:	1
License:	GPLv2+
Group:		System/Configuration/Other
Url:		https://github.com/OpenMandrivaSoftware/mdkonline
Source0:	%{name}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
BuildArch:	noarch
BuildRequires:	gettext
BuildRequires:	perl-MDK-Common-devel
# for LWP::UserAgent:
Requires:	perl(LWP::UserAgent)
Requires:	rpmdrake >= 5.11.1
Requires:	drakxtools-curses >= 16.0
# for gurpmi.addmedia & update API:
Requires:       rpmdrake
# For adding restricted media:
Requires:	perl(Crypt::SSLeay)
# for good gurpmi:

Requires:	urpmi >= 7.5
Requires:	gurpmi
Requires:	libdrakx-net >= 2.6
Requires:       typelib(AppIndicator3)

%rename		%{name}-backend
BuildRequires:	gettext perl-MDK-Common-devel
BuildRequires:	intltool
BuildArch:	noarch

%description
The %{vendor} Online tool allows users to be kept informed about
security updates, hardware support/enhancements and other high
value services.
The package includes :
* Update daemon which allows you to install security updates 
  automatically,
* A KDE/Gnome/IceWM compliant applet for security updates notification
  and installation. 

%prep
%setup -q
%autopatch -p1

%build
perl -pi -e 's!my \$ver = 1;!my \$ver = '"'%{version}-%{release}'"';!' mdkapplet

%install
make PREFIX=%{buildroot} MANDRIVA_VERSION=%{distepoch} install


mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
touch %{buildroot}%{_sysconfdir}/cron.daily/mdkupdate

mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit.d
cat > %{buildroot}%{_sysconfdir}/X11/xinit.d/mdkapplet <<EOF
#!/bin/sh
DESKTOP=\$1
case \$DESKTOP in
   IceWM|Fluxbox) exec /usr/bin/mdkapplet;;
esac
EOF

#install lang
%find_lang %{name}

mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
cat > %{buildroot}%{_sysconfdir}/xdg/autostart/omvonline.desktop <<EOF
[Desktop Entry]
Name=%{vendor} Online Applet
Comment=Applet for %{vendor} Online
Exec=mdkapplet
Icon=mdkonline
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
X-KDE-autostart-after=kdesktop
EOF

%post
if [ -r /etc/cron.daily/mdkupdate ]; then
  perl -p -i -e 's!/usr/bin/mdkupdate!/usr/sbin/mdkupdate!' /etc/cron.daily/mdkupdate
fi

%files -f %{name}.lang
%{_bindir}/mdkapplet
%{_bindir}/mdkapplet-config
%{_bindir}/mdkapplet-update-checker
%{_bindir}/mdkapplet-upgrade-helper
%{_bindir}/mdkupdate
%{_bindir}/urpmi.update
%{_libexecdir}/mdkapplet-config
%{_libexecdir}/mdkapplet-upgrade-helper
%{_libexecdir}/mdkupdate
%{_datadir}/polkit-1/actions/*.policy
%dir %{_prefix}/lib/libDrakX/drakfirsttime
%{_prefix}/lib/libDrakX/drakfirsttime/*.pm
%{_sysconfdir}/xdg/autostart/*.desktop
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/mime/packages
%{_datadir}/mimelnk/application
%{_datadir}/%{name}/pixmaps
%{_sysconfdir}/X11/xinit.d/mdkapplet
%ghost %config(noreplace) %{_sysconfdir}/cron.daily/mdkupdate
%config(noreplace) %{_sysconfdir}/sysconfig/mdkapplet
