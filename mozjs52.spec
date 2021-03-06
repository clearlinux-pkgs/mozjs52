#
# Inspired by the Arch Linux equivalent package.....
#
Name     : mozjs52
Version  : 52
Release  : 19
Source0  : https://hg.mozilla.org/mozilla-unified/archive/c3e447e07077.tar.gz
Group    : Development/Tools
License  : Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-3-Clause-Clear GPL-2.0 LGPL-2.0 LGPL-2.1 MIT MPL-2.0-no-copyleft-exception
Requires: mozjs52-bin
Requires: mozjs52-lib
Requires: psutil
Requires: pyOpenSSL
Requires: pyasn1
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
Patch6: trim.patch

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
%patch6 -p1

pushd ..
cp -a  mozilla-unified-c3e447e07077 build-avx2
popd

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C
export SOURCE_DATE_EPOCH=1501084420
export CFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition -fassociative-math -fno-signed-zeros "
export FCFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export FFLAGS="$CFLAGS -O3 -falign-functions=32 -fno-semantic-interposition "
export CXXFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition -fassociative-math -fno-signed-zeros"
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

pushd ../build-avx2/js/src
export CFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition -march=haswell"
export FCFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export FFLAGS="$CFLAGS -O3 -falign-functions=32 -fno-semantic-interposition "
export CXXFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition -march=haswell"
export AUTOCONF="/usr/bin/autoconf213"
CFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp -flto=10'
CXXFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp -flto=10'
export CC=gcc CXX=g++ PYTHON=/usr/bin/python2

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
    --libdir=/usr/lib64/haswell \
    --without-system-icu
make V=1  %{?_smp_mflags}

popd


