%define major 6
%define libname %mklibname tasn1_ %{major}
%define devname %mklibname -d tasn1

Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.12
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://josefsson.org/libtasn1/
Source0:	http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	help2man
%ifnarch %armx %mips
BuildRequires:	valgrind
%endif

%description
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

%package -n %{libname}
Summary:	The ASN.1 library used in GNUTLS
Group:		System/Libraries

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
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libtasn1 is an implementation of the ASN.1 standard used by GnuTLS and others.

This contains development files and headers for %{name}.

%prep
%setup -q

%build
%configure \
	--disable-static \
%ifnarch %arm %mips aarch64
	--enable-valgrind-tests
%endif

%make

%check
make check

%install
%makeinstall_std

%files tools
%doc NEWS README THANKS
%{_bindir}/asn*
%{_mandir}/man1/asn*

%files -n %{libname}
%{_libdir}/libtasn1.so.%{major}*

%files -n %{devname}
%doc AUTHORS
%{_includedir}/libtasn1.h
%{_libdir}/libtasn1.so
%{_libdir}/pkgconfig/libtasn1.pc
%{_infodir}/libtasn1.info*
%{_mandir}/man3/*

