//
// Created by sho sumioka on 西暦 2019/10/29.
//

#ifndef YURLUNGUR_NATIVE_H
#define YURLUNGUR_NATIVE_H

//https://pybind11.readthedocs.io/en/stable/advanced/pycpp/index.html
// At beginning of file
# include <pybind11/eval.h>

// Evaluate in scope of main module
py::object scope = py::module::import("__main__").attr("__dict__");

// Evaluate an isolated expression
int result = py::eval("my_variable + 10", scope).cast<int>();

// Evaluate a sequence of statements
py::exec(
    "print('Hello')\n"
    "print('world!');",
    scope);

// Evaluate the statements in an separate Python file on disk
py::eval_file("script.py", scope);

#endif //YURLUNGUR_NATIVE_H
