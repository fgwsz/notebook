# 封装
```cpp
// Person.hpp
class Person{
public:
    ::std::string const& get_name(void)const;
    ::std::size_t get_age(void)const;
    void set_name(::std::string const& name);
    void set_age(::std::size_t age);
private:
    ::std::string name_;
    ::std::size_t age_;
};
```
```c
// Person.h
struct Person{
    void (*get_name)(struct Person const* self,string_t* ret);
    size_t (*get_age)(struct Person const* self);
    void (*set_name)(struct Person* self,string_t const* name);
    void (*set_age)(struct Person* self,size_t age);
};
struct PersonImpl{
    struct Person person;
    string_t name;
    size_t age;
};
extern struct Person* Person_new(void);
extern void PersonImpl_init(struct PersonImpl* self);
extern void Person_delete(struct Person* self);
// Person.c
static void Person_get_name(struct Person const* self,string_t* ret);
static size_t Person_get_age(struct Person const* self);
static void Person_set_name(struct Person* self,string_t const* name);
static void Person_set_age(struct Person* self,size_t age);
struct Person* Person_new(void){
    struct PersonImpl* ret=(struct PersonImpl*)malloc(sizeof(struct PersonImpl));
    PersonImpl_init(ret);
    return (struct Person*)ret;
}
void PersonImpl_init(struct PersonImpl* self){
    self->person.get_name=&Person_get_name;
    self->person.get_age=&Person_get_age;
    self->person.set_name=&Person_set_name;
    self->person.set_age=&Person_set_age;
    // ctor self->name
    // ctor self->age
}
void Person_delete(struct Person* self){
    if(NULL!=self){
        // dtor ((struct PersonImpl*)self)->name
        // dtor ((struct PersonImpl*)self)->age
        free((struct PersonImpl*)self);
    }
}
```
# 继承
```cpp
// Animal.hpp
class Animal{
public:
    size_t get_age(void)const;
private:
    size_t age;
};
// Dog.hpp
class Dog:public Animal{
public:
    void speak(void)const;
private:
    ::std::string speak_info_;
};
// Test.cpp
Animal* animal=new Dog();
animal->get_age();
dynamic_cast<Dog*>(animal)->speak();
```
```c
// Animal.h
struct Animal{
    void (*get_age)(struct Animal const* self);
};
struct AnimalImpl{
    struct Animal animal;
    size_t age;
};
extern struct Animal* Animal_new(void);
extern struct AnimalImpl_init(struct AnimalImpl* self);
// Dog.h
struct Dog{
    struct AnimalImpl base;
    void (*speak)(struct Dog const* self);
};
struct DogImpl{
    struct Dog dog;
    string_t speak_info;
};
extern struct Dog* Dog_new(void);
extern void DogImpl_init(struct DogImpl* self);
// Dog.c
static void Dog_speak(struct Dog* self);
struct Dog* Dog_new(void){
    struct DogImpl* ret=(struct DogImpl*)malloc(sizeof(struct DogImpl));
    DogImpl_init(ret);
    return (struct Dog*)ret;
}
void DogImpl_init(struct DogImpl* self){
    AnimalImpl_init(&(self->dog.base));
    self->dog.speak=&Dog_speak;
    // ctor self->dog.speak_info
}
// Test.c
struct Animal* animal=(struct Animal*)(Dog_new());
animal->get_age(animal);
struct Dog* dog=(struct Dog*)(animal);
dog->speak(dog);
```
# 多态
