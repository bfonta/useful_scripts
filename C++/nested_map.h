#ifndef NESTEDMAP_H
#define NESTEDMAP_H

#include <iostream>
#include <unordered_map>

template <class KEY_T, class VAL_T, unsigned int DEPTH>
  class nested_map_def
{
 public:
  typedef std::unordered_map<KEY_T,
   	typename nested_map_def<KEY_T, VAL_T, DEPTH-1>::map_type> map_type;
};

template<class KEY_T, class VAL_T>
  class nested_map_def<KEY_T, VAL_T, 0>
{
 public:
  typedef std::unordered_map<KEY_T, VAL_T> map_type;
};

template <class KEY_T, class VAL_T, unsigned int DEPTH>
  class nested_map
{
 public:
  void operator[](KEY_T key) const
	{
	  std::cout << "The `[]` operator was not implemented. Use `()` instead."
				<< std::endl;
	  std::exit(0);
	}

  //Read-only
  template <class ... Ts>
	const VAL_T& operator()(KEY_T key, Ts... args) const
	{
	  if( sizeof...(args) != DEPTH) {
		std::cout << "Number of arguments does not match depth of nested map."
				  << std::endl;
		std::exit(0);
	  }
	  return internal_read_only_call(catch_out_of_range(m, key), args...);
	}

  //Modifier
  template <class ... Ts>
	void set(VAL_T val, KEY_T key, Ts... args)
  {
	if( sizeof...(args) != DEPTH) {
	  std::cout << "Number of arguments does not match depth of nested map."
				<< std::endl;
	  std::exit(0);
	}
	internal_modifier_call(m[key], val, args...);
  }

  //Check whether an elements exists
  template <class ... Ts>
	bool exists(KEY_T key, Ts... args)
  {
	try {
	  (*this)(key, args...);
	}
	catch (std::out_of_range e) {
	  return false;
	}
	return true;
  }


 private:
  typename nested_map_def<KEY_T, VAL_T, DEPTH>::map_type m;

  //catch situations where entry does not exist
  template <class U>
	auto& catch_out_of_range(const U& map, KEY_T key) const {
	try {
	  return map.at(key);
	}
	catch (std::out_of_range e) {
	  std::cout << "The entry was not set (key = " << key << ")." << std::endl;
	  if(map.size() != 0) {
		  std::cout << "The following keys were already set:" << std::endl;
		  for (auto const &pair: map) {
			std::cout << "- " << pair.first << "\n";
		  }
	  }
	  else
		std::cout << "Currently no keys are defined for the offending map nesting level." << std::endl;
	  std::exit(0);
	}
  }

  //Read-only
  template <class U>
	const VAL_T& internal_read_only_call(const U& map, KEY_T key) const
	{
	  return catch_out_of_range(map, key);
	}
  template <class U, class... RestKeys>
	const VAL_T& internal_read_only_call(const U& map, KEY_T key, RestKeys... args) const
	{
	  return internal_read_only_call(catch_out_of_range(map, key), args...);
	}

  //Modifier
  template <class U>
	void internal_modifier_call(U& map, VAL_T val, KEY_T key)
	{
	  map[key] = val;
	}  
  template <class U, class... RestKeys>
	void internal_modifier_call(U& map, VAL_T val, KEY_T key, RestKeys... args)
  {
	internal_modifier_call(map[key], val, args...);
  }


};

#endif