%install
export SOURCE_DATE_EPOCH=1501084420
rm -rf %{buildroot}
pushd ../build-avx2/js/src
%make_install
popd
rm -rf %{buildroot}/usr/bin/*
pushd js/src
%make_install
popd
rm %{buildroot}/usr/lib64/*.ajs
rm %{buildroot}/usr/lib64/haswell/libjs_static.ajs

cp %{buildroot}/usr/lib64/libmozjs-52.so %{buildroot}/usr/lib64/libmozjs-52.so.0
cp %{buildroot}/usr/lib64/haswell/libmozjs-52.so %{buildroot}/usr/lib64/haswell/libmozjs-52.so.0
#find %{buildroot}/usr/{lib/pkgconfig,include} -type f -exec chmod -c a-x {} +
## make_install_append content
#mv %{buildroot}/usr/lib64/pkgconfig/js.pc %{buildroot}/usr/lib64/pkgconfig/mozjs-52.pc
## make_install_append end

%files
%defattr(-,root,root,-)
#/usr/lib64/libjs_static.ajs

%files bin
%defattr(-,root,root,-)
   /usr/bin/js52
   /usr/bin/js52-config

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
   /usr/include/mozjs-52/fdlibm.h
   /usr/include/mozjs-52/jemalloc_types.h
   /usr/include/mozjs-52/js/GCAnnotations.h
   /usr/include/mozjs-52/js/GCHashTable.h
   /usr/include/mozjs-52/js/GCPolicyAPI.h
   /usr/include/mozjs-52/js/GCVariant.h
   /usr/include/mozjs-52/js/GCVector.h
   /usr/include/mozjs-52/js/Initialization.h
   /usr/include/mozjs-52/js/Realm.h
   /usr/include/mozjs-52/js/SweepingAPI.h
   /usr/include/mozjs-52/js/TraceKind.h
   /usr/include/mozjs-52/js/UbiNodeBreadthFirst.h
   /usr/include/mozjs-52/js/UbiNodeCensus.h
   /usr/include/mozjs-52/js/UbiNodeDominatorTree.h
   /usr/include/mozjs-52/js/UbiNodePostOrder.h
   /usr/include/mozjs-52/js/UbiNodeShortestPaths.h
   /usr/include/mozjs-52/js/UniquePtr.h
   /usr/include/mozjs-52/mozilla/BufferList.h
   /usr/include/mozjs-52/mozilla/EndianUtils.h
   /usr/include/mozjs-52/mozilla/EnumTypeTraits.h
   /usr/include/mozjs-52/mozilla/EnumeratedRange.h
   /usr/include/mozjs-52/mozilla/FastBernoulliTrial.h
   /usr/include/mozjs-52/mozilla/Function.h
   /usr/include/mozjs-52/mozilla/IndexSequence.h
   /usr/include/mozjs-52/mozilla/NotNull.h
   /usr/include/mozjs-52/mozilla/Opaque.h
   /usr/include/mozjs-52/mozilla/OperatorNewExtensions.h
   /usr/include/mozjs-52/mozilla/RangedArray.h
   /usr/include/mozjs-52/mozilla/RefCounted.h
   /usr/include/mozjs-52/mozilla/Saturate.h
   /usr/include/mozjs-52/mozilla/ScopeExit.h
   /usr/include/mozjs-52/mozilla/Sprintf.h
   /usr/include/mozjs-52/mozilla/StackWalk.h
   /usr/include/mozjs-52/mozilla/StaticAnalysisFunctions.h
   /usr/include/mozjs-52/mozilla/TimeStamp.h
   /usr/include/mozjs-52/mozilla/Tuple.h
   /usr/include/mozjs-52/mozilla/UniquePtrExtensions.h
   /usr/include/mozjs-52/mozilla/Unused.h
   /usr/include/mozjs-52/mozilla/Variant.h
   /usr/include/mozjs-52/mozilla/XorShift128PlusRNG.h
   /usr/include/mozjs-52/mozilla/fallible.h
   /usr/include/mozjs-52/mozilla/mozalloc.h
   /usr/include/mozjs-52/mozilla/mozalloc_abort.h
   /usr/include/mozjs-52/mozilla/mozalloc_oom.h
   /usr/include/mozjs-52/mozmemory.h
   /usr/include/mozjs-52/mozmemory_wrap.h
   /usr/include/mozjs-52/unicode/alphaindex.h
   /usr/include/mozjs-52/unicode/appendable.h
   /usr/include/mozjs-52/unicode/basictz.h
   /usr/include/mozjs-52/unicode/brkiter.h
   /usr/include/mozjs-52/unicode/bytestream.h
   /usr/include/mozjs-52/unicode/bytestrie.h
   /usr/include/mozjs-52/unicode/bytestriebuilder.h
   /usr/include/mozjs-52/unicode/calendar.h
   /usr/include/mozjs-52/unicode/caniter.h
   /usr/include/mozjs-52/unicode/chariter.h
   /usr/include/mozjs-52/unicode/choicfmt.h
   /usr/include/mozjs-52/unicode/coleitr.h
   /usr/include/mozjs-52/unicode/coll.h
   /usr/include/mozjs-52/unicode/compactdecimalformat.h
   /usr/include/mozjs-52/unicode/curramt.h
   /usr/include/mozjs-52/unicode/currpinf.h
   /usr/include/mozjs-52/unicode/currunit.h
   /usr/include/mozjs-52/unicode/datefmt.h
   /usr/include/mozjs-52/unicode/dbbi.h
   /usr/include/mozjs-52/unicode/dcfmtsym.h
   /usr/include/mozjs-52/unicode/decimfmt.h
   /usr/include/mozjs-52/unicode/docmain.h
   /usr/include/mozjs-52/unicode/dtfmtsym.h
   /usr/include/mozjs-52/unicode/dtintrv.h
   /usr/include/mozjs-52/unicode/dtitvfmt.h
   /usr/include/mozjs-52/unicode/dtitvinf.h
   /usr/include/mozjs-52/unicode/dtptngen.h
   /usr/include/mozjs-52/unicode/dtrule.h
   /usr/include/mozjs-52/unicode/enumset.h
   /usr/include/mozjs-52/unicode/errorcode.h
   /usr/include/mozjs-52/unicode/fieldpos.h
   /usr/include/mozjs-52/unicode/filteredbrk.h
   /usr/include/mozjs-52/unicode/fmtable.h
   /usr/include/mozjs-52/unicode/format.h
   /usr/include/mozjs-52/unicode/fpositer.h
   /usr/include/mozjs-52/unicode/gender.h
   /usr/include/mozjs-52/unicode/gregocal.h
   /usr/include/mozjs-52/unicode/icudataver.h
   /usr/include/mozjs-52/unicode/icuplug.h
   /usr/include/mozjs-52/unicode/idna.h
   /usr/include/mozjs-52/unicode/listformatter.h
   /usr/include/mozjs-52/unicode/localpointer.h
   /usr/include/mozjs-52/unicode/locdspnm.h
   /usr/include/mozjs-52/unicode/locid.h
   /usr/include/mozjs-52/unicode/measfmt.h
   /usr/include/mozjs-52/unicode/measunit.h
   /usr/include/mozjs-52/unicode/measure.h
   /usr/include/mozjs-52/unicode/messagepattern.h
   /usr/include/mozjs-52/unicode/msgfmt.h
   /usr/include/mozjs-52/unicode/normalizer2.h
   /usr/include/mozjs-52/unicode/normlzr.h
   /usr/include/mozjs-52/unicode/numfmt.h
   /usr/include/mozjs-52/unicode/numsys.h
   /usr/include/mozjs-52/unicode/parseerr.h
   /usr/include/mozjs-52/unicode/parsepos.h
   /usr/include/mozjs-52/unicode/platform.h
   /usr/include/mozjs-52/unicode/plurfmt.h
   /usr/include/mozjs-52/unicode/plurrule.h
   /usr/include/mozjs-52/unicode/ptypes.h
   /usr/include/mozjs-52/unicode/putil.h
   /usr/include/mozjs-52/unicode/rbbi.h
   /usr/include/mozjs-52/unicode/rbnf.h
   /usr/include/mozjs-52/unicode/rbtz.h
   /usr/include/mozjs-52/unicode/regex.h
   /usr/include/mozjs-52/unicode/region.h
   /usr/include/mozjs-52/unicode/reldatefmt.h
   /usr/include/mozjs-52/unicode/rep.h
   /usr/include/mozjs-52/unicode/resbund.h
   /usr/include/mozjs-52/unicode/schriter.h
   /usr/include/mozjs-52/unicode/scientificnumberformatter.h
   /usr/include/mozjs-52/unicode/search.h
   /usr/include/mozjs-52/unicode/selfmt.h
   /usr/include/mozjs-52/unicode/simpleformatter.h
   /usr/include/mozjs-52/unicode/simpletz.h
   /usr/include/mozjs-52/unicode/smpdtfmt.h
   /usr/include/mozjs-52/unicode/sortkey.h
   /usr/include/mozjs-52/unicode/std_string.h
   /usr/include/mozjs-52/unicode/strenum.h
   /usr/include/mozjs-52/unicode/stringpiece.h
   /usr/include/mozjs-52/unicode/stringtriebuilder.h
   /usr/include/mozjs-52/unicode/stsearch.h
   /usr/include/mozjs-52/unicode/symtable.h
   /usr/include/mozjs-52/unicode/tblcoll.h
   /usr/include/mozjs-52/unicode/timezone.h
   /usr/include/mozjs-52/unicode/tmunit.h
   /usr/include/mozjs-52/unicode/tmutamt.h
   /usr/include/mozjs-52/unicode/tmutfmt.h
   /usr/include/mozjs-52/unicode/translit.h
   /usr/include/mozjs-52/unicode/tzfmt.h
   /usr/include/mozjs-52/unicode/tznames.h
   /usr/include/mozjs-52/unicode/tzrule.h
   /usr/include/mozjs-52/unicode/tztrans.h
   /usr/include/mozjs-52/unicode/ubidi.h
   /usr/include/mozjs-52/unicode/ubiditransform.h
   /usr/include/mozjs-52/unicode/ubrk.h
   /usr/include/mozjs-52/unicode/ucal.h
   /usr/include/mozjs-52/unicode/ucasemap.h
   /usr/include/mozjs-52/unicode/ucat.h
   /usr/include/mozjs-52/unicode/uchar.h
   /usr/include/mozjs-52/unicode/ucharstrie.h
   /usr/include/mozjs-52/unicode/ucharstriebuilder.h
   /usr/include/mozjs-52/unicode/uchriter.h
   /usr/include/mozjs-52/unicode/uclean.h
   /usr/include/mozjs-52/unicode/ucnv.h
   /usr/include/mozjs-52/unicode/ucnv_cb.h
   /usr/include/mozjs-52/unicode/ucnv_err.h
   /usr/include/mozjs-52/unicode/ucnvsel.h
   /usr/include/mozjs-52/unicode/ucol.h
   /usr/include/mozjs-52/unicode/ucoleitr.h
   /usr/include/mozjs-52/unicode/uconfig.h
   /usr/include/mozjs-52/unicode/ucsdet.h
   /usr/include/mozjs-52/unicode/ucurr.h
   /usr/include/mozjs-52/unicode/udat.h
   /usr/include/mozjs-52/unicode/udata.h
   /usr/include/mozjs-52/unicode/udateintervalformat.h
   /usr/include/mozjs-52/unicode/udatpg.h
   /usr/include/mozjs-52/unicode/udisplaycontext.h
   /usr/include/mozjs-52/unicode/uenum.h
   /usr/include/mozjs-52/unicode/ufieldpositer.h
   /usr/include/mozjs-52/unicode/uformattable.h
   /usr/include/mozjs-52/unicode/ugender.h
   /usr/include/mozjs-52/unicode/uidna.h
   /usr/include/mozjs-52/unicode/uiter.h
   /usr/include/mozjs-52/unicode/uldnames.h
   /usr/include/mozjs-52/unicode/ulistformatter.h
   /usr/include/mozjs-52/unicode/uloc.h
   /usr/include/mozjs-52/unicode/ulocdata.h
   /usr/include/mozjs-52/unicode/umachine.h
   /usr/include/mozjs-52/unicode/umisc.h
   /usr/include/mozjs-52/unicode/umsg.h
   /usr/include/mozjs-52/unicode/unifilt.h
   /usr/include/mozjs-52/unicode/unifunct.h
   /usr/include/mozjs-52/unicode/unimatch.h
   /usr/include/mozjs-52/unicode/unirepl.h
   /usr/include/mozjs-52/unicode/uniset.h
   /usr/include/mozjs-52/unicode/unistr.h
   /usr/include/mozjs-52/unicode/unorm.h
   /usr/include/mozjs-52/unicode/unorm2.h
   /usr/include/mozjs-52/unicode/unum.h
   /usr/include/mozjs-52/unicode/unumsys.h
   /usr/include/mozjs-52/unicode/uobject.h
   /usr/include/mozjs-52/unicode/upluralrules.h
   /usr/include/mozjs-52/unicode/uregex.h
   /usr/include/mozjs-52/unicode/uregion.h
   /usr/include/mozjs-52/unicode/ureldatefmt.h
   /usr/include/mozjs-52/unicode/urename.h
   /usr/include/mozjs-52/unicode/urep.h
   /usr/include/mozjs-52/unicode/ures.h
   /usr/include/mozjs-52/unicode/uscript.h
   /usr/include/mozjs-52/unicode/usearch.h
   /usr/include/mozjs-52/unicode/uset.h
   /usr/include/mozjs-52/unicode/usetiter.h
   /usr/include/mozjs-52/unicode/ushape.h
   /usr/include/mozjs-52/unicode/uspoof.h
   /usr/include/mozjs-52/unicode/usprep.h
   /usr/include/mozjs-52/unicode/ustring.h
   /usr/include/mozjs-52/unicode/ustringtrie.h
   /usr/include/mozjs-52/unicode/utext.h
   /usr/include/mozjs-52/unicode/utf.h
   /usr/include/mozjs-52/unicode/utf16.h
   /usr/include/mozjs-52/unicode/utf32.h
   /usr/include/mozjs-52/unicode/utf8.h
   /usr/include/mozjs-52/unicode/utf_old.h
   /usr/include/mozjs-52/unicode/utmscale.h
   /usr/include/mozjs-52/unicode/utrace.h
   /usr/include/mozjs-52/unicode/utrans.h
   /usr/include/mozjs-52/unicode/utypes.h
   /usr/include/mozjs-52/unicode/uvernum.h
   /usr/include/mozjs-52/unicode/uversion.h
   /usr/include/mozjs-52/unicode/vtzone.h

%files lib
%defattr(-,root,root,-)
/usr/lib64/libmozjs-52.so
/usr/lib64/libmozjs-52.so.0
/usr/lib64/haswell/libmozjs-52.so
/usr/lib64/haswell/libmozjs-52.so.0

