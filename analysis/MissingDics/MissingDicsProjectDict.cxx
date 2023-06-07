// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME MissingDicsProjectDict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "ROOT/RConfig.hxx"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Header files passed as explicit arguments
#include "MissingDicsProjectHeaders.h"

// Header files passed via #pragma extra_include

// The generated code does not explicitly qualify STL entities
namespace std {} using namespace std;

namespace edm {
   namespace ROOTDict {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *edm_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("edm", 0 /*version*/, "edm__Hash_1_.h", 10,
                     ::ROOT::Internal::DefineBehavior((void*)nullptr,(void*)nullptr),
                     &edm_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_DICT_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_DICT_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *edm_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }
}

namespace ROOT {
   static TClass *pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR_Dictionary();
   static void pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR_TClassManip(TClass*);
   static void *new_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p = nullptr);
   static void *newArray_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(Long_t size, void *p);
   static void delete_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p);
   static void deleteArray_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p);
   static void destruct_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const pair<edm::Hash<1>,edm::ParameterSetBlob>*)
   {
      pair<edm::Hash<1>,edm::ParameterSetBlob> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(pair<edm::Hash<1>,edm::ParameterSetBlob>));
      static ::ROOT::TGenericClassInfo 
         instance("pair<edm::Hash<1>,edm::ParameterSetBlob>", "string", 211,
                  typeid(pair<edm::Hash<1>,edm::ParameterSetBlob>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR_Dictionary, isa_proxy, 4,
                  sizeof(pair<edm::Hash<1>,edm::ParameterSetBlob>) );
      instance.SetNew(&new_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR);
      instance.SetNewArray(&newArray_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR);
      instance.SetDelete(&delete_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR);
      instance.SetDeleteArray(&deleteArray_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR);
      instance.SetDestructor(&destruct_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR);

      ::ROOT::AddClassAlternate("pair<edm::Hash<1>,edm::ParameterSetBlob>","std::pair<edm::Hash<1>, edm::ParameterSetBlob>");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const pair<edm::Hash<1>,edm::ParameterSetBlob>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const pair<edm::Hash<1>,edm::ParameterSetBlob>*>(nullptr))->GetClass();
      pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR_TClassManip(theClass);
   return theClass;
   }

   static void pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *edmcLcLHashlE1gR_Dictionary();
   static void edmcLcLHashlE1gR_TClassManip(TClass*);
   static void *new_edmcLcLHashlE1gR(void *p = nullptr);
   static void *newArray_edmcLcLHashlE1gR(Long_t size, void *p);
   static void delete_edmcLcLHashlE1gR(void *p);
   static void deleteArray_edmcLcLHashlE1gR(void *p);
   static void destruct_edmcLcLHashlE1gR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::edm::Hash<1>*)
   {
      ::edm::Hash<1> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::edm::Hash<1> >(nullptr);
      static ::ROOT::TGenericClassInfo 
         instance("edm::Hash<1>", ::edm::Hash<1>::Class_Version(), "edm__Hash_1_.h", 21,
                  typeid(::edm::Hash<1>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &edmcLcLHashlE1gR_Dictionary, isa_proxy, 4,
                  sizeof(::edm::Hash<1>) );
      instance.SetNew(&new_edmcLcLHashlE1gR);
      instance.SetNewArray(&newArray_edmcLcLHashlE1gR);
      instance.SetDelete(&delete_edmcLcLHashlE1gR);
      instance.SetDeleteArray(&deleteArray_edmcLcLHashlE1gR);
      instance.SetDestructor(&destruct_edmcLcLHashlE1gR);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::edm::Hash<1>*)
   {
      return GenerateInitInstanceLocal(static_cast<::edm::Hash<1>*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::edm::Hash<1>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *edmcLcLHashlE1gR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::edm::Hash<1>*>(nullptr))->GetClass();
      edmcLcLHashlE1gR_TClassManip(theClass);
   return theClass;
   }

   static void edmcLcLHashlE1gR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static void *new_edmcLcLProcessConfiguration(void *p = nullptr);
   static void *newArray_edmcLcLProcessConfiguration(Long_t size, void *p);
   static void delete_edmcLcLProcessConfiguration(void *p);
   static void deleteArray_edmcLcLProcessConfiguration(void *p);
   static void destruct_edmcLcLProcessConfiguration(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::edm::ProcessConfiguration*)
   {
      ::edm::ProcessConfiguration *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::edm::ProcessConfiguration >(nullptr);
      static ::ROOT::TGenericClassInfo 
         instance("edm::ProcessConfiguration", ::edm::ProcessConfiguration::Class_Version(), "edm__ProcessConfiguration.h", 20,
                  typeid(::edm::ProcessConfiguration), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::edm::ProcessConfiguration::Dictionary, isa_proxy, 4,
                  sizeof(::edm::ProcessConfiguration) );
      instance.SetNew(&new_edmcLcLProcessConfiguration);
      instance.SetNewArray(&newArray_edmcLcLProcessConfiguration);
      instance.SetDelete(&delete_edmcLcLProcessConfiguration);
      instance.SetDeleteArray(&deleteArray_edmcLcLProcessConfiguration);
      instance.SetDestructor(&destruct_edmcLcLProcessConfiguration);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::edm::ProcessConfiguration*)
   {
      return GenerateInitInstanceLocal(static_cast<::edm::ProcessConfiguration*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::edm::ProcessConfiguration*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_edmcLcLProcessHistory(void *p = nullptr);
   static void *newArray_edmcLcLProcessHistory(Long_t size, void *p);
   static void delete_edmcLcLProcessHistory(void *p);
   static void deleteArray_edmcLcLProcessHistory(void *p);
   static void destruct_edmcLcLProcessHistory(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::edm::ProcessHistory*)
   {
      ::edm::ProcessHistory *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::edm::ProcessHistory >(nullptr);
      static ::ROOT::TGenericClassInfo 
         instance("edm::ProcessHistory", ::edm::ProcessHistory::Class_Version(), "edm__ProcessHistory.h", 20,
                  typeid(::edm::ProcessHistory), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::edm::ProcessHistory::Dictionary, isa_proxy, 4,
                  sizeof(::edm::ProcessHistory) );
      instance.SetNew(&new_edmcLcLProcessHistory);
      instance.SetNewArray(&newArray_edmcLcLProcessHistory);
      instance.SetDelete(&delete_edmcLcLProcessHistory);
      instance.SetDeleteArray(&deleteArray_edmcLcLProcessHistory);
      instance.SetDestructor(&destruct_edmcLcLProcessHistory);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::edm::ProcessHistory*)
   {
      return GenerateInitInstanceLocal(static_cast<::edm::ProcessHistory*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::edm::ProcessHistory*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_edmcLcLParameterSetBlob(void *p = nullptr);
   static void *newArray_edmcLcLParameterSetBlob(Long_t size, void *p);
   static void delete_edmcLcLParameterSetBlob(void *p);
   static void deleteArray_edmcLcLParameterSetBlob(void *p);
   static void destruct_edmcLcLParameterSetBlob(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::edm::ParameterSetBlob*)
   {
      ::edm::ParameterSetBlob *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::edm::ParameterSetBlob >(nullptr);
      static ::ROOT::TGenericClassInfo 
         instance("edm::ParameterSetBlob", ::edm::ParameterSetBlob::Class_Version(), "edm__ParameterSetBlob.h", 19,
                  typeid(::edm::ParameterSetBlob), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::edm::ParameterSetBlob::Dictionary, isa_proxy, 4,
                  sizeof(::edm::ParameterSetBlob) );
      instance.SetNew(&new_edmcLcLParameterSetBlob);
      instance.SetNewArray(&newArray_edmcLcLParameterSetBlob);
      instance.SetDelete(&delete_edmcLcLParameterSetBlob);
      instance.SetDeleteArray(&deleteArray_edmcLcLParameterSetBlob);
      instance.SetDestructor(&destruct_edmcLcLParameterSetBlob);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::edm::ParameterSetBlob*)
   {
      return GenerateInitInstanceLocal(static_cast<::edm::ParameterSetBlob*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::edm::ParameterSetBlob*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace edm {
//______________________________________________________________________________
atomic_TClass_ptr Hash<1>::fgIsA(nullptr);  // static to hold class pointer

//______________________________________________________________________________
const char *Hash<1>::Class_Name()
{
   return "edm::Hash<1>";
}

//______________________________________________________________________________
const char *Hash<1>::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::Hash<1>*)nullptr)->GetImplFileName();
}

//______________________________________________________________________________
int Hash<1>::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::Hash<1>*)nullptr)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Hash<1>::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::Hash<1>*)nullptr)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Hash<1>::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::Hash<1>*)nullptr)->GetClass(); }
   return fgIsA;
}

} // namespace edm
namespace edm {
//______________________________________________________________________________
atomic_TClass_ptr ProcessConfiguration::fgIsA(nullptr);  // static to hold class pointer

//______________________________________________________________________________
const char *ProcessConfiguration::Class_Name()
{
   return "edm::ProcessConfiguration";
}

//______________________________________________________________________________
const char *ProcessConfiguration::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessConfiguration*)nullptr)->GetImplFileName();
}

