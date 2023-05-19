namespace std {}
using namespace std;
#include "MissingDicsProjectHeaders.h"

#include "MissingDicsLinkDef.h"

#include "MissingDicsProjectDict.cxx"

struct DeleteObjectFunctor {
   template <typename T>
   void operator()(const T *ptr) const {
      delete ptr;
   }
   template <typename T, typename Q>
   void operator()(const std::pair<T,Q> &) const {
      // Do nothing
   }
   template <typename T, typename Q>
   void operator()(const std::pair<T,Q*> &ptr) const {
      delete ptr.second;
   }
   template <typename T, typename Q>
   void operator()(const std::pair<T*,Q> &ptr) const {
      delete ptr.first;
   }
   template <typename T, typename Q>
   void operator()(const std::pair<T*,Q*> &ptr) const {
      delete ptr.first;
      delete ptr.second;
   }
};

#ifndef edm__Hash_1__cxx
#define edm__Hash_1__cxx
edm::Hash<1>::Hash() {
}
edm::Hash<1> &edm::Hash<1>::operator=(const Hash & rhs)
{
   // This is NOT a copy operator=. This is actually a move operator= (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   hash_ = (const_cast<Hash &>( rhs ).hash_);
   Hash &modrhs = const_cast<Hash &>( rhs );
   modrhs.hash_.clear();
   return *this;
}
edm::Hash<1>::Hash(const Hash & rhs)
   : hash_(const_cast<Hash &>( rhs ).hash_)
{
   // This is NOT a copy constructor. This is actually a move constructor (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   Hash &modrhs = const_cast<Hash &>( rhs );
   modrhs.hash_.clear();
}
edm::Hash<1>::~Hash() {
}
#endif // edm__Hash_1__cxx

#ifndef edm__ProcessHistory_cxx
#define edm__ProcessHistory_cxx
edm::ProcessHistory::ProcessHistory() {
}
edm::ProcessHistory &edm::ProcessHistory::operator=(const ProcessHistory & rhs)
{
   // This is NOT a copy operator=. This is actually a move operator= (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   data_ = (const_cast<ProcessHistory &>( rhs ).data_);
   ProcessHistory &modrhs = const_cast<ProcessHistory &>( rhs );
   modrhs.data_.clear();
   return *this;
}
edm::ProcessHistory::ProcessHistory(const ProcessHistory & rhs)
   : data_(const_cast<ProcessHistory &>( rhs ).data_)
{
   // This is NOT a copy constructor. This is actually a move constructor (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   ProcessHistory &modrhs = const_cast<ProcessHistory &>( rhs );
   modrhs.data_.clear();
}
edm::ProcessHistory::~ProcessHistory() {
}
#endif // edm__ProcessHistory_cxx

#ifndef edm__ProcessConfiguration_cxx
#define edm__ProcessConfiguration_cxx
edm::ProcessConfiguration::ProcessConfiguration() {
}
edm::ProcessConfiguration &edm::ProcessConfiguration::operator=(const ProcessConfiguration & rhs)
{
   // This is NOT a copy operator=. This is actually a move operator= (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   processName_ = (const_cast<ProcessConfiguration &>( rhs ).processName_);
   parameterSetID_ = (const_cast<ProcessConfiguration &>( rhs ).parameterSetID_);
   releaseVersion_ = (const_cast<ProcessConfiguration &>( rhs ).releaseVersion_);
   passID_ = (const_cast<ProcessConfiguration &>( rhs ).passID_);
   ProcessConfiguration &modrhs = const_cast<ProcessConfiguration &>( rhs );
   modrhs.processName_.clear();
   modrhs.releaseVersion_.clear();
   modrhs.passID_.clear();
   return *this;
}
edm::ProcessConfiguration::ProcessConfiguration(const ProcessConfiguration & rhs)
   : processName_(const_cast<ProcessConfiguration &>( rhs ).processName_)
   , parameterSetID_(const_cast<ProcessConfiguration &>( rhs ).parameterSetID_)
   , releaseVersion_(const_cast<ProcessConfiguration &>( rhs ).releaseVersion_)
   , passID_(const_cast<ProcessConfiguration &>( rhs ).passID_)
{
   // This is NOT a copy constructor. This is actually a move constructor (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   ProcessConfiguration &modrhs = const_cast<ProcessConfiguration &>( rhs );
   modrhs.processName_.clear();
   modrhs.releaseVersion_.clear();
   modrhs.passID_.clear();
}
edm::ProcessConfiguration::~ProcessConfiguration() {
}
#endif // edm__ProcessConfiguration_cxx

#ifndef edm__ParameterSetBlob_cxx
#define edm__ParameterSetBlob_cxx
edm::ParameterSetBlob::ParameterSetBlob() {
}
edm::ParameterSetBlob &edm::ParameterSetBlob::operator=(const ParameterSetBlob & rhs)
{
   // This is NOT a copy operator=. This is actually a move operator= (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   pset_ = (const_cast<ParameterSetBlob &>( rhs ).pset_);
   ParameterSetBlob &modrhs = const_cast<ParameterSetBlob &>( rhs );
   modrhs.pset_.clear();
   return *this;
}
edm::ParameterSetBlob::ParameterSetBlob(const ParameterSetBlob & rhs)
   : pset_(const_cast<ParameterSetBlob &>( rhs ).pset_)
{
   // This is NOT a copy constructor. This is actually a move constructor (for stl container's sake).
   // Use at your own risk!
   (void)rhs; // avoid warning about unused parameter
   ParameterSetBlob &modrhs = const_cast<ParameterSetBlob &>( rhs );
   modrhs.pset_.clear();
}
edm::ParameterSetBlob::~ParameterSetBlob() {
}
#endif // edm__ParameterSetBlob_cxx


