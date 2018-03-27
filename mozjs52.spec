#
# Inspired by the Arch Linux equivalent package.....
#
Name     : mozjs52
Version  : 52
Release  : 10
Source0  : https://hg.mozilla.org/mozilla-unified/archive/c3e447e07077.tar.gz
Group    : Development/Tools
License  : Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-3-Clause-Clear GPL-2.0 LGPL-2.0 LGPL-2.1 MIT MPL-2.0-no-copyleft-exception
Requires: mozjs52-bin
Requires: mozjs52-lib
Requires: psutil
Requires: py
Requires: pyOpenSSL
Requires: pyasn1
Requires: pytest
Requires: pytest-cov
Requires: wheel
BuildRequires : icu4c-dev
BuildRequires : nspr-dev
BuildRequires : pbr
BuildRequires : pip
BuildRequires : pkgconfig(libffi)
BuildRequires : pkgconfig(x11)
BuildRequires : psutil
BuildRequires : python-dev
BuildRequires : python3-dev
BuildRequires : setuptools
BuildRequires : zlib-dev
BuildRequires : autoconf213
BuildRequires : readline-dev
BuildRequires : ncurses-dev
Summary: mozjs

Patch1: mozjs52-copy-headers.patch
Patch2: mozjs52-disable-mozglue.patch
Patch3: mozjs52-fix-soname.patch
Patch4: mozjs52-include-configure-script.patch
Patch5: autoconf.patch

