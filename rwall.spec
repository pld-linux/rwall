Summary:	Client and server for sending messages to a host's logged in users.
Name:		rwall
Version:	0.10
Release:	24
Copyright:	BSD
Group:		System Environment/Daemons
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-%{name}-%{version}.tar.gz
Source1:	rwalld.init
Patch0:		netkit-rwall-0.10-misc.patch
Patch1:		netkit-rwalld-0.10-banner.patch
Patch2:		netkit-rwall-install.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rwall command sends a message to all of the users logged into
a specified host.  Actually, your machine's rwall client sends the
message to the rwall daemon running on the specified host, and the
rwall daemon relays the message to all of the users logged in to
that host.  The rwall daemon is run from /etc/inetd.conf and is
disabled by default on Red Hat Linux systems (it can be very annoying
to keep getting all those messages when you're trying to play
Quake--I mean trying to get some work done).

Install rwall if you'd like the ability to send messages to users
logged in to a specified host machine.

%prep
%setup -q -n netkit-rwall-0.10
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make INSTALLROOT=$RPM_BUILD_ROOT install
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rwalld

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rwalld

%postun
if [ $1 = 0 ]; then
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
