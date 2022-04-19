#include<iostream>
#include<fstream>
#include <json.hpp> //https://github.com/nlohmann/json

/*
Python
import json

testdict = {'level1': {'level2': 2}, 'level1_2': 'check'}
with open('test.json', 'w') as f:
    json.dump(testdict, f)
*/

int main() {
  using json = nlohmann::json;
  
  std::ifstream i("test.json");
  json j;
  i >> j;

  std::cout << j["level1"] << std::endl;
  std::cout << j["level1"]["level2"].get<int>() + 1 << std::endl;
  std::cout << j["level1_2"].get<std::string>() + "_add" << std::endl;
  return 0;
}
