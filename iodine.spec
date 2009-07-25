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
BuildRoot:	%{_tmppath}/%{name}-root

%description

%package	client
Summary:	Iodine client (Tunnel IP over DNS)
Group:		Networking/Other

%description	client
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in 
different situations where internet access is firewalled, but DNS queries 
are allowed. 

This package contains the client part.

%package	server
Summary:	Iodine server (Tunnel IP over DNS)
Group:		Networking/Other

%description	server
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in 
different situations where internet access is firewalled, but DNS queries 
are allowed. 


This package contains the server part.

%prep
%setup -q 

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

%clean
rm -rf $RPM_BUILD_ROOT

%post server
%_post_service %{name}d

%preun server
%_preun_service %{name}d

%post client
%_post_service %{name}

%preun client
%_preun_service %{name}

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

