#include <memory>
#include "pfpsim/core/PFPObject.h"
#include "../behavioural/top.h"

using pfp::core::PFPObject;

std::unique_ptr<PFPObject> create_top() {
  auto t = new top("top");
  t->init();
  return std::unique_ptr<PFPObject>(t);
}
