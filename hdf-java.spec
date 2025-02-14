Summary:	Java HDF5 Object Package
Name:		hdf-java
Version:	2.6.1
Release:	9
License:	BSD-like
Group:		Development/Java
Url:		https://www.hdfgroup.org/
# http://www.hdfgroup.org/ftp/HDF5/hdf-java/src/hdf-java-2.6.1-src.tar
Source0:	hdf-java-2.6.1-src.tar.xz
Patch0:		hdf-java-2.6-not-writable-fix.patch
Patch1:		hdf-java-2.6-use-shared-libraries.patch
Patch2:		hdf-java-2.6-optflags.patch
Patch3:		hdf-java-2.6-installdirs.patch
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel-openjdk
BuildRequires:	classpath-devel
BuildRequires:	hdf-util
BuildRequires:	hdf-devel
BuildRequires:	hdf5-devel
BuildRequires:	netcdf-devel
BuildRequires:	jpeg-devel
BuildRequires:	zlib-devel
BuildConflicts:	libgcj-devel
Requires:	hdf-util
Requires:	hdf5

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
%define _disable_lto 1
export JAVA_HOME="%{java_home}"
export COPT="%{optflags}"

sed -i -e 's|LDOPT=-G|LDOPT=-g|g' \
    -e 's|COPT=-G|COPT=-g|g' -e 's|LDOPT=-shared|LDOPT="-g -shared"|g' \
    -e 's|COPT=-shared|COPT="-shared  -fPIC"|g' -e 's|x86_64-pc-linux|x86_64-*-linux|g' \
    -e 's|x86_64-pc|x86_64-*|g' configure*

#(tpg) make it work
sed -i -e 's|x86_64-pc|x86_64-*|g' Config/config.sub
find . -name 'Makefile.in' | xargs sed -i -e 's|CFLAGS =|CFLAGS +=|g'
find . -name 'Makefile.in' | xargs sed -i -e 's|LDOPT=|LDOPT+=|g'
find . -name 'Makefile.in' | xargs sed -i -e 's|COPT=|COPT+=|g'

# (tpg) get rid of some jars
rm -rf lib/junit.jar
sed -i -e 's|cp lib/junit.jar $(LIBDIR)||g' Makefile*

autoreconf -fiv

%configure2_5x \
	--with-jdk=%{java_home}/include,%{java_home}/lib \
	--with-javabin=%{java_home}/bin  \
	--with-libz=yes,%{_libdir}  \
	--with-libjpeg=yes,%{_libdir}   \
	--with-hdf5=yes,%{_libdir} \
	--with-hdf4=yes,%{_libdir}

%make -j1

%install

%makeinstall_std
rm -rf %{buildroot}%{_docdir}/hdf-java

# should be another jni specific directory, but only hdf-java install
# .so files there...
mkdir -p %{buildroot}%{_libdir}
mv -f %{buildroot}%{_javadir}/*.so %{buildroot}%{_libdir}

%files
%doc Readme.txt docs/*
%{_bindir}/hdfview.sh
%{_javadir}/*.jar
%{_javadir}/ext/*.jar
%{_libdir}/*.so
