Summary:	Mandriva Online Update Tool  
Name:		mdkonline
Version:	2.78
Release:	2
License:	GPLv2+
Group:		System/Configuration/Other
Url:		http://www.openmandriva.org/
Source0:	%{name}-%{version}.tar.xz
Patch0:		mdkonline-2.78-new-url.patch
BuildArch:	noarch
BuildRequires:	gettext
BuildRequires:	perl-MDK-Common-devel
# for LWP::UserAgent:
Requires:	perl-libwww-perl
Requires:	rpmdrake >= 5.11.1

# For adding restricted media:
Requires:	perl-Crypt-SSLeay
# for good gurpmi:

Requires:	urpmi >= 6.17
Requires:	gurpmi >= 6.17
Requires:	libdrakx-net >= 0.29
%rename		%{name}-backend

%description
The OpenMandriva Online tool allows users to be kept informed about security
updates, hardware support/enhancements and other high value services.
The package include :
* Update daemon which allows you to install security updates 
  automatically,
* A KDE/Gnome/IceWM compliant applet for security updates notification
  and installation. 

%prep
%setup -q
%apply_patches

%build
perl -pi -e 's!my \$ver = 1;!my \$ver = '"'%{version}-%{release}'"';!' mdkapplet

%install
make PREFIX=%{buildroot} MANDRIVA_VERSION=%{distepoch} install


mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
touch %{buildroot}%{_sysconfdir}/cron.daily/mdkupdate

#install lang
%find_lang %{name}

mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
cat > %{buildroot}%{_sysconfdir}/xdg/autostart/mandriva-mdvonline.desktop <<EOF
[Desktop Entry]
Name=OpenMandriva Online Applet
Comment=Applet for OpenMandriva Online
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
%{_datadir}/mime/packages/*
%{_datadir}/mimelnk/application/
%{_datadir}/%{name}/pixmaps/*.png
%{_sysconfdir}/security/console.apps/urpmi.update
%{_sysconfdir}/pam.d/urpmi.update
%ghost %config(noreplace) %{_sysconfdir}/cron.daily/mdkupdate
%config(noreplace) %{_sysconfdir}/sysconfig/mdkapplet

