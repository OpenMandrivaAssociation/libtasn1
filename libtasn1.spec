# libtasn1 is used by gnutls, gnutls is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 6
%define oldlibname %mklibname tasn1_ 6
%define libname %mklibname tasn1
%define devname %mklibname -d tasn1
%define sdevname %mklibname -d -s tasn1
%define lib32name %mklib32name tasn1_ %{major}
%define dev32name %mklib32name -d tasn1
%define sdev32name %mklib32name -d -s tasn1

Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.20.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://josefsson.org/libtasn1/
Source0:	http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/libtasn1/blob/master/f/libtasn1-3.4-rpath.patch
#Patch1:		libtasn1-4.18.0-clang.patch
BuildRequires:	bison
BuildRequires:	help2man
BuildRequires:	hostname
BuildRequires:	slibtool
%ifnarch %{armx} %mips %{riscv}
BuildRequires:	valgrind
%endif
%if %{with compat32}
BuildRequires:	libc6
%endif
BuildSystem:	autotools
BuildOption:	--enable-static

%description
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%package -n %{libname}
Summary:	The ASN.1 library used in GNUTLS
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%package tools
Summary:	Command line ASN.1 tools
Group:		Text tools
License:	GPLv3+

%description tools
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains the command line tools to work with ASN.1 data.

%package -n %{devname}
Summary:	The ASN.1 development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains development files and headers for %{name}.

%package -n %{sdevname}
Summary:	The ASN.1 static library
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	tasn1-static-devel = %{EVRD}

%description -n %{sdevname}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains development the static library for %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	The ASN.1 library used in GNUTLS (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%package -n %{dev32name}
Summary:	The ASN.1 development files (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains development files and headers for %{name}.

%package -n %{sdev32name}
Summary:	The ASN.1 static library (32-bit)
Group:		Development/C
Requires:	%{dev32name} = %{version}-%{release}

%description -n %{sdev32name}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains the static library for %{name}.
%endif

%prep -a
# Force regenerate autotools files so they
# don't hardcode "automake-1.16" references
# when we have automake 1.17
slibtoolize --force
aclocal -I m4 -I src/gl/m4
automake -a
autoconf

%check
# (tpg) https://gitlab.com/gnutls/libtasn1/issues/9
make -C _OMV_rpm_build check ||:
[ -e tests/test-suite.log ] && cat tests/test-suite.log || :
[ -e fuzz/test-suite.log ] && cat fuzz/test-suite.log || :

%files tools
%doc NEWS THANKS
%{_bindir}/asn*
%doc %{_mandir}/man1/asn*

%files -n %{libname}
%{_libdir}/libtasn1.so.%{major}*

%files -n %{devname}
%doc AUTHORS
%{_includedir}/libtasn1.h
%{_libdir}/libtasn1.so
%{_libdir}/pkgconfig/libtasn1.pc
%doc %{_infodir}/libtasn1.info*
%doc %{_mandir}/man3/*

%files -n %{sdevname}
%{_libdir}/libtasn1.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libtasn1.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libtasn1.so
%{_prefix}/lib/pkgconfig/libtasn1.pc

%files -n %{sdev32name}
%{_prefix}/lib/libtasn1.a
%endif
