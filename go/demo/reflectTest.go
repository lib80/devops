package main

import (
    "fmt"
    "reflect"
)

type Student struct {
    Name string
    Age int
    Grade int
    //id int
    Hobbies []string
}

func (std Student) Study(subject string) {
    fmt.Printf("[grade:%d][name:%s]在学习%v\n", std.Grade, std.Name, subject)
}

func (std Student) Examine() {
    fmt.Printf("[grade:%d][name:%s]在考试\n", std.Grade, std.Name)
}

func (std *Student) Excise() {
    fmt.Printf("[grade:%d][name:%s]在锻炼\n", std.Grade, std.Name)
}

func main() {
    std1 := Student{
        Name: "jerry",
        Age: 20,
        Grade: 2,
        //id: 1,
        Hobbies: []string{"sing", "badmiton"},
    }

    t := reflect.TypeOf(std1)
    v := reflect.ValueOf(std1)

    //探查字段
    for i := 0; i < t.NumField(); i++ {
        fmt.Printf("[第%v个字段][字段名:%v][字段类型:%v][字段值:%v]\n", i+1, t.Field(i).Name, t.Field(i).Type, v.Field(i).Interface())
    }

    //探查方法
    for i:= 0; i < t.NumMethod(); i++ {
        fmt.Printf("[方法名:%v][方法类型:%v]\n", t.Method(i).Name, t.Method(i).Type)
    }

    //调用带参数方法
    args := []reflect.Value{reflect.ValueOf("数学")}
    v.MethodByName("Study").Call(args)

    //调用不带参数方法
    args2 := []reflect.Value{}
    v.MethodByName("Examine").Call(args2)

    //修改字段值
    iv := reflect.ValueOf(&std1)
    iv.Elem().FieldByName("Age").SetInt(19)
    fmt.Println(std1.Age)
}
