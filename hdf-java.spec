Summary:	Java HDF5 Object Package
Name:		hdf-java
Version:	2.6
Release:	%mkrel 1
License:	BSD-like
Group:		Development/Java
Url:		http://www.hdfgroup.org/
Source0:	http://www.hdfgroup.org/ftp/HDF5/hdf-java/src/hdf-java-2.6-src.tar.bz2
Patch0:		hdf-java-2.6-not-writable-fix.patch
Patch1:		hdf-java-2.6-use-shared-libraries.patch
Patch2:		hdf-java-2.6-optflags.patch
Patch3:		hdf-java-2.6-installdirs.patch
BuildRequires:  java-rpmbuild
BuildRequires:	java-devel-openjdk
BuildRequires:	classpath-devel
BuildRequires:	hdf5-devel
BuildRequires:	HDF-devel
BuildRequires:	HDF
BuildRequires:	netcdf-devel
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
BuildConflicts:	libgcj-devel
Requires:	HDF
Requires:	libhdf5
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This Java package implements HDF5 data objects in an 
object-oriented form.

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

export JAVA_HOME="%{java_home}"
export COPT="%{optflags}"
sed -i -e 's|LDOPT=-G|LDOPT=-g|g' -e 's|COPT=-G|COPT=-g|g' -e 's|LDOPT=-shared|"LDOPT=-g -shared"|g' -e 's|COPT=-shared|COPT="-shared  -fPIC"|g' configure*
find . -name 'Makefile.in' | xargs sed -i -e 's|CFLAGS =|CFLAGS +=|g'
find . -name 'Makefile.in' | xargs sed -i -e 's|LDOPT=|LDOPT+=|g'
find . -name 'Makefile.in' | xargs sed -i -e 's|COPT=|COPT+=|g'

autoreconf -fiv

%configure2_5x \
	--with-jdk=%{java_home}/include,%{java_home}/lib \
	--with-javabin=%{java_home}/bin  \
	--with-libz=yes,%{_libdir}  \
	--with-libjpeg=yes,%{_libdir}   \
	--with-hdf5=yes,%{_libdir} \
	--with-hdf4=yes,%{_libdir}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std
rm -rf %{buildroot}%{_docdir}/hdf-java

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Readme.txt docs/*
%{_bindir}/hdfview.sh
%{_datadir}/java/*.jar
%{_datadir}/java/ext/*.jar
%{_datadir}/java/*.so