//______________________________________________________________________________
int ProcessConfiguration::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessConfiguration*)nullptr)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ProcessConfiguration::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessConfiguration*)nullptr)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ProcessConfiguration::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessConfiguration*)nullptr)->GetClass(); }
   return fgIsA;
}

} // namespace edm
namespace edm {
//______________________________________________________________________________
atomic_TClass_ptr ProcessHistory::fgIsA(nullptr);  // static to hold class pointer

//______________________________________________________________________________
const char *ProcessHistory::Class_Name()
{
   return "edm::ProcessHistory";
}

//______________________________________________________________________________
const char *ProcessHistory::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessHistory*)nullptr)->GetImplFileName();
}

//______________________________________________________________________________
int ProcessHistory::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessHistory*)nullptr)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ProcessHistory::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessHistory*)nullptr)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ProcessHistory::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::ProcessHistory*)nullptr)->GetClass(); }
   return fgIsA;
}

} // namespace edm
namespace edm {
//______________________________________________________________________________
atomic_TClass_ptr ParameterSetBlob::fgIsA(nullptr);  // static to hold class pointer

//______________________________________________________________________________
const char *ParameterSetBlob::Class_Name()
{
   return "edm::ParameterSetBlob";
}

//______________________________________________________________________________
const char *ParameterSetBlob::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::ParameterSetBlob*)nullptr)->GetImplFileName();
}

