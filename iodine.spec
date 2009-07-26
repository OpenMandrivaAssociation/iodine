%define name	iodine
%define version	0.5.2
%define release	%mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Tunnel IP over DNS NULL request 
Group:		Networking/Other
License:	BSD
URL:		http://code.kryo.se/iodine/
Source0:	%{name}-%{version}.tar.gz
Source1: 	iodine.init
Source2: 	iodine.conf
Source3: 	iodined.init
Source4: 	iodined.conf
# sent upstream : http://dev.kryo.se/iodine/ticket/70
Patch0:     iodine-0.5.2-pidfile.diff

BuildRoot:	%{_tmppath}/%{name}-root

%description
odine lets you tunnel IPv4 data through a DNS server. This can be usable in 
different situations where internet access is firewalled, but DNS queries 
are allowed.

The bandwidth is asymmetrical with limited upstream and up to 1 Mbit/s 
downstream.

Compared to other DNS tunnel implementations, iodine offers:

 * Higher performance
    iodine uses the NULL type that allows the downstream data to be sent 
    without encoding. Each DNS reply can contain over a kilobyte of compressed 
    payload data.
 * Portability
    iodine runs on many different UNIX-like systems as well as on Win32. 
    Tunnels can be set up between two hosts no matter their endianness or 
    operating system.
 * Security
    iodine uses challenge-response login secured by MD5 hash. It also 
    filters out any packets not coming from the IP used when logging in.
 * Less setup
    iodine handles setting IP number on interfaces automatically, and up 
    to 16 users can share one server at the same time. Packet size is 
    automatically probed for maximum downstream throughput. 


%package	client
Summary:	Iodine client (Tunnel IP over DNS)
Group:		Networking/Other
Requires:   %{name}-common

%description	client
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in 
different situations where internet access is firewalled, but DNS queries 
are allowed. 

This package contains the client part.

%package	server
Summary:	Iodine server (Tunnel IP over DNS)
Group:		Networking/Other
Requires:   %{name}-common

%description	server
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in 
different situations where internet access is firewalled, but DNS queries 
are allowed. 


This package contains the server part.

%package	common
Summary:	Iodine common part (Tunnel IP over DNS)
Group:		Networking/Other

%description    common
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in 
different situations where internet access is firewalled, but DNS queries 
are allowed. 


This package contains some script shared between server and client.


%prep
%setup -q 
%patch0 -p0

%build
%make


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT/%_initrddir/
mkdir -p $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/
install -m 0755 %SOURCE1 $RPM_BUILD_ROOT/%_initrddir/%{name}
install -m 0755 %SOURCE2 $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/%{name}
install -m 0755 %SOURCE3 $RPM_BUILD_ROOT/%_initrddir/%{name}d
install -m 0755 %SOURCE4 $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/%{name}d

# this is a hack so we can bypass ifplugd that try to run dhcp on the 
# newly created interface
mkdir -p $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/network-scripts
echo -e '#!/bin/bash\nexit 0\n' > $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/network-scripts/ifup-dns
%clean
rm -rf $RPM_BUILD_ROOT

%pre server
%_pre_useradd %{name}d /var/empty /bin/bash

%post server
%_post_service %{name}d

%preun server
%_preun_service %{name}d

%postun server
%_postun_userdel %{name}d


%pre client
%_pre_useradd %{name} /var/empty /bin/bash

%post client
%_post_service %{name}

%preun client
%_preun_service %{name}

%postun client
%_postun_userdel %{name}

%files common
%defattr(-,root,root)
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/sysconfig/network-scripts/ifup-dns

%files server
%defattr(-,root,root)
%doc README 
%{_sbindir}/%{name}d
%{_initrddir}/%{name}d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}d

%files client
%defattr(-,root,root)
%doc README 
%{_sbindir}/%{name}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%_mandir/man8/%{name}.*

