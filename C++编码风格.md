# C++编码风格
## 缩进
缩进统一使用4个英文空格，不要使用`Tab`。  
设置文本编辑器自动把`Tab`转换为4个英文空格。
## 文件编码
文件编码统一使用`UTF8`编码，注意不要使用`UTF8 with BOM`。
## 行宽字符限制
每一行的字符宽度设置为80，超过80个字符宽度需要换行。
## 连续空行
不允许出现连续两行是空行。
## 文件名
所有文件名统一采用蛇形命名法。
## 宏
### 命名
```cpp
#define MACRO_EMPTY//宏采用大写字母+下划线分隔的形式
#define MACRO_FUNCTION(parameter_variable__)//宏函数参数采用蛇形命名法，然后尾部加上两个下划线`__`
```
### 分支缩进
```cpp
#ifndef COUNTER
    #define COUNTER 0
#else
    #undef COUNTER
    #define COUNTER 1
#endif
```
### 宏函数编写规范
```cpp
//没有返回值的宏函数
#define MACRO_NO_RETURN_FUNCTION(...) do{ \//注意这里是` \`，不要忘记这个空格
    ::std::cout<<#__VA_ARGS__<<"\n"; \
}while(0) \
//这一行是为了分隔，不要忘记
//带有返回值的宏函数
#define MACRO_FUNCTION(variable__) \
    (variable__) \//如果可能的话，把宏函数参数用`()`包裹一下再使用，同时注意：这里尾部没有`;`号，宏展开的最后尽量不要设置`;`号。
//这一行也是为了分隔，不要忘记
```
## 头文件
### 存放位置
统一存放在目录`project_name/include/`下。
### 防卫式保护
`mypro/include/base/hello.h`
```cpp
#ifndef MYPRO_BASE_HELLO_H//项目名/include/子目录名/文件名
#define MYPRO_BASE_HELLO_H//这里没有采用宏分支缩进，是为了保持头文件内部宏定义缩进格式的整洁性
//C++相关内容
#ifdef __cplusplus
    extern "C"{
#endif
//C语言相关内容
#ifdef __cplusplus
    }//extern "C"
#endif
//C++相关内容
#endif//MYPRO_BASE_HELLO_H
```
### 非标准扩展
`mypro/include/hello.hpp`
```cpp
#pragma once
```
### 选择方式
当需要和`C语言`兼容的头文件采用`.h`后缀名，并采用`防卫式保护`。  
当只使用`C++`的时候头文件采用`.hpp`后缀名，并使用`非标准扩展`。
## 模板
### 类型模板参数
```cpp
template<typename TypeParameter__>//普通类型参数
template<typename TI_TemplateInstanceTypeParameter__>//类模板实例化类型参数
```
### 变量模板参数
```cpp
template<int variable_parameter__>
```
### 模板模板参数
```cpp
template<template<typename...>typename T_TemplateParameter__>
```
### 类模板
命名方式同类。
### 函数模板
命名方式同函数。
### 模板参数列表缩进
以下使用类模板来举例，函数模板也遵循同样的方式。
```cpp
//模板参数列表小于行宽的话放在同一行
template<typename Type1__,typename Type2__>//此处换行
struct ClassTemplate1;
//模板参数列表大于行宽的话，每个参数单独放在一行
//第二个参数开始以`,`开头
template<
    typename Type1__
    ,typename Type2__
    ,typename Type3__
    ,typename Type4__
>//此处换行
struct ClassTemplate1;
template<typename Type__>
struct ClassTemplate2//此处换行
    <Type__,Type__>{//模板偏特化单独起一行，带缩进，此处换行
    //...
};
//模板偏特化参数列表大于行宽的话，每个参数需要换行
//第二个模板参数用`,`开头
template<typename Type__>
struct ClassTemplate3//此处换行
    <
        Type__[1]
        ,Type__[2]
        ,Type__[3]
        ,Type__[4]
    >{//此处换行
    //...
};
```
## 类/结构体/联合体/枚举
### 命名
```cpp
class MyClass;
struct MyStruct;
union MyUnion;
enum MyEnum;
enum class MyEnumClass;
```
统一使用大驼峰命名法。  
一些特殊情况如下：
```cpp
class ColorRGB;//对于单词缩写统一使用大写字母拼接的形式
template<typename TI_TypeList__>
class TypeList_At;//对于类模板的成员元函数使用类模板名_元函数名的形式
```
### 类空格/缩进
```cpp
class EmptyClass
{};//空类大括号在一行
class NoEmptyClass{
    //...
};
```
### 继承缩进
```cpp
class EmptyDerivedClass
    :public BaseClass1//存在父类`:`后需要换行
{};
class NoEmptyDerivedClass
    :public BaseClass1//每一个父类都需要换行
    ,protected BaseClass2
    ,private BaseClass3{
    //...
};
template<>
class MyClass
    <1,2,3>:public BaseClass1{//类模板实例化参数表小于行宽的话和父类放在一行
    //...
};
```
### 访问权限缩进
```cpp
class MyClass{
public:
protected:
private:
};
```
### 成员缩进
```cpp
class MyClass{
public:
    void member_function();
protected:
    static void static_member_function();
private:
    struct PrivateClass
    {};
};
```
## 变量
### 局部变量
```cpp
int local_variable;//蛇形命名法
```
### 成员变量
```cpp
int member_variable_;//蛇形命名法+尾部1个`_`
```
### 模板参数变量
```cpp
int template_parameter_variable__;//蛇形命名法+尾部2个`_`
```
### 枚举值
```cpp
enum JsonValueType{
    kUndefined,//`k`+大驼峰命名法
    kNull,
    kBoolean,
    kNumber,
    kString,
    kArray,
    kObject
};
```
## 函数
### 命名
```cpp
//普通函数采用蛇形命名法
void this_is_a_function();
//类构造/析构等特殊函数函数遵循类的命名方式
MyClass();
//函数参数的命名方式遵循局部变量的命名方式
void foo(::std::string const& c_str);
```
### 缩进
```cpp
//函数参数列表小于行宽的话放在同一行
//比较小的函数体（只有一行），也需要让`{}`换行。
void print_person_info(Person const& person){//此处换行
    ::std::cout<<person<<"\n";
}
//函数参数列表大于行宽的话，每个参数起一行，第二行开始用`,`开始
void print_person_info(
    ::std::string_view const& person_name
    ,::std::size_t person_age
){//此处换行
    ::std::cout<<person_name<<","<<person_age<<"\n";
}
//空函数体也需要让`{}`换行。
MyClass()noexcept
    :name_("Tom")//使用初始化列表每个参数都需要换行，`:`/`,`开始
    ,age_(20)
{}//空函数体在一行
MyClass(MyClass)noexcept
    :MyClass(){//调用其他的构造函数需要换行，`:`开始
    do_something();
}
```
### 类型修饰符
`&`/`*`均采用左结合的方式靠近附近的非空字符。  
`const`/`votaile`均放置在类型名的后面，保持类型名清晰。
```cpp
int const ic_number;
char const& cref_character;
char const volatile* const c_str;
```
## 运算符
如无必要，运算符的左右不使用空格/换行。  
必要的情况如下：
### 不使用空格会造成语法错误/语义歧义的情况
```cpp
//                      这个空格是必要的。
//                      |
//                      v
for(auto const& element: ::std::vector<int>{1,2,3})
```
### 三目运算符来模拟分支结构的情况
```cpp
int max(int number1,int number2){
    //这里换行是为了代码可读性，让逻辑更清晰
    return number1>number2
        ?number1
        :number2;
}
```
## 命名空间
```cpp
//命名空间采用蛇形命名法
namespace this_is_a_namespace{
//命名空间内部不缩进
void test();
}//namespace this_is_a_namespace
```
## 类型别名
类型别名/别名模板统一采用蛇形命名法。
```cpp
using size_type=unsigned long long;
template<typename Type1__,typename Type2__>
struct IsSame{
    using type=false_type;
};
template<typename Type__>
struct IsSame
    <Type__,Type__>{
    using type=true_type;
};
template<typename Type__>
using is_same_t=typename IsSame<Type__>::type;
```
## 逻辑结构
### if
```cpp
if(){//即使只有一行语句也要换行
    //...
}
//...
if(){
    //...
}else if(){
    //...
}else{
    //...
}
//...
//条件语句大于行宽的时候，需要换行
//每个独立逻辑语句起一行，第二行开始使用逻辑运算符开头
if(
    (value>0||value<1000)
    &&value%3==0
){
    //...
}
```
### while/for
while/for遵循if的规则。
### switch
```cpp
switch(number){
    case 0:{
        break;
    }
    case 1:{
        break;
    }
    case 2:{
        break;
    }
    case 3:{
        break;
    }
    default:{
        //...
    }
}
```