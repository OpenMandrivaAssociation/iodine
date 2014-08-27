# define to %{nil} for release builds
%define beta rc1

Name:           iodine
Version:        0.6.0
%if "%beta" != ""
Release:        0.%{beta}.1
%else
Release:        1
%endif
Summary:        Tunnel IP over DNS NULL request
Group:          Networking/Other
License:        BSD
URL:            http://code.kryo.se/iodine/
Source0:        http://code.kryo.se/iodine/%{name}-%{version}%{?beta:-}%{beta}.tar.gz
Source1:        iodine.service
Source2:        iodine.conf
Source3:        iodined.service
Source4:        iodined.conf
BuildRequires: zlib-devel

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
%setup -qn %{name}-%{version}%{?beta:-}%{beta}

%build
%make prefix=%{_prefix}

%install
%makeinstall
mkdir -p %{buildroot}/%{_unitdir}/service
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
install -m 0755 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -m 0755 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -m 0755 %{SOURCE3} %{buildroot}/%{_unitdir}/%{name}d.service
install -m 0755 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}d

# this is a hack so we can bypass ifplugd that try to run dhcp on the 
# newly created interface
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts
echo -e '#!/bin/bash\nexit 0\n' > %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts/ifup-dns

%pre server
%_pre_useradd %{name}d /var/empty /sbin/nologin

%post server
%systemd_post %{name}d.service

%preun server
%systemd_preun %{name}d.service

%postun server
%_postun_userdel %{name}d
%systemd_postun_with_restart %{name}d.service


%pre client
%_pre_useradd %{name} /var/empty /sbin/nologin

%post client
%systemd_post %{name}.service

%preun client
%systemd_preun %{name}.service

%postun client
%_postun_userdel %{name}
%systemd_postun_with_restart %{name}.service

%files common
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/sysconfig/network-scripts/ifup-dns

%files server
%doc README 
%{_sbindir}/%{name}d
%{_unitdir}/%{name}d.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}d

%files client
%doc README 
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man8/%{name}.*