%description
your system under test with mock objects and make assertions about how they
        have been used.
        
        mock is now part of the Python standard library, available as `unittest.mock <

%package bin
Summary: bin components for the mozjs52 package.
Group: Binaries

%description bin
bin components for the mozjs52 package.


%package dev
Summary: dev components for the mozjs52 package.
Group: Development
Requires: mozjs52-lib
Requires: mozjs52-bin
Provides: mozjs52-devel

%description dev
dev components for the mozjs52 package.


%package lib
Summary: lib components for the mozjs52 package.
Group: Libraries

%description lib
lib components for the mozjs52 package.


%prep
%setup -q -n mozilla-unified-c3e447e07077
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C
export SOURCE_DATE_EPOCH=1501084420
export CFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export FCFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export FFLAGS="$CFLAGS -O3 -falign-functions=32 -fno-semantic-interposition "
export CXXFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export AUTOCONF="/usr/bin/autoconf213"
CFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp -flto=10'
CXXFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp -flto=10'
export CC=gcc CXX=g++ PYTHON=/usr/bin/python2

pushd js/src
%configure --disable-static --with-x \
    --prefix=/usr \
    --disable-debug \
    --disable-debug-symbols \
    --disable-strip \
    --enable-gold \
    --enable-optimize="-O3" \
    --enable-pie \
    --enable-posix-nspr-emulation \
    --enable-readline \
    --enable-release \
    --enable-shared-js \
    --enable-tests \
    --with-intl-api \
    --with-system-zlib \
    --program-suffix=52 \
    --without-system-icu
    
make V=1  %{?_smp_mflags}
popd

%install
export SOURCE_DATE_EPOCH=1501084420
rm -rf %{buildroot}
pushd js/src
%make_install
popd
rm %{buildroot}/usr/lib64/*.ajs
#find %{buildroot}/usr/{lib/pkgconfig,include} -type f -exec chmod -c a-x {} +
## make_install_append content
#mv %{buildroot}/usr/lib64/pkgconfig/js.pc %{buildroot}/usr/lib64/pkgconfig/mozjs-52.pc
## make_install_append end

%files
%defattr(-,root,root,-)
#/usr/lib64/libjs_static.ajs

%files bin
%defattr(-,root,root,-)
#/usr/bin/js
#/usr/bin/js-config

%files dev
%defattr(-,root,root,-)
/usr/include/mozjs-52/js-config.h
/usr/include/mozjs-52/js.msg
/usr/include/mozjs-52/js/CallArgs.h
/usr/include/mozjs-52/js/CallNonGenericMethod.h
/usr/include/mozjs-52/js/CharacterEncoding.h
/usr/include/mozjs-52/js/Class.h
/usr/include/mozjs-52/js/Conversions.h
/usr/include/mozjs-52/js/Date.h
/usr/include/mozjs-52/js/Debug.h
/usr/include/mozjs-52/js/GCAPI.h
/usr/include/mozjs-52/js/HashTable.h
/usr/include/mozjs-52/js/HeapAPI.h
/usr/include/mozjs-52/js/Id.h
/usr/include/mozjs-52/js/LegacyIntTypes.h
/usr/include/mozjs-52/js/MemoryMetrics.h
/usr/include/mozjs-52/js/Principals.h
/usr/include/mozjs-52/js/ProfilingFrameIterator.h
/usr/include/mozjs-52/js/ProfilingStack.h
/usr/include/mozjs-52/js/Proxy.h
/usr/include/mozjs-52/js/RequiredDefines.h
/usr/include/mozjs-52/js/RootingAPI.h
/usr/include/mozjs-52/js/SliceBudget.h
/usr/include/mozjs-52/js/StructuredClone.h
/usr/include/mozjs-52/js/TracingAPI.h
/usr/include/mozjs-52/js/TrackedOptimizationInfo.h
/usr/include/mozjs-52/js/TypeDecls.h
/usr/include/mozjs-52/js/UbiNode.h
/usr/include/mozjs-52/js/Utility.h
/usr/include/mozjs-52/js/Value.h
/usr/include/mozjs-52/js/Vector.h
/usr/include/mozjs-52/js/WeakMapPtr.h
/usr/include/mozjs-52/jsalloc.h
/usr/include/mozjs-52/jsapi.h
/usr/include/mozjs-52/jsbytecode.h
/usr/include/mozjs-52/jsclist.h
/usr/include/mozjs-52/jscpucfg.h
/usr/include/mozjs-52/jsfriendapi.h
/usr/include/mozjs-52/jsperf.h
/usr/include/mozjs-52/jsprf.h
/usr/include/mozjs-52/jsprototypes.h
/usr/include/mozjs-52/jspubtd.h
/usr/include/mozjs-52/jstypes.h
/usr/include/mozjs-52/jsversion.h
/usr/include/mozjs-52/jswrapper.h
/usr/include/mozjs-52/mozilla/Alignment.h
/usr/include/mozjs-52/mozilla/AllocPolicy.h
/usr/include/mozjs-52/mozilla/AlreadyAddRefed.h
/usr/include/mozjs-52/mozilla/Array.h
/usr/include/mozjs-52/mozilla/ArrayUtils.h
/usr/include/mozjs-52/mozilla/Assertions.h
/usr/include/mozjs-52/mozilla/Atomics.h
/usr/include/mozjs-52/mozilla/Attributes.h
/usr/include/mozjs-52/mozilla/BinarySearch.h
/usr/include/mozjs-52/mozilla/BloomFilter.h
/usr/include/mozjs-52/mozilla/Casting.h
/usr/include/mozjs-52/mozilla/ChaosMode.h
/usr/include/mozjs-52/mozilla/Char16.h
/usr/include/mozjs-52/mozilla/CheckedInt.h
/usr/include/mozjs-52/mozilla/Compiler.h
/usr/include/mozjs-52/mozilla/Compression.h
/usr/include/mozjs-52/mozilla/DebugOnly.h
/usr/include/mozjs-52/mozilla/Decimal.h
/usr/include/mozjs-52/mozilla/EnumSet.h
/usr/include/mozjs-52/mozilla/EnumeratedArray.h
/usr/include/mozjs-52/mozilla/FloatingPoint.h
/usr/include/mozjs-52/mozilla/GuardObjects.h
/usr/include/mozjs-52/mozilla/HashFunctions.h
/usr/include/mozjs-52/mozilla/IntegerPrintfMacros.h
/usr/include/mozjs-52/mozilla/IntegerRange.h
/usr/include/mozjs-52/mozilla/IntegerTypeTraits.h
/usr/include/mozjs-52/mozilla/JSONWriter.h
/usr/include/mozjs-52/mozilla/Likely.h
/usr/include/mozjs-52/mozilla/LinkedList.h
/usr/include/mozjs-52/mozilla/LinuxSignal.h
/usr/include/mozjs-52/mozilla/MacroArgs.h
/usr/include/mozjs-52/mozilla/MacroForEach.h
/usr/include/mozjs-52/mozilla/MathAlgorithms.h
/usr/include/mozjs-52/mozilla/Maybe.h
/usr/include/mozjs-52/mozilla/MaybeOneOf.h
/usr/include/mozjs-52/mozilla/MemoryChecking.h
/usr/include/mozjs-52/mozilla/MemoryReporting.h
/usr/include/mozjs-52/mozilla/Move.h
/usr/include/mozjs-52/mozilla/NullPtr.h
/usr/include/mozjs-52/mozilla/Pair.h
/usr/include/mozjs-52/mozilla/PodOperations.h
/usr/include/mozjs-52/mozilla/Poison.h
/usr/include/mozjs-52/mozilla/Range.h
/usr/include/mozjs-52/mozilla/RangedPtr.h
/usr/include/mozjs-52/mozilla/ReentrancyGuard.h
/usr/include/mozjs-52/mozilla/RefCountType.h
/usr/include/mozjs-52/mozilla/RefPtr.h
/usr/include/mozjs-52/mozilla/ReverseIterator.h
/usr/include/mozjs-52/mozilla/RollingMean.h
/usr/include/mozjs-52/mozilla/SHA1.h
/usr/include/mozjs-52/mozilla/Scoped.h
/usr/include/mozjs-52/mozilla/SegmentedVector.h
/usr/include/mozjs-52/mozilla/SizePrintfMacros.h
/usr/include/mozjs-52/mozilla/SplayTree.h
/usr/include/mozjs-52/mozilla/TaggedAnonymousMemory.h
/usr/include/mozjs-52/mozilla/TemplateLib.h
/usr/include/mozjs-52/mozilla/ThreadLocal.h
/usr/include/mozjs-52/mozilla/ToString.h
/usr/include/mozjs-52/mozilla/TypeTraits.h
/usr/include/mozjs-52/mozilla/TypedEnumBits.h
/usr/include/mozjs-52/mozilla/Types.h
/usr/include/mozjs-52/mozilla/UniquePtr.h
/usr/include/mozjs-52/mozilla/Vector.h
/usr/include/mozjs-52/mozilla/WeakPtr.h
/usr/include/mozjs-52/mozilla/double-conversion.h
/usr/include/mozjs-52/mozilla/utils.h
/usr/lib64/pkgconfig/mozjs-52.pc

%files lib
%defattr(-,root,root,-)
/usr/lib64/libmozjs-52.so
