Summary:	Client and server for sending messages to a host's logged in users
Summary(de):	Client und Server zum Senden von Nachrichten an Benutzer am entfernten Host
Summary(fr):	Client et serveur pour envoyer des messages aux utilisteurs de machines distantes
Summary(tr):	Baþka bir makinada çalýþan tüm kullanýcýlara mesaj gönderme
Name:		rwall
Version:	0.16
Release:	7
License:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-%{name}-%{version}.tar.gz
Source1:	rwalld.init
Patch0:		netkit-rwall-WALL_CMD.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rwall command sends a message to all of the users logged into a
specified host. Actually, your machine's rwall client sends the
message to the rwall daemon running on the specified host, and the
rwall daemon relays the message to all of the users logged in to that
host. The rwall daemon is run from /etc/inetd.conf and is disabled by
default on Red Hat Linux systems (it can be very annoying to keep
getting all those messages when you're trying to play Quake--I mean
trying to get some work done).

%description -l de
Der rwall-Client sendet eine Meldung an einen rwall-Dämon, der auf
einem entfernten Rechner läuft und die Meldung an alle Benutzer der
des entfernten Rechners verbreitet. Der rwall-Dämon wird von
/etc/inetd.conf betrieben und ist auf Red-Hat-Systemen standardmäßig
deaktiviert.

%description -l fr
Le client rwall envoie un message à un démon rwall tournant sur une
machine distante, qui relaie le message vers tous les utilisateurs de
la machine distante. Le démon rwall est lancé depuis /etc/inetd.conf,
et est desactivé par défaut sur les systèmes Red Hat.

%description -l tr
Bir rwall sunucusu kendisine istemci tarafýndan gönderilen bir mesajý
o anda çalýþan tüm kullanýcýlara yansýtýr. Bu paket hem istemciyi hem
sunucuyu içermektedir ve /etc/inetd.conf'tan çalýþtýrýlmaktadýr.
Öntanýmlý olarak bu hizmet kullaným dýþý býrakýlmýþtýr.

%prep
%setup -q -n netkit-rwall-%{version}
%patch0 -p1

%build
./configure --installroot=$RPM_BUILD_ROOT
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install MANDIR=%{_mandir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rwalld

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rwalld.8
echo ".so rpc.rwalld.8" > $RPM_BUILD_ROOT%{_mandir}/man8/rwalld.8

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rwalld
if [ -f /var/lock/subsys/rwalld ]; then
	/etc/rc.d/init.d/rwalld restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rwalld start\" to start rwalld sever" 1>&2
fi
	
%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rwalld ]; then
		/etc/rc.d/init.d/rwalld stop 1>&2
	fi
	/sbin/chkconfig --del rwalld
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) %config /etc/rc.d/init.d/rwalld
%attr(755,root,root) %{_bindir}/rwall
%attr(755,root,root) %{_sbindir}/rpc.rwalld
%{_mandir}/man8/rpc.rwalld.8*
%{_mandir}/man8/rwalld.8*
%{_mandir}/man1/rwall.1*
