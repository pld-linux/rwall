Summary: Client and server for sending messages to a host's logged in users.
Name: rwall
Version: 0.10
Release: 22
Copyright: BSD
Group: System Environment/Daemons
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rwall-0.10.tar.gz
Source1: rwalld.init
Patch: netkit-rwall-0.10-misc.patch
Patch1: netkit-rwalld-0.10-banner.patch
Prereq: /sbin/chkconfig
Buildroot: /var/tmp/%{name}-root

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
%setup -n netkit-rwall-0.10
%patch -p1
%patch1 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
make INSTALLROOT=$RPM_BUILD_ROOT install
install -m 755 $RPM_SOURCE_DIR/rwalld.init $RPM_BUILD_ROOT/etc/rc.d/init.d/rwalld

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rwalld

%postun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rwalld
fi

%files
%defattr(-,root,root)
/usr/sbin/rpc.rwalld
/usr/man/man8/rpc.rwalld.8
/usr/man/man8/rwalld.8
/usr/bin/rwall
/usr/man/man1/rwall.1
%config /etc/rc.d/init.d/rwalld