//______________________________________________________________________________
int ParameterSetBlob::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::edm::ParameterSetBlob*)nullptr)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ParameterSetBlob::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::ParameterSetBlob*)nullptr)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ParameterSetBlob::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::edm::ParameterSetBlob*)nullptr)->GetClass(); }
   return fgIsA;
}

} // namespace edm
namespace ROOT {
   // Wrappers around operator new
   static void *new_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) pair<edm::Hash<1>,edm::ParameterSetBlob> : new pair<edm::Hash<1>,edm::ParameterSetBlob>;
   }
   static void *newArray_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) pair<edm::Hash<1>,edm::ParameterSetBlob>[nElements] : new pair<edm::Hash<1>,edm::ParameterSetBlob>[nElements];
   }
   // Wrapper around operator delete
   static void delete_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p) {
      delete (static_cast<pair<edm::Hash<1>,edm::ParameterSetBlob>*>(p));
   }
   static void deleteArray_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p) {
      delete [] (static_cast<pair<edm::Hash<1>,edm::ParameterSetBlob>*>(p));
   }
   static void destruct_pairlEedmcLcLHashlE1gRcOedmcLcLParameterSetBlobgR(void *p) {
      typedef pair<edm::Hash<1>,edm::ParameterSetBlob> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class pair<edm::Hash<1>,edm::ParameterSetBlob>

namespace edm {
//______________________________________________________________________________
void Hash<1>::Streamer(TBuffer &R__b)
{
   // Stream an object of class edm::Hash<1>.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(edm::Hash<1>::Class(),this);
   } else {
      R__b.WriteClassBuffer(edm::Hash<1>::Class(),this);
   }
}

} // namespace edm
namespace ROOT {
   // Wrappers around operator new
   static void *new_edmcLcLHashlE1gR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::Hash<1> : new ::edm::Hash<1>;
   }
   static void *newArray_edmcLcLHashlE1gR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::Hash<1>[nElements] : new ::edm::Hash<1>[nElements];
   }
   // Wrapper around operator delete
   static void delete_edmcLcLHashlE1gR(void *p) {
      delete (static_cast<::edm::Hash<1>*>(p));
   }
   static void deleteArray_edmcLcLHashlE1gR(void *p) {
      delete [] (static_cast<::edm::Hash<1>*>(p));
   }
   static void destruct_edmcLcLHashlE1gR(void *p) {
      typedef ::edm::Hash<1> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::edm::Hash<1>

namespace edm {
//______________________________________________________________________________
void ProcessConfiguration::Streamer(TBuffer &R__b)
{
   // Stream an object of class edm::ProcessConfiguration.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(edm::ProcessConfiguration::Class(),this);
   } else {
      R__b.WriteClassBuffer(edm::ProcessConfiguration::Class(),this);
   }
}

} // namespace edm
namespace ROOT {
   // Wrappers around operator new
   static void *new_edmcLcLProcessConfiguration(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::ProcessConfiguration : new ::edm::ProcessConfiguration;
   }
   static void *newArray_edmcLcLProcessConfiguration(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::ProcessConfiguration[nElements] : new ::edm::ProcessConfiguration[nElements];
   }
   // Wrapper around operator delete
   static void delete_edmcLcLProcessConfiguration(void *p) {
      delete (static_cast<::edm::ProcessConfiguration*>(p));
   }
   static void deleteArray_edmcLcLProcessConfiguration(void *p) {
      delete [] (static_cast<::edm::ProcessConfiguration*>(p));
   }
   static void destruct_edmcLcLProcessConfiguration(void *p) {
      typedef ::edm::ProcessConfiguration current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::edm::ProcessConfiguration

namespace edm {
//______________________________________________________________________________
void ProcessHistory::Streamer(TBuffer &R__b)
{
   // Stream an object of class edm::ProcessHistory.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(edm::ProcessHistory::Class(),this);
   } else {
      R__b.WriteClassBuffer(edm::ProcessHistory::Class(),this);
   }
}

} // namespace edm
namespace ROOT {
   // Wrappers around operator new
   static void *new_edmcLcLProcessHistory(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::ProcessHistory : new ::edm::ProcessHistory;
   }
   static void *newArray_edmcLcLProcessHistory(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::ProcessHistory[nElements] : new ::edm::ProcessHistory[nElements];
   }
   // Wrapper around operator delete
   static void delete_edmcLcLProcessHistory(void *p) {
      delete (static_cast<::edm::ProcessHistory*>(p));
   }
   static void deleteArray_edmcLcLProcessHistory(void *p) {
      delete [] (static_cast<::edm::ProcessHistory*>(p));
   }
   static void destruct_edmcLcLProcessHistory(void *p) {
      typedef ::edm::ProcessHistory current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::edm::ProcessHistory

namespace edm {
//______________________________________________________________________________
void ParameterSetBlob::Streamer(TBuffer &R__b)
{
   // Stream an object of class edm::ParameterSetBlob.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(edm::ParameterSetBlob::Class(),this);
   } else {
      R__b.WriteClassBuffer(edm::ParameterSetBlob::Class(),this);
   }
}

} // namespace edm
namespace ROOT {
   // Wrappers around operator new
   static void *new_edmcLcLParameterSetBlob(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::ParameterSetBlob : new ::edm::ParameterSetBlob;
   }
   static void *newArray_edmcLcLParameterSetBlob(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::edm::ParameterSetBlob[nElements] : new ::edm::ParameterSetBlob[nElements];
   }
   // Wrapper around operator delete
   static void delete_edmcLcLParameterSetBlob(void *p) {
      delete (static_cast<::edm::ParameterSetBlob*>(p));
   }
   static void deleteArray_edmcLcLParameterSetBlob(void *p) {
      delete [] (static_cast<::edm::ParameterSetBlob*>(p));
   }
   static void destruct_edmcLcLParameterSetBlob(void *p) {
      typedef ::edm::ParameterSetBlob current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::edm::ParameterSetBlob

namespace ROOT {
   static TClass *vectorlEedmcLcLProcessConfigurationgR_Dictionary();
   static void vectorlEedmcLcLProcessConfigurationgR_TClassManip(TClass*);
   static void *new_vectorlEedmcLcLProcessConfigurationgR(void *p = nullptr);
   static void *newArray_vectorlEedmcLcLProcessConfigurationgR(Long_t size, void *p);
   static void delete_vectorlEedmcLcLProcessConfigurationgR(void *p);
   static void deleteArray_vectorlEedmcLcLProcessConfigurationgR(void *p);
   static void destruct_vectorlEedmcLcLProcessConfigurationgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<edm::ProcessConfiguration>*)
   {
      vector<edm::ProcessConfiguration> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<edm::ProcessConfiguration>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<edm::ProcessConfiguration>", -2, "vector", 389,
                  typeid(vector<edm::ProcessConfiguration>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEedmcLcLProcessConfigurationgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<edm::ProcessConfiguration>) );
      instance.SetNew(&new_vectorlEedmcLcLProcessConfigurationgR);
      instance.SetNewArray(&newArray_vectorlEedmcLcLProcessConfigurationgR);
      instance.SetDelete(&delete_vectorlEedmcLcLProcessConfigurationgR);
      instance.SetDeleteArray(&deleteArray_vectorlEedmcLcLProcessConfigurationgR);
      instance.SetDestructor(&destruct_vectorlEedmcLcLProcessConfigurationgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<edm::ProcessConfiguration> >()));

