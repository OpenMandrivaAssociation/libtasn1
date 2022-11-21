# libtasn1 is used by gnutls, gnutls is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 6
%define libname %mklibname tasn1_ %{major}
%define devname %mklibname -d tasn1
%define sdevname %mklibname -d -s tasn1
%define lib32name %mklib32name tasn1_ %{major}
%define dev32name %mklib32name -d tasn1
%define sdev32name %mklib32name -d -s tasn1

Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.19.0
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://josefsson.org/libtasn1/
Source0:	http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/libtasn1/blob/master/f/libtasn1-3.4-rpath.patch
Patch1:		libtasn1-4.18.0-clang.patch
BuildRequires:	bison
BuildRequires:	help2man
BuildRequires:	hostname
%ifnarch %{armx} %mips %{riscv}
BuildRequires:	valgrind
%endif
%if %{with compat32}
BuildRequires:	libc6
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

%prep
%autosetup -p1

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-static
# libtasn1 likes to regenerate docs
touch doc/stamp_docs
cd ..
%endif

mkdir build
cd build
%configure \
	--enable-static \
%ifnarch %{armx} %{mips} %{riscv}
	--enable-valgrind-tests
%endif
# libtasn1 likes to regenerate docs
touch doc/stamp_docs

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%check
# (tpg) https://gitlab.com/gnutls/libtasn1/issues/9
make -C build check ||:
[ -e tests/test-suite.log ] && cat tests/test-suite.log || :
[ -e fuzz/test-suite.log ] && cat fuzz/test-suite.log || :

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

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
