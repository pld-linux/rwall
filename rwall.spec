Summary:	Client for sending messages to a host's logged in users
Summary(es):	Cliente y servidor para enviar mensajes para usuarios en máquinas remotas
Summary(de):	Client zum Senden von Nachrichten an Benutzer am entfernten Host
Summary(fr):	Client pour envoyer des messages aux utilisteurs de machines distantes
Summary(pl):	Klient do wysy³ania komunikatów do zalogowanych u¿ytkowników
Summary(pt_BR):	Cliente e servidor para enviar mensagens para usuários em máquinas remotas
Summary(tr):	Baþka çalýþan tüm kullanýcýlara mesaj gönderme
Name:		rwall
Version:	0.17
Release:	13
License:	BSD
Group:		Networking
Group(de):	Netzwerkwesen
Group(es):	Red
Group(pl):	Sieciowe
Group(pt_BR):	Rede
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	%{name}d.init
Patch0:		netkit-%{name}-WALL_CMD.patch
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rwall command sends a message to all of the users logged into a
specified host. Actually, your machine's rwall client sends the
message to the rwall daemon running on the specified host, and the
rwall daemon relays the message to all of the users logged in to that
host.

%description -l de
Der rwall-Client sendet eine Meldung an einen rwall-Dämon, der auf
einem entfernten Rechner läuft und die Meldung an alle Benutzer der
des entfernten Rechners verbreitet.

%description -l es
El cliente rwall envía un mensaje para un servidor rwall ejecutando
en una máquina remota, que retransmite el mensaje para todos
los usuarios de esta máquina. El servidor rwall es ejecutado por
el inetd (/etc/inetd.conf), y se inhabilita por defecto en los
sistemas.

%description -l fr
Le client rwall envoie un message à un démon rwall tournant sur une
machine distante, qui relaie le message vers tous les utilisateurs de
la machine distante.

%description -l pl
Komenda rwall wysy³a komunikat do wszystkich u¿ytkowników zalogowanych
na okre¶lony komputer. Lokalny klient rwall wysy³a komunikat do
serwera rwall dzia³aj±cego na wybranym komputerze, który to przekazuje
go wszystkim zalogowanym tam u¿ytkownikom.

%description -l pt_BR
O cliente rwall envia uma mensagem para um servidor rwall rodando
numa máquina remota, o qual retransmite a mensagem para todos
os usuários dessa máquina. O servidor rwall é executado pelo inetd
(/etc/inetd.conf), e é desabilitado por default nos sistemas.

%description -l tr
Bir rwall sunucusu kendisine istemci tarafýndan gönderilen bir mesajý
o anda çalýþan tüm kullanýcýlara yansýtýr.

%package -n rwalld
Summary:	Server for sending messages to a host's logged in users
Summary(pl):	Serwer do wysy³ania komunikatów do zalogowanych u¿ytkowników
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Obsoletes:	rwall-server

%description -n rwalld
Server for sending messages to a host's logged in users.

%description -n rwalld -l pl
Serwer do wysy³ania komunikatów do zalogowanych u¿ytkowników.

%prep
%setup -q -n netkit-rwall-%{version}
%patch0 -p1

%build
./configure --installroot=$RPM_BUILD_ROOT
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install MANDIR=%{_mandir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rwalld

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rwalld.8
echo ".so rpc.rwalld.8" > $RPM_BUILD_ROOT%{_mandir}/man8/rwalld.8

%clean
rm -rf $RPM_BUILD_ROOT

%post -n rwalld
/sbin/chkconfig --add rwalld
if [ -f /var/lock/subsys/rwalld ]; then
	/etc/rc.d/init.d/rwalld restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rwalld start\" to start rwalld server" 1>&2
fi
	
%preun -n rwalld
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rwalld ]; then
		/etc/rc.d/init.d/rwalld stop 1>&2
	fi
	/sbin/chkconfig --del rwalld
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rwall
%{_mandir}/man1/rwall.1*

%files -n rwalld
%defattr(644,root,root,755)
%attr(754,root,root) %config /etc/rc.d/init.d/rwalld
%attr(755,root,root) %{_sbindir}/rpc.rwalld
%{_mandir}/man8/rpc.rwalld.8*
%{_mandir}/man8/rwalld.8*