      ::ROOT::AddClassAlternate("vector<edm::ProcessConfiguration>","std::vector<edm::ProcessConfiguration, std::allocator<edm::ProcessConfiguration> >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<edm::ProcessConfiguration>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEedmcLcLProcessConfigurationgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<edm::ProcessConfiguration>*>(nullptr))->GetClass();
      vectorlEedmcLcLProcessConfigurationgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEedmcLcLProcessConfigurationgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEedmcLcLProcessConfigurationgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<edm::ProcessConfiguration> : new vector<edm::ProcessConfiguration>;
   }
   static void *newArray_vectorlEedmcLcLProcessConfigurationgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<edm::ProcessConfiguration>[nElements] : new vector<edm::ProcessConfiguration>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEedmcLcLProcessConfigurationgR(void *p) {
      delete (static_cast<vector<edm::ProcessConfiguration>*>(p));
   }
   static void deleteArray_vectorlEedmcLcLProcessConfigurationgR(void *p) {
      delete [] (static_cast<vector<edm::ProcessConfiguration>*>(p));
   }
   static void destruct_vectorlEedmcLcLProcessConfigurationgR(void *p) {
      typedef vector<edm::ProcessConfiguration> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<edm::ProcessConfiguration>

namespace {
  void TriggerDictionaryInitialization_MissingDicsProjectDict_Impl() {
    static const char* headers[] = {
"MissingDicsProjectHeaders.h",
nullptr
    };
    static const char* includePaths[] = {
"/work/submit/pdmonte/miniforge3/envs/myenv/include",
"/work/submit/pdmonte/miniforge3/envs/myenv/etc/",
"/work/submit/pdmonte/miniforge3/envs/myenv/etc//cling",
"/work/submit/pdmonte/miniforge3/envs/myenv/etc//cling/plugins/include",
"/work/submit/pdmonte/miniforge3/envs/myenv/include/",
"/work/submit/pdmonte/miniforge3/envs/myenv/include",
"/work/submit/pdmonte/miniforge3/envs/myenv/include/",
"/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/MissingDics/",
nullptr
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "MissingDicsProjectDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
namespace edm{class __attribute__((annotate("$clingAutoload$edm__ProcessConfiguration.h")))  __attribute__((annotate("$clingAutoload$MissingDicsProjectHeaders.h")))  ProcessConfiguration;}
namespace edm{class __attribute__((annotate("$clingAutoload$edm__ProcessHistory.h")))  __attribute__((annotate("$clingAutoload$MissingDicsProjectHeaders.h")))  ProcessHistory;}
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "MissingDicsProjectDict dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "MissingDicsProjectHeaders.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"edm::Hash<1>", payloadCode, "@",
"edm::ParameterSetBlob", payloadCode, "@",
"edm::ProcessConfiguration", payloadCode, "@",
"edm::ProcessHistory", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("MissingDicsProjectDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_MissingDicsProjectDict_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_MissingDicsProjectDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_MissingDicsProjectDict() {
  TriggerDictionaryInitialization_MissingDicsProjectDict_Impl();
}
