%define name libtasn1
%define version 1.4
%define release %mkrel 2
%define major 3
%define libname %mklibname tasn1_ %major
%define develname %mklibname -d tasn1

Summary: The ASN.1 library used in GNUTLS
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://josefsson.org/gnutls/releases/libtasn1/%{name}-%{version}.tar.gz
License: LGPLv2+
Group: System/Libraries
Url: http://josefsson.org/libtasn1/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot


%description
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%package -n %libname
Summary: The ASN.1 library used in GNUTLS
Group: System/Libraries

%description -n %libname
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%package tools
Summary: Command line ASN.1 tools
Group: Text tools
License: GPLv3+

%description tools
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains the command line tools to work with ASN.1 data.

%package -n %develname
Summary: The ASN.1 library used in GNUTLS
Group: Development/C
Requires: %libname = %version
Provides: %name-devel = %version-%release

%description -n %develname
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%multiarch_binaries %buildroot%_bindir/libtasn1-config

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%post -n %develname
%_install_info %{name}.info
%preun -n %develname
%_remove_install_info %{name}.info


%files tools
%defattr(-,root,root)
%doc NEWS README THANKS
%_bindir/asn*
%_mandir/man1/asn*

%files -n %libname
%defattr(-,root,root)
%_libdir/libtasn1.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%doc AUTHORS ChangeLog
%{multiarch_bindir}/libtasn1-config
%_bindir/libtasn1-config
%_includedir/libtasn1.h
%_libdir/libtasn1.a
%_libdir/libtasn1.la
%_libdir/libtasn1.so
%_libdir/pkgconfig/libtasn1.pc
%_datadir/aclocal/libtasn1.m4
%_infodir/libtasn1.info*
%_mandir/man3/*


