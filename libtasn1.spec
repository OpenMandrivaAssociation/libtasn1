%define major 6
%define libname %mklibname tasn1_ %{major}
%define devname %mklibname -d tasn1
%ifnarch %{riscv}
%global optflags %{optflags} --rtlib=compiler-rt
%endif

Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.15.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://josefsson.org/libtasn1/
Source0:	http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
Patch0:		libtasn1-4.13-check-for-__builtin_mul_overflow_p.patch
Patch1:		https://src.fedoraproject.org/rpms/libtasn1/blob/master/f/libtasn1-3.4-rpath.patch
BuildRequires:	bison
BuildRequires:	help2man
BuildRequires:	hostname
%ifnarch %armx %mips %{riscv}
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
%autosetup -p1

%build
%configure \
	--disable-static \
%ifnarch %arm %mips aarch64
	--enable-valgrind-tests
%endif

# libtasn1 likes to regenerate docs
touch doc/stamp_docs

%make_build

%check
# (tpg) https://gitlab.com/gnutls/libtasn1/issues/9
make check ||:
[ -e tests/test-suite.log ] && cat tests/test-suite.log && exit 0
[ -e fuzz/test-suite.log ] && cat fuzz/test-suite.log && exit 0

%install
%make_install

%files tools
%doc NEWS THANKS
%{_bindir}/asn*
%{_bindir}/corpus2array
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
