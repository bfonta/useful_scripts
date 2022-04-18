#include <iostream>
#include <string>
#include "nested_map.h"

//compile with `g++ -o exe main.cc`
int main()
{
  //std::unordered_map<std::string, float> myMap;
  nested_map<std::string, float, 2> myMap2;

  myMap2.set(3.5f, "etau", "IsoMu27", "test");
  std::cout << myMap2.exists("etau", "IsoMu27", "test") << std::endl;
  std::cout << myMap2.exists("mutau", "IsoMu27", "test") << std::endl;
  std::cout << myMap2.exists("eta", "IsoMu27", "test") << std::endl;
  std::cout << myMap2.exists("IsoMu27", "etau", "test") << std::endl;
  std::cout << myMap2("etau", "IsoMu27", "test") << std::endl;
  std::cout << myMap2("mutau", "IsoMu27", "test") << std::endl;
  return 0;
}
